"""Settings for the three research agents. Change limits and site lists here."""

# Official sources only, for laws, standards and responsible-AI rules.
STANDARDS_DOMAINS = [
    "nist.gov",            # AI Risk Management Framework, cybersecurity
    "owasp.org",           # OWASP Top 10, Top 10 for LLM Applications
    "eur-lex.europa.eu",   # EU AI Act, GDPR (official legal texts)
    "europa.eu",           # European Commission guidance
    "iso.org",             # ISO/IEC 42001, 27001
    "w3.org",              # WCAG accessibility
    "ftc.gov",             # US consumer protection, AI and advertising rules
    "learn.microsoft.com", # Microsoft Responsible AI Standard and guidance
    "microsoft.com",       # Responsible AI resources
    "pair.withgoogle.com", # Google People + AI Guidebook
    "ai.google",           # Google AI principles
    "oecd.ai",             # OECD AI principles
    "copyright.gov",       # US Copyright Office (AI-generated content)
    "ico.org.uk",          # UK data protection guidance
]

# Search limits were 8 / 6 / 5. A real run (2026-10-09) showed each search adds ~25-35k tokens of
# page text (research was ~$2.47 of a $5.93 run). Cut to 2 / 2 / 1 (and 1 / 1 / 1 in --lean mode) to bring a run near $1.
AGENTS = {
    "market": {
        "title": "Market research",
        "max_searches": 2,
        "allowed_domains": None,  # open web; every source is graded instead
        "stale_after_days": 730,
    },
    "standards": {
        "title": "Industry standards and regulation",
        "max_searches": 2,
        "allowed_domains": STANDARDS_DOMAINS,
        "stale_after_days": 365,
    },
    "tech": {
        "title": "Technical build research",
        "max_searches": 1,
        "allowed_domains": None,
        "stale_after_days": 730,
    },
}
