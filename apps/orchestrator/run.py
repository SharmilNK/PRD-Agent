"""Orchestrator: runs the agents in order for one transcript.

Steps so far:
  1. Guardrails  - mask personal data, check injection / topic / risk. May stop the run.
  2. Research    - Market, Standards and Tech agents search the web (in parallel); sources are graded.
  3. PRD Writer  - writes the PRD from the cleaned transcript, guardrail notes and research brief.

Each run writes:
  data/outputs/<transcript-name>/guardrails.json
  data/outputs/<transcript-name>/research/<agent>.json and research_brief.md
  data/outputs/<transcript-name>/PRD.md          (unless guardrails blocked the run)
  data/metrics/<run-id>.json                     (per-step model, prompt version, tokens, cost, time)

Usage:
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --dry-run
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-guardrail-review
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-research
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from evals.check_structure import check_prd
from packages.agents.common import WEB_SEARCH_USD
from packages.agents.guardrails import agent as guardrails
from packages.agents.prd_writer import agent as prd_writer
from packages.agents.research import agent as research
from packages.agents.research.config import AGENTS as RESEARCH_AGENTS

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = REPO_ROOT / "data" / "outputs"
METRICS_DIR = REPO_ROOT / "data" / "metrics"


def _timed(fn, *args, **kwargs):
    started = time.monotonic()
    result = fn(*args, **kwargs)
    return result, round(time.monotonic() - started, 2)


def _research_one(kind: str, transcript: str, client) -> tuple[str, object, float]:
    """Run one research agent. A failure is returned, not raised, so the other agents still count."""
    started = time.monotonic()
    try:
        result = research.run_research(kind, transcript, client=client)
    except ImportError:
        raise
    except Exception as e:  # noqa: BLE001 - one failed agent must not stop the run
        result = e
    return kind, result, round(time.monotonic() - started, 2)


def run_research_step(transcript: str, client, out_dir: Path) -> tuple[list, dict, list[dict]]:
    """Run all research agents in parallel. Returns (results, failures, metric steps)."""
    with ThreadPoolExecutor(max_workers=len(RESEARCH_AGENTS)) as pool:
        outcomes = list(pool.map(lambda k: _research_one(k, transcript, client), RESEARCH_AGENTS))

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


def run(
    transcript_path: Path,
    client=None,
    outputs_dir: Path = OUTPUTS_DIR,
    metrics_dir: Path = METRICS_DIR,
    guardrail_review: bool = True,
    do_research: bool = True,
) -> dict:
    transcript = transcript_path.read_text()
    name = transcript_path.stem
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{name}"
    out_dir = outputs_dir / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Guardrails
    report, g_time = _timed(guardrails.run_guardrails, transcript, client=client, use_llm=guardrail_review)
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
        brief = ""
        if do_research:
            _, failed, research_steps = run_research_step(report.sanitized_transcript, client, out_dir)
            steps.extend(research_steps)
            metrics["research_failed"] = failed
            brief = (out_dir / "research_brief.md").read_text()

        # Step 3: PRD Writer
        result, p_time = _timed(
            prd_writer.write_prd, report.sanitized_transcript, client=client,
            notes=report.notes_for_prd, research=brief,
        )
        prd_path = out_dir / "PRD.md"
        prd_path.write_text(result.markdown)
        steps.append({
            "agent": "prd_writer",
            "model": result.model,
            "prompt_version": result.prompt_version,
            "stop_reason": result.stop_reason,
            "usage": result.usage,
            "cost_usd": result.cost_usd,
            "duration_s": p_time,
        })
        metrics["output"] = str(prd_path)
        metrics["structure_check"] = check_prd(result.markdown)

    metrics["total_cost_usd"] = round(sum(s["cost_usd"] for s in steps), 6)
    metrics["total_duration_s"] = round(sum(s["duration_s"] for s in steps), 2)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / f"{run_id}.json").write_text(json.dumps(metrics, indent=2) + "\n")
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
    print(f"System prompt:  {len(system_prompt):,} characters")
    print(f"User message:   {len(user_message):,} characters")
    print("\n--- user message to PRD Writer ---\n" + user_message)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Turn a transcript into a PRD.md")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="show the prompt without calling the API")
    parser.add_argument("--skip-guardrail-review", action="store_true",
                        help="run only the rule-based guardrails (skip the Claude review)")
    parser.add_argument("--skip-research", action="store_true", help="skip the web research agents")
    args = parser.parse_args(argv)

    if args.dry_run:
        dry_run(args.transcript)
        return 0

    try:
        metrics = run(args.transcript, guardrail_review=not args.skip_guardrail_review,
                      do_research=not args.skip_research)
    except ImportError:
        print("The anthropic package is missing. Run: pip install -r requirements.txt", file=sys.stderr)
        return 1
    except (guardrails.GuardrailsError, prd_writer.PRDWriterError) as e:
        print(f"Run failed: {e}", file=sys.stderr)
        return 1

    g = metrics["guardrails"]
    print(f"Guardrails:      {g['decision'].upper()}")
    for reason in g["reasons"]:
        print(f"  - {reason}")
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

    check = metrics["structure_check"]
    print(f"PRD written:     {metrics['output']}")
    print(f"Cost:            ${metrics['total_cost_usd']:.4f}   Time: {metrics['total_duration_s']}s")
    print(f"Structure check: {'PASS' if check['passed'] else 'FAIL'} "
          f"({check['sections_found']}/{check['sections_expected']} sections)")
    if check["missing_sections"]:
        print("Missing:         " + ", ".join(check["missing_sections"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
