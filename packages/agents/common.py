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

# Web search is billed per search, on top of tokens.
WEB_SEARCH_USD = 0.01  # $10 per 1,000 searches


def create_message(client, *, system: str, user: str, effort: str, error: type[Exception],
                   label: str, max_tokens: int = 16000, output_format: dict | None = None):
    """One non-streaming Claude call with the project defaults. Raises `error` on refusal or truncation."""
    output_config = {"effort": effort}
    if output_format:
        output_config["format"] = output_format
    from packages.observability.tracing import span

    with span(f"llm:{label}", effort=effort) as s:
        message = get_client(client).beta.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            betas=[FALLBACK_BETA],
            thinking={"type": "adaptive"},
            output_config=output_config,
            system=system,
            messages=[{"role": "user", "content": user}],
            extra_body={"fallbacks": "default"},
        )
        s.record_message(message, system)
    if message.stop_reason == "refusal":
        raise error(f"{label}: model declined: {getattr(message, 'stop_details', None)}")
    if message.stop_reason == "max_tokens":
        raise error(f"{label}: answer was cut off at max_tokens.")
    if not text_of(message):
        raise error(f"{label}: model returned no text.")
    return message


def run_tool_turn(client, *, system: str, user: str, tools: list[dict], effort: str,
                  error: type[Exception], label: str, max_tokens: int = 16000, max_continuations: int = 3):
    """One turn with server-side tools (web search / web fetch), resuming `pause_turn` stops.

    Returns (final message, every content block from all responses, summed usage, web searches used).
    """
    client = get_client(client)
    messages = [{"role": "user", "content": user}]
    content, usage, searches = [], {}, 0
    from packages.observability.tracing import span

    for attempt in range(max_continuations + 1):
        with span(f"llm:{label}", effort=effort, attempt=attempt, tools=[t["type"] for t in tools]) as s:
            message = client.beta.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                betas=[FALLBACK_BETA],
                thinking={"type": "adaptive"},
                output_config={"effort": effort},
                system=system,
                tools=tools,
                messages=messages,
                extra_body={"fallbacks": "default"},
            )
            s.record_message(message, system)
        for k, v in usage_dict(message).items():
            usage[k] = usage.get(k, 0) + v
        server = getattr(message.usage, "server_tool_use", None)
        searches += getattr(server, "web_search_requests", 0) or 0
        content.extend(message.content)
        if message.stop_reason != "pause_turn":
            break
        # Resume the paused turn: send everything the assistant produced so far, with no new user message.
        messages = messages[:1] + [{"role": "assistant", "content": list(content)}]
    else:
        raise error(f"{label}: turn was still paused after {max_continuations} continuations.")

    if message.stop_reason == "refusal":
        raise error(f"{label}: model declined: {getattr(message, 'stop_details', None)}")
    if message.stop_reason == "max_tokens":
        raise error(f"{label}: answer was cut off at max_tokens.")
    return message, content, usage, searches
