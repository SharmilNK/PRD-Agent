# ADR-0010: Built-in tracing, a per-run cost budget, and an operations report

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
AI products fail in ways normal software doesn't: cost drifts, prompts change behavior, calls get slow, caches stop hitting. We need to see every step and every model call, and to stop a run from overspending.

## Decision
- **Tracing in-house, OpenTelemetry-shaped:** a small tracer (`contextvars`, standard library) records spans for the run, each step and each Claude call, saved as JSONL in `data/traces/`. Spans carry model, stop reason, tokens, cost, cache use, web searches, prompt version and request id, and never any transcript, prompt or PRD text. Parallel research threads join the same trace. Outside a run, spans are no-ops.
- **Why not an external tracing service now:** it would need an account, a key and extra packages. The JSONL file uses OpenTelemetry field names, so exporting to Langfuse, Honeycomb or another backend later is a small step.
- **Budget:** default $10 per run (`--budget`, `PRD_AGENT_MAX_COST_USD`). When reached, optional steps are skipped and the PRD is still written. A `budget` alert is sent.
- **Operations report** (CLI and dashboard): p50/p95 time, cost, error rate and cache hit rate per agent.

## Consequences
- Every run leaves a trace in git. Traces are small (metadata only).
- The budget is checked between steps, so one expensive step can overshoot it a little.
- Costs are estimates from public list prices in `packages/agents/common.py`; update them if prices change.
