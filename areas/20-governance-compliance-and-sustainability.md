# 20. Governance, compliance and sustainability

- **ID prefix:** GOV
- **Status:** draft, 2026-10-31

## Purpose
This area makes sure that someone accountable decides when a system is allowed to operate, that suppliers and external
services are known and assessed, that users are told about and supported through each release, and that the system
has an owner and a maintenance plan for its whole life, including a planned end. Without it, systems go live
without a decision on record, depend on unassessed vendors, run on unsupported components, and are left unowned or
switched off with data and credentials left behind.

## Scope
Authorisation to operate, supplier and third-party risk, inventory of external services, end-of-life tracking,
release communication, user training, support model and feedback loop, long-term maintenance, and decommissioning
(this area owns release communication, support, the feedback loop and decommissioning). It leaves to other areas:

- Acceptance criteria and UAT sign-off: see Area 1.
- SBOM, dependency pinning and build provenance: see Area 9.
- Versioning, changelog and release mechanics: see Area 11.
- Data retention and deletion rules: see Areas 6 and 14.
- User documentation and in-app help: see Area 15.
- Documentation system and handover documents: see Area 16.
- Linking feedback items into the traceability chain: see Area 17.
- Assessing AI tools specifically: see Area 19.

## Requirements

### GOV-1 · MUST · Recorded authorisation to operate
A named accountable owner MUST authorise the system to operate before first go-live, in a recorded decision that
references the acceptance results from Area 1.
- **Note:** this covers the first go-live; approval of each deployment is REL-7.
- **Gate:** G3
- **Evidence:** a recorded go-live approval naming the owner and the date, referencing the UAT sign-off.
- **Basis:** [SP800-53] (CA-6, SA-4).

### GOV-2 · SHOULD · Re-authorisation on significant change
The authorisation to operate SHOULD be revisited on significant change (for example a major release or an
architecture change), not given once for ever.
- **Gate:** G3 · **Trigger:** each significant change (for example a major release or an architecture change)
- **Evidence:** re-approval records for major releases and architecture changes.
- **Basis:** [SP800-53] (CA-6). Trigger on significant change: author's judgement (CA-6 sets an organisation-defined
  frequency).

### GOV-3 · MUST · Suppliers assessed before use
Third-party suppliers and external services (cloud, SaaS, contractors, AI providers) MUST be listed and assessed for
risk before use.
- **Gate:** G1 · **Trigger:** each new supplier or external service
- **Evidence:** a supplier list with a risk rating and assessment date per entry, each dated before the supplier was
  first used.
- **Basis:** [SP800-53] (SR-6), [SP800-161].

### GOV-4 · MUST · Supplier terms cover security and privacy
The contract or terms with each supplier MUST be checked to meet the organisation's security and privacy
requirements and to identify the responsible parties.
- **Gate:** G1 · **Trigger:** each new supplier
- **Evidence:** contract clauses or reviewed terms of service per supplier, with the check recorded.
- **Basis:** [SP800-53] (SA-9, SA-4).

### GOV-5 · SHOULD · Suppliers reviewed periodically
Supplier risk SHOULD be reviewed periodically and when a supplier or its service changes.
- **Gate:** G1 · **Trigger:** a supplier or its service changes
- **Evidence:** the review interval stated on the supplier list; review dates within it.
- **Basis:** [SP800-53] (SR-6).

### GOV-6 · MAY · Supply-chain risk management plan
The project MAY keep a supply-chain risk management
plan that covers acquisition through to disposal and is reviewed on change.
- **Gate:** G1 · **Condition:** when the system first depends on several critical external suppliers · **Trigger:** a change to a critical supplier
- **Evidence:** the plan with a review date.
- **Basis:** [SP800-53] (SR-2), [SP800-161]. Condition: author's judgement.

### GOV-7 · MUST · Inventory of components and services
An inventory of system components and external services MUST be kept accurate and reviewed; the SBOM for software
components is defined in Area 9.
- **Gate:** G2
- **Evidence:** the component and service inventory with a review interval set in it and a last-review date within
  that interval; it matches what is deployed.
- **Basis:** [SP800-53] (CM-8), [SSDF] (PS.3.2).

### GOV-8 · MUST · End-of-life tracked and acted on
End-of-support dates for runtimes, frameworks, operating-system images and managed services MUST be tracked, with
each component replaced, or alternative support arranged, before support ends.
- **Gate:** G2
- **Evidence:** an end-of-life register with dates; upgrade plans for entries due within the next year; no component
  in production past end of support without a valid waiver (README, "Deviations and waivers").
- **Basis:** [SP800-53] (SA-22).

### GOV-9 · MUST · Release communication to users
Each release that changes what users see or do MUST be announced to the affected users, stating what changed and who
is affected. User documentation updates are covered by Area 15.
- **Gate:** G3 · **Trigger:** each release that changes what users see or do
- **Evidence:** a release announcement or user-facing release notes per such release.
- **Basis:** [KACL]. Level: author's judgement (sources support SHOULD). Content: author's judgement (Keep a Changelog
  supports human-readable notes only).

### GOV-10 · SHOULD · User training and guidance
Users SHOULD receive training or guidance for new or changed functionality before or at release.
- **Gate:** G3 · **Trigger:** each release with new or changed functionality
- **Evidence:** training material, session records or updated in-app guidance for the release.
- **Basis:** Author's judgement (no primary source found).

### GOV-11 · MUST · Defined support model
The project MUST define and publish how users get help, who handles which kind of request, and the expected
response times.
- **Gate:** G3
- **Evidence:** a published support route and ownership; after go-live, request records showing it is used.
- **Basis:** Author's judgement (no primary source found).

### GOV-12 · MUST · Feedback collected into the backlog
User feedback and support data MUST be collected through a known channel and fed into the backlog.
- **Gate:** G3
- **Evidence:** the feedback channel; backlog items that link to the feedback they came from (see Area 17).
- **Basis:** [DORA-FEEDBACK].

### GOV-13 · MUST · Long-term maintenance plan
The project MUST plan long-term maintenance: who maintains the system after delivery, how corrective, preventive,
adaptive and perfective changes are handled, and with what budget.
- **Gate:** G3
- **Evidence:** a maintenance plan; a named maintaining team; a handover record (see Area 16).
- **Basis:** [IEEE-14764] (maintenance planning begins with development planning), [IEEE-12207]. The four change
  categories and the budget are the author's judgement (not visible in the public abstract).

### GOV-14 · MUST · Planned decommissioning
Retirement MUST be planned before it happens, in a plan that covers: users told in advance, how their need will be
met afterwards, data retained, migrated or deleted under the data policy, credentials and infrastructure removed, and
residual risks recorded.
- **Gate:** G4
- **Evidence:** a decommissioning plan dated before switch-off began (checked in the G4 self-assessment) and a completed closure checklist; a record of what happened to each data set.
- **Basis:** [GOVUK-RETIRE], [SP800-53] (SR-12), [IEEE-12207].

### GOV-15 · SHOULD · Secure disposal throughout the life cycle
Data, documentation, credentials and components SHOULD be disposed of securely whenever they leave use, not only at
final retirement.
- **Gate:** G2 · **Trigger:** data, documentation, a credential or a component leaves use
- **Evidence:** a disposal procedure; records of key and secret revocation and storage deletion.
- **Basis:** [SP800-53] (SR-12).

### GOV-16 · MAY · Mapping to a life-cycle standard
The project MAY record how its process maps to a recognised life-cycle process standard (for example ISO/IEC/IEEE
12207).
- **Gate:** G1
- **Evidence:** a process description with the mapping.
- **Basis:** [IEEE-12207].

### GOV-17 · MUST · Formal audit by an independent assessor
The system MUST be formally audited against this standard before go-live, at least once a year after that and after each
major change, by an assessor who was not part of the delivery team during the period audited, did not write, approve or
review the work audited, and does not report to the system's lead or accountable owner.
- **Gate:** G3 · **Trigger:** each year after go-live, and each major change (as the project defines it)
- **Evidence:** dated audit records in the system's home repository, each citing the version of this standard used, with
  the assessor's declaration against the three independence criteria; the yearly audit dates.
- **Basis:** [SP800-53] (CA-2, CA-2(1)). Level, yearly interval and the reporting-line criterion: author's judgement (CA-2
  leaves the frequency to the organisation; the reporting-line criterion applies CA-2(1)'s "conflicts of interest
  regarding … management of the systems").

## Failure modes
- No named owner after the delivery team leaves; the system runs unowned until something breaks. (Author's
  judgement.)
- A vendor or SaaS adopted by one team without assessment or contract terms on security and data, leading to
  "decreased visibility into and understanding of how the technology they acquire is developed" [SP800-161].
- Runtimes and base images left past end of support, which SP 800-53 warns gives adversaries an opportunity to
  exploit weaknesses [SP800-53] (SA-22).
- Releases shipped silently: users learn about changes from errors, and support is not briefed. (Author's
  judgement.)
- "Switch-off" decommissioning: servers stopped but data, DNS records, credentials and backups left behind
  [SP800-53] (SR-12); "You should have a plan for securing the information you've got about your users."
  [GOVUK-RETIRE].

## References
- **[DORA-FEEDBACK]** Capabilities: Customer feedback. DORA. https://dora.dev/capabilities/customer-feedback/.
  Accessed 2026-10-31.
  > "Seek out and attend to customer feedback on product and feature quality."
- **[GOVUK-RETIRE]** Retiring your service. GOV.UK Service Manual, UK Government Digital Service.
  https://www.gov.uk/service-manual/phases/retirement. Accessed 2026-10-31.
  > "When retiring a service you should consider user needs in the same way you did when you built the service." (introduction)
  > "You need to consider how the user need your service met will be met after your service is retired." (Consider user needs)
  > "You should have a plan for securing the information you've got about your users." (Protecting information)
- **[IEEE-12207]** ISO/IEC/IEEE 12207:2017 Systems and software engineering — Software life cycle processes. IEEE SA.
  https://standards.ieee.org/ieee/12207/5672/. Accessed 2026-10-31. Paywalled; public abstract only. The page marks
  the 2017 edition as superseded. Its successor, ISO/IEC/IEEE 12207:2026, is listed on the ISO catalogue
  (https://committee.iso.org/standard/90219.html, verified 2026-10-31); the quotes below are from the 2017 abstract.
  > "This International Standard establishes a common framework for software life cycle processes" (abstract)
  > "during the supply, development, operation, maintenance and disposal of software products" (abstract)
- **[IEEE-14764]** ISO/IEC/IEEE 14764:2022 (IEEE 14764-2021) Software engineering — Software life cycle processes —
  Maintenance. IEEE SA. https://standards.ieee.org/ieee/14764/7701/. Accessed 2026-10-31. Paywalled; public abstract
  only.
  > "This standard describes an iterative process for managing and executing software maintenance activities." (abstract)
  > "Ideally, maintenance planning should begin during planning for software development." (abstract)
  > "Use of this standard is not restricted by size, complexity, criticality, or application of the software product." (abstract)
- **[KACL]** Keep a Changelog 1.1.0. Olivier Lacan. https://keepachangelog.com/en/1.1.0/. Accessed 2026-10-31.
  > "Changelogs are for humans, not machines."
- **[SP800-53]** NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations. NIST.
  Control text from NIST's official OSCAL catalog (release 5.2.0):
  https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json;
  publication page https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final. Accessed 2026-10-31.
  > "Ensure that the authorizing official for the system, before commencing operations:" (CA-6)
  > "Authorizes the system to operate;" (CA-6)
  > "Update the authorizations" (CA-6; organisation-defined frequency)
  > "Allocation of responsibility or identification of parties responsible for information security, privacy, and supply chain risk management; and" (SA-4)
  > "Acceptance criteria." (SA-4)
  > "Produce a control assessment report that document the results of the assessment; and" (CA-2)
  > "Employ independent assessors or assessment teams to conduct control assessments." (CA-2(1))
  > "Impartiality means that assessors are free from any perceived or actual conflicts of interest regarding the development, operation, sustainment, or management of the systems under assessment or the determination of control effectiveness." (CA-2(1))
  > "Require that providers of external system services comply with organizational security and privacy requirements and employ the following controls:" (SA-9)
  > "Assess and review the supply chain-related risks associated with suppliers or contractors and the system, system component, or system service they provide" (SR-6)
  > "Develop a plan for managing supply chain risks associated with the research and development, design, manufacturing, acquisition, delivery, integration, operations and maintenance, and disposal" (SR-2)
  > "Develop and document an inventory of system components that:" (CM-8)
  > "Accurately reflects the system;" (CM-8)
  > "Review and update the system component inventory" (CM-8; organisation-defined frequency)
  > "Replace system components when support for the components is no longer available from the developer, vendor, or manufacturer; or" (SA-22)
  > "Data, documentation, tools, or system components can be disposed of at any time during the system development life cycle" (SR-12, guidance)
- **[SP800-161]** NIST SP 800-161 Rev. 1 (update 1), Cybersecurity Supply Chain Risk Management Practices for Systems
  and Organizations. NIST, May 2022 (updated November 2024). https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final.
  Accessed 2026-10-31.
  > "The publication integrates cybersecurity supply chain risk management (C-SCRM) into risk management activities" (abstract)
  > "decreased visibility into and understanding of how the technology they acquire is developed" (abstract)
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST, February 2022.
  https://doi.org/10.6028/NIST.SP.800-218. Accessed 2026-10-31.
  > "Collect, safeguard, maintain, and share provenance data for all components of each software release (e.g., in a software bill of materials [SBOM])." (PS.3.2)
