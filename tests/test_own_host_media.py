"""Checks the /approved award logo loads from this site.

WHY (Greg, 2026-11-19): raw.githubusercontent.com is banned on the quiz. The
buyers are on slow rural mobile connections, same as www. The logo used to
be hot-linked from there; it now lives in assets/.

Every request that is not for this site is aborted, so a hot-linked file
cannot load here and no test data leaves the machine.
Run: scripts/run-tests
"""
import functools
import http.server
import threading
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class OwnHostMedia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(Quiet, directory=str(ROOT))
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()

    def test_approved_award_logo_loads_from_this_site(self):
        ctx = self.browser.new_context()
        self.addCleanup(ctx.close)
        page = ctx.new_page()
        page.route(
            "**/*",
            lambda r: r.continue_() if r.request.url.startswith(self.base) else r.abort(),
        )
        page.goto(f"{self.base}/approved/")
        page.locator(".award-strip img").scroll_into_view_if_needed()
        page.wait_for_function(
            "(function(){var i=document.querySelector('.award-strip img');"
            "return !!(i&&i.complete&&i.naturalWidth>0);})()"
        )
        self.assertEqual(
            page.evaluate("document.querySelector('.award-strip img').currentSrc"),
            f"{self.base}/assets/oil-and-gas-awards-finalist.jpg",
        )


if __name__ == "__main__":
    unittest.main()
