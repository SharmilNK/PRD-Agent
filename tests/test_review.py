"""Phase 5 tests: quality checks, Reviewer (link spot-check + review), revision, and the eval harness."""

import json
import tempfile
import unittest
from pathlib import Path

from apps.orchestrator import run as orchestrator
from evals import run_evals
from evals.check_structure import template_sections
from evals.quality_checks import check_links, check_scores, readability, run_checks
from packages.agents.prd_writer import agent as prd_writer
from packages.agents.reviewer import agent as reviewer
from packages.agents.scorer.agent import load_scorecard
from tests.fakes import FakeClient, link_message, sample_review

ROOT = Path(__file__).resolve().parents[1]
STORYML = ROOT / "data" / "transcripts" / "storyml-newsletter.md"
CARD = load_scorecard()
NAMES = {c["id"]: c["name"] for c in CARD["criteria"]}


def good_prd(score=4, link="https://statquest.org/about") -> str:
    """A PRD that passes every free check against the default fake scorecard (all 4s)."""
    rows = "\n".join(f"| {NAMES[c['id']]} | {score}/5 | {c['frameworks'][0]} | evidence | reason |" for c in CARD["criteria"])
    parts = ["# PRD: StoryML"]
    for num, title in template_sections():
        body = f"GUCCI first.\n\n| Criterion | Score | Framework | Evidence | Rationale |\n|---|---|---|---|---|\n{rows}" \
            if num == "16" else f"Short clear text. See [source]({link})."
        parts.append(f"## {num}. {title}\n{body}")
    return "\n\n".join(parts) + "\n"


def claim(url, text="Fact.", quote="the exact quote words here", grade="B"):
    return {"claim": text, "url": url, "quote": quote, "checks": {"grade": grade}}


class QualityCheckTests(unittest.TestCase):
    def test_links(self):
        prd = "See [a](https://www.nist.gov/ai/) and https://made-up.com/x."
        result = check_links(prd, {"https://nist.gov/ai"})
        self.assertEqual(result["unknown_links"], ["https://made-up.com/x"])
        self.assertTrue(check_links("No links at all.", set())["passed"])

    def test_scores_match_and_mismatch(self):
        card = {"scores": {c["id"]: {"score": 4} for c in CARD["criteria"]}}
        self.assertTrue(check_scores(good_prd(4), card, NAMES)["passed"])
        result = check_scores(good_prd(3), card, NAMES)
        self.assertEqual(len(result["mismatches"]), 10)
        self.assertIn("Customer need: scorecard 4, PRD 3", result["mismatches"])
        self.assertFalse(check_scores(good_prd(4), None, NAMES)["checked"])

    def test_readability(self):
        self.assertTrue(readability("Short words here. Another short one.")["passed"])
        long = " ".join(["word"] * 40) + "."
        self.assertFalse(readability(long)["passed"])

    def test_run_checks(self):
        card = {"scores": {c["id"]: {"score": 4} for c in CARD["criteria"]}}
        self.assertTrue(run_checks(good_prd(), {"https://statquest.org/about"}, card, NAMES)["passed"])
        self.assertFalse(run_checks(good_prd(), set(), card, NAMES)["passed"])  # link not from research


class LinkCheckTests(unittest.TestCase):
    def test_pick_claims_prefers_numbers_and_good_grades(self):
        claims = [claim("https://d.com", grade="D"), claim("https://a.gov", grade="A"),
                  claim("https://n.com", text="A $2 billion market", grade="D"),
                  claim("https://a.gov", text="dup", grade="A")]
        picked = reviewer.pick_claims(claims, limit=2)
        self.assertEqual([c["url"] for c in picked], ["https://n.com", "https://a.gov"])
        self.assertEqual(len(reviewer.pick_claims(claims)), 3)  # one per URL

    def test_decide_status(self):
        c = claim("https://x.com/p", quote="AI-generated content must be labelled")
        pages = {"https://x.com/p": "Rules: AI-generated content must be labelled clearly."}
        self.assertEqual(reviewer.decide_link_status(c, pages, {})["status"], "confirmed")
        self.assertEqual(reviewer.decide_link_status(c, {"https://x.com/p": "Other text."}, {})["status"], "not_found")
        reported = {"https://x.com/p": {"fetched": True, "quote_present": "partly"}}
        self.assertEqual(reviewer.decide_link_status(c, {}, reported)["status"], "partly")
        self.assertEqual(reviewer.decide_link_status(c, {}, {})["status"], "fetch_failed")

    def test_check_links_uses_page_text_over_model_report(self):
        url = "https://x.com/p"
        reply = link_message([{"url": url, "fetched": True, "quote_present": "yes"}],
                             pages=[(url, "Nothing relevant on this page.")])
        client = FakeClient(link_reply=reply)
        results, usage = reviewer.check_links([claim(url)], client=client)
        self.assertEqual((results[0]["status"], results[0]["checked_by"]), ("not_found", "code"))
        tool = client.link_calls[0]["tools"][0]
        self.assertEqual((tool["type"], tool["max_uses"]), ("web_fetch_20260209", 1))
        self.assertIn(url, client.link_calls[0]["messages"][0]["content"])

    def test_no_claims_no_call(self):
        client = FakeClient()
        self.assertEqual(reviewer.check_links([], client=client), ([], {}))
        self.assertEqual(client.link_calls, [])


class ReviewTests(unittest.TestCase):
    def test_review_result(self):
        findings = [{"severity": "minor", "section": "1", "category": "c", "issue": "i", "fix": "f"},
                    {"severity": "critical", "section": "10", "category": "security", "issue": "No auth.", "fix": "Add auth."}]
        client = FakeClient(prd_review=sample_review(findings=findings, score=3))
        result = reviewer.review_prd(good_prd(), claims=[claim("https://statquest.org/about")], client=client)
        self.assertEqual(result.findings[0]["severity"], "critical")  # sorted by severity
        self.assertEqual(result.rubric_average, 3.0)
        self.assertTrue(result.needs_revision)
        self.assertEqual(len(client.link_calls), 1)
        self.assertEqual(result.to_json()["counts"], {"critical": 1, "major": 0, "minor": 1})

    def test_minor_only_needs_no_revision(self):
        result = reviewer.review_prd(good_prd(), client=FakeClient())
        self.assertFalse(result.needs_revision)

    def test_revision_feedback(self):
        result = reviewer.review_prd(good_prd(), client=FakeClient(prd_review=sample_review(findings=[
            {"severity": "major", "section": "13", "category": "observability", "issue": "No alerts.", "fix": "Add alerts."}])))
        quality = run_checks(good_prd(3), set(), {"scores": {"wow": {"score": 4}}}, NAMES)
        text = reviewer.revision_feedback(result, quality)
        self.assertIn("[major] Section 13 (observability): No alerts. Fix: Add alerts.", text)
        self.assertIn("is not from the checked research", text)
        self.assertIn("Wow factor: scorecard 4, PRD 3", text)
        self.assertNotIn("minor", text)

    def test_writer_revise_mode(self):
        client = FakeClient()
        prd_writer.write_prd("idea", client=client, draft="# PRD: old", feedback="- fix X")
        msg = client.stream_calls[0]["messages"][0]["content"]
        self.assertIn("<draft_prd>\n# PRD: old\n</draft_prd>", msg)
        self.assertIn("<review_findings>\n- fix X\n</review_findings>", msg)


class OrchestratorReviewTests(unittest.TestCase):
    def _run(self, client, **kwargs):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out, met = Path(tmp.name, "outputs"), Path(tmp.name, "metrics")
        metrics = orchestrator.run(STORYML, client=client, outputs_dir=out, metrics_dir=met, **kwargs)
        return metrics, out / STORYML.stem

    def test_clean_prd_is_not_revised_and_passes_gate(self):
        client = FakeClient(prd_text=good_prd())
        metrics, out = self._run(client)
        self.assertFalse(metrics["revised"])
        self.assertEqual(client.revision_calls, [])
        self.assertEqual(metrics["quality_gate"], "pass")
        self.assertTrue((out / "review.json").exists())
        self.assertTrue((out / "quality.json").exists())

    def test_serious_findings_trigger_one_revision(self):
        review = sample_review(findings=[{"severity": "major", "section": "10", "category": "security",
                                          "issue": "No auth plan.", "fix": "Add one."}])
        client = FakeClient(prd_text=good_prd(), prd_review=review)
        metrics, out = self._run(client)
        self.assertTrue(metrics["revised"])
        self.assertEqual(len(client.revision_calls), 1)
        self.assertTrue((out / "PRD.draft.md").exists())
        self.assertIn("No auth plan.", client.revision_calls[0]["messages"][0]["content"])

    def test_failed_checks_trigger_revision_even_without_review(self):
        client = FakeClient(prd_text=good_prd(score=3))  # scores differ from the scorecard
        metrics, _ = self._run(client, do_review=False)
        self.assertTrue(metrics["revised"])
        self.assertIn("scorecard 4, PRD 3", client.revision_calls[0]["messages"][0]["content"])

    def test_no_revise(self):
        client = FakeClient(prd_text=good_prd(score=3))
        metrics, _ = self._run(client, revise=False)
        self.assertFalse(metrics["revised"])
        self.assertEqual(metrics["quality_gate"], "fail")

    def test_low_rubric_fails_gate(self):
        metrics, _ = self._run(FakeClient(prd_text=good_prd(), prd_review=sample_review(findings=[], score=2)))
        self.assertEqual(metrics["quality_gate"], "fail")

    def test_reviewer_failure_keeps_prd(self):
        metrics, out = self._run(FakeClient(prd_text=good_prd(), fail={"reviewer": RuntimeError("overloaded")}))
        self.assertIn("error", metrics["review"])
        self.assertTrue((out / "PRD.md").exists())
        self.assertEqual(metrics["quality_gate"], "pass")


class EvalHarnessTests(unittest.TestCase):
    def test_check_expectations(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "PRD.md").write_text("Contact jane.doe@example.com")
            metrics = {"status": "completed", "guardrails": {"decision": "allow"}, "quality_gate": "fail"}
            failures = run_evals.check_expectations(
                {"status": "blocked", "guardrails_in": ["warn"], "quality_gate": "pass",
                 "must_not_contain": ["jane.doe@example.com"]}, metrics, out)
            self.assertEqual(len(failures), 4)
            self.assertEqual(run_evals.check_expectations({"status": "completed"}, metrics, out), [])

    def test_cases_file_is_valid(self):
        for case in run_evals.load_cases():
            self.assertTrue((ROOT / case["transcript"]).exists(), case["name"])

    def test_run_evals_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = run_evals.run_evals(run_evals.load_cases(["injection"]), client=FakeClient(),
                                          cheap=True, root=Path(tmp))
            self.assertEqual((summary["passed"], summary["total"]), (1, 1))
            self.assertTrue((Path(tmp) / "summary.json").exists())

    def test_a_crashing_case_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = FakeClient(review="not json")  # guardrail review breaks
            summary = run_evals.run_evals(run_evals.load_cases(["storyml"]), client=client, root=Path(tmp))
            self.assertFalse(summary["results"][0]["passed"])
            self.assertIn("crashed", summary["results"][0]["failures"][0])


if __name__ == "__main__":
    unittest.main()
