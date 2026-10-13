"""Hard budget tests: no Claude call may start unless its worst case fits, and the run never goes over."""

import tempfile
import threading
import unittest
from unittest import mock
from pathlib import Path

from apps.orchestrator import run as orchestrator
from packages.observability import budget
from tests.fakes import FakeClient
from tests.test_review import good_prd

STORYML = orchestrator.REPO_ROOT / "data" / "transcripts" / "storyml-newsletter.md"


class FakeMessage:
    def __init__(self, inp, out, searches=0, model=budget.MODEL):
        from types import SimpleNamespace
        self.model = model
        self.usage = SimpleNamespace(input_tokens=inp, output_tokens=out, cache_read_input_tokens=0,
                                     cache_creation_input_tokens=0,
                                     server_tool_use=SimpleNamespace(web_search_requests=searches))


class MeterTests(unittest.TestCase):
    def test_no_meter_means_no_limit(self):
        with budget.budget_call("x", 10_000, 64_000) as (allowed, settle):
            self.assertEqual(allowed, 64_000)
            settle(FakeMessage(1, 1))

    def test_caps_max_tokens_to_what_fits(self):
        meter = budget.Meter(1.0)
        with meter.active(), budget.budget_call("x", 3_000, 64_000) as (allowed, settle):
            # input: 3000 chars / 3 = 1000 tokens, reserved at the fallback-safe price
            self.assertEqual(allowed, int((1.0 - 1000 * budget.IN_USD) / budget.OUT_USD))
            settle(FakeMessage(1000, 20_000))
        self.assertAlmostEqual(meter.spent, (1000 * 4 + 20_000 * 20) / 1e6)
        self.assertAlmostEqual(meter.held, 0.0)

    def test_refuses_when_even_a_short_answer_does_not_fit(self):
        meter = budget.Meter(0.03)
        with meter.active(), self.assertRaises(budget.BudgetExceeded):
            with budget.budget_call("x", 3_000, 64_000):
                pass
        self.assertEqual((meter.spent, meter.held), (0.0, 0.0))

    def test_searches_count_toward_the_worst_case(self):
        meter = budget.Meter(1.0)
        with meter.active(), budget.budget_call("x", 0, 64_000, searches=4) as (allowed, settle):
            fixed = 4 * (budget.TOKENS_PER_SEARCH * budget.IN_USD + 0.01)
            self.assertEqual(allowed, int((1.0 - fixed) / budget.OUT_USD))
            settle(FakeMessage(0, 0, searches=4))
        self.assertAlmostEqual(meter.spent, 0.04)

    def test_reserve_is_off_limits(self):
        meter = budget.Meter(2.0)
        meter.reserve(1.5)
        self.assertAlmostEqual(meter.available(), 0.5)
        with meter.active(), budget.budget_call("x", 0, 64_000) as (allowed, settle):
            self.assertEqual(allowed, int(0.5 / budget.OUT_USD))
            settle(FakeMessage(0, 0))
        meter.release_reserve()
        self.assertAlmostEqual(meter.available(), 2.0)

    def test_parallel_calls_cannot_overspend_together(self):
        meter = budget.Meter(1.0)
        allowed, errors, gate = [], [], threading.Barrier(4)

        def worker():
            with meter.active():
                gate.wait()
                try:
                    with budget.budget_call("x", 0, 30_000) as (a, settle):
                        allowed.append(a)
                        gate_after.wait()
                        settle(FakeMessage(0, a))  # worst case: uses every allowed token
                except budget.BudgetExceeded:
                    errors.append(1)
                    gate_after.wait()

        gate_after = threading.Barrier(4)
        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertLessEqual(sum(allowed) * budget.OUT_USD, 1.0 + 1e-9)
        self.assertLessEqual(meter.spent, 1.0 + 1e-9)


class RunBudgetTests(unittest.TestCase):
    def _run(self, limit, client=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        t = Path(tmp.name)
        client = client or FakeClient(prd_text=good_prd())
        m = orchestrator.run(STORYML, client=client, outputs_dir=t / "outputs", metrics_dir=t / "metrics",
                             budget_usd=limit)
        return m, t, client

    def test_two_dollar_run_stays_under_and_writes_prd(self):
        m, t, client = self._run(2.0)
        self.assertLessEqual(m["budget"]["spent_usd"], 2.0)
        self.assertTrue(m["budget"]["hard_limit"])
        self.assertTrue((t / "outputs" / "storyml-newsletter" / "PRD.md").exists())
        self.assertLessEqual(client.stream_calls[0]["max_tokens"], 64_000)

    def test_small_budget_keeps_money_for_the_prd(self):
        m, t, client = self._run(1.0)
        self.assertIn("research", m["budget"]["skipped"])
        self.assertIn("debate", m["budget"]["skipped"])
        self.assertEqual(client.research_calls, [])
        self.assertTrue((t / "outputs" / "storyml-newsletter" / "PRD.md").exists())
        self.assertLessEqual(m["budget"]["spent_usd"], 1.0)

    def test_refused_calls_are_reported_as_skipped(self):
        # Just enough that research may start (>= $0.25 free after guardrails and the PRD reserve),
        # but, with large pages per search, not enough for the market agent's first call (2 searches).
        limit = orchestrator.PRD_RESERVE_USD + 0.022 + 0.255
        with mock.patch.object(budget, "TOKENS_PER_SEARCH", 100_000):
            m, _, _ = self._run(limit)
        self.assertIn("research:market", m["budget"]["skipped"])
        self.assertLessEqual(m["budget"]["spent_usd"], limit)

    def test_too_small_budget_is_rejected(self):
        with self.assertRaises(ValueError):
            self._run(orchestrator.MIN_BUDGET_USD - 0.01)

    def test_reserve_matches_prd_writer_settings(self):
        from packages.agents.prd_writer import agent as writer
        self.assertAlmostEqual(orchestrator.PRD_RESERVE_USD,
                               round(writer.MAX_TOKENS * budget.out_usd(writer.MODEL) + 0.10, 2))
        self.assertLess(orchestrator.PRD_RESERVE_USD, 1.0)

    def test_research_worst_case_uses_sonnet_prices(self):
        # 7 searches on Sonnet: well under $1 at worst, so at the $2 default all three run in parallel.
        worst = orchestrator.research_worst_case_usd(STORYML.read_text())
        self.assertGreater(worst, 0.5)
        self.assertLess(worst, 2.0 - orchestrator.PRD_RESERVE_USD - 0.05)

    def test_agents_use_the_configured_models(self):
        from packages.agents.common import OPUS, SONNET
        _, _, client = self._run(None)
        self.assertEqual({k["model"] for k in client.research_calls}, {SONNET})
        self.assertEqual({k["model"] for _, k in client.debate_calls}, {SONNET})
        self.assertEqual(client.stream_calls[0]["model"], OPUS)


class PricingTests(unittest.TestCase):
    def test_reserve_prices_cover_the_fallback_model(self):
        from packages.agents.common import OPUS, SONNET
        self.assertAlmostEqual(budget.out_usd(OPUS), 25 / 1e6)    # Opus 5.5 may fall back to Opus 4.8
        self.assertAlmostEqual(budget.out_usd(SONNET), 10 / 1e6)  # Sonnet 5 costs the same as Sonnet 5.5

    def test_cost_uses_the_model_that_answered(self):
        from packages.agents.common import OPUS, SONNET, estimate_cost
        usage = {"input_tokens": 1_000_000, "output_tokens": 1_000_000}
        self.assertEqual(estimate_cost(usage, OPUS), 24.0)
        self.assertEqual(estimate_cost(usage, SONNET), 12.0)
        self.assertEqual(estimate_cost(usage, "some-new-model"), 30.0)  # unknown: priced high, never under

    def test_worst_case_fallback_reply_stays_under_the_limit(self):
        meter = budget.Meter(1.0)
        with meter.active(), budget.budget_call("x", 0, 64_000) as (allowed, settle):
            settle(FakeMessage(0, allowed, model="claude-opus-4-8"))  # declined, then answered by Opus 4.8
        self.assertLessEqual(meter.spent, 1.0 + 1e-9)


class LeanProfileTests(unittest.TestCase):
    def _run(self, **kwargs):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        t = Path(tmp.name)
        client = FakeClient(prd_text=good_prd())
        m = orchestrator.run(STORYML, client=client, outputs_dir=t / "outputs", metrics_dir=t / "metrics",
                             budget_usd=None, **kwargs)
        return m, client

    def test_lean_settings_are_applied(self):
        m, client = self._run(profile="lean")
        self.assertEqual(m["profile"], "lean")
        self.assertEqual({k["tools"][0]["max_uses"] for k in client.research_calls}, {1})
        skeptic_turns = [r for r, _ in client.debate_calls if r == "skeptic"]
        self.assertEqual(len(skeptic_turns), 2)  # 1 round + closing
        self.assertEqual(client.link_calls, [])
        self.assertEqual(client.stream_calls[0]["output_config"]["effort"], "low")

    def test_standard_is_the_default(self):
        m, client = self._run()
        self.assertEqual(m["profile"], "standard")
        self.assertEqual(len([r for r, _ in client.debate_calls if r == "skeptic"]), 3)
        self.assertEqual(sorted(k["tools"][0]["max_uses"] for k in client.research_calls), [1, 2, 2])

    def test_profile_from_env(self):
        for value, expected in [(None, "standard"), ("lean", "lean"), (" LEAN ", "lean"), ("odd", "standard")]:
            env = {} if value is None else {"PRD_AGENT_PROFILE": value}
            with mock.patch.dict("os.environ", env, clear=True):
                self.assertEqual(orchestrator.default_profile(), expected, value)


if __name__ == "__main__":
    unittest.main()
