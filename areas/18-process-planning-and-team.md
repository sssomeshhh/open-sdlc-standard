# 18. Process, planning and team

- **ID prefix:** PRC
- **Status:** draft, 2026-10-31

## Purpose
This area makes sure work is visible, ordered and owned, that changes to production are controlled, and that the
team learns and improves over time. Without it, work happens off the books, risks surface only when they hit,
technical debt grows unseen, and nobody can show whether delivery is getting better or worse. It also guards against
the opposite failure: heavyweight process and misused metrics that slow delivery without making it safer.

## Scope
Issue tracking and backlog, change management, roles and ownership, risk register, batch size, estimation and
capacity, retrospectives, technical debt, and delivery and quality metrics (this area owns the DORA metrics and
technical debt). It leaves to other areas:

- Definition of done and code review guidelines: see Area 3.
- Required reviews and branch protection settings: see Area 7.
- Release approval and rollback: see Area 11.
- Incident management and post-mortems: see Area 12.
- Linking issues to changes, tests and releases: see Area 17.
- Ordering the backlog so the first release solves a core need: see PRD-14 (the backlog itself is PRC-1).
- Vendor and third-party risk: see Area 20.

## Requirements

### PRC-1 · MUST · Single ordered backlog
All planned work, defects and change requests MUST be recorded in one issue tracker that serves as the project's
ordered backlog.
- **Gate:** G1
- **Evidence:** the tracker exists; after the first release, work in the last release maps to tracker items; the backlog has an explicit
  order or priority.
- **Basis:** [SCRUM].

### PRC-2 · MUST · Written change process
Changes to the production system MUST follow a written change process that defines change types (for example
standard and emergency), who reviews and approves each type, how impact is assessed, and where the decision is
recorded.
- **Gate:** G3
- **Evidence:** the written process; for a sample of production changes, an approval and an impact note exist and
  are retained.
- **Basis:** [SP800-53] (CM-3, CM-4).

### PRC-3 · SHOULD · Peer review instead of a change board
Routine change approval SHOULD be done by peer review when code is checked in, not by an external change board, with
emergency changes going through the same pipeline.
- **Note:** a separate board can be added where a regulation requires one.
- **Gate:** G1
- **Evidence:** review required at merge (see Area 7); no separate manual board gate for standard changes; emergency
  changes visible in the same pipeline history.
- **Basis:** [DORA-CA].

### PRC-4 · MUST · Roles and responsibilities defined
Roles across the life cycle (who decides, approves, builds, reviews and operates) MUST be written down with named
people and reviewed periodically.
- **Gate:** G0
- **Evidence:** a roles document (for example a RACI table) with names, a review interval set in that document, and a
  last-review date within it.
- **Basis:** [SSDF] (PO.2.1), [SP800-53] (SA-3).

### PRC-5 · MUST · Risk register
The project MUST keep a risk register in which each risk has an owner, a likelihood and impact rating, a response
and a last-review date, and which is reviewed on a schedule and after significant change.
- **Gate:** G0 · **Trigger:** each significant change
- **Evidence:** the register with those fields filled per entry; the review interval and what counts as significant
  change stated in the register; review dates within that interval.
- **Basis:** [NISTIR8286], [SP800-53] (RA-3, PM-9). Level: author's judgement (sources support SHOULD).

### PRC-6 · SHOULD · Small batches
Work SHOULD be split into batches that can be completed and checked in one week or less.
- **Gate:** G1
- **Evidence:** median issue cycle time and change size; items larger than a week are split.
- **Basis:** [DORA-BATCH].

### PRC-7 · SHOULD · Estimates compared with actuals
Estimates and capacity plans SHOULD be recorded and compared with actual results so planning improves over time.
- **Gate:** G2
- **Evidence:** iteration plans with estimates and completed work; a recorded review of the variance.
- **Basis:** Author's judgement (no primary source found).

### PRC-8 · MUST · Retrospectives with tracked actions
The team MUST hold regular retrospectives and track the resulting improvement actions to completion.
- **Gate:** G2
- **Evidence:** dated retrospective notes; actions with owners recorded in the tracker; closed actions over time.
- **Basis:** [SCRUM]. Level: author's judgement (sources support SHOULD). Tracking actions to completion: author's
  judgement.

### PRC-9 · MUST · Technical debt recorded
Known technical debt MUST be recorded as backlog items that state its cost (the extra effort it causes).
- **Gate:** G2
- **Evidence:** debt items in the tracker, labelled as such, each with a description of its cost.
- **Basis:** [CUNNINGHAM-DEBT]. Level: author's judgement (sources support SHOULD).

### PRC-10 · SHOULD · Planned debt repayment
Technical debt SHOULD be repaid on a planned basis, either through a set share of capacity or through explicit
items scheduled each period.
- **Gate:** G2
- **Evidence:** debt items scheduled and closed in each period's plan.
- **Basis:** [CUNNINGHAM-DEBT]. Author's judgement (no primary source states the capacity mechanism).

### PRC-11 · SHOULD · DORA delivery metrics
The project SHOULD measure software delivery performance at the application or service level using the DORA
metrics: change lead time, deployment frequency, change fail rate, failed deployment recovery time and deployment
rework rate.
- **Gate:** G3
- **Evidence:** written metric definitions; a dashboard or report with history.
- **Basis:** [DORA-METRICS].

### PRC-12 · SHOULD · Metrics in tension tracked together
Throughput metrics SHOULD be tracked together with stability and quality metrics, so that improving one is not
bought at the cost of another.
- **Gate:** G3
- **Evidence:** the metric report shows speed and stability metrics side by side.
- **Basis:** [DORA-METRICS].

### PRC-13 · MUST · Metrics used for improvement, not ranking
Delivery metrics MUST be used to improve the team's own performance over time, not to rank teams or as targets in
themselves.
- **Gate:** G3
- **Evidence:** a written metric policy; no team league tables or individual targets set on the metrics.
- **Basis:** [DORA-METRICS], [DORA-VM]. Level: author's judgement (sources support SHOULD).

### PRC-14 · SHOULD · Visible work in progress
Work in progress SHOULD be visible to the whole team on a shared board.
- **Note:** work-in-progress limits can be set on it.
- **Gate:** G1
- **Evidence:** a board that reflects the current state of work.
- **Basis:** [DORA-VM].

## Failure modes
- Heavyweight external change approval that slows delivery without lowering failure rates; DORA reports that "these
  approaches have a negative impact on software delivery performance" [DORA-CA].
- Metrics turned into mandates or comparisons between teams, which invites gaming [DORA-METRICS].
- Large batches that take weeks to finish and review: "Any batch of code that takes longer than a week to complete
  and check is too big." [DORA-BATCH].
- Retrospectives held but actions never tracked or closed. (Author's judgement.)
- Technical debt kept as tribal knowledge instead of backlog items, so its cost grows unseen [CUNNINGHAM-DEBT].
- A risk register written once at project start and never reviewed, contrary to [SP800-53] (RA-3). (Author's
  judgement.)

## References
- **[CUNNINGHAM-DEBT]** The WyCash Portfolio Management System, OOPSLA '92 Experience Report. Ward Cunningham.
  https://c2.com/doc/oopsla92.html. Accessed 2026-10-31.
  > "Shipping first time code is like going into debt." (introduction)
  > "Every minute spent on not-quite-right code counts as interest on that debt." (introduction)
- **[DORA-BATCH]** Capabilities: Working in small batches. DORA.
  https://dora.dev/capabilities/working-in-small-batches/. Accessed 2026-10-31.
  > "Any batch of code that takes longer than a week to complete and check is too big." (Common pitfalls with working in small batches)
  > "Application features are sliced in a way that lets developers complete the work in one week or less." (Ways to measure the size of work batches)
- **[DORA-CA]** Capabilities: Streamlining change approval. DORA.
  https://dora.dev/capabilities/streamlining-change-approval/. Accessed 2026-10-31.
  > "However, DORA's research shows that these approaches have a negative impact on software delivery performance." (How to implement a change approval process)
  > "change approvals are best implemented through peer review during the development process" (introduction)
  > "Moving to a peer-review based process for individual changes, enforced at code check-in time" (Ways to improve your change approval process)
- **[DORA-METRICS]** DORA's software delivery performance metrics. DORA. https://dora.dev/guides/dora-metrics-four-keys/.
  Accessed 2026-10-31. The URL now redirects to https://dora.dev/guides/dora-metrics/; the page names five metrics,
  including deployment rework rate. Page by Nathen Harvey.
  > "DORA has identified five software delivery performance metrics"
  > "The amount of time it takes for a change to go from committed to version control to deployed in production." (Throughput)
  > "The goal is to improve your team's performance over time, not to compete against other teams or organizations." (Common pitfalls)
  > "Teams should identify multiple metrics, including some with a healthy amount of tension between them." (Common pitfalls)
- **[DORA-VM]** Capabilities: Visual management. DORA. https://dora.dev/capabilities/visual-management/. Accessed
  2026-10-31.
  > "Visual management boards can create a shared understanding of where the team is" (introduction)
  > "Displays should be used to drive improvements (fix the problem), not become a goal in themselves (keep the board green)." (Common pitfalls with visual management)
- **[NISTIR8286]** NIST IR 8286 Rev. 1, Integrating Cybersecurity and Enterprise Risk Management (ERM). NIST, December
  2025. https://csrc.nist.gov/pubs/ir/8286/r1/final. Accessed 2026-10-31.
  > "This document includes guidance on the use of risk registers to set out cybersecurity risk"
- **[SCRUM]** The Scrum Guide (2020). Ken Schwaber and Jeff Sutherland. https://scrumguides.org/scrum-guide.html.
  Accessed 2026-10-31.
  > "The Product Backlog is an emergent, ordered list of what is needed to improve the product." (Product Backlog)
  > "The purpose of the Sprint Retrospective is to plan ways to increase quality and effectiveness." (Sprint Retrospective)
- **[SP800-53]** NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations. NIST.
  Control text from NIST's official OSCAL catalog (release 5.2.0):
  https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json;
  publication page https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final. Accessed 2026-10-31.
  > "Determine and document the types of changes to the system that are configuration-controlled;" (CM-3)
  > "Review proposed configuration-controlled changes to the system and approve or disapprove such changes with explicit consideration for security and privacy impact analyses;" (CM-3)
  > "Document configuration change decisions associated with the system;" (CM-3)
  > "Analyze changes to the system to determine potential security and privacy impacts prior to change implementation." (CM-4)
  > "Define and document information security and privacy roles and responsibilities throughout the system development life cycle;" (SA-3)
  > "Document risk assessment results in" (RA-3; organisation-defined document)
  > "Review risk assessment results" (RA-3; organisation-defined frequency)
  > "Review and update the risk management strategy" (PM-9; organisation-defined frequency)
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST, February 2022.
  https://doi.org/10.6028/NIST.SP.800-218. Accessed 2026-10-31.
  > "Periodically review and maintain the defined roles and responsibilities, updating them as needed." (PO.2.1)
