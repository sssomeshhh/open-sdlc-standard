# Contributing to the Open SDLC Standard

Thank you for helping to improve the standard. Every requirement in it must be traceable to a source or clearly labelled as the
author's judgement, so contributions are held to the same rules the standard sets for itself.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). By submitting a contribution, you agree to
license your own text under the [Creative Commons Attribution 4.0 International licence](../LICENSE) (CC BY 4.0); quoted
material keeps its owners' terms (see [NOTICE.md](../NOTICE.md)).

## Ways to contribute

- **Report a problem with a citation**: a quote that does not match its source, a broken link, or a source that does not support
  the requirement it is cited for. Use the "Citation problem" issue template.
- **Propose a change to a requirement**: a new requirement, a different level (MUST / SHOULD / MAY), a different gate, or clearer
  wording. Use the "Change proposal" issue template, and discuss it before opening a pull request.
- **Fix a typo or broken formatting**: open a pull request directly.

## How the standard is written

Read the README first, especially "Applying the standard". Each area file under `areas/` has the same shape:

```
# N. Area name

## Purpose
## Scope
## Requirements
### XXX-1 · MUST · Short title
One or two sentences, using MUST / SHOULD / MAY (RFC 2119 / RFC 8174) in capitals, once per requirement (MUST NOT and
SHOULD NOT are headed MUST and SHOULD).
- **Gate:** G0–G4, optionally followed by `· **Condition:** <state reached>` and/or `· **Trigger:** <event>`, in that order.
- **Evidence:** what an auditor looks at to confirm it, concrete enough to check yes or no.
- **Basis:** source keys, for example [SSDF], [ASVS]; plus a judgement label where it applies.
## Failure modes
## References
- **[KEY]** Title. Publisher or author. URL. Accessed YYYY-MM-DD.
  > "verbatim quote"
```

### Rules for requirements

1. **One obligation per requirement**, testable, with one RFC 2119 keyword. If a requirement holds two obligations, split it.
2. **Levels.** MUST: without it the project is unsafe, unmaintainable, unauditable or non-compliant. SHOULD: the expected default;
   a project that deviates records why in its tailoring record (README, "Deviations and waivers"). MAY: truly optional. The level is the author's grading unless the cited text is
   itself normative; if a requirement goes beyond what its sources say, its Basis line says so ("author's judgement").
3. **Generic.** No product, company, project or person names outside References and attribution, and no tool lock-in: name a
   tool only as an example.
4. **Proportionate.** Every MUST applies to every project, whatever its size. Heavier practices are SHOULD or MAY; where they
   apply only after a state is reached, they carry a Condition.
5. **One home per topic.** A rule is stated once, in the area that owns the topic, and other areas refer to it. Do not add a second
   copy of a rule at a different level.
6. **No claim without a source key or an explicit judgement label.**

### Gates, conditions and triggers

- **Gate:** the earliest gate by which the requirement can reasonably be met and must be met (definitions in the README).
- **Condition:** a one-off state that, once reached, makes the requirement apply from then on (for example "once a measured SLO
  exists").
- **Trigger:** add one when something must be done or produced for each occurrence of an event (each release, deployment, schema
  change, sensitive change, incident, new supplier and so on), so that it can be checked per occurrence. Standing properties of the
  system or the pipeline, and obligations on every change, carry no trigger.

### Rules for citations

1. **Quote verbatim.** Copy the exact text from the source. Do not paraphrase inside quotation marks; mark any cut with "…".
2. **Verify against the live source** before you add or change a quote: fetch the page and confirm the exact text. State the date
   in "Accessed". If you cannot confirm a quote, do not use it; cite the source without a quote, or label the requirement as the
   author's judgement.
3. **Prefer primary sources**: international standards (public pages only for paywalled standards), official guides of
   recognised bodies, and the originators' own publications. Avoid blogs and secondary summaries.
4. **Only cite what supports the requirement**, and remove sources that nothing cites any more.
5. **Law.** Quote official texts or government-published translations, and say when a translation is for reference only.
   Statements about law are examples for orientation, not legal advice.
6. **One key per source document.** Cite the article or section after the key (for example `[GDPR] Art. 30(1)`). When an
   entry quotes several parts of a document, each quote carries its location in brackets after the closing quotation
   mark, for example `> "…" (Art. 8(2))`.
7. **Order.** References are listed in alphabetical order of their keys, ignoring case, with numbers compared by value
   (`RFC3339` before `RFC8259`, `12F-2` before `12F-10`). Number parts of a key use Arabic numerals. `check_structure.py`
   enforces the order.

## Pull requests

- Before opening a pull request, run the same checks CI runs (Python 3, no packages needed):
  - `python3 tools/check_structure.py` checks the area format, links and counts;
  - `python3 -m unittest discover -s tools/tests` tests the tools themselves, if you change them;
  - `python3 tools/check_citations.py --changed origin/trunk` checks the quotes you added or changed against their live
    sources (PDF sources need `pdftotext` from poppler-utils). A quote reported as UNVERIFIED could not be read
    automatically. Check it by hand against the source and add a record to
    [docs/sdlc/manual-citation-checks.json](../docs/sdlc/manual-citation-checks.json): the reference key, file and line, the
    fingerprint of the quote (run `python3 tools/check_citations.py --fingerprint "<quote>"`), the source URL, how you
    checked it, the date and your name. A record covers the quote only while its text is unchanged, and for 12 months; the
    monthly check reminds you 30 days before it expires. A MISMATCH is never covered by a record.
- Keep each pull request to one topic, and fill in the pull request template.
- Explain why the change is needed, and give the source for any new or changed claim.
- Do not renumber existing requirement IDs; the maintainer handles numbering when needed.
- The maintainer reviews every change before it is merged. Notable changes are recorded in the [CHANGELOG](../CHANGELOG.md)
  under [Unreleased], as the README defines them ("This standard").
