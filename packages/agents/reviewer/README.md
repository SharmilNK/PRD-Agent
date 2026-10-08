# Reviewer (Phase 5)

The last check before anyone relies on the PRD.

**1. Link spot-check.** Opens up to 5 cited sources with web fetch (numbers and A/B sources first) and checks the quote is really on the page.
- When the page text comes back, **plain code** decides (`confirmed` / `not_found`).
- Otherwise Claude's report is used (`confirmed` / `partly` / `not_found` / `fetch_failed`).

**2. Review.** Claude reviews the PRD like a principal PM at a large tech company: logic, evidence, security, responsible AI, explainability, observability, performance, right-sizing, plain language.
- Each finding has a severity (`critical` / `major` / `minor`), a section and a concrete fix.
- The PRD is scored on the 10 criteria in [`evals/rubric.json`](../../../evals/rubric.json).

**3. One revision.** If there are critical or major findings, a quote not found on its page, or a failed free check, the PRD Writer fixes them **once**. The first draft is kept as `PRD.draft.md`.

Outputs: `review.json`, `quality.json`. Settings (`MAX_LINKS`, page size) are in [`agent.py`](agent.py).
