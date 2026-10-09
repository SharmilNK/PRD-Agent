"""Guardrails agent: checks a transcript before any other agent reads it.

Steps:
  1. Size limit.
  2. Mask personal data and secrets (rule-based, before any AI call).
  3. Spot obvious prompt-injection phrases (rule-based).
  4. Claude review: on topic? injection? EU AI Act risk level? harm?
  5. Decide: allow, warn (continue, with notes for the PRD) or block (stop).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from packages.agents.common import (
    FALLBACK_BETA,
    MODEL,
    estimate_cost,
    get_client,
    text_of,
    usage_dict,
)
from packages.agents.guardrails.checks import MAX_CHARS, find_injection, mask_pii
from packages.observability.tracing import span

PROMPT_PATH = Path(__file__).with_name("prompt.md")
MAX_TOKENS = 16000
EFFORT = "low"

RISK_LEVELS = ["minimal", "limited", "high", "unacceptable"]

REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "is_product_idea": {"type": "boolean"},
        "injection_detected": {"type": "boolean"},
        "injection_evidence": {"type": "array", "items": {"type": "string"}},
        "eu_ai_act_risk": {"type": "string", "enum": RISK_LEVELS},
        "risk_reason": {"type": "string"},
        "sensitive_areas": {"type": "array", "items": {"type": "string"}},
        "harm_concerns": {"type": "array", "items": {"type": "string"}},
        "recommendation": {"type": "string", "enum": ["allow", "warn", "block"]},
        "notes_for_prd": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "is_product_idea", "injection_detected", "injection_evidence", "eu_ai_act_risk",
        "risk_reason", "sensitive_areas", "harm_concerns", "recommendation", "notes_for_prd",
    ],
    "additionalProperties": False,
}


class GuardrailsError(RuntimeError):
    """The Claude review did not return a usable result."""


@dataclass
class GuardrailReport:
    decision: str  # allow | warn | block
    reasons: list[str]
    sanitized_transcript: str
    pii_masked: dict[str, int]
    injection_phrases: list[str]
    review: dict | None = None
    notes_for_prd: list[str] = field(default_factory=list)
    model: str | None = None
    usage: dict = field(default_factory=dict)

    @property
    def cost_usd(self) -> float:
        return estimate_cost(self.usage)

    def to_json(self) -> dict:
        """Report for saving. Leaves out the transcript text itself."""
        data = asdict(self)
        data.pop("sanitized_transcript")
        data["cost_usd"] = self.cost_usd
        return data


def review_with_claude(sanitized: str, client=None) -> tuple[dict, str, dict]:
    """Ask Claude to review the (already masked) transcript. Returns (review, model, usage)."""
    client = get_client(client)
    system = PROMPT_PATH.read_text()
    with span("llm:guardrails review", effort=EFFORT) as s:
        message = client.beta.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            betas=[FALLBACK_BETA],
            thinking={"type": "adaptive"},
            output_config={
                "effort": EFFORT,
                "format": {"type": "json_schema", "schema": REVIEW_SCHEMA},
            },
            system=system,
            messages=[{
                "role": "user",
                "content": f"Review this transcript.\n\n<transcript>\n{sanitized.strip()}\n</transcript>",
            }],
            extra_body={"fallbacks": "default"},
        )
        s.record_message(message, system)
    if message.stop_reason == "refusal":
        raise GuardrailsError(f"Model declined the review: {getattr(message, 'stop_details', None)}")
    if message.stop_reason == "max_tokens":
        raise GuardrailsError("Review was cut off at max_tokens.")
    try:
        review = json.loads(text_of(message))
    except json.JSONDecodeError as e:
        raise GuardrailsError(f"Review was not valid JSON: {e}") from e
    return review, message.model, usage_dict(message)


def decide(pii: dict[str, int], phrases: list[str], review: dict | None) -> tuple[str, list[str], list[str]]:
    """Combine rule-based and Claude results into (decision, reasons, notes_for_prd)."""
    block, warn, notes = [], [], []

    if pii:
        found = ", ".join(f"{n} {kind.lower()}" for kind, n in sorted(pii.items()))
        warn.append(f"Personal data or secrets masked: {found}")
        notes.append("The transcript contained personal data or secrets (now masked). "
                     "Cover how the product will handle personal data.")
    if phrases:
        warn.append(f"Possible prompt injection: {len(phrases)} suspicious phrase(s)")
        notes.append("The transcript contained possible prompt-injection text. List it as a risk "
                     "and plan input checks for any AI feature that reads user text.")

    if review:
        if not review["is_product_idea"]:
            block.append("Not a product idea or requirements transcript")
        if review["eu_ai_act_risk"] == "unacceptable":
            block.append(f"Unacceptable risk under the EU AI Act: {review['risk_reason']}")
        if review["recommendation"] == "block" and not block:
            block.append("Guardrails reviewer recommended blocking: " + review["risk_reason"])
        if review["injection_detected"] and not phrases:
            warn.append("Claude review found a possible prompt injection")
        if review["eu_ai_act_risk"] == "high":
            warn.append(f"High risk under the EU AI Act: {review['risk_reason']}")
        if review["harm_concerns"]:
            warn.append("Harm concerns: " + "; ".join(review["harm_concerns"]))
        if review["recommendation"] == "warn" and not warn:
            warn.append("Guardrails reviewer recommended a warning")
        notes.extend(review["notes_for_prd"])
        notes.append(f"EU AI Act risk level (first review): {review['eu_ai_act_risk']} - {review['risk_reason']}")

    if block:
        return "block", block + warn, notes
    if warn:
        return "warn", warn, notes
    return "allow", [], notes


def run_guardrails(transcript: str, client=None, use_llm: bool = True) -> GuardrailReport:
    if len(transcript) > MAX_CHARS:
        return GuardrailReport(
            decision="block",
            reasons=[f"Transcript is too long ({len(transcript):,} characters; limit {MAX_CHARS:,})"],
            sanitized_transcript="",
            pii_masked={},
            injection_phrases=[],
        )

    sanitized, pii = mask_pii(transcript)
    phrases = find_injection(sanitized)

    review, model, usage = (None, None, {})
    if use_llm:
        review, model, usage = review_with_claude(sanitized, client=client)

    decision, reasons, notes = decide(pii, phrases, review)
    return GuardrailReport(
        decision=decision,
        reasons=reasons,
        sanitized_transcript=sanitized,
        pii_masked=pii,
        injection_phrases=phrases,
        review=review,
        notes_for_prd=notes,
        model=model,
        usage=usage,
    )
