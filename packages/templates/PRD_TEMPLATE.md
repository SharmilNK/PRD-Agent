# PRD: {{product_name}}

| Field | Value |
|---|---|
| Owner | {{owner}} |
| Status | Draft |
| Version | 0.1 |
| Last updated | {{date}} |
| Reviewers | {{reviewers}} |

> Each section names the public source it is based on. See `packages/templates/SOURCES.md`.
> Markers: **[ASSUMPTION]** = not confirmed, **[NEEDS RESEARCH]** = must be checked with real data, **[OPEN QUESTION]** = needs a decision.

## 1. Press Release and FAQ
_Based on: Amazon "Working Backwards" PR/FAQ._
- One-paragraph press release written as if the product just launched (headline, who it is for, the problem, the solution, a customer quote).
- 3-5 customer FAQs and 3-5 internal FAQs.

## 2. Problem Statement and Why Now
_Based on: Marty Cagan / SVPG (problem before solution); GUCCI (U - Unmet Needs)._
- The problem in plain words, who has it, how often, and how painful it is.
- Why now (technology, market or behavior change).

## 3. Strategic Fit (GUCCI)
_Based on: GUCCI (Dr. Nancy Li)._
- Goals & Mission, Unmet Needs, Competition, Customer Segmentation, Integrated Ecosystem.

## 4. Target Users and Jobs-to-be-Done
_Based on: JTBD (Christensen / Ulwick); CIRCLES (I - Identify the customer)._
- Primary persona, secondary personas, early-adopter segment.
- Job statements: "When ___, I want to ___, so I can ___."

## 5. Market and Competitive Analysis
_Based on: Porter's Five Forces; Lean Canvas (TAM/SAM/SOM); SWOT._
- Market size estimate, top competitors and substitutes, our differentiation.

## 6. Goals, Non-Goals and Success Metrics
_Based on: Google design docs (goals / non-goals); Google HEART; North Star metric._
- Goals, explicit non-goals.
- North Star metric, HEART metrics, guardrail metrics (what must not get worse).

## 7. User Stories and Key Flows
_Based on: CIRCLES (R - Report customer needs); Lenny Rachitsky PRD templates._
- "As a ___, I want ___ so that ___" with acceptance criteria.
- Main user journey step by step.

## 8. Requirements and Prioritization
_Based on: RICE (Intercom); MoSCoW; Kano Model._
- Functional requirements table: ID, requirement, MoSCoW, Kano type, RICE score.

## 9. AI System Design
_Based on: Google PAIR Guidebook; Google Model Cards._
- Does this need AI? (AI-fit). Where AI is used and where it is not.
- Model choice, data sources, prompt strategy, evaluation plan and quality targets.
- Failure handling: what happens when the AI is wrong; human-in-the-loop points.
- Cost per request and latency budget.

## 10. Security and Privacy
_Based on: OWASP Top 10; OWASP Top 10 for LLM Applications; GDPR / CCPA._
- Authentication and authorization, encryption, secrets management.
- LLM risks: prompt injection, sensitive data leakage, insecure output handling, excessive agency.
- Personal data collected, retention, user rights.

## 11. Responsible AI
_Based on: Microsoft Responsible AI Standard v2 and Impact Assessment; NIST AI RMF; EU AI Act._
- Fairness, reliability and safety, privacy, inclusiveness, transparency, accountability.
- EU AI Act risk level and disclosure duties (e.g., "this content is AI-assisted").

## 12. Explainability
_Based on: Google PAIR (explainability + trust); Google Model Cards._
- How users see why the AI produced an output: sources, citations, confidence, limits.

## 13. Observability and Operations
_Based on: Google SRE practices; LLM observability practice (tracing, evals in production)._
- Logs, traces, prompt/response tracking, quality monitoring, cost and latency dashboards, alerts.
- Prompt and model versioning; re-evaluation when the model changes.

## 14. Technical Architecture and Non-Functional Requirements
_Based on: Google design docs (alternatives considered)._
- High-level architecture, build vs. buy, alternatives considered.
- Performance, scalability, availability, accessibility (WCAG 2.2 AA).

## 15. Pricing and Go-to-Market
_Based on: Lean Canvas (revenue, channels); AARRR pirate metrics._
- Pricing tiers, channels, launch audience, growth loops.

## 16. Product Evaluation Scorecard
_Based on: `packages/frameworks/scorecard.json` (Cagan Four Risks, GUCCI, Kano, HEART, 7 Powers, Responsible AI frameworks)._
- Table: criterion, score (1-5), framework used, evidence. Verdict: Go / Pivot / No-Go.

## 17. Risks, Assumptions and Open Questions
_Based on: Cagan Four Risks; NIST AI RMF (Map / Manage)._
- Risk table: risk, likelihood, impact, mitigation, owner.
- Assumptions list and open questions.

## 18. Launch Plan and Rollback
_Based on: staged rollout practice (alpha / beta / GA) common at Google, Microsoft and Meta._
- Milestones, exit criteria for each stage, rollback plan, kill criteria.

## 19. Decision Log and Appendix
_Based on: Architecture Decision Records (Michael Nygard)._
- Key decisions with date and reason; glossary.
- **Sources** table: title or site, link, grade (A/B/C/D), date, sections that use it.
