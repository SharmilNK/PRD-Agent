"""Research agents: Market, Standards and Tech. Each one searches the web and returns checked claims.

Flow for one agent:
  1. Claude searches the web (limited by max_searches, and by allowed sites for Standards).
  2. If the API pauses a long search turn (stop_reason "pause_turn"), we send it back to continue.
  3. Claude answers with JSON claims (url + quote for each).
  4. sources.check_claims grades every source and rejects invented links, unsafe text,
     and numbers taken from forums.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from packages.agents.common import (
    FALLBACK_BETA,
    MODEL,
    WEB_SEARCH_USD,
    estimate_cost,
    get_client,
    text_of,
    usage_dict,
)
from packages.agents.research import sources
from packages.agents.research.config import AGENTS

PROMPTS_DIR = Path(__file__).with_name("prompts")
MAX_TOKENS = 16000
EFFORT = "medium"
MAX_CONTINUATIONS = 3


class ResearchError(RuntimeError):
    """A research agent did not return usable results."""


@dataclass
class ResearchResult:
    kind: str
    summary: str
    accepted: list[dict]
    rejected: list[dict]
    open_questions: list[str]
    searches: int
    model: str
    usage: dict = field(default_factory=dict)

    @property
    def cost_usd(self) -> float:
        return round(estimate_cost(self.usage) + self.searches * WEB_SEARCH_USD, 6)

    def to_json(self) -> dict:
        return {
            "kind": self.kind,
            "summary": self.summary,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "open_questions": self.open_questions,
            "searches": self.searches,
            "model": self.model,
            "usage": self.usage,
            "cost_usd": self.cost_usd,
        }


def system_prompt(kind: str) -> str:
    return (PROMPTS_DIR / "base.md").read_text() + "\n\n" + (PROMPTS_DIR / f"{kind}.md").read_text()


def search_tool(kind: str) -> dict:
    cfg = AGENTS[kind]
    tool = {"type": "web_search_20260209", "name": "web_search", "max_uses": cfg["max_searches"]}
    if cfg["allowed_domains"]:
        tool["allowed_domains"] = cfg["allowed_domains"]
    return tool


def extract_json(text: str) -> dict:
    """Read the JSON object from Claude's answer (inside a ```json block, or bare)."""
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced[-1] if fenced else text[text.find("{"): text.rfind("}") + 1]
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ResearchError(f"Answer was not valid JSON: {e}") from e
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise ResearchError("Answer JSON has no 'claims' list.")
    return data


def collect_evidence(content: list) -> tuple[dict[str, dict], dict[str, list[str]]]:
    """From response blocks: search results (url -> title, page_age) and citations (url -> cited texts)."""
    results: dict[str, dict] = {}
    citations: dict[str, list[str]] = {}
    for block in content:
        if block.type == "web_search_tool_result" and isinstance(block.content, list):
            for r in block.content:
                if getattr(r, "type", "") == "web_search_result":
                    results[r.url] = {"title": getattr(r, "title", ""), "page_age": getattr(r, "page_age", None)}
        elif block.type == "text":
            for c in getattr(block, "citations", None) or []:
                if getattr(c, "url", None):
                    citations.setdefault(c.url, []).append(getattr(c, "cited_text", "") or "")
    return results, citations


def _add_usage(total: dict, message) -> int:
    for k, v in usage_dict(message).items():
        total[k] = total.get(k, 0) + v
    server = getattr(message.usage, "server_tool_use", None)
    return getattr(server, "web_search_requests", 0) or 0


def run_research(kind: str, transcript: str, client=None) -> ResearchResult:
    if kind not in AGENTS:
        raise ValueError(f"Unknown research agent: {kind}")
    client = get_client(client)
    cfg = AGENTS[kind]

    messages = [{
        "role": "user",
        "content": "Research this product idea. Use your focus topics.\n\n"
                   f"<transcript>\n{transcript.strip()}\n</transcript>",
    }]
    content, usage, searches = [], {}, 0

    for _ in range(MAX_CONTINUATIONS + 1):
        message = client.beta.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            betas=[FALLBACK_BETA],
            thinking={"type": "adaptive"},
            output_config={"effort": EFFORT},
            system=system_prompt(kind),
            tools=[search_tool(kind)],
            messages=messages,
            extra_body={"fallbacks": "default"},
        )
        searches += _add_usage(usage, message)
        content.extend(message.content)
        if message.stop_reason != "pause_turn":
            break
        # Resume the paused turn: send everything the assistant produced so far, with no new user message.
        messages = messages[:1] + [{"role": "assistant", "content": list(content)}]
    else:
        raise ResearchError(f"{kind}: search turn was still paused after {MAX_CONTINUATIONS} continuations.")

    if message.stop_reason == "refusal":
        raise ResearchError(f"{kind}: model declined: {getattr(message, 'stop_details', None)}")
    if message.stop_reason == "max_tokens":
        raise ResearchError(f"{kind}: answer was cut off at max_tokens.")

    data = extract_json(text_of(message))
    results, citations = collect_evidence(content)
    accepted, rejected = sources.check_claims(data["claims"], results, citations, cfg["stale_after_days"])

    return ResearchResult(
        kind=kind,
        summary=str(data.get("summary", "")),
        accepted=accepted,
        rejected=rejected,
        open_questions=[str(q) for q in data.get("open_questions", [])],
        searches=searches,
        model=message.model,
        usage=usage,
    )


def brief_for_prd(results: list[ResearchResult], failed: dict[str, str] | None = None) -> str:
    """Turn checked research into a compact brief for the PRD Writer."""
    parts = []
    for r in results:
        lines = [f"### {AGENTS[r.kind]['title']} ({r.searches} searches)", r.summary, ""]
        for c in r.accepted:
            tags = sources.labels(c)
            tag_text = f" ({', '.join(tags)})" if tags else ""
            lines.append(
                f"- [{c['checks']['grade']}] {c['claim']}{tag_text}\n"
                f"  Source: {c['url']} | published: {c['checks']['published']} | quote: \"{c['quote']}\""
            )
        if r.rejected:
            lines.append(f"- ({len(r.rejected)} claim(s) rejected by source checks and left out)")
        for q in r.open_questions:
            lines.append(f"- Open question: {q}")
        parts.append("\n".join(lines))
    for kind, error in (failed or {}).items():
        parts.append(f"### {AGENTS[kind]['title']}\nResearch failed ({error}). Treat this area as [NEEDS RESEARCH].")
    return "\n\n".join(parts)
