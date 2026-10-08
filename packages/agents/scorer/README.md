# Scorer (Phase 4)

Reads the transcript, research and full debate, then:

1. Runs **GUCCI** (Goals & Mission, Unmet Needs, Competition, Customer Segmentation, Integrated Ecosystem).
2. Scores the 10 criteria in [`scorecard.json`](../../frameworks/scorecard.json) from 1 to 5. Each score names a framework and gives evidence.
3. Lists unresolved Skeptic concerns.

**Plain code then checks the answer:**
- Every criterion scored once, with evidence.
- At least one framework named that is listed for that criterion. Common alternative names count: "Marty Cagan's Four Big Risks" = Cagan Four Risks, "Jobs to be Done" = JTBD.
- Problems are recorded in `issues`, not hidden.

**The verdict is computed by code**, from the written rules, so it can't drift:

| Verdict | Rule |
|---|---|
| Go | Average ≥ 3.5 and every criterion ≥ 3 |
| No-Go | Average < 2.5, or ethics = 1 |
| Pivot | Everything in between |

A missing score counts as 1 ("unproven"). Output: `data/outputs/<name>/scorecard.json`. The PRD Writer copies the scores into section 16 without changing them.
