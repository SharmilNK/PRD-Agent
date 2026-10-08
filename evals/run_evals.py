"""Eval harness: run the whole pipeline on test transcripts and check the expected outcomes.

Each case in evals/cases.json says what should happen (completed or blocked, guardrail decision,
quality gate, text that must never appear in any output). This catches regressions when a prompt,
model or rule changes.

This calls the real API and costs money (roughly the cost of one full run per case).
Use --cheap for a fast smoke test (no research, debate or review).

Usage:
    python -m evals.run_evals
    python -m evals.run_evals --case injection --case off_topic
    python -m evals.run_evals --cheap
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from apps.orchestrator import run as orchestrator

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.json"


def load_cases(names: list[str] | None = None) -> list[dict]:
    cases = json.loads(CASES_PATH.read_text())["cases"]
    if names:
        unknown = set(names) - {c["name"] for c in cases}
        if unknown:
            raise SystemExit(f"Unknown case(s): {', '.join(sorted(unknown))}")
        cases = [c for c in cases if c["name"] in names]
    return cases


def check_expectations(expect: dict, metrics: dict, out_dir: Path) -> list[str]:
    """Return a list of failures (empty = case passed)."""
    failures = []
    if "status" in expect and metrics["status"] != expect["status"]:
        failures.append(f"status: expected {expect['status']}, got {metrics['status']}")
    decision = metrics["guardrails"]["decision"]
    if "guardrails_in" in expect and decision not in expect["guardrails_in"]:
        failures.append(f"guardrails: expected one of {expect['guardrails_in']}, got {decision}")
    if "quality_gate" in expect and metrics.get("quality_gate") != expect["quality_gate"]:
        failures.append(f"quality gate: expected {expect['quality_gate']}, got {metrics.get('quality_gate')}")
    if expect.get("must_not_contain"):
        texts = [p.read_text() for p in out_dir.rglob("*") if p.is_file() and p.suffix in (".md", ".json")]
        for needle in expect["must_not_contain"]:
            if any(needle in t for t in texts):
                failures.append(f"output contains forbidden text: {needle!r}")
    return failures


def run_evals(cases: list[dict], client=None, cheap: bool = False, root: Path | None = None) -> dict:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = root or ROOT / "data" / "evals" / run_id
    results = []
    for case in cases:
        transcript = ROOT / case["transcript"]
        case_root = root / case["name"]
        try:
            metrics = orchestrator.run(
                transcript, client=client, outputs_dir=case_root / "outputs", metrics_dir=case_root / "metrics",
                do_research=not cheap, do_debate=not cheap, do_review=not cheap, revise=not cheap,
            )
        except ImportError:
            raise
        except Exception as e:  # noqa: BLE001 - one broken case must not hide the others
            results.append({"name": case["name"], "passed": False, "failures": [f"crashed: {type(e).__name__}: {e}"],
                            "cost_usd": 0.0})
            continue
        failures = check_expectations(case["expect"], metrics, case_root / "outputs" / transcript.stem)
        results.append({
            "name": case["name"], "passed": not failures, "failures": failures,
            "status": metrics["status"], "guardrails": metrics["guardrails"]["decision"],
            "verdict": (metrics.get("evaluation") or {}).get("verdict"),
            "quality_gate": metrics.get("quality_gate"),
            "rubric_average": (metrics.get("review") or {}).get("rubric_average"),
            "cost_usd": metrics["total_cost_usd"],
        })
    summary = {
        "run_id": run_id,
        "cheap": cheap,
        "passed": sum(r["passed"] for r in results),
        "total": len(results),
        "total_cost_usd": round(sum(r["cost_usd"] for r in results), 4),
        "results": results,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the PRD-Agent eval cases")
    parser.add_argument("--case", action="append", help="run only this case (repeatable)")
    parser.add_argument("--cheap", action="store_true", help="skip research, debate and review")
    args = parser.parse_args(argv)
    try:
        summary = run_evals(load_cases(args.case), cheap=args.cheap)
    except ImportError:
        print("The anthropic package is missing. Run: pip install -r requirements.txt", file=sys.stderr)
        return 1
    for r in summary["results"]:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"{mark}  {r['name']:<12} ${r['cost_usd']:.4f}  " + ("; ".join(r["failures"]) or "ok"))
    print(f"\n{summary['passed']}/{summary['total']} cases passed. Total cost ${summary['total_cost_usd']:.4f}")
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
