"""Scorer: rates the idea on the scorecard after the debate.

Claude runs GUCCI, then scores each criterion with a named framework and evidence.
Plain code then checks the answer and computes the verdict (Go / Pivot / No-Go), so
the verdict always follows the written rules in scorecard.json.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from packages.agents.common import create_message, estimate_cost, text_of, usage_dict

HERE = Path(__file__).parent
SCORECARD_PATH = HERE.parents[1] / "frameworks" / "scorecard.json"
EFFORT = "high"
GUCCI_KEYS = ["goals_mission", "unmet_needs", "competition", "customer_segmentation", "integrated_ecosystem"]


class ScorerError(RuntimeError):
    """The Scorer did not return a usable result."""


def load_scorecard() -> dict:
    return json.loads(SCORECARD_PATH.read_text())


def output_schema(scorecard: dict) -> dict:
    finding = {
        "type": "object",
        "properties": {"finding": {"type": "string"}, "evidence": {"type": "string"}},
        "required": ["finding", "evidence"],
        "additionalProperties": False,
    }
    score = {
        "type": "object",
        "properties": {
            "criterion": {"type": "string", "enum": [c["id"] for c in scorecard["criteria"]]},
            "score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
            "frameworks": {"type": "array", "items": {"type": "string"}},
            "evidence": {"type": "string"},
            "rationale": {"type": "string"},
        },
        "required": ["criterion", "score", "frameworks", "evidence", "rationale"],
        "additionalProperties": False,
    }
    strings = {"type": "array", "items": {"type": "string"}}
    return {
        "type": "object",
        "properties": {
            "gucci": {
                "type": "object",
                "properties": {k: finding for k in GUCCI_KEYS},
                "required": GUCCI_KEYS,
                "additionalProperties": False,
            },
            "scores": {"type": "array", "items": score},
            "top_strengths": strings,
            "top_risks": strings,
            "unresolved_concerns": strings,
            "summary": {"type": "string"},
        },
        "required": ["gucci", "scores", "top_strengths", "top_risks", "unresolved_concerns", "summary"],
        "additionalProperties": False,
    }


# Other names people use for each framework in scorecard.json (matched as whole words).
FRAMEWORK_ALIASES = {
    "JTBD": ["jtbd", "jobs-to-be-done", "jobs to be done"],
    "CIRCLES": ["circles"],
    "Porter's Five Forces": ["porter", "five forces"],
    "SWOT": ["swot"],
    "Value Proposition Canvas": ["value proposition canvas", "value proposition"],
    "Kano Model": ["kano"],
    "Cagan Four Risks": ["cagan", "four risks", "four big risks", "4 risks"],
    "Google HEART": ["heart"],
    "RICE": ["rice"],
    "Lean Canvas": ["lean canvas"],
    "TAM/SAM/SOM": ["tam", "sam", "som", "tam/sam/som"],
    "AARRR": ["aarrr", "pirate metrics"],
    "Microsoft Responsible AI Standard": ["microsoft responsible ai", "responsible ai standard"],
    "Google PAIR": ["pair", "people + ai", "people and ai"],
    "NIST AI RMF": ["nist", "ai rmf"],
    "EU AI Act": ["eu ai act", "ai act"],
    "7 Powers": ["7 powers", "seven powers", "helmer"],
}


def _framework_ok(named: list[str], allowed: list[str]) -> bool:
    """True if any named framework matches one allowed for the criterion."""
    text = " | ".join(named).lower()
    for a in allowed:
        base = a.split(" (")[0]
        for alias in FRAMEWORK_ALIASES.get(base, [base.lower()]):
            if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", text):
                return True
    return False


def validate(result: dict, scorecard: dict) -> tuple[dict[str, dict], list[str]]:
    """Return (scores by criterion id, list of problems). Problems are recorded, not fatal."""
    issues = []
    by_id: dict[str, dict] = {}
    for s in result["scores"]:
        if s["criterion"] in by_id:
            issues.append(f"{s['criterion']}: scored twice; kept the first score")
            continue
        by_id[s["criterion"]] = s
    for c in scorecard["criteria"]:
        s = by_id.get(c["id"])
        if not s:
            issues.append(f"{c['id']}: missing score")
            continue
        if not _framework_ok(s["frameworks"], c["frameworks"]):
            issues.append(f"{c['id']}: no listed framework named (expected one of: {', '.join(c['frameworks'])})")
        if not s["evidence"].strip():
            issues.append(f"{c['id']}: no evidence given")
    for k in GUCCI_KEYS:
        if not result["gucci"][k]["finding"].strip():
            issues.append(f"GUCCI {k}: empty")
    return by_id, issues


def verdict(scores: dict[str, dict], scorecard: dict) -> tuple[str, float]:
    """Apply the written rules in scorecard.json. Missing criteria count as 1 (unproven)."""
    values = {c["id"]: scores.get(c["id"], {}).get("score", 1) for c in scorecard["criteria"]}
    average = round(sum(values.values()) / len(values), 2)
    if average < 2.5 or values.get("ethics") == 1:
        return "no_go", average
    if average >= 3.5 and min(values.values()) >= 3:
        return "go", average
    return "pivot", average


@dataclass
class ScoreResult:
    gucci: dict
    scores: dict[str, dict]
    verdict: str
    average: float
    top_strengths: list[str]
    top_risks: list[str]
    unresolved_concerns: list[str]
    summary: str
    issues: list[str]
    model: str
    usage: dict = field(default_factory=dict)

    @property
    def cost_usd(self) -> float:
        return estimate_cost(self.usage)

    def to_json(self) -> dict:
        return {
            "verdict": self.verdict, "average": self.average, "gucci": self.gucci,
            "scores": self.scores, "top_strengths": self.top_strengths, "top_risks": self.top_risks,
            "unresolved_concerns": self.unresolved_concerns, "summary": self.summary,
            "issues": self.issues, "model": self.model, "usage": self.usage, "cost_usd": self.cost_usd,
        }

    def brief_for_prd(self, scorecard: dict) -> str:
        """Compact text for the PRD Writer: GUCCI, the score table and the verdict."""
        names = {c["id"]: c["name"] for c in scorecard["criteria"]}
        lines = ["GUCCI:"]
        for k in GUCCI_KEYS:
            g = self.gucci[k]
            lines.append(f"- {k.replace('_', ' ').title()}: {g['finding']} (evidence: {g['evidence']})")
        lines += ["", "| Criterion | Score | Framework(s) | Evidence | Rationale |", "|---|---|---|---|---|"]
        for c in scorecard["criteria"]:
            s = self.scores.get(c["id"])
            if s:
                lines.append(f"| {names[c['id']]} | {s['score']}/5 | {', '.join(s['frameworks'])} | "
                             f"{s['evidence']} | {s['rationale']} |")
            else:
                lines.append(f"| {names[c['id']]} | not scored | | | |")
        lines += ["", f"Average: {self.average} -> Verdict: {self.verdict.upper().replace('_', '-')}",
                  f"Summary: {self.summary}"]
        if self.unresolved_concerns:
            lines.append("Unresolved Skeptic concerns:")
            lines += [f"- {u}" for u in self.unresolved_concerns]
        if self.issues:
            lines.append("Scoring issues found by checks: " + "; ".join(self.issues))
        return "\n".join(lines)


def run_scorer(transcript: str, research: str = "", debate_md: str = "", client=None) -> ScoreResult:
    scorecard = load_scorecard()
    user = "\n\n".join(filter(None, [
        f"<scorecard>\n{json.dumps(scorecard, indent=2)}\n</scorecard>",
        f"<transcript>\n{transcript.strip()}\n</transcript>",
        f"<research>\n{research.strip()}\n</research>" if research else "",
        f"<debate>\n{debate_md.strip()}\n</debate>" if debate_md else "",
        "Run GUCCI, then score every criterion.",
    ]))
    message = create_message(
        client, system=(HERE / "prompt.md").read_text(), user=user, effort=EFFORT,
        error=ScorerError, label="scorer",
        output_format={"type": "json_schema", "schema": output_schema(scorecard)},
    )
    try:
        result = json.loads(text_of(message))
    except json.JSONDecodeError as e:
        raise ScorerError(f"scorer: answer was not valid JSON: {e}") from e

    scores, issues = validate(result, scorecard)
    decision, average = verdict(scores, scorecard)
    return ScoreResult(
        gucci=result["gucci"], scores=scores, verdict=decision, average=average,
        top_strengths=result["top_strengths"], top_risks=result["top_risks"],
        unresolved_concerns=result["unresolved_concerns"], summary=result["summary"],
        issues=issues, model=message.model, usage=usage_dict(message),
    )
