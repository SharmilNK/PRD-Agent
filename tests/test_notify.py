"""Phase 7 tests: Gmail alerts on new / updated PRDs and on problems."""

import email
import json
import smtplib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from apps.orchestrator import run as orchestrator
from apps.orchestrator.publish import publish, read_prd
from packages.integrations import notify
from tests.test_github_log import metrics

OLD = "# PRD: X\n\n## 1. Press Release and FAQ\nOld text.\n\n## 2. Problem Statement and Why Now\nSame.\n\n## 3. Old Section\nGone.\n"
NEW = "# PRD: X\n\n## 1. Press Release and FAQ\nNew text.\n\n## 2. Problem Statement and Why Now\nSame.\n\n## 4. New Section\nHi.\n"
GMAIL = {"GMAIL_ADDRESS": "sender@gmail.com", "GMAIL_APP_PASSWORD": "app-pass", "ALERT_TO": "a@x.com, b@x.com"}


class FakeSMTP:
    instances = []

    def __init__(self, host, port, context=None, timeout=None):
        self.host, self.port, self.sent, self.login_args = host, port, [], None
        FakeSMTP.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def login(self, user, password):
        self.login_args = (user, password)

    def send_message(self, msg):
        self.sent.append(msg)


class BrokenSMTP(FakeSMTP):
    def login(self, user, password):
        raise smtplib.SMTPAuthenticationError(535, b"bad credentials")


class SectionTests(unittest.TestCase):
    def test_split_and_changes(self):
        self.assertEqual(list(notify.split_sections(OLD)),
                         ["1. Press Release and FAQ", "2. Problem Statement and Why Now", "3. Old Section"])
        changes = notify.section_changes(OLD, NEW)
        self.assertEqual(changes, {"added": ["4. New Section"], "changed": ["1. Press Release and FAQ"],
                                   "removed": ["3. Old Section"]})

    def test_whitespace_only_is_not_a_change(self):
        self.assertEqual(notify.section_changes(OLD, OLD.replace("Old text.", "Old   text.")),
                         {"added": [], "changed": [], "removed": []})


class EventTests(unittest.TestCase):
    def test_events(self):
        self.assertEqual(notify.detect_events(metrics(), None, NEW)[0], ["new"])
        self.assertEqual(notify.detect_events(metrics(), OLD, NEW)[0], ["updated"])
        self.assertEqual(notify.detect_events(metrics(), NEW, NEW)[0], [])
        self.assertEqual(notify.detect_events(metrics(status="blocked"), OLD, None)[0], ["blocked"])
        m = metrics(quality_gate="fail", steps=[{"agent": "reviewer", "error": "x"}])
        self.assertEqual(notify.detect_events(m, NEW, NEW)[0], ["quality_fail", "error"])

    def test_alert_on_filter(self):
        self.assertEqual(notify.wanted_events({}), set(notify.EVENTS))
        self.assertEqual(notify.wanted_events({"ALERT_ON": "blocked, error, bogus"}), {"blocked", "error"})


class BuildAlertTests(unittest.TestCase):
    def test_content_and_escaping(self):
        m = metrics(transcript="data/transcripts/<script>.md")
        changes = notify.section_changes(OLD, NEW)
        with mock.patch.dict("os.environ", {"GITHUB_REPOSITORY": "o/r", "DASHBOARD_URL": "https://o.github.io/r"}):
            alert = notify.build_alert(m, ["updated"], changes, issues=[12])
        self.assertTrue(alert.subject.startswith("[PRD-Agent] PRD updated: <script> | verdict PIVOT | quality pass"))
        self.assertIn("Changed: 1. Press Release and FAQ", alert.text)
        self.assertIn("wow: 4/5", alert.text)
        self.assertIn("https://github.com/o/r/issues/12", alert.text)
        self.assertIn("Dashboard: https://o.github.io/r", alert.text)
        self.assertNotIn("<script>", alert.html)
        self.assertIn("&lt;script&gt;", alert.html)

    def test_blocked_alert(self):
        m = metrics(status="blocked", guardrails={"decision": "block", "reasons": ["Not a product idea"]})
        alert = notify.build_alert(m, ["blocked"], {})
        self.assertEqual(alert.subject, "[PRD-Agent] Run blocked: storyml-newsletter")
        self.assertIn("Why blocked: Not a product idea", alert.text)


class NotifyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)
        (self.out / "PRD.md").write_text(NEW)
        FakeSMTP.instances = []

    def test_sends_with_gmail_settings(self):
        info = notify.notify(metrics(), self.out, OLD, env=GMAIL, smtp_factory=FakeSMTP)
        self.assertTrue(info["sent"])
        smtp = FakeSMTP.instances[0]
        self.assertEqual((smtp.host, smtp.port), ("smtp.gmail.com", 465))
        self.assertEqual(smtp.login_args, ("sender@gmail.com", "app-pass"))
        msg = smtp.sent[0]
        self.assertEqual(msg["To"], "a@x.com, b@x.com")
        self.assertEqual([p.get_content_type() for p in msg.iter_parts()], ["text/plain", "text/html"])
        self.assertNotIn("app-pass", json.dumps(info))

    def test_saves_eml_without_settings(self):
        info = notify.notify(metrics(), self.out, None, env={})
        self.assertFalse(info["sent"])
        saved = email.message_from_bytes((self.out / "alert.eml").read_bytes())
        self.assertIn("New PRD", saved["Subject"])

    def test_send_failure_is_reported_and_saved(self):
        info = notify.notify(metrics(), self.out, OLD, env=GMAIL, smtp_factory=BrokenSMTP)
        self.assertFalse(info["sent"])
        self.assertIn("SMTPAuthenticationError", info["reason"])
        self.assertNotIn("app-pass", info["reason"])
        self.assertTrue((self.out / "alert.eml").exists())

    def test_nothing_to_report(self):
        info = notify.notify(metrics(), self.out, NEW, env=GMAIL, smtp_factory=FakeSMTP)
        self.assertEqual(info["reason"], "nothing to report")
        self.assertEqual(FakeSMTP.instances, [])

    def test_alert_on_filters_out_updates(self):
        info = notify.notify(metrics(), self.out, OLD, env={**GMAIL, "ALERT_ON": "blocked"}, smtp_factory=FakeSMTP)
        self.assertFalse(info["sent"])
        self.assertEqual(FakeSMTP.instances, [])


class PublishAlertTests(unittest.TestCase):
    def test_full_run_sends_new_then_nothing(self):
        from tests.fakes import FakeClient
        from tests.test_review import good_prd

        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            out, met = t / "outputs", t / "metrics"
            transcript = orchestrator.REPO_ROOT / "data" / "transcripts" / "storyml-newsletter.md"
            kw = dict(index_path=t / "index.json", run_log_path=t / "RUN_LOG.md", env=GMAIL, smtp_factory=FakeSMTP)

            FakeSMTP.instances = []
            old = read_prd(out, transcript)
            m = orchestrator.run(transcript, client=FakeClient(prd_text=good_prd()), outputs_dir=out, metrics_dir=met)
            publish(m, out, met, alert=True, old_prd=old, **kw)
            self.assertEqual(m["alert"]["events"], ["new"])
            self.assertEqual(len(FakeSMTP.instances), 1)

            old = read_prd(out, transcript)
            m = orchestrator.run(transcript, client=FakeClient(prd_text=good_prd()), outputs_dir=out, metrics_dir=met)
            publish(m, out, met, alert=True, old_prd=old, **kw)
            self.assertEqual(m["alert"]["reason"], "nothing to report")
            saved = json.loads((met / f"{m['run_id']}.json").read_text())
            self.assertIn("alert", saved)
            self.assertNotIn("sender@gmail.com", json.dumps(saved))


if __name__ == "__main__":
    unittest.main()
