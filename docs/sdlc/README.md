# SDLC records

This repository applies its own standard to itself. This folder holds the records that exist because it does, following the
optional default layout in the [README](../../README.md) ("Default layout (optional)").

- **Records as of:** the v0.1.0 release, 2026-11-01.
- **Standard applied:** Open SDLC Standard v0.1.0 (draft).
- **Gates:** no gate decision is recorded. With the v0.1.0 release the repository is past the G1, G2 and G3 events (first
  commit, first push to the shared repository, first public release) without gate decisions. G1 cannot be recorded until
  SCM-6 is met: no waiver is possible (see below). Because SCM-6 and GOV-17 are unmet without a waiver, the repository does
  not pass an audit (README, "Results"). Gate decisions are added under `gates/` as they are made.
- **Audits:** none. No self-assessment has been made, so the repository's conformance to its own standard has not been
  assessed. The first self-assessment is due by 2026-11-15 (owner: SomesH S) and is added under `audits/`.
- **Tailoring and waivers:** none. The files are added when there is a first entry.

## Evidence

| Requirement area | Where the evidence is |
|---|---|
| Contribution rules (SCM-9) | [.github/CONTRIBUTING.md](../../.github/CONTRIBUTING.md) |
| Pull request and issue templates (SCM-8) | [.github/pull_request_template.md](../../.github/pull_request_template.md), [.github/ISSUE_TEMPLATE/](../../.github/ISSUE_TEMPLATE/) |
| Ignore rules (SCM-10) | [.gitignore](../../.gitignore) |
| Vulnerability reporting (SEC-16) | [.github/SECURITY.md](../../.github/SECURITY.md) |
| Decision records (DOC-10) | [docs/decisions/](../decisions/) |
| Changelog | [CHANGELOG.md](../../CHANGELOG.md) |
| Licence and attribution | [LICENSE](../../LICENSE), [NOTICE.md](../../NOTICE.md) |
| Quotes checked against their sources | [citation-check-2026-11-01.txt](citation-check-2026-11-01.txt) (automatic, all quotes), [manual-citation-checks.json](manual-citation-checks.json) (by hand) |

## Unmet requirements

This list holds only what is known without an assessment. SCM-6 and GOV-17 are listed because a sole maintainer cannot
meet them, whatever else an assessment finds. Until the first self-assessment is made, other requirements may also be unmet. Each
entry is recorded as the standard requires ("Auditing", "Remediation"): every unmet MUST has an owner and a due date, and
is either fixed by that date or covered by a waiver.

### SCM-6 · MUST · Independent approving review, re-approved after changes

- **Status:** not met.
- **Reason:** the repository has one maintainer, so no pull request can be approved by someone other than its author. No
  one outside the delivery team is available to review or to accept a waiver, so no fallback reviewer can be named (README,
  "Rules that need a second person"). This gap is recorded here. Until SCM-6 is met, the repository does not pass an audit
  (README, "Results").
- **Owner:** SomesH S.
- **Remediation:** find a second maintainer or reviewer among the people who use or contribute to the public repository;
  when one joins, require one approving review on `trunk`.
- **Due date:** 2027-04-30.
- **Compensating measures** (they reduce the risk; they do not meet SCM-6): every change goes through a pull request with
  the required checks; commits are signed; the history is public; anyone can comment on a pull request.

### GOV-17 · MUST · Formal audit by an independent assessor

- **Status:** not met.
- **Reason:** the standard and its tools are released on their own and used by others, so they are treated as a tool
  under README "Project types": go-live (G3) is the first release used by others, taken here as the first public release,
  v0.1.0. GOV-17 requires a formal audit before go-live by an assessor
  outside the delivery team, and, as for SCM-6, no one outside the delivery team is available. Until GOV-17 is met, the
  repository has no formal audit and cannot state "Conforms" (README, "Claims").
- **Owner:** SomesH S.
- **Remediation:** find an assessor who meets GOV-17's three independence criteria (the repository is public, so anyone
  can offer), and record the formal audit under `audits/`.
- **Due date:** 2027-04-30.
