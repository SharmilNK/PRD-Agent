# ADR-0006: Reviewer with link spot-checks, free quality checks, one revision, and an eval harness

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
The PRD Writer can still make mistakes: invented links, scores that differ from the Scorer, generic security sections, quotes that aren't really on the cited page. We also need a repeatable way to know whether a prompt or model change made things better or worse.

## Decision
- **Free checks first** (`evals/quality_checks.py`): structure, every link came from checked research, section 16 scores equal `scorecard.json`, readability.
- **Reviewer:** opens up to 5 cited links with web fetch; plain code confirms the quote when page text is available. Then a Claude review with severities and fixes, scored on `evals/rubric.json`.
- **One revision** when there are critical or major findings, a quote not found, or a failed free check. Only one, to cap cost; the draft is kept.
- **Quality gate:** pass = free checks pass on the final PRD and rubric average ≥ 3.5. Note: the rubric scores the draft before revision.
- **Eval harness** (`evals/run_evals.py`, `evals/cases.json`): normal, injection, off-topic and high-risk transcripts with expected outcomes. Not run in CI because it costs money; run it after prompt, rule or model changes.

## Consequences
- Invented links and changed scores are caught by code, not by trust.
- A run costs more: a link check, a review, and sometimes a second PRD write (the revision reuses the cached system prompt).
- The rubric score is not re-measured after revision; re-running the Reviewer would double that cost.
