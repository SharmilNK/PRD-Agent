# ADR-0012: Cheaper runs — Sonnet for reading and judging, short PRD, lean mode

- **Date:** 2026-10-13
- **Status:** Accepted (updates the amounts in ADR-0011)

## Context
The founder wants each run to cost as little as possible: at most $2, ideally about $1. In the first real run (all Opus), research cost $2.47, the revision $1.25 and the PRD Writer $1.00. The PRD was ~112k characters long, much longer than anyone reads.

## Decision
- **Model per agent** (`MODELS` in `packages/agents/common.py`). Claude Sonnet 5.5 ($2/$10 per million tokens) runs guardrails, research, the debate, the Scorer and the Reviewer. Claude Opus 5.5 ($4/$20) runs only the PRD Writer, where writing quality matters most.
- **Costs are priced per model.** Every response is priced by the model that actually answered. Reservations use the dearer of a model and its fallback model.
- **Short PRD.** Prompt v4 asks for 2,500-3,500 words (never more than 4,000), mostly bullets and tables. PRD Writer `max_tokens` goes from 64k to 32k, and effort from high to medium. This keeps $0.90 for the writer instead of $1.20.
- **Less research.** Searches go from 4/3/3 to 2/2/1. Each search adds 25-35k tokens of page text, so this is the biggest cut.
- **Lighter checks.**
  - Debate turns have word limits and use low effort.
  - The Reviewer opens 3 links instead of 5, with smaller pages.
  - The revision runs only for **critical** findings, failed links or failed free checks. Major and minor findings stay in `review.json`.
- **Lean profile** (`--lean` / `PRD_AGENT_PROFILE=lean`): 1 search per agent, 1 debate round, no link check, low PRD effort.

## Consequences
- Estimated cost (not yet measured live):
  - standard: ~$1.40 per run;
  - lean: ~$1;
  - a revision, when one runs, adds ~$0.50.
- The $2 hard limit stays as a safety net.
- Fewer sources per PRD. There are more `[NEEDS RESEARCH]` marks, especially in lean mode.
- Sonnet judging may be less strict than Opus. Compare eval scores (`python -m evals.run_evals`) before and after; if quality drops, move the Reviewer back to Opus first.
- Major review findings are no longer fixed automatically: a human should read `review.json`.
