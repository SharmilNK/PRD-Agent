"""Reviewer: final check of the PRD before anyone relies on it.

Two parts:
  1. Link spot-check - open up to MAX_LINKS cited sources with web fetch and confirm the quote is there.
     When the fetched page text is available, plain code makes the call; otherwise Claude's report is used.
  2. Review - Claude reviews the PRD (logic, evidence, security, responsible AI, observability,
     performance, right-sizing, plain language) and scores it on evals/rubric.json.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from packages.agents.common import create_message, estimate_cost, run_tool_turn, text_of, usage_dict
from packages.agents.research.sources import NUMBER_RE, quote_found

HERE = Path(__file__).parent
RUBRIC_PATH = HERE.parents[2] / "evals" / "rubric.json"
MAX_LINKS = 5
MAX_PAGE_TOKENS = 8000
EFFORT = "high"
LINK_EFFORT = "low"
SEVERITIES = ["critical", "major", "minor"]


class ReviewerError(RuntimeError):
    """The Reviewer did not return a usable result."""


def load_rubric() -> dict:
    return json.loads(RUBRIC_PATH.read_text())


# ---------- Part 1: link spot-check ----------

def pick_claims(claims: list[dict], limit: int = MAX_LINKS) -> list[dict]:
    """Check the claims that matter most first: numbers, then A/B sources. One claim per URL."""
    def priority(c):
        has_number = bool(NUMBER_RE.search(c["claim"]))
        return (not has_number, c["checks"]["grade"] not in ("A", "B"))

    picked, seen = [], set()
    for c in sorted(claims, key=priority):
        if c["url"] not in seen:
            picked.append(c)
            seen.add(c["url"])
        if len(picked) == limit:
            break
    return picked


def fetched_pages(content: list) -> dict[str, str]:
    """URL -> page text, from web_fetch result blocks (when the text is included)."""
    pages = {}
    for block in content:
        if getattr(block, "type", "") != "web_fetch_tool_result":
            continue
        result = getattr(block, "content", None)
        if getattr(result, "type", "") != "web_fetch_result":
            continue
        source = getattr(getattr(result, "content", None), "source", None)
        text = getattr(source, "data", None)
        if isinstance(text, str) and getattr(result, "url", None):
            pages[result.url] = text
    return pages


def _extract_json(text: str) -> dict:
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced[-1] if fenced else text[text.find("{"): text.rfind("}") + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ReviewerError(f"link check: answer was not valid JSON: {e}") from e


def decide_link_status(claim: dict, pages: dict[str, str], reported: dict[str, dict]) -> dict:
    url = claim["url"]
    if url in pages:
        ok = quote_found(claim["quote"], [pages[url]])
        return {"url": url, "status": "confirmed" if ok else "not_found", "checked_by": "code"}
    r = reported.get(url)
    if not r or not r.get("fetched"):
        return {"url": url, "status": "fetch_failed", "checked_by": "model", "note": (r or {}).get("note", "")}
    status = {"yes": "confirmed", "partly": "partly", "no": "not_found"}.get(r.get("quote_present"), "unknown")
    return {"url": url, "status": status, "checked_by": "model", "note": r.get("note", "")}


def check_links(claims: list[dict], client=None) -> tuple[list[dict], dict]:
    """Returns (one result per checked claim, usage)."""
    picked = pick_claims(claims)
    if not picked:
        return [], {}
    listing = "\n".join(f"{i}. URL: {c['url']}\n   Quote: \"{c['quote']}\"" for i, c in enumerate(picked, 1))
    tool = {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": len(picked),
            "max_content_tokens": MAX_PAGE_TOKENS}
    message, content, usage, _ = run_tool_turn(
        client, system=(HERE / "link_check.md").read_text(), user=f"Check these sources:\n\n{listing}",
        tools=[tool], effort=LINK_EFFORT, error=ReviewerError, label="link check",
    )
    reported = {c.get("url"): c for c in _extract_json(text_of(message)).get("checks", [])}
    pages = fetched_pages(content)
    results = []
    for c in picked:
        r = decide_link_status(c, pages, reported)
        r.update(claim=c["claim"], quote=c["quote"], grade=c["checks"]["grade"])
        results.append(r)
    return results, usage


# ---------- Part 2: review ----------

def revision_feedback(review: "ReviewResult | None", quality: dict) -> str:
    """The problems the PRD Writer must fix: serious review findings, failed links, failed checks."""
    lines = []
    if review:
        for f in review.findings:
            if f["severity"] in ("critical", "major"):
                lines.append(f"- [{f['severity']}] Section {f['section']} ({f['category']}): {f['issue']} Fix: {f['fix']}")
        for l in review.link_checks:
            if l["status"] == "not_found":
                lines.append(f"- [major] The quote for {l['url']} was not found on the page. "
                             "Remove that claim or mark it [NEEDS RESEARCH].")
    for u in quality["links"]["unknown_links"]:
        lines.append(f"- [critical] Link {u} is not from the checked research. Remove it or mark the claim [NEEDS RESEARCH].")
    for m in quality["scores"]["mismatches"]:
        lines.append(f"- [critical] Section 16 score differs from the evaluation: {m}. Copy the evaluation exactly.")
    for sec in quality["structure"]["missing_sections"]:
        lines.append(f"- [critical] Missing section: {sec}.")
    return "\n".join(lines)


def review_schema(rubric: dict) -> dict:
    finding = {
        "type": "object",
        "properties": {
            "severity": {"type": "string", "enum": SEVERITIES},
            "section": {"type": "string"},
            "category": {"type": "string"},
            "issue": {"type": "string"},
            "fix": {"type": "string"},
        },
        "required": ["severity", "section", "category", "issue", "fix"],
        "additionalProperties": False,
    }
    ids = [c["id"] for c in rubric["criteria"]]
    return {
        "type": "object",
        "properties": {
            "findings": {"type": "array", "items": finding},
            "rubric": {
                "type": "object",
                "properties": {i: {"type": "integer", "enum": [1, 2, 3, 4, 5]} for i in ids},
                "required": ids,
                "additionalProperties": False,
            },
            "summary": {"type": "string"},
        },
        "required": ["findings", "rubric", "summary"],
        "additionalProperties": False,
    }


@dataclass
class ReviewResult:
    findings: list[dict]
    rubric: dict[str, int]
    rubric_average: float
    summary: str
    link_checks: list[dict]
    model: str
    usage: dict = field(default_factory=dict)

    @property
    def cost_usd(self) -> float:
        return estimate_cost(self.usage)

    def count(self, severity: str) -> int:
        return sum(f["severity"] == severity for f in self.findings)

    @property
    def needs_revision(self) -> bool:
        return bool(self.count("critical") or self.count("major")
                    or any(l["status"] == "not_found" for l in self.link_checks))

    def to_json(self) -> dict:
        return {
            "summary": self.summary,
            "counts": {s: self.count(s) for s in SEVERITIES},
            "findings": self.findings,
            "rubric": self.rubric,
            "rubric_average": self.rubric_average,
            "link_checks": self.link_checks,
            "model": self.model,
            "usage": self.usage,
            "cost_usd": self.cost_usd,
        }


def review_prd(prd: str, evaluation: str = "", research: str = "", quality: dict | None = None,
               claims: list[dict] | None = None, client=None, check_sources: bool = True) -> ReviewResult:
    rubric = load_rubric()
    link_checks, usage = (check_links(claims or [], client=client) if check_sources else ([], {}))

    user = "\n\n".join(filter(None, [
        f"<rubric>\n{json.dumps(rubric, indent=2)}\n</rubric>",
        f"<prd>\n{prd.strip()}\n</prd>",
        f"<evaluation>\n{evaluation.strip()}\n</evaluation>" if evaluation else "",
        f"<research>\n{research.strip()}\n</research>" if research else "",
        f"<link_checks>\n{json.dumps(link_checks, indent=2)}\n</link_checks>" if link_checks else "",
        f"<quality_checks>\n{json.dumps(quality, indent=2)}\n</quality_checks>" if quality else "",
        "Review the PRD and score it on the rubric.",
    ]))
    message = create_message(
        client, system=(HERE / "prompt.md").read_text(), user=user, effort=EFFORT,
        error=ReviewerError, label="reviewer",
        output_format={"type": "json_schema", "schema": review_schema(rubric)},
    )
    try:
        data = json.loads(text_of(message))
    except json.JSONDecodeError as e:
        raise ReviewerError(f"reviewer: answer was not valid JSON: {e}") from e

    for k, v in usage_dict(message).items():
        usage[k] = usage.get(k, 0) + v
    scores = data["rubric"]
    order = {s: i for i, s in enumerate(SEVERITIES)}
    return ReviewResult(
        findings=sorted(data["findings"], key=lambda f: order[f["severity"]]),
        rubric=scores,
        rubric_average=round(sum(scores.values()) / len(scores), 2),
        summary=data["summary"],
        link_checks=link_checks,
        model=message.model,
        usage=usage,
    )
