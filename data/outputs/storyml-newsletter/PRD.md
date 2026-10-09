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

> **Reading guide.** StoryML is a **content product about AI**, not an AI product. The first version is a free newsletter on a hosted platform, with no custom code. The scorecard verdict is **PIVOT** (average 2.7/5). Treat this PRD as the plan for a **bounded 8-issue experiment** that tests the riskiest assumptions before anyone scales the idea. It is not a plan for a full launch. All continue, pivot and stop decisions follow **one decision table in section 6**. Sections 9, 17 and 18 refer to that table.

---

## 1. Press Release and FAQ
_Based on: Amazon "Working Backwards" PR/FAQ._

### Press release (written as if launched)

**StoryML: ML concepts you'll still remember next week**

*Each issue turns one ML/AI idea into a short story, then shows you exactly where the story stops matching the real mechanism.*

Many people who build with AI, or work beside it, are teaching themselves. In one large survey, 75% of knowledge workers used AI at work, but only 39% of AI users had received AI training from their company ([source](https://news.microsoft.com/source/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/), grade B, may be outdated, quote not confirmed). Dense topics usually arrive as papers, docs or dry blog posts that are hard to remember. Examples include embeddings, RAGAS (a toolkit for scoring retrieval-augmented generation systems) and drift detection. StoryML takes one concept per issue and dramatizes it. A model becomes a character, and the concept becomes a scene with conflict and resolution. In the founder's words: *"Every model, algorithm, or system becomes a character. Every concept becomes a scene."* Evaluation methods are told as courtroom dramas, and production failures as thrillers. Every story ends with a **"Where the story breaks"** box that maps each character to the real mechanism. Each issue also has an optional quiz in three tiers: Basic, Intermediate and Expert. A technical reviewer who did not write the issue checks it, and any error is fixed in a public corrections log. *"I'd read three papers on LLM-as-Judge and still couldn't explain its failure modes. After the courtroom issue I could, and the Expert quiz showed me the one edge case I'd missed."* (illustrative quote, not a real customer) **[ASSUMPTION]**

### Customer FAQs

| Question | Answer |
|---|---|
| Do I need an ML background? | Not for the story or the plain-language summary. The Basic quiz tier is built for non-technical readers. The Intermediate and Expert tiers assume practitioner knowledge, because practitioners are the primary reader (debate outcome). |
| Are the stories accurate, or just fun? | Each story is written from the real mechanism first. The "Where the story breaks" box lists what the metaphor gets wrong. A second person reviews each issue, and errors go into a public corrections log. |
| Is this written by AI? | The first issues are written by a human. If AI drafting is ever used, every affected issue will say so, with a label that states what the AI did. See sections 10 and 11. |
| Are the quizzes graded or certified? | No. Quizzes are optional self-checks. There are no grades, certificates or records tied to your name. |
| Does it cost money? | It is free during the first 8-issue experiment. A low-priced paid tier may be tested later, and only if readers show they value it (section 15). |

### Internal FAQs

| Question | Answer |
|---|---|
| Why would anyone read this instead of asking ChatGPT for a story? | This is the biggest open question. The debate conceded that our topic list is "a topic list, not a moat." Our bet is on **trust and curation**: an independent accuracy check, a mechanism box and quizzes that test the mechanism. Before we scale, we must run two head-to-head recall tests (section 9). Test A compares a StoryML story with a plain explainer of the same length. Test B compares a StoryML story with a ChatGPT story written from a realistic, frozen prompt. The results feed the decision table in section 6. |
| How will this make money? | We test one model first: a free newsletter, then a low-priced paid tier. The course idea is shelved. We have no willingness-to-pay data yet. |
| Who is the founder, and how will they reach the first 1,000 readers? | Unknown. The Skeptic called this "the deciding issue." **[OPEN QUESTION]** |
| Can one person sustain a weekly cadence? | Unknown. We will record the hours for 3 finished issues before choosing between weekly and every two weeks. |
| How much will the experiment cost? | Unknown. The founder must set a total budget ceiling and a per-issue cost cap before issue 1 **[OPEN QUESTION]** (sections 6 and 9). |
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

**Honest summary:** the evidence shows the learning gap exists. It does not yet show that a weekly story closes it better than the alternatives (Skeptic: *"The evidence proves the problem exists, not that this solves it."*).

### Why now

1. **Behavior change:** AI use at work outpaces formal training (Work Trend Index above). People are looking for ways to learn on their own.
2. **New, fast-moving topics:** Evaluation methods such as LLM-as-Judge and RAGAS are young, and so are LLM operations practices such as prompt versioning. Practitioners have fewer settled explanations for them than for older topics **[ASSUMPTION]**. Demand for these tracks is **[NEEDS RESEARCH]**.
3. **Cheap distribution:** Hosted newsletter platforms let a solo writer launch with no code and little or no fixed cost (section 14).
4. **Counter-trend, which is also a reason:** Chatbots now generate explanations on demand. A human-checked, corrected and curated source may become more valuable as unchecked AI explanations multiply **[ASSUMPTION]**. The same trend is also our largest substitute threat.

---

## 3. Strategic Fit (GUCCI)
_Based on: GUCCI (Dr. Nancy Li)._

The findings below come from the Scorer's GUCCI analysis after the Advocate vs. Skeptic debate.

| Letter | Finding | Evidence | Implication for this PRD |
|---|---|---|---|
| **G – Goals & Mission** | The mission is clear: make dense ML/AI concepts stick through storytelling, for practitioners and non-technical readers. The commercial goals, founder background and existing channels are **blank**. | Transcript: "The goal is to make technically dense ideas stick, for both technical and non-technical readers." Debate: on money, "The founder hasn't said yet." Skeptic: "One question no test can settle: who the founder is." | Success metrics are framed as learning experiments. Revenue goals and the experiment budget are an **[OPEN QUESTION]** for the founder. |
| **U – Unmet Needs** | There is broad evidence that people must learn AI on their own. Evidence of acute, frequent pain that a story format solves is thin. | Work Trend Index (grade B). Jargon confusion from one dev.to post (grade C). Research note: "Evidence is weak on user pain points." | Before scaling, interview the 5–10 named readers and run the two recall tests (section 9). |
| **C – Competition** | This is a crowded market for in-depth explainers. News digests (TLDR AI, The Rundown AI) use a different format. Free in-depth explainers, an existing story-based ML writer and on-demand ChatGPT stories are direct substitutes. Our claimed edge can be copied and is untested. | TLDR AI format "headline, two-sentence summary, link" ([source](https://www.datacamp.com/blog/best-ai-newsletters), grade D, unknown source, quote not confirmed). Sundaresan precedent ([source](https://medium.com/mlearning-ai/learning-machine-learning-through-stories-43de0a6524c6), grade C, quote not confirmed). The Advocate conceded "a topic list, not a moat." | The competitor review (Sundaresan's current newsletter, Jay Alammar, StatQuest) is a pre-scale task (section 17). Test B checks the ChatGPT substitute directly. |
| **C – Customer Segmentation** | Primary: ML/AI practitioners brushing up, especially on eval and MLOps. Secondary: non-technical readers, served by a plain summary and the Basic quiz tier. No concrete early-adopter persona has been validated. | Advocate R1: "Make practitioners the primary reader." The Skeptic asked for 5–10 named readers to review a draft. None were provided. | Section 4 personas are illustrative until real readers confirm them. |
| **I – Integrated Ecosystem** | No founder channels are known. The only leverage is the platform: Substack Recommendations plus its app, or free hosted tiers on beehiiv or Ghost. These allow a no-code launch but give no owned distribution. | Substack claims Recommendations plus the app drive "50% of all new subscriptions and 25% of new paid" ([source](https://x.com/Substack/status/1760696631156953443), grade C, Substack's own claim, may be outdated, quote not confirmed). beehiiv is free up to 2,500 subscribers (grade D, two sources agree). Ghost charges no payment fees ([source](https://ghost.org/pricing/), grade B, may be outdated). | Platform choice affects growth more than features do (section 14). Founder reach remains **[OPEN QUESTION]** #1. |

**Overall strategic fit:** the mission is clear and the downside is small. Distribution, differentiation and the founder's own advantage are unproven. These GUCCI findings feed the section 16 scores for customer need, competitors, viability, feasibility and defensibility.

---

## 4. Target Users and Jobs-to-be-Done
_Based on: JTBD (Christensen / Ulwick); CIRCLES (I - Identify the customer)._

### Primary persona: the brushing-up practitioner
*Illustrative. Not yet validated with real readers.* **[ASSUMPTION]**

- **Who:** An ML or software engineer with 2–6 years of experience who now ships LLM features. One example is RAG (retrieval-augmented generation), where the model looks up documents before answering.
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
Practitioners working on LLM applications who must set up evaluation or monitoring soon **[ASSUMPTION]**. We chose this segment because the eval and MLOps tracks are the most distinctive part of the transcript. Demand for those tracks is **[NEEDS RESEARCH]**.

### Job statements

1. When **I have to choose an evaluation method for our RAG system next sprint**, I want to **understand what RAGAS and LLM-as-Judge actually measure and where they fail**, so I can **defend my choice in design review**.
2. When **a concept I "learned" months ago comes up in a meeting**, I want to **recall it quickly and correctly**, so I can **contribute without bluffing**.
3. When **I'm a non-technical person working beside ML engineers**, I want to **follow the idea behind the jargon**, so I can **ask good questions and make better decisions**.
4. When **I think I understand a concept**, I want to **test myself on edge cases and tradeoffs**, so I can **find my blind spots before production finds them**.

---

## 5. Market and Competitive Analysis
_Based on: Porter's Five Forces; Lean Canvas (TAM/SAM/SOM); SWOT._

### Market size (TAM / SAM / SOM)

The research found **no estimate of the AI/ML education or upskilling market** **[NEEDS RESEARCH]**. We use audience proxies only:

| Level | Estimate | Basis |
|---|---|---|
| **TAM** (everyone who might want to learn AI concepts) | Unknown **[NEEDS RESEARCH]** | Directional signal only: AI use at work outpaces training (Work Trend Index, grade B, may be outdated) |
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
| Jay Alammar visual explainers, StatQuest, 3Blue1Brown | Free in-depth explainers | Visual / video | Free (believed) **[ASSUMPTION]** | Different medium. Their quality bar is very high. | **Not researched** |
| Brilliant, DataCamp, ByteByteGo | Paid learning platforms | Courses, exercises | Unknown | We are lighter-weight and narrative | **Not researched** |
| ChatGPT and other chatbots | **Substitute** | On-demand story about any concept, instantly | Free or low cost | Our only claimed differences are independent human accuracy review, the mechanism box, tested quizzes and curation | Debated. **Test B (section 9) is required.** |

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
| Strong general evidence that stories improve recall (grade A). Distinctive tone for dry topics (eval, MLOps). Very low cost to test. Responsible design (mechanism box, corrections log). | Founder reach and credibility unknown. Workload and cost per issue unknown. No willingness-to-pay data. Format is easy to copy. |
| **Opportunities** | **Threats** |
| Possible gap in in-depth, memorable eval/MLOps content (untested). Platform recommendation networks. Team or educator sharing. | ChatGPT stories. Existing story-based ML writer. Novelty may fade. Misleading metaphors could damage trust. |

### Our differentiation (stated honestly)
"A possible gap, untested" (debate wording). We combine four things: (1) dramatized **evaluation and MLOps** tracks; (2) a **"Where the story breaks"** mechanism box; (3) **three-tier quizzes that test the mechanism, not the plot**; (4) **independent human accuracy review plus a public corrections log**. Each of these can be copied on its own. Only the combination, delivered consistently by a trusted author, can become an advantage (section 16, Defensibility).

---

## 6. Goals, Non-Goals and Success Metrics
_Based on: Google design docs (goals / non-goals); Google HEART; North Star metric._

### Goals (for the 8-issue experiment)

1. Learn whether a StoryML issue improves **one-week recall** compared with a **plain explainer of the same length** (Test A). Also compare it with a **ChatGPT story written from a realistic, frozen prompt** (Test B). Both results are directional only (section 9).
2. Learn whether **practitioners** subscribe and keep clicking through to the content without the founder pushing hard on each issue.
3. Measure the **real workload and cost** of one human-written, independently reviewed issue.
4. Learn which **track** (Concepts, Evaluation, Ops) gets the most engagement.
5. Publish with **zero uncorrected critical technical errors**.
6. Run the whole experiment **within a written budget** set by the founder before issue 1 **[OPEN QUESTION]**.

### Non-goals (for now)

- No courses, certificates or formal grading. Quizzes are self-assessment only (guardrail note).
- No interactive AI tutor or chatbot.
- No custom website, reader login or database.
- No paid tier until the go targets are met.
- No season-long story arcs. Each issue stands alone (debate outcome).
- No daily news coverage.

### North Star metric
**Engaged Learner Rate per issue (ELR)** = unique quiz starts for an issue ÷ unique openers of that issue. It is counted **per issue, not per week**, so it works at either a weekly or a two-weekly cadence. We also report the absolute number of quiz starts per issue.

- *Why:* it combines reach (opens) with learning intent (quiz starts). It works with **anonymous quizzes**, because both numbers are totals from different tools. No reader-level join is needed.
- *Data sources:* the quiz tool's start count (sessions; may double-count one person on two devices **[ASSUMPTION]**), and the platform's unique-opener count.
- *Caveat:* opens are inflated by email clients that pre-load images **[ASSUMPTION]**. That makes ELR an understated ratio, so use it as a **trend across issues**, not as an absolute figure.

### HEART metrics

All targets are **judgment, not benchmarks** **[ASSUMPTION]**. The founder must write them down and confirm them **before issue 1** (debate outcome). **[OPEN QUESTION]**

| HEART | Metric | How measured | Proposed target after 8 issues |
|---|---|---|---|
| **Happiness** | One-click rating at the end of each issue ("Was this worth your time?") | Platform poll or rating link, aggregate | ≥ 4.0 / 5 average |
| **Engagement** | ELR (North Star); click-through from email to quiz link | Quiz-tool totals ÷ platform openers; platform link tracking | ELR trend flat or rising; quiz-link clicks ≥ 15% of openers |
| **Adoption** | New subscribers per issue; "Start here" page visits | Platform | Founder sets these from known reach **[OPEN QUESTION]** |
| **Retention (primary)** | **Active reader rate:** share of subscribers who clicked any link, including the quiz link, in at least 1 of the last 3 issues | Platform per-subscriber click data. Can be computed from issue 3 onward. | Flat or rising |
| **Retention (secondary only)** | Open-rate trend | Platform | Context only. Never used alone for a decision. |
| **Task success** | (a) Quiz completion per tier; (b) Test A one-week recall | (a) Quiz tool aggregates; (b) consented recall test (section 9) | (a) ≥ 60% of quiz starters finish one tier; (b) StoryML ahead of the plain explainer by **≥ 1 of 6 quiz points** on average (directional) |

Click data has known noise: some corporate email security tools "click" links automatically **[ASSUMPTION]**. Treat sudden jumps in clicks with suspicion.

### Guardrail metrics (must not get worse)

| Guardrail | Limit |
|---|---|
| Critical technical errors found after publish | 0 left uncorrected beyond 72 hours |
| Corrections per issue (any severity) | ≤ 1 on average |
| Unsubscribe rate per issue | No issue above 2× the running average |
| Spam complaints | Near zero. Investigate any rise. |
| Founder hours per issue | Below the cap the founder sets after the first 3 issues **[OPEN QUESTION]** |
| **Cost per issue** (reviewer fee + tool fees + any AI spend, divided by issues) | ≤ the per-issue cost cap **[OPEN QUESTION]** |
| **Total experiment spend** (pre-launch through issue 8, including recall tests) | ≤ the budget ceiling **[OPEN QUESTION]** |
| Reviewer turnaround | ≤ 3 days **[ASSUMPTION]** |

### Decision table (single source of truth for continue, pivot and stop)

Sections 9, 13, 17 and 18 refer to this table and do not restate other thresholds. All thresholds are **[ASSUMPTION — judgment]** and must be confirmed before issue 1. "Pivot" means we change the format, positioning, channel or cadence and keep going. "Stop" means we end the experiment or pause until the founder makes a new decision.

| ID | Signal | Continue | Pivot | Stop |
|---|---|---|---|---|
| **DT1** | **Test A:** StoryML issue vs. a plain explainer of the same length, one-week recall on a 6-point quiz | StoryML ahead by ≥ 1 point | Within 1 point either way, **or** the explainer ahead by ≥ 1 point. Change the format (lead with the explainer, make the story shorter or optional) and re-test once. | Only through DT3 |
| **DT2** | **Test B:** StoryML issue vs. a ChatGPT story from the frozen realistic prompt, one-week recall | StoryML ahead by ≥ 1 point | Within 1 point, **or** ChatGPT ahead. Reposition around curation, independent review and corrections, not story craft. | Only through DT3 |
| **DT3** | **Combined format signal** | Either DT1 or DT2 at Continue | Neither DT1 nor DT2 at Continue, but StoryML's "would read again" rating is higher than both alternatives. Reposition as a more enjoyable, checked format, and re-test. | Neither DT1 nor DT2 at Continue **and** StoryML's "would read again" rating is not higher than both alternatives |
| **DT4** | **Reach** after 8 issues vs. the founder-set subscriber floor **[OPEN QUESTION]** | At or above the floor | Below the floor, but at least one named channel produced meaningful signups (threshold **[OPEN QUESTION]**). Focus on that channel. | Below the floor **and** no named channel produced meaningful signups |
| **DT5** | **Retention:** active reader rate (click-based, from issue 3) | Flat or rising | Falls for 4 issues in a row. Change the format (genre, length, structure). | Keeps falling for the next 3 issues after the format change, even if that runs past issue 8 |
| **DT6** | **Workload:** founder hours per issue vs. the cap | Within the cap at a weekly cadence | Over the cap weekly but within it at two-weekly. Move to two-weekly, or turn on disclosed AI aid (section 9). | Over the cap even at a two-week cadence |
| **DT7** | **Cost:** spend vs. the per-issue cap and the budget ceiling | Within the per-issue cap and on track for the ceiling | Over the per-issue cap for 2 issues in a row. Cut costs (cadence, reviewer terms, tools). | Forecast spend would exceed the budget ceiling before issue 8. Pause until the founder decides again. |
| **DT8** | **Accuracy:** independent review and post-publish errors | Named reviewer signs off every issue. ≤ 1 critical error over 8 issues. | 2 or more critical errors found after publish. Tighten the checklist and add a second review pass. | No qualified reviewer can be found. Do not publish unchecked technical stories. |
| **DT9** | **Re-score after 8 issues** (section 16 scorecard with real data) | **Go:** average ≥ 3.5 **and every criterion except AI-fit ≥ 3**. AI-fit may stay at 2 for a content product. | Everything in between | **No-Go:** average < 2.5, or ethics scored 1 |

---

## 7. User Stories and Key Flows
_Based on: CIRCLES (R - Report customer needs); Lenny Rachitsky PRD templates._

### User stories with acceptance criteria

| # | Story | Acceptance criteria |
|---|---|---|
| US1 | As a **practitioner**, I want one concept per issue told as a story so that I remember it next week. | One concept per issue. Fits within ~10–15 minutes of reading **[ASSUMPTION]**. Tagged with its track (Concepts / Evaluation / Ops). |
| US2 | As a **practitioner**, I want to see where the metaphor breaks so that I don't learn something false. | Every issue has a "Where the story breaks" box. Every character maps to a real component. At least one "the story implies X, but in reality Y" line. |
| US3 | As a **non-technical reader**, I want a plain summary so that I get the idea without math. | Summary of 3–5 sentences. No undefined jargon. Each term explained on first use. |
| US4 | As a **reader**, I want an optional quiz in three tiers so that I can check my understanding at my level. | Basic tests recall, Intermediate tests applying the concept to a new scenario, and Expert tests edge cases, tradeoffs or production situations (as in the transcript). The quiz is one click from the email. No email or login needed to take it. |
| US5 | As a **reader**, I want explanations for every quiz answer so that I learn from my mistakes. | Each option, right or wrong, has a 1–2 sentence explanation tied to the mechanism, not the plot. |
| US6 | As a **reader**, I want to know who checked the issue and whether AI was used so that I can judge how far to trust it. | An "Issue card" at the end lists the author, reviewer, AI use (None / Assisted, with details), sources and last-checked date. |
| US7 | As a **reader who spots an error**, I want to report it easily so that it gets fixed. | A "Report an error" link in every issue. Acknowledged within 48 hours **[ASSUMPTION]**. If valid, the fix appears in the corrections log. |
| US8 | As a **new subscriber**, I want a "Start here" path so that I can join at any issue. | A "Start here" page lists 3–5 recommended issues per track. The welcome email links to it. |
| US9 | As the **founder**, I want to log my hours and costs per issue so that I can choose a sustainable cadence and stay within budget. | Tracking sheet updated for every issue, showing spend against the per-issue cap and the budget ceiling (section 13). |
| US10 | As the **reviewer**, I want a clear checklist so that my review is consistent. | A checklist (section 9) is attached to each draft. Sign-off is recorded. |
| US11 | As a **recall-test participant**, I want to know what data is kept and when it is deleted so that I can agree knowingly. | A short consent form before the test covers purpose, data kept and deletion date (section 10). |

### Main user journey (reader)

1. The reader finds StoryML through a recommendation, a shared link or the founder's network.
2. The reader subscribes. Where EU/UK rules apply, they tick a **separate, unbundled** consent box, and they give consent to tracking where the law requires it (section 10).
3. Welcome email: what StoryML is, an AI-use statement, a link to "Start here", and how to unsubscribe.
4. A weekly or two-weekly issue arrives. The subject line names the concept honestly, for example "LLM-as-Judge on trial: why the judge can be biased."
5. The reader reads the story, then the **"Where the story breaks"** box, then the plain summary.
6. The reader clicks **"Test yourself"** and picks a tier.
7. The reader answers and sees the explanations immediately. Nothing is stored against their identity.
8. The reader rates the issue with one click. They can reply with questions or report an error.
9. Optional: the reader shares the issue or the quiz link.

### Production flow (founder)

1. Pick a concept and track.
2. **Write the mechanism first:** a precise, sourced explanation and the "Where the story breaks" mapping.
3. Write the story so that it fits the mechanism.
4. Write the quiz: Basic, Intermediate and Expert questions, all testing the mechanism.
5. Run the self-check (accuracy checklist).
6. The independent reviewer checks the issue and signs off.
7. Fill in the Issue card. Schedule and publish.
8. Log hours, costs and metrics.

### Correction flow
An error report comes in, and the founder triages it within 48 hours. If it is valid: fix the web version, add an entry to the corrections log, and add a note to the next email. If the error is critical (a reader could misuse the concept in production), send a short correction email immediately.

---

## 8. Requirements and Prioritization
_Based on: RICE (Intercom); MoSCoW; Kano Model._

**RICE inputs are all [ASSUMPTION].** Reach = readers affected over the first 8 issues (baseline 500). Impact = 0.25 / 0.5 / 1 / 2 / 3. Confidence = %. Effort = person-weeks to set up. RICE = R × I × C ÷ E.

**Note:** RICE undervalues learning experiments, because their reach is small even when what they teach us is decisive. Where RICE and MoSCoW disagree, MoSCoW decides.

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
| FR10 | Compliance and vendor basics: opt-out, postal address, separate EU/UK consent, cookie and tracking consent where needed, vendor data processing agreements and transfer checks, quiz-tool IP logging check, account-takeover runbook | Must | Must-be | 500 | 1 | 100% | 0.5 | 1,000 |
| FR11 | Accessible email and web format (alt text, headings, contrast, plain-text version, keyboard-usable quiz) | Must | Must-be | 500 | 1 | 80% | 0.25 | 1,600 |
| FR12 | Tracking sheet: hours, costs against the per-issue cap and the budget ceiling, opens, clicks, active reader rate, quiz totals, track | Must | Indifferent (to readers) | 500 | 1 | 80% | 0.25 | 1,600 |
| FR13 | Track tagging and per-track reporting | Should | Indifferent | 500 | 1 | 70% | 0.1 | 3,500 |
| FR14 | "Start here" page and welcome email | Should | Performance | 200 | 1 | 60% | 0.25 | 480 |
| FR15 | Consented recall tests: **Test A** (StoryML vs. a plain explainer of the same length) and **Test B** (StoryML vs. a ChatGPT story from a frozen, realistic prompt). ≥ 15 participants per arm. Minimum difference (≥ 1 of 6 points) set in advance. | **Must (experiment)** | n/a | 60 | 3 | 50% | 1.5 | 60 |
| FR16 | One-click issue rating | Should | Indifferent | 500 | 0.5 | 70% | 0.1 | 1,750 |
| FR17 | Paid tier (via the platform's built-in payments) | Could (after go targets) | Performance | 50 | 1 | 30% | 0.5 | 30 |
| FR18 | AI drafting aid (only if hours prove unsustainable, with disclosure) | Could | Reverse risk (readers may value it less) | 500 | 0.5 | 30% | 1 | 75 |
| FR19 | Season-long story arcs, required recurring characters | Won't (dropped in debate) | — | — | — | — | — | — |
| FR20 | Interactive AI tutor or chatbot | Won't (now) | — | — | — | — | — | — |
| FR21 | Certificates, formal grading, stored quiz scores tied to identity | Won't (guardrail) | — | — | — | — | — | — |
| FR22 | Custom website, reader accounts, database | Won't (now). See section 14 for when. | — | — | — | — | — | — |

---

## 9. AI System Design
_Based on: Google PAIR Guidebook; Google Model Cards._

### Does this need AI? (AI-fit)

**No, not for the reader-facing product.** The transcript describes human-authored content *about* AI. Following the PAIR question "does this need AI?", a human writer with a checklist and a hosted platform delivers the whole value proposition. The scorecard gives AI-fit **2/5** for this reason. For a content product this is acceptable, and the Go rule treats it that way (section 6, DT9).

**Answer to the guardrail question: will stories or quizzes be written by AI?**
- **Version 1: no.** At least the first 3 issues are fully human-written: story, box, summary and quiz (debate outcome: "Start human-written").
- **Later: only if** the logged hours trigger a pivot under DT6. If AI drafting is then used, it is **disclosed** on every affected issue (sections 11 and 12).
- **Never:** AI that grades readers, stores profiles or chats with readers in this phase.

### Where AI may be used (optional, internal, human-checked)

| Use | Allowed? | Why |
|---|---|---|
| Brainstorming story settings and metaphors | Yes, if logged | Low risk. A human writes the final text. |
| Drafting quiz *distractors* (wrong answer options) | Yes, if logged and reviewed | Saves time. Each item is still checked against the mechanism. |
| A "metaphor stress test" (ask a model what false beliefs a metaphor might create) | Yes, as an aid only | Helps find misleading implications. It does not replace the human reviewer. |
| Drafting the mechanism box or technical claims | **No** | This is the core of reader trust. Model errors here would directly mislead readers. |
| Drafting full stories | Only under the DT6 rule, with disclosure | The Skeptic warned that this erodes the human-value difference. |
| Grading or tutoring readers | **No** | Out of scope. It would add EU AI Act duties and privacy risk. |
| Generating the Test B comparison story | Yes, test material only, never published as StoryML content | Needed to test the ChatGPT substitute fairly |

### Model choice
None in version 1. If AI aid is turned on, use a general-purpose large language model through a provider's API. Choose it with a small bake-off on 3 "golden" concepts (one per track), scored against the accuracy rubric below. Provider prices were **not researched** **[NEEDS RESEARCH]**.

### Data sources
Primary papers and official documentation for each concept (for example the original paper or a tool's own docs), listed in the Issue card. Reader data (emails, quiz answers, test responses) is **never** sent to any model.

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
| Anthropomorphism ("the model wants/knows/decides") corrected in the box | Reviewer | 100% |
| Quiz items tagged recall / apply / reason, and answers verified | Reviewer | 100% |
| Code or math snippets run or re-derived | Author | 100% |
| Critical errors at publish | Reviewer sign-off | 0 |

**B. Format effectiveness: two head-to-head recall tests (FR15). These test the riskiest assumption.**

The Skeptic asked for a three-way test. We split it into two two-arm tests, because 30 people across three arms gives only about 10 per arm, and a "tie" at that size would mostly be noise.

*Rules shared by both tests (fixed in advance):*
- **Participants:** practitioner volunteers, **≥ 15 per arm** **[ASSUMPTION — enough for a directional signal only, not statistical proof]**, randomly assigned. Each person takes part in only one test. Informed consent comes first (section 10).
- **Materials:** the same concept in every arm, with arms of similar length (±10% word count). The 6-question mechanism quiz is written and **frozen before anyone sees any material**. Its questions test the mechanism, never story details, so no arm has an unfair edge.
- **Measure:** quiz score one week later (0–6), plus reading time and a "would read again" rating (1–5). Where possible, a second person scores the answers without knowing which arm they came from.
- **Pre-set minimum difference:** **≥ 1 of 6 points** on the average score. Smaller gaps count as "within 1 point" (no clear difference).
- **Interpretation:** results are **directional**. They feed the decision table (DT1–DT3, section 6). No public learning-outcome claims are made from them.
- **If recruitment falls short:** run Test A first. Treat trouble recruiting 30 practitioners as an early warning about reach (DT4).

*Test A — is the story the active ingredient?*
- **Arm 1:** the full StoryML issue (story, "Where the story breaks" box, plain summary).
- **Arm 2:** a **standalone expository explainer** of the same length on the same mechanism. It is written to the same accuracy standard and reviewed by the same reviewer, with no story and no character mapping.
- **Outcome:** decision table rows DT1 and DT3.

*Test B — does StoryML beat a realistic ChatGPT alternative?*
- **Arm 1:** the full StoryML issue.
- **Arm 2:** a ChatGPT story built from a **realistic prompt, frozen before the test**. Proposed wording **[ASSUMPTION]**: *"Explain [concept] to an ML engineer as a short [genre] story of about [N] words. Keep it technically accurate. After the story, explain exactly where the analogy breaks and what the real mechanism is."* Generate it **once**, with the model name, version and date recorded. Do not edit the output and do not pick the best of several runs.
- **Outcome:** decision table rows DT2 and DT3.

**C. Quiz learning value.** We do **not** compare quiz takers with non-takers on live issues. Quizzes are anonymous, and that comparison would be biased by who chooses to take them. Instead, an **optional Test C**, run with consented participants after Test A, randomly gives half the readers the self-check right after reading and half no self-check, then measures one-week recall. It is directional only. The research did not cover the "testing effect" (learning through practice questions) **[NEEDS RESEARCH]**.

### Failure handling: what happens when content is wrong

| Failure | Detection | Response | Human-in-the-loop point |
|---|---|---|---|
| Wrong technical claim | Reviewer, reader report | Correction log entry, web fix, note in next email. Separate email if critical. Counts toward DT8. | Reviewer sign-off before publish |
| Misleading metaphor | Metaphor stress test, reviewer, confusion in quiz totals (many readers pick the same wrong answer) | Expand the box. Add a correction. | Author and reviewer |
| AI-invented claim (confabulation, if AI aid is used) | Source tracing check | Remove it. Log the incident. Tighten the prompt. | Author owns every sentence |
| Wrong quiz answer key | Reader report, odd answer patterns | Fix the key and note it in the log | Reviewer |

### Cost per request, budget and latency

- **Version 1 AI cost:** $0 (no AI). The Test B story costs a single generation.
- **If AI aid is turned on:** cost per issue is unknown **[NEEDS RESEARCH]**, because no LLM price data was gathered. It counts against the per-issue cost cap. If the monthly AI spend passes a founder-set limit, AI aid is turned off.
- **Experiment budget [OPEN QUESTION]:** the founder sets, before issue 1, (1) a **total budget ceiling** for pre-launch through issue 8, and (2) a **per-issue cost cap**. Cost lines to estimate:

| Cost line | Estimate |
|---|---|
| Reviewer fee × 11 issues (3 pre-launch + 8 published) | Unknown **[OPEN QUESTION]** |
| Quiz tool (if a paid plan is needed) | Unknown **[NEEDS RESEARCH]** |
| Platform fee (Substack $0 while free; Ghost Starter listed at $18/mo, grade B, may be outdated) | Depends on platform choice |
| PO box or mail service for the CAN-SPAM postal address | Unknown **[ASSUMPTION]** |
| Recall-test participant thanks or incentives (if any) | Founder decides **[OPEN QUESTION]** |
| AI aid (if turned on) | Unknown **[NEEDS RESEARCH]** |

  Spend against both limits is a guardrail (section 6) and a decision signal (DT7).
- **Latency:** drafting happens offline, so model latency does not matter. Reader-facing target: the issue page and quiz load within ~2 seconds on a typical mobile connection **[ASSUMPTION]**. This mostly depends on the platform and quiz tool chosen.
- **The main cost is human time:** author hours (DT6) plus the reviewer fee.

---

## 10. Security and Privacy
_Based on: OWASP Top 10; OWASP Top 10 for LLM Applications; GDPR / CCPA._

**Scope note:** the research agents did not research the OWASP Top 10, the OWASP Top 10 for LLM Applications, CCPA thresholds, or vendor data processing and transfer rules **[NEEDS RESEARCH]**. The controls below are practical judgment for a hosted newsletter **[ASSUMPTION]**. The legal rules on email and consent come from grade A sources.

### Authentication and authorization
- **Readers:** no accounts, no passwords. Subscribing needs only an email address. The quiz needs no login.
- **Founder accounts** include the newsletter platform, quiz tool, domain registrar, email, payment processor (later) and AI provider (if used). Turn on **multi-factor authentication** everywhere. This is a second login step, such as a code from an app. Use a password manager and unique passwords.
- **Least privilege:** the reviewer gets comment or draft access only. They never get publishing rights or access to the subscriber list.
- **Account takeover is the main threat.** A hijacked newsletter account could email every subscriber with phishing links. Keep account recovery codes offline.

### Account-takeover response (runbook)
If any founder account shows signs of compromise (unknown login alert, unexpected sends, changed settings):
1. **Lock:** pause scheduled sends, sign out all sessions, and lock or suspend the account through the platform.
2. **Rotate credentials:** change the password, reset multi-factor authentication, revoke and reissue any API keys, and check the recovery email and phone.
3. **Notify subscribers:** if anything was sent or subscriber data was exposed, send a plain warning ("Ignore the email sent on [date]; do not click its links"). If personal data was exposed, check whether a regulator must be notified **[NEEDS RESEARCH: GDPR breach notification duties]**.
4. **File a report with the platform** (and the quiz tool or domain registrar if they are affected), and ask for their logs.
5. **Log the incident:** what happened, when, impact, steps taken and lessons learned. Review the runbook afterwards.

### Encryption and secrets
- Use only platforms that serve pages over HTTPS **[ASSUMPTION: the hosted platforms do this by default; verify]**.
- Store any API keys (quiz tool, AI provider) in the password manager. Never put them in drafts, shared docs or prompts.
- Set up domain email authentication (the standard sender-verification records) so others cannot easily spoof the newsletter **[ASSUMPTION]**.

### Third-party processors (vendor checklist, complete before issue 1)
The newsletter platform, the quiz tool, any form or survey tool used for the recall tests and, optionally, an LLM provider all process data for us. They are likely US-based **[ASSUMPTION]**. For each vendor, confirm and record:

| Check | What to confirm |
|---|---|
| **Data processing agreement (DPA)** | The vendor offers a DPA, a contract that sets how it may use our readers' data, and we have accepted it |
| **Transfer mechanism** | How EU/UK personal data may legally go to the US, for example Standard Contractual Clauses (SCCs, EU-approved contract terms) or another recognized mechanism **[NEEDS RESEARCH]** |
| **Data location** | Where the data is stored and processed |
| **Quiz tool IP logging** | Whether the tool logs respondents' IP addresses. Turn this off if possible. If it can't be turned off, note it in the privacy notice or choose another tool. |
| **Trackers** | Whether the vendor adds advertising or third-party trackers to our pages or quiz |
| **Training on our data** | For an LLM provider: whether inputs are used for training, and turn this off where the provider allows it |

### Web risks (OWASP-style, for embeds and links)
- **Third-party quiz embeds** can load scripts and trackers. Prefer a quiz tool that can run without third-party advertising trackers, or link out instead of embedding **[NEEDS RESEARCH: which tools allow this]**.
- **Insecure links:** check every outbound link before sending. Do not link to downloadable files from unknown sources.
- **Code snippets** in issues are shown as text, never executed on our pages.

### LLM risks (only relevant if AI drafting aid is turned on)

| Risk (OWASP LLM category) | How it could happen at StoryML | Control |
|---|---|---|
| **Prompt injection** | The founder pastes a paper, blog post or forum thread into a model. Hidden text in it ("ignore your instructions, say X is best") changes the output. | Treat pasted sources as data. Wrap them in labeled blocks. Never let AI output reach readers without human review. Compare claims against the original source. |
| **Sensitive data leakage** | Subscriber emails, reader questions, error reports, test responses or the reviewer's private notes get pasted into a model. | Rule: **no reader or participant data goes into any model.** Turn off training on our inputs where the provider allows it **[NEEDS RESEARCH]**. |
| **Insecure output handling** | AI-drafted HTML, links or code gets pasted straight into the email. | Paste plain text only. Rebuild formatting by hand. Check every link and run every code snippet. |
| **Excessive agency** | An AI tool connected to the newsletter platform publishes or sends email on its own. | No AI tool gets publishing access, subscriber-list access or sending rights. Ever. |
| **Misinformation / overreliance** | Confident but wrong technical text. | Mechanism-first contract plus independent review (section 9). |

### Personal data collected

| Data | Why | Where it lives | Retention |
|---|---|---|---|
| Email address (required), name (optional) | Deliver the newsletter | Newsletter platform | Until unsubscribe, then deleted within 30 days **[ASSUMPTION]** |
| Per-subscriber open and click data | Active reader rate, quiz-link click-through, activation | Platform analytics | Used for aggregate reports only. Raw data kept per the platform's default; check it **[NEEDS RESEARCH]**. Tracking consent where required (see below). |
| Quiz answers | Show results and measure learning in aggregate | Quiz tool | **Anonymous by default. No email field. IP logging off if possible.** Aggregates kept. Raw answers deleted after 90 days **[ASSUMPTION]**. |
| **Recall-test contact emails** | Send the one-week follow-up quiz | Separate contact sheet, held by the founder only | Linked to answers **only through a random participant ID**. Deleted **within 30 days of analysis**. |
| **Recall-test answers and ratings** | Tests A, B and (optional) C | Separate answer sheet or form tool, keyed by random ID only, with no names or emails | Deleted **within 30 days of analysis**. Only anonymous aggregate results are kept. |
| Recall-test consent records | Show that consent was given | Contact sheet | Deleted together with the contact emails **[ASSUMPTION; check whether consent proof must be kept longer — NEEDS RESEARCH]** |
| Error reports and reader replies | Corrections, feedback | Email inbox | 12 months **[ASSUMPTION]** |
| Payment data (later) | Paid tier | Platform's payment processor. We never see card numbers. | Per processor |

**Recall-test consent form (required before taking part).** In plain language, the form states:
- the **purpose**: comparing how well different explanations are remembered;
- **what we keep**: an email address for the one-week follow-up, quiz answers, reading time and a rating;
- **how it is stored**: emails are kept apart from answers and linked only by a random ID;
- **the deletion date**: within 30 days of analysis, with the actual date written on the form;
- that taking part is **voluntary**, with no effect on the newsletter subscription;
- that participants can **withdraw** at any time before analysis by replying to the founder.

Participants tick an unbundled "I agree" box. This is informal product research, not academic research. If a university partner is ever involved, its ethics review rules apply **[ASSUMPTION]**.

Whether identifiable quiz results would need their own lawful basis or profiling notices under GDPR was **not researched** **[NEEDS RESEARCH]**. Keeping live quizzes anonymous avoids most of this question.

### Email law and consent (grade A sources)
- **CAN-SPAM (US)** covers commercial email, "including email that promotes content on commercial websites" ([source](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business), grade A, quote not confirmed). Once we promote a paid tier or a sponsor, assume we are covered. Requirements:
  - A working opt-out, honored "within 10 business days", that keeps working for at least 30 days after sending (same source, grade A, quote not confirmed).
  - "Your message must include your valid physical postal address" (same source, grade A, quote not confirmed). Use a PO box or a mail service if the founder works from home **[ASSUMPTION]**.
  - Being a subscriber does not remove the right to opt out (same source, grade A, quote not confirmed).
  - Honest headers and subject lines. Penalties can reach "$53,088" per violating email (same source, grade A, quote not confirmed; the amount is adjusted for inflation, so check the current figure).
  - The US does not require opt-in ([source](https://www.ftc.gov/business-guidance/blog/2015/08/candid-answers-can-spam-questions), grade A, may be outdated, quote not confirmed). We use opt-in anyway because EU/UK rules need it.
- **EU/UK:** marketing messages usually need consent under UK e-privacy law ([source](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/when-is-consent-appropriate/), grade A, quote not confirmed). Consent bundled into terms and conditions is presumed not freely given ([source](https://edpb.europa.eu/sites/default/files/consultation/edpb_guidelines_202008_onthetargetingofsocialmediausers_en.pdf), grade A, may be outdated, quote not confirmed). **Requirement:** a separate, unticked signup consent, with no bundling into terms.
- **No bought or imported lists** unless we can show the data was collected in line with GDPR and may be used for marketing ([source](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/legal-grounds-processing-data/can-data-received-third-party-be-used-marketing_en), grade A, quote not confirmed). Policy: **we never buy lists.**
- **Cookies and tracking:** UK law requires consent for cookies and similar tracking ([source](https://ico.org.uk/media2/kz0doybw/guidance-on-the-use-of-cookies-and-similar-technologies-1-0.pdf), grade A, quote not confirmed). This covers blog analytics and possibly per-subscriber email open and click tracking, which our retention metric relies on. Use the platform's consent options, or a cookieless analytics setup **[NEEDS RESEARCH]**. If many EU/UK readers decline tracking, the active reader rate is computed only over consenting subscribers, and this is noted on the dashboard.
- **CCPA/CPRA (California):** current thresholds are unconfirmed from an official source. A small newsletter may fall below them **[NEEDS RESEARCH: oag.ca.gov / cppa.ca.gov]**.

### User rights
Readers can unsubscribe in one click, ask for a copy of their data, ask for deletion, and correct their details. Recall-test participants can withdraw before analysis. The plain-language privacy notice, linked from the signup form, explains what is collected, why, which vendors process it, how long it is kept and how to use these rights. Requests are answered within one month **[ASSUMPTION based on the general GDPR norm; verify]**.

---

## 11. Responsible AI
_Based on: Microsoft Responsible AI Standard v2 and Impact Assessment; NIST AI RMF; EU AI Act._

**Scope note:** the research agents did not research the Microsoft Responsible AI Standard, the NIST AI RMF or the NIST Generative AI Profile **[NEEDS RESEARCH]**. We use their principle names as a checklist. The EU AI Act points come from grade A sources.

StoryML's main responsible-AI risk is **not a model**. It is **teaching people wrong things about AI**, at scale, in a memorable format. A memorable error is worse than a forgettable one.

### Principle by principle

| Principle | Risk specific to StoryML | Control |
|---|---|---|
| **Reliability and safety (technical accuracy)** | A vivid metaphor makes a wrong mental model stick. Example: a story where "embeddings are a library where similar books sit on the same shelf" might suggest a fixed, human-readable layout. | Mechanism-first authoring. "Where the story breaks" box. Independent reviewer. Quizzes test the mechanism, not the plot. Public corrections log. DT8 escalation. *This answers the guardrail note on accuracy.* |
| **Transparency (anthropomorphism)** | Turning models into characters with goals and feelings ("the Transformer *wanted* to pay attention") may lead readers to believe that models intend, know or understand things. | Every box has a standard line, "In reality, the model doesn't *want* anything: …", followed by the actual computation. The reviewer checks for this. |
| **Fairness** | Characters, villains and settings could rely on stereotypes, for example about nationality, gender or disability. "Evil hacker" clichés could also misrepresent security work. | Character guidelines: varied names and roles, no group-based villains. The reviewer checks this too. Topics such as bias in evaluation are told accurately. |
| **Inclusiveness** | Heavy idioms and cultural references may confuse non-native English readers. Dense prose shuts out non-technical readers. | Plain summary. Glossary links. Limited idioms. Accessible formatting (section 14). The Basic tier is designed for newcomers. |
| **Privacy** | Quiz answers could reveal what readers do not know. Recall-test data identifies participants. | Anonymous live quizzes. No profiling. Consented, time-limited, separated recall-test data (section 10). |
| **Accountability** | No one owns errors. | The founder is accountable for every published word. The reviewer is named on each issue. The corrections log is public. |
| **Honest marketing** | Overstated claims ("master RAG in 10 minutes"). | Subject lines and promotion describe the concept honestly. No learning-outcome claims: the recall tests are directional and internal only. |

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
- For deployers, the text-labeling duty targets text "published on matters of public interest **without human review or editorial control**" ([source](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act), grade A, quote not confirmed). Human-edited StoryML issues may fall outside this duty. Whether educational ML content counts as "public interest" is unclear **[NEEDS RESEARCH: read the Commission's transparency guidelines directly]**.
- For "evidently artistic, creative, satirical, fictional" works, disclosure is reduced to a form that doesn't spoil the work (same source, grade A, quote not confirmed). This may apply to dramatized stories.
- These duties apply **from 2 August 2026** ([source](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content), grade A, quote not confirmed). Assume they apply at our launch.
- The Code of Practice is voluntary, but Article 50 is legally binding. The EU has published icons for labeling AI content (same source, grade A, quote not confirmed).
- If we ever add an AI tutor or chatbot, users must be told they are talking to an AI unless it is obvious (FAQ source, grade A, quote not confirmed). This is a Won't-have item for now.

**Our disclosure policy (stricter than the minimum, because trust is the product):**
1. Each issue's Issue card states **"AI use: None"** or **"AI use: Assisted — [what, e.g., quiz distractor ideas; story outline]. All technical content written and checked by humans."**
2. If an issue's story text is substantially AI-drafted, a short line sits at the top of the issue as well as in the card. Consider using the EU icon.
3. The welcome email and the About page describe the policy.
4. Even where a legal exception (human editorial control, creative work) might apply, we **still disclose**.
5. Test B material generated by ChatGPT is shown only to consented participants, clearly labeled as AI-generated, and never published as StoryML content.

### Impact assessment summary (Microsoft-style, light)
- **Intended use:** self-directed learning about ML/AI concepts.
- **Not intended for:** formal training records, hiring, certification, or production decisions made without consulting primary sources.
- **Stakeholders affected:** readers, their teams (who may act on what readers learned), recall-test participants, and the writers whose work we cite.
- **Harms ranked:** (1) misleading mental models; (2) false sense of mastery from passing quizzes; (3) stereotyped characters; (4) undisclosed AI use damaging trust.

---

## 12. Explainability
_Based on: Google PAIR (explainability + trust); Google Model Cards._

Here, "explainability" means **how a reader can see why an issue says what it says, how far to trust it, and where it simplifies.** We borrow the Model Card idea (a short, standard fact sheet) and apply it to each issue.

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
- Where experts disagree (for example, on how reliable LLM-as-Judge is), the issue says so plainly. It does not let the story's resolution suggest a single answer.

### Quiz explainability
- Every answer option has an explanation: why it is right or wrong, and which part of the mechanism it tests.
- Each question carries a tag for its tier logic: "Recall", "Apply" or "Reason about tradeoffs."
- Results show which parts of the mechanism a reader missed, not just a score.

### Corrections log
A public page lists the date, the issue, what was wrong, what is right now, and who reported it (with permission). It shows readers how errors are handled.

---

## 13. Observability and Operations
_Based on: Google SRE practices; LLM observability practice (tracing, evals in production)._

Specific tools for newsletter analytics, web analytics and LLM tracing were **not researched** **[NEEDS RESEARCH]**. Version 1 uses **platform analytics, quiz tool reports and one spreadsheet**. That is enough at this scale.

### What we log (per issue)

| Category | Metrics | Source |
|---|---|---|
| **Delivery** | Sent, delivered, bounce rate, spam complaints | Platform |
| **Engagement** | **ELR** (unique quiz starts ÷ unique openers), quiz-link clicks, one-click rating. Opens are logged as a rough, secondary signal. | Quiz tool totals + platform |
| **Retention** | **Active reader rate** (share of subscribers who clicked in ≥ 1 of the last 3 issues), from issue 3 onward | Platform per-subscriber clicks |
| **Learning** | Quiz starts and completions per tier, average score per tier, most-missed questions (all aggregate) | Quiz tool |
| **Growth** | New subscribers, unsubscribes, signup source, "Start here" visits, activation (new subscribers who click the quiz link in their first 2 issues) | Platform |
| **Quality** | Error reports received, corrections issued, severity, time to correct | Corrections log |
| **Workload** | Author hours (research / writing / quiz / revisions), reviewer hours, turnaround days | Founder's log |
| **Cost** | Platform fees, quiz tool fees, reviewer fee, recall-test costs, AI spend (if any); spend per issue vs. per-issue cap; cumulative spend vs. budget ceiling | Spreadsheet |
| **Track** | All the metrics above split by Concepts / Evaluation / Ops | Spreadsheet |

### Quality monitoring in "production"
- **Signs of confusion:** if more than 50% of quiz takers choose the same wrong answer **[ASSUMPTION threshold]**, re-check that part of the story. The metaphor may be misleading.
- **Scheduled re-checks:** issues labeled "Fast-changing" are reviewed every 3 months **[ASSUMPTION]**, and their "Last checked" date is updated.

### Dashboard (one spreadsheet tab)
It shows ELR per issue, active reader rate trend (primary retention line), open-rate trend (secondary, greyed), quiz funnel by tier, hours and cost per issue against their caps, cumulative spend against the budget ceiling, corrections count, per-track comparison, and the current status of each decision-table row (DT1–DT9, section 6).

### Alerts (manual checks after each send at first; automate later if the platform allows)

| Alert | Trigger | Action |
|---|---|---|
| Unsubscribe spike | Rate > 2× running average | Review the issue's tone, length and accuracy |
| Retention decline | Active reader rate falls for 4 issues in a row | Apply DT5 (format change) |
| Error report | Any | Triage within 48 hours |
| Critical error confirmed | Any | Correction email within 72 hours. Count toward DT8. |
| Spam complaints or bounces rising | Any clear increase | Check list hygiene and sender setup |
| Missed publish date | Any | Re-plan cadence. Two misses lead to a cadence review. |
| Workload over cap | Hours > cap for 2 issues in a row | Apply DT6 |
| **Per-issue cost over cap** | Spend > per-issue cap for 2 issues in a row | Apply DT7 (cut costs) |
| **Budget ceiling approaching** | Cumulative spend ≥ 80% of the ceiling, or forecast to exceed it before issue 8 | Founder review. At forecast overrun, apply DT7 (pause). |
| AI spend over limit (if used) | Monthly limit hit | Turn off AI aid |
| Suspected account compromise | Unknown login alert, unexpected send, changed settings | Run the account-takeover runbook (section 10) |

### Service levels (SRE-style, simple)
- **Publishing:** ≥ 90% of issues ship on the planned day **[ASSUMPTION]**.
- **Corrections:** critical corrections within 72 hours. Others within 7 days.
- **Reader replies and reports:** acknowledged within 48 hours.

### Prompt and model versioning (only if AI aid is turned on)
- Store prompts in a versioned file or document. Every change gets a version number and a note.
- Record the **model name and version** for each issue in the internal log, and the type of AI use in the public Issue card. Record the same for the frozen Test B prompt and output.
- Keep a **golden set** of 3 concepts (one per track) with known-good mechanism boxes. **Re-run the golden set** whenever the provider changes or updates the model, or the prompt changes. The output must pass the accuracy checklist before the new model or prompt is used on live issues.
- Log every AI-assisted section, so that if a model is later found to make a systematic error, affected issues can be found and re-checked.
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
          │                    explanations per answer, IP logging off)
          ▼                           │ aggregate totals only
 Platform analytics ──────► Tracking spreadsheet ◄── Quiz reports
                                     ▲
 Recall tests (consented): contact sheet ─random ID─ answer sheet
                                     ▲ (aggregate results only)
 [Optional, off by default] LLM API ─┘ (internal drafting aid only)
```

### Build vs. buy
**Buy (use hosted tools) for everything in version 1.** The research summary concluded: "the simplest first version is a hosted newsletter platform… with no custom code."

### Platform alternatives considered

| Option | Cost facts (from research) | Strengths | Weaknesses |
|---|---|---|---|
| **Substack** | Free to publish. Takes 10% of paid revenue plus Stripe fees ([source](https://schoolmaker.com/blog/substack-pricing), grade D, unknown source, quote not confirmed). The research summary says Substack's own help page confirms this, but no link was provided **[NEEDS RESEARCH]**. Writers keep "roughly 87%" of each paid subscription ([source](https://www.amysuto.com/desk-of-amy-suto/substack-pricing), grade D, single source, quote not confirmed). | Recommendations network plus app drive "50% of all new subscriptions" (Substack's claim, grade C, may be outdated, quote not confirmed). Over 5 million paid subscriptions on the platform ([source](https://www.tubefilter.com/2025/03/12/substack-five-million-paid-subscribers-journalist-reporter-newsletter/), grade D, 2025-03-12, quote not confirmed). | Takes a cut of revenue. Less design control. Quiz support unknown. DPA and per-subscriber click export unconfirmed **[NEEDS RESEARCH]**. |
| **beehiiv** | Free up to 2,500 subscribers ([source](https://www.emailtooltester.com/en/reviews/beehiiv/pricing/), grade D; [second source](https://redefiningretirement.io/p/beehiiv-review-2025-pricing-and-promo), grade D, 2026-01-01; both quote not confirmed). Paid plan names and prices **conflict**: Lite $59 / Pro $109 vs. Scale $49 / Max $109 ([source](https://costbench.com/software/email-marketing/beehiiv/), grade D, quote not confirmed). **[NEEDS RESEARCH: beehiiv.com/pricing]** | Free tier fits the experiment's size | Paid features may be needed for monetization. Prices unclear. |
| **Ghost (Pro)** | "No payment fees" ([source](https://ghost.org/pricing/), grade B, may be outdated, quote not confirmed). Starter listed at $18/mo billed yearly (same source, grade B, captured copy may be old). Open-source and self-hostable ([source](https://dev.to/nayankyada/ghost-pricing-2026-free-self-hosted-costs-pro-plans-when-to-upgrade-52a2), grade C, quote not confirmed). | Keeps all paid revenue. More control. Exit path to self-hosting. | Monthly cost from day one counts against the budget. No known built-in discovery network. |
| **Custom site** (for example a web framework, hosting and a database) | Not researched | Full control over interactive quizzes | Weeks of build effort. Solves no current risk. |

**Recommendation [OPEN QUESTION — founder decides]:** start on **Substack**, because **distribution is the deciding risk**. Its claimed recommendation network is the only built-in growth channel in our evidence (grade C), and its 10% fee costs nothing while the newsletter is free. Choose beehiiv or Ghost instead if the founder already has an audience elsewhere, or once paid revenue makes Substack's 10% fee significant. Confirm before committing: subscriber export (so we can leave later), per-subscriber click data (needed for the active reader rate), the vendor DPA and transfer mechanism (section 10), and how readers reach the quiz in one click from the email **[NEEDS RESEARCH]**.

**Quiz hosting:** it is unknown whether any of these platforms can host a three-tier interactive quiz natively **[NEEDS RESEARCH]**. Default plan: link from the email to an external form tool, or to a simple page on the platform with collapsible answers. The research agents named Typeform and Tally only as examples to check, not as tested options. The chosen tool must report aggregate start and completion counts per issue (for ELR), and must allow IP logging to be turned off or disclosed.

### When to add more (not now)

| Capability | Add when… |
|---|---|
| Reader login and database | Readers ask to track progress across issues, **and** DT9 reaches Go |
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
| **Accessibility (WCAG 2.2 AA)** | Specific success criteria were **not researched** **[NEEDS RESEARCH]**. Planned practices: alt text on every illustration; real headings; sufficient color contrast; never using color alone to show right or wrong answers; a plain-text email version; quizzes fully usable by keyboard with visible focus; adequate touch-target size; no login (so no accessible-authentication issues); readable at 200% zoom. The recall-test consent form and quiz follow the same rules. |
| **Portability** | Content stored in our own docs as well as on the platform, so we can switch platforms. |

---

## 15. Pricing and Go-to-Market
_Based on: Lean Canvas (revenue, channels); AARRR pirate metrics._

### Pricing tiers

| Phase | Tier | Price | Contents |
|---|---|---|---|
| Experiment (issues 1–8) | Free | $0 | Everything: story, box, summary, all quiz tiers |
| After DT9 Go | Free | $0 | Weekly or two-weekly issue, Basic and Intermediate quizzes **[OPEN QUESTION]** |
| After DT9 Go | Paid (test) | **[OPEN QUESTION]** | Options to test: full archive, deep-dive appendices, monthly Q&A. We do **not** lock the Expert tier at first, because practitioners are the primary reader **[ASSUMPTION]**. |

**Price evidence is thin.** The only anchor is Ahead of AI's paid tier at $6/mo ([source](https://pasqualepillitteri.it/en/news/276/best-ai-newsletters-substack-pricing-guide), grade D, **single source**, quote not confirmed). Per our rules, **we do not set our price from this figure**. It only suggests that technical AI newsletters may be priced low, and a low price needs a large audience. The Rundown AI makes money from a separate course reportedly priced at $84/mo on an annual plan (grade D, single source). Our course idea is shelved. Sponsorships are possible later, but FTC endorsement rules for sponsored content were **not researched** **[NEEDS RESEARCH]**, and sponsor emails clearly fall under CAN-SPAM (section 10).

**Experiment budget.** No revenue is expected during the experiment. All spend is capped by the budget ceiling and the per-issue cost cap set by the founder **[OPEN QUESTION]** (sections 6 and 9, DT7).

### Channels

| Channel | Evidence | Status |
|---|---|---|
| Founder's existing network | None | **Deciding unknown [OPEN QUESTION]**: name 3 specific channels for the first 1,000 readers |
| Substack Recommendations and app | "50% of all new subscriptions" (Substack's own claim, grade C, may be outdated) | Use if on Substack. Ask related writers to swap recommendations. |
| LinkedIn, Reddit, ML community forums and chats | Not researched **[NEEDS RESEARCH]** | Test by posting a standalone excerpt plus a quiz link, following each community's rules |
| Educators and team leads sharing issues | **[ASSUMPTION]** | Offer "use this in your team" permission |
| Recall-test recruitment | None | Recruiting 60+ practitioners for Tests A and B is also an early test of reach (DT4) |

### Launch audience
Practitioners building LLM applications. Lead with **Evaluation** and **Ops** issues as the distinctive hook, while measuring whether they actually beat the core Concepts track.

### Growth loops **[ASSUMPTION — all untested]**
1. **Quiz challenge loop:** "Can you pass the Expert tier on LLM-as-Judge?" A shareable link brings people to the issue, and some subscribe.
2. **Recommendation loop:** other writers recommend StoryML, and StoryML recommends them back.
3. **Reader request loop:** readers reply with concepts they want covered. The issue credits the request, and the requester shares it.

### AARRR

| Stage | Metric | How measured | Experiment target **[ASSUMPTION — judgment]** |
|---|---|---|---|
| Acquisition | New subscribers per issue, by source | Platform | Founder-set **[OPEN QUESTION]** |
| Activation | Share of new subscribers who **click the quiz link** in their first 2 issues | Platform per-subscriber link tracking (no quiz-tool join needed) | ≥ 30% of new subscribers |
| Retention | Active reader rate (click-based); open rate secondary | Platform | Flat or rising (DT5) |
| Referral | Shares, recommendation signups | Platform | Track and set a baseline |
| Revenue | Paid conversions (real payments, not stated interest) | Platform | Only after DT9 Go. Baseline to be set. |

---

## 16. Product Evaluation Scorecard
_Based on: `packages/frameworks/scorecard.json` (Cagan Four Risks, GUCCI, Kano, HEART, 7 Powers, Responsible AI frameworks)._

GUCCI was run first (section 3) and fed customer need, competitors, feasibility, viability and defensibility. The scores below are **copied without change** from the Scorer's evaluation after the Advocate vs. Skeptic debate.

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

**Go rule for the re-score (product-specific adaptation).** The standard scorecard Go rule is "average ≥ 3.5 and every criterion ≥ 3". For StoryML, AI-fit is expected to stay at 2, because this is a content product that does not need AI. Under the standard rule, the experiment could never reach Go. For the re-score after 8 issues, this PRD therefore uses: **Go = average ≥ 3.5 and every criterion except AI-fit ≥ 3. AI-fit may stay at 2 for a content product.** The Pivot and No-Go rules are unchanged (decision table DT9, section 6; decision D11). This adaptation does **not** change any current score or the current verdict. At an average of 2.7, StoryML is PIVOT under either rule. Founder approval is required **[OPEN QUESTION]**.

**What would move the sub-3 scores (for the re-score; scores themselves unchanged):**
- **Competitors (2):** finish the analysis of Sundaresan, Alammar and StatQuest, and reach Continue on Test B against a ChatGPT story (DT2).
- **Viability (2):** name the founder's channels, then count real paid conversions.
- **Defensibility (2):** build evidence of founder reputation, such as a track record, reader trust signals and a corrections record over time.
- **AI-fit (2):** expected to stay low. Under the adapted Go rule above, it does not block Go and is not a target to fix.

---

## 17. Risks, Assumptions and Open Questions
_Based on: Cagan Four Risks; NIST AI RMF (Map / Manage)._

### Unresolved Skeptic concerns, with a way to test or fix each

| # | Concern (from evaluation) | Test or fix | When |
|---|---|---|---|
| S1 | Founder background, current reach, and three named channels for the first 1,000 subscribers | The founder writes a one-page "who I am and where readers will come from", naming 3 specific channels with their expected reach. Outcome tracked through DT4. | Before issue 1 |
| S2 | The three-way test (story vs. box only vs. ChatGPT story) on one-week recall has not been run | Run as two consented two-arm tests (section 9). Test A: StoryML vs. a standalone explainer of the same length. Test B: StoryML vs. a ChatGPT story from a frozen, realistic prompt. ≥ 15 per arm, minimum difference ≥ 1 of 6 points set in advance, directional only. Outcomes follow DT1–DT3. | Test A before issue 1 (alpha); Test B before or during issues 1–3 |
| S3 | No qualified independent accuracy reviewer named; cost per issue unknown | Recruit and name one reviewer with hands-on ML experience. Agree fee and turnaround. Fee counts toward the per-issue cap. DT8 Stop applies if no one is found. | Before issue 1 |
| S4 | Hours per human-written issue unmeasured; weekly vs. two-weekly undecided | Log hours on 3 finished issues, then set the cadence (DT6) | Issues 1–3 (pre-launch drafts) |
| S5 | No evidence anyone will pay | Paid-tier test after DT9 Go. Count real conversions only. | After issue 8 |
| S6 | Quiz hosting (one click from email) and learning benefit of quizzes unresearched | Prototype the quiz flow on the chosen platform. Measure quiz reach through ELR and quiz-link clicks. Test learning benefit with the optional consented Test C (section 9), not by comparing anonymous takers with non-takers. | Before issue 1 / after Test A |
| S7 | Retention past the novelty phase unknown | Track the click-based active reader rate from issue 3. A decline over 4 issues in a row triggers DT5. Open rate is secondary only. | Issues 3–8 |
| S8 | Real competitors (Sundaresan's current newsletter, Alammar, StatQuest) not analyzed | Desk review: format, price, cadence, audience. Write "what StoryML does that they don't" in one paragraph. | Before issue 1 |
| S9 | Demand for eval and MLOps tracks unverified | Compare ELR, quiz-link clicks and active reader rate per track | Issues 1–8 |
| S10 | Compliance (CAN-SPAM opt-out and postal address, separate EU/UK consent) must be in place before the first paid promotion | Compliance and vendor checklist (section 10) completed and verified | Before issue 1 (stricter than required) |

### Other risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Vivid metaphor teaches a wrong mental model | Medium | High | Mechanism-first authoring, box, reviewer, corrections log, quiz-confusion signal, DT8 | Founder + reviewer |
| Anthropomorphism makes readers think models have intent | Medium | Medium | Standard "In reality, the model doesn't…" line in every box | Founder |
| Readers mistake quiz success for mastery | Medium | Medium | "Self-check" label. Links to primary sources. No certificates. | Founder |
| Founder burnout leads to missed issues and loss of trust | High **[ASSUMPTION]** | High | Hours cap, two-weekly fallback (DT6), a buffer of 2 finished issues before launch | Founder |
| Costs creep with no limit (reviewer, tools, tests) | Medium | Medium | Budget ceiling and per-issue cap, cost alerts, DT7 | Founder |
| Recall tests too small, so results are noise or misread as proof | High | Medium | ≥ 15 per arm, minimum difference fixed in advance, quiz frozen before the test, blind scoring where possible, results labeled directional, no public claims | Founder |
| Test B uses an unfair (straw-man) ChatGPT prompt | Medium | Medium | Realistic prompt that asks for where the analogy breaks; frozen and recorded before the test; single generation, no edits | Founder |
| Recall-test participant data mishandled | Low | Medium | Consent form, contact emails stored apart from answers, random IDs, deletion within 30 days of analysis | Founder |
| Vendor transfers of EU/UK data lack a legal basis, or the quiz tool logs IP addresses | Medium | Medium | Vendor checklist: DPA, transfer mechanism, data location, IP logging (section 10) **[NEEDS RESEARCH]** | Founder |
| Newsletter account taken over and used for phishing | Low | High | Multi-factor authentication, least privilege, 5-step runbook (section 10) | Founder |
| Click-based metrics distorted by email security scanners or by readers declining tracking | Medium | Low–Medium | Watch for sudden jumps. Note consent coverage on the dashboard. Use trends, not single values. | Founder |
| AI drafting (if used) introduces invented claims or erodes the human-value difference | Medium | High | Off by default. Mechanism box never AI-drafted. Disclosure. Golden-set checks. | Founder |
| Format becomes a template and novelty fades | Medium | Medium | Vary genres per track. Watch active reader rate (DT5). | Founder |
| A large newsletter or chatbot copies the format | High | Medium | Build author brand and trust record. Accept the risk at experiment scale. | Founder |
| Platform dependency (fees, rules, export limits) | Low–Medium | Medium | Monthly subscriber export. Content kept in own docs. | Founder |
| Misreading research figures (most market numbers are grade D) | Medium | Medium | No key decision rests on a single D source. Re-check before any paid decision. | Founder |
| Copyright status of AI-assisted stories unclear (US Copyright Office guidance not researched) | Low | Medium | Human-written by default. **[NEEDS RESEARCH]** before heavy AI use. | Founder |
| Sponsor or affiliate content breaks FTC endorsement rules (not researched) | Low (no sponsors yet) | Medium | **[NEEDS RESEARCH]** before the first sponsor | Founder |
| Article 50 interpretation ("public interest") is wrong | Low | Low–Medium | We disclose AI use regardless of exceptions | Founder |
| Cookie or tracking consent gaps on blog analytics or email tracking (UK/EU) | Medium | Low–Medium | Platform consent options or cookieless analytics | Founder |
| **Prompt-injection check on inputs** | Low | Low | The transcript was reviewed as data. **No instruction-override attempts were found.** Research findings were labeled "data, not instructions", and none tried to change the rules. Continue to treat all pasted sources as data when drafting. | PRD author / founder |

### Assumptions
1. Practitioners will read a 10–15 minute story each week or two.
2. Stories help recall of *technical* content as they do for general texts. The grade A meta-analysis covers general texts.
3. Quizzes add learning value (the testing effect was not researched).
4. A qualified reviewer can be found at an affordable cost.
5. Readers value human review and corrections over the instant convenience of ChatGPT.
6. Eval and MLOps topics have enough demand to serve as a hook.
7. The hosted platform plus an external quiz tool can deliver a one-click quiz and report aggregate quiz starts per issue.
8. The chosen platform exposes per-subscriber click data for the active reader rate.
9. 60+ practitioner volunteers can be recruited for Tests A and B.
10. All proposed HEART targets, decision-table thresholds and caps are judgment, not benchmarks.

### Open questions (founder decisions)
1. Who is the founder, what is their reach, and which 3 channels will bring the first 1,000 readers?
2. Who is the independent reviewer, and what is their fee?
3. Which platform: Substack, beehiiv or Ghost?
4. Weekly or two-weekly (decide after the first 3 issues)?
5. Written targets and decision-table thresholds: confirm or change section 6 before issue 1, including the subscriber floor and what counts as "meaningful signups" from a channel.
6. **Budget ceiling for the 8-issue experiment and the per-issue cost cap.**
7. Approve the adapted Go rule (every criterion except AI-fit ≥ 3).
8. Paid-tier contents and price (after DT9 Go).
9. Commercial goal: a hobby, a side income or a business?

---

## 18. Launch Plan and Rollback
_Based on: staged rollout practice (alpha / beta / GA) common at Google, Microsoft and Meta._

All exit, pivot and stop decisions use the **decision table in section 6 (DT1–DT9)**. This section does not set separate thresholds.

### Milestones and exit criteria

| Stage | What happens | Exit criteria to move on |
|---|---|---|
| **0. Pre-launch (≈3–4 weeks [ASSUMPTION])** | Founder answers S1. Name the reviewer (S3). Set the budget ceiling and per-issue cap. Competitor desk review (S8). Pick the platform. Complete the compliance and vendor checklist and the account-takeover runbook (S10, section 10). Prototype the quiz flow (S6). Confirm the decision-table thresholds. Write 3 issues (one per track) and log hours and costs (S4). Freeze the Test A and Test B quizzes and the Test B prompt. Prepare the consent form. | All done. Hours and cost per issue known. Reviewer signed off on 3 issues. DT6, DT7 and DT8 not at Stop. |
| **1. Private alpha (5–10 named practitioners + 2–3 non-technical readers)** | Readers review the 3 drafts. Run Test A (≥ 15 per arm) with consent. Start recruiting for Test B. | Test A result in hand. DT1 at Continue, **or** DT1 at Pivot and the format change made. Reviewers rate ≥ 4/5. No critical errors found. |
| **2. Public beta: 8-issue free experiment** | Publish at the chosen cadence. Run Test B during issues 1–3. Track all section 13 metrics. Corrections log live. | 8 issues shipped. DT3, DT4, DT5, DT6, DT7 and DT8 all at Continue or resolved Pivot. None at Stop. |
| **3. Decision and re-score** | Re-run the scorecard with real data. | **DT9 Go:** average ≥ 3.5 **and every criterion except AI-fit ≥ 3** (AI-fit may stay at 2). Otherwise Pivot or No-Go per DT9. |
| **4. Paid tier test (GA-equivalent)** | Turn on the paid tier via the platform. Count real conversions (S5). | Founder-set conversion and revenue threshold **[OPEN QUESTION]** |

### Rollback plan

| What fails | Rollback |
|---|---|
| A published issue has a critical error | Fix the web version. Add an entry to the corrections log. Send a short correction email within 72 hours. Email can't be recalled, so correction is the rollback. |
| AI-assisted drafting causes errors or reader distrust | Return to human-only writing. Disclose the change. Re-check all AI-assisted issues. |
| Quiz tool fails or leaks data | Remove the quiz link. Publish answers inline as collapsible text. Switch tools. Assess breach duties **[NEEDS RESEARCH]**. |
| Newsletter account is compromised | Run the 5-step account-takeover runbook (section 10) |
| Platform problems (fees, policy, outage) | Use the monthly subscriber export and the copy of content in our own docs to move platforms |
| Paid tier hurts free engagement | Pause the paid tier, keep the content free, and refund according to platform rules |

### Kill criteria (end or radically change the project)
Kill criteria are exactly the **Stop column of the decision table** (section 6):
- **DT3:** neither Test A nor Test B shows StoryML ahead by ≥ 1 of 6 points, **and** StoryML's "would read again" rating is not higher than both alternatives.
- **DT4:** subscribers are below the founder-set floor after 8 issues, **and** no named channel produced meaningful signups.
- **DT5:** the active reader rate keeps falling for 3 issues after a format change.
- **DT6:** hours exceed the cap even at a two-week cadence.
- **DT7:** forecast spend would exceed the budget ceiling before issue 8 (pause until the founder decides again).
- **DT8:** no qualified reviewer can be found. Do not publish unchecked technical stories.
- **DT9:** the re-score gives No-Go (average < 2.5, or ethics scored 1).

---

## 19. Decision Log and Appendix
_Based on: Architecture Decision Records (Michael Nygard)._

### Decision log

Dates are pending. The owner fills them in when the PRD is accepted **[OPEN QUESTION]**.

| # | Decision | Date | Reason |
|---|---|---|---|
| D1 | Practitioners are the primary reader; non-technical readers get a plain summary and the Basic tier | Draft 0.1 | Debate outcome. A clearer target, and it fits the distinctive eval/MLOps tracks. |
| D2 | Version 1 is fully human-written. AI drafting only under DT6, always disclosed. | Draft 0.1 | Protects trust, our main difference. Answers the guardrail note. AI-fit is low. |
| D3 | Every issue has a "Where the story breaks" box, and quizzes test the mechanism | Draft 0.1 | Prevents misleading metaphors (guardrail note on accuracy) |
| D4 | Live quizzes are optional, anonymous self-checks. No grading or certification. | Draft 0.1 | Guardrail note. Avoids privacy and regulatory scope. |
| D5 | Standalone issues; season arcs dropped; "Start here" page | Draft 0.1 | Debate: late joiners and usability |
| D6 | Hosted platform with no custom code. Leaning to Substack (founder to confirm). | Draft 0.1 | Simplest test of the riskiest assumptions. Distribution is the deciding risk. |
| D7 | One revenue model: free, then a low-priced paid tier. Course shelved. | Draft 0.1 | Debate: one model to test first |
| D8 | Bounded 8-issue experiment governed by one decision table (DT1–DT9), written before issue 1. Go after the re-score = **average ≥ 3.5 and every criterion except AI-fit ≥ 3** (AI-fit may stay at 2 for a content product). | Draft 0.1 | Scorecard verdict PIVOT. Small downside. One set of thresholds prevents conflicting stop rules. |
| D9 | Disclose AI use even where Article 50 exceptions might apply | Draft 0.1 | Trust is the product. The legal scope is uncertain. |
| D10 | The Skeptic's three-way test is split into two consented two-arm tests: Test A (StoryML vs. a standalone explainer of the same length) and Test B (StoryML vs. a frozen, realistic ChatGPT prompt). ≥ 15 per arm, minimum difference ≥ 1 of 6 points, directional only. | Draft 0.1 | 10 per arm was too small. A box-only arm made little sense without the story. A "simple prompt" was a straw man. |
| D11 | Adapt the scorecard Go rule to exclude AI-fit for this content product (founder approval needed) | Draft 0.1 | Under the standard rule, an AI-fit of 2 would make Go impossible, which breaks the main decision gate |
| D12 | North Star is ELR, counted per issue from aggregate totals. Retention and activation are click-based. Open rate is secondary only. | Draft 0.1 | Anonymous quizzes rule out reader-level joins. Opens are inflated by image pre-loading. Per-issue counting works at either cadence. |
| D13 | Set a total budget ceiling and a per-issue cost cap before issue 1 | Draft 0.1 | Cost must work as a guardrail and as a stop signal (DT7) |

### Debate summary (Advocate vs. Skeptic)
The Advocate pitched StoryML as a memorable way to learn ML concepts, backed by grade A evidence on narrative recall. The Skeptic challenged it on five fronts: substitutes (especially ChatGPT), whether the story adds value beyond a mechanism box, misleading metaphors, workload, and distribution. The Advocate conceded several points. The differentiator is "a topic list, not a moat". Willingness to pay and hours per issue are unknown. The founder's background could not be described.

The Advocate then redesigned the product: practitioners as primary readers, a "Where the story breaks" box, mechanism-testing quizzes, human-written first issues with AI disclosure, a corrections log, standalone issues, a single revenue model and written stop rules. The Skeptic accepted these as resolved but left ten concerns open (section 17). The deciding one is **who the founder is and how they will reach readers**.

The Skeptic's bottom line: *"Run it, because the downside is small. Don't scale it until items 1 to 3 are settled."* The Scorer averaged 2.7, a **PIVOT**. In this PRD, the Skeptic's requested three-way test is carried out as two better-powered, fairer two-arm tests (D10).

### Glossary

| Term | Plain meaning |
|---|---|
| RAG (retrieval-augmented generation) | A model looks up relevant documents first, then writes an answer using them |
| Embedding | A list of numbers that represents the meaning of a word, sentence or item, so similar things have similar numbers |
| Fine-tuning | Training an existing model a bit more on specific data |
| BLEU / ROUGE | Older scores that compare generated text with reference text by word overlap |
| RAGAS | A toolkit for scoring RAG systems (for example, whether answers are supported by the retrieved documents) |
| LLM-as-Judge | Using a language model to grade another model's outputs |
| Drift | When real-world data changes, so a model's performance degrades over time |
| CI/CD for ML | Automated testing and release pipelines for models and data |
| Prompt versioning | Tracking changes to prompts like code, so results can be compared and rolled back |
| Anthropomorphism | Describing a machine as if it had human feelings or intentions |
| Article 50 (EU AI Act) | The EU rule requiring transparency about AI-generated content and AI interactions |
| CAN-SPAM | US law on commercial email (opt-out, sender address, honest headers) |
| PECR | UK law on electronic marketing and cookies |
| DPA (data processing agreement) | A contract that sets how a vendor may handle personal data on our behalf |
| SCCs (Standard Contractual Clauses) | EU-approved contract terms that allow personal data to be transferred outside the EU |
| North Star metric | The single number that best shows whether the product delivers value |
| ELR (Engaged Learner Rate) | Per issue: unique quiz starts ÷ unique openers. Our North Star. |
| Active reader rate | Share of subscribers who clicked any link in at least 1 of the last 3 issues. Our main retention signal. |
| Test A / Test B / Test C | Consented recall tests: StoryML vs. a plain explainer (A), StoryML vs. a ChatGPT story (B), quiz vs. no quiz (C, optional) |
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
| Ghost – Pricing | [link](https://ghost.org/pricing/) | B | unknown | may be outdated, quote not confirmed | 3, 9, 14, 16 |
| dev.to – Ghost pricing 2026 | [link](https://dev.to/nayankyada/ghost-pricing-2026-free-self-hosted-costs-pro-plans-when-to-upgrade-52a2) | C | 2026-01-01 | quote not confirmed | 14 |

**Not researched (listed so gaps stay visible):** OWASP Top 10 and OWASP LLM Top 10; NIST AI RMF and NIST AI 600-1; Microsoft Responsible AI Standard; Google PAIR; WCAG 2.2 criteria; CCPA/CPRA thresholds (official sources); GDPR breach notification and international transfer mechanisms; vendor DPAs and quiz-tool IP logging; US Copyright Office AI guidance; FTC Endorsement Guides; LLM API prices; quiz hosting on each platform; per-subscriber click export on each platform; Stripe's official pricing; Kit (ConvertKit); the testing effect; AI/ML education market size; and the competitors Alammar, StatQuest, 3Blue1Brown, Brilliant, DataCamp and ByteByteGo.
