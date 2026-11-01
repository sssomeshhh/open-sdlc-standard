# Research A: areas 1–4

Research notes for the Open SDLC Standard: candidate requirements, evidence and sources for areas 1–4. Prepared 2026-10-31.

**Method.** Each source page or PDF was fetched on 2026-10-31 and converted to plain text. Every quotation below was then checked word for word against that text. Quotes keep the source's own spelling and punctuation. ISO standards are paywalled. For those, only the public abstract on the ISO catalogue page is quoted, and the entry says so. Levels follow RFC 2119 / RFC 8174 and are candidate levels; the areas set the final ones. A requirement marked **[judgement]** has no direct source. A level that is stronger than its source (for example, a MUST where the source only describes good practice) is marked **(level: judgement)**.

---

## Area 1: Product and requirements

### Candidate requirements

1. **MUST**: Before build starts, the project records the problem it solves, framed as a user or business problem rather than as a pre-chosen solution.
   *Evidence:* a problem statement or discovery report, dated before the first feature commit, that says what is wrong today and for whom. *Sources:* GDS-DISC, GDS-P1. (level: judgement)
2. **MUST**: The project states measurable success criteria (KPIs), with a baseline and a target, and says how each will be measured.
   *Evidence:* a list of KPIs, the data source for each, and a record of measurements after release. *Sources:* GDS-P10, GDS-DISC, USDS. (level: judgement)
3. **SHOULD**: The business case estimates the value of solving the problem, including what the problem costs today.
   *Evidence:* a business case or discovery note with a cost/value estimate and its assumptions. *Sources:* GDS-DISC.
4. **SHOULD**: Discovery includes research with real current or prospective users, and the findings are written down and shared.
   *Evidence:* research plan, session notes or synthesis, and a findings document shared with the team and sponsor. *Sources:* USDS, GDS-P1.
5. **SHOULD**: Feasibility is assessed explicitly. The project lists hard and soft constraints (legislation, contracts, legacy technology, existing processes) and records a go/stop decision.
   *Evidence:* a constraints register and a dated go/no-go decision. *Sources:* GDS-DISC.
6. **MUST**: Scope is documented, including explicit non-goals (what is not part of the problem).
   *Evidence:* a scope section with in-scope, out-of-scope and non-goals lists. Change requests refer to it. *Sources:* GDS-DISC. (level: judgement)
7. **MUST**: Each functional requirement or user story has acceptance criteria that can be shown to pass or fail.
   *Evidence:* sampled backlog items. Each has acceptance criteria (for example Given/When/Then) that a tester could execute. *Sources:* SWEBOK, INVEST, FOWLER-GWT. (level: judgement)
8. **SHOULD**: Requirements meet stated quality properties: unambiguous, testable, atomic, consistent, and in stakeholder vocabulary. They are checked against these properties before being accepted.
   *Evidence:* a requirements review checklist, plus review comments or sign-off on the requirements set. *Sources:* SWEBOK, ISO29148.
9. **MUST**: Non-functional requirements (performance, security, availability, accessibility, maintainability and so on) are written down with measurable thresholds, using a recognised quality model as the checklist.
   *Evidence:* an NFR section mapped to the ISO/IEC 25010 characteristics, each with a number or a test. *Sources:* ISO25010, SWEBOK. (level: judgement)
10. **SHOULD**: User stories follow INVEST: independent, negotiable, valuable, estimable, small, testable.
    *Evidence:* a story template. Sampled stories are small enough to estimate and have tests. *Sources:* INVEST.
11. **SHOULD**: The project keeps a domain glossary (ubiquitous language). The same terms are used in requirements, UI and code.
    *Evidence:* a glossary file. Sampled terms appear consistently in specs and identifiers. *Sources:* FOWLER-UBIQ, SWEBOK.
12. **SHOULD**: Requirements are traceable backward to their source and forward to design, code and test cases, so that the impact of a change can be assessed.
    *Evidence:* requirement IDs referenced in issues, PRs and test names, or a traceability matrix. *Sources:* SWEBOK, ISO29148.
13. **SHOULD**: The backlog is prioritised, and the first release is a minimum viable product that solves a core user need.
    *Evidence:* an ordered backlog and a release plan that defines the MVP. *Sources:* USDS.
14. **MUST**: User acceptance testing (UAT) is run by or with end users against the acceptance criteria before release to users, and the result is recorded.
    *Evidence:* UAT plan, executed checklists with tester and date, a defect log, and the sign-off decision. *Sources:* SWEBOK, DORA-TA. (level: judgement)
15. **MAY**: Acceptance tests are agreed with domain experts before implementation (ATDD/BDD) and automated.
    *Evidence:* executable acceptance specs committed before or with the feature. *Sources:* SWEBOK, FOWLER-GWT.

### Failure modes

- **Solution-first projects.** Teams build a pre-defined solution without testing the problem. GOV.UK warns that the real problem "might not be the one you originally thought needed solving" (GDS-P1).
- **No success measure.** Without defined metrics, nobody can tell "whether the service is solving the problem it’s meant to solve" (GDS-P10).
- **Untestable requirements.** Natural-language requirements stay ambiguous. SWEBOK notes that "Natural languages are inherently ambiguous, but test case language is not" (SWEBOK).
- **NFRs left implicit.** Performance, security and accessibility are discovered at UAT or in production. SWEBOK notes that NFRs interact, and that a change to one should be checked for its "impact it may cause on others" (SWEBOK).
- **Scope creep.** Nobody agreed "what is not part of the problem" (GDS-DISC).
- **UAT as a formality.** UAT is run late, by the developers rather than the users, with no recorded criteria. [judgement]

---

## Area 2: Architecture and design

### Candidate requirements

1. **MUST**: Significant architecture decisions are recorded as Architecture Decision Records (title, context, decision, status, consequences), kept in the repository.
   *Evidence:* a `docs/adr/` (or similar) folder with numbered ADRs, each with a status. Major technology choices in the codebase have a matching ADR. *Sources:* NYGARD, SWEBOK. (level: judgement)
2. **MUST**: Superseded decisions are kept and marked as superseded, with a link to the replacement. They are never deleted.
   *Evidence:* ADRs with status "superseded by ADR-NNN". The history is visible in version control. *Sources:* NYGARD. (level: judgement)
3. **SHOULD**: Each ADR records the alternatives considered and why they were rejected, as well as the chosen option.
   *Evidence:* an "Options considered" section in the ADRs. *Sources:* SWEBOK.
4. **MUST**: The project has an up-to-date architecture description that includes at least a system context view. The view shows the system, its users, and every external system it depends on or serves.
   *Evidence:* a context diagram (for example C4 level 1) in the repository docs, matching the integrations actually in the code and config. *Sources:* C4, ISO42010. (level: judgement)
5. **SHOULD**: Architecture views follow a recognised structure, such as C4 (context, containers, components) or the ISO/IEC/IEEE 42010 concepts of viewpoints and views.
   *Evidence:* the diagrams and their notation key. *Sources:* C4, ISO42010.
6. **MUST**: Every external contract is documented in a machine-readable form and owned. This covers APIs exposed to other teams or clients, file imports and exports, and events.
   *Evidence:* an OpenAPI (or equivalent) document, generated or checked in CI, and a named owner for each interface. *Sources:* OPENAPI, AIP-180. (level: judgement)
7. **MUST**: Public APIs carry an explicit version, and breaking changes are released only as a new major version.
   *Evidence:* a version in the URI or package, a change policy, and the changelog. *Sources:* AIP-185, AIP-180, SEMVER. (level: judgement)
8. **SHOULD**: Released versions are immutable, and version numbers follow Semantic Versioning (MAJOR.MINOR.PATCH) for libraries and packages.
   *Evidence:* tags or releases that are never re-pointed. Version bumps match the kind of change. *Sources:* SEMVER.
9. **SHOULD**: HTTP APIs return errors in one consistent, machine-readable format, such as RFC 9457 Problem Details.
   *Evidence:* sampled error responses share a schema, and the schema is documented. *Sources:* RFC9457.
10. **SHOULD**: Contracts between services or teams are checked by automated contract tests (for example consumer-driven contracts).
    *Evidence:* contract tests running in CI for each provider/consumer pair. *Sources:* PRACTICAL-PYRAMID.
11. **SHOULD**: The data model (entities, relationships, ownership, and the meaning of each field that carries business rules) is documented and kept in step with schema migrations.
    *Evidence:* an ER diagram or schema doc, and migrations under version control. [judgement]
12. **SHOULD**: Domain boundaries are explicit. Where different parts of the system use different models of the same concept, the boundary (bounded context) and the translation between them are documented.
    *Evidence:* a context map, and mapping/translation code in one place. *Sources:* FOWLER-BC.
13. **MUST**: All dependencies are declared explicitly and completely in a manifest and lock file. Nothing relies on implicitly installed system packages.
    *Evidence:* manifest and lock files exist, and a clean-checkout build succeeds with only the documented prerequisites. *Sources:* 12F-DEPS. (level: judgement)
14. **SHOULD**: Build-vs-buy decisions and technology choices are documented, including total cost of ownership and how to avoid lock-in.
    *Evidence:* an ADR or decision note per major component or vendor. *Sources:* GDS-P11.
15. **MUST**: Vendored or copied third-party code is kept in a clearly marked location, with its licence, its origin and version, any local modifications, and a named owner. That owner monitors and patches vulnerabilities.
    *Evidence:* a `third_party/` (or similar) folder with licence and metadata files, and an owner entry. *Sources:* G-3P. (level: judgement)

### Failure modes

- **Undocumented decisions.** Newcomers either "Blindly accept the decision" or "Blindly change it" (NYGARD).
- **Rationale lost.** Rejected options are not recorded, so the team repeats "a poor decision — one rejected earlier for forgotten reasons" (SWEBOK).
- **Accidental contracts.** Interfaces are "sometimes accidentally grown" and never specified or tested, so changes break consumers silently (PRACTICAL-PYRAMID).
- **Unversioned breaking changes.** Old clients stop working, although "Existing client code must not be broken by a service updating to a new minor or patch release" (AIP-180).
- **Abandoned vendored code.** Copied in once and never upgraded. Google's policy warns: "Do not expect to check in open source code at Google and never have to touch it or maintain it" (G-3P).
- **Stale diagrams.** Architecture diagrams that no longer match the code. [judgement]

---

## Area 3: Code quality and conventions

### Candidate requirements

1. **MUST**: The project adopts a written coding standard for each language it uses. The standard may be an established external guide (for example PEP 8 or a Google style guide) plus local additions.
   *Evidence:* a CONTRIBUTING or style file that names the guide per language. *Sources:* SWEBOK, PEP8, GTR-STD. (level: judgement)
2. **MUST**: Formatting is done by an automatic formatter and checked in CI, so formatting is never a review topic.
   *Evidence:* formatter config in the repo, and a CI step that fails on unformatted code. *Sources:* SWE-STYLE. (level: judgement)
3. **MUST**: Rules that a tool can check are enforced by linters or static analysis in CI, not by reviewers' memory.
   *Evidence:* linter config, a CI job, and a zero-warning (or ratcheted) baseline. *Sources:* SWE-STYLE, SSDF. (level: judgement)
4. **SHOULD**: Static analysis checks are tuned to a low false-positive rate. Noisy checks are fixed or disabled, not ignored.
   *Evidence:* a documented suppression policy, with few blanket suppressions. *Sources:* SWE-STATIC.
5. **MUST**: Where the language supports static typing, the strictest practical type-checking mode is on and checked in CI. Exceptions are listed per module.
   *Evidence:* `tsc --noEmit` / mypy (or equivalent) with strict settings in CI, and a documented list of relaxations. *Sources:* TS-STRICT. (level: judgement)
6. **SHOULD**: Comments explain *why* (intent, constraints, decisions), not *what*. Public modules and functions document their purpose and usage.
   *Evidence:* review sample, and doc comments on public APIs. *Sources:* GTR-LOOK.
7. **SHOULD**: Function complexity is limited by a measured threshold (for example cyclomatic complexity 10, up to 15 with justification), and file and function size is monitored.
   *Evidence:* complexity checker config and its CI output. Exceptions are justified. *Sources:* NIST-500-235.
8. **SHOULD**: Dead code (unreachable code, unused exports, dependencies and feature flags) is detected by tooling and removed.
   *Evidence:* an unused-code or unused-dependency check in CI, or periodic reports. *Sources:* CWE-561, ISO5055.
9. **MUST**: Every change to the main branch is reviewed by at least one person other than its author before merge.
   *Evidence:* branch protection requiring an approval, and merged PRs that show a non-author approver. *Sources:* SWE-REVIEW, USDS, SSDF. (level: judgement)
10. **SHOULD**: The project publishes code review guidelines covering: what reviewers check (design, functionality, complexity, tests, naming, comments, style, docs), the approval standard, and the expected response time.
    *Evidence:* a review guide in the repo. PR timestamps show the response time. *Sources:* GTR-STD, GTR-LOOK, GTR-SPEED.
11. **SHOULD**: Changes are small and self-contained, with their tests in the same change. Refactors and reformatting are separated from functional changes.
    *Evidence:* PR size distribution (a median of a few hundred lines or less), and tests in the same PR. *Sources:* GTR-SMALL, GTR-LOOK.
12. **SHOULD**: Each change has a description that states what changed and why.
    *Evidence:* PR template, and a sample of PR descriptions. *Sources:* GTR-DESC.
13. **MUST**: The team has a written Definition of Done that every change must meet before it counts as complete or releasable. At minimum: reviewed, tests pass, docs updated, and acceptance criteria met.
    *Evidence:* a DoD document, linked from the PR template or checklist. *Sources:* SCRUM. (level: judgement)
14. **SHOULD**: Changes that alter how users build, test or release the code also update the related documentation in the same change.
    *Evidence:* PRs that change build or test scripts also touch the README or docs. *Sources:* GTR-LOOK.

### Failure modes

- **Style debates in review.** Without a formatter and a style authority, review time goes on nits. Google: "the style guide is the absolute authority" (GTR-STD). Automating formatting eliminates "the review cycles that are otherwise spent finding, flagging, and fixing minor style nits" (SWE-STYLE).
- **Rules enforced by memory.** These are "dropped or forgotten as time passes or as an organization scales up" (SWE-STYLE).
- **Noisy analysers ignored.** Low false-positive rates "are often critical for developers to actually want to use a tool" (SWE-STATIC).
- **Huge PRs rubber-stamped.** "1000 lines is usually too large" (GTR-SMALL).
- **Gradual decay.** "codebases degrade through small decreases in code health over time" (GTR-STD).
- **"Done" means "merged".** Untested or undocumented work counts as complete because no shared Definition of Done exists (SCRUM).

---

## Area 4: Testing and quality assurance

### Candidate requirements

1. **MUST**: The project has a written test strategy: which test levels exist (unit, integration/service, end-to-end, manual), what each covers, where each runs, and the target balance (a test pyramid, not an ice-cream cone).
   *Evidence:* a TESTING doc, and test folders that match it. Test counts per level are roughly pyramid-shaped. *Sources:* PYRAMID, SWE-TEST, ISO29119. (level: judgement)
2. **MUST**: The automated test suite runs on every change in CI, and a change cannot merge while tests fail.
   *Evidence:* a required CI status check on the default branch. *Sources:* FOWLER-CI, USDS, DORA-TA. (level: judgement)
3. **MUST**: The main branch is kept green. A broken build is fixed or reverted immediately, as the top-priority task.
   *Evidence:* CI history on main. The time-to-fix for red builds is short, and reverts are used. *Sources:* FOWLER-CI. (level: judgement)
4. **SHOULD**: The commit-stage test suite gives feedback in under about ten minutes.
   *Evidence:* CI job durations. *Sources:* DORA-TA, FOWLER-CI.
5. **MUST**: Critical business rules (for example permissions, calculations and state transitions) have automated tests. Coverage reports are used to find untested critical code, not as a numeric target alone.
   *Evidence:* a list of critical rules mapped to tests, and the coverage report with critical modules reviewed. *Sources:* FOWLER-COV, SWE-TEST. (level: judgement)
6. **MUST**: Every fixed defect gets a regression test that fails before the fix and passes after it, at the lowest practical level.
   *Evidence:* sampled bug-fix PRs contain a new test. *Sources:* PYRAMID, SSDF, SWEBOK. (level: judgement)
7. **MUST**: Flaky (non-deterministic) tests are tracked and fixed or quarantined promptly. They are not tolerated by blind reruns.
   *Evidence:* a flaky-test list or label, a quarantine mechanism, and the flake rate. *Sources:* FOWLER-NONDET, SWE-TEST. (level: judgement)
8. **SHOULD**: Tests are hermetic. Each sets up and tears down its own data and does not depend on test order or a shared mutable database.
   *Evidence:* review of test fixtures. Tests pass in random order. *Sources:* SWE-TEST, DORA-TDM.
9. **MUST**: Test data is synthetic or anonymised. Production personal data is not copied into test environments or fixtures without an approved, documented basis.
   *Evidence:* fixtures and seed scripts, and a scan of the test data for real personal data. *Sources:* DORA-TDM. (level: judgement)
10. **SHOULD**: Test data needed by the automated suites is available on demand and does not limit which tests can run.
    *Evidence:* seed/factory scripts, and the suite runs from a clean environment. *Sources:* DORA-TDM.
11. **SHOULD**: Performance and load tests run against stated NFR thresholds before launch and at regular intervals after it.
    *Evidence:* load-test scripts, dated results compared with the NFR targets. *Sources:* USDS, ISO25010.
12. **MAY**: Resilience is tested with controlled fault-injection experiments, defining steady state first and limiting the blast radius. This applies especially to distributed systems.
    *Evidence:* experiment records (hypothesis, scope, result). *Sources:* CHAOS.
13. **MUST**: Security testing is part of the test plan: functional tests of security controls (for example authorisation rules), automated static and dynamic checks, and tests for previously reported vulnerabilities. Findings are triaged in the issue tracker.
    *Evidence:* security test cases, SAST/DAST jobs in CI, triaged findings, and the verification level chosen (for example OWASP ASVS). *Sources:* SSDF, OWASP-ASVS, OWASP-WSTG. (level: judgement)
14. **MUST** (for user-facing web UIs): Accessibility is tested against WCAG 2.2 Level AA, using automated tools plus manual checks, because tools alone cannot determine conformance.
    *Evidence:* automated a11y checks in CI, and a manual audit report against the WCAG 2.2 AA criteria. *Sources:* WCAG22, WAI-TOOLS. (level: judgement)
15. **SHOULD**: Exploratory, usability and acceptance testing happen throughout delivery, not only at the end. UAT results feed back into the backlog.
    *Evidence:* exploratory session notes, UAT records, and defects linked to backlog items. *Sources:* DORA-TA, SWEBOK.

### Failure modes

- **Ice-cream cone.** Many end-to-end tests and few unit tests make suites "slow, unreliable, and difficult to work with" (SWE-TEST, PYRAMID).
- **Coverage as a target.** "high coverage numbers are too easy to reach with low quality testing" (FOWLER-COV).
- **Flaky tests tolerated.** These erode trust: "as you approach 1% flakiness, the tests begin to lose value" (SWE-TEST). Non-deterministic tests are "a virulent infection that can completely ruin your entire test suite" (FOWLER-NONDET).
- **Red main left red.** CI "can only work if the mainline is kept in a healthy state" (FOWLER-CI).
- **Production data in tests.** "Copying production data introduces risk because it might contain sensitive information" (DORA-TDM).
- **Accessibility "passed" by a tool.** "Web accessibility evaluation tools can not determine accessibility, they can only assist in doing so" (WAI-TOOLS).

---

## Sources

All sources accessed 2026-10-31.

**ISO29148**: ISO/IEC/IEEE 29148:2018 *Systems and software engineering — Life cycle processes — Requirements engineering*. ISO/IEC/IEEE. Catalogue page: https://www.iso.org/standard/72089.html (fetched via the mirror https://committee.iso.org/standard/72089.html). **Paywalled; only the public abstract is quoted.** The catalogue lists its stage as "International Standard to be revised [90.92]".
> "specifies the required processes implemented in the engineering activities that result in requirements for systems and software products (including services) throughout the life cycle"
> "specifies the required contents of the required information items"

**ISO25010**: ISO/IEC 25010:2023 *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. ISO/IEC. https://www.iso.org/standard/78176.html (mirror: committee.iso.org). **Paywalled; abstract only.**
> "The product quality model is composed of nine characteristics (which are further subdivided into subcharacteristics) that relate to quality properties of the products."
> "identifying acceptance criteria for a product and/or an information system"

**ISO42010**: ISO/IEC/IEEE 42010:2022 *Software, systems and enterprise — Architecture description*. ISO/IEC/IEEE. https://www.iso.org/standard/74393.html (mirror: committee.iso.org). **Paywalled; abstract only.**
> "This document specifies requirements for the structure and expression of an architecture description (AD) for various entities, including software, systems, enterprises"
> "This document does not specify the processes, architecting methods, models, notations, techniques or tools by which an AD is created, utilized or managed."

**ISO12207**: ISO/IEC/IEEE 12207:2026 *Systems and software engineering — Software life cycle processes* (published 2026-04; replaces the 2017 edition, now withdrawn). https://www.iso.org/standard/90219.html (mirror: committee.iso.org). **Paywalled; abstract only.** It is a framing reference for the whole standard rather than support for one requirement.
> "This document establishes a common framework for software life cycle processes."
> "It is applicable for agile approaches and methods"

**ISO29119**: ISO/IEC/IEEE 29119-1:2022 *Software and systems engineering — Software testing — Part 1: General concepts*. https://www.iso.org/standard/81291.html (mirror: committee.iso.org). **Paywalled; abstract only.**
> "This document specifies general concepts in software testing and presents key concepts for the ISO/IEC/IEEE 29119 series."

**ISO5055**: ISO/IEC 5055:2021 *Information technology — Software measurement — Software quality measurement — Automated source code quality measures*. https://www.iso.org/standard/80623.html (mirror: committee.iso.org). **Paywalled; abstract only.**
> "The measures in this standard were calculated from detecting and counting violations of good architectural and coding practices in the source code that could result in unacceptable operational risks or excessive costs."

**SWEBOK**: *Guide to the Software Engineering Body of Knowledge (SWEBOK Guide) v4.0a*, H. Washizaki (ed.), IEEE Computer Society. The PDF title page reads "Released August 2026". Landing page: https://www.computer.org/education/bodies-of-knowledge/software-engineering ; PDF: https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf
> "be testable (quantified), meaning that compliance or noncompliance can be clearly demonstrated" (Software Requirements KA, 3.1)
> "Natural languages are inherently ambiguous, but test case language is not." (Software Requirements KA, 4.3)
> "Software requirements can be traced back to source documentation such as system requirements, standards documents and other relevant specifications." (Software Requirements KA)
> "Acceptance testing targets the deployment of a SUT. Its main goal is to verify that the SUT satisfies the requirements and the end-users’ expectations." (Software Testing KA, 2.1.4)
> "Design rationale captures why a design decision was made. This includes prior assumptions made, alternatives considered, and trade-offs and criteria analyzed to select one approach and reject others." (Software Design KA, 4.6)
> "Recording rejected decisions and the reasons for their rejection can also be useful." (Software Architecture KA)
> "regression testing is the “selective retesting of a SUT to verify that modifications have not caused unintended effects and that the SUT still complies with its specified requirements.”" (Software Testing KA, 2.2.5)
> "Defining and adopting apt coding standard for the project, and ensuring every team member implements the same in spirit is key for developing clean code" (Computing Foundations KA)

**GDS-DISC**: "How the discovery phase works", *Service Manual*, UK Government Digital Service (GOV.UK). https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works
> "Before you commit to building a service, you need to understand the problem that needs to be solved."
> "Reframing the problem also includes agreeing what is not part of the problem."
> "During discovery, that means understanding how much the problem is currently costing."
> "If there’s a hard constraint which means you are not able to improve on the solution that’s currently available, it might be worth stopping at the end of discovery."

**GDS-P1**: "Service Standard, 1. Understand users and their needs", GOV.UK. https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs
> "The real problem might not be the one you originally thought needed solving. Testing your assumptions early and often reduces the risk of building the wrong thing."

**GDS-P10**: "Service Standard, 10. Define what success looks like and publish performance data", GOV.UK. https://www.gov.uk/service-manual/service-standard/point-10-define-success-publish-performance-data
> "Defining what good looks like and identifying appropriate metrics means that you’ll know whether the service is solving the problem it’s meant to solve."
> "identify metrics which will indicate how well the service is solving the problem it’s meant to solve, and track performance against them"

**GDS-P11**: "Service Standard, 11. Choose the right tools and technology", GOV.UK. https://www.gov.uk/service-manual/service-standard/point-11-choose-the-right-tools-and-technology
> "be able to show that they’ve made good decisions about what technology to build and what to buy, including use of common platforms where appropriate"
> "understand total cost of ownership of the technology and preserve the ability to make different choices in future"

**USDS**: *Digital Services Playbook*, U.S. Digital Service. https://playbook.usds.gov/
> "Document the findings about user goals, needs, behaviors, and preferences" (Play 1)
> "Create a prioritized list of features and bugs, also known as the “feature backlog” and “bug backlog”" (Play 4)
> "Use code reviews to ensure quality" (Play 4)
> "Run tests automatically as part of the build process" (Play 10)
> "Conduct load and performance tests at regular intervals, including before public launch" (Play 10)

**INVEST**: Bill Wake, "INVEST in Good Stories, and SMART Tasks", XP123, 17 August 2003. https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
> "A good story is testable . Writing a story card carries an implicit promise: “I understand what I want well enough that I could write a test for it.”" (the space before the period is the page's own)
> "Good stories tend to be small . Stories typically represent at most a few person-weeks worth of work." (likewise)

**FOWLER-GWT**: Martin Fowler, "GivenWhenThen", martinfowler.com, 21 August 2013. https://martinfowler.com/bliki/GivenWhenThen.html
> "Given-When-Then is a style of representing tests - or as its advocates would say - specifying a system's behavior using SpecificationByExample ."

**FOWLER-UBIQ**: Martin Fowler, "UbiquitousLanguage", martinfowler.com, 31 October 2006. https://martinfowler.com/bliki/UbiquitousLanguage.html
> "the practice of building up a common, rigorous language between developers and users. This language should be based on the Domain Model used in the software"

**FOWLER-BC**: Martin Fowler, "BoundedContext", martinfowler.com, 15 January 2014. https://martinfowler.com/bliki/BoundedContext.html
> "DDD deals with large models by dividing them into different Bounded Contexts and being explicit about their interrelationships."

**NYGARD**: Michael Nygard, "Documenting Architecture Decisions", Cognitect blog, 15 November 2011. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
> "One of the hardest things to track during the life of a project is the motivation behind certain decisions."
> "We will keep ADRs in the project repository under doc/arch/adr-NNN.md"
> "If a decision is reversed, we will keep the old one around, but mark it as superseded."

**C4**: Simon Brown, "The C4 model for visualising software architecture" and "System context diagram", c4model.com. https://c4model.com/ ; https://c4model.com/diagrams/system-context
> "Draw a diagram showing your system as a box in the centre, surrounded by its users and the other systems that it interacts with."
> "Yes, a system context diagram is recommended for all software development teams."

**OPENAPI**: *OpenAPI Specification v3.1.1*, OpenAPI Initiative, 24 October 2024. https://spec.openapis.org/oas/v3.1.1.html
> "The OpenAPI Specification (OAS) defines a standard, programming language-agnostic interface description for HTTP APIs"

**AIP-180**: "AIP-180: Backwards compatibility", Google API Improvement Proposals. https://google.aip.dev/180 (cloud.google.com/apis/design/compatibility redirects here)
> "APIs are fundamentally contracts with users"
> "Existing client code must not be broken by a service updating to a new minor or patch release."

**AIP-185**: "AIP-185: API Versioning", Google API Improvement Proposals. https://google.aip.dev/185 (cloud.google.com/apis/design/versioning redirects here)
> "All Google API interfaces must provide a major version number , which is encoded at the end of the protobuf package, and included as the first part of the URI path for REST APIs." (the space before the comma is the page's own)

**SEMVER**: Tom Preston-Werner, *Semantic Versioning 2.0.0*. https://semver.org/
> "Software using Semantic Versioning MUST declare a public API."
> "Once a versioned package has been released, the contents of that version MUST NOT be modified. Any modifications MUST be released as a new version."

**RFC9457**: M. Nottingham, E. Wilde, S. Dalal, RFC 9457 *Problem Details for HTTP APIs*, IETF, July 2023 (obsoletes RFC 7807). https://www.rfc-editor.org/rfc/rfc9457.html
> "This document defines a "problem detail" to carry machine-readable details of errors in HTTP response content to avoid the need to define new error response formats for HTTP APIs."

**12F-DEPS**: Adam Wiggins, "The Twelve-Factor App: II. Dependencies". https://12factor.net/dependencies
> "A twelve-factor app never relies on implicit existence of system-wide packages. It declares all dependencies, completely and exactly, via a dependency declaration manifest."

**G-3P**: Google Open Source, "Third-Party" and "//third_party Owners' and Users' Responsibilities". https://opensource.google/documentation/reference/thirdparty ; https://opensource.google/documentation/reference/thirdparty/responsibilities
> "Important: All third party code must have a license ."
> "Monitor Vulnerabilities: You need to monitor upstream source code for security vulnerabilities."
> "Do not expect to check in open source code at Google and never have to touch it or maintain it."

**PRACTICAL-PYRAMID**: Ham Vocke, "The Practical Test Pyramid", martinfowler.com, 26 February 2018. https://martinfowler.com/articles/practical-test-pyramid.html
> "Automated contract tests make sure that the implementations on the consumer and provider side still stick to the defined contract."
> "services need to communicate with each other via certain (hopefully well-defined, sometimes accidentally grown) interfaces."

**GTR-STD**: Google, "The Standard of Code Review", *Google Engineering Practices*. https://google.github.io/eng-practices/review/reviewer/standard.html
> "reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn’t perfect."
> "On matters of style, the style guide is the absolute authority."

**GTR-LOOK**: Google, "What to look for in a code review". https://google.github.io/eng-practices/review/reviewer/looking-for.html
> "In general, tests should be added in the same CL as the production code unless the CL is handling an emergency ."
> "Usually comments are useful when they explain why some code exists, and should not be explaining what some code is doing."
> "If a CL changes how users build, test, interact with, or release code, check to see that it also updates associated documentation"

**GTR-SMALL**: Google, "Small CLs". https://google.github.io/eng-practices/review/developer/small-cls.html
> "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large, but it’s up to the judgment of your reviewer."

**GTR-SPEED**: Google, "Speed of Code Reviews". https://google.github.io/eng-practices/review/reviewer/speed.html
> "One business day is the maximum time it should take to respond to a code review request"

**GTR-DESC**: Google, "Writing good CL descriptions". https://google.github.io/eng-practices/review/developer/cl-descriptions.html
> "A CL description is a public record of change"
> "Why are these changes being made?"

**SWE-STYLE**: T. Winters, T. Manshreck, H. Wright (eds.), *Software Engineering at Google*, Ch. 8 "Style Guides and Rules", O'Reilly 2020, free online edition. https://abseil.io/resources/swe-book/html/ch08.html
> "when it comes to checking for compliance, rather than exclusively depending on engineer-based verification, we strongly prefer to automate enforcement with tooling."
> "Automated rule enforcement ensures that rules are not dropped or forgotten as time passes or as an organization scales up."

**SWE-STATIC**: *Software Engineering at Google*, Ch. 20 "Static Analysis". https://abseil.io/resources/swe-book/html/ch20.html
> "We only deploy analysis tools with low false-positive rates"
> "low false-positive rates are often critical for developers to actually want to use a tool"

**SWE-REVIEW**: *Software Engineering at Google*, Ch. 9 "Code Review". https://abseil.io/resources/swe-book/html/ch09.html
> "Code review is a process in which code is reviewed by someone other than the author, often before the introduction of that code into a codebase."
> "At Google, essentially every change is reviewed before being committed"

**SWE-TEST**: *Software Engineering at Google*, Ch. 11 "Testing Overview". https://abseil.io/resources/swe-book/html/ch11.html
> "we tend to aim to have a mix of around 80% of our tests being narrow-scoped unit tests that validate the majority of our business logic; 15% medium-scoped integration tests"
> "All tests should strive to be hermetic: a test should contain all of the information necessary to set up, execute, and tear down its environment."
> "Our experience suggests that as you approach 1% flakiness, the tests begin to lose value."
> "“If you liked it, then you shoulda put a test on it.”"

**SCRUM**: Ken Schwaber and Jeff Sutherland, *The Scrum Guide* (2020). https://scrumguides.org/scrum-guide.html
> "The Definition of Done is a formal description of the state of the Increment when it meets the quality measures required for the product."
> "If a Product Backlog item does not meet the Definition of Done, it cannot be released or even presented at the Sprint Review."

**PEP8**: G. van Rossum, B. Warsaw, A. Coghlan, *PEP 8 – Style Guide for Python Code*, Python Software Foundation. https://peps.python.org/pep-0008/
> "code is read much more often than it is written."
> "A style guide is about consistency. Consistency with this style guide is important. Consistency within a project is more important."

**TS-STRICT**: Microsoft, "TSConfig Option: strict", TypeScript documentation. https://www.typescriptlang.org/tsconfig/strict.html
> "The strict flag enables a wide range of type checking behavior that results in stronger guarantees of program correctness."

**NIST-500-235**: A. H. Watson, T. J. McCabe, *Structured Testing: A Testing Methodology Using the Cyclomatic Complexity Metric*, NIST Special Publication 500-235, August 1996. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf
> "Overly complex modules are more prone to error, are harder to understand, are harder to test, and are harder to modify."
> "The original limit of 10 as proposed by McCabe has significant supporting evidence, but limits as high as 15 have been used successfully as well."

**CWE-561**: MITRE, "CWE-561: Dead Code" (CWE 5.0). https://cwe.mitre.org/data/definitions/561.html
> "The product contains dead code, which can never be executed."
> "Remove dead code before deploying the application."

**SSDF**: M. Souppaya, K. Scarfone, D. Dodson, NIST SP 800-218 *Secure Software Development Framework (SSDF) Version 1.1*, February 2022. https://csrc.nist.gov/pubs/sp/800/218/final ; PDF https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf
> "Use a static analysis tool to automatically check code for vulnerabilities and compliance with the organization’s secure coding standards with a human reviewing the issues reported by the tool" (PW.7.2, Example 4)
> "Scope the testing, design the tests, perform the testing, and document the results, including recording and triaging all discovered issues and recommended remediations" (PW.8.2)
> "Incorporate tests for previously reported vulnerabilities into the project’s test suite to ensure that errors are not reintroduced." (PW.8.2, Example 3)

**PYRAMID**: Martin Fowler, "TestPyramid", martinfowler.com, 1 May 2012. https://martinfowler.com/bliki/TestPyramid.html
> "Its essential point is that you should have many more low-level UnitTests than high level BroadStackTests running through a GUI."
> "before fixing a bug exposed by a high level test, you should replicate the bug with a unit test. Then the unit test ensures the bug stays dead."

**FOWLER-CI**: Martin Fowler, "Continuous Integration", martinfowler.com, revised 18 January 2024. https://martinfowler.com/articles/continuousIntegration.html
> "Continuous Integration can only work if the mainline is kept in a healthy state. Should the integration build fail, then it needs to be fixed right away."
> "For most projects, however, the XP guideline of a ten minute build is perfectly within reason."

**FOWLER-COV**: Martin Fowler, "TestCoverage", martinfowler.com, 17 April 2012. https://martinfowler.com/bliki/TestCoverage.html
> "Test coverage is a useful tool for finding untested parts of a codebase. Test coverage is of little use as a numeric statement of how good your tests are."
> "high coverage numbers are too easy to reach with low quality testing."

**FOWLER-NONDET**: Martin Fowler, "Eradicating Non-Determinism in Tests", martinfowler.com, 14 April 2011. https://martinfowler.com/articles/nonDeterminism.html
> "Non-deterministic tests have two problems, firstly they are useless, secondly they are a virulent infection that can completely ruin your entire test suite."

**DORA-TA**: DORA, "Capabilities: Test automation". https://dora.dev/capabilities/test-automation/
> "Keep the test suite fast. Developers should be able to get feedback from automated tests in less than ten minutes both on local workstations and from the continuous integration system."
> "Perform manual test activities such as exploratory testing, usability testing, and acceptance testing throughout the delivery process."

**DORA-TDM**: DORA, "Capabilities: Test data management". https://dora.dev/capabilities/test-data-management/
> "Copying production data introduces risk because it might contain sensitive information."
> "Test data for automated test suites can be acquired on demand."

**CHAOS**: "Principles of Chaos Engineering". https://principlesofchaos.org/
> "Chaos Engineering is the discipline of experimenting on a system in order to build confidence in the system’s capability to withstand turbulent conditions in production."
> "Start by defining ‘steady state’ as some measurable output of a system that indicates normal behavior."

**OWASP-ASVS**: OWASP, "Application Security Verification Standard" project page. https://owasp.org/www-project-application-security-verification-standard/
> "The OWASP Application Security Verification Standard (ASVS) Project provides a basis for testing web application technical security controls and also provides developers with a list of requirements for secure development."

**OWASP-WSTG**: OWASP, "Web Security Testing Guide" project page. https://owasp.org/www-project-web-security-testing-guide/
> "The Web Security Testing Guide (WSTG) Project produces the premier cybersecurity testing resource for web application developers and security professionals."

**WCAG22**: W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation 12 December 2024. https://www.w3.org/TR/WCAG22/
> "For Level AA conformance, the web page satisfies all the Level A and Level AA success criteria, or a Level AA conforming alternate version is provided."

**WAI-TOOLS**: W3C WAI, "Selecting Web Accessibility Evaluation Tools". https://www.w3.org/WAI/test-evaluate/tools/selecting/
> "Tools cannot check all accessibility aspects automatically. Human judgement is required."
> "Web accessibility evaluation tools can not determine accessibility, they can only assist in doing so."

---

## Gaps (could not source)

- **ISO standards' normative text** (29148, 25010, 42010, 29119, 12207, 5055). Only the public abstracts are verified. The specific clauses (for example 29148's requirement characteristics, 25010's list of nine characteristics, 29119-3 test documentation) need a purchased copy before they are quoted.
- **Data model documentation.** No primary source fetched. SWEBOK mentions data models, but nothing was quoted for this requirement. Marked [judgement].
- **Type-safety strictness as a MUST.** The TypeScript docs describe the `strict` flag but do not prescribe its use. No standard mandates strict typing.
- **Explicit non-goals and scope documents.** Supported only indirectly (GOV.UK "what is not part of the problem"). There is no standard template source.
- **UAT sign-off and recorded acceptance decision.** SWEBOK and DORA describe acceptance testing, but no fetched source requires formal sign-off. That could come from ISO 29119-3 or 12207 (paywalled).
- **ISTQB glossary definitions** (UAT, regression). The glossary site is JavaScript-rendered and was not fetched.
- **Microsoft Azure REST API Guidelines.** Fetched but not used: AIP-180 and AIP-185 cover the same point.
- **Numeric thresholds.** Thresholds for PR size, complexity, flake rate, build time and coverage come only from originator guidance (Google, NIST 1996, Fowler, DORA), not from standards. They should be presented as SHOULD-level defaults.
