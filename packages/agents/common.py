"""Settings and helpers shared by all agents."""

from __future__ import annotations

MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# USD per million tokens for claude-opus-5-5 (cache write = 1.25x input).
PRICE_PER_MTOK = {
    "input_tokens": 4.00,
    "output_tokens": 20.00,
    "cache_creation_input_tokens": 5.00,
    "cache_read_input_tokens": 0.20,
}


def get_client(client=None):
    """Return the given client, or create a real Anthropic client."""
    if client is not None:
        return client
    import anthropic

    return anthropic.Anthropic()


def usage_dict(message) -> dict:
    return {k: getattr(message.usage, k, 0) or 0 for k in PRICE_PER_MTOK}


def estimate_cost(usage: dict) -> float:
    return round(
        sum(usage.get(k, 0) * price for k, price in PRICE_PER_MTOK.items()) / 1_000_000, 6
    )


def text_of(message) -> str:
    return "".join(b.text for b in message.content if b.type == "text").strip()
