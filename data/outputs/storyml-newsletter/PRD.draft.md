# PRD: StoryML Newsletter (working title)

| Field | Value |
|---|---|
| Owner | Founder (name not given) **[OPEN QUESTION]** |
| Status | Draft |
| Version | 0.1 |
| Last updated | To be set by owner on save **[OPEN QUESTION]** |
| Reviewers | Independent technical reviewer (not yet named) **[OPEN QUESTION]**; 5–10 named practitioner readers (not yet recruited) |

> Each section names the public source it is based on. See `packages/templates/SOURCES.md`.
> Markers: **[ASSUMPTION]** = not confirmed, **[NEEDS RESEARCH]** = must be checked with real data, **[OPEN QUESTION]** = needs a decision.

> **Reading guide.** StoryML is a **content product about AI**. It is not an AI product. The first version is a free newsletter on a hosted platform, with no custom code. The scorecard verdict is **PIVOT** (average 2.7/5). Treat this PRD as the plan for a **bounded 8-issue experiment** that tests the riskiest assumptions before anyone scales the idea. It is not a plan for a full launch.

---

## 1. Press Release and FAQ
_Based on: Amazon "Working Backwards" PR/FAQ._

### Press release (written as if launched)

**StoryML: ML concepts you'll still remember next week**

*Each issue turns one ML/AI idea into a short story, then shows you exactly where the story stops matching the real mechanism.*

Many people who build with AI, or work beside it, are teaching themselves. In one large survey, 75% of knowledge workers used AI at work, but only 39% of AI users had received AI training from their company ([source](https://news.microsoft.com/source/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/), grade B, may be outdated, quote not confirmed). Dense topics such as embeddings, RAGAS (a toolkit for scoring retrieval-augmented generation systems) or drift detection usually come as papers, docs or dry blog posts that are hard to remember. StoryML takes one concept per issue and dramatizes it. A model becomes a character, and the concept becomes a scene with conflict and resolution. In the founder's words: *"Every model, algorithm, or system becomes a character. Every concept becomes a scene."* Evaluation methods are told as courtroom dramas, and production failures as thrillers. Every story ends with a **"Where the story breaks"** box that maps each character to the real mechanism. Each issue also has an optional three-tier quiz: Basic, Intermediate and Expert. Every issue is checked by a technical reviewer who did not write it, and any error is fixed in a public corrections log. *"I'd read three papers on LLM-as-Judge and still couldn't explain its failure modes. After the courtroom issue I could, and the Expert quiz showed me the one edge case I'd missed."* (illustrative quote, not a real customer) **[ASSUMPTION]**

### Customer FAQs

| Question | Answer |
|---|---|
| Do I need an ML background? | No for the story and the plain-language summary. The Basic quiz tier is built for non-technical readers. The Intermediate and Expert tiers assume practitioner knowledge, because practitioners are the primary reader (debate outcome). |
| Are the stories accurate, or just fun? | Each story is written from the real mechanism first. The "Where the story breaks" box lists what the metaphor gets wrong. A second person reviews each issue, and errors go into a public corrections log. |
| Is this written by AI? | The first issues are written by a human. If AI drafting is ever used, every affected issue will say so, with a label that states what the AI did. See sections 10 and 11. |
| Are the quizzes graded or certified? | No. Quizzes are optional self-checks. There are no grades, certificates or records tied to your name. |
| Does it cost money? | It is free during the first 8-issue experiment. A low-priced paid tier may be tested later, and only if readers show they value it (section 15). |

### Internal FAQs

| Question | Answer |
|---|---|
| Why would anyone read this instead of asking ChatGPT for a story? | This is the biggest open question. The debate conceded that our topic list is "a topic list, not a moat." Our bet is on **trust and curation**: an independent accuracy check, a mechanism box and quizzes that test the mechanism. A three-way recall test (full story vs. box only vs. ChatGPT story) must be run before we scale (sections 9 and 17). |
| How will this make money? | We test one model first: a free newsletter, then a low-priced paid tier. The course idea is shelved. We have no willingness-to-pay data yet. |
| Who is the founder, and how will they reach the first 1,000 readers? | Unknown. The Skeptic called this "the deciding issue." **[OPEN QUESTION]** |
| Can one person sustain a weekly cadence? | Unknown. We will record the hours for 3 finished issues before choosing between weekly and every two weeks. |
| Why not make this an AI product? | It does not need AI to deliver value (AI-fit 2/5). AI drafting could also weaken our main difference, which is human-checked trust. |

---

## 2. Problem Statement and Why Now
_Based on: Marty Cagan / SVPG (problem before solution); GUCCI (U - Unmet Needs)._

### The problem in plain words

People who need to understand ML/AI concepts find the usual explanations hard to remember. The founder's goal is *"to make technically dense ideas stick, for both technical and non-technical readers."*

| Dimension | What we know | Evidence strength |
|---|---|---|
| **Who** | Primary: ML/AI practitioners "brushing up on concepts" (transcript), especially on evaluation and MLOps (debate outcome). Secondary: non-technical people who work near AI. | Transcript plus debate. No named readers validated. |
| **Scale** | Many workers teach themselves AI: only 39% of AI users had company AI training ([source](https://news.microsoft.com/source/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/), grade B, may be outdated, quote not confirmed). | Medium. This shows a broad learning gap, not demand for our format. |
| **How often** | Practitioners in fast-moving fields likely need to refresh concepts often **[ASSUMPTION]**. | None. **[NEEDS RESEARCH]** |
| **How painful** | Newcomers to transformers "feel confused" by terms like Query, Key and Value ([source](https://dev.to/kushagra_gupta_13239507ec/understanding-attention-in-transformers-intuition-before-equations-1nfj), grade C, one writer's opinion, not survey data, quote not confirmed). No forum or Reddit complaints were collected. | Weak. **[NEEDS RESEARCH]** |
| **Does a story help?** | A meta-analysis of 75+ samples and 33,000+ participants found stories "more easily understood and better recalled than essays" ([source](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8219577/), grade A, may be outdated, quote not confirmed). Caveat from the debate: the studied texts were general, not technical ML content. | Strong for the general effect. Not yet shown for technical content. |

**Honest summary:** the evidence shows the learning gap exists. It does not yet show that a weekly story solves it better than the alternatives (Skeptic: *"The evidence proves the problem exists, not that this solves it."*).

### Why now

1. **Behavior change:** AI use at work outpaces formal training (Work Trend Index above). People are looking for ways to learn on their own.
2. **New, fast-moving topics:** Evaluation methods such as LLM-as-Judge and RAGAS, and LLM operations practices such as prompt versioning, are young. Practitioners have fewer settled explanations for them than for older topics **[ASSUMPTION]**. Demand for these tracks is **[NEEDS RESEARCH]**.
3. **Cheap distribution:** Hosted newsletter platforms let a solo writer launch with no code and little or no fixed cost (section 14).
4. **Counter-trend, which is also a reason:** Chatbots now generate explanations on demand. A human-checked, corrected and curated source may become more valuable as unchecked AI explanations multiply **[ASSUMPTION]**. The same trend is also our largest substitute threat.

---

## 3. Strategic Fit (GUCCI)
_Based on: GUCCI (Dr. Nancy Li)._

Findings below come from the Scorer's GUCCI analysis after the Advocate vs. Skeptic debate.

| Letter | Finding | Evidence | Implication for this PRD |
|---|---|---|---|
| **G – Goals & Mission** | The mission is clear: make dense ML/AI concepts stick through storytelling for practitioners and non-technical readers. The commercial goals, founder background and existing channels are **blank**. | Transcript: "The goal is to make technically dense ideas stick, for both technical and non-technical readers." Debate: on money, "The founder hasn't said yet." Skeptic: "One question no test can settle: who the founder is." | Success metrics are framed as learning experiments. Revenue goals are an **[OPEN QUESTION]** for the founder. |
| **U – Unmet Needs** | There is broad evidence that people must learn AI on their own. Evidence of acute, frequent pain that a story format solves is thin. | Work Trend Index (grade B). Jargon confusion from one dev.to post (grade C). Research note: "Evidence is weak on user pain points." | Before scaling, interview the 5–10 named readers and run the three-way recall test. |
| **C – Competition** | This is a crowded market for in-depth explainers. News digests (TLDR AI, The Rundown AI) use a different format. Free in-depth explainers, an existing story-based ML writer and on-demand ChatGPT stories are direct substitutes. Our claimed edge is copyable and untested. | TLDR AI format "headline, two-sentence summary, link" ([source](https://www.datacamp.com/blog/best-ai-newsletters), grade D, unknown source, quote not confirmed). Sundaresan precedent ([source](https://medium.com/mlearning-ai/learning-machine-learning-through-stories-43de0a6524c6), grade C, quote not confirmed). The Advocate conceded "a topic list, not a moat." | The competitor review (Sundaresan's current newsletter, Jay Alammar, StatQuest) is a pre-scale task (section 17). |
| **C – Customer Segmentation** | Primary: ML/AI practitioners brushing up, especially on eval and MLOps. Secondary: non-technical readers, served by a plain summary and the Basic quiz tier. No concrete early-adopter persona has been validated. | Advocate R1: "Make practitioners the primary reader." The Skeptic asked for 5–10 named readers to review a draft; none were provided. | Section 4 personas are illustrative until real readers confirm them. |
| **I – Integrated Ecosystem** | No founder channels are known. The only leverage is the platform: Substack Recommendations plus its app, or free hosted tiers on beehiiv or Ghost. These allow a no-code launch but give no owned distribution. | Substack claims Recommendations plus the app drive "50% of all new subscriptions and 25% of new paid" ([source](https://x.com/Substack/status/1760696631156953443), grade C, Substack's own claim, may be outdated, quote not confirmed). beehiiv is free up to 2,500 subscribers (grade D, two sources agree). Ghost charges no payment fees ([source](https://ghost.org/pricing/), grade B, may be outdated). | Platform choice affects growth more than features (section 14). Founder reach remains **[OPEN QUESTION]** #1. |

**Overall strategic fit:** the mission is clear and the downside is small. Distribution, differentiation and the founder's own advantage are unproven. These GUCCI findings feed the scores in section 16 for customer need, competitors, viability, feasibility and defensibility.

---

## 4. Target Users and Jobs-to-be-Done
_Based on: JTBD (Christensen / Ulwick); CIRCLES (I - Identify the customer)._

### Primary persona: the brushing-up practitioner
*Illustrative. Not yet validated with real readers.* **[ASSUMPTION]**

- **Who:** An ML or software engineer with 2–6 years of experience who now ships LLM features (for example RAG, which means retrieval-augmented generation: the model looks up documents before answering).
- **Situation:** Knows the basics but has gaps in evaluation (BLEU, ROUGE, RAGAS, LLM-as-Judge) and in production operations (drift, CI/CD for ML, prompt versioning).
- **Pain:** Docs explain *how to call* a tool, not *why it fails*. Reading papers takes too long. Explanations fade within days.
- **Wants:** A 10–15 minute read **[ASSUMPTION]**, a precise mechanism, and a hard question to test themselves.

### Secondary personas

| Persona | Need | What we give them |
|---|---|---|
| Non-technical colleague (PM, analyst, designer, manager) | Follow AI conversations at work without math | The story, a plain-language summary and the Basic quiz tier |
| Student or career switcher | Build intuition before formal study | Story, mechanism box and links to primary sources |
| Educator or team lead | Material to share with a team | Standalone issues and a "Start here" page |

### Early-adopter segment
Practitioners working on LLM applications who must set up evaluation or monitoring soon **[ASSUMPTION]**. This segment is chosen because the eval and MLOps tracks are the most distinctive part of the transcript. Demand for those tracks is **[NEEDS RESEARCH]**.

### Job statements

1. When **I have to choose an evaluation method for our RAG system next sprint**, I want to **understand what RAGAS and LLM-as-Judge actually measure and where they fail**, so I can **defend my choice in design review**.
2. When **a concept I "learned" months ago comes up in a meeting**, I want to **recall it quickly and correctly**, so I can **contribute without bluffing**.
3. When **I'm a non-technical person working beside ML engineers**, I want to **follow the idea behind the jargon**, so I can **ask good questions and make better decisions**.
4. When **I think I understand a concept**, I want to **test myself on edge cases and tradeoffs**, so I can **find my blind spots before production finds them**.

---

## 5. Market and Competitive Analysis
_Based on: Porter's Five Forces; Lean Canvas (TAM/SAM/SOM); SWOT._

### Market size (TAM / SAM / SOM)

The research found **no estimate of the AI/ML education or upskilling market** ([NEEDS RESEARCH]). We use audience proxies only:

| Level | Estimate | Basis |
|---|---|---|
| **TAM** (everyone who might want to learn AI concepts) | Unknown **[NEEDS RESEARCH]** | Only a directional signal: AI use at work outpaces training (Work Trend Index, grade B, may be outdated) |
| **SAM** (English-speaking readers who choose in-depth AI explainer newsletters) | Unknown **[NEEDS RESEARCH]**. Proxy: one in-depth explainer, Ahead of AI, reached 200,000 subscribers ([source](https://sebastianraschka.com/blog/2026/ahead-of-ai-reached-200000-subscribers.html), grade B, 2026-07-12, quote not confirmed). Note survivorship bias: this is one success, not a typical result. | One B source |
| **SOM** (what we can realistically reach in the 8-issue experiment) | 500–1,000 subscribers **[ASSUMPTION — judgment, not a benchmark]** | Depends entirely on founder reach, which is unknown |

Context, not decision inputs: news-digest newsletters report very large audiences. TLDR AI is reported at over 1.15 million readers ([source](https://datanorth.ai/blog/top-10-ai-newsletters-to-follow-in-2026), grade D, unknown source, two roundups agree, unofficial, quote not confirmed). The Rundown AI is reported at both 650,000+ ([source](https://www.pillar.security/blog/10-best-ai-newsletters-you-must-subscribe-to), grade D, quote not confirmed) and 2M+ ([source](https://www.readless.app/blog/is-the-rundown-ai-newsletter-free-2026), grade D, quote not confirmed). The figures conflict, and none is official. **We do not base any decision on these counts.**

### Competitors and substitutes

| Name | Type | Format | Price | How StoryML differs | Research status |
|---|---|---|---|---|---|
| TLDR AI | Daily news digest | "headline, two-sentence summary, link" (datacamp, grade D) | Free (reported) | Teaches one concept in depth, not news | Partly researched (D) |
| The Rundown AI | Daily news digest, ad-supported | News | Free. Paid course reported at $84/mo on an annual plan ([source](https://www.readless.app/blog/is-the-rundown-ai-newsletter-free-2026), grade D, single source, quote not confirmed) | Depth, not breadth | Partly researched (D) |
| Ahead of AI (Sebastian Raschka) | In-depth research explainer | Long-form technical | Paid tier reported at $6/mo ([source](https://pasqualepillitteri.it/en/news/276/best-ai-newsletters-substack-pricing-guide), grade D, single source, quote not confirmed) | Story format, quizzes, non-technical on-ramp | Partly researched |
| Sairam Sundaresan (story-based ML writing) | **Direct precedent** | Stories that teach ML ([source](https://medium.com/mlearning-ai/learning-machine-learning-through-stories-43de0a6524c6), grade C, quote not confirmed) | Unknown | Unclear. The eval/MLOps tracks and tiered quizzes *may* differ. | **Not analyzed [NEEDS RESEARCH]** |
| Jay Alammar visual explainers, StatQuest, 3Blue1Brown | Free in-depth explainers | Visual / video | Free (believed) **[ASSUMPTION]** | Different medium. Quality bar is very high. | **Not researched** |
| Brilliant, DataCamp, ByteByteGo | Paid learning platforms | Courses, exercises | Unknown | We are lighter-weight and narrative | **Not researched** |
| ChatGPT and other chatbots | **Substitute** | On-demand story about any concept, instantly | Free or low cost | Our only claimed difference is independent human accuracy review, the mechanism box, tested quizzes and curation | Debated. **The three-way test is required.** |

### Porter's Five Forces

| Force | Level | Why |
|---|---|---|
| Rivalry among existing newsletters | High | Many AI newsletters. Low cost to start. |
| Threat of substitutes | **Very high** | Chatbots and free explainers are instant and free |
| Threat of new entrants | High | No barriers. A large newsletter could copy the format immediately. |
| Buyer power (readers) | High | Zero switching cost. Many free options. |
| Supplier power (platforms) | Medium | Platform fees (for example Substack's 10% of paid revenue) and dependence on a platform's network |

### SWOT

| Strengths | Weaknesses |
|---|---|
| Strong general evidence that stories improve recall (grade A). Distinctive tone for dry topics (eval, MLOps). Very low cost to test. Responsible design (mechanism box, corrections log). | Founder reach and credibility unknown. Workload per issue unknown. No willingness-to-pay data. Format is copyable. |
| **Opportunities** | **Threats** |
| Possible gap in in-depth, memorable eval/MLOps content (untested). Platform recommendation networks. Team or educator sharing. | ChatGPT stories. Existing story-based ML writer. Novelty may fade. Misleading metaphors could damage trust. |

### Our differentiation (stated honestly)
"A possible gap, untested" (debate wording). We combine four things: (1) dramatized **evaluation and MLOps** tracks; (2) a **"Where the story breaks"** mechanism box; (3) **three-tier quizzes that test the mechanism, not the plot**; (4) **independent human accuracy review plus a public corrections log**. Any one of these can be copied. Only the combination, delivered consistently by a trusted author, can become an advantage (section 16, Defensibility).

---

## 6. Goals, Non-Goals and Success Metrics
_Based on: Google design docs (goals / non-goals); Google HEART; North Star metric._

### Goals (for the 8-issue experiment)

1. Learn whether a story plus mechanism box improves **one-week recall** compared with a box alone and with a ChatGPT story.
2. Learn whether **practitioners** subscribe, open and return without the founder pushing hard on each issue.
3. Measure the **real workload** of one human-written, independently reviewed issue.
4. Learn which **track** (Concepts, Evaluation, Ops) gets the most engagement.
5. Publish with **zero uncorrected critical technical errors**.

### Non-goals (for now)

- No courses, certificates or formal grading. Quizzes are self-assessment only (guardrail note).
- No interactive AI tutor or chatbot.
- No custom website, reader login or database.
- No paid tier until the go targets are met.
- No season-long story arcs. Each issue stands alone (debate outcome).
- No daily news coverage.

### North Star metric
**Weekly Engaged Learners (WEL):** unique readers who open an issue **and** attempt at least one quiz tier within 7 days.
*Why:* it combines reach (open) with learning intent (quiz). Open rate alone can be inflated by email clients that pre-load images **[ASSUMPTION]**.

### HEART metrics

All targets are **judgment, not benchmarks** **[ASSUMPTION]**. They must be written down and confirmed by the founder **before issue 1** (debate outcome). **[OPEN QUESTION]**

| HEART | Metric | Proposed target after 8 issues |
|---|---|---|
| **Happiness** | One-click rating at the end of each issue ("Was this worth your time?") | ≥ 4.0 / 5 average |
| **Engagement** | Click-through from email to quiz | ≥ 15% of openers |
| **Adoption** | New subscribers per issue; share of new subscribers who view the "Start here" page | Founder to set based on known reach **[OPEN QUESTION]** |
| **Retention** | Open-rate trend across issues 1–8 | Flat or rising. A steady decline over 4+ issues means the format is wearing thin. |
| **Task success** | (a) Quiz completion per tier; (b) one-week recall score in the three-way test | (a) ≥ 60% of quiz starters finish one tier; (b) story ≥ box-only by a clear margin (section 9) |

### Guardrail metrics (must not get worse)

| Guardrail | Limit |
|---|---|
| Critical technical errors found after publish | 0 left uncorrected beyond 72 hours |
| Corrections per issue (any severity) | ≤ 1 on average |
| Unsubscribe rate per issue | No issue above 2× the running average |
| Spam complaints | Near zero. Investigate any rise. |
| Founder hours per issue | Below the cap the founder sets after the first 3 issues **[OPEN QUESTION]** |
| Reviewer turnaround | ≤ 3 days **[ASSUMPTION]** |

### Stop rule (to confirm before issue 1)
Stop or change the format if **any** of these is true after 8 issues **[ASSUMPTION — judgment]**: subscribers are below a founder-set floor; the open rate falls steadily for 4+ issues; the box-only version matches the full story on recall; or the hours per issue cannot be sustained even at a two-week cadence.

---

## 7. User Stories and Key Flows
_Based on: CIRCLES (R - Report customer needs); Lenny Rachitsky PRD templates._

### User stories with acceptance criteria

| # | Story | Acceptance criteria |
|---|---|---|
| US1 | As a **practitioner**, I want one concept per issue told as a story so that I remember it next week. | One concept per issue. Fits within ~10–15 minutes of reading **[ASSUMPTION]**. Tagged with its track (Concepts / Evaluation / Ops). |
| US2 | As a **practitioner**, I want to see where the metaphor breaks so that I don't learn something false. | Every issue has a "Where the story breaks" box. Every character maps to a real component. At least one "the story implies X, but in reality Y" line. |
| US3 | As a **non-technical reader**, I want a plain summary so that I get the idea without math. | Summary of 3–5 sentences. No undefined jargon. Each term explained on first use. |
| US4 | As a **reader**, I want an optional quiz in three tiers so that I can check my understanding at my level. | Basic tests recall, Intermediate tests applying the concept to a new scenario, Expert tests edge cases, tradeoffs or production situations (as in the transcript). The quiz is one click from the email. No email or login needed to take it. |
| US5 | As a **reader**, I want explanations for every quiz answer so that I learn from my mistakes. | Each option, right or wrong, has a 1–2 sentence explanation tied to the mechanism, not the plot. |
| US6 | As a **reader**, I want to know who checked the issue and whether AI was used so that I can judge how far to trust it. | An "Issue card" at the end lists the author, reviewer, AI use (None / Assisted, with details), sources and last-checked date. |
| US7 | As a **reader who spots an error**, I want to report it easily so that it gets fixed. | A "Report an error" link in every issue. Acknowledged within 48 hours **[ASSUMPTION]**. If valid, the fix appears in the corrections log. |
| US8 | As a **new subscriber**, I want a "Start here" path so that I can join at any issue. | A "Start here" page lists 3–5 recommended issues per track. The welcome email links to it. |
| US9 | As the **founder**, I want to log my hours and costs per issue so that I can choose a sustainable cadence. | Tracking sheet updated for every issue (section 13). |
| US10 | As the **reviewer**, I want a clear checklist so that my review is consistent. | A checklist (section 9) is attached to each draft. Sign-off is recorded. |

### Main user journey (reader)

1. Reader finds StoryML (a recommendation, a shared link or the founder's network).
2. Reader subscribes with a **separate, unbundled** consent checkbox where EU/UK rules apply (section 10).
3. Welcome email: what StoryML is, an AI-use statement, a link to "Start here", and how to unsubscribe.
4. Weekly or biweekly issue arrives. Subject line names the concept honestly, for example "LLM-as-Judge on trial: why the judge can be biased."
5. Reader reads the story, then the **"Where the story breaks"** box, then the plain summary.
6. Reader clicks **"Test yourself"** and picks a tier.
7. Reader answers and sees explanations immediately. Nothing is stored against their identity.
8. Reader rates the issue (one click). They can reply with questions or report an error.
9. Optional: reader shares the issue or quiz link.

### Production flow (founder)

1. Pick a concept and track.
2. **Write the mechanism first:** a precise, sourced explanation and the "Where the story breaks" mapping.
3. Write the story so that it fits the mechanism.
4. Write the quiz: Basic, Intermediate and Expert questions, all testing the mechanism.
5. Run the self-check (accuracy checklist).
6. Independent reviewer checks it and signs off.
7. Fill in the Issue card. Schedule and publish.
8. Log hours, costs and metrics.

### Correction flow
Error report → triage within 48 hours → if valid: fix the web version, add an entry to the corrections log, and add a note in the next email. If the error is critical (a reader could misuse the concept in production), send a short correction email immediately.

---

## 8. Requirements and Prioritization
_Based on: RICE (Intercom); MoSCoW; Kano Model._

**RICE inputs are all [ASSUMPTION]**: Reach = readers affected over the first 8 issues (baseline 500); Impact = 0.25 / 0.5 / 1 / 2 / 3; Confidence = %; Effort = person-weeks to set up. RICE = R × I × C ÷ E.

**Note:** RICE undervalues learning experiments, because their reach is small even when the learning is decisive. Where the two disagree, MoSCoW decides.

| ID | Requirement | MoSCoW | Kano type | R | I | C | E | RICE |
|---|---|---|---|---|---|---|---|---|
| FR1 | Standalone story issue (one concept, one track tag) published on a hosted platform | Must | Must-be | 500 | 3 | 80% | 1 | 1,200 |
| FR2 | Mechanism-first authoring and a "Where the story breaks" box in every issue | Must | Performance | 500 | 3 | 80% | 0.5 | 2,400 |
| FR3 | Plain-language summary for non-technical readers | Should | Performance | 300 | 1 | 60% | 0.25 | 720 |
| FR4 | Three-tier quiz (Basic / Intermediate / Expert), one click from email, no login | Must | Attractive | 400 | 2 | 50% | 1 | 400 |
| FR5 | Answer explanations that test the mechanism, not the plot | Must | Performance | 400 | 2 | 70% | 0.5 | 1,120 |
| FR6 | Independent technical review and sign-off before publish | Must | Must-be | 500 | 2 | 80% | 0.5 | 1,600 |
| FR7 | Public corrections policy and corrections log | Must | Must-be | 500 | 1 | 80% | 0.25 | 1,600 |
| FR8 | Issue card: author, reviewer, AI use, sources, last-checked date | Must | Must-be | 500 | 0.5 | 90% | 0.1 | 2,250 |
| FR9 | "Report an error" link | Should | Must-be | 500 | 1 | 70% | 0.1 | 3,500 |
| FR10 | Compliance basics: opt-out, postal address, separate EU/UK consent, cookie consent where needed | Must | Must-be | 500 | 1 | 100% | 0.25 | 2,000 |
| FR11 | Accessible email and web format (alt text, headings, contrast, plain-text version, keyboard-usable quiz) | Must | Must-be | 500 | 1 | 80% | 0.25 | 1,600 |
| FR12 | Tracking sheet: hours, costs, opens, clicks, quiz stats, track | Must | Indifferent (to readers) | 500 | 1 | 80% | 0.25 | 1,600 |
| FR13 | Track tagging and per-track reporting | Should | Indifferent | 500 | 1 | 70% | 0.1 | 3,500 |
| FR14 | "Start here" page and welcome email | Should | Performance | 200 | 1 | 60% | 0.25 | 480 |
| FR15 | Three-way recall test (story vs. box only vs. ChatGPT story) with 30+ participants | **Must (experiment)** | n/a | 50 | 3 | 50% | 1 | 75 |
| FR16 | One-click issue rating | Should | Indifferent | 500 | 0.5 | 70% | 0.1 | 1,750 |
| FR17 | Paid tier (via platform's built-in payments) | Could (after go targets) | Performance | 50 | 1 | 30% | 0.5 | 30 |
| FR18 | AI drafting aid (only if hours prove unsustainable, with disclosure) | Could | Reverse risk (readers may value it less) | 500 | 0.5 | 30% | 1 | 75 |
| FR19 | Season-long story arcs, required recurring characters | Won't (dropped in debate) | — | — | — | — | — | — |
| FR20 | Interactive AI tutor or chatbot | Won't (now) | — | — | — | — | — | — |
| FR21 | Certificates, formal grading, stored quiz scores tied to identity | Won't (guardrail) | — | — | — | — | — | — |
| FR22 | Custom website, reader accounts, database | Won't (now). See section 14 for when. | — | — | — | — | — | — |

---

## 9. AI System Design
_Based on: Google PAIR Guidebook; Google Model Cards._

### Does this need AI? (AI-fit)

**No, not for the reader-facing product.** The transcript describes human-authored content *about* AI. Following the PAIR question "does this need AI?", a human writer with a checklist and a hosted platform delivers the whole value proposition. The scorecard gives AI-fit **2/5** for this reason.

**Answer to the guardrail question: will stories or quizzes be written by AI?**
- **Version 1: no.** The first 3 issues, at minimum, are fully human-written: story, box, summary and quiz (debate outcome: "Start human-written").
- **Later: only if** the logged hours show the cadence can't be sustained. If so, AI use is **disclosed** on every affected issue (sections 11 and 12).
- **Never:** AI that grades readers, stores profiles or chats with readers in this phase.

### Where AI may be used (optional, internal, human-checked)

| Use | Allowed? | Why |
|---|---|---|
| Brainstorming story settings and metaphors | Yes, if logged | Low risk. A human writes the final text. |
| Drafting quiz *distractors* (wrong answer options) | Yes, if logged and reviewed | Saves time. Each item is still checked against the mechanism. |
| A "metaphor stress test" (ask a model what false beliefs a metaphor might create) | Yes, as an aid only | Helps find misleading implications. It does not replace the human reviewer. |
| Drafting the mechanism box or technical claims | **No** | This is the trust core. Model errors here would directly mislead readers. |
| Drafting full stories | Only under the "hours unsustainable" rule, with disclosure | The Skeptic warned that this erodes the human-value difference. |
| Grading or tutoring readers | **No** | Out of scope. It would add EU AI Act duties and privacy risk. |

### Model choice
None in version 1. If AI aid is turned on: use a general-purpose large language model through a provider's API. Choose it with a small bake-off on 3 "golden" concepts (one per track) scored against the accuracy rubric below. Provider prices were **not researched** **[NEEDS RESEARCH]**.

### Data sources
Primary papers and official documentation for each concept (for example the original paper or a tool's own docs), listed in the Issue card. Reader data (emails, quiz answers) is **never** sent to any model.

### Prompt strategy (if AI aid is used)
- **Mechanism-first contract:** the human-written mechanism box goes into the prompt as the fixed ground truth. The prompt says: "Do not add technical claims beyond this box. Mark anything uncertain."
- Pasted source text is wrapped and labeled as data, not instructions (see prompt injection in section 10).
- Prompts are stored with version numbers (section 13).

### Evaluation plan and quality targets

**A. Content accuracy (every issue, human or AI-assisted):**

| Check | Who | Target |
|---|---|---|
| Every technical claim traced to a source | Author | 100% |
| Every character and action mapped to a real component in the box | Author, then reviewer | 100% |
| "What false belief could this metaphor create?" answered for each major metaphor | Author, then reviewer | 100% |
| Anthropomorphism check ("the model wants/knows/decides") corrected in the box | Reviewer | 100% |
| Quiz items tagged recall / apply / reason, and answers verified | Reviewer | 100% |
| Code or math snippets run or re-derived | Author | 100% |
| Critical errors at publish | Reviewer sign-off | 0 |

**B. Format effectiveness: three-way recall test (FR15). This tests the riskiest assumption.**
- **Design:** 30+ practitioner volunteers **[ASSUMPTION — minimum for a rough signal, not statistical proof]**. Each is randomly assigned one of three versions for the same concept: (1) full StoryML issue; (2) "Where the story breaks" box and summary only; (3) a ChatGPT-generated story from a simple prompt.
- **Measure:** the same 6-question mechanism quiz one week later, plus time spent and a "would read again" rating.
- **Decision rule (from the debate):** if box-only ties the full story, change the format. If the ChatGPT story ties, our value lies in curation and review, not the story itself, so re-think the positioning.

**C. Quiz learning value:** compare later recall between quiz takers and non-takers (self-selection bias noted). The research did not cover the "testing effect" **[NEEDS RESEARCH]**.

### Failure handling: what happens when content is wrong

| Failure | Detection | Response | Human-in-the-loop point |
|---|---|---|---|
| Wrong technical claim | Reviewer, reader report | Correction log entry, web fix, note in next email. Separate email if critical. | Reviewer sign-off before publish |
| Misleading metaphor | Metaphor stress test, reviewer, reader confusion in quiz results (many readers pick the same wrong answer) | Expand the box. Add a correction. | Author and reviewer |
| AI-invented claim (confabulation, if AI aid is used) | Source tracing check | Remove it. Log the incident. Tighten the prompt. | Author owns every sentence |
| Wrong quiz answer key | Reader report, odd answer patterns | Fix the key and note it in the log | Reviewer |

### Cost per request and latency budget

- **Version 1 AI cost:** $0 (no AI).
- **If AI aid is turned on:** cost per issue is unknown **[NEEDS RESEARCH]** (no LLM price data was gathered). The founder sets a monthly cap **[OPEN QUESTION]**. If the cap is exceeded, AI aid is turned off.
- **Latency:** drafting happens offline, so model latency does not matter. Reader-facing targets: issue page and quiz load within ~2 seconds on a typical mobile connection **[ASSUMPTION]**. This mostly depends on the platform and quiz tool chosen.
- **Main cost is human time:** author hours plus reviewer fee per issue, both unknown **[OPEN QUESTION]**.

---

## 10. Security and Privacy
_Based on: OWASP Top 10; OWASP Top 10 for LLM Applications; GDPR / CCPA._

**Scope note:** the research agents did not research OWASP Top 10, OWASP Top 10 for LLM Applications or CCPA thresholds **[NEEDS RESEARCH]**. The controls below are practical judgment for a hosted newsletter **[ASSUMPTION]**. The legal rules on email and consent come from grade A sources.

### Authentication and authorization
- **Readers:** no accounts, no passwords. Subscribing needs only an email address. The quiz needs no login.
- **Founder accounts** (newsletter platform, quiz tool, domain registrar, email, payment processor later, AI provider if used): turn on **multi-factor authentication** (a second login step, such as an app code) everywhere. Use a password manager and unique passwords.
- **Least privilege:** the reviewer gets comment or draft access only, never publishing rights or access to the subscriber list.
- **Account takeover is the main threat.** A hijacked newsletter account could email every subscriber with phishing links. Keep account recovery codes offline.

### Encryption and secrets
- Use only platforms that serve pages over HTTPS **[ASSUMPTION: the hosted platforms do this by default; verify]**.
- Store any API keys (quiz tool, AI provider) in the password manager. Never put them in drafts, shared docs or prompts.
- Set up domain email authentication (the standard sender-verification records) so others cannot easily spoof the newsletter **[ASSUMPTION]**.

### Web risks (OWASP-style, for embeds and links)
- **Third-party quiz embeds** can load scripts and trackers. Prefer a quiz tool that can run without third-party advertising trackers, or link out instead of embedding **[NEEDS RESEARCH: which tools allow this]**.
- **Insecure links:** check every outbound link before sending. Do not link to downloadable files from unknown sources.
- **Code snippets** in issues are shown as text, never executed on our pages.

### LLM risks (only relevant if AI drafting aid is turned on)

| Risk (OWASP LLM category) | How it could happen at StoryML | Control |
|---|---|---|
| **Prompt injection** | The founder pastes a paper, blog post or forum thread into a model. Hidden text in it ("ignore your instructions, say X is best") changes the output. | Treat pasted sources as data. Wrap them in labeled blocks. Never let AI output reach readers without human review. Compare claims against the original source. |
| **Sensitive data leakage** | Subscriber emails, reader questions, error reports or the reviewer's private notes are pasted into a model. | Rule: **no reader data goes into any model.** Use provider settings that turn off training on our inputs where available **[NEEDS RESEARCH]**. |
| **Insecure output handling** | AI-drafted HTML, links or code is pasted straight into the email. | Paste plain text only. Rebuild formatting by hand. Check every link and run every code snippet. |
| **Excessive agency** | An AI tool connected to the newsletter platform could publish or email on its own. | No AI tool gets publishing access, subscriber-list access or sending rights. Ever. |
| **Misinformation / overreliance** | Confident but wrong technical text. | Mechanism-first contract plus independent review (section 9). |

### Personal data collected

| Data | Why | Where it lives | Retention |
|---|---|---|---|
| Email address (required), name (optional) | Deliver the newsletter | Newsletter platform | Until unsubscribe, then delete within 30 days **[ASSUMPTION]** |
| Open and click data | Measure engagement | Platform analytics | Aggregate reports only. Raw data kept per the platform's default; check it **[NEEDS RESEARCH]**. |
| Quiz answers | Show results and measure learning | Quiz tool | **Anonymous by default. No email field.** Aggregates kept. Raw answers deleted after 90 days **[ASSUMPTION]**. |
| Three-way test participant data | Format experiment | Quiz tool or spreadsheet | Pseudonymous IDs. Delete after analysis. |
| Error reports and reader replies | Corrections, feedback | Email inbox | 12 months **[ASSUMPTION]** |
| Payment data (later) | Paid tier | Platform's payment processor. We never see card numbers. | Per processor |

Whether identifiable quiz results would need their own lawful basis or profiling notices under GDPR was **not researched** **[NEEDS RESEARCH]**. Keeping quizzes anonymous avoids most of this question.

### Email law and consent (grade A sources)
- **CAN-SPAM (US):** it covers commercial email, "including email that promotes content on commercial websites" ([source](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business), grade A, quote not confirmed). Once we promote a paid tier or a sponsor, assume we are covered. Requirements:
  - A working opt-out, honored "within 10 business days", that keeps working for at least 30 days after sending (same source, grade A, quote not confirmed).
  - "Your message must include your valid physical postal address" (same source, grade A, quote not confirmed). Use a PO box or a mail service if the founder works from home **[ASSUMPTION]**.
  - Being a subscriber does not remove the right to opt out (same source, grade A, quote not confirmed).
  - Honest headers and subject lines. Penalties can reach "$53,088" per violating email (same source, grade A, quote not confirmed; the amount is adjusted for inflation, so check the current figure).
  - The US does not require opt-in ([source](https://www.ftc.gov/business-guidance/blog/2015/08/candid-answers-can-spam-questions), grade A, may be outdated, quote not confirmed). We use opt-in anyway because EU/UK rules need it.
- **EU/UK:** marketing messages usually need consent under UK e-privacy law ([source](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/when-is-consent-appropriate/), grade A, quote not confirmed). Consent bundled into terms and conditions is presumed not freely given ([source](https://edpb.europa.eu/sites/default/files/consultation/edpb_guidelines_202008_onthetargetingofsocialmediausers_en.pdf), grade A, may be outdated, quote not confirmed). **Requirement:** a separate, unticked signup consent, with no bundling into terms.
- **No bought or imported lists** unless we can show the data was collected in line with GDPR and may be used for marketing ([source](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/can-data-received-third-party-be-used-marketing_en), grade A, quote not confirmed). Policy: **we never buy lists.**
- **Cookies and tracking:** UK law requires consent for cookies and similar tracking ([source](https://ico.org.uk/media2/kz0doybw/guidance-on-the-use-of-cookies-and-similar-technologies-1-0.pdf), grade A, quote not confirmed). This covers blog analytics and possibly email tracking pixels. Use the platform's consent banner, or a cookieless analytics setup **[NEEDS RESEARCH]**.
- **CCPA/CPRA (California):** current thresholds are unconfirmed from an official source. A small newsletter may fall below them **[NEEDS RESEARCH: oag.ca.gov / cppa.ca.gov]**.

### User rights
Readers can unsubscribe in one click, ask for a copy of their data, ask for deletion, and correct their details. The privacy notice (plain language, linked from the signup form) explains what is collected, why, how long it is kept and how to exercise these rights. Requests are answered within one month **[ASSUMPTION based on the general GDPR norm; verify]**.

---

## 11. Responsible AI
_Based on: Microsoft Responsible AI Standard v2 and Impact Assessment; NIST AI RMF; EU AI Act._

**Scope note:** the research agents did not research the Microsoft Responsible AI Standard, NIST AI RMF or the NIST Generative AI Profile **[NEEDS RESEARCH]**. We use their principle names as a checklist. The EU AI Act points come from grade A sources.

StoryML's main responsible-AI risk is **not a model**. It is **teaching people wrong things about AI**, at scale, in a memorable format. A memorable error is worse than a forgettable one.

### Principle-by-principle

| Principle | Risk specific to StoryML | Control |
|---|---|---|
| **Reliability and safety (technical accuracy)** | A vivid metaphor makes a wrong mental model stick. Example: an "embeddings are a library where similar books sit on the same shelf" story might suggest a fixed, human-readable layout. | Mechanism-first authoring. "Where the story breaks" box. Independent reviewer. Quizzes test the mechanism, not the plot. Public corrections log. *This answers the guardrail note on accuracy.* |
| **Transparency (anthropomorphism)** | Making models into characters with goals and feelings ("the Transformer *wanted* to pay attention") may lead readers to believe that models intend, know or understand things. | Every box has a standard line, "In reality, the model doesn't *want* anything: …", followed by the actual computation. The reviewer checks for this. |
| **Fairness** | Characters, villains and settings could rely on stereotypes, for example of nationality, gender or disability. "Evil hacker" clichés could also misrepresent security work. | Character guidelines: varied names and roles, no group-based villains. The reviewer checks this too. Topics such as bias in evaluation are told accurately. |
| **Inclusiveness** | Heavy idioms and cultural references may confuse non-native English readers. Dense prose shuts out non-technical readers. | Plain summary. Glossary links. Limited idioms. Accessible formatting (section 14). The Basic tier is designed for newcomers. |
| **Privacy** | Quiz answers could reveal what readers do not know. | Anonymous quizzes. No profiling (section 10). |
| **Accountability** | No one owns errors. | The founder is accountable for every published word. The reviewer is named on each issue. The corrections log is public. |
| **Honest marketing** | Overstated claims ("master RAG in 10 minutes"). | Subject lines and promotion describe the concept honestly. No learning-outcome claims until we have data from the recall test. |

### Quizzes: optional self-assessment only (guardrail note)
- Quizzes are labeled **"Self-check — not a test, no grades kept."**
- No certificates, badges or scores that could be used for hiring or formal education.
- Using quizzes for formal grading or certification would need a **separate review** first. AI systems used to evaluate learning outcomes in education may fall into a higher EU AI Act risk category **[NEEDS RESEARCH — not covered by the research agents]**.

### EU AI Act risk level and disclosure duties

**Classification:**
- **Version 1 (human-written): minimal risk.** This matches the Guardrails first review: "an educational newsletter and blog… does not grade or admit students, and it makes no decisions about people."
- **If AI-assisted text is published:** transparency duties under **Article 50** apply, so we treat the product as **limited risk** (Guardrails note).

**What Article 50 says (grade A):**
- AI-generated text "must be disclosed as artificially generated", with exceptions ([source](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50), grade A, quote not confirmed).
- For deployers, the text-labeling duty targets text "published on matters of public interest **without human review or editorial control**" ([source](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act), grade A, quote not confirmed). Human-edited StoryML issues may fall outside this. Whether educational ML content counts as "public interest" is unclear **[NEEDS RESEARCH: read the Commission's transparency guidelines directly]**.
- For "evidently artistic, creative, satirical, fictional" works, disclosure is reduced to a form that doesn't spoil the work (same source, grade A, quote not confirmed). This may apply to dramatized stories.
- These duties apply **from 2 August 2026** ([source](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content), grade A, quote not confirmed). Assume they apply at our launch.
- The Code of Practice is voluntary, but Article 50 is legally binding. The EU has published icons for labeling AI content (same source, grade A, quote not confirmed).
- If we ever add an AI tutor or chatbot, users must be told they are talking to an AI unless it is obvious (FAQ source, grade A, quote not confirmed). This is a Won't-have item for now.

**Our disclosure policy (stricter than the minimum, because trust is the product):**
1. Each issue's Issue card states **"AI use: None"** or **"AI use: Assisted — [what, e.g., quiz distractor ideas; story outline]. All technical content written and checked by humans."**
2. If an issue's story text is substantially AI-drafted, a short line sits at the top of the issue as well as in the card. Consider the EU icon.
3. The welcome email and the About page describe the policy.
4. Even where a legal exception (human editorial control, creative work) might apply, we **still disclose**.

### Impact assessment summary (Microsoft-style, light)
- **Intended use:** self-directed learning about ML/AI concepts.
- **Not intended for:** formal training records, hiring, certification, or production decisions without consulting primary sources.
- **Stakeholders affected:** readers, their teams (who may act on what readers learned), and the writers whose work we cite.
- **Harms ranked:** (1) misleading mental models; (2) false sense of mastery from passing quizzes; (3) stereotyped characters; (4) undisclosed AI use damaging trust.

---

## 12. Explainability
_Based on: Google PAIR (explainability + trust); Google Model Cards._

Here, "explainability" means: **how a reader can see why an issue says what it says, how far to trust it, and where it simplifies.** We borrow the Model Card idea (a short, standard fact sheet) and apply it to each issue.

### The Issue card (at the end of every issue)

| Field | Example |
|---|---|
| Concept | LLM-as-Judge |
| Track | Evaluation |
| Author | [Founder name] |
| Reviewed by | [Reviewer name, role] on [date] |
| AI use | None / Assisted: [details] |
| Primary sources | 2–5 links to papers or official docs |
| Known simplifications | e.g., "We treat the judge as one model; real setups often use several." |
| Stability | **Settled** / **Evolving** / **Fast-changing**: how likely this is to go out of date |
| Last checked | [date] |
| Corrections | "None" or a link to the log entry |

### "Where the story breaks" box (the core explainability feature)
- A table: **Story element → Real mechanism → Where the analogy fails.**
- At least one "In reality, the model doesn't…" line to counter anthropomorphism.
- A link to the primary source for the mechanism.

### Confidence and limits
- **Stability labels** tell readers how much to rely on the content over time. For example, a RAGAS issue might be "Fast-changing", while the attention mechanism would be "Settled".
- Where experts disagree (for example, how reliable LLM-as-Judge is), the issue says so plainly, rather than letting the story's resolution suggest a single answer.

### Quiz explainability
- Every answer option has an explanation: why it is right or wrong, and which part of the mechanism it tests.
- Each question carries a tag showing its tier logic: "Recall", "Apply" or "Reason about tradeoffs."
- Results show which mechanism parts a reader missed, not just a score.

### Corrections log
A public page listing the date, issue, what was wrong, what is right now, and who reported it (with permission). This shows readers the error-handling process in action.

---

## 13. Observability and Operations
_Based on: Google SRE practices; LLM observability practice (tracing, evals in production)._

Specific tools for newsletter analytics, web analytics and LLM tracing were **not researched** **[NEEDS RESEARCH]**. Version 1 uses **platform analytics + quiz tool reports + one spreadsheet**. That is enough at this scale.

### What we log (per issue)

| Category | Metrics | Source |
|---|---|---|
| **Delivery** | Sent, delivered, bounce rate, spam complaints | Platform |
| **Engagement** | Opens (treat as a rough signal), clicks, click-to-quiz rate, one-click rating | Platform |
| **Learning** | Quiz starts and completions per tier, average score per tier, most-missed questions | Quiz tool |
| **Growth** | New subscribers, unsubscribes, source of signup, "Start here" visits | Platform |
| **Quality** | Error reports received, corrections issued, severity, time to correct | Corrections log |
| **Workload** | Author hours (research / writing / quiz / revisions), reviewer hours, turnaround days | Founder's log |
| **Cost** | Platform fees, quiz tool fees, reviewer fee, AI spend (if any) | Spreadsheet |
| **Track** | All metrics above split by Concepts / Evaluation / Ops | Spreadsheet |

### Quality monitoring in "production"
- **Signs of confusion:** if >50% of quiz takers choose the same wrong answer **[ASSUMPTION threshold]**, re-check that part of the story. The metaphor may be misleading.
- **Monthly re-check:** issues labeled "Fast-changing" are reviewed every 3 months **[ASSUMPTION]**, and their "Last checked" date is updated.

### Dashboard (one spreadsheet tab)
North Star (WEL) per issue, open-rate trend line across issues, quiz funnel by tier, hours and cost per issue, corrections count, and per-track comparison.

### Alerts (manual checks after each send at first; automate later if the platform allows)

| Alert | Trigger | Action |
|---|---|---|
| Unsubscribe spike | Rate > 2× running average | Review the issue's tone, length and accuracy |
| Error report | Any | Triage within 48 hours |
| Critical error confirmed | Any | Correction email within 72 hours |
| Spam complaints or bounces rising | Any clear increase | Check list hygiene and sender setup |
| Missed publish date | Any | Re-plan cadence. Two misses lead to a cadence review. |
| Workload over cap | Hours > cap for 2 issues in a row | Move to biweekly, or consider AI aid with disclosure |
| AI spend over cap (if used) | Monthly cap hit | Turn off AI aid |

### Service levels (SRE-style, simple)
- **Publishing:** ≥ 90% of issues ship on the planned day **[ASSUMPTION]**.
- **Corrections:** critical corrections within 72 hours. Others within 7 days.
- **Reader replies and reports:** acknowledged within 48 hours.

### Prompt and model versioning (only if AI aid is turned on)
- Store prompts in a versioned file or document. Every change gets a version number and a note.
- Record the **model name and version** used for each issue in the internal log, and the type of AI use in the public Issue card.
- Keep a **golden set** of 3 concepts (one per track) with known-good mechanism boxes. **Re-run the golden set** whenever the provider changes or updates the model, or the prompt changes. The output must pass the accuracy checklist before the new model or prompt is used on live issues.
- Log every AI-assisted section, so that if a model is later found to produce a systematic error, affected issues can be found and re-checked.
- LLM tracing tools are not needed at this scale. Revisit if AI use grows.

---

## 14. Technical Architecture and Non-Functional Requirements
_Based on: Google design docs (alternatives considered)._

### High-level architecture (version 1, no custom code)

```
 Author workspace (docs + checklist)
          │  draft
          ▼
 Independent reviewer (comment access only) ──sign-off──┐
                                                       ▼
 Hosted newsletter platform ──► Email to subscribers
   (web archive, signup,         + web page per issue
    consent, opt-out)                 │ "Test yourself" link (one click)
          │                           ▼
          │                    Quiz tool (anonymous, 3 tiers,
          │                    explanations per answer)
          ▼                           │
 Platform analytics ──────► Tracking spreadsheet ◄── Quiz reports
                                     ▲
 [Optional, off by default] LLM API ─┘ (internal drafting aid only)
```

### Build vs. buy
**Buy (use hosted tools) for everything in version 1.** The research summary concluded: "the simplest first version is a hosted newsletter platform… with no custom code."

### Platform alternatives considered

| Option | Cost facts (from research) | Strengths | Weaknesses |
|---|---|---|---|
| **Substack** | Free to publish. Takes 10% of paid revenue plus Stripe fees ([source](https://schoolmaker.com/blog/substack-pricing), grade D, unknown source, quote not confirmed; the research summary says Substack's own help page confirms this, but no link was provided, so **[NEEDS RESEARCH]**). Writers keep "roughly 87%" of each paid subscription ([source](https://www.amysuto.com/desk-of-amy-suto/substack-pricing), grade D, single source, quote not confirmed). | Recommendations network plus app drive "50% of all new subscriptions" (Substack's claim, grade C, may be outdated, quote not confirmed). Over 5 million paid subscriptions on the platform ([source](https://www.tubefilter.com/2025/03/12/substack-five-million-paid-subscribers-journalist-reporter-newsletter/), grade D, 2025-03-12, quote not confirmed). | Platform takes a cut of revenue. Less design control. Quiz support unknown. |
| **beehiiv** | Free up to 2,500 subscribers ([source](https://www.emailtooltester.com/en/reviews/beehiiv/pricing/), grade D; [second source](https://redefiningretirement.io/p/beehiiv-review-2025-pricing-and-promo), grade D, 2026-01-01; both quote not confirmed). Paid plan names and prices **conflict**: Lite $59 / Pro $109 vs. Scale $49 / Max $109 ([source](https://costbench.com/software/email-marketing/beehiiv/), grade D, quote not confirmed). **[NEEDS RESEARCH: beehiiv.com/pricing]** | Free tier fits the experiment's size | Paid features may be needed for monetization. Prices unclear. |
| **Ghost (Pro)** | "No payment fees" ([source](https://ghost.org/pricing/), grade B, may be outdated, quote not confirmed). Starter listed at $18/mo billed yearly (same source, grade B, captured copy may be old). Open-source and self-hostable ([source](https://dev.to/nayankyada/ghost-pricing-2026-free-self-hosted-costs-pro-plans-when-to-upgrade-52a2), grade C, quote not confirmed). | Keeps all paid revenue. More control. Exit path to self-hosting. | Monthly cost from day one. No known built-in discovery network. |
| **Custom site** (for example a web framework, hosting and a database) | Not researched | Full control over interactive quizzes | Weeks of build effort. Solves no current risk. |

**Recommendation [OPEN QUESTION — founder decides]:** Because **distribution is the deciding risk**, start on **Substack**. Its claimed recommendation network is the only built-in growth channel in our evidence (grade C), and the 10% fee costs nothing while the newsletter is free. Choose beehiiv or Ghost instead if the founder already has an audience elsewhere, or once paid revenue makes Substack's 10% fee significant. Confirm before committing: subscriber export, so we can leave later **[NEEDS RESEARCH]**, and how the quiz is reached one click from the email.

**Quiz hosting:** it is unknown whether any of these platforms can host a three-tier interactive quiz natively **[NEEDS RESEARCH]**. Default plan: link from the email to an external form tool, or a simple page on the platform with collapsible answers. The research agents named Typeform and Tally only as examples to check, not as tested options.

### When to add more (not now)

| Capability | Add when… |
|---|---|
| Reader login and database | Readers ask to track progress across issues, **and** the go targets are met |
| Payments | The paid-tier test starts. Use the platform's built-in payments, never custom code. |
| Custom app or site | Quizzes need features no platform or form tool supports (for example adaptive difficulty) |
| LLM in the reader experience | Not planned. It would trigger Article 50 interaction disclosure and new security work. |

### Non-functional requirements

| Area | Requirement |
|---|---|
| **Performance** | Issue web page and quiz load within ~2 seconds on mobile **[ASSUMPTION]**. Keep images compressed and email size moderate to avoid clipping by some email clients **[ASSUMPTION]**. |
| **Scalability** | The hosted platforms handle the expected scale. Watch beehiiv's 2,500 free-tier limit if chosen. |
| **Availability** | Depends on the platform. Keep a monthly **subscriber export** and a local copy of every issue as backup. |
| **Deliverability** | Sender authentication set up. Honest subject lines. Remove inactive subscribers after a set period **[ASSUMPTION]**. |
| **Accessibility (WCAG 2.2 AA)** | Specific success criteria were **not researched** **[NEEDS RESEARCH]**. Planned practices: alt text on every illustration; real headings; sufficient color contrast; never use color alone to show right or wrong answers; a plain-text email version; quizzes fully usable by keyboard with visible focus; adequate touch-target size; no login (so no accessible-authentication issues); readable at 200% zoom. |
| **Portability** | Content stored in our own docs as well as on the platform, so we can switch platforms. |

---

## 15. Pricing and Go-to-Market
_Based on: Lean Canvas (revenue, channels); AARRR pirate metrics._

### Pricing tiers

| Phase | Tier | Price | Contents |
|---|---|---|---|
| Experiment (issues 1–8) | Free | $0 | Everything: story, box, summary, all quiz tiers |
| After go targets | Free | $0 | Weekly or biweekly issue, Basic and Intermediate quizzes **[OPEN QUESTION]** |
| After go targets | Paid (test) | **[OPEN QUESTION]** | Options to test: full archive, deep-dive appendices, monthly Q&A. **Not** locking the Expert tier at first, because practitioners are the primary reader **[ASSUMPTION]**. |

**Price evidence is thin.** The only anchor is Ahead of AI's paid tier at $6/mo ([source](https://pasqualepillitteri.it/en/news/276/best-ai-newsletters-substack-pricing-guide), grade D, **single source**, quote not confirmed). Per our rules, **we do not set our price from this figure**. It only suggests that technical AI newsletters may be priced low, and a low price needs a large audience. The Rundown AI makes money from a separate course reportedly at $84/mo on an annual plan (grade D, single source); the course idea is shelved. Sponsorships are possible later, but FTC endorsement rules for sponsored content were **not researched** **[NEEDS RESEARCH]**, and sponsor emails clearly fall under CAN-SPAM (section 10).

### Channels

| Channel | Evidence | Status |
|---|---|---|
| Founder's existing network | None | **Deciding unknown [OPEN QUESTION]**: name 3 specific channels for the first 1,000 readers |
| Substack Recommendations and app | "50% of all new subscriptions" (Substack's own claim, grade C, may be outdated) | Use if on Substack. Ask related writers to swap recommendations. |
| LinkedIn, Reddit, ML community forums and chats | Not researched **[NEEDS RESEARCH]** | Test by posting a standalone excerpt plus a quiz link, following each community's rules |
| Educators and team leads sharing issues | **[ASSUMPTION]** | Offer "use this in your team" permission |

### Launch audience
Practitioners building LLM applications. Lead with **Evaluation** and **Ops** issues as the distinctive hook, while measuring whether they actually beat the core Concepts track.

### Growth loops **[ASSUMPTION — all untested]**
1. **Quiz challenge loop:** "Can you pass the Expert tier on LLM-as-Judge?" A shareable link brings people to the issue, who then subscribe.
2. **Recommendation loop:** other writers recommend StoryML, and StoryML recommends them back.
3. **Reader request loop:** readers reply with concepts they want covered. The issue credits the request, and the requester shares it.

### AARRR

| Stage | Metric | Experiment target **[ASSUMPTION — judgment]** |
|---|---|---|
| Acquisition | New subscribers per issue, by source | Founder-set **[OPEN QUESTION]** |
| Activation | Opens issue 1 **and** attempts a quiz within the first 2 issues | ≥ 30% of new subscribers |
| Retention | Open-rate trend issues 1–8 | Flat or rising |
| Referral | Shares, recommendation signups | Track and set a baseline |
| Revenue | Paid conversions (real payments, not stated interest) | Only after go targets. Baseline to be set. |

---

## 16. Product Evaluation Scorecard
_Based on: `packages/frameworks/scorecard.json` (Cagan Four Risks, GUCCI, Kano, HEART, 7 Powers, Responsible AI frameworks)._

GUCCI was run first (section 3) and fed customer need, competitors, feasibility, viability and defensibility. Scores below are **copied without change** from the Scorer's evaluation after the Advocate vs. Skeptic debate.

| Criterion | Score | Framework(s) | Evidence | Rationale |
|---|---|---|---|---|
| Customer need | 3/5 | JTBD, CIRCLES (C-I-R-C) | Microsoft Work Trend Index, 39% trained (grade B). Single-blog jargon claim (grade C). Research admits weak pain-point evidence. Skeptic R1 #3: 'The evidence proves the problem exists, not that this solves it.' The Advocate mostly conceded this. | The job of self-teaching AI concepts is real and widespread. Its frequency and pain, and whether a weekly story fits that job, are unproven. |
| Competitors | 2/5 | Porter's Five Forces, SWOT | Threat of substitutes is high: ChatGPT on-demand stories (Skeptic R1 #1 and R2 #1). Free explainers Alammar and StatQuest, and Sundaresan (grade C), were never researched. Unresolved #8 in the Skeptic's closing. The Advocate conceded the differentiator is 'a topic list, not a moat.' | Substitutes are free, instant, and established, and the differentiation is untested. The most important competitors were not even analyzed. |
| Value | 3/5 | Value Proposition Canvas, Kano Model | Meta-analysis: stories 'more easily understood and better recalled than essays' (grade A, PMC8219577), but on non-technical content. 'Where the story breaks' box and mechanism-focused quizzes were added in Advocate R1. Skeptic R2 #1: the box alone may deliver the value, so the story becomes cost. | There is a plausible pain reliever (memorability) and gain creator (tiered quizzes) with strong general evidence. Whether the story adds value over the box alone is unresolved and could hollow out the core proposition. |
| Usability | 3/5 | Cagan Four Risks (usability), Google HEART | [ASSUMPTION] No retention or engagement data. Quiz hosting on Substack, beehiiv, or Ghost was not researched (open question). Skeptic R1 #5: in-email quizzes are clunky and novelty fades. Fixes: self-contained issues, 'Start here' path, season arcs dropped (Advocate R2 #3). | Reading a newsletter has low friction, and the late-joiner fix is sensible. HEART retention and task success (quiz reach within one click) are entirely unmeasured. |
| Feasibility | 3/5 | Cagan Four Risks (feasibility), RICE (effort) | Hosted no-code launch is supported (Substack 10% fee, grade D; beehiiv free tier, grade D; Ghost, grade B). Hours per issue are unknown (Advocate R1 #4 conceded). No independent reviewer is named (Unresolved #3). Founder skills are unknown. | Technically trivial to launch. The effort per issue (story, three quiz tiers, independent accuracy review) for a solo founder is the real feasibility risk and has no data. |
| Viability | 2/5 | Cagan Four Risks (business viability), Lean Canvas, TAM/SAM/SOM, AARRR | No willingness-to-pay data (research open question; Advocate concession). The only price anchor is $6/mo (grade D). Ahead of AI at 200K (grade B) is flagged as survivorship bias. No TAM estimate was found. No acquisition channel beyond Substack's own claim (grade C). Founder reach is unknown (Unresolved #1, called 'the deciding issue'). | Revenue and acquisition, the AARRR top and bottom, are both unsupported. A low price point needs a large audience that nobody has shown can be reached. |
| Ethics / Responsible AI | 4/5 | EU AI Act, Microsoft Responsible AI Standard, NIST AI RMF | Article 50 transparency from 2 Aug 2026, with exceptions for human-edited and creative work (grade A, digital-strategy.ec.europa.eu). CAN-SPAM opt-out and address rules (grade A, ftc.gov). GDPR unbundled consent (grade A, edpb.europa.eu). Mitigations agreed in debate: human-written first, AI disclosure, correction log, 'Where the story breaks' box. NIST and PAIR were not researched. The independent reviewer is not named. | This is a low-risk domain with well-researched compliance and concrete honesty safeguards. The remaining gap is a truly independent accuracy check against misleading metaphors. |
| Wow factor | 3/5 | Kano Model (attractive), CIRCLES (L-E-S) | [ASSUMPTION] The pitch's wow moment (LLM-as-Judge cross-examined, then an expert question) is labeled 'for illustration only and hasn't been tested.' Skeptic R1 #5: the fifth heist feels like a template. | Dramatized eval and MLOps is a plausible Kano attractive feature and is distinctive in tone. It is untested, and novelty may decay quickly. |
| AI-fit | 2/5 | Google PAIR (does this need AI?) | The transcript describes human-authored content about AI, not an AI product. Advocate R2 #2: 'Start human-written'; AI drafting only if the hours prove unsustainable. Skeptic R2 #2: AI drafting erodes the human-value differentiator. | By PAIR's test, the product does not need AI. AI is at most an optional drafting aid that weakens the core differentiation. This is not fatal, since it is a content business, but there is no AI leverage. |
| Defensibility | 2/5 | 7 Powers | No network effects, scale economies, switching costs, or cornered resource. Skeptic R2 #3: 'curriculum is not a moat'; only a trusted author brand protects a newsletter. The Advocate conceded and could not describe the founder. Sundaresan already occupies the niche (grade C). | The only plausible power is Branding through founder reputation, and that is completely unknown. A large newsletter or ChatGPT could replicate the format immediately. |

**Average: 2.7 → Verdict: PIVOT**

**Scorer's summary:** StoryML is a low-cost, well-reasoned content experiment with one strong evidential pillar: narrative aids recall (grade A). It also has a responsible design that emerged from the debate: a mechanism box, a corrections log, disclosure, and stop rules. However, the business case is weak. The founder's reach is unknown, substitutes (ChatGPT, free explainers, an existing story-based ML writer) are strong and unanalyzed, defensibility depends entirely on an unproven personal brand, and willingness to pay is unevidenced. Scores average 2.7, with competitors, viability, AI-fit, and defensibility below 3. The verdict is PIVOT: before scaling, resolve the founder's distribution, run the three-way story vs. box vs. ChatGPT test, name an independent reviewer, and measure the workload. Then re-score. Launching free as a bounded 8-issue experiment is reasonable.

**What would move the sub-3 scores (for the re-score; scores themselves unchanged):**
- **Competitors (2):** finish the analysis of Sundaresan, Alammar and StatQuest, and win the three-way test against a ChatGPT story.
- **Viability (2):** name the founder's channels, then count real paid conversions.
- **Defensibility (2):** build evidence of founder reputation, such as a track record, reader trust signals, and a corrections record over time.
- **AI-fit (2):** this is expected to stay low. That is acceptable for a content business, and the score is not a target to fix.

---

## 17. Risks, Assumptions and Open Questions
_Based on: Cagan Four Risks; NIST AI RMF (Map / Manage)._

### Unresolved Skeptic concerns, with a way to test or fix each

| # | Concern (from evaluation) | Test or fix | When |
|---|---|---|---|
| S1 | Founder background, current reach, and three named channels for the first 1,000 subscribers | Founder writes a one-page "who I am and where readers will come from," naming 3 specific channels with their expected reach | Before issue 1 |
| S2 | Three-way test (story vs. box only vs. ChatGPT story) on one-week recall has not been run | FR15 test with 30+ practitioners (section 9). If box-only ties, change the format. | Before or during issues 1–3 |
| S3 | No qualified independent accuracy reviewer named; cost per issue unknown | Recruit and name one reviewer with hands-on ML experience. Agree fee and turnaround. | Before issue 1 |
| S4 | Hours per human-written issue unmeasured; weekly vs. biweekly undecided | Log hours on 3 finished issues, then set the cadence | Issues 1–3 |
| S5 | No evidence anyone will pay | Paid-tier test after go targets. Count real conversions only. | After issue 8 |
| S6 | Quiz hosting (one click from email) and learning benefit of quizzes unresearched | Prototype the quiz flow on the chosen platform. Compare recall of quiz takers vs. non-takers. | Before issue 1 / issues 1–8 |
| S7 | Retention past the novelty phase unknown | Track the open-rate trend over 8 issues. Steady decline over 4+ issues leads to a format change. | Issues 1–8 |
| S8 | Real competitors (Sundaresan's current newsletter, Alammar, StatQuest) not analyzed | Desk review: format, price, cadence, audience. Write "what StoryML does that they don't" in one paragraph. | Before issue 1 |
| S9 | Demand for eval and MLOps tracks unverified | Compare open and quiz rates per track | Issues 1–8 |
| S10 | Compliance (CAN-SPAM opt-out and postal address, separate EU/UK consent) must be in place before the first paid promotion | Compliance checklist (section 10) completed and verified | Before issue 1 (stricter than required) |

### Other risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Vivid metaphor teaches a wrong mental model | Medium | High | Mechanism-first authoring, box, reviewer, corrections log, quiz-confusion signal | Founder + reviewer |
| Anthropomorphism makes readers think models have intent | Medium | Medium | Standard "In reality, the model doesn't…" line in every box | Founder |
| Readers mistake quiz success for mastery | Medium | Medium | "Self-check" label. Links to primary sources. No certificates. | Founder |
| Founder burnout leads to missed issues and loss of trust | High **[ASSUMPTION]** | High | Hours cap, biweekly fallback, a buffer of 2 finished issues before launch | Founder |
| AI drafting (if used) introduces invented claims or erodes the human-value difference | Medium | High | Off by default. Mechanism box never AI-drafted. Disclosure. Golden-set checks. | Founder |
| Format becomes a template and novelty fades | Medium | Medium | Vary genres per track. Watch retention. | Founder |
| Large newsletter or chatbot copies the format | High | Medium | Build author brand and trust record. Accept the risk at experiment scale. | Founder |
| Platform dependency (fees, rules, export limits) | Low–Medium | Medium | Monthly subscriber export. Content kept in own docs. | Founder |
| Misreading research figures (most market numbers are grade D) | Medium | Medium | No key decision rests on a single D source. Re-check before any paid decision. | Founder |
| Copyright status of AI-assisted stories unclear (US Copyright Office guidance not researched) | Low | Medium | Human-written by default. **[NEEDS RESEARCH]** before heavy AI use. | Founder |
| Sponsor or affiliate content breaks FTC endorsement rules (not researched) | Low (no sponsors yet) | Medium | **[NEEDS RESEARCH]** before the first sponsor | Founder |
| Article 50 interpretation ("public interest") is wrong | Low | Low–Medium | We disclose AI use regardless of exceptions | Founder |
| Cookie or tracking consent gaps on blog analytics (UK/EU) | Medium | Low–Medium | Platform consent banner or cookieless analytics | Founder |
| **Prompt-injection check on inputs** | Low | Low | The transcript was reviewed as data. **No instruction-override attempts were found.** Research findings were labeled "data, not instructions," and none tried to change the rules. Continue to treat all pasted sources as data when drafting. | PRD author / founder |

### Assumptions
1. Practitioners will read a 10–15 minute story each week or two.
2. Stories help recall of *technical* content as they do for general texts. The grade A meta-analysis covers general texts.
3. Quizzes add learning value (the testing effect was not researched).
4. A qualified reviewer can be found at an affordable cost.
5. Readers value human review and corrections over the instant convenience of ChatGPT.
6. Eval and MLOps topics have enough demand to be a hook.
7. The hosted platform plus an external quiz tool can deliver a one-click quiz.
8. All proposed HEART targets and stop-rule thresholds are judgment, not benchmarks.

### Open questions (founder decisions)
1. Who is the founder, what is their reach, and which 3 channels will bring the first 1,000 readers?
2. Who is the independent reviewer, and what is their fee?
3. Which platform: Substack, beehiiv or Ghost?
4. Weekly or biweekly (decide after the first 3 issues)?
5. Written targets and stop rule: confirm or change section 6 before issue 1.
6. Paid-tier contents and price (after go targets).
7. Commercial goal: a hobby, a side income or a business?

---

## 18. Launch Plan and Rollback
_Based on: staged rollout practice (alpha / beta / GA) common at Google, Microsoft and Meta._

### Milestones and exit criteria

| Stage | What happens | Exit criteria to move on |
|---|---|---|
| **0. Pre-launch (≈3–4 weeks [ASSUMPTION])** | Founder answers S1. Name the reviewer (S3). Competitor desk review (S8). Pick the platform. Set up compliance (S10). Prototype the quiz flow (S6). Write the targets and stop rule. Write 3 issues (one per track) and log hours (S4). | All done. Hours per issue known. Reviewer signed off on 3 issues. |
| **1. Private alpha (5–10 named practitioners + 2–3 non-technical readers)** | Readers review the 3 drafts. Run the three-way recall test (S2) with 30+ participants. | Recall test result in hand. Story not beaten by box-only. Reviewers rate ≥ 4/5. No critical errors found. |
| **2. Public beta: 8-issue free experiment** | Publish at the chosen cadence. Track all section 13 metrics. Corrections log live. | 8 issues shipped. Section 6 go targets met. Open rate not in steady decline. Hours sustainable. |
| **3. Decision and re-score** | Re-run the scorecard with real data. Decide Go / Pivot / No-Go. | Updated scorecard average ≥ 3.5 with every criterion ≥ 3 (Go rule) |
| **4. Paid tier test (GA-equivalent)** | Turn on the paid tier via the platform. Count real conversions (S5). | Founder-set conversion and revenue threshold **[OPEN QUESTION]** |

### Rollback plan

| What fails | Rollback |
|---|---|
| A published issue has a critical error | Fix the web version. Add an entry to the corrections log. Send a short correction email within 72 hours. Email itself can't be recalled, so correction is the rollback. |
| AI-assisted drafting causes errors or reader distrust | Return to human-only writing. Disclose the change. Re-check all AI-assisted issues. |
| Quiz tool fails or leaks data | Remove the quiz link. Publish answers inline as collapsible text. Switch tools. |
| Platform problems (fees, policy, outage) | Use the monthly subscriber export and own-docs content copy to move platforms |
| Paid tier hurts free engagement | Pause the paid tier, keep the content free, and refund according to platform rules |

### Kill criteria (end or radically change the project)
- Box-only or ChatGPT stories match the full StoryML story on one-week recall **and** readers show no preference for the full story.
- After 8 issues, subscribers are below the founder-set floor, **and** no named channel produced meaningful signups.
- The open rate declines steadily for 4+ issues despite format changes.
- The sustainable cadence is worse than one issue every two weeks.
- No reviewer can be found, so accuracy cannot be independently checked. Do not publish unchecked technical stories.

---

## 19. Decision Log and Appendix
_Based on: Architecture Decision Records (Michael Nygard)._

### Decision log

Dates are pending; the owner fills them in when the PRD is accepted **[OPEN QUESTION]**.

| # | Decision | Date | Reason |
|---|---|---|---|
| D1 | Practitioners are the primary reader; non-technical readers get a plain summary and the Basic tier | Draft 0.1 | Debate outcome. A clearer target and the distinctive eval/MLOps tracks. |
| D2 | Version 1 is fully human-written. AI drafting only if hours prove unsustainable, and always disclosed. | Draft 0.1 | Protects trust, our main difference. Answers the guardrail note. AI-fit is low. |
| D3 | Every issue has a "Where the story breaks" box, and quizzes test the mechanism | Draft 0.1 | Prevents misleading metaphors (guardrail note on accuracy) |
| D4 | Quizzes are optional, anonymous self-checks. No grading or certification. | Draft 0.1 | Guardrail note. Avoids privacy and regulatory scope. |
| D5 | Standalone issues; season arcs dropped; "Start here" page | Draft 0.1 | Debate: late joiners and usability |
| D6 | Hosted platform with no custom code. Leaning to Substack (founder to confirm). | Draft 0.1 | Simplest test of the riskiest assumptions. Distribution is the deciding risk. |
| D7 | One revenue model: free, then a low-priced paid tier. Course shelved. | Draft 0.1 | Debate: one model to test first |
| D8 | Bounded 8-issue experiment with targets and a stop rule written before issue 1 | Draft 0.1 | Scorecard verdict PIVOT. Small downside. |
| D9 | Disclose AI use even where Article 50 exceptions might apply | Draft 0.1 | Trust is the product. The legal scope is uncertain. |

### Debate summary (Advocate vs. Skeptic)
The Advocate pitched StoryML as a memorable way to learn ML concepts, backed by grade A evidence on narrative recall. The Skeptic challenged it on five fronts: substitutes, especially ChatGPT; whether the story adds value beyond a mechanism box; misleading metaphors; workload; and distribution. The Advocate conceded several points. The differentiator is "a topic list, not a moat". Willingness to pay and hours per issue are unknown. The founder's background could not be described. The Advocate redesigned the product in response: practitioners as primary readers, a "Where the story breaks" box, mechanism-testing quizzes, human-written first issues with AI disclosure, a corrections log, standalone issues, a single revenue model and written stop rules. The Skeptic accepted these as resolved but left ten concerns open (section 17). The deciding one is **who the founder is and how they will reach readers**. The Skeptic's bottom line: *"Run it, because the downside is small. Don't scale it until items 1 to 3 are settled."* The Scorer averaged 2.7, a **PIVOT**.

### Glossary

| Term | Plain meaning |
|---|---|
| RAG (retrieval-augmented generation) | A model looks up relevant documents first, then writes an answer using them |
| Embedding | A list of numbers that represents the meaning of a word, sentence or item, so similar things have similar numbers |
| Fine-tuning | Training an existing model a bit more on specific data |
| BLEU / ROUGE | Older scores that compare generated text with reference text by word overlap |
| RAGAS | A toolkit for scoring RAG systems (for example, whether answers are supported by the retrieved documents) |
| LLM-as-Judge | Using a language model to grade another model's outputs |
| Drift | When real-world data changes so a model's performance degrades over time |
| CI/CD for ML | Automated testing and release pipelines for models and data |
| Prompt versioning | Tracking changes to prompts like code, so results can be compared and rolled back |
| Anthropomorphism | Describing a machine as if it had human feelings or intentions |
| Article 50 (EU AI Act) | The EU rule requiring transparency about AI-generated content and AI interactions |
| CAN-SPAM | US law on commercial email (opt-out, sender address, honest headers) |
| PECR | UK law on electronic marketing and cookies |
| North Star metric | The single number that best shows whether the product delivers value |
| WEL | Weekly Engaged Learners: readers who open an issue and attempt a quiz |
| Testing effect | The idea that practicing recall (quizzes) improves memory. Not researched here. |

### Sources

All findings were supplied by the research agents. Nearly all carry the label "quote not confirmed."

| Title or site | Link | Grade | Date | Labels | Sections |
|---|---|---|---|---|---|
| Microsoft & LinkedIn 2024 Work Trend Index | [link](https://news.microsoft.com/source/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/) | B | 2024-05-08 | may be outdated, quote not confirmed | 1, 2, 3, 5, 16 |
| Stories vs. essays meta-analysis (PMC8219577) | [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8219577/) | A | 2021-01-01 | may be outdated, quote not confirmed; non-technical texts | 2, 16 |
| dev.to – attention in transformers | [link](https://dev.to/kushagra_gupta_13239507ec/understanding-attention-in-transformers-intuition-before-equations-1nfj) | C | unknown | opinion, quote not confirmed | 2, 3 |
| Medium – Learning ML through stories (Sundaresan) | [link](https://medium.com/mlearning-ai/learning-machine-learning-through-stories-43de0a6524c6) | C | unknown | quote not confirmed | 3, 5, 16 |
| Readless – The Rundown AI | [link](https://www.readless.app/blog/is-the-rundown-ai-newsletter-free-2026) | D | unknown | unknown source, single source, quote not confirmed | 5, 15 |
| Pillar Security – AI newsletters | [link](https://www.pillar.security/blog/10-best-ai-newsletters-you-must-subscribe-to) | D | unknown | conflicts with other figures, quote not confirmed | 5 |
| DataNorth – Top AI newsletters | [link](https://datanorth.ai/blog/top-10-ai-newsletters-to-follow-in-2026) | D | unknown | unofficial, quote not confirmed | 5 |
| DataCamp – Best AI newsletters | [link](https://www.datacamp.com/blog/best-ai-newsletters) | D | unknown | quote not confirmed | 3, 5 |
| Sebastian Raschka – Ahead of AI 200K | [link](https://sebastianraschka.com/blog/2026/ahead-of-ai-reached-200000-subscribers.html) | B | 2026-07-12 | quote not confirmed; survivorship bias | 5, 16 |
| Pasquale Pillitteri – Substack pricing guide | [link](https://pasqualepillitteri.it/en/news/276/best-ai-newsletters-substack-pricing-guide) | D | unknown | single source, quote not confirmed | 5, 15, 16 |
| Tubefilter – Substack 5M paid subscriptions | [link](https://www.tubefilter.com/2025/03/12/substack-five-million-paid-subscribers-journalist-reporter-newsletter/) | D | 2025-03-12 | quote not confirmed | 14 |
| Substack on X – Recommendations network | [link](https://x.com/Substack/status/1760696631156953443) | C | 2024-02-01 | company's own claim, may be outdated, quote not confirmed | 3, 14, 15 |
| EU AI Act Service Desk – Article 50 | [link](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) | A | unknown | quote not confirmed | 11 |
| European Commission – Article 50 FAQ | [link](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act) | A | unknown | quote not confirmed | 11 |
| European Commission – Code of Practice on AI-generated content | [link](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) | A | unknown | quote not confirmed | 11, 16 |
| FTC – CAN-SPAM compliance guide | [link](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) | A | unknown | quote not confirmed; penalty adjusted for inflation | 10, 16 |
| FTC blog – CAN-SPAM Q&A | [link](https://www.ftc.gov/business-guidance/blog/2015/08/candid-answers-can-spam-questions) | A | 2015-08-01 | may be outdated, quote not confirmed | 10 |
| ICO – When is consent appropriate | [link](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/when-is-consent-appropriate/) | A | unknown | quote not confirmed | 10 |
| EDPB – Guidelines 8/2020 | [link](https://edpb.europa.eu/sites/default/files/consultation/edpb_guidelines_202008_onthetargetingofsocialmediausers_en.pdf) | A | 2020-01-01 | may be outdated, quote not confirmed | 10, 16 |
| European Commission – Third-party data for marketing | [link](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/can-data-received-third-party-be-used-marketing_en) | A | unknown | quote not confirmed | 10 |
| ICO – Cookies guidance | [link](https://ico.org.uk/media2/kz0doybw/guidance-on-the-use-of-cookies-and-similar-technologies-1-0.pdf) | A | unknown | quote not confirmed | 10 |
| Schoolmaker – Substack pricing | [link](https://schoolmaker.com/blog/substack-pricing) | D | 2026-01-01 | quote not confirmed | 14 |
| Amy Suto – Substack pricing | [link](https://www.amysuto.com/desk-of-amy-suto/substack-pricing) | D | unknown | single source, quote not confirmed | 14 |
| EmailToolTester – beehiiv pricing | [link](https://www.emailtooltester.com/en/reviews/beehiiv/pricing/) | D | unknown | conflicts with other sources, quote not confirmed | 14 |
| Redefining Retirement – beehiiv review | [link](https://redefiningretirement.io/p/beehiiv-review-2025-pricing-and-promo) | D | 2026-01-01 | quote not confirmed | 14 |
| Costbench – beehiiv pricing | [link](https://costbench.com/software/email-marketing/beehiiv/) | D | unknown | conflicts with other sources, quote not confirmed | 14 |
| Ghost – Pricing | [link](https://ghost.org/pricing/) | B | unknown | may be outdated, quote not confirmed | 3, 14, 16 |
| dev.to – Ghost pricing 2026 | [link](https://dev.to/nayankyada/ghost-pricing-2026-free-self-hosted-costs-pro-plans-when-to-upgrade-52a2) | C | 2026-01-01 | quote not confirmed | 14 |

**Not researched (listed so gaps stay visible):** OWASP Top 10 and OWASP LLM Top 10, NIST AI RMF and NIST AI 600-1, Microsoft Responsible AI Standard, Google PAIR, WCAG 2.2 criteria, CCPA/CPRA thresholds (official sources), US Copyright Office AI guidance, FTC Endorsement Guides, LLM API prices, quiz hosting on each platform, Stripe's official pricing, Kit (ConvertKit), the testing effect, AI/ML education market size, and the competitors Alammar, StatQuest, 3Blue1Brown, Brilliant, DataCamp and ByteByteGo.
