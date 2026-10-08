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

## Gmail alerts (Phase 7), with `--alert`
`notify.py` emails you a short summary when:

| Event | When |
|---|---|
| `new` | A PRD was written for a transcript that had none |
| `updated` | The PRD changed (the email lists which sections were added, changed or removed) |
| `blocked` | Guardrails stopped the run |
| `quality_fail` | The quality gate failed |
| `error` | A pipeline step failed |

The email shows: the verdict, the scores, the quality gate, the Reviewer score, whether the PRD was revised, the cost, the changed sections, and links to the PRD, the run log, the issues and the dashboard. No email is sent if nothing changed and nothing went wrong. To get only some alerts, set `ALERT_ON`, e.g. `ALERT_ON=blocked,quality_fail,error`.

**Setup (Gmail app password):**
1. Use a Gmail account with **2-Step Verification** turned on (Google Account → Security).
2. Create an **app password**: Google Account → Security → App passwords. Copy the 16-character password. Some school or work accounts don't allow app passwords; a personal Gmail account works.
3. Set these as environment variables (locally) or as repository secrets (for the GitHub Action):
   - `GMAIL_ADDRESS`: the sending Gmail address
   - `GMAIL_APP_PASSWORD`: the app password
   - `ALERT_TO`: who receives alerts (comma-separated; defaults to `GMAIL_ADDRESS`)
   - optional repository *variable* `DASHBOARD_URL`: link shown in the email

**Not set up yet?** Nothing is sent; the email is saved as `data/outputs/<name>/alert.eml` (git-ignored) so you can open it and see what it would look like.

**Privacy:** the password is never written to logs, metrics or files. Metrics record only whether an alert was sent and how many people received it, never the addresses.
