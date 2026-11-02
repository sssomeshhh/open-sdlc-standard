# 2. Architecture and design

- **ID prefix:** ARC
- **Status:** draft, 2026-10-31

## Purpose

This area protects against decisions nobody can explain, boundaries nobody can see, and contracts that break consumers
without warning. It covers how significant decisions, the system's context, its external contracts, its data model and its
third-party code are written down and owned, so the system can be changed safely by people who were not there when it was
built.

## Scope

Covers: architecture decision records (ADRs), the architecture description and system context, domain boundaries, external
contracts (APIs and events), API versioning and error format, the data model, the choice of dependencies (declaring and locking them: Area 9),
build-vs-buy and technology choices, and vendored third-party code.

Leaves to other areas:
- Contract tests and other test types: see Area 4 (TST-8).
- Dependency pinning, lock files, SBOM, licence compliance and provenance: see Area 9.
- Release versioning, changelogs, database migrations and rollback: see Area 11.
- Integration and import behaviour (validation, idempotency) and data ownership over time: see Area 14.
- File import and export contracts (format, schema, encoding, frequency, failure contact, owner): see Area 14 (DAT-2).
- Vulnerability monitoring and remediation time frames for all dependencies: see Area 5 (SEC-11).
- The documentation system as a whole (where docs live, review, onboarding): see Area 16.

## Requirements

### ARC-1 · MUST · Architecture decision records
Significant architecture decisions MUST be recorded as ADRs (title, context, decision, status, consequences) kept in the
repository.
- **Gate:** G1
- **Evidence:** a `docs/decisions/` (or similar) folder of numbered ADRs, each with a status; each major technology choice in the
  codebase has a matching ADR.
- **Basis:** [NYGARD], [SWEBOK]. Level: author's judgement (sources support SHOULD).

### ARC-2 · MUST · Superseded decisions kept
A reversed or replaced decision MUST be kept and marked as superseded, with a link to its replacement, rather than deleted.
- **Gate:** G1
- **Evidence:** ADRs with status "superseded by ADR-NNN"; no ADR deletions in version-control history.
- **Basis:** [NYGARD]. Level: author's judgement (sources support SHOULD).

### ARC-3 · SHOULD · Alternatives and rationale recorded
Each ADR SHOULD record the alternatives considered and why they were rejected, as well as the chosen option.
- **Gate:** G1
- **Evidence:** an "Options considered" section in sampled ADRs.
- **Basis:** [SWEBOK].

### ARC-4 · MUST · System context description
The project MUST keep an up-to-date architecture description with at least a system context view showing the system, its
users, and every external system it depends on or serves.
- **Gate:** G1
- **Evidence:** a context diagram (for example C4 level 1) in the repository docs that matches the integrations present in the
  code and configuration.
- **Basis:** [C4], [ISO42010]. Level: author's judgement (sources support SHOULD).

### ARC-5 · SHOULD · Recognised view structure
Architecture views SHOULD follow a recognised structure, such as C4 (context, containers, components) or the ISO/IEC/IEEE 42010
concepts of viewpoints and views.
- **Gate:** G1
- **Evidence:** the diagrams and their notation key.
- **Basis:** [C4], [ISO42010].

### ARC-6 · MUST · API and event contracts documented and owned
Every external API or event contract (APIs and events exposed to other teams or clients) MUST be documented in a
machine-readable form with a named owner. File import and export contracts: DAT-2.
- **Gate:** G2
- **Evidence:** an OpenAPI (or equivalent schema) document per interface, generated or checked on every change, and an owner
  entry for each.
- **Basis:** [OPENAPI], [AIP-180]. Level: author's judgement (sources support SHOULD). The named owner: author's
  judgement.

### ARC-7 · MUST · Versioned public APIs
APIs used by consumers outside the team MUST carry an explicit major version, with breaking changes released only under a new
major version.
- **Gate:** G2
- **Evidence:** a version in the URI, package or schema; a written API change policy; no breaking change under an existing
  major version in the change history.
- **Basis:** [AIP-185], [AIP-180], [SEMVER] (rule 8 is a MUST for software that uses SemVer). Level: author's judgement
  (sources support SHOULD). Release versioning and changelogs: REL-5.

### ARC-8 · SHOULD · Consistent error format
HTTP APIs SHOULD return errors in one consistent, documented, machine-readable format, such as RFC 9457 Problem Details.
- **Gate:** G2
- **Evidence:** sampled error responses share one schema, and the schema is documented.
- **Basis:** [RFC9457].

### ARC-9 · SHOULD · Documented data model
The data model (entities, relationships, ownership, and the meaning of each field that carries business rules) SHOULD be
documented and kept in step with schema changes.
- **Gate:** G2
- **Evidence:** an entity-relationship diagram or schema document whose last update matches the latest schema change.
- **Basis:** Author's judgement (no primary source found).

### ARC-10 · SHOULD · Explicit domain boundaries
Where parts of the system use different models of the same concept, the boundary (bounded context) and the translation
between the models SHOULD be documented, with the translation code kept in one place.
- **Gate:** G2
- **Evidence:** a context map, and mapping code located in one module per boundary.
- **Basis:** [FOWLER-BC]. Translation code kept in one place: author's judgement.

### ARC-11 · SHOULD · Build-vs-buy decisions recorded
Build-vs-buy decisions and major technology choices SHOULD be documented, including total cost of ownership and how the
choice can be reversed later.
- **Gate:** G1 · **Trigger:** each new major component, technology or vendor choice
- **Evidence:** an ADR or decision note per major component or vendor, with a cost section and an exit note.
- **Basis:** [GOVUK-P11].

### ARC-12 · MUST · Vendored code marked and licensed
Vendored or copied third-party code MUST sit in a clearly marked location together with its licence, origin, version, and a
record of local modifications.
- **Gate:** G1 · **Trigger:** each newly vendored or copied package
- **Evidence:** a `third_party/` (or similar) folder with a licence file and a metadata file (origin, version, local changes)
  per package.
- **Basis:** [G-3P]. Level: author's judgement (sources support SHOULD). The origin, version and record of local
  modifications: author's judgement.

### ARC-13 · MUST · Vendored code owned and patched
Each vendored package MUST have a named owner who monitors it for upstream vulnerabilities and applies fixes.
- **Gate:** G1 · **Trigger:** each upstream vulnerability or security fix in a vendored package
- **Evidence:** an owner entry per vendored package, and a record of upstream updates or security patches applied within the
  remediation time frames of SEC-11.
- **Basis:** [G-3P]. Level: author's judgement (sources support SHOULD). Remediation time frames: SEC-11.

## Failure modes

- **Undocumented decisions.** Without recorded motivation, newcomers either accept or reverse past decisions blindly
  [NYGARD].
- **Rationale lost.** Rejected options are not recorded, so the team revisits them without knowing why they were rejected
  [SWEBOK].
- **Accidental contracts.** Interfaces are "sometimes accidentally grown" and never specified or tested, so changes break
  consumers silently [PRACTICAL-PYRAMID].
- **Unversioned breaking changes.** Old clients stop working, although "Existing client code must not be broken by a service
  updating to a new minor or patch release." [AIP-180]
- **Abandoned vendored code.** Copied in once and never upgraded: "Do not expect to check in open source code at Google and
  never have to touch it or maintain it." [G-3P]
- **Stale diagrams.** Architecture diagrams that no longer match the code. Author's judgement.

## References

- **[AIP-180]** AIP-180: Backwards compatibility. Google API Improvement Proposals. https://google.aip.dev/180. Accessed 2026-10-31.
  > "APIs are fundamentally contracts with users" (introduction)
  > "Existing client code must not be broken by a service updating to a new minor or patch release." (Guidance)
- **[AIP-185]** AIP-185: API Versioning. Google API Improvement Proposals. https://google.aip.dev/185. Accessed 2026-10-31.
  > "All Google API interfaces must provide a major version number , which is encoded at the end of the protobuf package, and included as the first part of the URI path for REST APIs." (the space before the comma is the page's own)
- **[C4]** The C4 model for visualising software architecture; System context diagram. Simon Brown, c4model.com. https://c4model.com/ ; https://c4model.com/diagrams/system-context. Accessed 2026-10-31.
  > "Draw a diagram showing your system as a box in the centre, surrounded by its users and the other systems that it interacts with." (introduction)
  > "Yes, a system context diagram is recommended for all software development teams." (Recommended?)
- **[FOWLER-BC]** BoundedContext. Martin Fowler, martinfowler.com, 15 January 2014. https://martinfowler.com/bliki/BoundedContext.html. Accessed 2026-10-31.
  > "DDD deals with large models by dividing them into different Bounded Contexts and being explicit about their interrelationships."
- **[G-3P]** Third-Party; //third_party Owners' and Users' Responsibilities. Google Open Source. https://opensource.google/documentation/reference/thirdparty ; https://opensource.google/documentation/reference/thirdparty/responsibilities. Accessed 2026-10-31.
  > "Important: All third party code must have a license ." (introduction)
  > "Monitor Vulnerabilities: You need to monitor upstream source code for security vulnerabilities." (introduction)
  > "Do not expect to check in open source code at Google and never have to touch it or maintain it." (introduction)
- **[GOVUK-P11]** Service Standard, 11. Choose the right tools and technology. UK Government Digital Service. https://www.gov.uk/service-manual/service-standard/point-11-choose-the-right-tools-and-technology. Accessed 2026-10-31.
  > "be able to show that they’ve made good decisions about what technology to build and what to buy, including use of common platforms where appropriate" (What it means)
  > "understand total cost of ownership of the technology and preserve the ability to make different choices in future" (What it means)
- **[ISO42010]** ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description. ISO/IEC/IEEE. https://www.iso.org/standard/74393.html. Accessed 2026-10-31. Paywalled; public abstract only. Mirror: https://committee.iso.org/standard/74393.html (verified 2026-10-31 on the committee.iso.org mirror; www.iso.org blocks automated access).
  > "This document specifies requirements for the structure and expression of an architecture description (AD) for various entities, including software, systems, enterprises"
- **[NYGARD]** Documenting Architecture Decisions. Michael Nygard, Cognitect blog, 15 November 2011. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions. Accessed 2026-10-31.
  > "One of the hardest things to track during the life of a project is the motivation behind certain decisions." (Context)
  > "We will keep ADRs in the project repository under doc/arch/adr-NNN.md" (introduction)
  > "If a decision is reversed, we will keep the old one around, but mark it as superseded." (introduction)
- **[OPENAPI]** OpenAPI Specification v3.1.1. OpenAPI Initiative, 24 October 2024. https://spec.openapis.org/oas/v3.1.1.html. Accessed 2026-10-31.
  > "The OpenAPI Specification (OAS) defines a standard, programming language-agnostic interface description for HTTP APIs"
- **[PRACTICAL-PYRAMID]** The Practical Test Pyramid. Ham Vocke, martinfowler.com, 26 February 2018. https://martinfowler.com/articles/practical-test-pyramid.html. Accessed 2026-10-31. (Cited here for a failure mode; the contract-test requirement it supports is TST-8 in Area 4.)
  > "services need to communicate with each other via certain (hopefully well-defined, sometimes accidentally grown) interfaces."
- **[RFC9457]** RFC 9457 Problem Details for HTTP APIs. M. Nottingham, E. Wilde, S. Dalal, IETF, July 2023 (obsoletes RFC 7807). https://www.rfc-editor.org/rfc/rfc9457.html. Accessed 2026-10-31.
  > "This document defines a "problem detail" to carry machine-readable details of errors in HTTP response content to avoid the need to define new error response formats for HTTP APIs."
- **[SEMVER]** Semantic Versioning 2.0.0. Tom Preston-Werner. https://semver.org/. Accessed 2026-10-31.
  > "Software using Semantic Versioning MUST declare a public API." (Semantic Versioning Specification (SemVer))
  > "Major version X (X.y.z | X > 0) MUST be incremented if any backward incompatible changes are introduced to the public API." (rule 8)
- **[SWEBOK]** Guide to the Software Engineering Body of Knowledge (SWEBOK Guide) v4.0a. H. Washizaki (ed.), IEEE Computer Society. https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf. Accessed 2026-10-31.
  > "Design rationale captures why a design decision was made. This includes prior assumptions made, alternatives considered, and trade-offs and criteria analyzed to select one approach and reject others." (Software Design KA, 4.6)
  > "Recording rejected decisions and the reasons for their rejection can also be useful." (Software Architecture KA)
