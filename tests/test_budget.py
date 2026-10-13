"""Hard budget tests: no Claude call may start unless its worst case fits, and the run never goes over."""

import tempfile
import threading
import unittest
from pathlib import Path

from apps.orchestrator import run as orchestrator
from packages.observability import budget
from tests.fakes import FakeClient
from tests.test_review import good_prd

STORYML = orchestrator.REPO_ROOT / "data" / "transcripts" / "storyml-newsletter.md"


class FakeMessage:
    def __init__(self, inp, out, searches=0):
        from types import SimpleNamespace
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
            # input: 3000 chars / 3 = 1000 tokens = $0.004; output room: $0.996 / $20 per M
            self.assertEqual(allowed, int((1.0 - 0.004) / budget.OUT_USD))
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
        m, t, client = self._run(0.8)
        self.assertIn("research", m["budget"]["skipped"])
        self.assertIn("debate", m["budget"]["skipped"])
        self.assertEqual(client.research_calls, [])
        self.assertTrue((t / "outputs" / "storyml-newsletter" / "PRD.md").exists())
        self.assertLessEqual(m["budget"]["spent_usd"], 0.8)

    def test_refused_calls_are_reported_as_skipped(self):
        # $1.50: $1.20 is kept for the PRD, so research may start but its first search call can't fit.
        m, _, _ = self._run(1.5)
        self.assertIn("research:market", m["budget"]["skipped"])
        self.assertLessEqual(m["budget"]["spent_usd"], 1.5)

    def test_too_small_budget_is_rejected(self):
        with self.assertRaises(ValueError):
            self._run(0.5)

    def test_research_runs_one_by_one_when_money_is_tight(self):
        transcript = STORYML.read_text()
        self.assertGreater(orchestrator.research_worst_case_usd(transcript), 1.0)


if __name__ == "__main__":
    unittest.main()
