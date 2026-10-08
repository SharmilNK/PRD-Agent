"""Local dashboard with live reload: every change shows up on the page by itself.

Watches data/metrics, data/outputs, data/decisions and the dashboard's own files. When any file
changes, it rebuilds the site and bumps a version number; the open page notices within ~2 seconds
and redraws. Standard library only.

Usage:
    python -m apps.dashboard.serve            # http://localhost:8000
    python -m apps.dashboard.serve --demo     # sample data (clearly labelled)
    python -m apps.dashboard.serve --port 8080
"""

from __future__ import annotations

import argparse
import functools
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from apps.dashboard.build import REPO_ROOT, STATIC, build

WATCH = [REPO_ROOT / "data" / "metrics", REPO_ROOT / "data" / "outputs", REPO_ROOT / "data" / "decisions", STATIC]


def snapshot(paths: list[Path]) -> dict[str, float]:
    """File path -> last modified time, for every file under the watched folders."""
    seen = {}
    for root in paths:
        if root.exists():
            for f in root.rglob("*"):
                if f.is_file():
                    try:
                        seen[str(f)] = f.stat().st_mtime
                    except OSError:
                        pass  # file vanished between listing and reading
    return seen


class Site:
    """The built site plus a version number that changes on every rebuild."""

    def __init__(self, out: Path, demo: bool, watch: list[Path] = WATCH):
        self.out, self.demo, self.watch = out, demo, watch
        # Always build once at start, even if the watched folders are empty (no runs yet).
        self._last = snapshot(self.watch)
        build(self.out, demo=self.demo)
        self.version = 1

    def rebuild_if_changed(self) -> bool:
        now = snapshot(self.watch)
        if now == self._last:
            return False
        self._last = now
        build(self.out, demo=self.demo)
        self.version += 1
        return True

    def loop(self, interval: float = 1.0) -> None:
        while True:
            time.sleep(interval)
            try:
                if self.rebuild_if_changed():
                    print(f"Change detected - rebuilt (version {self.version})")
            except Exception as e:  # noqa: BLE001 - a half-written file must not stop the server
                print(f"Rebuild failed, will retry: {e}")


class Handler(SimpleHTTPRequestHandler):
    site: Site

    def do_GET(self):
        if self.path.split("?")[0] == "/__version":
            body = str(self.site.version).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):  # keep the terminal quiet
        pass


def make_server(site: Site, port: int) -> ThreadingHTTPServer:
    handler = type("SiteHandler", (Handler,), {"site": site})
    return ThreadingHTTPServer(("127.0.0.1", port), functools.partial(handler, directory=str(site.out)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the dashboard locally with live reload")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--demo", action="store_true", help="use clearly labelled sample data")
    args = parser.parse_args(argv)
    site = Site(Path(tempfile.mkdtemp(prefix="prd-dashboard-")), args.demo)
    threading.Thread(target=site.loop, daemon=True).start()
    server = make_server(site, args.port)
    print(f"Dashboard: http://localhost:{args.port}  (live reload on; Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
