"""GitHub issues: turn problems from a run into issues a person can act on.

What becomes an issue:
  - critical and major Reviewer findings
  - cited quotes the Reviewer could not find on the source page
  - a failed quality gate
  - a run blocked by guardrails
  - a pipeline step that failed (research, debate, scorer, reviewer, revision)

No duplicates: each issue carries a hidden fingerprint. If an open issue with the same
fingerprint exists, we add a comment instead of opening a new one. Open issues for the same
transcript that no longer appear are closed with a comment.

Without a GitHub token nothing is sent; the plan is saved to issues.plan.json instead.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

API = "https://api.github.com"
BASE_LABEL = "prd-agent"
FINGERPRINT_RE = re.compile(r"<!-- prd-agent:fingerprint=([0-9a-f]{16}) transcript=([\w.-]+) kind=(\w+) -->")
KINDS = ("blocked", "error", "finding", "link", "quality_gate")


class GitHubError(RuntimeError):
    """A GitHub API call failed."""


@dataclass
class PlannedIssue:
    fingerprint: str
    transcript: str
    kind: str
    title: str
    body: str
    labels: list[str]

    def full_body(self) -> str:
        return (f"{self.body}\n\n<!-- prd-agent:fingerprint={self.fingerprint} "
                f"transcript={self.transcript} kind={self.kind} -->")


def fingerprint(*parts: str) -> str:
    """Stable id from the parts that identify a problem (not its wording, which changes per run)."""
    return hashlib.sha256("|".join(p.strip().lower() for p in parts).encode()).hexdigest()[:16]


def _short(text: str, n: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def review_ran(metrics: dict) -> bool:
    return bool(metrics.get("review")) and "error" not in metrics["review"]


def checked_kinds(metrics: dict) -> set[str]:
    """Kinds of problem this run actually looked for. Only these may be auto-closed."""
    kinds = {"blocked", "error"}
    if metrics["status"] == "completed":
        kinds.add("quality_gate")
    if review_ran(metrics):
        kinds |= {"finding", "link"}
    return kinds


def plan_issues(metrics: dict, out_dir: Path) -> list[PlannedIssue]:
    name = Path(metrics["transcript"]).stem
    run = metrics["run_id"]
    footer = f"\n\n---\nRun `{run}` · transcript `{name}` · created automatically by PRD-Agent."
    revised_note = ("\n\n> The PRD was revised once to address this. Please confirm it is fixed, then close this issue."
                    if metrics.get("revised") else "")
    issues: list[PlannedIssue] = []

    def add(fp_parts, title, body, labels):
        issues.append(PlannedIssue(fingerprint(name, *fp_parts), name, fp_parts[0], f"[{name}] {title}",
                                   body + footer, [BASE_LABEL, f"transcript:{name}", *labels]))

    if metrics["status"] == "blocked":  # kind: blocked
        reasons = "\n".join(f"- {r}" for r in metrics["guardrails"]["reasons"])
        add(["blocked"], "Run blocked by guardrails",
            f"The Guardrails agent stopped this run before any PRD was written.\n\n**Reasons:**\n{reasons}",
            ["guardrails", "severity:critical"])

    for step in metrics["steps"]:
        if "error" in step:
            add(["error", step["agent"]], f"Pipeline step failed: {step['agent']}",
                f"The step `{step['agent']}` failed and was skipped. The run continued without it.\n\n"
                f"**Error:** `{_short(step['error'], 300)}`", ["pipeline-error"])

    review_path = out_dir / "review.json"
    if review_ran(metrics) and review_path.exists():
        review = json.loads(review_path.read_text())
        for f in review["findings"]:
            if f["severity"] not in ("critical", "major"):
                continue
            add(["finding", f["severity"], f["section"], f["category"]],
                f"PRD section {f['section']}: {_short(f['issue'])}",
                f"**Severity:** {f['severity']}\n**Section:** {f['section']}\n**Category:** {f['category']}\n\n"
                f"**Issue:** {f['issue']}\n\n**Suggested fix:** {f['fix']}{revised_note}",
                ["review", f"severity:{f['severity']}", f"area:{f['category'].lower().replace(' ', '-')}"])
        for link in review.get("link_checks", []):
            if link["status"] == "not_found":
                add(["link", link["url"]], f"Quote not found on cited page: {_short(link['url'], 60)}",
                    f"The Reviewer opened {link['url']} and could not find the quote.\n\n"
                    f"**Claim:** {link['claim']}\n**Quote:** \"{link['quote']}\"{revised_note}",
                    ["evidence", "severity:major"])

    if metrics.get("quality_gate") == "fail":
        q = metrics.get("quality", {})
        details = []
        details += [f"- Missing section: {s}" for s in q.get("structure", {}).get("missing_sections", [])]
        details += [f"- Link not from checked research: {u}" for u in q.get("links", {}).get("unknown_links", [])]
        details += [f"- Score mismatch: {m}" for m in q.get("scores", {}).get("mismatches", [])]
        rubric = (metrics.get("review") or {}).get("rubric_average")
        if rubric is not None:
            details.append(f"- Reviewer rubric average: {rubric} (pass needs 3.5)")
        add(["quality_gate"], "Quality gate failed",
            "The final PRD did not pass the quality gate.\n\n" + ("\n".join(details) or "- See quality.json"),
            ["quality", "severity:major"])
    return issues


class GitHubClient:
    """Tiny GitHub REST client (standard library only)."""

    def __init__(self, repo: str, token: str):
        self.repo, self.token = repo, token

    @classmethod
    def from_env(cls) -> "GitHubClient | None":
        repo, token = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN")
        return cls(repo, token) if repo and token else None

    def request(self, method: str, path: str, body: dict | None = None):
        req = urllib.request.Request(
            f"{API}/repos/{self.repo}{path}", method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "prd-agent"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read() or b"null")
        except urllib.error.HTTPError as e:
            raise GitHubError(f"{method} {path} -> {e.code}: {e.read()[:300]!r}") from e

    def open_issues(self) -> list[dict]:
        issues, page = [], 1
        while True:
            batch = self.request("GET", f"/issues?labels={BASE_LABEL}&state=open&per_page=100&page={page}")
            issues += [i for i in batch if "pull_request" not in i]
            if len(batch) < 100:
                return issues
            page += 1

    def create_issue(self, title: str, body: str, labels: list[str]) -> dict:
        return self.request("POST", "/issues", {"title": title, "body": body, "labels": labels})

    def comment(self, number: int, body: str) -> None:
        self.request("POST", f"/issues/{number}/comments", {"body": body})

    def close(self, number: int) -> None:
        self.request("PATCH", f"/issues/{number}", {"state": "closed", "state_reason": "completed"})


def sync_issues(planned: list[PlannedIssue], transcript: str, run_id: str, gh: GitHubClient,
                checked: set[str] | None = None) -> dict:
    """Create new issues, comment on repeats, close ones that went away. Returns what happened.

    Only issues whose kind is in `checked` can be closed (a run that skipped the review
    must not close review issues).
    """
    checked = set(KINDS) if checked is None else checked
    existing, kinds = {}, {}
    for issue in gh.open_issues():
        m = FINGERPRINT_RE.search(issue.get("body") or "")
        if m and m.group(2) == transcript:
            existing[m.group(1)] = issue["number"]
            kinds[m.group(1)] = m.group(3)

    result = {"created": [], "commented": [], "closed": []}
    for p in planned:
        if p.fingerprint in existing:
            gh.comment(existing[p.fingerprint], f"Seen again in run `{run_id}`:\n\n{p.body}")
            result["commented"].append(existing[p.fingerprint])
        else:
            result["created"].append(gh.create_issue(p.title, p.full_body(), p.labels)["number"])

    planned_fps = {p.fingerprint for p in planned}
    for fp, number in existing.items():
        if fp not in planned_fps and kinds[fp] in checked:
            gh.comment(number, f"Not found in run `{run_id}`. Closing automatically.")
            gh.close(number)
            result["closed"].append(number)
    return result
