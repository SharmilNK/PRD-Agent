# ADR-0001: Use one repository (monorepo)

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
The project has many parts: agents, an orchestrator, a dashboard, integrations, templates, data and evals. They change together often.

## Decision
Keep everything in one repository with `apps/` (things you run), `packages/` (shared building blocks), `data/` (inputs, outputs, decisions, metrics) and `evals/` (quality tests).

## Consequences
- Easier: one place to look, one pull request can change an agent and its template together, one CI setup.
- Harder: the repo grows; we must keep folder boundaries clean.
