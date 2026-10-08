"""Rule-based source checks for research claims. No AI, so the results are predictable.

For every claim we check:
  1. grade        - A (official/primary), B (respected), C (community), D (unknown)
  2. link_found   - the link really appeared in this run's search results (no invented links)
  3. quote_found  - the quote matches text Claude cited from that page
  4. stale        - the source is older than the agent's freshness limit
  5. corroborated - a claim with a number has a second source from a different site
  6. safe         - the claim and quote contain no prompt-injection text
"""

from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse

from packages.agents.guardrails.checks import find_injection, mask_pii

GRADE_A_SUFFIXES = (".gov", ".mil", ".edu", ".int", ".gov.uk", ".gc.ca", ".gov.au", ".ac.uk")
GRADE_A_DOMAINS = {
    "europa.eu", "nist.gov", "owasp.org", "iso.org", "w3.org", "ietf.org", "oecd.org", "oecd.ai",
    "arxiv.org", "acm.org", "ieee.org", "nature.com", "science.org", "who.int",
    "pair.withgoogle.com", "ai.google", "learn.microsoft.com", "ico.org.uk",
}
GRADE_B_DOMAINS = {
    "reuters.com", "apnews.com", "bloomberg.com", "ft.com", "wsj.com", "nytimes.com", "economist.com",
    "bbc.co.uk", "bbc.com", "theverge.com", "techcrunch.com", "wired.com", "arstechnica.com",
    "gartner.com", "forrester.com", "mckinsey.com", "bcg.com", "deloitte.com", "hbr.org",
    "statista.com", "pewresearch.org", "cbinsights.com", "a16z.com", "microsoft.com", "google.com",
    "anthropic.com", "openai.com", "github.blog", "stackoverflow.blog",
}
GRADE_C_DOMAINS = {
    "reddit.com", "quora.com", "news.ycombinator.com", "stackoverflow.com", "medium.com",
    "substack.com", "producthunt.com", "x.com", "twitter.com", "youtube.com", "linkedin.com",
    "facebook.com", "dev.to", "trustpilot.com", "g2.com", "capterra.com",
}

NUMBER_RE = re.compile(r"\d[\d,.]*\s*(?:%|percent|million|billion|thousand|k\b|m\b|bn\b)|[$€£]\s?\d", re.IGNORECASE)


def domain_of(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def _matches(host: str, domains: set[str]) -> bool:
    return any(host == d or host.endswith("." + d) for d in domains)


def site_of(url: str) -> str:
    """Registered site, e.g. 'blog.example.co.uk' -> 'example.co.uk'. Used to count independent sources."""
    parts = domain_of(url).split(".")
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in {"co", "com", "ac", "gov", "org", "net"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def grade_url(url: str, source_type: str = "") -> str:
    host = domain_of(url)
    if ("." + host).endswith(GRADE_A_SUFFIXES) or _matches(host, GRADE_A_DOMAINS):
        return "A"
    if _matches(host, GRADE_B_DOMAINS):
        return "B"
    if _matches(host, GRADE_C_DOMAINS):
        return "C"
    # A company's own page is the primary source for facts about that company
    # (its pricing, features). It is self-reported, so it gets B, not A.
    if source_type == "company_own_page":
        return "B"
    return "D"


def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    return f"{domain_of(url)}{parsed.path.rstrip('/')}"


MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


def parse_date(text: str | None) -> date | None:
    """Accepts YYYY-MM-DD, YYYY-MM, 'March 3, 2025', 'Mar 2025' or YYYY. Anything else counts as unknown."""
    if not text:
        return None
    iso = re.search(r"\b((?:19|20)\d{2})-(\d{2})(?:-(\d{2}))?\b", text)
    named = re.search(r"\b([A-Za-z]{3})[a-z]*\.?\s+(?:(\d{1,2}),?\s+)?((?:19|20)\d{2})\b", text)
    year_only = re.search(r"\b((?:19|20)\d{2})\b", text)
    try:
        if iso:
            return date(int(iso.group(1)), int(iso.group(2)), int(iso.group(3) or 1))
        if named and named.group(1).lower() in MONTHS:
            return date(int(named.group(3)), MONTHS[named.group(1).lower()], int(named.group(2) or 1))
        if year_only:
            return date(int(year_only.group(1)), 1, 1)
    except ValueError:
        return None
    return None


def _squash(text: str) -> str:
    return re.sub(r"\W+", " ", text.lower()).strip()


def quote_found(quote: str, cited_texts: list[str]) -> bool:
    """True if the quote (or most of its words) appears in text Claude cited."""
    q = _squash(quote)
    if not q:
        return False
    for cited in cited_texts:
        c = _squash(cited)
        if q in c or c in q:
            return True
        q_words = set(q.split())
        if len(q_words) >= 5 and len(q_words & set(c.split())) / len(q_words) >= 0.8:
            return True
    return False


def check_claims(
    claims: list[dict],
    search_results: dict[str, dict],
    citations: dict[str, list[str]],
    stale_after_days: int,
    today: date | None = None,
) -> tuple[list[dict], list[dict]]:
    """Return (accepted, rejected). Each claim gets a `checks` dict explaining the result."""
    today = today or date.today()
    known = {normalize_url(u) for u in search_results} | {normalize_url(u) for u in citations}
    cited_by_url = {normalize_url(u): texts for u, texts in citations.items()}

    accepted, rejected = [], []
    for raw in claims:
        claim = {k: str(raw.get(k, "") or "") for k in ("claim", "url", "quote", "published", "topic", "source_type")}
        claim["claim"], _ = mask_pii(claim["claim"])
        claim["quote"], _ = mask_pii(claim["quote"])
        key = normalize_url(claim["url"])

        page_age = search_results.get(claim["url"], {}).get("page_age") or ""
        published = parse_date(claim["published"]) or parse_date(page_age)
        checks = {
            "grade": grade_url(claim["url"], claim["source_type"]),
            "link_found": bool(claim["url"]) and key in known,
            "quote_found": quote_found(claim["quote"], cited_by_url.get(key, [])),
            "published": published.isoformat() if published else "unknown",
            "stale": bool(published) and (today - published).days > stale_after_days,
            "has_number": bool(NUMBER_RE.search(claim["claim"])),
            "safe": not find_injection(claim["claim"] + "\n" + claim["quote"]),
        }
        claim["checks"] = checks

        if not checks["link_found"]:
            claim["rejected_because"] = "link did not appear in the search results"
            rejected.append(claim)
        elif not checks["safe"]:
            claim["rejected_because"] = "contains prompt-injection text"
            rejected.append(claim)
        elif checks["grade"] == "C" and checks["has_number"]:
            claim["rejected_because"] = "community source used for a number"
            rejected.append(claim)
        else:
            accepted.append(claim)

    # Numbers need two independent sites on the same topic.
    for claim in accepted:
        if claim["checks"]["has_number"]:
            sites = {site_of(c["url"]) for c in accepted if c["topic"] == claim["topic"]}
            claim["checks"]["corroborated"] = len(sites) >= 2
    return accepted, rejected


def labels(claim: dict) -> list[str]:
    """Short warning labels shown next to a claim in the PRD."""
    c = claim["checks"]
    out = []
    if c["grade"] == "D":
        out.append("unknown source")
    if not c["quote_found"]:
        out.append("quote not confirmed")
    if c["has_number"] and not c.get("corroborated"):
        out.append("single source")
    if c["stale"]:
        out.append("may be outdated")
    elif c["published"] == "unknown":
        out.append("date unknown")
    return out
