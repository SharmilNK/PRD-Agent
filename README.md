# PRD-Agent

How an AI product goes from **idea to launch (0 to 1)**.
Turn a requirements transcript into a professional **PRD.md** using a team of AI agents and real product-management frameworks. A run costs **at most $2** (about $1.40 standard, about $1 with `--lean`; estimates, not yet measured live).

## How it works

```
Transcript → Guardrails → Research (Market, Standards, Tech)
          → Advocate (with context) ⇄ Skeptic (no context)
          → Scorer → PRD Writer → Checks → Reviewer → (one revision if critical)
          → PRD.md + run log + GitHub issues + Gmail alert + dashboard
```

An **orchestrator** runs the agents in a fixed order and passes data between them. Transcripts and web pages are treated as data, never as instructions.

| Step | What it does | Model |
|---|---|---|
| **Guardrails** | Masks personal data and secrets, spots prompt-injection text, asks Claude if this is a real product idea and how risky it is (EU AI Act levels). Ends with allow, warn or block. | Sonnet |
| **Research** | Market, Standards and Tech agents search the web (2 / 2 / 1 searches; Standards uses official sites only). Plain code grades every source A-D and rejects invented links. [Details](packages/agents/research/README.md) | Sonnet |
| **Debate** | The Advocate (full context) pitches; the Skeptic (sees only the pitch) challenges for 2 rounds plus a closing. [Details](packages/agents/debate/README.md) | Sonnet |
| **Scorer** | Runs GUCCI, scores 10 criteria with a named framework and evidence. Code checks the scores and computes Go / Pivot / No-Go. [Details](packages/agents/scorer/README.md) | Sonnet |
| **PRD Writer** | Writes a short PRD (2,500-3,500 words, 19 sections), cites checked research, copies the scores unchanged. | Opus |
| **Checks** | Free, plain code: all sections present, no links outside the research, scores match. | none |
| **Reviewer** | Opens up to 3 cited links, reviews the PRD on a 10-point rubric. One revision only for critical problems. [Details](packages/agents/reviewer/README.md), [evals](evals/README.md) | Sonnet |

Why two models? Sonnet reads and judges at about half the price. Opus only writes the PRD, where writing quality matters most. See [ADR-0012](data/decisions/0012-cheaper-runs.md).

## Cost control

- **Hard limit, default $2.** Before every Claude call, the run reserves that call's worst-case cost. A call that does not fit is shortened or skipped, so a run cannot go over. The PRD Writer's money ($0.90) is kept aside, so the PRD is always written. Change it with `--budget 3` or `PRD_AGENT_MAX_COST_USD` (`none` = no limit).
- **Lean mode** (`--lean` or `PRD_AGENT_PROFILE=lean`): 1 search per agent, 1 debate round, no link check, less PRD thinking. Aims at about $1.
- Skipped steps are listed in the metrics and trigger a `budget` Gmail alert.

More: [`packages/observability/`](packages/observability/README.md), [ADR-0011](data/decisions/0011-hard-budget.md).

## Repo layout (monorepo)

```
apps/
  orchestrator/   runs the agents in order
  dashboard/      static web page (live locally, GitHub Pages online)
packages/
  agents/         one folder per agent (prompt + code)
  frameworks/     GUCCI, CIRCLES, Cagan's Four Risks, RICE, Kano, HEART, ... + scorecard.json
  templates/      PRD template and its sources
  integrations/   GitHub issues, run log, Gmail alerts
  observability/  tracing, cost budget, operations report
data/
  transcripts/    inputs (first: storyml-newsletter.md)
  outputs/        generated PRDs
  decisions/      decision records (ADRs) and RUN_LOG.md
  metrics/        run data as JSON
  traces/         one trace per run (metadata only, no text)
evals/            quality checks and test cases
tests/            unit tests (no API key needed)
.github/workflows/  the prd-agent Action and the Pages deploy
```

## Frameworks

Every score names a framework and evidence. See [`packages/frameworks/`](packages/frameworks/README.md).
The PRD template and where each section comes from: [`packages/templates/`](packages/templates/SOURCES.md).

## Run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # or: ant auth login

# See the settings without calling the API (free). Add --lean to see lean mode.
python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --dry-run

# Generate the PRD (default $2 limit)
python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md

# Cheaper: about $1
python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --lean
```

Options: `--budget N`, `--lean`, `--skip-guardrail-review` (rules only), `--skip-research`, `--skip-debate`, `--skip-review`, `--no-revise`, `--github-issues`, `--alert`.

Each run writes, under `data/outputs/<transcript-name>/`:
- `guardrails.json`: what Guardrails found (allow / warn / block)
- `research/*.json` and `research_brief.md`: checked research with sources
- `debate.md` and `scorecard.json`: the debate, and the scores with the verdict
- `review.json`, `quality.json` (and `PRD.draft.md` if revised)
- `PRD.md`: the PRD (skipped if guardrails block the run)

And elsewhere: `data/metrics/<run-id>.json` (model, prompt version, tokens, cost, time, profile, budget) and `data/traces/<run-id>.jsonl`.

## Operations

| What | How |
|---|---|
| **Run log** | Every run is logged in `data/metrics/index.json` and `data/decisions/RUN_LOG.md`. |
| **GitHub issues** | `--github-issues` (needs `GITHUB_TOKEN`, `GITHUB_REPOSITORY`). No duplicates; fixed problems close automatically. Issues get labels but no assignee yet. |
| **Gmail alerts** | `--alert` for new or updated PRDs and problems. Setup: [`packages/integrations/`](packages/integrations/README.md). |
| **Dashboard** | `python -m apps.dashboard.serve` (live reload on your computer) or GitHub Pages. See [`apps/dashboard/`](apps/dashboard/README.md). |
| **Operations report** | `python -m packages.observability.report`: speed, cost, errors and cache use per agent. |
| **Automatic runs** | Push a transcript to `data/transcripts/` on `main` and the `prd-agent` Action runs the pipeline and commits results. Optional repo variables: `PRD_AGENT_MAX_COST_USD`, `PRD_AGENT_PROFILE`. Setup: [`packages/integrations/`](packages/integrations/README.md). |

## Checks and tests

```bash
python -m unittest discover -s tests -t .              # free, no API key
python -m evals.quality_checks data/outputs/storyml-newsletter   # check a finished PRD, free
python -m evals.run_evals                              # costs money; add --cheap for a smoke test
```

## Status

All phases 0-9 are built and merged except the cost work, which is open in [PR #22](https://github.com/SharmilNK/PRD-Agent/pull/22). Not yet tested live: the cheaper models, the short-PRD prompt, lean mode, GitHub API calls, Gmail sending and the Pages deploy. The first real run (before the cost work) passed the quality gate with verdict Pivot but cost $5.93. Project memory and next steps are in [`MEMORY.md`](MEMORY.md).

| Phase | What | Status |
|---|---|---|
| 0 | Repo layout, templates, framework rubrics, first transcript | done |
| 1 | One agent: transcript → PRD.md | done |
| 2 | Guardrails agent | done |
| 3 | Market, Standards, Tech research agents with citations | done |
| 4 | Advocate vs. Skeptic debate + Scorer | done |
| 5 | Reviewer + evals | done |
| 6 | GitHub auto-logging + Actions | done |
| 7 | Gmail alerts on PRD updates | done |
| 8 | Dashboard + live local reload | done |
| 9 | Observability (tracing, cost) | done |
| 10 | Hard cost limit, cheaper models, short PRD, lean mode | built, in PR #22 |
