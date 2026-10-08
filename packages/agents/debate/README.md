# Debate: Advocate vs. Skeptic (Phase 4)

| | Advocate | Skeptic |
|---|---|---|
| Sees | Transcript, guardrail notes, research, the debate | **Only** the pitch and the debate |
| Job | Make the strongest honest case; concede what it can't support | Challenge like an experienced investor seeing the idea cold |

**Why the Skeptic has no background:** real customers and investors only see the pitch. If the idea needs insider knowledge to make sense, the Skeptic will expose it.

**Flow (2 rounds, 6 calls):** pitch → Skeptic challenges → Advocate answers → Skeptic challenges → Advocate answers → Skeptic closing statement (Resolved / Unresolved).

Every call is built from scratch, so the code (and a test) can prove the Skeptic never receives the transcript, research or notes.

Change the number of rounds with `ROUNDS` in [`agent.py`](agent.py). Output: `data/outputs/<name>/debate.md`.

Next step: the [Scorer](../scorer/) reads the whole debate.
