#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check that quotes in the areas' References match their live sources, word for word.

Usage:
  python3 tools/check_citations.py --all                 check every quote
  python3 tools/check_citations.py --changed <git-ref>   check only quotes added or changed since <git-ref>
  python3 tools/check_citations.py --fingerprint "<quote>"   print a quote's fingerprint for a check done by hand
  options: --report <file>   also write a Markdown report
           --manual <file>   record of checks done by hand (default: docs/sdlc/manual-citation-checks.json)

Each quote ends in one of four results:
  OK            the quote was found, in order, in the text of one of its sources
  MISMATCH      every source of the entry was read, and the quote is not in any of them (or the quote is malformed)
  UNVERIFIED    a source could not be read automatically (refused, blocked by robots.txt, unavailable, too little
                text, or a PDF without pdftotext installed), or a PDF table layout hides the match; a person checks it
  MANUAL        UNVERIFIED, but covered by a current record of a check done by hand (same quote text, under 12 months)

Exit status: 1 if any quote is a MISMATCH, otherwise 0. UNVERIFIED and MANUAL never fail the run.

Fetching rules: one honest User-Agent that names this tool, robots.txt is respected (also for every redirect), a pause
between requests to the same host (also for robots.txt), one attempt per URL (failures are remembered), and no
workaround when a site refuses. Uses only the Python standard library, plus the pdftotext program (poppler-utils) for
PDF sources when it is installed.
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser

def _read_version():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION")
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "unknown"


VERSION = _read_version()  # one version for the standard and its tools
USER_AGENT = f"open-sdlc-standard-citecheck/{VERSION} (+https://github.com/sssomeshhh/open-sdlc-standard)"
TIMEOUT = 30
HOST_PAUSE = 2.0
MIN_TEXT = 500           # fewer normalised characters than this is treated as an unreadable page
MIN_FRAGMENT_WORDS = 4   # each part of a quote cut with an ellipsis must be at least this long
MANUAL_VALID_DAYS = 365  # a check done by hand covers a quote for at most 12 months
MANUAL_DUE_DAYS = 30     # report records that expire within this many days

REF_RE = re.compile(r"^- \*\*\[([^\]]+)\]\*\*\s*(.*)$")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
# A quote line: > "text" with an optional parenthesised note after it. Anything else starting with '>' is an error.
QUOTE_RE = re.compile(r'^\s*>\s*"(.*)"(\s*\([^"]*\)\.?)?\s*$')
NEGATIONS = {"not", "no", "never", "none", "nor", "except", "without", "neither", "cannot", "unless"}
MAX_ELLIPSIS_GAP = 300  # characters an ellipsis may skip before a person must check the cut

# Supplementary sources: the full text behind a landing page that the reference cites.
SUPPLEMENTARY = {
    "https://csrc.nist.gov/pubs/sp/800/218/final":
        "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf",
    "https://csrc.nist.gov/pubs/sp/800/92/r1/ipd":
        "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-92r1.ipd.pdf",
    "https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final":
        "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1-upd1.pdf",
    "https://csrc.nist.gov/pubs/ir/8286/r1/final":
        "https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8286r1.pdf",
}


# ---------------------------------------------------------------- parsing


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def parse_references(path) -> list:
    """Return the References entries of one area file.

    Each entry: key, line, urls, quotes [(line, text)], bad [(line, reason)], lines (citation lines, for --changed).
    """
    lines = read_text(path).split("\n")
    entries, cur, in_refs = [], None, False
    for i, ln in enumerate(lines, 1):
        if ln.startswith("## "):
            in_refs = ln.strip() == "## References"
            cur = None
            continue
        if not in_refs:
            continue
        m = REF_RE.match(ln)
        if m:
            cur = {"key": m.group(1), "line": i, "desc": m.group(2), "quotes": [], "bad": [], "lines": {i}}
            entries.append(cur)
            continue
        if cur is None:
            continue
        if ln.lstrip().startswith(">"):
            q = QUOTE_RE.match(ln)
            if q:
                cur["quotes"].append((i, q.group(1)))
            else:
                cur["bad"].append((i, "quote line is not '> \"text\"' with an optional '(note)'"))
        elif ln.strip():
            cur["desc"] += " " + ln.strip()
            cur["lines"].add(i)
    for e in entries:
        e["urls"] = list(dict.fromkeys(u.rstrip(".,;") for u in URL_RE.findall(e["desc"])))
    return entries


def changed_lines(root, base):
    """Map area file -> set of line numbers added or changed since base (git diff, zero context)."""
    cmd = ["git", "-C", root, "diff", "--unified=0", "--no-color", "--no-ext-diff", "--no-renames",
           "--src-prefix=a/", "--dst-prefix=b/", base, "--", "areas"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"check_citations: git diff against '{base}' failed ({r.stderr.strip()}); "
                 f"is the ref fetched? try: git fetch origin")
    changed, cur = {}, None
    for ln in r.stdout.split("\n"):
        if ln.startswith("+++ "):
            cur = ln[6:] if ln.startswith("+++ b/") else None
        elif ln.startswith("@@") and cur:
            m = re.search(r"\+(\d+)(?:,(\d+))?", ln)
            if not m:
                continue
            start, count = int(m.group(1)), int(m.group(2) or "1")
            changed.setdefault(cur, set()).update(range(start, start + count))
    return changed


# ---------------------------------------------------------------- fetching

class Fetcher:
    def __init__(self):
        self.last = {}
        self.robots = {}
        self.robots_error = {}  # base URL -> why robots.txt could not be read
        self.cache = {}  # (url, headers) -> (bytes, ctype) or RuntimeError
        self.texts = {}  # source URL -> [(label, text, is_pdf)] or the exception it raised (extracted once)
        self.norms = {}  # label -> (normalised text, loose text) (computed once)
        fetcher = self

        class Redirects(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                if not fetcher.allowed(newurl):
                    raise RuntimeError(f"redirect to {newurl}, which robots.txt does not allow (or cannot be read)")
                fetcher.pause(newurl)
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        self.opener = urllib.request.build_opener(Redirects)

    def pause(self, url):
        host = urllib.parse.urlsplit(url).netloc
        wait = HOST_PAUSE - (time.time() - self.last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        self.last[host] = time.time()

    def allowed(self, url):
        parts = urllib.parse.urlsplit(url)
        base = f"{parts.scheme}://{parts.netloc}"
        if base not in self.robots:
            rp = urllib.robotparser.RobotFileParser()
            self.pause(base)
            try:
                req = urllib.request.Request(base + "/robots.txt", headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                    rp.parse(r.read().decode("utf-8", "replace").splitlines())
            except urllib.error.HTTPError as e:
                e.close()
                # 404/410: no robots.txt, so no restrictions. Other errors (including 401/403, which RFC 9309 would
                # let a crawler treat as unrestricted): this tool is stricter and treats the site as unreadable.
                if e.code in (404, 410):
                    rp.parse([])
                else:
                    rp, self.robots_error[base] = None, f"HTTP {e.code}"
            except Exception as e:
                rp, self.robots_error[base] = None, type(e).__name__
            self.robots[base] = rp
        rp = self.robots[base]
        return rp is not None and rp.can_fetch(USER_AGENT, url)

    def get(self, url, headers=None):
        """Return (bytes, content type), or raise RuntimeError with the reason the source is unreadable."""
        key = (url, json.dumps(headers or {}, sort_keys=True))
        if key in self.cache:
            hit = self.cache[key]
            if isinstance(hit, RuntimeError):
                raise hit
            return hit
        try:
            if not self.allowed(url):
                parts = urllib.parse.urlsplit(url)
                base = f"{parts.scheme}://{parts.netloc}"
                if base in self.robots_error:
                    raise RuntimeError(f"robots.txt for {parts.netloc} could not be read ({self.robots_error[base]})")
                raise RuntimeError(f"robots.txt for {parts.netloc} does not allow it")
            self.pause(url)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
            try:
                with self.opener.open(req, timeout=TIMEOUT) as r:
                    result = (r.read(), r.headers.get("Content-Type", ""))
            except urllib.error.HTTPError as e:
                e.close()
                raise RuntimeError(f"HTTP {e.code}")
            except RuntimeError:
                raise
            except Exception as e:  # network errors, timeouts
                raise RuntimeError(type(e).__name__)
        except RuntimeError as err:
            self.cache[key] = err
            raise
        self.cache[key] = result
        return result


def _read(fetched):
    raw, ctype = fetched
    return to_text(raw, ctype), (raw[:5] == b"%PDF-" or "pdf" in (ctype or "").lower())


def source_texts(fetcher, url):
    """Return [(label, text, is_pdf)] for a source URL, following the special routes some sources need."""
    out = []
    if url == "http://publications.europa.eu/resource/celex/32016R0679":
        out.append((url,) + _read(fetcher.get(url, {"Accept": "application/xhtml+xml", "Accept-Language": "eng"})))
    elif url.startswith("https://laws.e-gov.go.jp/law/"):
        law_id = url.rstrip("/").split("/")[-1]
        out.append((url,) + _read(fetcher.get("https://laws.e-gov.go.jp/api/2/law_data/" + law_id)))
    elif re.match(r"^https://github\.com/[^/]+/[^/]+/tree/", url):
        parts = url.rstrip("/").split("/")
        if len(parts) < 8:
            raise RuntimeError("GitHub tree URL has no folder path")
        owner, repo, ref, path = parts[3], parts[4], parts[6], "/".join(parts[7:])
        api = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
        listing = json.loads(fetcher.get(api)[0].decode("utf-8"))
        if not isinstance(listing, list):
            raise RuntimeError("GitHub tree URL is not a folder")
        for item in listing:
            if isinstance(item, dict) and item.get("type") == "file" and str(item.get("name", "")).endswith(".md"):
                out.append(_try_read(fetcher, item["download_url"]))
    else:
        out.append((url,) + _read(fetcher.get(url)))
    if url in SUPPLEMENTARY:
        out.append(_try_read(fetcher, SUPPLEMENTARY[url]))
    return out


def _try_read(fetcher, url):
    """An extra file of a source: on failure return (url, None, reason) so the source's other text is still used."""
    try:
        return (url,) + _read(fetcher.get(url))
    except Exception as err:
        return (url, None, str(err))


# ---------------------------------------------------------------- text extraction

class _Strip(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "template"}
    # Inline elements do not separate words: "ISO/<wbr>IEC" and "<code>.claude</code>" keep their spacing as written.
    INLINE = {"a", "abbr", "b", "bdi", "bdo", "cite", "code", "data", "dfn", "em", "i", "kbd", "mark", "q", "rp", "rt",
              "ruby", "s", "samp", "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag == "meta":
            self.out.extend(" " + v + " " for k, v in attrs if k == "content" and v)
        if tag not in self.INLINE:
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag not in self.INLINE:
            self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def _decode(raw, ctype):
    names = re.findall(r"charset=([\w\-]+)", ctype or "", re.I)
    names += [m.decode() for m in re.findall(rb'charset=["\']?([\w\-]+)', raw[:3000], re.I)]
    for name in names + ["utf-8", "cp932"]:
        name = {"shift_jis": "cp932", "x-sjis": "cp932"}.get(name.lower(), name)
        try:
            return raw.decode(name)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", "replace")


def _json_strings(o, acc):
    if isinstance(o, str):
        acc.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            _json_strings(v, acc)
    elif isinstance(o, list):
        for v in o:
            _json_strings(v, acc)


def to_text(raw, ctype):
    ctype = (ctype or "").lower()
    if raw[:5] == b"%PDF-" or "pdf" in ctype:
        if not shutil.which("pdftotext"):
            raise RuntimeError("PDF source, and pdftotext is not installed")
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-", "-"], input=raw, capture_output=True)
        return r.stdout.decode("utf-8", "replace")
    if "json" in ctype or raw.lstrip()[:1] in (b"{", b"["):
        try:
            acc = []
            _json_strings(json.loads(raw.decode("utf-8")), acc)
            parts = []
            for s in acc:  # JSON strings may carry markup; strip it, and keep fields apart with a paragraph break
                if "<" in s:
                    p = _Strip()
                    p.feed(s)
                    s = "".join(p.out)
                parts.append(s)
            return "\n\u2029\n".join(parts)
        except ValueError:
            pass
    if "html" in ctype or "xml" in ctype or b"<html" in raw[:5000].lower():
        s = _Strip()
        s.feed(_decode(raw, ctype))
        return "".join(s.out)
    return _decode(raw, ctype)


# ---------------------------------------------------------------- matching

_CJK = r"[\u3000-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]"
_CHARMAP = {"\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'", "\u00a0": " ", "\u00ad": "",
            "\u200b": "", "\u2010": "-", "\u2011": "-", "\ufeff": ""}


def normalise(s, unescape=False):
    """Compare text, not layout: NFKC, straight quotes, whitespace runs collapsed to one space, no space before
    closing punctuation or after an opening bracket. Words are never joined. Source text is already unescaped by the
    HTML parser; quotes written in Markdown are unescaped here (unescape=True)."""
    if unescape:
        s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    for a, b in _CHARMAP.items():
        s = s.replace(a, b)
    s = re.sub(r"[ \t\r\n\f\v]+", " ", s)
    s = re.sub(r" ([,.;:!?])(?=\s|$)", r"\1", s)  # " ," becomes ","; a leading dot as in " .claude" stays
    s = re.sub(r" ([)\]])", r"\1", s)
    s = re.sub(r"([)\]]) (?=\w)", r"\1", s)  # list markers: "(i) the" and "(i)the" compare equal
    s = re.sub(rf"(?<={_CJK}) | (?={_CJK})", "", s)  # no word spaces around CJK text
    s = re.sub(r"([(\[]) ", r"\1", s)
    return s.strip()


_LETTER = r"[^\W\d_]"


def loose(s):
    """Also ignore Markdown emphasis, dashes between letters and hyphenation at a line break (letter-dash-space-letter).
    Never touches a dash next to a digit, so '3-5' and '35' stay different."""
    s = re.sub(r"(?<!\d)[*_`]|[*_`](?!\d)", "", s)  # emphasis markers, but "2*3" never becomes "23"
    s = re.sub(rf"(?<={_LETTER})[-\u2013\u2014] ?(?={_LETTER})", "", s)
    return s


def fragments(quote):
    """A quote may cut text with an ellipsis; the parts are returned in order."""
    parts = re.split(r"\s*(?:\u2026|\.\.\.|\[\u2026\]|\[\.\.\.\])\s*", quote.replace("\\", ""))
    return [p for p in parts if normalise(p, unescape=True)]


def match_detail(quote, text_n, text_l):
    """Return (how, gaps): how is 'exact', 'loose' or None; gaps are the source texts an ellipsis skipped.
    Fragments must appear in order, each after the previous one."""
    frags = fragments(quote)
    if not frags:
        return None, []
    if len(frags) > 1 and any(len(f.split()) < MIN_FRAGMENT_WORDS for f in frags):
        return None, []
    how, pos_n, pos_l, gaps = "exact", 0, 0, []
    for k, frag in enumerate(frags):
        f = normalise(frag, unescape=True)
        i = text_n.find(f, pos_n)
        if i >= 0 and how == "exact":
            if k:
                gaps.append(text_n[pos_n:i])
            pos_n = i + len(f)
            continue
        fl = loose(f)
        j = text_l.find(fl, pos_l) if fl else -1
        if j < 0:
            return None, []
        if k:
            gaps.append(text_l[pos_l:j])
        how, pos_l = "loose", j + len(fl)
    return how, gaps


def match(quote, text_n, text_l):
    """Return 'exact', 'loose', or None."""
    return match_detail(quote, text_n, text_l)[0]


def gap_problem(gaps):
    """Why an ellipsis cut needs attention: ('MISMATCH', reason), ('UNVERIFIED', reason) or None."""
    for g in gaps:
        if NEGATIONS & set(_words(g)):
            return "MISMATCH", "the text cut by an ellipsis contains a negation; quote the full sentence or cut elsewhere"
    if any(len(g) > MAX_ELLIPSIS_GAP for g in gaps):
        return "UNVERIFIED", "the parts of this quote are far apart in the source; check the cut by hand"
    return None


def _words(s):
    return re.findall(r"\w+", unicodedata.normalize("NFKC", html.unescape(s)).lower())


def in_order_with_gaps(quote, text, max_extra=8):
    """True if the quote's words appear in order in text with at most max_extra other words between them in total,
    none of which is a negation. Used only to explain a PDF table whose columns pdftotext interleaves; never OK."""
    q = _words(quote)
    if not q:
        return False
    t = _words(text)
    for start in (i for i, w in enumerate(t) if w == q[0]):
        k, extra, j, bad = 1, 0, start + 1, False
        while k < len(q) and j < len(t) and extra <= max_extra:
            if t[j] == q[k]:
                k += 1
            else:
                extra += 1
                bad = bad or t[j] in NEGATIONS
            j += 1
        if k == len(q) and extra <= max_extra and not bad:
            return True
    return False


# ---------------------------------------------------------------- record of checks done by hand

def quote_hash(quote):
    return hashlib.sha256(normalise(quote, unescape=True).encode("utf-8")).hexdigest()


def load_manual(path):
    if not path or not os.path.exists(path):
        return {}
    data = json.loads(read_text(path))
    return {(r["key"], r["sha256"]): r for r in data.get("checks", [])}


def manual_status(record, today):
    """Return ('valid'|'due'|'expired', expiry date) for a record."""
    checked = datetime.date.fromisoformat(record["checked"])
    expires = checked + datetime.timedelta(days=MANUAL_VALID_DAYS)
    if today >= expires:
        return "expired", expires
    if (expires - today).days <= MANUAL_DUE_DAYS:
        return "due", expires
    return "valid", expires


# ---------------------------------------------------------------- main

def cached_source_texts(fetcher, url):
    """source_texts, extracted once per URL (a PDF cited by several entries is converted only once)."""
    if url not in fetcher.texts:
        try:
            fetcher.texts[url] = source_texts(fetcher, url)
        except Exception as err:  # remembered, so a failing source is not retried for the next entry
            fetcher.texts[url] = err
    hit = fetcher.texts[url]
    if isinstance(hit, Exception):
        raise hit
    return hit


def normalised(fetcher, label, text):
    """(normalised, loose) text for a source, computed once per source."""
    if label not in fetcher.norms:
        tn = normalise(text)
        fetcher.norms[label] = (tn, loose(tn))
    return fetcher.norms[label]


def check_entry(fetcher, e, quotes):
    """Check one entry's quotes; return [(line, quote, status, note)]."""
    sources, reasons = [], []
    for url in e["urls"]:
        try:
            sources.extend(cached_source_texts(fetcher, url))
        except Exception as err:  # any failure makes the entry partly unreadable, never a crash
            reasons.append(f"{url}: {err}")
    if not e["urls"]:
        reasons.append("no URL in the entry")
    readable = []
    for lbl, t, pdf in sources:
        if t is None:  # an extra file that could not be read; pdf holds the reason
            reasons.append(f"{lbl}: {pdf}")
            continue
        tn, tl = normalised(fetcher, lbl, t)
        if len(tn) >= MIN_TEXT:
            readable.append((lbl, tn, tl, pdf, t))
        else:
            reasons.append(f"{lbl}: too little text (possibly a bot check or an empty page)")
    out = []
    for line, quote in quotes:
        if not fragments(quote):
            out.append((line, quote, "MISMATCH", "empty quote"))
            continue
        found, cut = None, None
        for lbl, tn, tl, _pdf, _raw in readable:
            how, gaps = match_detail(quote, tn, tl)
            if how:
                found, cut = (lbl, how), gap_problem(gaps)
                break
        if found and cut:
            out.append((line, quote, cut[0], f"found in {found[0]}, but {cut[1]}"))
        elif found:
            note = f"found in {found[0]}" + ("" if found[1] == "exact" else " (loose: emphasis or dashes ignored)")
            out.append((line, quote, "OK", note))
        elif reasons:
            out.append((line, quote, "UNVERIFIED", "; ".join(reasons)))
        elif any(pdf and in_order_with_gaps(quote, raw) for _l, _tn, _tl, pdf, raw in readable):
            out.append((line, quote, "UNVERIFIED", "PDF layout: the quote's words are in the PDF in order, with "
                                                   "other text between them (likely a table); check by hand"))
        elif len(fragments(quote)) > 1 and any(len(f.split()) < MIN_FRAGMENT_WORDS for f in fragments(quote)):
            out.append((line, quote, "MISMATCH", f"a part cut by an ellipsis is shorter than {MIN_FRAGMENT_WORDS} words"))
        else:
            out.append((line, quote, "MISMATCH", "every source was read; quote not found in order"))
    return out


def main():
    ap = argparse.ArgumentParser(description="Check that quotes in the areas' References match their live sources.")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true")
    mode.add_argument("--changed", metavar="GIT_REF")
    mode.add_argument("--fingerprint", metavar="QUOTE",
                      help="print the fingerprint of a quote, for a record of a check done by hand")
    ap.add_argument("--report", metavar="FILE")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ap.add_argument("--manual", metavar="FILE", default=None)
    args = ap.parse_args()
    if args.fingerprint is not None:
        print(quote_hash(args.fingerprint))
        return 0
    root = os.path.abspath(args.root)
    manual_path = args.manual or os.path.join(root, "docs", "sdlc", "manual-citation-checks.json")
    manual = load_manual(manual_path)
    today = datetime.date.today()
    areas = sorted(f for f in os.listdir(os.path.join(root, "areas")) if re.match(r"^\d{2}-.*\.md$", f))
    changed = changed_lines(root, args.changed) if args.changed else None

    results = []
    fetcher = Fetcher()
    for i, f in enumerate(areas, 1):
        rel = "areas/" + f
        print(f"[{i:02d}/{len(areas)}] {rel}", file=sys.stderr, flush=True)
        for e in parse_references(os.path.join(root, rel)):
            touched = changed.get(rel, set()) if changed is not None else None
            for line, reason in e["bad"]:
                if touched is None or line in touched:
                    results.append(dict(file=rel, line=line, key=e["key"], status="MISMATCH", note=reason, quote=""))
            quotes = e["quotes"]
            if touched is not None:
                # a changed URL or citation line re-checks the whole entry; otherwise only changed quotes
                quotes = quotes if e["lines"] & touched else [q for q in quotes if q[0] in touched]
            if not quotes:
                continue
            for line, quote, status, note in check_entry(fetcher, e, quotes):
                if status == "UNVERIFIED":
                    rec = manual.get((e["key"], quote_hash(quote)))
                    if rec:
                        state, expires = manual_status(rec, today)
                        if state == "expired":
                            note += f"; the check by hand expired on {expires}, re-check by hand"
                        else:
                            status = "MANUAL"
                            note = f"checked by hand on {rec['checked']} ({rec['method']})"
                            if state == "due":
                                note += f"; expires {expires}, re-check by hand soon"
                results.append(dict(file=rel, line=line, key=e["key"], status=status, note=note, quote=quote))

    statuses = ("OK", "MANUAL", "MISMATCH", "UNVERIFIED")
    counts = {s: sum(r["status"] == s for r in results) for s in statuses}
    due = [r for r in results if r["status"] == "MANUAL" and "re-check" in r["note"]]
    scope = "all quotes" if args.all else f"quotes changed since {args.changed}"
    summary = (f"{scope}: {len(results)} checked, {counts['OK']} OK, {counts['MANUAL']} MANUAL, "
               f"{counts['MISMATCH']} MISMATCH, {counts['UNVERIFIED']} UNVERIFIED")
    print(f"check_citations {VERSION}: {summary}")
    for r in results:
        if r["status"] in ("MISMATCH", "UNVERIFIED") or r in due:
            print(f"{r['status']} {r['file']}:{r['line']} [{r['key']}] {r['note']}")
    if args.report:
        with open(args.report, "w", encoding="utf-8") as out:
            out.write(f"# Citation check\n\n{summary}.\n\n")
            sections = [("MISMATCH", [r for r in results if r["status"] == "MISMATCH"]),
                        ("UNVERIFIED", [r for r in results if r["status"] == "UNVERIFIED"]),
                        ("RE-CHECK DUE", due)]
            for title, rows in sections:
                if rows:
                    out.write(f"## {title}\n\n| Where | Key | Note |\n|---|---|---|\n")
                    for r in rows:
                        out.write(f"| `{r['file']}:{r['line']}` | [{r['key']}] | {r['note']} |\n")
                    out.write("\n")
    return 1 if counts["MISMATCH"] else 0


if __name__ == "__main__":
    sys.exit(main())
