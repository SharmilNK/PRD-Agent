"""Tracing: a timed record ("span") for every pipeline step and every Claude call.

One trace per run, saved as data/traces/<run id>.jsonl (one JSON span per line). Field names
follow OpenTelemetry conventions (trace_id, span_id, parent_span_id, start/end time, status,
attributes), so the file is easy to load into tracing tools later.

What is recorded: names, timings, model, stop reason, tokens, cost, cache use, web searches,
prompt version, request id, errors. What is NOT recorded: transcript, prompt or PRD text.

Usage:
    tracer = Tracer(run_id)
    with tracer.active():
        with span("step:research", agent="market") as s:
            ...
            s.record_message(message)      # for a Claude call
    tracer.save(path)

Outside an active tracer, span() does nothing, so agents work the same with or without tracing.
"""

from __future__ import annotations

import contextvars
import hashlib
import json
import re
import secrets
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

_tracer: contextvars.ContextVar["Tracer | None"] = contextvars.ContextVar("tracer", default=None)
_parent: contextvars.ContextVar["Span | None"] = contextvars.ContextVar("parent_span", default=None)
PROMPT_HEADER_RE = re.compile(r"<!--\s*prompt:\s*([\w.-]+)\s+(v\d+)\s*-->")


def _now_iso(t: float) -> str:
    return datetime.fromtimestamp(t, timezone.utc).isoformat(timespec="milliseconds")


def prompt_version(system: str | list) -> str:
    """'<name> <version>@<hash>' from a prompt's header comment, e.g. 'guardrails v1@3f2a9c1b04de'."""
    text = system if isinstance(system, str) else " ".join(b.get("text", "") for b in system)
    match = PROMPT_HEADER_RE.search(text)
    label = f"{match.group(1)} {match.group(2)}" if match else "prompt"
    return f"{label}@{hashlib.sha256(text.encode()).hexdigest()[:12]}"


class Span:
    def __init__(self, name: str, trace_id: str, parent: "Span | None", attributes: dict):
        self.name, self.trace_id = name, trace_id
        self.span_id = secrets.token_hex(8)
        self.parent_span_id = parent.span_id if parent else None
        self.attributes = dict(attributes)
        self.start = time.time()
        self.end: float | None = None
        self.status, self.error = "ok", None

    def set(self, **attributes) -> None:
        self.attributes.update(attributes)

    def record_message(self, message, system=None) -> None:
        """Record what a Claude response tells us: model, stop reason, tokens, cost, request id."""
        from packages.agents.common import WEB_SEARCH_USD, estimate_cost, usage_dict

        usage = usage_dict(message)
        server = getattr(message.usage, "server_tool_use", None)
        searches = getattr(server, "web_search_requests", 0) or 0
        self.set(
            model=getattr(message, "model", None),
            stop_reason=getattr(message, "stop_reason", None),
            request_id=getattr(message, "_request_id", None),
            web_searches=searches,
            cost_usd=round(estimate_cost(usage) + searches * WEB_SEARCH_USD, 6),
            **{f"tokens.{k.replace('_input_tokens', '').replace('_tokens', '')}": v for k, v in usage.items()},
        )
        if system is not None:
            self.set(prompt_version=prompt_version(system))

    def to_json(self) -> dict:
        end = self.end or time.time()
        return {
            "trace_id": self.trace_id, "span_id": self.span_id, "parent_span_id": self.parent_span_id,
            "name": self.name, "start_time": _now_iso(self.start), "end_time": _now_iso(end),
            "duration_ms": round((end - self.start) * 1000, 1), "status": self.status,
            **({"error": self.error} if self.error else {}), "attributes": self.attributes,
        }


class _NoSpan:
    """Used when no tracer is active: accepts the same calls and does nothing."""

    def set(self, **attributes) -> None:
        pass

    def record_message(self, message, system=None) -> None:
        pass


class Tracer:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.spans: list[Span] = []
        self._lock = threading.Lock()

    @contextmanager
    def active(self):
        token = _tracer.set(self)
        try:
            yield self
        finally:
            _tracer.reset(token)

    def add(self, s: Span) -> None:
        with self._lock:
            self.spans.append(s)

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            lines = [json.dumps(s.to_json()) for s in sorted(self.spans, key=lambda s: s.start)]
        path.write_text("\n".join(lines) + "\n")
        return path

    def summary(self) -> dict:
        """Totals for the metrics file: number of Claude calls, tokens, cache hit rate, errors."""
        llm = [s.attributes for s in self.spans if s.name.startswith("llm:")]
        tok = lambda k: sum(a.get(f"tokens.{k}", 0) for a in llm)  # noqa: E731
        prompt_in = tok("input") + tok("cache_read") + tok("cache_creation")
        return {
            "spans": len(self.spans),
            "llm_calls": len(llm),
            "input_tokens": prompt_in,
            "output_tokens": tok("output"),
            "cache_hit_rate": round(tok("cache_read") / prompt_in, 3) if prompt_in else 0.0,
            "web_searches": sum(a.get("web_searches", 0) for a in llm),
            "errors": sum(s.status == "error" for s in self.spans),
        }


@contextmanager
def span(name: str, **attributes):
    tracer = _tracer.get()
    if tracer is None:
        yield _NoSpan()
        return
    s = Span(name, tracer.trace_id, _parent.get(), attributes)
    token = _parent.set(s)
    try:
        yield s
    except BaseException as e:
        s.status, s.error = "error", f"{type(e).__name__}: {str(e)[:300]}"
        raise
    finally:
        s.end = time.time()
        _parent.reset(token)
        tracer.add(s)


def run_in_context(fn, *args, **kwargs):
    """For thread pools: run fn in a copy of the current context, so its spans join this trace."""
    ctx = contextvars.copy_context()
    return lambda: ctx.run(fn, *args, **kwargs)
