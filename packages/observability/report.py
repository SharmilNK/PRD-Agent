"""Operations report: how fast, how costly and how reliable each agent is, across all runs.

Reads data/metrics/<run id>.json (and the trace summaries inside them). Per agent:
calls, median and 95th-percentile time, average and total cost, error rate, cache hit rate.

Usage:
    python -m packages.observability.report
    python -m packages.observability.report --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
METRICS_DIR = REPO_ROOT / "data" / "metrics"


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    k = (len(ordered) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(ordered) - 1)
    return round(ordered[lo] + (ordered[hi] - ordered[lo]) * (k - lo), 2)


def agent_group(name: str) -> str:
    """'research:market' -> 'research', 'prd_writer:revision' -> 'prd_writer (revision)'."""
    if name.startswith("research:"):
        return "research"
    return name.replace(":revision", " (revision)")


def load_runs(metrics_dir: Path = METRICS_DIR) -> list[dict]:
    runs = []
    for f in sorted(metrics_dir.glob("*.json")):
        if f.name == "index.json":
            continue
        try:
            runs.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            continue  # a half-written file; skip it
    return runs


def build_report(runs: list[dict]) -> dict:
    agents: dict[str, dict] = {}
    for run in runs:
        for step in run.get("steps", []):
            a = agents.setdefault(agent_group(step["agent"]), {"durations": [], "costs": [], "errors": 0, "calls": 0,
                                                             "cache_read": 0, "prompt_tokens": 0})
            a["calls"] += 1
            if "error" in step:
                a["errors"] += 1
                continue
            a["durations"].append(step.get("duration_s", 0.0))
            a["costs"].append(step.get("cost_usd", 0.0))
            usage = step.get("usage") or {}
            a["cache_read"] += usage.get("cache_read_input_tokens", 0)
            a["prompt_tokens"] += sum(usage.get(k, 0) for k in
                                      ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    rows = []
    for name, a in sorted(agents.items(), key=lambda kv: -sum(kv[1]["costs"])):
        rows.append({
            "agent": name,
            "calls": a["calls"],
            "p50_s": _percentile(a["durations"], 0.5),
            "p95_s": _percentile(a["durations"], 0.95),
            "avg_cost_usd": round(sum(a["costs"]) / len(a["costs"]), 4) if a["costs"] else 0.0,
            "total_cost_usd": round(sum(a["costs"]), 4),
            "error_rate": round(a["errors"] / a["calls"], 3),
            "cache_hit_rate": round(a["cache_read"] / a["prompt_tokens"], 3) if a["prompt_tokens"] else 0.0,
        })
    completed = [r for r in runs if r.get("status") == "completed"]
    total = sum(r.get("total_cost_usd", 0.0) for r in runs)
    return {
        "runs": len(runs),
        "completed": len(completed),
        "total_cost_usd": round(total, 4),
        "avg_cost_per_run_usd": round(total / len(runs), 4) if runs else 0.0,
        "p50_run_s": _percentile([r.get("total_duration_s", 0.0) for r in runs], 0.5),
        "p95_run_s": _percentile([r.get("total_duration_s", 0.0) for r in runs], 0.95),
        "budget_skips": sum(bool((r.get("budget") or {}).get("skipped")) for r in runs),
        "agents": rows,
    }


def format_table(report: dict) -> str:
    lines = [
        f"Runs: {report['runs']} ({report['completed']} completed)   "
        f"Total cost: ${report['total_cost_usd']:.2f}   Avg per run: ${report['avg_cost_per_run_usd']:.2f}   "
        f"Run time p50/p95: {report['p50_run_s']}s / {report['p95_run_s']}s   Budget skips: {report['budget_skips']}",
        "",
        f"{'Agent':<24}{'Calls':>6}{'p50 s':>8}{'p95 s':>8}{'Avg $':>9}{'Total $':>9}{'Errors':>8}{'Cache hit':>11}",
    ]
    for a in report["agents"]:
        lines.append(f"{a['agent']:<24}{a['calls']:>6}{a['p50_s']:>8}{a['p95_s']:>8}{a['avg_cost_usd']:>9.4f}"
                     f"{a['total_cost_usd']:>9.2f}{a['error_rate']:>8.0%}{a['cache_hit_rate']:>11.0%}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PRD-Agent operations report")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = build_report(load_runs())
    print(json.dumps(report, indent=2) if args.json else format_table(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
