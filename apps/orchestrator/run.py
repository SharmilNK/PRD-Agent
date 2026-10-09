"""Orchestrator: runs the agents in order for one transcript.

Steps so far:
  1. Guardrails  - mask personal data, check injection / topic / risk. May stop the run.
  2. Research    - Market, Standards and Tech agents search the web (in parallel); sources are graded.
  3. Debate      - Advocate (full context) pitches; Skeptic (pitch only) challenges for 2 rounds.
  4. Scorer      - GUCCI + scorecard with frameworks and evidence; code computes Go / Pivot / No-Go.
  5. PRD Writer  - writes the PRD from the cleaned transcript, guardrail notes, research and evaluation.
  6. Checks      - free quality checks: structure, no invented links, scores match, readability.
  7. Reviewer    - opens up to 5 cited links to confirm quotes; reviews the PRD on evals/rubric.json.
  8. Revision    - if the Reviewer or checks found serious problems, the PRD Writer fixes them once.

Each run writes:
  data/outputs/<transcript-name>/guardrails.json
  data/outputs/<transcript-name>/research/<agent>.json and research_brief.md
  data/outputs/<transcript-name>/debate.md and scorecard.json
  data/outputs/<transcript-name>/review.json, quality.json (and PRD.draft.md if revised)
  data/outputs/<transcript-name>/PRD.md          (unless guardrails blocked the run)
  data/metrics/<run-id>.json                     (per-step model, prompt version, tokens, cost, time)

Usage:
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --dry-run
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-guardrail-review
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-research
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-debate
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-review --no-revise
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --github-issues
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --alert

After every run, the run is added to data/metrics/index.json and data/decisions/RUN_LOG.md.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from apps.orchestrator.publish import publish, read_prd
from evals.quality_checks import run_checks
from packages.agents.common import WEB_SEARCH_USD
from packages.agents.debate import agent as debate
from packages.agents.guardrails import agent as guardrails
from packages.agents.prd_writer import agent as prd_writer
from packages.agents.research import agent as research
from packages.agents.research.config import AGENTS as RESEARCH_AGENTS
from packages.agents.reviewer import agent as reviewer
from packages.agents.scorer import agent as scorer
from packages.observability.tracing import Tracer, run_in_context, span

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = REPO_ROOT / "data" / "outputs"
METRICS_DIR = REPO_ROOT / "data" / "metrics"


def _writer_step(name: str, result, duration: float) -> dict:
    return {"agent": name, "model": result.model, "prompt_version": result.prompt_version,
            "stop_reason": result.stop_reason, "usage": result.usage, "cost_usd": result.cost_usd,
            "duration_s": duration}


def _timed(name: str, fn, *args, **kwargs):
    """Run one step inside a trace span and return (result, seconds)."""
    started = time.monotonic()
    with span(f"step:{name}"):
        result = fn(*args, **kwargs)
    return result, round(time.monotonic() - started, 2)


class Budget:
    """Spending limit for one run. Once reached, optional steps are skipped (the PRD is still written)."""

    def __init__(self, limit_usd: float | None):
        self.limit = limit_usd
        self.skipped: list[str] = []

    def allows(self, step: str, steps: list[dict]) -> bool:
        if self.limit is None or sum(s["cost_usd"] for s in steps) < self.limit:
            return True
        self.skipped.append(step)
        return False


def default_budget() -> float | None:
    """PRD_AGENT_MAX_COST_USD, default $10 (also when empty). Set it to 0 or 'none' for no limit."""
    raw = (os.environ.get("PRD_AGENT_MAX_COST_USD") or "10").strip().lower()
    return None if raw in ("0", "none") else float(raw)


def _research_one(kind: str, transcript: str, client) -> tuple[str, object, float]:
    """Run one research agent. A failure is returned, not raised, so the other agents still count."""
    started = time.monotonic()
    try:
        with span(f"step:research:{kind}"):
            result = research.run_research(kind, transcript, client=client)
    except ImportError:
        raise
    except Exception as e:  # noqa: BLE001 - one failed agent must not stop the run
        result = e
    return kind, result, round(time.monotonic() - started, 2)


def run_research_step(transcript: str, client, out_dir: Path) -> tuple[list, dict, list[dict]]:
    """Run all research agents in parallel. Returns (results, failures, metric steps)."""
    with ThreadPoolExecutor(max_workers=len(RESEARCH_AGENTS)) as pool:
        # run_in_context: each thread's spans join this run's trace.
        jobs = [run_in_context(_research_one, k, transcript, client) for k in RESEARCH_AGENTS]
        outcomes = [f.result() for f in [pool.submit(job) for job in jobs]]

    research_dir = out_dir / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    results, failed, steps = [], {}, []
    for kind, result, duration in outcomes:
        if isinstance(result, Exception):
            failed[kind] = f"{type(result).__name__}: {result}"
            steps.append({"agent": f"research:{kind}", "error": failed[kind], "cost_usd": 0.0, "duration_s": duration})
            continue
        results.append(result)
        (research_dir / f"{kind}.json").write_text(json.dumps(result.to_json(), indent=2) + "\n")
        steps.append({
            "agent": f"research:{kind}",
            "model": result.model,
            "searches": result.searches,
            "claims_accepted": len(result.accepted),
            "claims_rejected": len(result.rejected),
            "grades": {g: sum(c["checks"]["grade"] == g for c in result.accepted) for g in "ABCD"},
            "usage": result.usage,
            "cost_usd": result.cost_usd,
            "duration_s": duration,
        })
    brief = research.brief_for_prd(results, failed)
    (out_dir / "research_brief.md").write_text(brief + "\n")
    return results, failed, steps


def run_evaluation_step(transcript: str, brief: str, notes: list[str], client, out_dir: Path) -> tuple[str, list[dict], dict]:
    """Debate, then Scorer. Returns (evaluation text for the PRD Writer, metric steps, summary).

    A failure is recorded and the run continues; the PRD Writer then scores on its own.
    """
    steps, summary = [], {}
    try:
        result, d_time = _timed("debate", debate.run_debate, transcript, research=brief, notes=notes, client=client)
    except ImportError:
        raise
    except Exception as e:  # noqa: BLE001
        error = f"{type(e).__name__}: {e}"
        return "", [{"agent": "debate", "error": error, "cost_usd": 0.0, "duration_s": 0.0}], {"error": error}

    debate_md = result.transcript_md()
    (out_dir / "debate.md").write_text(debate_md)
    steps.append({"agent": "debate", "model": result.model, "calls": result.calls, "rounds": debate.ROUNDS,
                  "usage": result.usage, "cost_usd": result.cost_usd, "duration_s": d_time})
    try:
        scores, s_time = _timed("scorer", scorer.run_scorer, transcript, research=brief, debate_md=debate_md, client=client)
    except ImportError:
        raise
    except Exception as e:  # noqa: BLE001
        error = f"{type(e).__name__}: {e}"
        steps.append({"agent": "scorer", "error": error, "cost_usd": 0.0, "duration_s": 0.0})
        closing = f"Skeptic closing statement (Scorer failed, score the idea yourself):\n{result.closing}"
        return closing, steps, {"error": error}

    (out_dir / "scorecard.json").write_text(json.dumps(scores.to_json(), indent=2) + "\n")
    steps.append({"agent": "scorer", "model": scores.model, "verdict": scores.verdict, "average": scores.average,
                  "issues": len(scores.issues), "usage": scores.usage, "cost_usd": scores.cost_usd,
                  "duration_s": s_time})
    summary = {"verdict": scores.verdict, "average": scores.average,
               "scores": {k: v["score"] for k, v in scores.scores.items()}, "issues": scores.issues}
    evaluation = scores.brief_for_prd(scorer.load_scorecard()) + "\n\nSkeptic closing statement:\n" + result.closing
    return evaluation, steps, summary


def run(
    transcript_path: Path,
    client=None,
    outputs_dir: Path = OUTPUTS_DIR,
    metrics_dir: Path = METRICS_DIR,
    guardrail_review: bool = True,
    do_research: bool = True,
    do_debate: bool = True,
    do_review: bool = True,
    revise: bool = True,
    budget_usd: float | None | str = "default",
    traces_dir: Path | None = None,
) -> dict:
    """Run the pipeline with tracing and a cost budget. Writes the PRD, metrics and the trace."""
    name = transcript_path.stem
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{name}"
    budget = Budget(default_budget() if budget_usd == "default" else budget_usd)
    tracer = Tracer(run_id)
    with tracer.active(), span("run", transcript=name) as root:
        metrics = _pipeline(transcript_path, run_id, budget, client, outputs_dir, guardrail_review,
                            do_research, do_debate, do_review, revise)
        root.set(status=metrics["status"], cost_usd=metrics["total_cost_usd"])

    traces_dir = traces_dir or metrics_dir.parent / "traces"
    trace_path = tracer.save(traces_dir / f"{run_id}.jsonl")
    metrics["trace"] = {"file": str(trace_path), **tracer.summary()}
    metrics["budget"] = {"limit_usd": budget.limit, "spent_usd": metrics["total_cost_usd"], "skipped": budget.skipped}
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / f"{run_id}.json").write_text(json.dumps(metrics, indent=2) + "\n")
    return metrics


def _pipeline(transcript_path: Path, run_id: str, budget: Budget, client, outputs_dir: Path,
              guardrail_review: bool, do_research: bool, do_debate: bool, do_review: bool, revise: bool) -> dict:
    transcript = transcript_path.read_text()
    name = transcript_path.stem
    out_dir = outputs_dir / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Guardrails
    report, g_time = _timed("guardrails", guardrails.run_guardrails, transcript, client=client, use_llm=guardrail_review)
    (out_dir / "guardrails.json").write_text(json.dumps(report.to_json(), indent=2) + "\n")
    steps = [{
        "agent": "guardrails",
        "decision": report.decision,
        "model": report.model,
        "usage": report.usage,
        "cost_usd": report.cost_usd,
        "duration_s": g_time,
    }]
    metrics = {
        "run_id": run_id,
        "transcript": str(transcript_path),
        "status": "blocked" if report.decision == "block" else "completed",
        "guardrails": {"decision": report.decision, "reasons": report.reasons},
        "steps": steps,
    }

    if report.decision != "block":
        # Step 2: Research
        brief, research_results = "", []
        if do_research and budget.allows("research", steps):
            with span("step:research"):
                research_results, failed, research_steps = run_research_step(report.sanitized_transcript, client, out_dir)
            steps.extend(research_steps)
            metrics["research_failed"] = failed
            brief = (out_dir / "research_brief.md").read_text()

        # Steps 3-4: Debate and Scorer
        evaluation = ""
        if do_debate and budget.allows("debate", steps):
            evaluation, eval_steps, metrics["evaluation"] = run_evaluation_step(
                report.sanitized_transcript, brief, report.notes_for_prd, client, out_dir
            )
            steps.extend(eval_steps)

        # Step 5: PRD Writer
        result, p_time = _timed(
            "prd_writer", prd_writer.write_prd, report.sanitized_transcript, client=client,
            notes=report.notes_for_prd, research=brief, evaluation=evaluation,
        )
        prd_path = out_dir / "PRD.md"
        prd_path.write_text(result.markdown)
        steps.append(_writer_step("prd_writer", result, p_time))
        metrics["output"] = str(prd_path)

        # Step 6: free quality checks
        claims = [c for r in research_results for c in r.accepted]
        allowed = {c["url"] for c in claims}
        card_path = out_dir / "scorecard.json"
        card = json.loads(card_path.read_text()) if do_debate and card_path.exists() else None
        names = {c["id"]: c["name"] for c in scorer.load_scorecard()["criteria"]}
        quality = run_checks(result.markdown, allowed, card, names)
        prd = result.markdown

        # Step 7: Reviewer
        review = None
        if do_review and budget.allows("reviewer", steps):
            try:
                review, r_time = _timed("reviewer", reviewer.review_prd, prd, evaluation=evaluation, research=brief,
                                        quality=quality, claims=claims, client=client)
            except ImportError:
                raise
            except Exception as e:  # noqa: BLE001 - a failed review must not lose the PRD
                metrics["review"] = {"error": f"{type(e).__name__}: {e}"}
                steps.append({"agent": "reviewer", "error": metrics["review"]["error"], "cost_usd": 0.0, "duration_s": 0.0})
            else:
                (out_dir / "review.json").write_text(json.dumps(review.to_json(), indent=2) + "\n")
                statuses = [l["status"] for l in review.link_checks]
                metrics["review"] = {
                    "counts": review.to_json()["counts"],
                    "rubric_average": review.rubric_average,
                    "links_checked": len(statuses),
                    "links_confirmed": statuses.count("confirmed"),
                    "links_not_found": statuses.count("not_found"),
                }
                steps.append({"agent": "reviewer", "model": review.model, "usage": review.usage,
                              "cost_usd": review.cost_usd, "duration_s": r_time})

        # Step 8: one revision if needed
        metrics["revised"] = False
        if revise and ((review and review.needs_revision) or not quality["passed"]) \
                and budget.allows("revision", steps):
            feedback = reviewer.revision_feedback(review, quality)
            try:
                revised, v_time = _timed(
                    "prd_writer:revision", prd_writer.write_prd, report.sanitized_transcript, client=client, notes=report.notes_for_prd,
                    research=brief, evaluation=evaluation, draft=prd, feedback=feedback,
                )
            except ImportError:
                raise
            except Exception as e:  # noqa: BLE001 - keep the draft if the revision fails
                metrics["revision_error"] = f"{type(e).__name__}: {e}"
                steps.append({"agent": "prd_writer:revision", "error": metrics["revision_error"],
                              "cost_usd": 0.0, "duration_s": 0.0})
            else:
                (out_dir / "PRD.draft.md").write_text(prd)
                prd = revised.markdown
                prd_path.write_text(prd)
                steps.append(_writer_step("prd_writer:revision", revised, v_time))
                metrics["revised"] = True
                metrics["quality_before_revision"] = {k: quality[k]["passed"] for k in ("structure", "links", "scores")}
                quality = run_checks(prd, allowed, card, names)

        (out_dir / "quality.json").write_text(json.dumps(quality, indent=2) + "\n")
        metrics["quality"] = quality
        metrics["structure_check"] = quality["structure"]
        pass_average = reviewer.load_rubric()["pass_average"]
        metrics["quality_gate"] = "pass" if quality["passed"] and (
            review is None or review.rubric_average >= pass_average) else "fail"

    metrics["total_cost_usd"] = round(sum(s["cost_usd"] for s in steps), 6)
    metrics["total_duration_s"] = round(sum(s["duration_s"] for s in steps), 2)
    return metrics


def dry_run(transcript_path: Path) -> None:
    """Show what would happen, without calling the API (only the free rule-based guardrails run)."""
    report = guardrails.run_guardrails(transcript_path.read_text(), use_llm=False)
    system_prompt = prd_writer.build_system_prompt()
    user_message = prd_writer.build_user_message(report.sanitized_transcript, report.notes_for_prd)
    print(f"Guardrails (rules only): {report.decision}")
    for reason in report.reasons:
        print(f"  - {reason}")
    print(f"Model:          {prd_writer.MODEL} (PRD effort={prd_writer.EFFORT}, guardrails effort={guardrails.EFFORT})")
    print(f"Prompt version: {prd_writer.prompt_version(system_prompt)}")
    print("Research agents (in parallel):")
    for kind, cfg in RESEARCH_AGENTS.items():
        sites = f"{len(cfg['allowed_domains'])} official sites only" if cfg["allowed_domains"] else "open web, graded"
        print(f"  - {kind}: up to {cfg['max_searches']} searches, {sites}")
    max_search_cost = sum(c["max_searches"] for c in RESEARCH_AGENTS.values()) * WEB_SEARCH_USD
    print(f"  Max search cost: ${max_search_cost:.2f} (plus tokens)")
    print(f"Debate:         {debate.ROUNDS} rounds, {2 * debate.ROUNDS + 2} calls "
          "(Advocate has full context; Skeptic sees only the pitch)")
    print(f"Scorer:         GUCCI + {len(scorer.load_scorecard()['criteria'])} criteria; verdict computed by code")
    print(f"Reviewer:       opens up to {reviewer.MAX_LINKS} cited links; scores on "
          f"{len(reviewer.load_rubric()['criteria'])} rubric criteria; one revision if serious problems")
    print(f"System prompt:  {len(system_prompt):,} characters")
    print(f"User message:   {len(user_message):,} characters")
    print("\n--- user message to PRD Writer ---\n" + user_message)


def _print_github(gh: dict) -> None:
    if "created" in gh:
        print(f"GitHub issues:   {len(gh['created'])} created, {len(gh['commented'])} updated, "
              f"{len(gh['closed'])} closed")
    elif "error" in gh:
        print(f"GitHub issues:   FAILED - {gh['error']} (plan saved to issues.plan.json)")
    else:
        note = f" ({gh['skipped']})" if "skipped" in gh else ""
        print(f"GitHub issues:   {gh['planned']} planned, not sent{note}; see issues.plan.json")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Turn a transcript into a PRD.md")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="show the prompt without calling the API")
    parser.add_argument("--skip-guardrail-review", action="store_true",
                        help="run only the rule-based guardrails (skip the Claude review)")
    parser.add_argument("--skip-research", action="store_true", help="skip the web research agents")
    parser.add_argument("--skip-debate", action="store_true", help="skip the Advocate/Skeptic debate and Scorer")
    parser.add_argument("--skip-review", action="store_true", help="skip the Reviewer (free checks still run)")
    parser.add_argument("--no-revise", action="store_true", help="never run the revision pass")
    parser.add_argument("--github-issues", action="store_true",
                        help="create/update GitHub issues (needs GITHUB_TOKEN and GITHUB_REPOSITORY)")
    parser.add_argument("--budget", type=float, default=None,
                        help="max cost in USD for this run (default: PRD_AGENT_MAX_COST_USD or 10); "
                             "optional steps are skipped once it is reached")
    parser.add_argument("--alert", action="store_true",
                        help="email a Gmail alert if the PRD is new/updated or the run had problems")
    args = parser.parse_args(argv)

    if args.dry_run:
        dry_run(args.transcript)
        return 0

    old_prd = read_prd(OUTPUTS_DIR, args.transcript)
    try:
        metrics = run(args.transcript, guardrail_review=not args.skip_guardrail_review,
                      do_research=not args.skip_research, do_debate=not args.skip_debate,
                      do_review=not args.skip_review, revise=not args.no_revise,
                      budget_usd="default" if args.budget is None else args.budget)
    except ImportError:
        print("The anthropic package is missing. Run: pip install -r requirements.txt", file=sys.stderr)
        return 1
    except (guardrails.GuardrailsError, prd_writer.PRDWriterError) as e:
        print(f"Run failed: {e}", file=sys.stderr)
        return 1

    gh = publish(metrics, OUTPUTS_DIR, METRICS_DIR, github=args.github_issues, alert=args.alert, old_prd=old_prd)

    g = metrics["guardrails"]
    print(f"Guardrails:      {g['decision'].upper()}")
    for reason in g["reasons"]:
        print(f"  - {reason}")
    _print_github(gh)
    if "alert" in metrics:
        a = metrics["alert"]
        print(f"Gmail alert:     {'sent' if a['sent'] else 'not sent'}"
              + (f" ({', '.join(a['events'])})" if a["events"] else "") + (f" - {a['reason']}" if not a["sent"] else ""))
    if metrics["status"] == "blocked":
        print("Run stopped by guardrails. See data/outputs/<name>/guardrails.json")
        return 1

    for step in metrics["steps"]:
        if step["agent"].startswith("research:"):
            if "error" in step:
                print(f"{step['agent']:<17}FAILED - {step['error']}")
            else:
                g = step["grades"]
                print(f"{step['agent']:<17}{step['searches']} searches, {step['claims_accepted']} claims kept "
                      f"(A:{g['A']} B:{g['B']} C:{g['C']} D:{g['D']}), {step['claims_rejected']} rejected")

    ev = metrics.get("evaluation")
    if ev and "error" in ev:
        print(f"Debate/Scorer:   FAILED - {ev['error']}")
    elif ev:
        print(f"Verdict:         {ev['verdict'].upper().replace('_', '-')} (average {ev['average']}/5)")
        if ev["issues"]:
            print(f"Scoring issues:  {len(ev['issues'])} (see scorecard.json)")

    rv = metrics.get("review")
    if rv and "error" in rv:
        print(f"Reviewer:        FAILED - {rv['error']}")
    elif rv:
        c = rv["counts"]
        print(f"Reviewer:        {c['critical']} critical, {c['major']} major, {c['minor']} minor; "
              f"rubric {rv['rubric_average']}/5; links confirmed {rv['links_confirmed']}/{rv['links_checked']}")
    if metrics["revised"]:
        print("Revision:        PRD revised once (draft kept as PRD.draft.md)")

    q = metrics["quality"]
    s = q["structure"]
    print(f"PRD written:     {metrics['output']}")
    print(f"Cost:            ${metrics['total_cost_usd']:.4f}   Time: {metrics['total_duration_s']}s")
    print(f"Checks:          structure {s['sections_found']}/{s['sections_expected']}, "
          f"unknown links {len(q['links']['unknown_links'])}, score mismatches {len(q['scores']['mismatches'])}, "
          f"avg sentence {q['readability']['avg_sentence_words']} words")
    print(f"Quality gate:    {metrics['quality_gate'].upper()}")
    b, t = metrics["budget"], metrics["trace"]
    if b["skipped"]:
        print(f"Budget:          ${b['limit_usd']:.2f} reached - skipped: {', '.join(b['skipped'])}")
    print(f"Trace:           {t['llm_calls']} Claude calls, cache hit {t['cache_hit_rate']:.0%}, {t['file']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
