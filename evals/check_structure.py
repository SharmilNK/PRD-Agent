"""Structure check: does a PRD contain every section of the template?

This is the first, simplest eval. It checks shape, not quality.

Usage:
    python -m evals.check_structure data/outputs/storyml-newsletter/PRD.md
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "packages" / "templates" / "PRD_TEMPLATE.md"
SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
MARKERS = ("[ASSUMPTION]", "[NEEDS RESEARCH]", "[OPEN QUESTION]")
SCORECARD_FRAMEWORKS = ("GUCCI", "CIRCLES", "JTBD", "Kano", "HEART", "RICE", "Porter", "Cagan", "7 Powers", "PAIR")


def template_sections(template: str | None = None) -> list[tuple[str, str]]:
    text = template if template is not None else TEMPLATE_PATH.read_text()
    return SECTION_RE.findall(text)


def _norm(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def check_prd(prd: str, template: str | None = None) -> dict:
    expected = template_sections(template)
    found = {(num, _norm(title)) for num, title in SECTION_RE.findall(prd)}
    missing = [f"{num}. {title}" for num, title in expected if (num, _norm(title)) not in found]

    scorecard = _section_body(prd, "16")
    frameworks_named = [f for f in SCORECARD_FRAMEWORKS if f.lower() in scorecard.lower()]

    return {
        "passed": not missing and bool(frameworks_named),
        "sections_expected": len(expected),
        "sections_found": len(expected) - len(missing),
        "missing_sections": missing,
        "scorecard_frameworks_named": frameworks_named,
        "markers": {m: prd.count(m) for m in MARKERS},
    }


def _section_body(prd: str, number: str) -> str:
    match = re.search(rf"^##\s+{number}\.\s+.*?$(.*?)(?=^##\s+\d+\.|\Z)", prd, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    result = check_prd(Path(argv[0]).read_text())
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
