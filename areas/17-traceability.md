# 17. Traceability (cross-cutting)

- **ID prefix:** TRC
- **Status:** draft, 2026-10-31

## Purpose
Traceability links each requirement to the design, code, tests and release that implement it. It also links each
production incident or piece of feedback back to the change or gap that caused it. Without these links nobody can say
why a line of code exists, which requirement a test protects, what a release contains, or which change caused a
failure. Audits, impact analysis and safe change all depend on the chain staying unbroken.

## Scope
This area owns the chain requirement → design → code → test → release → production → incident/feedback →
requirement. It covers the links between artifacts. It does not cover how each artifact is produced:

- Writing requirements, acceptance criteria and UAT sign-off: see Area 1.
- Architecture decision records: see Area 2.
- Test types and test strategy: see Area 4.
- PR templates, required reviews and branch protection: see Area 7.
- SBOM and build provenance mechanics: see Area 9.
- Versioning, changelog and release mechanics: see Area 11.
- Incident management and post-mortems: see Area 12.
- Collecting user feedback: see Area 20.
- The reason for a change written down: see CQ-13.
- Each release unique, immutable and traceable to its commit: see REL-4; build provenance: see BLD-8.
- Recording decisions, threats and risks: see ARC-1, SEC-1 and PRC-5. Tracking postmortem actions: see OPS-7. Feeding
  feedback into the backlog: see GOV-12.

## Requirements

### TRC-1 · MUST · Stable requirement identifiers
Every requirement MUST have a stable, unique identifier (for example an issue number) that design notes, changes,
tests and release notes can reference.
- **Gate:** G1
- **Evidence:** requirements or issues carry IDs that are never re-used; a sample of 10 merged changes shows the IDs
  being referenced.
- **Basis:** [NASA-SWE052], [ISO29148].

### TRC-2 · MUST · Bi-directional traceability
Traceability MUST run both ways: forward from each requirement to its design, code and tests, and backward from each
change and test to the requirement that justifies it.
- **Gate:** G2
- **Evidence:** a traceability matrix, or a query across tracker, version control and tests, that answers both
  directions; a sample can be traced both ways, with no orphan changes and no requirement without a test.
- **Basis:** [NASA-SWE052].

### TRC-3 · MUST · Every change linked to its issue
Each code change (pull or merge request) MUST be linked to the issue or requirement it addresses.
- **Gate:** G1
- **Evidence:** a PR template field or closing keyword in each change; a repository rule or CI check that flags
  changes without a link; a sample of merged changes all carry a link.
- **Basis:** [GH-LINK], [NASA-SWE052].

### TRC-4 · SHOULD · Tests cite the requirement they verify
Each requirement's acceptance criteria SHOULD be covered by at least one test whose name or metadata cites the
requirement ID.
- **Gate:** G2
- **Evidence:** a test-to-requirement mapping; for critical rules, a per-requirement coverage report.
- **Basis:** [NASA-SWE052], [ISO29148].

### TRC-5 · MUST · Decisions, risks and security requirements linked
Design decisions (ARC-1), threats and security requirements (SEC-1) and risks (PRC-5) MUST be linked to the
requirements and changes they affect, so the reason for a control can be traced.
- **Gate:** G1
- **Evidence:** in a sample of decision, threat-model and risk records, each links to requirement IDs and to the
  changes that implement them.
- **Basis:** [SSDF] (PW.1.2).

### TRC-6 · MUST · Release contents recorded
Each release MUST record which changes (issue or PR IDs) it contains.
- **Gate:** G2 · **Trigger:** each release
- **Evidence:** per-version release notes or changelog entries listing issue/PR IDs. Immutable release identifiers:
  REL-4; changelog format: REL-6.
- **Basis:** [KACL]. Listing issue/PR IDs: author's judgement.

### TRC-7 · SHOULD · Deployed version visible per environment
Each environment SHOULD show which version or commit is running (for example a version endpoint), so an incident can be
traced to a release. The deploy history itself is required by REL-4.
- **Gate:** G2
- **Evidence:** a version endpoint or image tag visible in each environment.
- **Basis:** [SLSA-PROV] in part. Author's judgement (no primary source states this directly).

### TRC-8 · MUST · Incidents traced to cause and fix
Each production incident or defect record MUST link to its root cause, the change that fixed it, and the regression
test that guards against it.
- **Gate:** G3 · **Trigger:** each production incident or defect
- **Evidence:** post-incident or defect records with links: incident → root cause → fixing change → regression test.
- **Basis:** [SSDF] (RV.3.1), [SRE-PM]. Applying this to every defect, not only incidents and vulnerabilities, and the
  regression-test link (regression testing itself: Area 4): author's judgement.

### TRC-9 · SHOULD · Backlog items link back to their source
Each backlog item created from a post-incident review or from user feedback SHOULD link back to the record it came
from. Tracking the actions: OPS-7; feeding feedback into the backlog: GOV-12.
- **Gate:** G3 · **Trigger:** each backlog item created from a post-incident review or user feedback
- **Evidence:** in a sample of backlog items created from post-mortems and feedback, each has a link to its source
  record.
- **Basis:** Author's judgement (the sources cited by OPS-7 and GOV-12 cover tracking, not the link back).

### TRC-10 · SHOULD · Requirement changes tracked
Changes to requirements SHOULD be tracked (who, when, why), with the linked design and tests re-checked in the same
change.
- **Gate:** G1 · **Trigger:** each change to a requirement
- **Evidence:** requirement history in the tracker; affected tests updated alongside the requirement change.
- **Basis:** [NASA-SWE052], [ISO29148].

### TRC-11 · MAY · Generated traceability report
The project MAY generate its traceability report automatically from tool data (tracker, version control, CI) instead
of maintaining it by hand.
- **Gate:** G2
- **Evidence:** a script or dashboard that produces the report; the report's date matches the latest release.
- **Basis:** Author's judgement (no primary source found).

## Failure modes
- A traceability matrix maintained by hand drifts from reality and is refreshed only before an audit. (Author's
  judgement.)
- Changes merged with no issue link, so the reason for a change is lost; plain `git blame` cannot recover it once
  history has been rewritten. (Author's judgement.)
- Requirements refined or reinterpreted without trace, so the built feature diverges from the request; NASA notes
  that bidirectional traceability makes it "less likely that requirements are misinterpreted as they are refined"
  [NASA-SWE052].
- Released artifacts cannot be tied to a commit (mutable `latest` tags, re-used version numbers); see REL-4.
  (Author's judgement.)
- Post-mortem findings never become backlog items, so the same root cause recurs [SSDF] (RV.3.4); "An unreviewed
  postmortem might as well never have existed." [SRE-PM].

## References
- **[GH-LINK]** Linking a pull request to an issue. GitHub Docs.
  https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue.
  Accessed 2026-10-31.
  > "When you link a pull request to the issue the pull request addresses, collaborators can see that someone is working on the issue." (About linked issues and pull requests)
  > "When you merge a linked pull request into the default branch of a repository, its linked issue is automatically closed." (About linked issues and pull requests)
- **[ISO29148]** ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements
  engineering. IEEE SA. https://standards.ieee.org/ieee/29148/6937/. Accessed 2026-10-31. Paywalled; public abstract
  only.
  > "It defines the construct of a good requirement, provides attributes and characteristics of requirements," (abstract)
  > "and discusses the iterative and recursive application of requirements processes throughout the life cycle." (abstract)
- **[KACL]** Keep a Changelog 1.1.0. Olivier Lacan. https://keepachangelog.com/en/1.1.0/. Accessed 2026-10-31.
  > "A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project"
- **[NASA-SWE052]** SWE-052 – Bidirectional Traceability. NASA Software Engineering Handbook (implements NPR 7150.2
  §3.12.1), NASA. https://swehb.nasa.gov/display/SWEHBVD/SWE-052+-+Bidirectional+Traceability. Accessed 2026-10-31.
  > "The project manager shall perform, record, and maintain bi-directional traceability" (1. Requirements)
  > "Bidirectional traceability matrices also make it less likely that requirements are misinterpreted as they are refined." (2. Rationale)
- **[SLSA-PROV]** SLSA v1.0 Provenance. OpenSSF SLSA. https://slsa.dev/spec/v1.0/provenance. Accessed 2026-10-31.
  > "Provenance is an attestation that a particular build platform produced a set of software artifacts" (Model)
  > "The BuildDefinition describes all of the inputs to the build." (BuildDefinition)
- **[SRE-PM]** Postmortem Culture: Learning from Failure. Site Reliability Engineering (book), Google.
  https://sre.google/sre-book/postmortem-culture/. Accessed 2026-10-31.
  > "An unreviewed postmortem might as well never have existed." (Ch. 15, Best Practice: No Postmortem Left Unreviewed)
  > "Is the action plan appropriate and are resulting bug fixes at appropriate priority?" (Ch. 15, Collaborate and Share Knowledge)
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST, February 2022.
  https://doi.org/10.6028/NIST.SP.800-218. Accessed 2026-10-31.
  > "Track and maintain the software’s security requirements, risks, and design decisions." (PW.1.2)
  > "Analyze identified vulnerabilities to determine their root causes." (RV.3.1)
  > "Record the root cause of discovered issues." (RV.3.1, example)
  > "Review the SDLC process, and update it if appropriate to prevent (or reduce the likelihood of) the root cause recurring" (RV.3.4)
