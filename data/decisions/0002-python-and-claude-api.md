# ADR-0002: Python + Claude API, orchestrator calls agents in a fixed order

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
We need agents that hand work to each other. Options: free-form agent chat, or a simple program that calls each agent in order.

## Decision
Use Python with the official Anthropic SDK (`anthropic`). A small orchestrator (`apps/orchestrator`) calls each agent in a fixed order and passes plain data between them. Start with one agent (PRD Writer) and add agents phase by phase.

## Consequences
- Easier: simple to read, test and debug; every step leaves files we can inspect.
- Harder: less "creative" agent collaboration; we add the Advocate vs. Skeptic debate later as an explicit loop.
