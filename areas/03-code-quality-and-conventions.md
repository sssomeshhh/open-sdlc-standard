# 3. Code quality and conventions

- **ID prefix:** CQ
- **Status:** draft, 2026-10-31

## Purpose

This area protects against code that only its author can read, rules that live in reviewers' memory, and quality that decays
one small change at a time. It covers a written coding standard enforced by tools, comments that carry intent, limits on
complexity, dead code, code review, and a shared meaning of "done".

## Scope

Covers: coding standards, formatting, linting and static analysis, type safety, comments, complexity limits, dead code, code
review guidelines (what reviewers check and how fast), change size and descriptions, and the Definition of Done.

Leaves to other areas:
- Required reviews, approvals and branch protection: see Area 7.
- Running formatters, linters, type checks and tests as blocking pipeline gates: see Area 8.
- Lean repository and stray tracked files: see Area 7.
- Vulnerability, dependency and secret scanning: see Area 5.
- Test types and test strategy: see Area 4.
- The documentation system as a whole, and updating documentation in the same change: see Area 16 (DOC-4).
- Technical-debt tracking: see Area 18.

## Requirements

### CQ-1 · MUST · Written coding standard per language
The project MUST adopt a written coding standard for each language it uses (for example an established external guide plus
local additions).
- **Gate:** G1
- **Evidence:** a CONTRIBUTING or style file that names the guide for each language in the repository.
- **Basis:** [SWEBOK], [PEP8], [GTR-STD].

### CQ-2 · MUST · Automatic formatting
Code formatting MUST be done by an automatic formatter whose configuration is in the repository and which is checked on every
change (gate: CI-3), so formatting is never a review topic.
- **Gate:** G1
- **Evidence:** formatter configuration in the repository, and a pipeline step that fails on unformatted code.
- **Basis:** [SWE-STYLE].

### CQ-3 · MUST · Tool-enforced rules
Every coding rule that a tool can check MUST be enforced by a linter or static analyser on every change (gate: CI-3), not by
reviewers' memory.
- **Gate:** G1
- **Evidence:** linter configuration, a pipeline job running it, and a zero-warning or ratcheted baseline.
- **Basis:** [SWE-STYLE], [SSDF].

### CQ-4 · SHOULD · Low-noise analysis
Static analysis checks SHOULD be tuned to a low false-positive rate, with noisy checks fixed or disabled and every suppression
justified in place.
- **Gate:** G1
- **Evidence:** a documented suppression policy; no suppression without an inline reason; no file-wide or blanket
  suppressions.
- **Basis:** [SWE-STATIC].

### CQ-5 · MUST · Strict type checking
Where the language supports static typing, the strictest practical type-checking mode MUST be on and checked on every change
(gate: CI-3), with any relaxation listed per module.
- **Gate:** G1
- **Evidence:** strict settings in the type checker configuration (for example TypeScript `strict`, mypy `strict`), a pipeline
  step that runs it, and a documented list of per-module relaxations.
- **Basis:** [TS-STRICT]. Level: author's judgement (the source describes strict mode but does not require it).

### CQ-6 · SHOULD · Comments explain why
Inline comments SHOULD explain why the code exists or is written this way (intent, constraints, decisions), not restate what it
does.
- **Gate:** G2
- **Evidence:** a review sample of comments; no comments that only paraphrase the next line; non-obvious decisions carry a
  reason.
- **Basis:** [GTR-LOOK].

### CQ-7 · SHOULD · Documented public interfaces
Public modules, classes and functions SHOULD carry doc comments stating their purpose and usage.
- **Gate:** G2
- **Evidence:** doc comments on sampled public interfaces, or a documentation linter rule that requires them.
- **Basis:** Author's judgement (no primary source found).

### CQ-8 · SHOULD · Complexity limit
Function complexity SHOULD be limited by a measured threshold (for example cyclomatic complexity 10, up to 15 with a written
justification), with file and function size monitored.
- **Gate:** G1
- **Evidence:** complexity checker configuration and its output; each exception has a justification.
- **Basis:** [NIST-500-235].

### CQ-9 · SHOULD · No dead code
The codebase SHOULD NOT contain dead code: unreachable code, unused exports, unused dependencies, commented-out code or retired
feature flags.
- **Gate:** G2
- **Evidence:** a sample of the codebase and the output of an unused-code check show no dead code, or only items with an open
  removal ticket.
- **Basis:** [CWE-561], [ISO5055]. Items beyond dead code in the source's sense (unused exports and dependencies,
  commented-out code, retired feature flags): author's judgement.

### CQ-10 · SHOULD · Automated dead-code detection
Dead code and unused dependencies SHOULD be detected by tooling run on every change or on a fixed schedule.
- **Gate:** G1
- **Evidence:** an unused-code or unused-dependency check in the pipeline, or dated periodic reports.
- **Basis:** [CWE-561], [ISO5055].

### CQ-11 · SHOULD · Code review guidelines
The project SHOULD publish code review guidelines stating what reviewers check (design, functionality, complexity, tests,
naming, comments, style, documentation), the approval standard, and the expected response time (for example one business day).
- **Gate:** G1
- **Evidence:** a review guide in the repository; PR timestamps consistent with the stated response time.
- **Basis:** [GTR-STD], [GTR-LOOK], [GTR-SPEED].

### CQ-12 · SHOULD · Small, self-contained changes
Changes SHOULD be small and self-contained, with refactoring and reformatting in changes separate from functional changes.
- **Gate:** G1
- **Evidence:** PR size distribution, using the source's guide of about 100 changed lines as reasonable and 1000 as usually
  too large; refactoring PRs separate from feature or fix PRs; tests in the same PR as the code they test.
- **Basis:** [GTR-SMALL], [GTR-LOOK]. Reformatting kept separate: author's judgement.

### CQ-13 · SHOULD · Change descriptions
Each change SHOULD have a description that states what changed and why.
- **Gate:** G1
- **Evidence:** a PR template, and a sample of PR descriptions that state the reason for the change.
- **Basis:** [GTR-DESC].

### CQ-14 · MUST · Definition of Done
The team MUST keep a written Definition of Done that every change meets before it counts as complete or releasable; at
minimum: reviewed, tests pass, documentation updated, acceptance criteria met.
- **Gate:** G1
- **Evidence:** a Definition of Done document, linked from the PR template or checklist.
- **Basis:** [SCRUM]. Level: author's judgement (sources support SHOULD).

## Failure modes

- **Style debates in review.** Without a formatter and a style authority, review time goes on nits; "the style guide is the
  absolute authority" [GTR-STD].
- **Rules enforced by memory.** Without automation, rules get forgotten; automation "ensures that rules are not dropped or
  forgotten as time passes or as an organization scales up" [SWE-STYLE].
- **Noisy analysers ignored.** "low false-positive rates are often critical for developers to actually want to use a tool"
  [SWE-STATIC].
- **Huge changes rubber-stamped.** "1000 lines is usually too large" [GTR-SMALL].
- **"Done" means "merged".** Untested or undocumented work counts as complete because no shared Definition of Done exists
  [SCRUM].
- **Dead code kept "just in case".** It confuses readers and is still compiled, scanned and shipped [CWE-561].

## References

- **[CWE-561]** CWE-561: Dead Code (CWE 5.0). MITRE. https://cwe.mitre.org/data/definitions/561.html. Accessed 2026-10-31.
  > "The product contains dead code, which can never be executed." (Description)
  > "Remove dead code before deploying the application." (Potential Mitigations)
- **[GTR-DESC]** Writing good CL descriptions. Google Engineering Practices. https://google.github.io/eng-practices/review/developer/cl-descriptions.html. Accessed 2026-10-31.
  > "A CL description is a public record of change" (introduction)
  > "Why are these changes being made?" (introduction)
- **[GTR-LOOK]** What to look for in a code review. Google Engineering Practices. https://google.github.io/eng-practices/review/reviewer/looking-for.html. Accessed 2026-10-31.
  > "In general, tests should be added in the same CL as the production code unless the CL is handling an emergency ." (Tests)
  > "Usually comments are useful when they explain why some code exists, and should not be explaining what some code is doing." (Comments)
- **[GTR-SMALL]** Small CLs. Google Engineering Practices. https://google.github.io/eng-practices/review/developer/small-cls.html. Accessed 2026-10-31.
  > "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large, but it’s up to the judgment of your reviewer." (What is Small?)
  > "It’s usually best to do refactorings in a separate CL from feature changes or bug fixes." (Separate Out Refactorings)
- **[GTR-SPEED]** Speed of Code Reviews. Google Engineering Practices. https://google.github.io/eng-practices/review/reviewer/speed.html. Accessed 2026-10-31.
  > "One business day is the maximum time it should take to respond to a code review request"
- **[GTR-STD]** The Standard of Code Review. Google Engineering Practices. https://google.github.io/eng-practices/review/reviewer/standard.html. Accessed 2026-10-31.
  > "reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn’t perfect." (introduction)
  > "On matters of style, the style guide is the absolute authority." (Principles)
- **[ISO5055]** ISO/IEC 5055:2021 Information technology — Software measurement — Software quality measurement — Automated source code quality measures. ISO/IEC. https://www.iso.org/standard/80623.html. Accessed 2026-10-31. Paywalled; public abstract only. Mirror: https://committee.iso.org/standard/80623.html (verified 2026-10-31 on the committee.iso.org mirror; www.iso.org blocks automated access).
  > "The measures in this standard were calculated from detecting and counting violations of good architectural and coding practices in the source code that could result in unacceptable operational risks or excessive costs."
- **[NIST-500-235]** Structured Testing: A Testing Methodology Using the Cyclomatic Complexity Metric, NIST SP 500-235. A. H. Watson, T. J. McCabe, NIST, August 1996. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-235.pdf. Accessed 2026-10-31.
  > "Overly complex modules are more prone to error, are harder to understand, are harder to test, and are harder to modify." (2.5)
  > "The original limit of 10 as proposed by McCabe has significant supporting evidence, but limits as high as 15 have been used successfully as well." (2.5)
- **[PEP8]** PEP 8 – Style Guide for Python Code. G. van Rossum, B. Warsaw, A. Coghlan, Python Software Foundation. https://peps.python.org/pep-0008/. Accessed 2026-10-31.
  > "code is read much more often than it is written." (A Foolish Consistency is the Hobgoblin of Little Minds)
  > "A style guide is about consistency. Consistency with this style guide is important. Consistency within a project is more important." (A Foolish Consistency is the Hobgoblin of Little Minds)
- **[SCRUM]** The Scrum Guide (2020). Ken Schwaber and Jeff Sutherland. https://scrumguides.org/scrum-guide.html. Accessed 2026-10-31.
  > "The Definition of Done is a formal description of the state of the Increment when it meets the quality measures required for the product." (Commitment: Definition of Done)
  > "If a Product Backlog item does not meet the Definition of Done, it cannot be released or even presented at the Sprint Review." (Commitment: Definition of Done)
- **[SSDF]** NIST SP 800-218 Secure Software Development Framework (SSDF) Version 1.1. M. Souppaya, K. Scarfone, D. Dodson, NIST, February 2022. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf (landing page: https://csrc.nist.gov/pubs/sp/800/218/final). Accessed 2026-10-31.
  > "Use a static analysis tool to automatically check code for vulnerabilities and compliance with the organization’s secure coding standards with a human reviewing the issues reported by the tool" (PW.7.2, Example 4)
- **[SWE-STATIC]** Software Engineering at Google, Ch. 20 "Static Analysis". T. Winters, T. Manshreck, H. Wright (eds.), O'Reilly 2020, free online edition. https://abseil.io/resources/swe-book/html/ch20.html. Accessed 2026-10-31.
  > "We only deploy analysis tools with low false-positive rates" (Focus on Developer Happiness)
  > "low false-positive rates are often critical for developers to actually want to use a tool" (Focus on Developer Happiness)
- **[SWE-STYLE]** Software Engineering at Google, Ch. 8 "Style Guides and Rules". T. Winters, T. Manshreck, H. Wright (eds.), O'Reilly 2020, free online edition. https://abseil.io/resources/swe-book/html/ch08.html. Accessed 2026-10-31.
  > "when it comes to checking for compliance, rather than exclusively depending on engineer-based verification, we strongly prefer to automate enforcement with tooling." (Applying the Rules)
  > "Automated rule enforcement ensures that rules are not dropped or forgotten as time passes or as an organization scales up." (Applying the Rules)
- **[SWEBOK]** Guide to the Software Engineering Body of Knowledge (SWEBOK Guide) v4.0a. H. Washizaki (ed.), IEEE Computer Society. https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf. Accessed 2026-10-31.
  > "Defining and adopting apt coding standard for the project, and ensuring every team member implements the same in spirit is key for developing clean code" (Computing Foundations KA)
- **[TS-STRICT]** TSConfig Option: strict. Microsoft, TypeScript documentation. https://www.typescriptlang.org/tsconfig/strict.html. Accessed 2026-10-31.
  > "The strict flag enables a wide range of type checking behavior that results in stronger guarantees of program correctness."
