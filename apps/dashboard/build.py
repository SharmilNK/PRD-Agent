"""Build the dashboard: copy the static page and gather all run data into one data.json.

Reads (all from git):
  data/metrics/index.json              one summary per run (written by the run log)
  data/outputs/<name>/PRD.md           latest PRD per transcript
  data/outputs/<name>/scorecard.json   latest scores, GUCCI and verdict
  data/outputs/<name>/review.json      latest Reviewer findings and rubric
  data/outputs/<name>/quality.json     latest free checks

Usage:
    python -m apps.dashboard.build --out site
    python -m apps.dashboard.build --out site --demo   # sample data, clearly labelled, for a preview
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC = Path(__file__).with_name("static")
DATA = REPO_ROOT / "data"


def _load(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def transcript_details(outputs: Path, name: str) -> dict:
    out = outputs / name
    review = _load(out / "review.json") or {}
    card = _load(out / "scorecard.json") or {}
    prd = out / "PRD.md"
    return {
        "has_prd": prd.exists(),
        "prd": prd.read_text() if prd.exists() else "",
        "verdict": card.get("verdict"),
        "average": card.get("average"),
        "scores": {k: v.get("score") for k, v in (card.get("scores") or {}).items()},
        "gucci": card.get("gucci"),
        "unresolved_concerns": card.get("unresolved_concerns", []),
        "rubric": review.get("rubric", {}),
        "findings": [f for f in review.get("findings", []) if f.get("severity") in ("critical", "major")],
        "link_checks": [{"url": l["url"], "status": l["status"]} for l in review.get("link_checks", [])],
        "quality": _load(out / "quality.json"),
    }


def collect(data_dir: Path = DATA) -> dict:
    runs = (_load(data_dir / "metrics" / "index.json") or {}).get("runs", [])
    names = sorted({r["transcript"] for r in runs})
    from packages.observability.report import build_report, load_runs

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "demo": False,
        "runs": runs,
        "ops": build_report(load_runs(data_dir / "metrics")),
        "transcripts": {n: transcript_details(data_dir / "outputs", n) for n in names},
        "labels": _labels(),
    }


def _labels() -> dict:
    """Criterion id -> display name, for the scorecard and the rubric."""
    card = _load(REPO_ROOT / "packages" / "frameworks" / "scorecard.json") or {"criteria": []}
    rubric = _load(REPO_ROOT / "evals" / "rubric.json") or {"criteria": []}
    return {
        "criteria": {c["id"]: c["name"] for c in card["criteria"]},
        "rubric": {c["id"]: c["name"] for c in rubric["criteria"]},
        "rubric_pass": rubric.get("pass_average", 3.5),
    }


def demo_data() -> dict:
    """Clearly labelled sample data so the page can be previewed before any real run."""
    labels = _labels()
    runs = []
    for i, (cost, gate, verdict, avg, rubric) in enumerate(
            [(2.41, "fail", "pivot", 3.1, 3.2), (2.95, "pass", "pivot", 3.4, 3.7), (3.12, "pass", "go", 3.6, 3.9)]):
        runs.insert(0, {
            "run_id": f"2026100{i + 1}T120000Z-sample-newsletter", "transcript": "sample-newsletter",
            "status": "completed", "guardrails": "allow", "verdict": verdict, "average": avg, "scores": {},
            "quality_gate": gate, "rubric_average": rubric, "findings": {"critical": 0, "major": 2 - i, "minor": 3},
            "links_checked": 5, "links_confirmed": 3 + i, "source_grades": {"A": 3 + i, "B": 5, "C": 2, "D": 2 - i},
            "revised": i < 2, "errors": [], "cost_usd": cost, "duration_s": 410 + 30 * i, "issues": [],
        })
    scores = dict(zip(labels["criteria"], [4, 3, 4, 4, 3, 3, 4, 5, 4, 2]))
    prd = ("# PRD: Sample Newsletter\n\n> **Sample data** for previewing the dashboard.\n\n"
           "## 1. Press Release and FAQ\nA short sample section.\n\n## 16. Product Evaluation Scorecard\n"
           "| Criterion | Score |\n|---|---|\n" + "\n".join(f"| {labels['criteria'][k]} | {v}/5 |" for k, v in scores.items()))
    ops_rows = [("prd_writer", 0.92, 95, 140, 0.31), ("prd_writer (revision)", 0.71, 80, 110, 0.62),
                ("research", 0.38, 60, 120, 0.0), ("debate", 0.45, 70, 95, 0.0), ("reviewer", 0.33, 45, 70, 0.0),
                ("scorer", 0.21, 30, 40, 0.0), ("guardrails", 0.03, 6, 9, 0.0)]
    ops = {"runs": 3, "completed": 3, "total_cost_usd": 8.48, "avg_cost_per_run_usd": 2.83, "p50_run_s": 440,
           "p95_run_s": 467, "budget_skips": 0,
           "agents": [{"agent": a, "calls": 9 if a == "research" else 3, "p50_s": p50, "p95_s": p95,
                       "avg_cost_usd": c, "total_cost_usd": round(c * 3, 2), "error_rate": 0.0,
                       "cache_hit_rate": hit} for a, c, p50, p95, hit in ops_rows]}
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "demo": True,
        "runs": runs,
        "ops": ops,
        "transcripts": {"sample-newsletter": {
            "has_prd": True, "prd": prd, "verdict": "go", "average": 3.6, "scores": scores, "gucci": None,
            "unresolved_concerns": ["Who pays, and how much?"],
            "rubric": {k: 4 for k in labels["rubric"]},
            "findings": [{"severity": "major", "section": "13", "category": "observability",
                          "issue": "No alert when AI quiz answers are wrong.", "fix": "Track quiz error reports."}],
            "link_checks": [], "quality": None,
        }},
        "labels": labels,
    }


def build(out: Path, demo: bool = False, data_dir: Path = DATA) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    for f in STATIC.iterdir():
        if f.is_file():
            shutil.copy2(f, out / f.name)
    data = demo_data() if demo else collect(data_dir)
    (out / "data.json").write_text(json.dumps(data, indent=1) + "\n")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the PRD-Agent dashboard")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "site")
    parser.add_argument("--demo", action="store_true", help="use clearly labelled sample data")
    args = parser.parse_args(argv)
    print(f"Dashboard built in {build(args.out, args.demo)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
