# ADR-0005: Stateless Advocate vs. Skeptic debate, then a Scorer with a code-computed verdict

- **Date:** 2026-10-08
- **Status:** Accepted

## Context
A single agent tends to be too kind to the idea it is writing about. The founder asked for an Advocate with full context and a Skeptic with no context, and for every score to be backed by a named framework.

## Decision
- **Debate:** the Advocate writes a pitch from the transcript, guardrail notes and research. The Skeptic sees only the pitch and the debate. 2 rounds plus a closing statement (6 calls). Each call's prompt is built from scratch, so the "no context" rule is enforced by code and checked by tests, not left to the model.
- **Scorer:** a separate call with full context runs GUCCI, then scores the 10 scorecard criteria with frameworks and evidence, using a JSON schema.
- **Code checks** the scores (every criterion, evidence, a framework listed for that criterion) and **computes the verdict** from the written rules. Verdict rules were clarified: Go = average ≥ 3.5 and every criterion ≥ 3; No-Go = average < 2.5 or ethics = 1; otherwise Pivot.
- The PRD Writer copies the scores into section 16 without changing them and puts unresolved concerns in section 17.
- A failed debate or Scorer does not stop the run.

## Consequences
- Scores are traceable and consistent; the verdict can't be argued up by the model.
- About 7 extra calls per run (debate at medium effort, Scorer at high).
- The Skeptic can still learn facts the Advocate puts in the pitch. That is intended: the pitch is what real readers would see.
