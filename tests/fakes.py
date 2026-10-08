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


def _message(text, stop_reason="end_turn"):
    usage = SimpleNamespace(input_tokens=1000, output_tokens=2000,
                            cache_creation_input_tokens=0, cache_read_input_tokens=None)
    return SimpleNamespace(
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
        stop_reason=stop_reason, stop_details=None, model=MODEL, usage=usage,
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

    def __init__(self, prd_text="# PRD: Test\n", stop_reason="end_turn", review=None, review_stop_reason="end_turn"):
        self.stream_calls, self.create_calls = [], []
        self._prd = _message(prd_text, stop_reason)
        review_text = review if isinstance(review, str) else json.dumps(review or ALLOW_REVIEW)
        self._review = _message(review_text, review_stop_reason)
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream, create=self._create))

    def _stream(self, **kwargs):
        self.stream_calls.append(kwargs)
        return _Stream(self._prd)

    def _create(self, **kwargs):
        self.create_calls.append(kwargs)
        return self._review
