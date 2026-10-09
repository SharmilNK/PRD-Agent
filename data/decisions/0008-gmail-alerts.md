# ADR-0008: Gmail alerts on PRD changes, sent over SMTP with an app password

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
The founder wants an email when a PRD is created or updated, and when something goes wrong, without checking GitHub.

## Decision
- **Events:** `new`, `updated` (section-by-section comparison with the PRD from before the run), `blocked`, `quality_fail`, `error`. No email when nothing changed and nothing failed. `ALERT_ON` filters events.
- **Delivery:** Gmail SMTP (`smtp.gmail.com:465`, TLS) with an app password, using only the Python standard library. This works the same on a laptop and in GitHub Actions.
- **Why not the Gmail MCP connector:** it works inside a Claude session, but the pipeline runs as a normal program (and in GitHub Actions), where MCP connectors aren't available. SMTP is the standard choice for a program sending its own alerts.
- **Safety:** all dynamic text in the HTML email is escaped (model output could contain HTML). The password and addresses never appear in logs or committed metrics; saved `alert.eml` files are git-ignored.
- Alerts run in `publish`, after GitHub issues (so the email can link them), and can never lose a PRD.

## Consequences
- One-time setup: a Gmail app password (needs 2-Step Verification). Some school or work accounts block app passwords.
- Slack alerts are not built; they could reuse the same alert text later.
