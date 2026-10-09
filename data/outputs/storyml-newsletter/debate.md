## Pitch (Advocate)

# StoryML: The Pitch

**The problem**
Most people now learn AI on their own. In Microsoft and LinkedIn's 2024 Work Trend Index, 75% of knowledge workers used AI at work, but only 39% of AI users had received training from their company (grade B, news.microsoft.com/source/2024/05/08/...). The jargon trips up newcomers. One writer says people "feel confused" by terms like Query, Key and Value (grade C, dev.to/kushagra_gupta_13239507ec/...). That is one person's view, not survey data.

**Who it's for**
- Practitioners who want to brush up on concepts.
- Non-technical readers who want to follow the plot.

**The solution**
StoryML is a weekly newsletter and blog. Each issue turns one concept into a story, where models become characters and concepts become scenes. It has three tracks:
- **Core concepts** as heists and origin stories.
- **Evaluation** as courtroom dramas.
- **MLOps** as thrillers.

Every story ends with an optional quiz at three levels: recall, apply, and reason about tradeoffs.

**Why it's better**
The biggest AI newsletters are quick news digests. TLDR AI's format is "headline, two-sentence summary, link" (grade D, datacamp.com/blog/best-ai-newsletters). They help you sort news, but they don't teach one idea in depth.

The story format has strong backing. A meta-analysis of 33,000+ participants found stories "more easily understood and better recalled than essays" (grade A, ncbi.nlm.nih.gov/pmc/articles/PMC8219577/).

There are honest limits:
- The idea isn't new. Sairam Sundaresan has already taught ML through stories (grade C, medium.com/mlearning-ai/...). StoryML's edge would be the evaluation and MLOps tracks plus the tiered quizzes.
- There is no data yet on demand for those tracks.
- Nobody researched whether quizzes actually improve learning.

**The wow moment**
This example is for illustration only and hasn't been tested. A reader watches LLM-as-Judge cross-examined in a courtroom drama. Then they answer an expert-level question about a real production tradeoff and realize they actually get it.

**How it makes money**
The founder hasn't said yet, but the evidence points to a path:
- Substack passed 5M paid subscriptions (grade D, tubefilter.com/2025/03/12/...).
- Its recommendations network drives 25% of new paid subscriptions (grade C, x.com/Substack/status/1760696631156953443).
- In-depth AI newsletters can grow. Ahead of AI reached 200,000 subscribers (grade B, sebastianraschka.com/blog/2026/...), with a paid tier reportedly at $6/month (grade D, pasqualepillitteri.it/...).

Launch costs can stay low. beehiiv is reportedly free up to 2,500 subscribers (grade D, emailtooltester.com/...), and Substack is free to publish but takes 10% of paid revenue plus Stripe fees (grade D, schoolmaker.com/blog/substack-pricing).

**What I concede**
- There is no evidence that readers will pay for this format. The fix is to launch free, track quiz use, and test a paid tier before building anything custom.
- Drama can distort the facts. Every story needs a human technical accuracy check.
- If AI drafts any content, readers should be told.

## Round 1: Skeptic

# Skeptic: Round 1

The pitch is honest about its gaps, which helps. But several core claims rest on evidence about *other* things. Here are my five biggest concerns, strongest first.

**1. Why wouldn't readers just ask ChatGPT to tell them a story?**
This is the main threat. Anyone can type "explain LLM-as-Judge as a courtroom drama, then quiz me at three levels" and get it free, instantly, on the exact concept they're stuck on today. A weekly newsletter makes them wait for a topic someone else picked. The format can also be copied by any big AI newsletter, or by Sundaresan, who already does it. "Evaluation and MLOps tracks plus quizzes" is a topic list, not a moat.
*To convince me:* Show what a human-written StoryML issue does that a good prompt can't. Run a side-by-side test: 10 readers, one StoryML story versus one ChatGPT story on the same concept. Measure which they prefer and which helps them score better on the quiz a week later. Also name what you'd own that's hard to copy: an author's reputation, a community, or a curriculum.

**2. The two audiences pull in opposite directions.**
"Practitioners brushing up" and "non-technical readers following the plot" want different things. Your wow moment is an expert-level question about production tradeoffs. That's for practitioners, and it would lose a non-technical reader. Practitioners, meanwhile, may find heists and thrillers slow or patronizing when a diagram would take 30 seconds. Writing for both usually satisfies neither.
*To convince me:* Pick one primary reader, describe them concretely (job, what they're stuck on, how often), and get 5 to 10 of them to read a draft and say they'd subscribe.

**3. The evidence proves the problem exists, not that this solves it.**
- The Microsoft stat shows people lack company training. It says nothing about wanting stories or a newsletter. They may prefer courses, YouTube, or just asking an AI.
- The jargon-confusion claim is one blog post, as you admit.
- The meta-analysis compares stories with essays, mostly in general reading comprehension. It doesn't show stories teach *technical* concepts like attention or eval design better than visual explainers. Jay Alammar and StatQuest are free and proven alternatives.
- Metaphors also carry a specific risk in technical subjects. A vivid analogy for Query/Key/Value can stick *and* be wrong, and readers remember the wrong version. "Better recalled" can work against you.

*To convince me:* Find any study, or run your own small test, showing narrative beats a good plain explanation for technical concepts.

**4. The workload is heavy and the money is thin.**
Every week you'd need to research the concept, write a quality story, write three levels of quiz, and get a human accuracy check. That's many hours per issue, indefinitely, from one founder.
On revenue, Ahead of AI is survivorship bias. Raschka was already a well-known researcher and author. At $6/month and a typical 3 to 5% paid conversion, 200,000 free subscribers is roughly $430K to $720K a year. That would be great, but most newsletters never reach 2,000 subscribers. Who reviews accuracy, and who pays them?
*To convince me:* Show the hours per issue after writing 3 real ones. Explain the founder's credibility or distribution: why will the first 1,000 readers find this?

**5. Will people come back after week four?**
Novelty wears off. The fifth heist feels like a template. Quizzes inside emails are also clunky. Most readers skim email and won't click through to a quiz, so "track quiz use" may give you a misleadingly low number. And a weekly one-concept format has no clear path through the material. Readers who join in week 20 land in the middle.
*To convince me:* Show the plan for keeping the format fresh. Explain how quizzes work technically (embedded, linked, or on a site). Say what open and quiz rates would count as success after 8 issues.

---

**Claims with no evidence yet:** reader demand for evaluation and MLOps topics, that quizzes improve learning (you concede both), that the wow moment works, that any reader will pay, and that stories beat other formats for *technical* content specifically.

**What I'd need to see by round 2:** one named target reader, one finished sample issue, and a cheap test against "just ask ChatGPT."

## Round 1: Advocate

# Advocate: Round 1 Response

The Skeptic's challenges are fair, and several of them I can't answer with evidence. Below I take each one in turn, say what the evidence supports, concede what it doesn't, and suggest how the product should change.

---

**1. "Why wouldn't readers just ask ChatGPT?"**

**What I can defend:**
- **Accuracy checking.** A chatbot story on demand has no one checking whether the metaphor is right. StoryML's guardrails require every story to "stay technically accurate," checked by a human. That's a real difference. But I have **no evidence** that readers value a checked story over an instant one. The research on AI accuracy risks (NIST's confabulation guidance) was never gathered.
- **Distribution.** Substack says its Recommendations network and app drive 50% of all new subscriptions (grade C, x.com/Substack/status/1760696631156953443). A chatbot answers questions people already know to ask. A newsletter can show up in an inbox with a topic they didn't know to ask about. Whether readers care about that is untested.

**What I concede:**
- "Evaluation and MLOps tracks plus quizzes" is a topic list, not a moat.
- The research tells me nothing about the founder's reputation, community, or audience.

**How to change the product:**
- Run the Skeptic's side-by-side test before launch: StoryML story versus ChatGPT story on the same concept, with a quiz a week later.
- Make the **curriculum** the thing StoryML owns. That means a planned sequence where stories build on each other and characters recur. A one-off prompt doesn't give you that.
- Consider being open about using AI to draft, as long as a human checks the facts. That makes the human review the selling point. If AI drafts content, the guardrails require telling readers. Article 50 also applies from 2 August 2026 (grade A, digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content). Text under real human editorial control may fall outside the labeling duty (grade A, digital-strategy.ec.europa.eu/en/faqs/...). Even so, disclosing is the honest default.

---

**2. "The two audiences pull in opposite directions."**

**I concede this.** The pitch tries to serve both audiences equally, and the wow moment I picked is clearly for practitioners.

**What the evidence suggests:**
- The two tracks that set StoryML apart, evaluation and MLOps, are practitioner topics. So are the intermediate and expert quiz tiers.
- An in-depth practitioner audience exists. Ahead of AI reached 200,000 subscribers (grade B, sebastianraschka.com/blog/2026/...). The usual caveat applies: Raschka is a known researcher, so his numbers are not proof for a new writer.
- The Microsoft stat covers knowledge workers in general (grade B, news.microsoft.com/source/2024/05/08/...). It supports a non-technical audience too, but it says nothing about whether they want stories.

**How to change the product:**
- Make **practitioners the primary reader.**
- Serve non-technical readers through the Basic quiz tier and a plain one-paragraph summary at the top of each issue. They are not the target.
- The founder still needs to name the specific person: their job, what they're stuck on, and how often. Then get 5 to 10 of them to read a draft. I can't supply that from the research.

---

**3. "The evidence proves the problem exists, not that this solves it."**

**Mostly conceded.**
- The meta-analysis (grade A, ncbi.nlm.nih.gov/pmc/articles/PMC8219577/) compares stories with essays. It is flagged as possibly outdated. It does **not** test technical concepts, and it does not compare stories against visual explainers like Jay Alammar's or StatQuest. Those substitutes were listed as an open question and never checked.
- The jargon claim comes from one blog post (grade C).
- No research was collected on whether quizzes improve learning.

**The wrong-metaphor risk is the Skeptic's sharpest point.** "Better recalled" cuts both ways. If the metaphor is wrong, readers will remember the wrong version.

**How to change the product:**
- End every story with a **"Where the story breaks"** box. It maps each character and scene to the real mechanism, with a plain diagram or equation, and says where the metaphor stops being true.
- Write quizzes, especially Intermediate and Expert, to test the **real mechanism**, not the plot.
- Treat "stories beat plain explanations for technical topics" as a test to run, not a claim to make. The side-by-side test from point 1 can include a plain-explainer version too.

---

**4. "The workload is heavy and the money is thin."**

**On workload: conceded.** I have no data on hours per issue. The Skeptic is right to ask for real numbers after writing 3 issues.

**On revenue: half agree.**
- The arithmetic checks out at the conversion rates the Skeptic assumed. But the "3 to 5% paid conversion" and "most newsletters never reach 2,000 subscribers" figures aren't in our research, so I can't confirm or rule them out.
- On Substack, the writer would also give up 10% plus Stripe fees and keep roughly 87% (grade D, amysuto.com/...).
- I agree Ahead of AI is a best case, not a forecast.

**One more revenue model the evidence shows:** The Rundown AI keeps its newsletter free and earns money from a separate paid training product, priced at $84/month on an annual plan (grade D, readless.app/...). For StoryML, the tiered quizzes and a structured curriculum could become a paid course later, rather than relying on a $6/month subscription.

**How to keep the workload manageable:**
- Write 3 issues before launch and measure the hours.
- Consider publishing every two weeks if weekly isn't sustainable.
- Reuse a quiz template.
- If AI drafts content, keep the human accuracy check and the disclosure (see point 1).

**Costs stay low while testing:**
- beehiiv is reportedly free up to 2,500 subscribers (grade D, emailtooltester.com/...).
- Ghost says it charges no payment fees (grade B, ghost.org/pricing/).

**On credibility and the first 1,000 readers:** I have nothing. The transcript doesn't describe the founder's background or audience. This is a real gap the founder must fill.

---

**5. "Will people come back after week four?"**

**I have no evidence on retention.**

**How quizzes would work: not yet known.** Whether Substack, beehiiv, or Ghost can host a three-tier quiz natively was never researched. The realistic plan is a quiz on the blog page or an embedded form, linked from the email. The Skeptic is right that this means low click-through, so a low quiz-use number may undercount real interest.

**How to change the product:**
- **Freshness.** The three tracks already rotate genres: heists and origin stories, courtroom dramas and audits, thrillers and disaster recovery. Add **recurring characters and season-long arcs**, so issues build on each other instead of repeating a template.
- **Readers who join in week 20.** Add a "Start here" path in the blog archive, ordered as a curriculum. This also strengthens the moat from point 1.
- **Success targets.** The founder should set open-rate and quiz-rate targets before issue 1. I have no benchmark data for what counts as good, so I won't invent one.

---

**Summary for round 2**

I accept the Skeptic's three asks:
1. One named target reader. I propose practitioners.
2. One finished sample issue, including the "Where the story breaks" box.
3. A cheap test against "just ask ChatGPT."

The strongest honest case today is this: there is a real gap for in-depth, accuracy-checked AI explainers, and launching costs very little. Every claim that StoryML's specific format fills that gap still needs to be tested.

## Round 2: Skeptic

# Skeptic: Round 2

The Advocate conceded honestly and made real fixes. Choosing practitioners as the primary reader, adding a "Where the story breaks" box, and building a "Start here" path all help. But the fixes create new tensions, and the biggest gap from round 1 is still open. These are my final five, strongest first.

**1. The practitioner pivot makes the ChatGPT problem worse, and the new box may make the story unnecessary.**
Practitioners are the readers most likely to already use ChatGPT and most likely to find a heist slow. The "Where the story breaks" box maps every character to the real mechanism with a diagram or equation. That box is a good plain explainer. If a busy practitioner skips straight to it, the story is just a cost that adds length and writing hours. Then you have built a plain explainer newsletter, a crowded space with free, proven players like Jay Alammar and StatQuest.
*To convince me:* In the side-by-side test, include a "box only" version alongside the full story and the ChatGPT story. If "box only" scores as well a week later, the story isn't earning its place. Also track how many readers scroll past the story to the box.

**2. AI drafting and human value pull against each other.**
The Advocate's answer to ChatGPT is "a human checked it." The answer to workload is "let AI draft it." Together they leave you selling a ChatGPT story with a review stamp, which is a thin difference. The review itself is also undefined. If the founder checks their own story, that isn't an independent check, and metaphor errors are exactly the kind an author misses.
*To convince me:*
- Decide whether StoryML is human-written or AI-drafted and human-checked.
- Name who does the accuracy check, how qualified they are, and what it costs per issue.
- Publish a correction policy, so readers can see that mistakes get fixed.

**3. The founder is still a blank, and "curriculum" is not a moat.**
This is now the decisive question. A planned sequence with recurring characters is copyable too. Anyone can publish a syllabus, and ChatGPT can follow one. What actually protects a newsletter is a trusted author with an audience. That is why Raschka worked, and why Sundaresan, who already does this, is the real competitor. Two rounds in, we know nothing about who writes this or where the first 1,000 readers come from. Season-long arcs also make each issue harder to write and harder for a new reader to join mid-season. That partly undoes the "Start here" fix.
*To convince me:* State the founder's credentials and current reach, such as followers, an existing list, or a community. Then name three specific channels for the first 1,000 subscribers.

**4. The revenue story keeps moving, and one number changed.**
- **Course model.** The new idea, a paid course like The Rundown's $84/month product, needs a large audience first and proof that people actually learn. That proof doesn't exist yet, since nobody has researched whether the quizzes improve learning. It is a second business, not a fallback.
- **Inconsistent figure.** The pitch said Substack Recommendations drive 25% of new *paid* subscriptions. The round 1 response says 50% of *all* new subscriptions, citing the same source. Those are different claims. Check the source before relying on either.
- **Unproven premise.** The Advocate's summary opens with "there is a real gap for in-depth, accuracy-checked AI explainers." That gap is asserted, not shown. Free in-depth explainers already exist.

*To convince me:* Pick one money model to test first, and fix the citation.

**5. There are still no success or stop criteria.**
"I won't invent a benchmark" is honest, but without targets set in advance, any result can be read as "promising." Here are the kind of targets I'd want. These are my judgment, not data:
- After 8 issues, at least 500 subscribers.
- An open rate that holds steady rather than falling issue by issue.
- At least 10% of openers starting a quiz.
- At least 5 readers saying, unprompted, that they'd pay.

If the numbers fall short, change the format or stop.
*To convince me:* Write down the targets and the stop rule before issue 1.

---

**Still without evidence:**
- Demand for the evaluation and MLOps tracks.
- That quizzes improve learning.
- That stories beat plain explainers for technical topics.
- That readers will pay.
- Retention past the first few issues.
- That an accuracy check exists and is independent.
- That recurring characters keep readers engaged.

**My verdict:** This is a cheap experiment worth running, but not yet a business. Launching free costs little, so the downside is mostly the founder's time. Go ahead if, before launch, you:
1. Name the founder's reach.
2. Run the three-way test: full story, box only, and ChatGPT.
3. Write down your stop rules.

If the "box only" version wins, or nobody can say where the first 1,000 readers come from, don't scale the story format.

## Round 2: Advocate

# Advocate: Round 2 Response

The Skeptic's verdict is fair: this is a cheap experiment worth running, not yet a business. I agree with it. Below I answer each point, defend what the evidence supports, and concede the rest.

---

**1. "The practitioner pivot makes the ChatGPT problem worse, and the box may make the story unnecessary."**

**What I can defend:**
- The one strong piece of evidence for the format is the meta-analysis. Stories were "more easily understood and better recalled than essays" (grade A, ncbi.nlm.nih.gov/pmc/articles/PMC8219577/). The box is closer to a short essay than to a story, so there is some reason to expect the story to add value.

**What I concede:**
- That study did not test technical topics. It also did not compare stories with a short diagram-plus-explanation, which is what the box is. Jay Alammar and StatQuest were never researched, so I can't say how StoryML compares.
- If practitioners skip to the box, the story is extra cost.

**How to change the product:**
- Add the "box only" arm to the test, as the Skeptic asks. The test then compares three versions: full story, box only, and ChatGPT story. Run the quiz a week later.
- Track how many readers scroll past the story. This only works on the blog, so it is one more reason to make the blog the main reading place.
- Set the rule now: if "box only" scores as well as the full story, StoryML becomes a short explainer newsletter with optional stories, or it stops.

---

**2. "AI drafting and human value pull against each other."**

**I concede this.** "A ChatGPT story with a review stamp" is a thin difference, and a self-check is not independent.

**My recommendation:**
- **Start human-written.** Write the first 3 issues by hand and measure the hours. That gives the workload numbers the Skeptic asked for in round 1. It also tests whether a human story is better than ChatGPT's before anyone relies on that claim.
- Use AI drafting only if the hours prove unsustainable. If AI drafts anything, tell readers, as the guardrails require. Article 50 applies from 2 August 2026 (grade A, digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content).
- Human editorial control may remove the legal labeling duty (grade A, digital-strategy.ec.europa.eu/en/faqs/...). Disclosure is still the honest choice. It is also unclear whether ML education counts as "matters of public interest," which is an open question.

**What I can't supply:**
- Who the reviewer is, how qualified they are, or what they cost. The research has no data on review workflows or costs; quality and safety was an open question. The founder must name a reviewer who is not the author.

**How to change the product:**
- Publish a correction policy and a visible corrections log. This fits the guardrail that dramatized explanations must not mislead readers.

---

**3. "The founder is still a blank, and 'curriculum' is not a moat."**

**I concede both parts.** After two rounds I still know nothing about the founder's background or reach. A trusted author is the most believable moat, and the research can't provide one. Sundaresan is the real competitor (grade C, medium.com/mlearning-ai/...). His current newsletter was listed as an open question and never checked.

**On channels:**
- I can name only one with evidence. Substack says its Recommendations network plus app drive half of all new subscriptions (grade C, x.com/Substack/status/1760696631156953443).
- LinkedIn and Reddit were never researched, so I can't vouch for them.
- The founder has to name the other two channels and state their current reach.

**On season-long arcs:** I accept that they work against the "Start here" path.
- Drop season-long arcs.
- Keep each issue self-contained.
- Let recurring characters be optional flavor rather than required context.

---

**4. "The revenue story keeps moving, and one number changed."**

**On the citation:** Both numbers are in the same quote, so neither was wrong. The quote says the network "drives 50% of all new subscriptions and 25% of new paid subscriptions." I was sloppy in two ways:
- I didn't say which figure I meant each time.
- The pitch credited the Recommendations network alone. The source credits Recommendations **plus the app**.

Either way it's Substack's own claim, graded C and possibly outdated.

**One money model to test first:** keep the newsletter free, then test a low-priced paid tier on the hosting platform. The only price reference is Ahead of AI at a reported $6/month (grade D, pasqualepillitteri.it/...).
- I'm dropping the course model for now. The Skeptic is right that it's a second business, and it needs proof that people learn from the quizzes, which we don't have.
- Once the newsletter promotes a paid tier, CAN-SPAM likely applies. Every email then needs a working opt-out honored within 10 business days and a valid postal address (grade A, ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business).
- EU and UK signups need separate consent, not bundled into the terms (grade A, edpb.europa.eu/...).

**On "a real gap":** I overstated it. The evidence shows only one thing: the biggest daily digests sort news rather than teach concepts in depth (grade D, datacamp.com/blog/best-ai-newsletters). Free in-depth explainers exist and were not researched. The honest claim is "a possible gap, untested."

---

**5. "There are still no success or stop criteria."**

**I accept.** I still have no benchmark data, so these targets are the Skeptic's judgment and should be labeled that way.

Here is the plan, written down before issue 1:
- **Go targets after 8 issues:**
  - At least 500 subscribers.
  - An open rate that stays steady rather than falling.
  - At least 10% of openers starting a quiz.
  - At least 5 readers saying, unprompted, that they'd pay.
- **Stop or change rule:**
  - If "box only" matches the full story in the pre-launch test, change the format.
  - If fewer than half the targets are met after 8 issues, stop or rethink.
- **One caveat on quiz rate:** Quiz hosting on these platforms was never researched. The founder should first confirm the quiz is one click from the email; otherwise the 10% target is unfair to the format.

---

**Summary**

The honest case now is narrow but real. StoryML is cheap to try. Its central idea has strong general support from the storytelling meta-analysis. And the Skeptic and I now agree on a test that will show whether the story earns its place.

Before launch, the founder must:
1. State their reach.
2. Name an independent reviewer.
3. Run the three-way test.
4. Write down the stop rules.

If they can't do those things, I wouldn't argue for scaling it.

## Closing statement (Skeptic)

# Skeptic: Closing Statement

The Advocate answered honestly, dropped weak claims, and turned vague promises into tests. StoryML is now a well-designed **experiment**. It is not yet a proven product. Nearly every remaining question can be settled cheaply, before launch or within 8 issues. One question no test can settle: **who the founder is.** If the founder can't name their reach, the rest doesn't matter.

## Resolved

1. **Target reader.** Practitioners are the primary reader. Non-technical readers get a plain summary and the Basic quiz tier.
2. **Wrong-metaphor risk.** The "Where the story breaks" box maps each character to the real mechanism. Quizzes will test the mechanism, not the plot.
3. **AI drafting versus human value.** The first 3 issues will be human-written. AI drafting comes in only if the hours prove unsustainable, and readers will be told if it does.
4. **Corrections.** There will be a public correction policy and a corrections log.
5. **Season-long arcs.** They are dropped. Each issue stands alone, recurring characters are optional, and a "Start here" path serves late joiners.
6. **Citation mix-up.** Both figures come from one Substack quote (50% of all new subscriptions, 25% of paid), and both are credited to Recommendations plus the app. This is still Substack's own claim.
7. **Shifting revenue story.** There is one model to test first: a free newsletter, then a low-priced paid tier. The course idea is shelved.
8. **Overstated "real gap."** This is now correctly called "a possible gap, untested."
9. **Success and stop rules.** Targets and a stop rule are written down before issue 1. They are labeled as judgment, not benchmarks.

## Unresolved

| Open question | What would settle it |
|---|---|
| **1. Founder credibility and distribution.** This is the deciding issue. | State the founder's background and current reach. Name three specific channels for the first 1,000 readers. |
| **2. Does the story beat ChatGPT, and does it beat the box alone?** | Run the three-way test: full story, box only, ChatGPT story. Test recall a week later. If "box only" ties, change the format. |
| **3. Independent accuracy review.** | Name a qualified reviewer who is not the author. State their cost per issue. |
| **4. Workload.** | Record the hours for 3 finished human-written issues. Decide weekly or every two weeks from that number. |
| **5. Will anyone pay?** | Test the paid tier after the go targets are met. Count real conversions, not stated interest. |
| **6. Do the quizzes help learning, and can readers reach them easily?** | Confirm the quiz is one click from the email. Compare quiz takers with non-takers on later recall. |
| **7. Retention past the novelty.** | Track the open-rate trend across 8 issues. A falling line means the format is wearing thin. |
| **8. Real competitors.** | Check Sundaresan's current newsletter, Jay Alammar, and StatQuest. Say plainly what StoryML does that they don't. |
| **9. Demand for evaluation and MLOps topics.** | Compare open and quiz rates on those tracks with the core-concepts track. |
| **10. Compliance before charging.** | Set up a CAN-SPAM opt-out, a postal address, and separate EU/UK consent before the first paid promotion. |

**Bottom line:** Run it, because the downside is small. Don't scale it until items 1 to 3 are settled.
