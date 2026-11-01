# Open SDLC Standard

An open, cited baseline for any software project: what it must, should and may have from inception to retirement, and the
evidence that shows it. It covers the whole software development lifecycle (SDLC) of software built in a professional setting.

- **Owner:** SomesH S
- **Status:** draft (2026-11-01). A draft is in force for projects that adopt it; later versions may change it substantially. Changes between versions are recorded in [CHANGELOG.md](CHANGELOG.md).
- **Version:** 0.1.0 (draft), from the [VERSION](VERSION) file. Audits cite the name and version, for example "Open SDLC
  Standard v0.1.0".
- **Language:** English.
- **Use:** (1) the baseline for new projects, from day one; (2) the yardstick for auditing existing projects.

> **Not legal advice.** Statements in this standard about laws and regulations (for example Japan's APPI or the EU GDPR) are
> examples for orientation only. Summaries of law are the author's own and unofficial. Whether a law applies to a given
> system, and what it requires, needs review by the organisation's legal function.

## Conventions

- **System and project.** A *system* is what is released, operated and retired as one (see "Unit of adoption"). The
  *project* is the work on one system, and the *project lead* leads that work.
- **Requirement levels:** MUST / SHOULD / MAY, as defined in RFC 2119 and RFC 8174 (the words carry this meaning only in capitals).
  A statement using MUST NOT or SHOULD NOT is headed MUST or SHOULD.
- **Every requirement is traceable to a source:** a recognised standard, an official guide or a primary reference, cited with an
  exact quote and URL in the area's References. Where no source exists, the requirement is marked as the author's judgement.
- **Each area has the same shape:**
  1. Purpose: what the area protects against, and why it matters.
  2. Scope: what the area covers, and what it leaves to other areas.
  3. Requirements: numbered (for example `SEC-4`), graded MUST / SHOULD / MAY. Each has a *Gate* line, the *Evidence* an auditor
     looks for to show it is met, and the *Basis* it rests on.
  4. Failure modes: common ways projects get this wrong.
  5. References: sources with exact quotes and URLs.

## Applying the standard

### Scope and levels

- **Unit of adoption.** The standard applies to a *system*: what is released, operated and retired as one, however many
  repositories it spans. Each system records its records (gates, tailoring, waivers, audits) in one home repository, which
  lists every repository that belongs to the system; the other repositories link to it. Requirements about code and
  repositories are met in each repository; requirements about the running system are met once for the system.
- **Scope of a MUST.** Every MUST applies to every project, whatever its size. Heavier practices are SHOULD or MAY; where
  they apply only after a state is reached (for example, once a service needs a response outside business hours), they carry
  a *Condition*.
- **Basis labels.** Each requirement's *Basis* line cites its sources. The level (MUST / SHOULD / MAY) is the author's grading,
  unless the cited text is itself normative (an RFC 2119 MUST, a "shall" in a standard, or a legal obligation): most sources
  recommend or describe a practice rather than require it. Where the content of a requirement goes beyond what its sources say,
  the Basis line says so ("author's judgement"), and some lines also note when the sources only support SHOULD.
- **Not applicable.** A requirement is not applicable only when its subject does not exist in the system (for example, no user
  interface, no personal data, no API used outside the team). The project records the reason, and the auditor confirms it. Effort
  or cost is never a reason for "not applicable"; that needs a gap waiver for a MUST, or a tailoring-record entry for a
  SHOULD.
- **Gates.** The life of a project is divided by five gates:
  - **G0 Inception:** the decision to build.
  - **G1 Start of build:** the first code or commit.
  - **G2 First shared deployment:** the first deployment outside a developer's own machine.
  - **G3 Go-live:** the first real users or real data. (Real personal data outside production before go-live is covered by its own
    requirement in Area 6.)
  - **G4 Retirement:** the system is switched off and decommissioning is complete.

  Each requirement carries a *Gate* line:

  - **Gate: G*n*.** By gate G*n*, a MUST is met or covered by a valid waiver, and a SHOULD is met or entered in the tailoring
    record. A MAY never blocks a gate; its gate only says from when the option applies. A gate is passed by a dated decision
    recorded by the project lead, with the gate self-assessment attached; that decision cannot be recorded while a MUST marked
    for that gate or an earlier one is unmet without a valid waiver, or such a SHOULD is unmet without a tailoring-record entry.
    Once met, a MUST or SHOULD stays met (or tailored) at every later point in the system's life. Meeting a requirement earlier
    is allowed. A requirement that was met and later stops being met (for example a protection switched off or backups
    stopped) is unmet from when it stopped being met, or from when the lapse was found if that cannot be established; the
    record states both dates. It is remediated like any other unmet requirement, the audit result reflects it, and the next
    gate cannot be recorded until it is met again or covered as the gate rule allows. A gate already passed stays passed;
    gates are not reopened.
  - **Condition: *state reached*** (only on some requirements). The requirement applies only once the condition is first reached
    (and not before its gate); from then on it stays in force.
  - **Trigger: *event*** (only on some requirements). From its gate onwards (and, where it also has a Condition, once that condition is reached), the requirement applies again every time the event
    happens and, at its level, is met for that occurrence within the time the requirement states (or the project sets). A
    requirement carries a trigger when something must be done or produced for each occurrence of an event (each release,
    deployment, schema change, sensitive change, incident, new supplier and so on), so that it can be checked per occurrence: a
    record, an artifact, a test result, an approval or a review. Standing properties of the system or the pipeline (for example
    zero-downtime design, a CI gate, a protected branch) hold continuously and carry no trigger; so do obligations on every change,
    which CI and review enforce.
- **Project types.** A prototype or proof of concept that never reaches real users or real data needs only the G0 and G1
  requirements, and is re-assessed against the full standard before any real use. Work built by a supplier meets the same standard
  through its contract (Area 20). For configured SaaS or low-code systems, requirements about source code are not applicable; the
  rest apply. A repository that belongs to a system follows that system (see "Unit of adoption"). A library, tool or module
  released on its own and used by others is a system in its own right: its go-live (G3) is its first release used by
  others, and requirements about a running service (for example service levels, on-call, backups and production telemetry)
  are not applicable when nothing is run on its behalf.
- **Risk.** MUSTs are the same for every project. A project with high risk (personal data at scale, money, safety) may raise
  selected SHOULDs to MUST in its tailoring record (the tailoring record also lists any requirements raised to MUST).
- **Contradictions inside the standard.** If two requirements conflict, the one in the area that owns the topic applies, and the
  conflict is reported to the owner of the standard.
- **Conflict with other obligations.** Law always applies, and nothing in this standard lowers it. Where a contract, an
  organisational policy or a customer requirement only asks less than this standard, the standard's requirement still applies
  and the difference is recorded. Where law or any of these forbids what a MUST requires:
  - **law or a contract** (including a customer requirement written into a contract): the project follows that obligation, and
    the MUST is recorded in a conflict waiver that names it, renewed while the conflict lasts (see "MUST waivers");
  - **an organisational policy or a customer requirement outside a contract:** this is not a binding obligation under this
    rule. The MUST is unmet, and its remediation is to have that policy or requirement corrected by whoever owns it; a gap
    waiver can cover the MUST meanwhile.

  A SHOULD that cannot be met for any of these reasons goes in the tailoring record.

### Deviations and waivers

- **SHOULD deviations.** One tailoring record per system, kept in its home repository: requirement, reason, owner and review date. The
  project lead approves it.
- **MUST waivers.** A separate record naming the risk, its kind, who accepted it (a person accountable for the system outside the
  delivery team) and an expiry date at most 12 months after acceptance. A MUST is never waived silently. A waiver is valid from
  its acceptance until it expires or ends, provided it was accepted by an eligible person and, for a gap waiver, states its
  plan and was accepted before the remediation due date. When a waiver expires or ends, its MUST is unmet from that date, unless it is met by then, and is handled under
  "Remediation".
  - **Gap:** the project can meet the MUST but has not yet. The waiver states the remediation plan: owner, actions and a target
    date no later than the expiry. This plan is the MUST's remediation plan. Its target date is the remediation due date: the
    date already set under "Remediation", or the date the waiver sets if none was set. A gap waiver is accepted only before that
    due date. If the target date passes with the MUST still unmet, the waiver stays in force until its expiry; the record notes
    the miss and a revised target date no later than the expiry, and the due date itself stays as recorded. The item is not
    overdue while the waiver is in force. If the waiver expires with the MUST still unmet, the remediation item is overdue. A gap
    waiver is not renewed or replaced: each gap gets at most one. If the MUST is met and later becomes unmet again, that is a new
    gap, but a MUST gets no new gap waiver within 12 months of the acceptance of its previous one. For a requirement with a
    Trigger, all occurrences missed within 12 months count as one gap.
  - **Conflict:** law or a contract prevents meeting the MUST ("Conflict with other obligations"). The waiver names that
    obligation; no plan is needed. It is renewed by adding an entry to the same record: the date, who accepted it (under the same
    rule), confirmation that the conflict still exists, and the new expiry, at most 12 months after the entry's date. An entry is
    added before the current expiry; after expiry the MUST is unmet until a new entry is accepted. Entries are only ever added,
    never edited or removed. If the conflict ends, the waiver ends with it: from then on the MUST is met, unmet, or covered by a
    gap waiver under the rules above.
  - **Both kinds.** A conflict waiver may follow a gap waiver for the same MUST when a conflict arises; it does not count as a
    replacement. A conflict waiver that ended under "Change of ownership" is renewed only by a new entry accepted under the
    same rule.
- **Change of ownership.** The system's records stay in its home repository and move with it. When the accountable owner
  changes, or the person who accepted a waiver leaves the role that made them eligible (whether or not they stay in the
  organisation), each open waiver is re-confirmed within 30 days of that change by the person now accountable for the system
  (the new owner, or the same owner when only the acceptor left), who must meet the same rule as an acceptor. The re-confirmation is added to the waiver record with its date and changes
  neither the expiry, the plan nor the target date. A waiver not re-confirmed in time ends on day 30: its MUST is unmet from
  then, a gap waiver's remediation item is overdue, and the gap gets no further waiver. Open remediation items and tailoring
  entries get a new named owner as part of the handover (DOC-14). The transfer is recorded with its date.
- **Rules that need a second person** (independent review, release approval, escalation). Nobody approves their own work. The
  project names a fallback reviewer from outside the team in advance. An emergency change may be released first and reviewed
  afterwards, within a time limit the project sets. For a change written with an AI tool, the person who directed the tool is the
  author.

### Dependencies outside the project

- **Organisation-level policies and roles** the standard assumes (legal or privacy review, approved AI providers, supplier
  assessment, licence policy, the accountable owner of the system, data owners): the project links to them where they exist.
  Where they do not, the project writes a minimal version for itself and records the gap for the organisation to close.
- **Requirements controlled by another team** (for example a platform or operations team): met when the project can show that
  team's evidence. The audit covers what the project depends on; a gap is recorded against the project and escalated to the team
  that owns it.
- **Records that cannot live in the repository** (signed approvals, records with personal data): kept in one named,
  access-controlled place with a defined retention, and linked from the system's home repository (for example from its
  README or `docs/sdlc/external-records.md`). They are never committed to source control.
- **Project-defined terms and thresholds** ("significant", "critical", time limits and intervals the standard leaves to the
  project): defined once, in one project document. That document is itself audited for existence and for being reasonable.

### Auditing

- **Results.** An audit takes each requirement, looks for its *Evidence*, and records met / partly met / not met / not applicable
  (with a reason). The listed Evidence is illustrative: equivalent evidence counts. "Partly met" means some evidence exists but there
  is a gap. The audit result is a pass when every MUST is met, not applicable, or covered by a valid waiver.
- **History.** A new project is judged on its whole history. A project that adopts the standard later starts with a gap
  analysis. A requirement tied to a one-time moment that has already passed (for example a problem statement dated before
  build, or authorisation before first go-live) is met by producing the record now, dated when it is made and noting the
  moment it should have preceded. Requirements that apply to each occurrence of an event apply from adoption onwards.
- **Who audits, and where results live.** The project makes its own self-assessments; they do not replace the formal audits
  GOV-17 requires, and GOV-17 also sets who may carry those out. Audit records are kept in the system's home repository and cite the version of this standard they
  used.
- **When audits happen.** A self-assessment at each gate; formal audits as GOV-17 requires (before go-live, then at least yearly
  and after each major change).
- **Remediation.** Every unmet MUST gets an owner and a due date, and is either fixed by that date or covered by a waiver. If the
  due date passes without a fix or a valid waiver, the item is recorded as overdue; its due date is not moved (a gap waiver's
  revised target date does not move it). Unmet SHOULDs go
  into the tailoring record.
- **Claims.** A system may state "Adopts the Open SDLC Standard vX.Y.Z" once it keeps its records under this standard and has at
  least one self-assessment. It may state "Conforms to the Open SDLC Standard vX.Y.Z (audited YYYY-MM-DD)" only while its latest
  formal audit result is a pass and is at most 12 months old, and, as far as is known, no MUST has since that audit been unmet
  without a valid waiver. Every claim names the version (for "Conforms", the version that was audited) and links to
  the records or the audit record, and is withdrawn when its conditions stop being true. No one certifies against this standard, so "certified"
  or "compliant" is not claimed.
- **Evidence retention.** Audit records and their evidence are kept for the life of the system and for a period after
  decommissioning that the organisation defines.

### Default layout (optional)

A project may use this layout for the records the standard asks for (this section is guidance, not an audited
requirement). It is optional: the requirements say what must exist
and that it is versioned with the code or linked from it (DOC-3, DOC-10), not where. A project that uses it keeps the
repository root for the files readers and tools expect there, and keeps its other documentation under `docs/`. (Layout: author's judgement.)

```
README.md, LICENSE, CHANGELOG.md   the project root: only files expected there
.github/                           CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, templates, CI workflows
docs/
  decisions/                       architecture decision records (DOC-10), using the MADR template: NNNN-title.md
  sdlc/                            records that exist because the project follows this standard
    README.md                      index: version of the standard applied, current gate, links to all evidence
    tailoring.md                   SHOULD deviations ("Deviations and waivers")
    waivers.md                     MUST waivers: risk, kind, acceptance, re-confirmations, expiry; gap: plan, missed and revised
                                   target dates; conflict: the obligation, renewal entries
    definitions.md                 project-defined terms and thresholds ("Dependencies outside the project")
    external-records.md            records kept outside the repository: where, who holds them, retention
    gates/                         one dated gate decision per gate, for example g1-start-of-build.md
    audits/                        self-assessments and audits, for example 2026-11-15-self-assessment-g1.md
  (other documentation)            organised by reader need (DOC-9)
```

- **`docs/sdlc/` holds only what exists because of this standard.** Documentation the project needs anyway (decision records,
  runbooks, guides) stays in its own place, and `docs/sdlc/README.md` links to it as evidence, so each document has one home
  (DOC-11).
- **In this layout, decision records use MADR** ([MADR], Area 16): one decision per file, numbered in sequence. A changed decision gets a
  new record, and the old one is kept and marked "superseded by" it (ARC-2).

### This standard

- **Ownership and change.** The owner named above maintains the standard. Changes are reviewed by the owner before release; while SCM-6 is unmet
  (see [docs/sdlc](docs/sdlc/README.md)) that review is not independent. Every notable change is recorded in the [CHANGELOG](CHANGELOG.md) under [Unreleased] when it is merged: anything that changes
  what a project must do or how it is audited, and any added, changed or removed reference. Typo and formatting fixes are
  not recorded. Each release gets a new version number.
- **Version numbers.** The standard and its tools are released together under one version, MAJOR.MINOR.PATCH, kept in
  the [VERSION](VERSION) file. A PATCH version changes no obligation: it fixes a tool, a link or a source, or clarifies
  wording without changing its meaning. A MINOR version adds a requirement, raises a level, moves a requirement to an
  earlier gate or adds a Trigger. A MAJOR version removes a requirement, lowers its level, moves it to a later gate, adds a
  Condition, or otherwise changes its meaning. Changes to "Applying the standard" follow the same rules: a stricter rule is
  MINOR, a relaxed one MAJOR, and any other change of meaning is MAJOR.
- **New versions.** Each system states, in its records, the version of this standard it applies; its gate decisions and
  audits use and cite that version. When a new version is released, the system moves to it within 90 days: it updates the
  stated version, records the date, and checks itself against the changes. Until then it may keep using the version it had.
  A system may move to the new version at any time within the 90 days, for example to use a relaxed rule at once; it moves
  to the whole version, never to single changes.
- **Modified versions.** The licence allows adapting this standard and, when the adapted text is shared, requires saying
  that it was modified. A modified version should be described as "based on the Open SDLC Standard vX.Y.Z", names who modified it and lists the changes; the claims in
  "Claims" refer only to the unmodified standard. (The name is not a registered trademark; this is a convention, not a legal
  restriction.) An organisation that only needs stricter rules can keep them in its own policy, which takes precedence where
  stricter; differences for one project belong in its tailoring record or a waiver.
- **Language.** The English text is authoritative; translations are for reference.
- **Other frameworks.** Mapping to external certifications (for example ISO/IEC 27001 or SOC 2) is out of scope for this version.

### Research

- `research/` holds the source notes the areas were drafted from, with verbatim quotes checked against the source pages on
  2026-10-31. Candidate requirements in the research notes are numbered per research file; their numbers do not match the
  requirement IDs in the areas, and their judgement labels use the notes' own shorthand rather than the areas' Basis wording.
- [CHANGELOG.md](CHANGELOG.md) records what each version contains and changes.

## Areas

| # | Area | ID | Covers |
|---|---|---|---|
| 1 | [Product and requirements](areas/01-product-and-requirements.md) | PRD | business case and measurable success criteria (KPIs), discovery and user research, feasibility, scope and non-goals, requirements with acceptance criteria, non-functional requirements, domain glossary, acceptance testing (UAT) |
| 2 | [Architecture and design](areas/02-architecture-and-design.md) | ARC | architecture decision records, system boundaries and external contracts, API design and versioning, data model, dependency and build-vs-buy policy, vendored code |
| 3 | [Code quality and conventions](areas/03-code-quality-and-conventions.md) | CQ | coding guidelines, linting and formatting, type safety, comments, size and complexity limits, dead-code detection, code review guidelines, definition of done |
| 4 | [Testing and quality assurance](areas/04-testing-and-quality-assurance.md) | TST | test strategy and pyramid, always-green main branch, coverage of critical rules, test data, regression tests, performance and load, resilience, security testing, accessibility testing, UAT |
| 5 | [Security](areas/05-security.md) | SEC | threat modelling, authentication and authorisation, session handling, secrets management, secure defaults, vulnerability and secret scanning, audit logging, security review, vulnerability reporting |
| 6 | [Privacy and data protection](areas/06-privacy-and-data-protection.md) | PRV | personal-data classification, minimisation, retention and deletion, access logging, applicable law (for example Japan's APPI, the EU GDPR), no personal data in repositories, test data or prompts |
| 7 | [Source control and repository hygiene](areas/07-source-control-and-repository-hygiene.md) | SCM | branching and PR workflow, branch protection, required reviews, CODEOWNERS, PR and issue templates, lean repository, ignore rules, nothing tracked that should not be |
| 8 | [Continuous integration](areas/08-continuous-integration.md) | CI | build, lint, type check, tests and security checks on every change; quality gates; fast feedback |
| 9 | [Build and supply chain](areas/09-build-and-supply-chain.md) | BLD | reproducible builds, dependency pinning and updates, SBOM, licence compliance, image scanning, signed artifacts and provenance, artifact registry and retention |
| 10 | [Environments, configuration and infrastructure](areas/10-environments-configuration-and-infrastructure.md) | ENV | environment separation and parity, infrastructure as code, configuration management, secrets store, reproducible local development (developer experience) |
| 11 | [Release and deployment](areas/11-release-and-deployment.md) | REL | continuous delivery, versioning, changelog and release notes, release approval, zero-downtime deploys, rollback, feature flags, database migrations |
| 12 | [Operations and reliability](areas/12-operations-and-reliability.md) | OPS | service-level objectives, runbooks, incident management and post-mortems, on-call, backups and disaster recovery (RPO/RTO, tested restores), capacity and cost management |
| 13 | [Observability and telemetry](areas/13-observability-and-telemetry.md) | OBS | structured logs, metrics, traces, dashboards, alerting, product/usage telemetry, audit trail |
| 14 | [Data lifecycle and integration](areas/14-data-lifecycle-and-integration.md) | DAT | data ownership, integration and import contracts (validation, idempotency), retention and archiving, data migration and cut-over, time/date/timezone policy |
| 15 | [User experience](areas/15-user-experience.md) | UX | design system, accessibility, internationalisation, error handling and messages, in-app help and user documentation, usability testing |
| 16 | [Documentation and knowledge management](areas/16-documentation-and-knowledge-management.md) | DOC | documentation types, where each lives, ownership, review, keeping docs in step with code, onboarding, handover |
| 17 | [Traceability (cross-cutting)](areas/17-traceability.md) | TRC | requirement → design → code → test → release → production → incident/feedback → requirement |
| 18 | [Process, planning and team](areas/18-process-planning-and-team.md) | PRC | issue tracking, change management, estimation and capacity planning, risk register, roles and ownership, retrospectives, technical debt, delivery and quality metrics |
| 19 | [AI-assisted development](areas/19-ai-assisted-development.md) | AI | shared and versioned agent configuration, rules for AI-generated code and its review, no confidential or personal data in prompts |
| 20 | [Governance, compliance and sustainability](areas/20-governance-compliance-and-sustainability.md) | GOV | stakeholder sign-off, vendor and third-party risk, release to users (notes, training, support model, feedback loop), long-term maintenance, decommissioning and end of life, formal independent audits |

## Contributing

Corrections and proposals are welcome. See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for how the standard is written and how citations
are checked, and the [Code of Conduct](.github/CODE_OF_CONDUCT.md). Changes between versions are listed in [CHANGELOG.md](CHANGELOG.md).

## Licence

The text of this standard, including its research notes, is © 2026 SomesH S and is licensed under the
[Creative Commons Attribution 4.0 International licence](LICENSE) (CC BY 4.0). Quoted material remains the property of its
owners and is not covered by that licence; see [NOTICE.md](NOTICE.md). The scripts and CI workflows (`tools/`,
`.github/workflows/`) are licensed under the [MIT License](LICENSE-CODE).
