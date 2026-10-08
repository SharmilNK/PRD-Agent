"""Publish a finished run: sync GitHub issues (optional), send a Gmail alert (optional), record the run.

Kept separate from run.py so the pipeline itself never depends on GitHub or email.
A failure here is recorded and never loses the PRD.
"""

from __future__ import annotations

import json
from pathlib import Path

from packages.integrations import github_issues, notify, run_log


def read_prd(outputs_dir: Path, transcript_path: Path) -> str | None:
    """The current PRD for a transcript, read BEFORE a run so alerts can show what changed."""
    path = outputs_dir / transcript_path.stem / "PRD.md"
    return path.read_text() if path.exists() else None


def publish(metrics: dict, outputs_dir: Path, metrics_dir: Path, *, github: bool = False, gh=None,
            alert: bool = False, old_prd: str | None = None, env: dict | None = None, smtp_factory=None,
            index_path: Path = run_log.INDEX_PATH, run_log_path: Path = run_log.RUN_LOG_PATH) -> dict:
    name = Path(metrics["transcript"]).stem
    out_dir = outputs_dir / name
    planned = github_issues.plan_issues(metrics, out_dir)
    info: dict = {"planned": len(planned), "issue_numbers": []}

    gh = gh or (github_issues.GitHubClient.from_env() if github else None)
    if github and gh is None:
        info["skipped"] = "GITHUB_TOKEN or GITHUB_REPOSITORY not set"
    if gh is not None:
        try:
            result = github_issues.sync_issues(planned, name, metrics["run_id"], gh,
                                               checked=github_issues.checked_kinds(metrics))
        except github_issues.GitHubError as e:
            info["error"] = str(e)
        else:
            info.update(result)
            info["issue_numbers"] = sorted(result["created"] + result["commented"])
    if gh is None or "error" in info:
        # Nothing was sent: keep the plan so a person (or a later run) can see what would have been filed.
        plan = [{"title": p.title, "labels": p.labels, "body": p.full_body()} for p in planned]
        (out_dir / "issues.plan.json").write_text(json.dumps(plan, indent=2) + "\n")

    metrics["github"] = info
    if alert:
        kwargs = {"smtp_factory": smtp_factory} if smtp_factory else {}
        metrics["alert"] = notify.notify(metrics, out_dir, old_prd, info["issue_numbers"], env=env, **kwargs)
    run_log.record_run(metrics, index_path, run_log_path)
    (metrics_dir / f"{metrics['run_id']}.json").write_text(json.dumps(metrics, indent=2) + "\n")
    return info
