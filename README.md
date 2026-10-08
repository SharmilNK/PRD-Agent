# PRD-Agent

Turn a requirements transcript into a professional **PRD.md** using a team of AI agents and real product-management frameworks.

This is also a learning project: how an AI product goes from **idea to launch (0 to 1)**.

## How it will work

```
Transcript → Reader → Guardrails → Research (Market, Standards, Tech)
          → Advocate (with context) ⇄ Skeptic (no context)
          → Scorer → PRD Writer → Reviewer
          → PRD.md + GitHub issues/decisions + metrics + Slack/Gmail alert + dashboard
```

An **orchestrator** runs the agents in order and passes data between them.

## Repo layout (monorepo)

```
apps/
  orchestrator/   runs the agents in order
  dashboard/      static web page for metrics (Phase 8)
packages/
  agents/         one folder per agent (prompt + code)
  frameworks/     GUCCI, CIRCLES, Cagan's Four Risks, RICE, Kano, HEART, ... + scorecard.json
  templates/      PRD template and its sources
  integrations/   GitHub, Slack, Gmail helpers (Phases 6-7)
data/
  transcripts/    inputs (first: storyml-newsletter.md)
  outputs/        generated PRDs
  decisions/      decision records (ADRs)
  metrics/        run data as JSON
evals/            quality checks
```

## Frameworks

Every score names a framework and evidence. See [`packages/frameworks/`](packages/frameworks/README.md).
The PRD template and where each section comes from: [`packages/templates/`](packages/templates/SOURCES.md).

## Run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # or: ant auth login

# See the prompt without calling the API (free)
python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md --dry-run

# Generate the PRD
python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md
```

Each run writes:
- `data/outputs/<transcript-name>/PRD.md` — the PRD
- `data/metrics/<run-id>.json` — model, prompt version, tokens, cost, time, structure check

Check any PRD's structure: `python -m evals.check_structure data/outputs/storyml-newsletter/PRD.md`

Run the tests (no API key needed): `python -m unittest discover -s tests -t .`

## Roadmap

| Phase | What | Status |
|---|---|---|
| 0 | Repo layout, templates, framework rubrics, first transcript | done |
| 1 | One agent: transcript → PRD.md | done |
| 2 | Guardrails agent | |
| 3 | Market, Standards, Tech research agents with citations | |
| 4 | Advocate vs. Skeptic debate + Scorer | |
| 5 | Reviewer + evals | |
| 6 | GitHub auto-logging + Actions | |
| 7 | Slack / Gmail alerts | |
| 8 | Dashboard + live local reload | |
| 9 | Observability (tracing, cost) | |
