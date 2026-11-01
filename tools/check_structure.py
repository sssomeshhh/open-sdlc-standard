#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline structure check for the Open SDLC Standard.

Checks every area file under areas/ against the shape described in .github/CONTRIBUTING.md, checks that relative
links in the published Markdown resolve, and checks that the counts stated in CHANGELOG.md match the files.

Usage:  python3 tools/check_structure.py [repository root]
Exit status 0 when everything passes, 1 when any problem is found. Uses only the Python standard library.
"""
import os
import re
import sys

def _read_version():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION")
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "unknown"


VERSION = _read_version()  # one version for the standard and its tools

SECTIONS = ["Purpose", "Scope", "Requirements", "Failure modes", "References"]
LEVELS = ("MUST", "SHOULD", "MAY")
GATES = {"G0", "G1", "G2", "G3", "G4"}

AREA_FILE_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
H1_RE = re.compile(r"^# (\d+)\. \S")
PREFIX_RE = re.compile(r"^- \*\*ID prefix:\*\* ([A-Z]+)\s*$")
REQ_RE = re.compile(r"^### ([A-Z]+)-([1-9]\d*) · (MUST|SHOULD|MAY) · \S")
REQ_LIKE_RE = re.compile(r"^#{1,6} [A-Z]+-\d+\b")
# Gate, then at most one Condition, then at most one Trigger; each value runs up to the next " · **".
GATE_RE = re.compile(
    r"^- \*\*Gate:\*\* (G\d)"
    r"(?: · \*\*Condition:\*\* (?:(?! · \*\*).)+)?"
    r"(?: · \*\*Trigger:\*\* (?:(?! · \*\*).)+)?\s*$"
)
REF_RE = re.compile(r"^- \*\*\[([^\]]+)\]\*\*")
# A reference key in square brackets, not Markdown link text ("[text](url)" or "[text][ref]").
KEY_RE = re.compile(r"\[([A-Z0-9][A-Za-z0-9.\-]*)\](?![(\[])")
# RFC 2119 / RFC 8174 keywords, longest first so "MUST NOT" is not also counted as "MUST".
KEYWORDS = [
    ("MUST NOT", "MUST"), ("SHALL NOT", "MUST"), ("SHOULD NOT", "SHOULD"), ("NOT RECOMMENDED", "SHOULD"),
    ("REQUIRED", "MUST"), ("SHALL", "MUST"), ("MUST", "MUST"), ("RECOMMENDED", "SHOULD"), ("SHOULD", "SHOULD"),
    ("OPTIONAL", "MAY"), ("MAY", "MAY"),
]
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")



def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def keyword_levels(text):
    """Return the RFC 2119 level of every capitalised keyword in text, in order.
    Code spans and link targets are ignored; a keyword glued to letters, digits or '_' is not a keyword."""
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    found = []
    pattern = "|".join(re.escape(k) for k, _ in KEYWORDS)
    for m in re.finditer(r"(?<![A-Za-z0-9_])(" + pattern + r")(?![A-Za-z0-9_])", text):
        found.append(dict(KEYWORDS)[m.group(1)])
    return found


def ref_sort_key(key):
    """Alphabetical, ignoring case, with runs of digits compared by value (RFC3339 < RFC8259, OPS05 < OPS06).

    Keys that compare equal this way (OPS5 and OPS05, or keys differing only in case) fall back to the key itself,
    so every list has exactly one valid order.
    """
    return ([int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", key)], key)


def check_area(path, problems, totals):
    name = os.path.basename(path)
    lines = read_text(path).split("\n")

    def err(lineno, msg):
        problems.append(f"{name}:{lineno}: {msg}")

    m = H1_RE.match(lines[0]) if lines else None
    if not m:
        err(1, "first line must be '# N. Area name'")
    elif int(m.group(1)) != int(name[:2]):
        err(1, f"heading number {m.group(1)} does not match file number {name[:2]}")

    prefix = None
    for i, ln in enumerate(lines[:10], 1):
        pm = PREFIX_RE.match(ln)
        if pm:
            prefix = pm.group(1)
    if not prefix:
        err(1, "missing '- **ID prefix:** XXX' line")

    sections = [(i, ln[3:].strip()) for i, ln in enumerate(lines, 1) if ln.startswith("## ")]
    if [s for _, s in sections] != SECTIONS:
        err(1, f"sections must be exactly {SECTIONS}, found {[s for _, s in sections]}")
    sec_line = {s: i for i, s in sections}

    # Requirements: each runs from its heading to the next ### or ## heading.
    req_start = sec_line.get("Requirements", 0)
    req_end = sec_line.get("Failure modes", len(lines) + 1)
    for k, ln in enumerate(lines, 1):
        if not (req_start < k < req_end) and (ln.startswith("### ") or REQ_LIKE_RE.match(ln)):
            err(k, "a requirement-style heading outside the Requirements section")
    numbers = []
    cited = set()
    i = req_start
    while i < req_end - 1:
        ln = lines[i]
        if ln.startswith("### "):
            hm = REQ_RE.match(ln)
            if not hm:
                err(i + 1, "requirement heading must be '### PREFIX-N · LEVEL · Title'")
                i += 1
                continue
            pfx, num, level = hm.group(1), int(hm.group(2)), hm.group(3)
            if prefix and pfx != prefix:
                err(i + 1, f"ID prefix {pfx} does not match the area prefix {prefix}")
            numbers.append(num)
            totals[level] += 1
            j = i + 1
            while j < req_end - 1 and not lines[j].startswith("### "):
                j += 1
            block = lines[i + 1:j]
            rid = f"{pfx}-{num}"
            first_field = next((k for k, b in enumerate(block) if b.startswith("- **")), len(block))
            statement = " ".join(block[:first_field])
            levels = keyword_levels(statement)
            if len(levels) != 1:
                err(i + 1, f"{rid}: statement must contain exactly one RFC 2119 keyword, found {len(levels)}")
            elif levels[0] != level:
                err(i + 1, f"{rid}: heading says {level} but the statement uses a {levels[0]} keyword")
            for field in ("Gate", "Evidence", "Basis"):
                n = sum(1 for b in block if b.startswith(f"- **{field}:**"))
                if n != 1:
                    err(i + 1, f"{rid}: needs exactly one '- **{field}:**' line, found {n}")
            gate_lines = [b for b in block if b.startswith("- **Gate:**")]
            if gate_lines:
                gm = GATE_RE.match(gate_lines[0])
                if not gm or gm.group(1) not in GATES:
                    err(i + 1, f"{rid}: Gate line must be '- **Gate:** G0–G4' with optional Condition then Trigger")
                else:
                    totals["gates"][gm.group(1)] = totals["gates"].get(gm.group(1), 0) + 1
                    totals["conditions"] += "**Condition:**" in gate_lines[0]
                    totals["triggers"] += "**Trigger:**" in gate_lines[0]
            basis_idx = next((k for k, b in enumerate(block) if b.startswith("- **Basis:**")), None)
            if basis_idx is not None:
                basis = block[basis_idx]
                k = basis_idx + 1
                while k < len(block) and block[k].startswith("  "):
                    basis += " " + block[k]
                    k += 1
                cited.update(KEY_RE.findall(basis))
            i = j
        else:
            i += 1
    if not numbers:
        err(req_start, "the area has no requirements")
    elif numbers != list(range(1, len(numbers) + 1)):
        err(req_start, f"requirement numbers must run 1..{len(numbers)} without gaps, found {numbers}")

    # References: every key cited in a Basis line is defined; every defined key is cited somewhere in the file.
    ref_start = sec_line.get("References", len(lines))
    defined = {}
    for k in range(ref_start, len(lines)):
        rm = REF_RE.match(lines[k])
        if rm:
            key = rm.group(1)
            if key in defined:
                err(k + 1, f"reference [{key}] is defined twice")
            defined[key] = k + 1
    order = list(defined)
    want = sorted(order, key=ref_sort_key)
    if order != want:
        first = next(i for i, (x, y) in enumerate(zip(order, want)) if x != y)
        err(defined[order[first]], f"References must be in alphabetical order, numbers by value: "
                                   f"[{want[first]}] should come before [{order[first]}]")
    for key in sorted(cited - set(defined)):
        err(ref_start, f"[{key}] is cited in a Basis line but has no References entry")
    body = re.sub(r"`[^`]*`", " ", "\n".join(lines[:ref_start - 1]))
    used_anywhere = set(KEY_RE.findall(body))
    for key in sorted(set(defined) - used_anywhere):
        err(defined[key], f"reference [{key}] is never cited in this area")
    for key in sorted(used_anywhere - set(defined) - cited):
        err(ref_start, f"[{key}] is cited in the text but has no References entry")
    return prefix


def check_links(root, problems):
    skip = {".git", ".tmp", ".claude", ".remember", "review", "node_modules"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            text = read_text(path)
            # ignore fenced code and inline code spans, keeping line numbers
            text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
            text = re.sub(r"`[^`\n]*`", " ", text)
            for m in LINK_RE.finditer(text):
                target = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                lineno = text[:m.start()].count("\n") + 1
                target = target.split("#", 1)[0]
                if target.startswith("/"):
                    problems.append(f"{rel}:{lineno}: absolute link path, use a relative link: {m.group(1)}")
                    continue
                resolved = os.path.normpath(os.path.join(dirpath, target))
                if target and os.path.commonpath([resolved, root]) != root:
                    problems.append(f"{rel}:{lineno}: relative link leaves the repository: {m.group(1)}")
                elif target and not os.path.exists(resolved):
                    problems.append(f"{rel}:{lineno}: relative link does not resolve: {m.group(1)}")


def check_counts(root, area_count, totals, problems):
    path = os.path.join(root, "CHANGELOG.md")
    if not os.path.exists(path):
        problems.append("CHANGELOG.md: missing")
        return
    text = read_text(path)
    # Only the newest released version's section counts (not [Unreleased], not older versions).
    m = re.search(r"^## \[\d+\.\d+\.\d+\][^\n]*\n(.*?)(?=^## |^\[[^\]]+\]: |\Z)", text, re.S | re.M)
    if not m:
        problems.append("CHANGELOG.md: no '## [MAJOR.MINOR.PATCH]' version section")
        return
    section = re.sub(r"\s+", " ", m.group(1))
    total = sum(totals[lv] for lv in LEVELS)
    expect = {
        f"{area_count} areas": "number of areas",
        f"{total} requirements": "number of requirements",
        f"{totals['MUST']} MUST, {totals['SHOULD']} SHOULD, {totals['MAY']} MAY": "requirements per level",
    }
    for phrase, what in expect.items():
        if not re.search(r"(?<!\d)" + re.escape(phrase), section):
            problems.append(f"CHANGELOG.md: the {what} does not match the area files (expected '{phrase}')")


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
    areas_dir = os.path.join(root, "areas")
    problems = []
    totals = {"MUST": 0, "SHOULD": 0, "MAY": 0, "gates": {}, "conditions": 0, "triggers": 0}
    files = sorted(f for f in os.listdir(areas_dir) if f.endswith(".md"))
    prefixes = {}
    for f in files:
        if not AREA_FILE_RE.match(f):
            problems.append(f"areas/{f}: file name must be 'NN-name.md'")
            continue
        prefix = check_area(os.path.join(areas_dir, f), problems, totals)
        if prefix and prefix in prefixes:
            problems.append(f"areas/{f}: ID prefix {prefix} is already used by areas/{prefixes[prefix]}")
        elif prefix:
            prefixes[prefix] = f
    nums = [int(f[:2]) for f in files if AREA_FILE_RE.match(f)]
    if nums != list(range(1, len(nums) + 1)):
        problems.append(f"areas/: area numbers must run 1..{len(nums)} without gaps, found {nums}")
    check_links(root, problems)
    check_counts(root, len(nums), totals, problems)
    readme = read_text(os.path.join(root, "README.md")) if os.path.exists(os.path.join(root, "README.md")) else ""
    vm = re.search(r"^- \*\*Version:\*\* (\S+)", readme, re.M)
    if not vm or vm.group(1) != VERSION:
        problems.append(f"README.md: the Version line does not match the VERSION file ({VERSION})")

    total = sum(totals[lv] for lv in LEVELS)
    gates = ", ".join(f"{g} {totals['gates'].get(g, 0)}" for g in sorted(GATES))
    print(f"check_structure {VERSION}: {len(nums)} areas, {total} requirements "
          f"({totals['MUST']} MUST, {totals['SHOULD']} SHOULD, {totals['MAY']} MAY); gates: {gates}; "
          f"{totals['conditions']} conditions, {totals['triggers']} triggers")
    for p in problems:
        print("ERROR " + p)
    print("OK" if not problems else f"{len(problems)} problem(s) found")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
