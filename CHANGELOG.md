# Changelog

All notable changes to the Open SDLC Standard are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions are numbered as described in the
README ("This standard").

## [Unreleased]

## [0.1.0] - 2026-11-01

Status: draft. First public draft.

### Added

- 20 areas covering the software development lifecycle, from product and requirements to governance, compliance and
  sustainability. Each area has the same shape: purpose, scope, requirements, failure modes and references.
- 306 requirements, each graded MUST, SHOULD or MAY in the sense of RFC 2119 and RFC 8174 (163 MUST, 127 SHOULD,
  16 MAY). Every requirement states the *Evidence* an auditor looks for and the *Basis* it rests on: cited sources, or
  a label where the content or level is the author's judgement.
- Five lifecycle gates, G0 Inception to G4 Retirement. Every requirement names its gate. By that gate, a MUST is met or
  covered by a valid waiver, and a SHOULD is met or recorded as a deviation in the tailoring record; for a MAY, the gate only
  says from when the option applies.
  Some also carry a *Condition* (it applies only once a state is reached) or a *Trigger* (it applies again at each occurrence
  of an event).
- Rules for applying the standard:
  - scope: the unit of adoption (a system with one home repository), project types including libraries and tools,
    "not applicable", and conflicts with law, contracts, policies and customer requirements;
  - gates: what blocks a gate, and lapses after a gate (gates are never reopened);
  - deviations: tailoring of SHOULDs; waivers for MUSTs (a one-off gap waiver with a remediation plan, or a conflict
    waiver renewed while law or a contract prevents the MUST); change of ownership; rules that need a second person;
  - auditing: results and the pass rule, history and late records, remediation and overdue items,
    and claims ("Adopts" and "Conforms");
  - this standard: version numbers (one version for the standard and its tools), new versions and modified versions.
- References with exact quotes, URLs and, where an entry quotes several parts of a source, the location of each quote.
  Every quote that can be read automatically was checked against its live source on 2026-11-01: 604 matched and none
  failed (`docs/sdlc/citation-check-2026-11-01.txt`). The 9 that cannot be read automatically were checked by hand on
  2026-10-31 and recorded (`docs/sdlc/manual-citation-checks.json`). Where a source is paywalled, only its public
  abstract is quoted, and the entry says so.
- Research notes (`research/`) with the source material the areas were drafted from.
- An optional default layout for a project's records under this standard (`docs/sdlc/`, with decision records in
  `docs/decisions/` using the MADR template).
- Verification tools (`tools/`, MIT licence in `LICENSE-CODE`): `check_structure.py` checks the area format, links and
  counts; `check_citations.py` checks quotes against their live sources. CI runs the structure check on every change,
  checks added or changed quotes on every pull request, and checks all quotes monthly. A signed version tag publishes a
  GitHub release, but only when CI passed for the tagged commit on `trunk`. The tools have regression tests
  (`tools/tests/`).
- This repository's own records under the standard (`docs/sdlc/`): two known unmet requirements (SCM-6 and GOV-17), each
  with its remediation plan; the decision record for the rules on applying the standard
  (`docs/decisions/0001-rules-for-applying-the-standard.md`); and a security policy (`.github/SECURITY.md`). No self-assessment has been made yet; the first is due by 2026-11-15.

[Unreleased]: https://github.com/sssomeshhh/open-sdlc-standard/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sssomeshhh/open-sdlc-standard/releases/tag/v0.1.0
