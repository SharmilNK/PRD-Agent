"""Phase 9 tests: tracing, cost budget, the operations report, and their dashboard/alert hooks."""

import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from apps.dashboard import build
from apps.orchestrator import run as orchestrator
from packages.integrations import notify
from packages.observability import report, tracing
from tests.fakes import FakeClient
from tests.test_github_log import metrics
from tests.test_review import good_prd

STORYML = orchestrator.REPO_ROOT / "data" / "transcripts" / "storyml-newsletter.md"


def fake_message(inp=100, out=50, read=300, write=0, searches=0):
    usage = SimpleNamespace(input_tokens=inp, output_tokens=out, cache_read_input_tokens=read,
                            cache_creation_input_tokens=write, server_tool_use=SimpleNamespace(web_search_requests=searches))
    return SimpleNamespace(model="claude-opus-5-5", stop_reason="end_turn", usage=usage, _request_id="req_123")


class TracingTests(unittest.TestCase):
    def test_no_tracer_means_no_op(self):
        with tracing.span("x") as s:
            s.set(a=1)
            s.record_message(fake_message())  # must not fail

    def test_nesting_errors_and_save(self):
        tracer = tracing.Tracer("run-1")
        with tracer.active():
            with tracing.span("run") as root:
                with tracing.span("step:a"):
                    pass
                with self.assertRaises(ValueError), tracing.span("step:b"):
                    raise ValueError("boom")
                root.set(status_note="done")
        spans = {s.name: s for s in tracer.spans}
        self.assertEqual(spans["step:a"].parent_span_id, spans["run"].span_id)
        self.assertEqual((spans["step:b"].status, spans["step:b"].error), ("error", "ValueError: boom"))
        with tempfile.TemporaryDirectory() as tmp:
            path = tracer.save(Path(tmp) / "t.jsonl")
            lines = [json.loads(l) for l in path.read_text().splitlines()]
        self.assertEqual([l["name"] for l in lines], ["run", "step:a", "step:b"])
        self.assertTrue(all(l["trace_id"] == "run-1" for l in lines))
        self.assertEqual(tracer.summary()["errors"], 1)

    def test_record_message(self):
        tracer = tracing.Tracer("r")
        with tracer.active(), tracing.span("llm:test") as s:
            s.record_message(fake_message(searches=2), "<!-- prompt: guardrails v1 -->\nRules")
        a = tracer.spans[0].attributes
        self.assertEqual((a["tokens.input"], a["tokens.output"], a["tokens.cache_read"]), (100, 50, 300))
        self.assertEqual(a["request_id"], "req_123")
        self.assertTrue(a["prompt_version"].startswith("guardrails v1@"))
        self.assertAlmostEqual(a["cost_usd"], (100 * 4 + 50 * 20 + 300 * 0.2) / 1e6 + 0.02)
        summary = tracer.summary()
        self.assertEqual((summary["llm_calls"], summary["web_searches"]), (1, 2))
        self.assertAlmostEqual(summary["cache_hit_rate"], 300 / 400, places=3)

    def test_threads_join_the_trace(self):
        tracer = tracing.Tracer("r")

        def work():
            with tracing.span("child"):
                pass

        with tracer.active(), tracing.span("parent") as parent:
            t = threading.Thread(target=tracing.run_in_context(work))
            t.start()
            t.join()
        child = next(s for s in tracer.spans if s.name == "child")
        self.assertEqual(child.parent_span_id, parent.span_id)

    def test_prompt_version_without_header(self):
        self.assertTrue(tracing.prompt_version("plain text").startswith("prompt@"))
        self.assertTrue(tracing.prompt_version([{"type": "text", "text": "<!-- prompt: prd_writer v3 -->"}])
                        .startswith("prd_writer v3@"))


class RunTracingTests(unittest.TestCase):
    def _run(self, **kwargs):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        t = Path(tmp.name)
        client = kwargs.pop("client", FakeClient(prd_text=good_prd()))
        m = orchestrator.run(STORYML, client=client, outputs_dir=t / "outputs", metrics_dir=t / "metrics", **kwargs)
        return m, t, client

    def test_trace_covers_every_claude_call(self):
        m, t, client = self._run()
        lines = [json.loads(l) for l in (t / "traces" / f"{m['run_id']}.jsonl").read_text().splitlines()]
        names = [l["name"] for l in lines]
        llm = [n for n in names if n.startswith("llm:")]
        calls = len(client.stream_calls) + len(client.create_calls) + len(client.research_calls) \
            + len(client.debate_calls) + len(client.link_calls)
        self.assertEqual(len(llm), calls)
        self.assertEqual(m["trace"]["llm_calls"], calls)
        for step in ["step:guardrails", "step:research", "step:research:market", "step:debate", "step:scorer",
                     "step:prd_writer", "step:reviewer"]:
            self.assertIn(step, names)
        by_id = {l["span_id"]: l for l in lines}
        market = next(l for l in lines if l["name"] == "step:research:market")
        self.assertEqual(by_id[market["parent_span_id"]]["name"], "step:research")
        root = next(l for l in lines if l["name"] == "run")
        self.assertIsNone(root["parent_span_id"])

    def test_trace_has_no_transcript_or_prd_text(self):
        m, t, _ = self._run()
        trace = (t / "traces" / f"{m['run_id']}.jsonl").read_text()
        self.assertNotIn("Every model, algorithm, or system becomes a character", trace)
        self.assertNotIn("Short clear text", trace)

    def test_budget_skips_optional_steps_but_writes_prd(self):
        m, t, client = self._run(budget_usd=0.0001)
        # Revision is also wanted (the PRD's link is not from research, which was skipped) and skipped too.
        self.assertEqual(m["budget"]["skipped"], ["research", "debate", "reviewer", "revision"])
        self.assertFalse(m["revised"])
        self.assertEqual(client.research_calls, [])
        self.assertTrue((t / "outputs" / "storyml-newsletter" / "PRD.md").exists())

    def test_no_budget(self):
        m, _, _ = self._run(budget_usd=None)
        self.assertEqual((m["budget"]["limit_usd"], m["budget"]["skipped"]), (None, []))

    def test_default_budget_from_env(self):
        for value, expected in [(None, 10.0), ("", 10.0), ("2.5", 2.5), ("0", None), ("none", None)]:
            env = {} if value is None else {"PRD_AGENT_MAX_COST_USD": value}
            with mock.patch.dict("os.environ", env, clear=True):
                self.assertEqual(orchestrator.default_budget(), expected, value)


class ReportTests(unittest.TestCase):
    def test_percentile(self):
        self.assertEqual(report._percentile([], 0.5), 0.0)
        self.assertEqual(report._percentile([1, 2, 3, 4], 0.5), 2.5)
        self.assertEqual(report._percentile([1, 2, 3, 4, 100], 0.95), 80.8)

    def test_build_report(self):
        runs = [
            {"status": "completed", "total_cost_usd": 2.0, "total_duration_s": 100, "budget": {"skipped": []},
             "steps": [{"agent": "research:market", "cost_usd": 0.2, "duration_s": 30},
                       {"agent": "research:tech", "error": "boom", "cost_usd": 0.0, "duration_s": 0},
                       {"agent": "prd_writer", "cost_usd": 1.0, "duration_s": 60,
                        "usage": {"input_tokens": 100, "cache_read_input_tokens": 300}}]},
            {"status": "blocked", "total_cost_usd": 0.1, "total_duration_s": 5, "budget": {"skipped": ["research"]},
             "steps": [{"agent": "guardrails", "cost_usd": 0.1, "duration_s": 5}]},
        ]
        r = report.build_report(runs)
        self.assertEqual((r["runs"], r["completed"], r["budget_skips"]), (2, 1, 1))
        agents = {a["agent"]: a for a in r["agents"]}
        self.assertEqual(agents["research"]["calls"], 2)
        self.assertEqual(agents["research"]["error_rate"], 0.5)
        self.assertEqual(agents["prd_writer"]["cache_hit_rate"], 0.75)
        self.assertEqual(r["agents"][0]["agent"], "prd_writer")  # most expensive first
        self.assertIn("prd_writer", report.format_table(r))

    def test_load_runs_skips_index_and_broken_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "index.json").write_text('{"runs": []}')
            (d / "a.json").write_text(json.dumps({"steps": []}))
            (d / "b.json").write_text("{half")
            self.assertEqual(len(report.load_runs(d)), 1)


class HookTests(unittest.TestCase):
    def test_budget_alert_event(self):
        m = metrics(budget={"limit_usd": 1.0, "spent_usd": 1.2, "skipped": ["reviewer"]})
        events, _ = notify.detect_events(m, "same", "same")
        self.assertIn("budget", events)
        alert = notify.build_alert(m, events, {})
        self.assertIn("budget reached", alert.subject)
        self.assertIn("Budget: $1.00 reached; skipped reviewer", alert.text)

    def test_dashboard_includes_ops(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(build.collect(Path(tmp))["ops"]["runs"], 0)
        self.assertTrue(build.demo_data()["ops"]["agents"])


if __name__ == "__main__":
    unittest.main()
