# ADR-0011: Hard per-run cost limit, default $2

- **Date:** 2026-10-13
- **Status:** Accepted (replaces the soft budget in ADR-0010)

## Context
The first real run (2026-10-09) cost $5.93 although its budget was $5: the old budget was only checked *between* steps, and the revision step alone cost $1.25. The founder wants each run to cost at most $2.

## Decision
- **Reservation before every call** (`packages/observability/budget.py`): input (text size / 3 characters per token), maximum output tokens, and for web tools every allowed search (35k tokens of page text each, from real data) or fetched page. If it doesn't fit, `max_tokens` is lowered; below 2,000 tokens the call is refused and the step is skipped. Holds are taken under a lock, so parallel research agents can't overspend together.
- **Default limit $2** (`--budget`, `PRD_AGENT_MAX_COST_USD`); minimum $0.75.
- **$1.20 is kept for the PRD Writer** until it runs, so the PRD is always written.
- **Research runs one agent at a time**, in priority order, when the budget can't cover all three at once.
- **Search limits cut** from 8/6/5 to 4/3/3, and research answers capped at 10,000 tokens.

## Consequences
- A run cannot go over its limit, except if a single web-search turn pulls far more page text than the 35k-tokens-per-search estimate (not seen so far).
- At $2 with Claude Opus 5.5, a full run doesn't fit: the PRD is always written, but research, the debate, the Reviewer and the revision are partly or fully skipped. Shorter PRDs or a cheaper model for some steps would let more of the pipeline fit.
