"""Orchestrator: runs the agents in order for one transcript.

Steps so far:
  1. Guardrails  - mask personal data, check injection / topic / risk. May stop the run.
  2. PRD Writer  - writes the PRD from the cleaned transcript and the guardrail notes.

Each run writes:
  data/outputs/<transcript-name>/guardrails.json
  data/outputs/<transcript-name>/PRD.md          (unless guardrails blocked the run)
  data/metrics/<run-id>.json                     (per-step model, prompt version, tokens, cost, time)

Usage:
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --dry-run
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --skip-guardrail-review
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from evals.check_structure import check_prd
from packages.agents.guardrails import agent as guardrails
from packages.agents.prd_writer import agent as prd_writer

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = REPO_ROOT / "data" / "outputs"
METRICS_DIR = REPO_ROOT / "data" / "metrics"


def _timed(fn, *args, **kwargs):
    started = time.monotonic()
    result = fn(*args, **kwargs)
    return result, round(time.monotonic() - started, 2)


def run(
    transcript_path: Path,
    client=None,
    outputs_dir: Path = OUTPUTS_DIR,
    metrics_dir: Path = METRICS_DIR,
    guardrail_review: bool = True,
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

    # Step 2: PRD Writer (only if guardrails did not block)
    if report.decision != "block":
        result, p_time = _timed(
            prd_writer.write_prd, report.sanitized_transcript, client=client, notes=report.notes_for_prd
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
    print(f"System prompt:  {len(system_prompt):,} characters")
    print(f"User message:   {len(user_message):,} characters")
    print("\n--- user message to PRD Writer ---\n" + user_message)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Turn a transcript into a PRD.md")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="show the prompt without calling the API")
    parser.add_argument("--skip-guardrail-review", action="store_true",
                        help="run only the rule-based guardrails (skip the Claude review)")
    args = parser.parse_args(argv)

    if args.dry_run:
        dry_run(args.transcript)
        return 0

    try:
        metrics = run(args.transcript, guardrail_review=not args.skip_guardrail_review)
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
