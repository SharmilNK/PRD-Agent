"""Orchestrator: runs the agents in order for one transcript.

Phase 1 has one step: PRD Writer. Each run writes:
  data/outputs/<transcript-name>/PRD.md
  data/metrics/<run-id>.json   (model, prompt version, tokens, cost, time, structure check)

Usage:
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md
    python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from evals.check_structure import check_prd
from packages.agents.prd_writer import agent as prd_writer

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = REPO_ROOT / "data" / "outputs"
METRICS_DIR = REPO_ROOT / "data" / "metrics"


def run(transcript_path: Path, client=None, outputs_dir: Path = OUTPUTS_DIR, metrics_dir: Path = METRICS_DIR) -> dict:
    transcript = transcript_path.read_text()
    name = transcript_path.stem
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{name}"

    started = time.monotonic()
    result = prd_writer.write_prd(transcript, client=client)
    duration_s = round(time.monotonic() - started, 2)

    prd_path = outputs_dir / name / "PRD.md"
    prd_path.parent.mkdir(parents=True, exist_ok=True)
    prd_path.write_text(result.markdown)

    metrics = {
        "run_id": run_id,
        "transcript": str(transcript_path),
        "output": str(prd_path),
        "steps": [
            {
                "agent": "prd_writer",
                "model": result.model,
                "prompt_version": result.prompt_version,
                "stop_reason": result.stop_reason,
                "usage": result.usage,
                "cost_usd": result.cost_usd,
                "duration_s": duration_s,
            }
        ],
        "total_cost_usd": result.cost_usd,
        "total_duration_s": duration_s,
        "structure_check": check_prd(result.markdown),
    }
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / f"{run_id}.json").write_text(json.dumps(metrics, indent=2) + "\n")
    return metrics


def dry_run(transcript_path: Path) -> None:
    """Show what would be sent to Claude, without calling the API."""
    system_prompt = prd_writer.build_system_prompt()
    user_message = prd_writer.build_user_message(transcript_path.read_text())
    print(f"Model:          {prd_writer.MODEL} (effort={prd_writer.EFFORT})")
    print(f"Prompt version: {prd_writer.prompt_version(system_prompt)}")
    print(f"System prompt:  {len(system_prompt):,} characters")
    print(f"User message:   {len(user_message):,} characters")
    print("\n--- user message ---\n" + user_message)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Turn a transcript into a PRD.md")
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="show the prompt without calling the API")
    args = parser.parse_args(argv)

    if args.dry_run:
        dry_run(args.transcript)
        return 0

    try:
        metrics = run(args.transcript)
    except ImportError:
        print("The anthropic package is missing. Run: pip install -r requirements.txt", file=sys.stderr)
        return 1
    except prd_writer.PRDWriterError as e:
        print(f"PRD Writer failed: {e}", file=sys.stderr)
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
