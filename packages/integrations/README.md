# Integrations

## Run log (Phase 6), always on
After every run, `run_log.py` records it in two places that live in git:
- `data/metrics/index.json`: one short summary per run (status, verdict, scores, quality gate, cost, issues). The dashboard reads this.
- `data/decisions/RUN_LOG.md`: the same as a readable table, so every decision has a history.

## GitHub issues (Phase 6), with `--github-issues`
`github_issues.py` turns problems from a run into issues a person can act on:

| Becomes an issue | Labels |
|---|---|
| Critical or major Reviewer finding | `review`, `severity:*`, `area:*` |
| Quote not found on the cited page | `evidence` |
| Quality gate failed | `quality` |
| Run blocked by guardrails | `guardrails` |
| A pipeline step failed | `pipeline-error` |

All issues also get `prd-agent` and `transcript:<name>`.

- **No duplicates:** each issue has a hidden fingerprint built from *what* the problem is (transcript, section, category), not its wording. If the same problem shows up again, the existing issue gets a comment instead of a new issue.
- **Auto-close:** if a later run checked for that kind of problem and it is gone, the issue is closed with a comment. A run that skipped the review never closes review issues.
- **No token?** Nothing is sent; the plan is saved to `data/outputs/<name>/issues.plan.json`.

Needs `GITHUB_TOKEN` and `GITHUB_REPOSITORY` (set automatically inside GitHub Actions).

## GitHub Action (Phase 6)
`.github/workflows/prd-agent.yml` runs the pipeline when you push a new or changed transcript to `data/transcripts/` on `main`, or by hand from the **Actions** tab ("Run workflow"). It then commits the outputs, metrics and run log back to the repo.

**One-time setup:**
1. Repo **Settings → Secrets and variables → Actions → New repository secret**: name `ANTHROPIC_API_KEY`, value your API key.
2. Repo **Settings → Actions → General → Workflow permissions**: choose **Read and write permissions** (so the Action can commit results and create issues).
