"""Checks the quiz page ships one layout with no video, whatever the URL says.

WHY (Greg, 2026-11-20): the Variant-B layout test was killed and there is no
video on the quiz. Before this, ?qv=b still opened Variant B, and the normal
page still started downloading its two hidden phone videos from
raw.githubusercontent.com (banned on the quiz: rural-mobile buyers).

Every request that is not for this site is aborted and recorded, so no test
data leaves the machine.
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


class OneLayoutNoVideo(unittest.TestCase):
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

    def load(self, path):
        """Open the page; return (page, every URL it asked for)."""
        ctx = self.browser.new_context()
        self.addCleanup(ctx.close)
        page = ctx.new_page()
        asked = []

        def route(r):
            asked.append(r.request.url)
            return r.continue_() if r.request.url.startswith(self.base) else r.abort()

        page.route("**/*", route)
        page.goto(f"{self.base}{path}", wait_until="load")
        page.wait_for_function("typeof window.__gbAttribution === 'function'")
        return page, asked

    def layout(self, page):
        return page.evaluate(
            "({variant: document.documentElement.dataset.variant,"
            " label: window.__quizVariant,"
            " variantB: document.querySelectorAll('.v-b').length,"
            " videos: document.querySelectorAll('video').length,"
            " forms: Array.prototype.map.call(document.querySelectorAll('[data-tf-widget]'),"
            "   function (w) { return w.id + ':' + w.getAttribute('data-tf-widget'); })})"
        )

    def test_every_address_gets_the_same_one_layout(self):
        want = {
            "variant": "a",
            "label": "a",
            "variantB": 0,
            "videos": 0,
            "forms": ["tf-gb-widget:sTbsRn"],
        }
        for path in ("/quiz/", "/quiz/?qv=b", "/quiz/?qv=a", "/quiz/?utm_source=google&gclid=G1"):
            with self.subTest(path=path):
                page, _ = self.load(path)
                self.assertEqual(self.layout(page), want)

    def test_page_asks_for_no_video_and_nothing_from_raw_github(self):
        for path in ("/quiz/", "/quiz/?qv=b"):
            with self.subTest(path=path):
                _, asked = self.load(path)
                bad = [
                    u for u in asked
                    if "raw.githubusercontent.com" in u
                    or u.split("?")[0].lower().endswith((".mp4", ".webm", ".mov", ".m4v"))
                ]
                self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
