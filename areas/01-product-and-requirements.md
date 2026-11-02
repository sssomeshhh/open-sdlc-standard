# 1. Product and requirements

- **ID prefix:** PRD
- **Status:** draft, 2026-10-31

## Purpose

This area protects against building the wrong thing, or building the right thing without knowing whether it worked. It
covers how the problem, the measure of success, the scope and the requirements are written down before and during build,
in a form that can be tested. It also owns user acceptance testing (UAT) and its sign-off, the point where users confirm the
product meets its acceptance criteria.

## Scope

Covers: problem statement and business case, measurable success criteria (KPIs), discovery and user research, feasibility,
scope and non-goals, the written specification, functional requirements and their acceptance criteria, non-functional
requirements (NFRs), the domain glossary, backlog prioritisation, and UAT with its recorded sign-off.

Leaves to other areas:
- Test types, test strategy, performance, security and accessibility testing: see Area 4.
- The full requirement → design → code → test → release → incident chain: see Area 17. This area only covers that each
  requirement has a recorded source (PRD-7); identifiers: TRC-1.
- The single ordered backlog itself: see Area 18 (PRC-1).
- Accessibility and internationalisation requirements themselves: see Area 15.
- Product and usage telemetry used to measure KPIs: see Area 13.
- Release communication, user support and the feedback loop after release: see Area 20.

## Requirements

### PRD-1 · MUST · Problem statement before build
Before build starts, the project MUST record the problem it solves, framed as a user or business problem rather than as a
pre-chosen solution.
- **Gate:** G0
- **Evidence:** a problem statement or discovery report, dated before the first feature commit, that says what is wrong today
  and for whom.
- **Basis:** [GOVUK-DISC], [GOVUK-P1]. Level: author's judgement (sources support SHOULD).

### PRD-2 · MUST · Measurable success criteria
The project MUST state its success criteria (KPIs), each with a baseline, a target and the method and data source used to
measure it.
- **Gate:** G0
- **Evidence:** a KPI list with baseline, target, and the method and data source per KPI. Measurement after release: OBS-14.
- **Basis:** [GOVUK-P10]. Level: author's judgement (sources support SHOULD). Baseline per KPI: author's judgement ([GOVUK-P10]
  asks for metrics and tracking performance against them).

### PRD-3 · SHOULD · Business case with the cost of the problem
The business case SHOULD estimate the value of solving the problem, including what the problem costs today, and state its
assumptions.
- **Gate:** G0
- **Evidence:** a business case or discovery note with a cost/value estimate and its listed assumptions.
- **Basis:** [GOVUK-DISC].

### PRD-4 · SHOULD · User research written down and shared
Discovery SHOULD include research with real current or prospective users, with the findings written down and shared with the
team and sponsor.
- **Gate:** G0
- **Evidence:** a research plan, session notes or synthesis, and a findings document with its distribution recorded.
- **Basis:** [USDS], [GOVUK-P1]. Sharing with the team and sponsor: author's judgement.

### PRD-5 · SHOULD · Feasibility and go/stop decision
The project SHOULD list its hard and soft constraints (legislation, contracts, legacy technology, existing processes) and
record a dated go/stop decision at the end of discovery.
- **Gate:** G0
- **Evidence:** a constraints register and a dated go/no-go decision record.
- **Basis:** [GOVUK-DISC].

### PRD-6 · SHOULD · Written, versioned specification
Requirements SHOULD be kept in a written specification under version control (in the repository, or in a document system linked
from it), not only in conversations, tickets or people's heads.
- **Gate:** G1
- **Evidence:** a specification file or linked document with a change history; sampled features in the code have a matching
  entry.
- **Basis:** Author's judgement; [ISO29148] public abstract only.

### PRD-7 · SHOULD · Requirement sources
Each requirement SHOULD record its source (stakeholder, regulation, contract or research finding). Its stable identifier is
required by TRC-1.
- **Gate:** G1
- **Evidence:** sampled requirements each show a source field.
- **Basis:** [SWEBOK].

### PRD-8 · MUST · Scope and non-goals
The specification MUST state what is in scope, what is out of scope, and explicit non-goals.
- **Gate:** G0
- **Evidence:** a scope section with in-scope, out-of-scope and non-goal lists; change requests refer to it.
- **Basis:** [GOVUK-DISC]. Level: author's judgement (sources support SHOULD).

### PRD-9 · MUST · Testable acceptance criteria
Each functional requirement or user story MUST have acceptance criteria that can be shown to pass or fail.
- **Gate:** G1
- **Evidence:** sampled backlog items each have acceptance criteria (for example Given/When/Then) that a tester could execute.
- **Basis:** [SWEBOK], [INVEST], [FOWLER-GWT]. Level: author's judgement (sources support SHOULD).

### PRD-10 · SHOULD · Requirements reviewed for quality
Requirements SHOULD be checked before acceptance against stated quality properties: unambiguous, testable, atomic, consistent,
and in stakeholder vocabulary.
- **Gate:** G1
- **Evidence:** a requirements review checklist, and review comments or sign-off on the requirements set.
- **Basis:** [SWEBOK], [ISO29148]. The property list other than "testable": author's judgement.

### PRD-11 · MUST · Measurable non-functional requirements
Non-functional requirements (for example performance, security, availability, accessibility, maintainability) MUST be written
down with measurable thresholds, using a recognised quality model as the checklist.
- **Gate:** G0
- **Evidence:** an NFR section mapped to the chosen quality model (for example ISO/IEC 25010), each NFR with a number or a
  test.
- **Basis:** [ISO25010], [SWEBOK]. Level: author's judgement (sources support SHOULD).

### PRD-12 · SHOULD · Small, testable user stories
User stories SHOULD follow INVEST: independent, negotiable, valuable, estimable, small, testable.
- **Gate:** G1
- **Evidence:** a story template; sampled stories are small enough to estimate and are testable.
- **Basis:** [INVEST].

### PRD-13 · SHOULD · Domain glossary
The project SHOULD keep a domain glossary (ubiquitous language) whose terms are used consistently in requirements, UI and code.
- **Gate:** G1
- **Evidence:** a glossary file; sampled terms appear consistently in specifications and code identifiers.
- **Basis:** [FOWLER-UBIQ].

### PRD-14 · SHOULD · First release solves a core need
The backlog (one ordered backlog: PRC-1) SHOULD be ordered so that the first release solves a core user need.
- **Gate:** G1
- **Evidence:** a release plan that names the first release's scope and the user need it solves.
- **Basis:** [USDS] for the prioritised backlog. First release solving a core need: author's judgement.

### PRD-15 · MUST · UAT with recorded sign-off
Before release to users, user acceptance testing MUST be run by or with end users against the acceptance criteria, and the
result and the sign-off decision recorded.
- **Gate:** G3 · **Trigger:** each release that adds or significantly changes what users can do
- **Evidence:** a UAT plan, executed checklists with tester and date, a defect log, and the signed-off decision.
- **Basis:** [SWEBOK], [DORA-TA]. Level: author's judgement (sources support SHOULD; no fetched source requires formal
  sign-off).

### PRD-16 · MAY · Executable acceptance specifications
Acceptance tests MAY be agreed with domain experts before implementation (ATDD/BDD) and automated.
- **Gate:** G1
- **Evidence:** executable acceptance specifications committed before or with the feature.
- **Basis:** [FOWLER-GWT].

## Failure modes

- **Solution-first projects.** Teams build a pre-defined solution without testing the problem; the real problem "might not be
  the one you originally thought needed solving" [GOVUK-P1].
- **No success measure.** Without defined metrics, nobody can tell "whether the service is solving the problem it’s meant to
  solve" [GOVUK-P10].
- **Untestable requirements.** "Natural languages are inherently ambiguous, but test case language is not." [SWEBOK]
- **NFRs left implicit.** Performance, security and accessibility needs are discovered at UAT or in production. Author's
  judgement.
- **Scope creep.** Nobody agreed "what is not part of the problem" [GOVUK-DISC].
- **UAT as a formality.** UAT is run late, by the developers rather than the users, with no recorded criteria. Author's
  judgement.

## References

- **[DORA-TA]** Capabilities: Test automation. DORA. https://dora.dev/capabilities/test-automation/. Accessed 2026-10-31.
  > "Perform manual test activities such as exploratory testing, usability testing, and acceptance testing throughout the delivery process."
- **[FOWLER-GWT]** GivenWhenThen. Martin Fowler, martinfowler.com, 21 August 2013. https://martinfowler.com/bliki/GivenWhenThen.html. Accessed 2026-10-31.
  > "Given-When-Then is a style of representing tests - or as its advocates would say - specifying a system's behavior using SpecificationByExample ."
- **[FOWLER-UBIQ]** UbiquitousLanguage. Martin Fowler, martinfowler.com, 31 October 2006. https://martinfowler.com/bliki/UbiquitousLanguage.html. Accessed 2026-10-31.
  > "the practice of building up a common, rigorous language between developers and users. This language should be based on the Domain Model used in the software"
- **[GOVUK-DISC]** How the discovery phase works. Service Manual, UK Government Digital Service. https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works. Accessed 2026-10-31.
  > "Before you commit to building a service, you need to understand the problem that needs to be solved." (introduction)
  > "Reframing the problem also includes agreeing what is not part of the problem." (Define the problem)
  > "During discovery, that means understanding how much the problem is currently costing." (Define the problem)
  > "If there’s a hard constraint which means you are not able to improve on the solution that’s currently available, it might be worth stopping at the end of discovery." (Understanding constraints)
- **[GOVUK-P1]** Service Standard, 1. Understand users and their needs. UK Government Digital Service. https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs. Accessed 2026-10-31.
  > "The real problem might not be the one you originally thought needed solving. Testing your assumptions early and often reduces the risk of building the wrong thing."
- **[GOVUK-P10]** Service Standard, 10. Define what success looks like and publish performance data. UK Government Digital Service. https://www.gov.uk/service-manual/service-standard/point-10-define-success-publish-performance-data. Accessed 2026-10-31.
  > "Defining what good looks like and identifying appropriate metrics means that you’ll know whether the service is solving the problem it’s meant to solve." (Why it’s important)
  > "identify metrics which will indicate how well the service is solving the problem it’s meant to solve, and track performance against them" (What it means)
- **[INVEST]** INVEST in Good Stories, and SMART Tasks. Bill Wake, XP123, 17 August 2003. https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/. Accessed 2026-10-31. Spaces before full stops in the quotes are the page's own.
  > "A good story is testable . Writing a story card carries an implicit promise: “I understand what I want well enough that I could write a test for it.”" (Testable)
  > "Good stories tend to be small . Stories typically represent at most a few person-weeks worth of work." (Small)
- **[ISO25010]** ISO/IEC 25010:2023 Systems and software engineering — SQuaRE — Product quality model. ISO/IEC. https://www.iso.org/standard/78176.html. Accessed 2026-10-31. Paywalled; public abstract only. Mirror: https://committee.iso.org/standard/78176.html (verified 2026-10-31 on the committee.iso.org mirror; www.iso.org blocks automated access).
  > "The product quality model is composed of nine characteristics (which are further subdivided into subcharacteristics) that relate to quality properties of the products." (introduction)
  > "identifying acceptance criteria for a product and/or an information system" (introduction)
- **[ISO29148]** ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering. ISO/IEC/IEEE. https://www.iso.org/standard/72089.html. Accessed 2026-10-31. Paywalled; public abstract only. Mirror: https://committee.iso.org/standard/72089.html (verified 2026-10-31 on the committee.iso.org mirror; www.iso.org blocks automated access). The catalogue lists it as "International Standard to be revised".
  > "specifies the required processes implemented in the engineering activities that result in requirements for systems and software products (including services) throughout the life cycle" (introduction)
  > "specifies the required contents of the required information items" (introduction)
- **[SWEBOK]** Guide to the Software Engineering Body of Knowledge (SWEBOK Guide) v4.0a. H. Washizaki (ed.), IEEE Computer Society. https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf. Accessed 2026-10-31.
  > "be testable (quantified), meaning that compliance or noncompliance can be clearly demonstrated" (Software Requirements KA, 3.1)
  > "Natural languages are inherently ambiguous, but test case language is not." (Software Requirements KA, 4.3)
  > "Software requirements can be traced back to source documentation such as system requirements, standards documents and other relevant specifications." (Software Requirements KA)
  > "Acceptance testing targets the deployment of a SUT. Its main goal is to verify that the SUT satisfies the requirements and the end-users’ expectations." (Software Testing KA, 2.1.4)
- **[USDS]** Digital Services Playbook. U.S. Digital Service. https://playbook.usds.gov/. Accessed 2026-10-31.
  > "Document the findings about user goals, needs, behaviors, and preferences" (Play 1)
  > "Create a prioritized list of features and bugs, also known as the “feature backlog” and “bug backlog”" (Play 4)
