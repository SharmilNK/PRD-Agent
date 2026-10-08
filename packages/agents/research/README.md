# Research agents (Phase 3)

Three agents search the web at the same time and give the PRD Writer **checked** facts with sources.

| Agent | Max searches | Which sites | Freshness limit |
|---|---|---|---|
| Market | 8 | Open web (every source is graded) | 2 years |
| Standards | 6 | Official sites only (NIST, OWASP, EU law, ISO, W3C, FTC, Microsoft/Google responsible-AI pages, ...) | 1 year |
| Tech | 5 | Open web (every source is graded) | 2 years |

Change these numbers and the site list in [`config.py`](config.py). Search cost is about $0.01 per search (max ~$0.19 per run), plus tokens.

## How sources are checked ([`sources.py`](sources.py), plain code, no AI)

| Check | What it means | If it fails |
|---|---|---|
| **Grade** | A = official/primary, B = respected, C = community, D = unknown | D is marked "unknown source" |
| **Link found** | The link really appeared in this run's search results | Claim rejected (stops invented links) |
| **Quote found** | The quote matches text Claude cited from that page | Marked "quote not confirmed" |
| **Fresh** | Published within the freshness limit | Marked "may be outdated" / "date unknown" |
| **Corroborated** | A number has a second source from a different site | Marked "single source" |
| **Community + number** | Forums can't be the source of a number | Claim rejected |
| **Safe** | No prompt-injection text in the claim or quote | Claim rejected |

Personal data in quotes is masked with the same rules as the Guardrails agent.

## Outputs
- `data/outputs/<name>/research/<agent>.json`: every claim with its checks, plus rejected claims and why
- `data/outputs/<name>/research_brief.md`: the short brief the PRD Writer reads

If one research agent fails (for example a rate limit), the run continues and the PRD marks that area **[NEEDS RESEARCH]**.
