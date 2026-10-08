"""PRD Writer agent: turns a requirements transcript into a PRD.md draft.

Phase 1 is a single Claude call. Later phases feed it research, debate and
scores from other agents.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_PATH = Path(__file__).with_name("prompt.md")
TEMPLATE_PATH = REPO_ROOT / "packages" / "templates" / "PRD_TEMPLATE.md"
SCORECARD_PATH = REPO_ROOT / "packages" / "frameworks" / "scorecard.json"

MODEL = "claude-opus-5-5"
MAX_TOKENS = 64000
EFFORT = "high"

# USD per million tokens for claude-opus-5-5 (cache write = 1.25x input).
PRICE_PER_MTOK = {
    "input_tokens": 4.00,
    "output_tokens": 20.00,
    "cache_creation_input_tokens": 5.00,
    "cache_read_input_tokens": 0.20,
}


class PRDWriterError(RuntimeError):
    """The model did not return a usable PRD."""


@dataclass
class PRDResult:
    markdown: str
    model: str
    stop_reason: str
    prompt_version: str
    usage: dict = field(default_factory=dict)

    @property
    def cost_usd(self) -> float:
        return estimate_cost(self.usage)


def build_system_prompt() -> str:
    """Instructions + PRD template + scorecard. Stable text, so it can be cached."""
    return "\n\n".join(
        [
            PROMPT_PATH.read_text(),
            "## PRD template\n\n" + TEMPLATE_PATH.read_text(),
            "## Scorecard (packages/frameworks/scorecard.json)\n\n```json\n"
            + SCORECARD_PATH.read_text()
            + "\n```",
        ]
    )


def prompt_version(system_prompt: str) -> str:
    """Short hash of the full system prompt, so each run records which prompt it used."""
    return hashlib.sha256(system_prompt.encode()).hexdigest()[:12]


def build_user_message(transcript: str) -> str:
    return (
        "Write the PRD for the product described in this transcript.\n\n"
        f"<transcript>\n{transcript.strip()}\n</transcript>"
    )


def estimate_cost(usage: dict) -> float:
    return round(
        sum(usage.get(k, 0) * price for k, price in PRICE_PER_MTOK.items()) / 1_000_000, 6
    )


def write_prd(transcript: str, client=None) -> PRDResult:
    """Call Claude once and return the PRD Markdown plus usage numbers."""
    if client is None:
        import anthropic

        client = anthropic.Anthropic()

    system_prompt = build_system_prompt()

    # Streaming avoids HTTP timeouts on long outputs.
    # fallbacks="default": if a safety classifier declines, the API retries on
    # a suitable fallback model inside the same call.
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        betas=["server-side-fallback-2026-07-01"],
        thinking={"type": "adaptive"},
        output_config={"effort": EFFORT},
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_user_message(transcript)}],
        extra_body={"fallbacks": "default"},
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == "refusal":
        details = getattr(message, "stop_details", None)
        raise PRDWriterError(f"Model declined the request: {details}")
    if message.stop_reason == "max_tokens":
        raise PRDWriterError("PRD was cut off at max_tokens; raise MAX_TOKENS or lower EFFORT.")

    markdown = "".join(b.text for b in message.content if b.type == "text").strip()
    if not markdown:
        raise PRDWriterError("Model returned no text.")

    usage = {k: getattr(message.usage, k, 0) or 0 for k in PRICE_PER_MTOK}
    return PRDResult(
        markdown=markdown + "\n",
        model=message.model,
        stop_reason=message.stop_reason,
        prompt_version=prompt_version(system_prompt),
        usage=usage,
    )
