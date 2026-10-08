# ADR-0004: Research agents with limited web search and rule-based source checks

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
The PRD needs real market, regulation and technical facts. Web search can return weak, outdated or manipulated pages, and AI can invent links that look real. The search tool itself does not judge source quality.

## Decision
- Three research agents (Market, Standards, Tech) run in parallel, using Claude's server-side web search with a per-agent `max_uses` limit (8 / 6 / 5).
- The Standards agent may only search an allow-list of official sites. Market and Tech use the open web.
- Each agent returns JSON claims, each with a URL and a quote. Plain code then grades every source (A/B/C/D), rejects links that did not appear in the search results, rejects injection text and forum-sourced numbers, and labels single-source numbers, unconfirmed quotes and old sources.
- The PRD Writer may use only these checked claims as outside facts, cites them inline, and lists them in a Sources table.
- A failed research agent does not stop the run.

## Consequences
- Every outside fact in the PRD is traceable to a link, a quote, a grade and a date.
- Grading by domain is simple and can be wrong for unknown sites (they get D until added to a list). The Phase 5 Reviewer will spot-check links by opening them.
- Adds roughly $0.19 of search cost per run, plus tokens.
