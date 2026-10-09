"""Entry point for the GitHub Action: run PRD-Agent on new or changed transcripts.

Reads (from environment variables, set by the workflow):
  INPUT_TRANSCRIPT   one transcript path, when the workflow is started by hand
  BEFORE_SHA, AFTER_SHA   the pushed commit range, when started by a push

Only files under data/transcripts/ ending in .md are ever run.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from apps.orchestrator import run as orchestrator
from apps.orchestrator.publish import publish, read_prd

REPO_ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPTS = REPO_ROOT / "data" / "transcripts"
ZERO_SHA = "0" * 40


def is_transcript(path: str) -> bool:
    p = (REPO_ROOT / path).resolve()
    return p.suffix == ".md" and p.parent == TRANSCRIPTS.resolve() and p.is_file()


def changed_transcripts(before: str, after: str) -> list[str]:
    if not before or before == ZERO_SHA:
        cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "--diff-filter=AM", after]
    else:
        cmd = ["git", "diff", "--name-only", "--diff-filter=AM", before, after]
    out = subprocess.run(cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True).stdout
    return sorted({line for line in out.splitlines() if line.startswith("data/transcripts/") and is_transcript(line)})


def pick_transcripts(env: dict) -> list[str]:
    manual = env.get("INPUT_TRANSCRIPT", "").strip()
    if manual:
        if not is_transcript(manual):
            raise SystemExit(f"Not a transcript under data/transcripts/: {manual!r}")
        return [manual]
    return changed_transcripts(env.get("BEFORE_SHA", ""), env.get("AFTER_SHA", "HEAD"))


def main() -> int:
    paths = pick_transcripts(dict(os.environ))
    if not paths:
        print("No new or changed transcripts.")
        return 0
    failed = 0
    for path in paths:
        print(f"=== {path}", flush=True)
        old_prd = read_prd(orchestrator.OUTPUTS_DIR, REPO_ROOT / path)
        try:
            metrics = orchestrator.run(REPO_ROOT / path)
        except Exception as e:  # noqa: BLE001 - keep going with the other transcripts
            print(f"Run failed: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
            failed += 1
            continue
        info = publish(metrics, orchestrator.OUTPUTS_DIR, orchestrator.METRICS_DIR, github=True,
                       alert=True, old_prd=old_prd)
        print(f"status={metrics['status']} gate={metrics.get('quality_gate')} "
              f"cost=${metrics['total_cost_usd']:.2f} issues={info.get('issue_numbers')}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
