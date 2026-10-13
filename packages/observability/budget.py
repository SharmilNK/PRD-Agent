"""Hard cost limit for a run: no Claude call may start unless its worst-case cost fits.

How it works:
  - Before every call, the meter *holds* the call's worst-case cost: input (estimated from the
    text size), output (max_tokens), and for web tools the searches and page text they may add.
  - If the full call doesn't fit, max_tokens is lowered to what fits. If not even a small answer
    fits, the call is refused (BudgetExceeded) and that step is skipped.
  - After the call, the hold is released and the real cost is charged.
  - Money can be *reserved* for a later step (the PRD Writer), so earlier optional steps can't use it.

Holds are taken under a lock, so the three research agents running in parallel can't overspend together.
Outside a run (tests, a single agent) there is no meter and calls are not limited.
"""

from __future__ import annotations

import contextvars
import threading
from contextlib import contextmanager

from packages.agents.common import PRICE_PER_MTOK, WEB_SEARCH_USD, estimate_cost, usage_dict

IN_USD = PRICE_PER_MTOK["input_tokens"] / 1_000_000
OUT_USD = PRICE_PER_MTOK["output_tokens"] / 1_000_000
CHARS_PER_TOKEN = 3  # cautious: English is usually ~4 characters per token
# Measured in a real run (2026-10-09): each web search added ~23-34k input tokens of page text.
TOKENS_PER_SEARCH = 35_000
MIN_OUTPUT_TOKENS = 2_000  # below this an answer is not useful; refuse the call instead

_meter: contextvars.ContextVar["Meter | None"] = contextvars.ContextVar("budget_meter", default=None)


class BudgetExceeded(RuntimeError):
    """A call (or step) was refused because it could push the run over its cost limit."""


class Meter:
    def __init__(self, limit_usd: float):
        self.limit = limit_usd
        self.spent = 0.0
        self.held = 0.0
        self.reserved = 0.0
        self._lock = threading.Lock()

    @contextmanager
    def active(self):
        token = _meter.set(self)
        try:
            yield self
        finally:
            _meter.reset(token)

    def available(self) -> float:
        with self._lock:
            return self.limit - self.spent - self.held - self.reserved

    def reserve(self, amount: float) -> None:
        """Set money aside for a later step. Only as much as is actually left."""
        with self._lock:
            self.reserved = max(0.0, min(amount, self.limit - self.spent - self.held))

    def release_reserve(self) -> None:
        with self._lock:
            self.reserved = 0.0

    def _hold(self, label: str, fixed_usd: float, max_tokens: int) -> tuple[int, float]:
        with self._lock:
            room = self.limit - self.spent - self.held - self.reserved
            allowed = min(max_tokens, int((room - fixed_usd) / OUT_USD))
            if allowed < MIN_OUTPUT_TOKENS:
                raise BudgetExceeded(
                    f"{label}: skipped - only ${max(room, 0):.2f} of the ${self.limit:.2f} budget is left")
            hold = fixed_usd + allowed * OUT_USD
            self.held += hold
            return allowed, hold

    def _settle(self, hold: float, cost: float) -> None:
        with self._lock:
            self.held -= hold
            self.spent += cost


def worst_case_input_usd(input_chars: int, searches: int = 0, extra_input_tokens: int = 0) -> float:
    tokens = input_chars / CHARS_PER_TOKEN + searches * TOKENS_PER_SEARCH + extra_input_tokens
    return tokens * IN_USD + searches * WEB_SEARCH_USD


def message_cost(message) -> float:
    server = getattr(message.usage, "server_tool_use", None)
    searches = getattr(server, "web_search_requests", 0) or 0
    return estimate_cost(usage_dict(message)) + searches * WEB_SEARCH_USD


@contextmanager
def budget_call(label: str, input_chars: int, max_tokens: int, searches: int = 0, extra_input_tokens: int = 0):
    """Wrap one Claude call. Yields (max_tokens to use, settle function to call with the response)."""
    meter = _meter.get()
    if meter is None:
        yield max_tokens, lambda message: None
        return
    allowed, hold = meter._hold(label, worst_case_input_usd(input_chars, searches, extra_input_tokens), max_tokens)
    charged = {"cost": 0.0}

    def settle(message) -> None:
        charged["cost"] = message_cost(message)

    try:
        yield allowed, settle
    finally:
        meter._settle(hold, charged["cost"])


def current() -> Meter | None:
    return _meter.get()
