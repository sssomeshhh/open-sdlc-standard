# SPDX-License-Identifier: MIT
"""Regression tests for tools/check_structure.py and tools/check_citations.py.

Run: python3 -m unittest discover -s tools/tests
Standard library only; no network access (the HTTP tests use local servers on 127.0.0.1).
"""
import contextlib
import http.server
import io
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import check_citations as cc  # noqa: E402
import check_structure as cs  # noqa: E402


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class Manual(unittest.TestCase):
    """Records of checks done by hand: keyed by the quote text, valid 12 months, never cover a MISMATCH."""

    def test_status_and_expiry(self):
        import datetime
        rec = {"checked": "2026-01-01"}
        self.assertEqual(cc.manual_status(rec, datetime.date(2026, 6, 1))[0], "valid")
        self.assertEqual(cc.manual_status(rec, datetime.date(2026, 12, 15))[0], "due")
        self.assertEqual(cc.manual_status(rec, datetime.date(2027, 1, 2))[0], "expired")

    def test_hash_follows_the_quote_text(self):
        self.assertEqual(cc.quote_hash("A  quote."), cc.quote_hash("A quote."))
        self.assertNotEqual(cc.quote_hash("A quote."), cc.quote_hash("A changed quote."))

    def test_fingerprint_option_matches_quote_hash(self):
        r = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "check_citations.py"), "--fingerprint", "A quote."],
                           capture_output=True, text=True, check=True)
        self.assertEqual(r.stdout.strip(), cc.quote_hash("A quote."))

    def test_loose_never_joins_digits(self):
        tn = cc.normalise("Rotate keys every 2*3 hours.")
        self.assertIsNone(cc.match("Rotate keys every 23 hours.", tn, cc.loose(tn)))


class Matching(unittest.TestCase):
    SRC = ("Backups are kept for 35 years. Access is reviewed monthly. The data is not encrypted at rest. "
           "infor-\nmation security (see the guide) is key , really.")

    def m(self, quote):
        tn = cc.normalise(self.SRC)
        return cc.match(quote, tn, cc.loose(tn))

    def test_exact_and_loose(self):
        self.assertEqual(self.m("Backups are kept for 35 years."), "exact")
        self.assertEqual(self.m("information security (see the guide) is key, really."), "loose")

    def test_numbers_are_not_joined_or_split(self):
        self.assertIsNone(self.m("Backups are kept for 3-5 years."))
        self.assertIsNone(self.m("Backups are kept for 3 5 years."))

    def test_empty_quotes_never_match(self):
        self.assertIsNone(self.m(""))
        self.assertIsNone(self.m("..."))

    def test_ellipsis_cannot_hide_a_negation_or_reorder(self):
        self.assertIsNone(self.m("The data is … encrypted at rest."))       # fragment too short
        self.assertIsNone(self.m("Access is reviewed … Backups are kept"))  # out of order
        self.assertEqual(self.m("Access is reviewed monthly. … The data is not encrypted at rest."), "exact")

    def test_ellipsis_cannot_skip_a_negation_or_a_long_stretch(self):
        src = ("Teams that deploy often should not, under any circumstances, rely on manual testing for every change. "
               + "Filler sentence here. " * 30 + "Every release has a named owner and a written rollback plan.")
        tn = cc.normalise(src)
        how, gaps = cc.match_detail("Teams that deploy often should \u2026 rely on manual testing for every change.",
                                    tn, cc.loose(tn))
        self.assertEqual(cc.gap_problem(gaps)[0], "MISMATCH")
        how, gaps = cc.match_detail("rely on manual testing for every change. \u2026 Every release has a named owner",
                                    tn, cc.loose(tn))
        self.assertEqual(cc.gap_problem(gaps)[0], "UNVERIFIED")
        how, gaps = cc.match_detail("Filler sentence here. \u2026 Every release has a named owner", tn, cc.loose(tn))
        self.assertIsNone(cc.gap_problem(gaps))

    def test_pdf_layout_fallback_rejects_dropped_negation(self):
        self.assertFalse(cc.in_order_with_gaps("The data is encrypted at rest", self.SRC))
        self.assertTrue(cc.in_order_with_gaps("to promote content provenance, including sources",
                                              "to promote content and Component Integration; provenance, including sources"))


class Spacing(unittest.TestCase):
    def test_inline_tags_leading_dots_and_cjk(self):
        html_src = ("<p>Commit <code>.claude/settings.json</code> so everyone gets it. ISO/<wbr>IEC 40500. "
                    "\u6539\u6b63JIS\u306f\u3001\nJIS X 8341-3</p>")
        t = cc.to_text(html_src.encode(), "text/html")
        tn = cc.normalise(t)
        for q in ["Commit `.claude/settings.json` so everyone gets it.", "ISO/IEC 40500.",
                  "\u6539\u6b63JIS\u306f\u3001JIS X 8341-3"]:
            self.assertIsNotNone(cc.match(q, tn, cc.loose(tn)), q)
        tn = cc.normalise("each paragraph: (i)the businesses handling it")
        self.assertIsNotNone(cc.match("(i) the businesses handling it", tn, cc.loose(tn)))


class Parsing(unittest.TestCase):
    def parse(self, body):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# 1. X\n\n## References\n\n" + body)
        try:
            return cc.parse_references(f.name)
        finally:
            os.unlink(f.name)

    def test_note_with_quotes_and_multiline_are_reported(self):
        e = self.parse('- **[K]** T. https://example.org/. Accessed 2026-10-31.\n'
                       '  > "One." (the "Overview" section)\n'
                       '  > "starts here\n  > and continues."\n'
                       '  > "Fine." (a note)\n')[0]
        self.assertEqual([q for _, q in e["quotes"]], ["Fine."])
        self.assertEqual(len(e["bad"]), 3)


class Http(unittest.TestCase):
    """Local servers: A redirects /page to B/secret; B's robots.txt disallows everything."""

    def setUp(self):
        self.servers = []

        def serve(handler):
            srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            self.servers.append(srv)
            return f"http://127.0.0.1:{srv.server_address[1]}"

        class B(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                body = b"User-agent: *\nDisallow: /\n" if self.path == "/robots.txt" else b"<html>secret</html>"
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body)

        self.b = serve(B)
        b = self.b

        class A(http.server.BaseHTTPRequestHandler):
            hits = 0

            def log_message(self, *a):
                pass

            def do_GET(self):
                if self.path == "/robots.txt":
                    self.send_response(404)
                    self.end_headers()
                elif self.path == "/page":
                    self.send_response(302)
                    self.send_header("Location", b + "/secret")
                    self.end_headers()
                else:
                    A.hits += 1
                    self.send_response(403)
                    self.end_headers()

        self.A = A
        self.a = serve(A)
        self._pause = cc.HOST_PAUSE
        cc.HOST_PAUSE = 0

    def tearDown(self):
        cc.HOST_PAUSE = self._pause
        for s in self.servers:
            s.shutdown()
            s.server_close()

    def test_redirect_to_disallowed_url_is_refused(self):
        with self.assertRaises(RuntimeError) as ctx:
            cc.Fetcher().get(self.a + "/page")
        self.assertIn("robots.txt", str(ctx.exception))

    def test_failures_are_fetched_once(self):
        f = cc.Fetcher()
        for _ in range(3):
            with self.assertRaises(RuntimeError):
                f.get(self.a + "/blocked")
        self.assertEqual(self.A.hits, 1)

    def test_one_failed_source_gives_unverified_not_mismatch(self):
        f = cc.Fetcher()
        f.cache[(self.a + "/ok", "{}")] = (b"<html>" + b"x " * 400 + b"present text here</html>", "text/html")
        e = {"urls": [self.a + "/ok", self.a + "/blocked"]}
        out = cc.check_entry(f, e, [(1, "the quote is on the blocked page")])
        self.assertEqual(out[0][2], "UNVERIFIED")


class ChangedLines(unittest.TestCase):
    def test_diff_parsing_survives_git_config(self):
        d = tempfile.mkdtemp()
        try:
            run = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True)  # noqa: E731
            run("init", "-q")
            os.makedirs(os.path.join(d, "areas"))
            p = os.path.join(d, "areas", "01-x.md")
            write(p, "a\nb\n")
            run("add", ".")
            run("-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "x")
            write(p, "a\nb\nc\n")
            for cfg in ([], ["diff.mnemonicPrefix", "true"], ["diff.noprefix", "true"], ["color.diff", "always"]):
                if cfg:
                    run("config", *cfg)
                self.assertEqual(cc.changed_lines(d, "HEAD"), {"areas/01-x.md": {3}}, cfg)
        finally:
            shutil.rmtree(d)


class Structure(unittest.TestCase):
    """Each mutation of a copy of the repository must make check_structure fail."""

    def run_on(self, mutate):
        d = tempfile.mkdtemp()
        try:
            for name in ("areas", "docs", ".github"):
                shutil.copytree(os.path.join(ROOT, name), os.path.join(d, name))
            for name in ("README.md", "CHANGELOG.md", "NOTICE.md", "LICENSE", "LICENSE-CODE", ".gitignore", "VERSION"):
                shutil.copy(os.path.join(ROOT, name), d)
            mutate(d)
            old = sys.argv
            sys.argv = ["check_structure.py", d]
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    rc = cs.main()
            finally:
                sys.argv = old
            return rc, buf.getvalue()
        finally:
            shutil.rmtree(d)

    @staticmethod
    def edit(d, rel, old, new):
        p = os.path.join(d, rel)
        s = cs.read_text(p)
        assert old in s, old
        write(p, s.replace(old, new, 1))

    A7 = "areas/07-source-control-and-repository-hygiene.md"

    def test_unchanged_copy_passes(self):
        self.assertEqual(self.run_on(lambda d: None)[0], 0)

    def test_references_out_of_order_fail(self):
        def swap(d):
            # Swap two keys everywhere in the file: both stay defined and cited, only their order is wrong.
            p = os.path.join(d, self.A7)
            s = cs.read_text(p).replace("[DORA-TBD]", "[@@]").replace("[FOWLER-CI]", "[DORA-TBD]").replace("[@@]", "[FOWLER-CI]")
            write(p, s)
        rc, out = self.run_on(swap)
        self.assertEqual(rc, 1, out)
        self.assertIn("alphabetical order", out)
        self.assertIn("1 problem(s) found", out)

    def test_reference_sort_key(self):
        def ordered(*keys):
            return list(keys) == sorted(keys, key=cs.ref_sort_key)
        self.assertTrue(ordered("12F-2", "12F-10", "12F-12"))
        self.assertTrue(ordered("RFC3339", "RFC8259", "RFC9110", "RFC9557"))
        self.assertTrue(ordered("AWS-OPS05-04", "AWS-OPS06-01", "AWS-REL08-04", "AWS-REL13-04"))
        self.assertTrue(ordered("SRE-ONCALL", "SREW-ONCALL"))
        self.assertTrue(ordered("gdpr-x", "GOVUK-P10"))
        self.assertTrue(ordered("OPS05", "OPS5"))
        self.assertFalse(ordered("12F-10", "12F-2"))

    def test_mutations_fail(self):
        cases = {
            "level mismatch": lambda d: self.edit(d, self.A7, "### SCM-6 · MUST", "### SCM-6 · SHOULD"),
            "bad gate": lambda d: self.edit(d, self.A7, "- **Gate:** G1", "- **Gate:** G7"),
            "trigger before condition": lambda d: self.edit(
                d, self.A7, "- **Gate:** G1", "- **Gate:** G1 · **Trigger:** x · **Condition:** y"),
            "keyword in code span only": lambda d: self.edit(
                d, self.A7, "Every pull request to a protected branch MUST be merged",
                "Every pull request to a protected branch (see `MUST`) is merged"),
            "keyword glued to underscore": lambda d: self.edit(
                d, self.A7, "Every pull request to a protected branch MUST be merged",
                "Every pull request to a protected branch MUST_PR is merged"),
            "requirement in failure modes": lambda d: self.edit(
                d, self.A7, "## Failure modes\n", "## Failure modes\n\n### SCM-99 · MUST · Hidden\n"),
            "duplicate prefix": lambda d: self.edit(
                d, "areas/08-continuous-integration.md", "- **ID prefix:** CI", "- **ID prefix:** SCM"),
            "undefined key in text": lambda d: self.edit(d, self.A7, "## Failure modes\n", "## Failure modes\n\n[NOPE-REF]\n"),
            "leading zero id": lambda d: self.edit(d, self.A7, "### SCM-1 ·", "### SCM-01 ·"),
            "count by substring": lambda d: self.edit(d, "CHANGELOG.md", "- 20 areas", "- 120 areas"),
            "link leaves repo": lambda d: self.edit(d, "README.md", "## Areas", "[x](../../../../etc/hosts)\n\n## Areas"),
        }
        for name, mutate in cases.items():
            with self.subTest(name):
                rc, out = self.run_on(mutate)
                self.assertEqual(rc, 1, out)


if __name__ == "__main__":
    unittest.main()
