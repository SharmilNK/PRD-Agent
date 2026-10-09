"""Phase 6 tests: run log, GitHub issue planning and syncing, publish, and the CI entry point."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from apps.orchestrator import ci
from apps.orchestrator import run as orchestrator
from apps.orchestrator.publish import publish
from packages.integrations import github_issues as gi
from packages.integrations import run_log
from tests.fakes import FakeClient, sample_review

ROOT = Path(__file__).resolve().parents[1]
STORYML = ROOT / "data" / "transcripts" / "storyml-newsletter.md"


def metrics(**changes):
    base = {
        "run_id": "20261008T120000Z-storyml-newsletter",
        "transcript": "data/transcripts/storyml-newsletter.md",
        "status": "completed",
        "guardrails": {"decision": "allow", "reasons": []},
        "steps": [{"agent": "guardrails", "cost_usd": 0.01, "duration_s": 1.0},
                  {"agent": "research:market", "grades": {"A": 1, "B": 2, "C": 0, "D": 1}, "cost_usd": 0.1,
                   "duration_s": 2.0}],
        "evaluation": {"verdict": "pivot", "average": 3.2, "scores": {"wow": 4}},
        "review": {"counts": {"critical": 0, "major": 1, "minor": 2}, "rubric_average": 3.8,
                   "links_checked": 3, "links_confirmed": 2},
        "quality_gate": "pass", "quality": {}, "revised": False,
        "total_cost_usd": 1.2345, "total_duration_s": 60.0,
    }
    base.update(changes)
    return base


def write_review(out_dir, findings, links=()):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "review.json").write_text(json.dumps({"findings": findings, "link_checks": list(links)}))


FINDING = {"severity": "major", "section": "10", "category": "Security", "issue": "No auth plan for admins.",
           "fix": "Add SSO for the editor."}


class FakeGitHub:
    def __init__(self, open_issues=()):
        self.issues = list(open_issues)
        self.created, self.comments, self.closed = [], [], []

    def open_issues(self):
        return self.issues

    def create_issue(self, title, body, labels):
        number = 100 + len(self.created)
        self.created.append({"number": number, "title": title, "body": body, "labels": labels})
        return {"number": number}

    def comment(self, number, body):
        self.comments.append((number, body))

    def close(self, number):
        self.closed.append(number)


class RunLogTests(unittest.TestCase):
    def test_record_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            index, log = Path(tmp, "index.json"), Path(tmp, "RUN_LOG.md")
            run_log.record_run(metrics(), index, log)
            run_log.record_run(metrics(run_id="20261009T000000Z-storyml-newsletter", status="blocked"), index, log)
            run_log.record_run(metrics(total_cost_usd=9.0), index, log)  # same run id: replaced, not added
            runs = json.loads(index.read_text())["runs"]
            self.assertEqual([r["run_id"][:9] for r in runs], ["20261009T", "20261008T"])
            self.assertEqual(runs[1]["cost_usd"], 9.0)
            self.assertEqual(runs[1]["source_grades"], {"A": 1, "B": 2, "C": 0, "D": 1})
            table = log.read_text()
            self.assertIn("| 20261008T120000Z-storyml-newsletter | storyml-newsletter | completed | allow | PIVOT | 3.2 |", table)
            self.assertEqual(table.count("\n| 2026"), 2)


class PlanIssueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)

    def test_findings_links_and_gate(self):
        write_review(self.out, [FINDING, {**FINDING, "severity": "minor"}],
                     [{"url": "https://x.com/a", "status": "not_found", "claim": "c", "quote": "q"},
                      {"url": "https://y.com/b", "status": "confirmed", "claim": "c", "quote": "q"}])
        m = metrics(quality_gate="fail", quality={"links": {"unknown_links": ["https://bad.com"]}})
        issues = gi.plan_issues(m, self.out)
        self.assertEqual([i.kind for i in issues], ["finding", "link", "quality_gate"])
        self.assertIn("area:security", issues[0].labels)
        self.assertIn("Link not from checked research: https://bad.com", issues[2].body)
        self.assertTrue(issues[0].title.startswith("[storyml-newsletter] PRD section 10:"))

    def test_blocked_and_errors(self):
        m = metrics(status="blocked", guardrails={"decision": "block", "reasons": ["Not a product idea"]},
                    steps=[{"agent": "research:tech", "error": "RateLimitError: slow down"}], review=None)
        kinds = [i.kind for i in gi.plan_issues(m, self.out)]
        self.assertEqual(kinds, ["blocked", "error"])

    def test_stale_review_file_is_ignored_when_review_did_not_run(self):
        write_review(self.out, [FINDING])
        self.assertEqual(gi.plan_issues(metrics(review=None), self.out), [])

    def test_fingerprint_ignores_wording(self):
        write_review(self.out, [FINDING])
        first = gi.plan_issues(metrics(), self.out)[0]
        write_review(self.out, [{**FINDING, "issue": "Admins have no login plan."}])
        second = gi.plan_issues(metrics(), self.out)[0]
        self.assertEqual(first.fingerprint, second.fingerprint)

    def test_revised_note(self):
        write_review(self.out, [FINDING])
        self.assertIn("revised once", gi.plan_issues(metrics(revised=True), self.out)[0].body)

    def test_checked_kinds(self):
        self.assertEqual(gi.checked_kinds(metrics()), {"blocked", "error", "quality_gate", "finding", "link"})
        self.assertEqual(gi.checked_kinds(metrics(review=None)), {"blocked", "error", "quality_gate"})
        self.assertEqual(gi.checked_kinds(metrics(status="blocked", review=None)), {"blocked", "error"})


class SyncIssueTests(unittest.TestCase):
    def issue(self, number, fp, kind="finding", transcript="storyml-newsletter"):
        return {"number": number, "body": f"x\n<!-- prd-agent:fingerprint={fp} transcript={transcript} kind={kind} -->"}

    def plan(self, fp, kind="finding"):
        return gi.PlannedIssue(fp, "storyml-newsletter", kind, "title", "body", ["prd-agent"])

    def test_create_comment_close(self):
        gh = FakeGitHub([self.issue(1, "a" * 16), self.issue(2, "b" * 16),
                         self.issue(3, "c" * 16, kind="error"), self.issue(4, "d" * 16, transcript="other")])
        result = gi.sync_issues([self.plan("a" * 16), self.plan("e" * 16)], "storyml-newsletter", "run1", gh,
                                checked={"finding"})
        self.assertEqual(result, {"created": [100], "commented": [1], "closed": [2]})
        self.assertIn("fingerprint=" + "e" * 16, gh.created[0]["body"])
        self.assertNotIn(3, gh.closed)  # kind not checked in this run
        self.assertNotIn(4, gh.closed)  # other transcript

    def test_client_request(self):
        client = gi.GitHubClient("owner/repo", "tok")
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"number": 7}'
        with mock.patch("urllib.request.urlopen", return_value=response) as urlopen:
            self.assertEqual(client.create_issue("t", "b", ["prd-agent"]), {"number": 7})
        req = urlopen.call_args[0][0]
        self.assertEqual(req.full_url, "https://api.github.com/repos/owner/repo/issues")
        self.assertEqual(req.get_header("Authorization"), "Bearer tok")
        self.assertEqual(json.loads(req.data), {"title": "t", "body": "b", "labels": ["prd-agent"]})

    def test_client_from_env(self):
        with mock.patch.dict("os.environ", {"GITHUB_REPOSITORY": "o/r", "GITHUB_TOKEN": "t"}):
            self.assertIsNotNone(gi.GitHubClient.from_env())
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertIsNone(gi.GitHubClient.from_env())


class PublishTests(unittest.TestCase):
    def _run(self, gh=None, github=False, review=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        t = Path(tmp.name)
        out, met = t / "outputs", t / "metrics"
        client = FakeClient(prd_review=review) if review else FakeClient()
        m = orchestrator.run(STORYML, client=client, outputs_dir=out, metrics_dir=met)
        info = publish(m, out, met, github=github, gh=gh, index_path=t / "index.json", run_log_path=t / "RUN_LOG.md")
        return m, info, out / STORYML.stem, t

    def test_without_github_saves_plan_and_logs_run(self):
        m, info, out, t = self._run(review=sample_review(findings=[FINDING]))
        self.assertEqual(info["issue_numbers"], [])
        plan = json.loads((out / "issues.plan.json").read_text())
        self.assertTrue(any("PRD section 10" in p["title"] for p in plan))
        self.assertEqual(json.loads((t / "index.json").read_text())["runs"][0]["run_id"], m["run_id"])
        saved = json.loads((t / "metrics" / f"{m['run_id']}.json").read_text())
        self.assertIn("github", saved)

    def test_with_github(self):
        gh = FakeGitHub()
        m, info, _, t = self._run(gh=gh, review=sample_review(findings=[FINDING]))
        self.assertTrue(info["created"])
        self.assertIn(f"#{info['created'][0]}", (t / "RUN_LOG.md").read_text())

    def test_github_flag_without_token(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            _, info, out, _ = self._run(github=True)
        self.assertIn("skipped", info)
        self.assertTrue((out / "issues.plan.json").exists())

    def test_github_error_keeps_plan(self):
        gh = FakeGitHub()
        gh.open_issues = mock.Mock(side_effect=gi.GitHubError("GET -> 401"))
        _, info, out, _ = self._run(gh=gh)
        self.assertIn("401", info["error"])
        self.assertTrue((out / "issues.plan.json").exists())


class CITests(unittest.TestCase):
    def test_is_transcript(self):
        self.assertTrue(ci.is_transcript("data/transcripts/storyml-newsletter.md"))
        self.assertFalse(ci.is_transcript("data/transcripts/../../README.md"))
        self.assertFalse(ci.is_transcript("evals/fixtures/injection.md"))
        self.assertFalse(ci.is_transcript("data/transcripts/missing.md"))

    def test_manual_input_is_validated(self):
        self.assertEqual(ci.pick_transcripts({"INPUT_TRANSCRIPT": "data/transcripts/storyml-newsletter.md"}),
                         ["data/transcripts/storyml-newsletter.md"])
        with self.assertRaises(SystemExit):
            ci.pick_transcripts({"INPUT_TRANSCRIPT": "../secrets.md"})

    def test_changed_transcripts_filters_paths(self):
        out = "data/transcripts/storyml-newsletter.md\nREADME.md\ndata/transcripts/missing.md\n"
        with mock.patch("subprocess.run", return_value=mock.Mock(stdout=out)) as run:
            self.assertEqual(ci.changed_transcripts("a" * 40, "b" * 40), ["data/transcripts/storyml-newsletter.md"])
            self.assertEqual(run.call_args[0][0][:2], ["git", "diff"])
            ci.changed_transcripts(ci.ZERO_SHA, "b" * 40)
            self.assertEqual(run.call_args[0][0][:2], ["git", "diff-tree"])

    def test_main_runs_and_publishes(self):
        with mock.patch.object(ci, "pick_transcripts", return_value=["data/transcripts/storyml-newsletter.md"]), \
             mock.patch.object(ci.orchestrator, "run", return_value=metrics()) as run, \
             mock.patch.object(ci, "publish", return_value={"issue_numbers": [5]}) as pub, \
             mock.patch("sys.stdout", new=io.StringIO()):
            self.assertEqual(ci.main(), 0)
        run.assert_called_once()
        self.assertTrue(pub.call_args.kwargs["github"])

    def test_main_reports_failure(self):
        with mock.patch.object(ci, "pick_transcripts", return_value=["data/transcripts/storyml-newsletter.md"]), \
             mock.patch.object(ci.orchestrator, "run", side_effect=RuntimeError("boom")), \
             mock.patch("sys.stdout", new=io.StringIO()), mock.patch("sys.stderr", new=io.StringIO()):
            self.assertEqual(ci.main(), 1)


if __name__ == "__main__":
    unittest.main()
