"""Free quality checks on a finished PRD (plain code, no AI).

  - structure:   all 19 template sections, frameworks named in the scorecard section
  - links:       every link in the PRD came from the checked research (no invented links)
  - scores:      section 16 scores match scorecard.json exactly
  - readability: average sentence length (plain-language goal: 20 words or fewer)

Usage:
    python -m evals.quality_checks data/outputs/storyml-newsletter
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from evals.check_structure import _section_body, check_prd

LINK_RE = re.compile(r"https?://[^\s)\]>|\"'`]+")
SCORE_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(\d)\s*/\s*5\s*\|", re.MULTILINE)
MAX_AVG_SENTENCE_WORDS = 20


def _norm_url(url: str) -> str:
    url = url.rstrip(".,;:")
    url = re.sub(r"^https?://(www\.)?", "", url.lower())
    return url.rstrip("/")


def check_links(prd: str, allowed_urls: set[str]) -> dict:
    found = {u.rstrip(".,;:") for u in LINK_RE.findall(prd)}
    allowed = {_norm_url(u) for u in allowed_urls}
    unknown = sorted(u for u in found if _norm_url(u) not in allowed)
    return {"links": len(found), "unknown_links": unknown, "passed": not unknown}


def check_scores(prd: str, scorecard: dict | None, criteria_names: dict[str, str]) -> dict:
    """Compare the score table in section 16 with scorecard.json (if there is one)."""
    if not scorecard:
        return {"checked": False, "passed": True, "mismatches": []}
    table = {name.strip().lower(): int(score) for name, score in SCORE_ROW_RE.findall(_section_body(prd, "16"))}
    mismatches = []
    for cid, s in scorecard["scores"].items():
        name = criteria_names.get(cid, cid).lower()
        got = table.get(name)
        if got != s["score"]:
            mismatches.append(f"{criteria_names.get(cid, cid)}: scorecard {s['score']}, PRD {got if got else 'missing'}")
    return {"checked": True, "passed": not mismatches, "mismatches": mismatches}


def readability(prd: str) -> dict:
    text = re.sub(r"```.*?```", " ", prd, flags=re.DOTALL)
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith(("|", "#"))]
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", " ".join(lines)) if len(s.split()) >= 3]
    avg = round(sum(len(s.split()) for s in sentences) / len(sentences), 1) if sentences else 0.0
    return {"avg_sentence_words": avg, "passed": avg <= MAX_AVG_SENTENCE_WORDS}


def run_checks(prd: str, allowed_urls: set[str], scorecard: dict | None, criteria_names: dict[str, str]) -> dict:
    result = {
        "structure": check_prd(prd),
        "links": check_links(prd, allowed_urls),
        "scores": check_scores(prd, scorecard, criteria_names),
        "readability": readability(prd),
    }
    result["passed"] = all(result[k]["passed"] for k in ("structure", "links", "scores"))
    return result


def allowed_urls_from(out_dir: Path) -> set[str]:
    """Links the PRD may use: accepted claims from the research step."""
    urls = set()
    for f in (out_dir / "research").glob("*.json"):
        urls |= {c["url"] for c in json.loads(f.read_text()).get("accepted", [])}
    return urls


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    from packages.agents.scorer.agent import load_scorecard

    out_dir = Path(argv[0])
    card = out_dir / "scorecard.json"
    names = {c["id"]: c["name"] for c in load_scorecard()["criteria"]}
    result = run_checks((out_dir / "PRD.md").read_text(), allowed_urls_from(out_dir),
                        json.loads(card.read_text()) if card.exists() else None, names)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
