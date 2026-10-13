"""Settings and helpers shared by all agents."""

from __future__ import annotations

OPUS = "claude-opus-5-5"
SONNET = "claude-sonnet-5-5"
MODEL = OPUS  # default when a call doesn't name a model
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# Which model each agent uses. Opus writes the PRD (writing quality matters most); Sonnet, at half
# the price, does the reading, judging and reviewing. Change a line here to switch an agent.
MODELS = {
    "guardrails": SONNET,
    "research": SONNET,
    "debate": SONNET,
    "scorer": SONNET,
    "reviewer": SONNET,
    "prd_writer": OPUS,
}

# USD per million tokens (5-minute cache write = 1.25x input).
PRICES = {
    OPUS: {"input_tokens": 4.00, "output_tokens": 20.00,
           "cache_creation_input_tokens": 5.00, "cache_read_input_tokens": 0.20},
    SONNET: {"input_tokens": 2.00, "output_tokens": 10.00,
             "cache_creation_input_tokens": 2.50, "cache_read_input_tokens": 0.20},
    # Possible safety-fallback models (the API may answer with one of these instead).
    "claude-sonnet-5": {"input_tokens": 2.00, "output_tokens": 10.00,
                        "cache_creation_input_tokens": 2.50, "cache_read_input_tokens": 0.20},
    "claude-opus-4-8": {"input_tokens": 5.00, "output_tokens": 25.00,
                        "cache_creation_input_tokens": 6.25, "cache_read_input_tokens": 0.50},
}
# fallbacks="default" may answer a declined request with another model: Opus 5.5 -> Opus 4.8,
# Sonnet 5.5 -> Sonnet 5. The budget reserves at the dearer of the two prices.
FALLBACK_MODEL = {OPUS: "claude-opus-4-8", SONNET: "claude-sonnet-5"}
# Unknown models are priced like the most expensive one above, so cost is never under-counted.
_MOST_EXPENSIVE = max(PRICES.values(), key=lambda p: p["output_tokens"])
PRICE_PER_MTOK = PRICES[OPUS]  # the usage fields we track (same keys for every model)


def prices_for(model: str | None) -> dict:
    return PRICES.get(model or "", _MOST_EXPENSIVE)


def get_client(client=None):
    """Return the given client, or create a real Anthropic client."""
    if client is not None:
        return client
    import anthropic

    return anthropic.Anthropic()


def usage_dict(message) -> dict:
    return {k: getattr(message.usage, k, 0) or 0 for k in PRICE_PER_MTOK}


def estimate_cost(usage: dict, model: str | None = MODEL) -> float:
    return round(
        sum(usage.get(k, 0) * price for k, price in prices_for(model).items()) / 1_000_000, 6
    )


def text_of(message) -> str:
    return "".join(b.text for b in message.content if b.type == "text").strip()

# Web search is billed per search, on top of tokens.
WEB_SEARCH_USD = 0.01  # $10 per 1,000 searches


def create_message(client, *, system: str, user: str, effort: str, error: type[Exception],
                   label: str, max_tokens: int = 16000, output_format: dict | None = None, model: str = MODEL):
    """One non-streaming Claude call with the project defaults. Raises `error` on refusal or truncation."""
    output_config = {"effort": effort}
    if output_format:
        output_config["format"] = output_format
    from packages.observability.budget import budget_call
    from packages.observability.tracing import span

    with span(f"llm:{label}", effort=effort) as s, \
            budget_call(label, len(system) + len(user), max_tokens, model=model) as (allowed, settle):
        message = get_client(client).beta.messages.create(
            model=model,
            max_tokens=allowed,
            betas=[FALLBACK_BETA],
            thinking={"type": "adaptive"},
            output_config=output_config,
            system=system,
            messages=[{"role": "user", "content": user}],
            extra_body={"fallbacks": "default"},
        )
        settle(message)
        s.record_message(message, system)
    if message.stop_reason == "refusal":
        raise error(f"{label}: model declined: {getattr(message, 'stop_details', None)}")
    if message.stop_reason == "max_tokens":
        raise error(f"{label}: answer was cut off at max_tokens.")
    if not text_of(message):
        raise error(f"{label}: model returned no text.")
    return message


def run_tool_turn(client, *, system: str, user: str, tools: list[dict], effort: str,
                  error: type[Exception], label: str, max_tokens: int = 16000, max_continuations: int = 3,
                  model: str = MODEL):
    """One turn with server-side tools (web search / web fetch), resuming `pause_turn` stops.

    Returns (final message, every content block from all responses, summed usage, web searches used).
    """
    client = get_client(client)
    messages = [{"role": "user", "content": user}]
    content, usage, searches = [], {}, 0
    from packages.observability.budget import budget_call
    from packages.observability.tracing import span

    # Worst case for the budget: every allowed search, and every fetched page at full size.
    max_searches = sum(t.get("max_uses", 5) for t in tools if t["type"].startswith("web_search"))
    fetch_tokens = sum(t.get("max_uses", 5) * t.get("max_content_tokens", 20000)
                       for t in tools if t["type"].startswith("web_fetch"))

    for attempt in range(max_continuations + 1):
        sent_chars = len(system) + len(user) + sum(len(str(b)) for b in content)
        with span(f"llm:{label}", effort=effort, attempt=attempt, tools=[t["type"] for t in tools]) as s, \
                budget_call(label, sent_chars, max_tokens, max_searches, fetch_tokens, model=model) as (allowed, settle):
            message = client.beta.messages.create(
                model=model,
                max_tokens=allowed,
                betas=[FALLBACK_BETA],
                thinking={"type": "adaptive"},
                output_config={"effort": effort},
                system=system,
                tools=tools,
                messages=messages,
                extra_body={"fallbacks": "default"},
            )
            settle(message)
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
