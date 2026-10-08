"""Phase 8 tests: dashboard data builder and the live-reload server."""

import json
import os
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path

from apps.dashboard import build, serve
from packages.integrations import run_log
from tests.test_github_log import metrics


def make_data(root: Path) -> None:
    run_log.record_run(metrics(), root / "metrics" / "index.json", root / "decisions" / "RUN_LOG.md")
    out = root / "outputs" / "storyml-newsletter"
    out.mkdir(parents=True)
    (out / "PRD.md").write_text("# PRD: StoryML\n")
    (out / "scorecard.json").write_text(json.dumps({"verdict": "pivot", "average": 3.2,
                                                    "scores": {"wow": {"score": 4}}, "unresolved_concerns": ["Who pays?"]}))
    (out / "review.json").write_text(json.dumps({"rubric": {"security": 3}, "findings": [
        {"severity": "minor", "section": "1", "category": "c", "issue": "i", "fix": "f"},
        {"severity": "major", "section": "10", "category": "security", "issue": "No auth.", "fix": "Add auth."}],
        "link_checks": [{"url": "https://x.com", "status": "not_found", "claim": "c", "quote": "q"}]}))


class BuildTests(unittest.TestCase):
    def test_collect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_data(root)
            data = build.collect(root)
            self.assertFalse(data["demo"])
            self.assertEqual(len(data["runs"]), 1)
            t = data["transcripts"]["storyml-newsletter"]
            self.assertEqual((t["verdict"], t["scores"]), ("pivot", {"wow": 4}))
            self.assertEqual([f["severity"] for f in t["findings"]], ["major"])  # minor left out
            self.assertEqual(t["link_checks"], [{"url": "https://x.com", "status": "not_found"}])
            self.assertEqual(data["labels"]["criteria"]["wow"], "Wow factor")

    def test_empty_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = build.collect(Path(tmp))
            self.assertEqual((data["runs"], data["transcripts"]), ([], {}))

    def test_build_copies_static_and_writes_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = build.build(Path(tmp) / "site", demo=True)
            self.assertEqual(sorted(p.name for p in out.iterdir()), ["app.js", "data.json", "index.html", "style.css"])
            data = json.loads((out / "data.json").read_text())
            self.assertTrue(data["demo"])
            self.assertEqual(set(data["transcripts"]["sample-newsletter"]["scores"]), set(data["labels"]["criteria"]))

    def test_page_inserts_data_as_text(self):
        js = (build.STATIC / "app.js").read_text()
        # innerHTML appears only in the header comment and the DOMPurify-sanitized PRD viewer.
        self.assertEqual(js.count("innerHTML"), 2)
        self.assertIn("box.innerHTML = window.DOMPurify.sanitize(", js)


class ServeTests(unittest.TestCase):
    def test_rebuilds_on_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            watched = Path(tmp) / "watched"
            watched.mkdir()
            (watched / "a.json").write_text("{}")
            site = serve.Site(Path(tmp) / "site", demo=True, watch=[watched])
            self.assertEqual(site.version, 1)
            self.assertFalse(site.rebuild_if_changed())
            later = time.time() + 5
            os.utime(watched / "a.json", (later, later))
            self.assertTrue(site.rebuild_if_changed())
            self.assertEqual(site.version, 2)

    def test_version_endpoint_and_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = serve.Site(Path(tmp) / "site", demo=True, watch=[])
            server = serve.make_server(site, 0)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            self.addCleanup(server.server_close)
            self.addCleanup(server.shutdown)
            port = server.server_address[1]
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/__version") as r:
                self.assertEqual(r.read(), b"1")
                self.assertEqual(r.headers["Cache-Control"], "no-store")
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/data.json") as r:
                self.assertTrue(json.loads(r.read())["demo"])


if __name__ == "__main__":
    unittest.main()
