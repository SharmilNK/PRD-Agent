# MEMORY.md — project memory

> What has happened and what is pending. Update at the end of every session.
> Keep it short: facts and decisions, not long explanations. Newest log entry at the top.

## Project goal
PRD-Agent turns a requirements transcript into a professional PRD.md using a team of AI agents and real product-management frameworks. It is also a learning project: how an AI product goes from idea to launch (0 to 1), using Claude, the GitHub MCP, Slack/Gmail alerts, GitHub-based logging and a dashboard.

## About the user
- Learning end-to-end AI product launches. Self-described slow learner: use **very simple language**, short steps, one concept at a time.
- Likes an overview first, then going deep on one topic at a time.
- Wants Claude to act as a senior AI/ML product manager (3-4 years launching AI products).

## Key decisions (see data/decisions/ for full records)
| Date | Decision |
|---|---|
| 2026-10-08 | One repo (monorepo): `apps/`, `packages/`, `data/`, `evals/` (ADR-0001) |
| 2026-10-08 | Python + official Anthropic SDK; orchestrator calls agents in a fixed order (ADR-0002) |
| 2026-10-08 | Agents use model `claude-opus-5-5`, adaptive thinking, streaming, `fallbacks: "default"` |
| 2026-10-08 | Every score must name a framework + evidence. GUCCI runs first ("should we build?"), CIRCLES for "what to build", Cagan Four Risks + RICE for "can we / in what order" |
| 2026-10-08 | GUCCI = Dr. Nancy Li: Goals & Mission, Unmet Needs, Competition, Customer Segmentation, Integrated Ecosystem |
| 2026-10-08 | PRD template is built from PUBLIC sources (big-company internal templates are not public); each section names its source |
| 2026-10-08 | Extra emphasis in PRDs: security, responsible AI, observability, explainable AI |
| 2026-10-08 | Memory across sessions: CLAUDE.md imports MEMORY.md + SKILLS.md |
| 2026-10-08 | Guardrails: rules first (mask PII/secrets, injection phrases), then Claude review (topic, injection, EU AI Act risk, harm); allow / warn / block (ADR-0003) |
| 2026-10-08 | User wants ALL phases built first, then will test everything at the end |
| 2026-10-08 | Research: Market 8 / Standards 6 / Tech 5 searches; Standards uses official-site allow-list; sources graded A-D by rules; invented links rejected; numbers need 2 sites (ADR-0004) |
| 2026-10-08 | Debate: stateless calls, Skeptic gets only pitch + debate (enforced by code + tests); 2 rounds + closing. Scorer: GUCCI + 10 criteria via JSON schema; code validates and computes verdict (ADR-0005) |
| 2026-10-08 | Reviewer: free checks (structure, links only from research, scores match) + web-fetch spot-check of up to 5 links + rubric review; one revision max; quality gate = checks pass and rubric >= 3.5; eval harness with 4 cases, not in CI (ADR-0006) |
| 2026-10-08 | GitHub logging: run log (index.json + RUN_LOG.md) always on; issues via stdlib urllib with fingerprints (no duplicates, auto-close only checked kinds); Action on push to data/transcripts on main + manual; publish kept separate from pipeline (ADR-0007) |
| 2026-10-08 | Verdict rules clarified: Go = avg >= 3.5 and every criterion >= 3; No-Go = avg < 2.5 or ethics = 1; else Pivot |

## Current status
- **Phases 0-5 are merged to `main`** (PRs 1-6, plus PR 8). 104 tests at that point.
- **Phase 6** (run log, GitHub issues, Action): done — branch `claude/optimistic-faraday-rl7bty-phase6`, PR into `main`
- First test input: `data/transcripts/storyml-newsletter.md` (ML/AI concepts taught as stories, 3 tracks, 3-tier quizzes)

## Where to resume
- Phases 6-9 are built as stacked branches: phase6 (from `main`) → phase7 → phase8 → phase9, one PR each.
- **All Phase 6-9 PRs target `main` directly** (not the previous phase branch), so nothing gets stranded again. Until earlier PRs merge, a later PR also shows the earlier phases' changes. Merge in order: 6 → 7 → 8 → 9.

## Pending tasks (in order)
1. Keep building Phases 7-9 (user will test at the end). Then user reviews and merges PRs in order (6 → 7 → 8 → 9). **Important:** new cloud sessions start from `main`, so these memory files only load in new sessions after merge.
2. First real run: `python -m evals.run_evals --cheap`, then full run on the StoryML transcript (needs `pip install -r requirements.txt` + API key). Not done yet: the cloud environment blocked pypi.org (403).
3. Phase 7: Gmail alerts on PRD updates (user chose Gmail).
4. Phase 8: Dashboard (GitHub Pages) + live local reload.
5. Phase 9: Observability (tracing, cost tracking).

## Open questions
- Cloud environment: allow `pypi.org` and `files.pythonhosted.org` so the SDK can be installed and tested in cloud sessions?

## Known issues
- PyPI blocked in the cloud environment → real API runs must happen on the user's computer for now.

## Session log (newest first)
- 2026-10-08 — New session: found Phases 0-5 merged to main. Built Phase 6 (run log, GitHub issues, Action).
- 2026-10-08 — Session ended by user after Phase 5. All work committed and pushed. Resume with Phase 6.
- 2026-10-08 — Built Phase 5 (Reviewer, evals). common.run_tool_turn shared by research + link check.
- 2026-10-08 — Built Phase 4 (Debate, Scorer). PRD Writer prompt v3 copies scores; common.create_message helper added.
- 2026-10-08 — Built Phase 3 (Research agents, sources.py checks). PRD Writer prompt v2 cites research and adds a Sources table.
- 2026-10-08 — Built Phase 2 (Guardrails). Shared helpers moved to packages/agents/common.py; shared FakeClient in tests/fakes.py.
- 2026-10-08 — Added CLAUDE.md, MEMORY.md, SKILLS.md for memory across sessions.
- 2026-10-08 — Built Phase 0 + Phase 1; opened PR 1 and PR 2.
- 2026-10-07 — Planned the project: agent pipeline, frameworks (incl. GUCCI, CIRCLES), PRD template sources, monorepo, build order.
