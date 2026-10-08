"""Rule-based guardrail checks. Fast, free, and run before any AI call.

- mask_pii: replaces personal data and secrets with placeholders such as [EMAIL].
- find_injection: spots common prompt-injection phrases.

These catch the obvious cases. The Claude review in agent.py catches the rest.
"""

from __future__ import annotations

import re

MAX_CHARS = 200_000

# Order matters: secrets and cards before phone numbers, so long digit runs are labeled correctly.
PII_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("SECRET", re.compile(
        r"\b(?:sk-[A-Za-z0-9_-]{16,}|sk-ant-[A-Za-z0-9_-]{16,}|AKIA[0-9A-Z]{16}"
        r"|gh[pousr]_[A-Za-z0-9]{30,}|xox[abpr]-[A-Za-z0-9-]{10,})\b"
    )),
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("CARD", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("IP", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")),
    ("PHONE", re.compile(r"(?<!\w)(?:\+?\d{1,3}[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]?\d{3}[ .-]?\d{4}\b")),
]

INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"ignore (?:all |any )?(?:the )?(?:previous|prior|above|earlier) (?:instructions|rules|prompts?)",
        r"disregard (?:all |any )?(?:the )?(?:previous|prior|above|earlier|your) (?:instructions|rules)",
        r"forget (?:all |everything )?(?:you were told|your instructions|previous instructions)",
        r"\byou are now\b",
        r"\bact as (?:a |an )?(?:different|new|unrestricted)\b",
        r"(?:reveal|print|show|repeat) (?:your |the )?(?:system prompt|hidden instructions|instructions above)",
        r"\bnew instructions\s*:",
        r"\bdeveloper mode\b|\bjailbreak\b|\bDAN mode\b",
        r"</?(?:system|transcript|guardrail_notes)>",
    ]
]


def _luhn_ok(digits: str) -> bool:
    total, parity = 0, len(digits) % 2
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def mask_pii(text: str) -> tuple[str, dict[str, int]]:
    """Return (masked text, count per PII type). Counts only; the values are never stored."""
    counts: dict[str, int] = {}

    for label, pattern in PII_PATTERNS:
        def replace(match: re.Match, label=label) -> str:
            digits = re.sub(r"\D", "", match.group())
            if label == "CARD" and not (13 <= len(digits) <= 19 and _luhn_ok(digits)):
                return match.group()
            # Long digit runs without a "+" are usually IDs, not phone numbers.
            if label == "PHONE" and len(digits) > 11 and not match.group().startswith("+"):
                return match.group()
            counts[label] = counts.get(label, 0) + 1
            return f"[{label}]"

        text = pattern.sub(replace, text)
    return text, counts


def find_injection(text: str) -> list[str]:
    """Return the suspicious phrases found (short snippets, for the report)."""
    hits = []
    for pattern in INJECTION_PATTERNS:
        for match in pattern.finditer(text):
            hits.append(match.group()[:80])
    return hits
