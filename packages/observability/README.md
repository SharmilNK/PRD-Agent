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

## 2. Hard cost limit (default $2)
A run **never costs more than its limit**. Before every Claude call, the code reserves that call's worst-case cost (its input, its maximum answer length, and for web tools the searches and page text they may add). If the call doesn't fit, its answer length is shortened; if not even a short answer fits, the call is skipped.

Priority when money is tight:
1. Guardrails
2. **$1.20 is kept aside for the PRD Writer**, so the PRD is always written
3. Research (one agent at a time, in the order market, standards, tech, when there isn't room for all three at once), then the debate and Scorer, using what is left
4. PRD Writer (gets the kept money plus anything left)
5. Reviewer and revision, only if money is still left

Skipped steps are listed in the metrics, printed at the end of the run, and trigger a `budget` Gmail alert.

- Change it per run: `--budget 3`
- Or for all runs: `PRD_AGENT_MAX_COST_USD=3` (local) or the repository variable of the same name (GitHub Action). Use `none` for no limit. The smallest allowed limit is $0.75.

**What $2 buys (from the first real run, 2026-10-09, which cost $5.93 with no hard limit):** research ~$2.47 at 8/6/5 searches (now 4/3/3), debate $0.54, Scorer $0.21, PRD Writer $1.00, Reviewer $0.45, revision $1.25. So with the $2 limit, expect the PRD plus *part* of the research and debate; the Reviewer and revision usually won't fit.

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
