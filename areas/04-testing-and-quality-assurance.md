# 4. Testing and quality assurance

- **ID prefix:** TST
- **Status:** draft, 2026-10-31

## Purpose

This area protects against changes that silently break what already worked, and against defects, slowness, security holes
and accessibility barriers that only users find. It covers the test strategy, the shape of the automated suite (running it as a gate on every change
and keeping the main branch green: see Area 8), and targeted tests for critical rules, fixed defects, performance, security
and accessibility.

## Scope

Covers: the test strategy and test pyramid, coverage of critical rules, regression tests, flaky tests, hermetic tests and test data, contract tests, performance and load testing,
resilience testing, security testing, accessibility testing, and exploratory and usability testing during delivery.

Leaves to other areas:
- Acceptance criteria and UAT sign-off: see Area 1 (PRD-9, PRD-15).
- Non-functional thresholds that performance tests check against: see Area 1 (PRD-11).
- The CI pipeline and its blocking gates, including running the tests on every change and keeping the main branch green: see
  Area 8 (CI-2, CI-4, CI-6).
- Test feedback time (about ten minutes for the checks that gate a change): see Area 8 (CI-7).
- Vulnerability, dependency and secret scanning (what and why): see Area 5.
- Personal data in test data and fixtures: see Area 6.
- Accessibility conformance targets: see Area 15.

## Requirements

### TST-1 · MUST · Written test strategy
The project MUST keep a written test strategy stating which test levels exist (for example unit, integration, end-to-end,
manual), what each covers, and where each runs.
- **Gate:** G1
- **Evidence:** a TESTING document, and test folders and pipeline jobs that match it.
- **Basis:** [PYRAMID], [SWE-TEST]. Level: author's judgement (sources support
  SHOULD).

### TST-2 · SHOULD · Pyramid-shaped suite
Most automated tests SHOULD be fast, narrow unit tests, with fewer integration tests and fewest end-to-end tests.
- **Gate:** G2
- **Evidence:** test counts per level are roughly pyramid-shaped (for example around 80% unit tests).
- **Basis:** [PYRAMID], [SWE-TEST].

### TST-3 · MUST · Critical rules tested
Critical business rules (for example permissions, calculations and state transitions) MUST have automated tests, with coverage
reports used to find untested critical code rather than as a numeric target alone.
- **Gate:** G2
- **Evidence:** a list of critical rules mapped to tests, and a coverage report with the critical modules reviewed.
- **Basis:** [FOWLER-COV], [SWE-TEST]. Level: author's judgement (sources support SHOULD).

### TST-4 · MUST · Regression test per fixed defect
Every fixed defect MUST get a test, at the lowest practical level, that fails before the fix and passes after it.
- **Gate:** G1
- **Evidence:** sampled bug-fix PRs each contain a new or changed test.
- **Basis:** [PYRAMID], [SWEBOK], [SWE-TEST]. Level: author's judgement (sources support SHOULD).

### TST-5 · MUST · Flaky tests handled
Non-deterministic (flaky) tests MUST be tracked and fixed or quarantined within a project-set limit in working days, not
tolerated by blind reruns.
- **Gate:** G1
- **Evidence:** the limit recorded in the test strategy (TST-1); a flaky-test list or label with the date each was found and
  fixed or quarantined, all within the limit; a quarantine mechanism; the measured flake rate.
- **Basis:** [FOWLER-NONDET], [SWE-TEST]. Level: author's judgement (sources support SHOULD).

### TST-6 · SHOULD · Hermetic tests
Each test SHOULD set up and tear down its own data and not depend on test order or a shared mutable database.
- **Gate:** G2
- **Evidence:** a review of test fixtures; the suite passes when run in random order.
- **Basis:** [SWE-TEST].

### TST-7 · SHOULD · Test data on demand
Test data needed by the automated suites SHOULD be created on demand by seed or factory scripts, so the suite runs from a clean
environment (rules on personal data in test data: Area 6).
- **Gate:** G2
- **Evidence:** seed or factory scripts, and a suite run from an empty environment.
- **Basis:** [DORA-TDM].

### TST-8 · SHOULD · Contract tests
Where services or teams exchange data through an interface, both sides SHOULD be checked against the documented contract
(APIs and events: ARC-6; file imports and exports: DAT-2) by automated contract tests.
- **Gate:** G2
- **Evidence:** contract tests running in the pipeline for each provider/consumer pair.
- **Basis:** [PRACTICAL-PYRAMID].

### TST-9 · SHOULD · Performance and load tests
Performance and load tests SHOULD run against the stated NFR thresholds before launch and at regular intervals after it.
- **Gate:** G3
- **Evidence:** load-test scripts and dated results compared with the NFR targets.
- **Basis:** [USDS].

### TST-10 · MAY · Resilience experiments
Resilience MAY be tested with controlled fault-injection experiments that define steady state first and limit the blast
radius; this is most useful for distributed systems.
- **Gate:** G3
- **Evidence:** experiment records (hypothesis, scope, result).
- **Basis:** [CHAOS].

### TST-11 · MUST · Security testing
The test plan MUST include security testing: functional tests of security controls (for example authorisation rules) and
tests for previously reported vulnerabilities, with findings recorded and triaged.
- **Gate:** G2
- **Evidence:** security test cases in the suite, regression tests for past vulnerabilities, and triaged findings in the issue
  tracker.
- **Basis:** [SSDF], [OWASP-ASVS], [OWASP-WSTG]. Level: author's judgement (sources support SHOULD).

### TST-12 · MUST · Accessibility testing for user interfaces
User-facing interfaces MUST be tested against the accessibility target set under Area 15 (for example WCAG 2.2 Level AA) with
both automated tools and manual checks.
- **Gate:** G3
- **Evidence:** automated accessibility checks in the pipeline, and a dated manual audit against the target criteria.
- **Basis:** [WCAG22], [WAI-TOOLS]. Level: author's judgement (sources support SHOULD).

### TST-13 · SHOULD · Manual testing throughout delivery
Exploratory, usability and acceptance testing SHOULD happen throughout delivery, not only at the end, with findings fed back
into the backlog.
- **Gate:** G2
- **Evidence:** exploratory session notes, usability and UAT records, and defects linked to backlog items.
- **Basis:** [DORA-TA]. Findings fed back into the backlog: author's judgement.

## Failure modes

- **Ice-cream cone.** Many end-to-end tests and few unit tests make the suite slow and unreliable [SWE-TEST], [PYRAMID].
- **Coverage as a target.** "high coverage numbers are too easy to reach with low quality testing." [FOWLER-COV]
- **Flaky tests tolerated.** "as you approach 1% flakiness, the tests begin to lose value" [SWE-TEST]; non-deterministic tests
  are "a virulent infection that can completely ruin your entire test suite" [FOWLER-NONDET].
- **Red main left red.** CI "can only work if the mainline is kept in a healthy state" [FOWLER-CI].
- **Production data in tests.** "Copying production data introduces risk because it might contain sensitive information."
  [DORA-TDM]
- **Accessibility "passed" by a tool.** "Web accessibility evaluation tools can not determine accessibility, they can only
  assist in doing so." [WAI-TOOLS]

## References

- **[CHAOS]** Principles of Chaos Engineering. https://principlesofchaos.org/. Accessed 2026-10-31.
  > "Chaos Engineering is the discipline of experimenting on a system in order to build confidence in the system’s capability to withstand turbulent conditions in production." (introduction)
  > "Start by defining ‘steady state’ as some measurable output of a system that indicates normal behavior." (CHAOS IN PRACTICE)
- **[DORA-TA]** Capabilities: Test automation. DORA. https://dora.dev/capabilities/test-automation/. Accessed 2026-10-31.
  > "Perform manual test activities such as exploratory testing, usability testing, and acceptance testing throughout the delivery process."
- **[DORA-TDM]** Capabilities: Test data management. DORA. https://dora.dev/capabilities/test-data-management/. Accessed 2026-10-31.
  > "Copying production data introduces risk because it might contain sensitive information." (introduction)
  > "Test data for automated test suites can be acquired on demand." (How to implement test data management)
- **[FOWLER-CI]** Continuous Integration. Martin Fowler, martinfowler.com, revised 18 January 2024. https://martinfowler.com/articles/continuousIntegration.html. Accessed 2026-10-31.
  > "Continuous Integration can only work if the mainline is kept in a healthy state. Should the integration build fail, then it needs to be fixed right away."
- **[FOWLER-COV]** TestCoverage. Martin Fowler, martinfowler.com, 17 April 2012. https://martinfowler.com/bliki/TestCoverage.html. Accessed 2026-10-31.
  > "Test coverage is a useful tool for finding untested parts of a codebase. Test coverage is of little use as a numeric statement of how good your tests are." (Test Coverage)
  > "high coverage numbers are too easy to reach with low quality testing." (Test Coverage)
- **[FOWLER-NONDET]** Eradicating Non-Determinism in Tests. Martin Fowler, martinfowler.com, 14 April 2011. https://martinfowler.com/articles/nonDeterminism.html. Accessed 2026-10-31.
  > "Non-deterministic tests have two problems, firstly they are useless, secondly they are a virulent infection that can completely ruin your entire test suite."
- **[OWASP-ASVS]** Application Security Verification Standard (project page). OWASP. https://owasp.org/www-project-application-security-verification-standard/. Accessed 2026-10-31.
  > "The OWASP Application Security Verification Standard (ASVS) Project provides a basis for testing web application technical security controls and also provides developers with a list of requirements for secure development."
- **[OWASP-WSTG]** Web Security Testing Guide (project page). OWASP. https://owasp.org/www-project-web-security-testing-guide/. Accessed 2026-10-31.
  > "The Web Security Testing Guide (WSTG) Project produces the premier cybersecurity testing resource for web application developers and security professionals."
- **[PRACTICAL-PYRAMID]** The Practical Test Pyramid. Ham Vocke, martinfowler.com, 26 February 2018. https://martinfowler.com/articles/practical-test-pyramid.html. Accessed 2026-10-31.
  > "Automated contract tests make sure that the implementations on the consumer and provider side still stick to the defined contract."
- **[PYRAMID]** TestPyramid. Martin Fowler, martinfowler.com, 1 May 2012. https://martinfowler.com/bliki/TestPyramid.html. Accessed 2026-10-31.
  > "Its essential point is that you should have many more low-level UnitTests than high level BroadStackTests running through a GUI." (Test Pyramid)
  > "before fixing a bug exposed by a high level test, you should replicate the bug with a unit test. Then the unit test ensures the bug stays dead." (Test Pyramid)
- **[SSDF]** NIST SP 800-218 Secure Software Development Framework (SSDF) Version 1.1. M. Souppaya, K. Scarfone, D. Dodson, NIST, February 2022. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf (landing page: https://csrc.nist.gov/pubs/sp/800/218/final). Accessed 2026-10-31.
  > "Scope the testing, design the tests, perform the testing, and document the results, including recording and triaging all discovered issues and recommended remediations" (PW.8.2)
  > "Incorporate tests for previously reported vulnerabilities into the project’s test suite to ensure that errors are not reintroduced." (PW.8.2, Example 3)
- **[SWE-TEST]** Software Engineering at Google, Ch. 11 "Testing Overview". T. Winters, T. Manshreck, H. Wright (eds.), O'Reilly 2020, free online edition. https://abseil.io/resources/swe-book/html/ch11.html. Accessed 2026-10-31.
  > "we tend to aim to have a mix of around 80% of our tests being narrow-scoped unit tests that validate the majority of our business logic; 15% medium-scoped integration tests" (Test Scope)
  > "All tests should strive to be hermetic: a test should contain all of the information necessary to set up, execute, and tear down its environment." (Properties common to all test sizes)
  > "Our experience suggests that as you approach 1% flakiness, the tests begin to lose value." (Case Study: Flaky Tests Are Expensive)
  > "“If you liked it, then you shoulda put a test on it.”" (The Beyoncé Rule)
- **[SWEBOK]** Guide to the Software Engineering Body of Knowledge (SWEBOK Guide) v4.0a. H. Washizaki (ed.), IEEE Computer Society. https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf. Accessed 2026-10-31.
  > "regression testing is the “selective retesting of a SUT to verify that modifications have not caused unintended effects and that the SUT still complies with its specified requirements.”" (Software Testing KA, 2.2.5)
- **[USDS]** Digital Services Playbook. U.S. Digital Service. https://playbook.usds.gov/. Accessed 2026-10-31.
  > "Conduct load and performance tests at regular intervals, including before public launch" (Play 10)
- **[WAI-TOOLS]** Selecting Web Accessibility Evaluation Tools. W3C WAI. https://www.w3.org/WAI/test-evaluate/tools/selecting/. Accessed 2026-10-31.
  > "Tools cannot check all accessibility aspects automatically. Human judgement is required." (What Evaluation Tools Can Do and Can Not Do)
  > "Web accessibility evaluation tools can not determine accessibility, they can only assist in doing so." (What Evaluation Tools Can Do and Can Not Do)
- **[WCAG22]** Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation, 12 December 2024. https://www.w3.org/TR/WCAG22/. Accessed 2026-10-31.
  > "For Level AA conformance, the web page satisfies all the Level A and Level AA success criteria, or a Level AA conforming alternate version is provided."
