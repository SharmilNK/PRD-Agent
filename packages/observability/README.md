# Observability (Phase 9)

How to see what the AI system did, how long it took, what it cost, and where it broke.

## 1. Tracing (`tracing.py`), always on
Every run saves a trace to `data/traces/<run id>.jsonl`: one line ("span") per pipeline step and per Claude call.

| Recorded | Not recorded |
|---|---|
| Step and call names, start/end time, duration | Transcript text |
| Model, stop reason, request id | Prompt text |
| Tokens (input, output, cache read/write), cost, web searches | PRD text |
| Prompt version (name + version + hash), errors | Email addresses, secrets |

Spans are nested (run → step → Claude call), and the three research agents running in parallel all land in the same trace. Field names follow OpenTelemetry conventions, so the file can be loaded into tracing tools later (for example Langfuse, Honeycomb, or Grafana Tempo).

The run's `data/metrics/<run id>.json` gets a short `trace` summary: number of Claude calls, tokens, **cache hit rate**, web searches, errors.

## 2. Cost budget
Each run has a spending limit (default **$10**). Once it is reached, optional steps are skipped (research, debate, Reviewer, revision), but the PRD is still written. Skipped steps are listed in metrics, shown on the command line, and trigger a `budget` Gmail alert.

- Change it per run: `--budget 3`
- Or for all runs: `PRD_AGENT_MAX_COST_USD=3` (local) or the repository variable of the same name (GitHub Action). Use `none` for no limit.

## 3. Operations report (`report.py`)
```bash
python -m packages.observability.report          # table
python -m packages.observability.report --json
```
Per agent across all runs: calls, typical (p50) and slow-case (p95) time, average and total cost, error rate, cache hit rate. Plus totals: runs, cost per run, run time, budget skips.

The same numbers are on the dashboard's **Operations** section.

## What to watch (why this matters for AI products)
- **Cost per run** creeping up: prompts growing, or more revisions.
- **Cache hit rate** near 0% on the PRD Writer: the cached system prompt is being invalidated.
- **p95 time** much larger than p50: some calls are very slow (long outputs, retries).
- **Error rate** above 0: a step is failing; check the trace's `error` field and the GitHub issue.
- **Prompt version** changes: compare quality and cost before and after (run `python -m evals.run_evals`).
