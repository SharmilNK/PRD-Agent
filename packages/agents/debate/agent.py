"""Debate: the Advocate (full context) argues for the idea; the Skeptic (pitch only) challenges it.

Flow (with ROUNDS = 2):
  1. Advocate writes the pitch from the transcript, guardrail notes and research.
  2. Skeptic challenges.  3. Advocate answers.        (round 1)
  4. Skeptic challenges.  5. Advocate answers.        (round 2)
  6. Skeptic closing statement: what is resolved and what is not.

Every call is stateless: we build each prompt from scratch. That is how we guarantee the
Skeptic never sees the transcript or the research, only the pitch and the debate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from packages.agents.common import create_message, estimate_cost, text_of, usage_dict

HERE = Path(__file__).parent
ROUNDS = 2
EFFORT = "medium"


class DebateError(RuntimeError):
    """A debate turn did not return usable text."""


@dataclass
class DebateResult:
    pitch: str
    turns: list[dict]  # {"round": int, "speaker": "skeptic" | "advocate", "text": str}
    closing: str
    model: str
    calls: int = 0
    usage: dict = field(default_factory=dict)

    @property
    def cost_usd(self) -> float:
        return estimate_cost(self.usage)

    def transcript_md(self) -> str:
        """The debate as readable Markdown (saved as debate.md, and read by the Scorer)."""
        parts = ["## Pitch (Advocate)", self.pitch]
        for t in self.turns:
            parts += [f"## Round {t['round']}: {t['speaker'].capitalize()}", t["text"]]
        parts += ["## Closing statement (Skeptic)", self.closing]
        return "\n\n".join(parts) + "\n"


def advocate_context(transcript: str, research: str, notes: list[str]) -> str:
    parts = [f"<transcript>\n{transcript.strip()}\n</transcript>"]
    if notes:
        parts.append("<guardrail_notes>\n" + "\n".join(f"- {n}" for n in notes) + "\n</guardrail_notes>")
    if research:
        parts.append(f"<research>\n{research.strip()}\n</research>")
    return "\n\n".join(parts)


def debate_so_far(pitch: str, turns: list[dict]) -> str:
    """What both sides can see: the pitch and the debate. No transcript, no research."""
    parts = [f"<pitch>\n{pitch.strip()}\n</pitch>"]
    for t in turns:
        parts.append(f"<{t['speaker']} round=\"{t['round']}\">\n{t['text'].strip()}\n</{t['speaker']}>")
    return "\n\n".join(parts)


class _Caller:
    """Runs calls and adds up usage."""

    def __init__(self, client):
        self.client, self.usage, self.calls, self.model = client, {}, 0, ""

    def __call__(self, prompt_file: str, user: str, label: str) -> str:
        message = create_message(
            self.client, system=(HERE / prompt_file).read_text(), user=user,
            effort=EFFORT, error=DebateError, label=label,
        )
        for k, v in usage_dict(message).items():
            self.usage[k] = self.usage.get(k, 0) + v
        self.calls += 1
        self.model = message.model
        return text_of(message)


def run_debate(transcript: str, research: str = "", notes: list[str] | None = None,
               client=None, rounds: int = ROUNDS) -> DebateResult:
    call = _Caller(client)
    context = advocate_context(transcript, research, notes or [])

    pitch = call("advocate.md", context + (
        "\n\nWrite the pitch for this product in at most 400 words: the problem, who it is for, "
        "the solution, why it is better than alternatives, the wow moment, and how it makes money. "
        "Use only evidence from the context above."
    ), "advocate pitch")

    turns: list[dict] = []
    for r in range(1, rounds + 1):
        challenge = call("skeptic.md", debate_so_far(pitch, turns) + (
            f"\n\nThis is round {r} of {rounds}. Give your strongest challenges."
        ), f"skeptic round {r}")
        turns.append({"round": r, "speaker": "skeptic", "text": challenge})

        answer = call("advocate.md", context + "\n\n" + debate_so_far(pitch, turns) + (
            f"\n\nAnswer the Skeptic's round {r} challenges one by one, by number. "
            "Use evidence from your context; concede what you can't support."
        ), f"advocate round {r}")
        turns.append({"round": r, "speaker": "advocate", "text": answer})

    closing = call("skeptic.md", debate_so_far(pitch, turns) + (
        "\n\nThe debate is over. Write a short closing statement with two lists: "
        "'Resolved' (challenges answered well) and 'Unresolved' (still open, with what would settle each)."
    ), "skeptic closing")

    return DebateResult(pitch=pitch, turns=turns, closing=closing, model=call.model,
                        calls=call.calls, usage=call.usage)
