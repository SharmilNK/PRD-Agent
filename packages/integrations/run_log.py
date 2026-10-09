"""Run log: every run is recorded automatically, so the history lives in git.

- data/metrics/index.json     one short summary per run (newest first). The dashboard reads this.
- data/decisions/RUN_LOG.md   the same, as a readable table: what was decided on each run.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / "data" / "metrics" / "index.json"
RUN_LOG_PATH = REPO_ROOT / "data" / "decisions" / "RUN_LOG.md"

RUN_LOG_HEADER = """# Run log

Written automatically after every PRD-Agent run (newest first). Full details: `data/metrics/<run id>.json`.

| Run | Transcript | Status | Guardrails | Verdict | Avg score | Quality gate | Rubric | Revised | Cost | Issues |
|---|---|---|---|---|---|---|---|---|---|---|
"""


def summarize(metrics: dict) -> dict:
    """The few numbers that matter for one run."""
    ev = metrics.get("evaluation") or {}
    rv = metrics.get("review") or {}
    grades = {g: 0 for g in "ABCD"}
    for step in metrics["steps"]:
        for g, n in (step.get("grades") or {}).items():
            grades[g] += n
    return {
        "run_id": metrics["run_id"],
        "transcript": Path(metrics["transcript"]).stem,
        "status": metrics["status"],
        "guardrails": metrics["guardrails"]["decision"],
        "verdict": ev.get("verdict"),
        "average": ev.get("average"),
        "scores": ev.get("scores", {}),
        "quality_gate": metrics.get("quality_gate"),
        "rubric_average": rv.get("rubric_average"),
        "findings": rv.get("counts"),
        "links_checked": rv.get("links_checked"),
        "links_confirmed": rv.get("links_confirmed"),
        "source_grades": grades,
        "revised": metrics.get("revised", False),
        "errors": [s["agent"] for s in metrics["steps"] if "error" in s],
        "cost_usd": metrics["total_cost_usd"],
        "duration_s": metrics["total_duration_s"],
        "issues": metrics.get("github", {}).get("issue_numbers", []),
    }


def _fmt(value, fmt="{}"):
    return "-" if value is None else fmt.format(value)


def _row(s: dict) -> str:
    verdict = s["verdict"].upper().replace("_", "-") if s["verdict"] else "-"
    issues = ", ".join(f"#{n}" for n in s["issues"]) or "-"
    return (f"| {s['run_id']} | {s['transcript']} | {s['status']} | {s['guardrails']} | {verdict} | "
            f"{_fmt(s['average'])} | {_fmt(s['quality_gate'])} | {_fmt(s['rubric_average'])} | "
            f"{'yes' if s['revised'] else 'no'} | ${s['cost_usd']:.2f} | {issues} |")


def record_run(metrics: dict, index_path: Path = INDEX_PATH, run_log_path: Path = RUN_LOG_PATH) -> dict:
    """Add (or replace) this run in the index and the run log. Returns the summary."""
    summary = summarize(metrics)
    runs = json.loads(index_path.read_text())["runs"] if index_path.exists() else []
    runs = [r for r in runs if r["run_id"] != summary["run_id"]]
    runs.insert(0, summary)
    runs.sort(key=lambda r: r["run_id"], reverse=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps({"runs": runs}, indent=2) + "\n")

    run_log_path.parent.mkdir(parents=True, exist_ok=True)
    run_log_path.write_text(RUN_LOG_HEADER + "\n".join(_row(r) for r in runs) + "\n")
    return summary
