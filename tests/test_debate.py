"""Phase 4 tests: Advocate vs. Skeptic debate, the Scorer, and their place in the orchestrator."""

import json
import tempfile
import unittest
from pathlib import Path

from apps.orchestrator import run as orchestrator
from packages.agents.debate import agent as debate
from packages.agents.scorer import agent as scorer
from tests.fakes import FakeClient, sample_scores

ROOT = Path(__file__).resolve().parents[1]
STORYML = ROOT / "data" / "transcripts" / "storyml-newsletter.md"
TRANSCRIPT = "SECRET-TRANSCRIPT-MARKER: a newsletter that teaches ML through stories."
RESEARCH = "SECRET-RESEARCH-MARKER: [A] fact from nist.gov"
NOTES = ["SECRET-NOTE-MARKER: disclose AI-written content"]
MARKERS = ["SECRET-TRANSCRIPT-MARKER", "SECRET-RESEARCH-MARKER", "SECRET-NOTE-MARKER"]


def user_text(kwargs):
    return kwargs["messages"][0]["content"]


class DebateTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient()
        self.result = debate.run_debate(TRANSCRIPT, research=RESEARCH, notes=NOTES, client=self.client)

    def test_skeptic_never_sees_background(self):
        skeptic_inputs = [user_text(k) for role, k in self.client.debate_calls if role == "skeptic"]
        self.assertEqual(len(skeptic_inputs), debate.ROUNDS + 1)
        for text in skeptic_inputs:
            for marker in MARKERS:
                self.assertNotIn(marker, text)
            self.assertIn("<pitch>", text)

    def test_advocate_sees_full_context(self):
        for role, k in self.client.debate_calls:
            if role == "advocate":
                for marker in MARKERS:
                    self.assertIn(marker, user_text(k))

    def test_turn_order_and_count(self):
        roles = [role for role, _ in self.client.debate_calls]
        self.assertEqual(roles, ["advocate", "skeptic", "advocate", "skeptic", "advocate", "skeptic"])
        self.assertEqual(self.result.calls, 2 * debate.ROUNDS + 2)
        self.assertEqual([(t["round"], t["speaker"]) for t in self.result.turns],
                         [(1, "skeptic"), (1, "advocate"), (2, "skeptic"), (2, "advocate")])

    def test_later_skeptic_turns_see_earlier_debate(self):
        last = [user_text(k) for role, k in self.client.debate_calls if role == "skeptic"][-1]
        self.assertIn("advocate turn 3", last)  # the round-2 answer

    def test_cost_adds_up(self):
        self.assertAlmostEqual(self.result.cost_usd, 6 * (1000 * 4 + 2000 * 20) / 1e6)

    def test_transcript_md(self):
        md = self.result.transcript_md()
        for heading in ["## Pitch (Advocate)", "## Round 1: Skeptic", "## Round 2: Advocate",
                        "## Closing statement (Skeptic)"]:
            self.assertIn(heading, md)


class VerdictTests(unittest.TestCase):
    def setUp(self):
        self.card = scorer.load_scorecard()

    def scores(self, default, **overrides):
        return {c["id"]: {"score": overrides.get(c["id"], default)} for c in self.card["criteria"]}

    def test_go(self):
        self.assertEqual(scorer.verdict(self.scores(4), self.card), ("go", 4.0))

    def test_strong_average_with_one_weak_criterion_is_pivot(self):
        self.assertEqual(scorer.verdict(self.scores(4, defensibility=2), self.card)[0], "pivot")

    def test_no_go(self):
        self.assertEqual(scorer.verdict(self.scores(2), self.card)[0], "no_go")
        self.assertEqual(scorer.verdict(self.scores(5, ethics=1), self.card)[0], "no_go")

    def test_missing_criterion_counts_as_one(self):
        partial = self.scores(4)
        partial.pop("wow")
        decision, average = scorer.verdict(partial, self.card)
        self.assertEqual((decision, average), ("pivot", 3.7))


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self.card = scorer.load_scorecard()

    def test_valid_answer_has_no_issues(self):
        _, issues = scorer.validate(sample_scores(), self.card)
        self.assertEqual(issues, [])

    def test_wrong_framework_missing_and_duplicate(self):
        answer = sample_scores()
        answer["scores"][0]["frameworks"] = ["Gut feeling"]
        answer["scores"][1]["evidence"] = " "
        answer["scores"].append(dict(answer["scores"][2]))
        answer["scores"] = [s for s in answer["scores"] if s["criterion"] != "wow"]
        _, issues = scorer.validate(answer, self.card)
        text = " ".join(issues)
        self.assertIn("customer_need: no listed framework named", text)
        self.assertIn("competitors: no evidence given", text)
        self.assertIn("scored twice", text)
        self.assertIn("wow: missing score", text)

    def test_framework_aliases(self):
        self.assertTrue(scorer._framework_ok(["Marty Cagan's Four Big Risks"], ["Cagan Four Risks (usability)"]))
        self.assertTrue(scorer._framework_ok(["Jobs to be Done"], ["JTBD"]))
        self.assertFalse(scorer._framework_ok(["price comparison"], ["RICE (effort)"]))
        self.assertFalse(scorer._framework_ok(["heartfelt"], ["Google HEART"]))


class RunScorerTests(unittest.TestCase):
    def test_result_and_request(self):
        client = FakeClient(scores=sample_scores(4, defensibility=2))
        result = scorer.run_scorer(TRANSCRIPT, research=RESEARCH, debate_md="## Pitch", client=client)
        self.assertEqual(result.verdict, "pivot")
        self.assertEqual(result.scores["defensibility"]["score"], 2)
        kwargs = client.debate_calls[0][1]
        schema = kwargs["output_config"]["format"]["schema"]
        self.assertEqual(len(schema["properties"]["scores"]["items"]["properties"]["criterion"]["enum"]), 10)
        for part in ["<scorecard>", "<transcript>", "<research>", "<debate>"]:
            self.assertIn(part, user_text(kwargs))

    def test_brief_for_prd(self):
        result = scorer.run_scorer(TRANSCRIPT, client=FakeClient())
        brief = result.brief_for_prd(scorer.load_scorecard())
        self.assertIn("| Customer need | 4/5 | JTBD |", brief)
        self.assertIn("Verdict: GO", brief)
        self.assertIn("Goals Mission: goals_mission finding", brief)
        self.assertIn("- Who pays?", brief)

    def test_bad_json_raises(self):
        with self.assertRaises(scorer.ScorerError):
            scorer.run_scorer(TRANSCRIPT, client=FakeClient(scores="not json"))


class OrchestratorDebateTests(unittest.TestCase):
    def _run(self, client, **kwargs):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out, met = Path(tmp.name, "outputs"), Path(tmp.name, "metrics")
        metrics = orchestrator.run(STORYML, client=client, outputs_dir=out, metrics_dir=met, **kwargs)
        return metrics, out / STORYML.stem

    def test_evaluation_feeds_prd_writer(self):
        client = FakeClient()
        metrics, out = self._run(client)
        self.assertTrue((out / "debate.md").exists())
        saved = json.loads((out / "scorecard.json").read_text())
        self.assertEqual(saved["verdict"], "go")
        self.assertEqual(metrics["evaluation"]["verdict"], "go")
        prd_input = client.stream_calls[0]["messages"][0]["content"]
        self.assertIn("<evaluation>", prd_input)
        self.assertIn("Verdict: GO", prd_input)
        self.assertIn("Skeptic closing statement", prd_input)

    def test_skeptic_never_gets_background_blocks_in_full_run(self):
        # The pitch may quote evidence (that is the point of a pitch), but the Skeptic
        # must never receive the transcript, research or guardrail notes themselves.
        client = FakeClient()
        self._run(client)
        for role, kwargs in client.debate_calls:
            if role == "skeptic":
                for tag in ("<transcript>", "<research>", "<guardrail_notes>"):
                    self.assertNotIn(tag, user_text(kwargs))

    def test_debate_failure_does_not_stop_the_run(self):
        metrics, out = self._run(FakeClient(fail={"skeptic": RuntimeError("overloaded")}))
        self.assertIn("error", metrics["evaluation"])
        self.assertTrue((out / "PRD.md").exists())
        self.assertFalse((out / "scorecard.json").exists())

    def test_scorer_failure_still_passes_skeptic_closing(self):
        client = FakeClient(fail={"scorer": RuntimeError("overloaded")})
        metrics, out = self._run(client)
        self.assertIn("error", metrics["evaluation"])
        self.assertTrue((out / "debate.md").exists())
        self.assertIn("Scorer failed", client.stream_calls[0]["messages"][0]["content"])

    def test_skip_debate(self):
        client = FakeClient()
        metrics, _ = self._run(client, do_debate=False)
        roles = {role for role, _ in client.debate_calls}
        self.assertFalse(roles & {"advocate", "skeptic", "scorer"})
        self.assertNotIn("evaluation", metrics)
        self.assertNotIn("<evaluation>", client.stream_calls[0]["messages"][0]["content"])


if __name__ == "__main__":
    unittest.main()
