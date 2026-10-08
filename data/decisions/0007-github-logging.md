# ADR-0007: Run log in git, GitHub issues with fingerprints, and a transcript-triggered Action

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
The project should record decisions, metrics and problems automatically, using git and GitHub as the record book, and run without someone at a laptop.

## Decision
- **Run log:** every run updates `data/metrics/index.json` and `data/decisions/RUN_LOG.md`. Always on, no network needed.
- **Issues:** critical/major findings, unconfirmed quotes, failed quality gates, blocked runs and failed steps become GitHub issues. A hidden fingerprint (transcript + what the problem is, not its wording) prevents duplicates; repeats get a comment. An issue is auto-closed only when a later run checked that kind of problem and didn't find it.
- **Standard library only** for GitHub calls (`urllib`), so nothing extra to install. Without a token the plan is saved to `issues.plan.json`.
- **Publishing is separate from the pipeline** (`apps/orchestrator/publish.py`), so GitHub problems can never lose a PRD.
- **GitHub Action** runs on pushes to `data/transcripts/*.md` on `main` and by hand. Inputs reach the script as environment variables (no shell injection); only files inside `data/transcripts/` are accepted. Results are committed back by the Action.

## Consequences
- Every run leaves a permanent, reviewable trail in git and in issues.
- Pushes made by the Action with `GITHUB_TOKEN` do not trigger other workflows; the dashboard deploy (Phase 8) must listen for this workflow finishing instead.
- Findings are measured on the draft before revision, so some issues may already be fixed; they are labelled with a note asking a person to confirm.
