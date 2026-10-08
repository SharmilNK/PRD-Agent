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

**Built so far:** Guardrails → Research (Market, Standards, Tech) → Debate (Advocate vs. Skeptic) → Scorer → PRD Writer.
- **Guardrails** masks personal data and secrets, spots prompt-injection text, and asks Claude whether the transcript is a real product idea and how risky it is (EU AI Act levels). It ends with allow, warn (continue with notes) or block (stop).
- **Research** agents search the web at the same time (8 / 6 / 5 searches; Standards uses official sites only). Plain code grades every source A-D and rejects invented links. See [`packages/agents/research/`](packages/agents/research/README.md).
- **Debate:** the Advocate (full context) pitches and the Skeptic (sees only the pitch) challenges for 2 rounds. See [`packages/agents/debate/`](packages/agents/debate/README.md).
- **Scorer** runs GUCCI, scores 10 criteria with frameworks and evidence; code checks the scores and computes Go / Pivot / No-Go. See [`packages/agents/scorer/`](packages/agents/scorer/README.md).
- **PRD Writer** writes the PRD from the cleaned transcript, addresses every guardrail note, cites the checked research, and copies the scores unchanged.

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
# Options: --skip-guardrail-review (rules only), --skip-research (no web search), --skip-debate
python -m apps.orchestrator.run data/transcripts/storyml-newsletter.md
```

Each run writes:
- `data/outputs/<transcript-name>/guardrails.json` — what the Guardrails agent found (allow / warn / block)
- `data/outputs/<transcript-name>/research/*.json` and `research_brief.md` — checked research with sources
- `data/outputs/<transcript-name>/debate.md` and `scorecard.json` — the debate and the scores with the verdict
- `data/outputs/<transcript-name>/PRD.md` — the PRD (skipped if guardrails block the run)
- `data/metrics/<run-id>.json` — model, prompt version, tokens, cost, time, structure check

Check any PRD's structure: `python -m evals.check_structure data/outputs/storyml-newsletter/PRD.md`

Run the tests (no API key needed): `python -m unittest discover -s tests -t .`

## Roadmap

| Phase | What | Status |
|---|---|---|
| 0 | Repo layout, templates, framework rubrics, first transcript | done |
| 1 | One agent: transcript → PRD.md | done |
| 2 | Guardrails agent | done |
| 3 | Market, Standards, Tech research agents with citations | done |
| 4 | Advocate vs. Skeptic debate + Scorer | done |
| 5 | Reviewer + evals | |
| 6 | GitHub auto-logging + Actions | |
| 7 | Slack / Gmail alerts | |
| 8 | Dashboard + live local reload | |
| 9 | Observability (tracing, cost) | |
