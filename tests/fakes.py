"""A fake Claude client for tests. No API key or network needed."""

import json
from types import SimpleNamespace

from packages.agents.common import MODEL

ALLOW_REVIEW = {
    "is_product_idea": True,
    "injection_detected": False,
    "injection_evidence": [],
    "eu_ai_act_risk": "minimal",
    "risk_reason": "Educational newsletter.",
    "sensitive_areas": [],
    "harm_concerns": [],
    "recommendation": "allow",
    "notes_for_prd": [],
}


def _message(text, stop_reason="end_turn", extra_blocks=(), searches=0, citations=()):
    usage = SimpleNamespace(input_tokens=1000, output_tokens=2000,
                            cache_creation_input_tokens=0, cache_read_input_tokens=None,
                            server_tool_use=SimpleNamespace(web_search_requests=searches))
    text_block = SimpleNamespace(type="text", text=text, citations=list(citations))
    return SimpleNamespace(
        content=[SimpleNamespace(type="thinking", thinking=""), *extra_blocks, text_block],
        stop_reason=stop_reason, stop_details=None, model=MODEL, usage=usage,
    )


def search_result_block(results):
    """results: list of (url, title, page_age)."""
    return SimpleNamespace(type="web_search_tool_result", content=[
        SimpleNamespace(type="web_search_result", url=u, title=t, page_age=a) for u, t, a in results
    ])


def citation(url, cited_text):
    return SimpleNamespace(type="web_search_result_location", url=url, title="", cited_text=cited_text)


def research_message(claims, results, citations=(), searches=2, stop_reason="end_turn", summary="Found evidence."):
    text = "Here is what I found.\n```json\n" + json.dumps(
        {"summary": summary, "claims": claims, "open_questions": ["Exact audience size"]}
    ) + "\n```"
    return _message(text, stop_reason, extra_blocks=[search_result_block(results)],
                    searches=searches, citations=citations)


DEFAULT_RESEARCH = research_message(
    claims=[{
        "topic": "competitors", "claim": "StatQuest explains ML concepts with simple visuals.",
        "url": "https://statquest.org/about", "quote": "StatQuest breaks down complicated statistics",
        "published": "2025-01-10", "source_type": "company_own_page",
    }],
    results=[("https://statquest.org/about", "About StatQuest", "2025-01-10")],
    citations=[citation("https://statquest.org/about", "StatQuest breaks down complicated statistics and ML")],
)


class _Stream:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.message


class FakeClient:
    """`stream` answers the PRD Writer; `create` answers the Guardrails review."""

    def __init__(self, prd_text="# PRD: Test\n", stop_reason="end_turn", review=None, review_stop_reason="end_turn",
                 research=None):
        """research: dict of agent kind -> list of messages (returned in order) or an Exception to raise."""
        self.stream_calls, self.create_calls, self.research_calls = [], [], []
        self._research = research or {}
        self._prd = _message(prd_text, stop_reason)
        review_text = review if isinstance(review, str) else json.dumps(review or ALLOW_REVIEW)
        self._review = _message(review_text, review_stop_reason)
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream, create=self._create))

    def _stream(self, **kwargs):
        self.stream_calls.append(kwargs)
        return _Stream(self._prd)

    def _create(self, **kwargs):
        if "tools" in kwargs:
            return self._research_reply(kwargs)
        self.create_calls.append(kwargs)
        return self._review

    def _research_reply(self, kwargs):
        self.research_calls.append(kwargs)
        kind = next(k for k in ("market", "standards", "tech") if f"focus: {_FOCUS[k]}" in kwargs["system"])
        reply = self._research.get(kind, [DEFAULT_RESEARCH])
        if isinstance(reply, Exception):
            raise reply
        return reply.pop(0) if len(reply) > 1 else reply[0]


_FOCUS = {"market": "market research", "standards": "industry standards", "tech": "technical build"}
