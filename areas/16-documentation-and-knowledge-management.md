# 16. Documentation and knowledge management

- **ID prefix:** DOC
- **Status:** draft, 2026-10-31

## Purpose
Knowledge that lives only in people's heads leaves with them, and documentation that is stored but never maintained becomes
wrong, which is worse than having none [WTD-PRIN]. This area makes sure the project's knowledge is written down, kept next to the
code, owned, reviewed and updated with each change, and handed over deliberately when people, teams or suppliers change.

## Scope
Covers the documentation system: which documentation exists, where each type lives, ownership, review, keeping documents in step
with code, the document lifecycle (create, update, archive, delete), the README, the storage and lifecycle of decision records,
onboarding and handover.

Left to other areas (the content rules for these documents live there; this area governs where they are kept and how they are
maintained):
- Requirements, acceptance criteria and the domain glossary: see Area 1.
- When an architecture decision record is needed and what it records: see Area 2.
- Code comments: see Area 3. Updating documentation in the same change as the code is set here (DOC-4); Area 3 refers to it.
- Local development set-up steps: see ENV-12 (Area 10); the onboarding path (DOC-13) links to them.
- Runbooks, incident reports and post-mortems: see Area 12.
- User documentation and in-app help: see UX-13 (Area 15).
- Release notes and user-facing release communication: see Areas 11 and 20.
- Running documentation checks as CI gates: see Area 8.

## Requirements

### DOC-1 · SHOULD · Written specifications and documentation
The project SHOULD have written specifications and documentation covering at least what the system has to do (the
specification, PRD-6), how it is built (architecture), how to set it up and run it locally, and how to operate it.
- **Gate:** G1
- **Evidence:** the documents, linked from the README; each document's last-updated date is not older than the last release that
  changed what it describes.
- **Basis:** [DORA-DOC].

### DOC-2 · SHOULD · Knowledge written down, not held in heads
Knowledge needed to build, run, change or support the system SHOULD be written down in the project's documentation, so that no
task depends on knowledge that only one person holds.
- **Gate:** G3
- **Evidence:** for a sample of recurring tasks (deploy, restore, data import, access change), a document that a second person can
  follow; no task listed as "ask a named person".
- **Basis:** [SRE-ACC], [AWS-KM].

### DOC-3 · MUST · Documentation in version control
Documentation MUST be under version control, in the repository of the code it describes; any documentation kept elsewhere (for
example a wiki) is linked from the repository (for example from the README).
- **Gate:** G1
- **Evidence:** a `docs/` folder or root-level documents in the repository; the repository links to every external location (for example from the README).
- **Basis:** [SWE-DOC], [WTD-DAC]. Linking documentation kept elsewhere from the README: author's judgement.

### DOC-4 · MUST · Documentation changes with the code
A change that alters documented behaviour, set-up, configuration or operation MUST update the affected documentation in the same
pull request. Code review checks this (review guidelines: see Area 3).
- **Gate:** G1
- **Evidence:** a documentation item in the pull-request template; sample pull requests that change code and docs together.
- **Basis:** [GDOC-BP], [SWE-DOC].
- Note: this is the single rule for documentation changing with code; other areas refer to it.

### DOC-5 · MUST · Owner and last-reviewed date
Every maintained document MUST have a named owner (a role or person) and a last-reviewed date.
- **Gate:** G1
- **Evidence:** front matter or a header in each document, or a code-ownership file that covers the docs.
- **Basis:** [SWE-DOC]. Last-reviewed date: author's judgement (the source supports ownership and reminders for untouched
  documents, not a recorded review date).

### DOC-6 · MUST · Documentation lifecycle
The project MUST have a defined way to create, update, review and archive or delete documents, including a review of any document
whose last-reviewed date is older than an age the project sets.
- **Gate:** G1
- **Evidence:** the documented lifecycle, stating the review age; review records; documents marked obsolete or removed in version
  history.
- **Basis:** [AWS-KM], [SWE-DOC]. Review triggered by age: author's judgement (the [SWE-DOC] quote describes reminders for untouched
  documents as an example).

### DOC-7 · SHOULD · Incorrect docs are defects
Incorrect documentation SHOULD be handled as a defect: fixed, or deleted when it can no longer be made right. When in doubt,
delete rather than keep a stale document.
- **Gate:** G1 · **Trigger:** each time documentation is found to be incorrect
- **Evidence:** documentation issues in the tracker; deletions of obsolete documents in version history.
- **Basis:** [GDOC-BP], [WTD-PRIN].

### DOC-8 · MUST · README essentials
The repository README MUST state what the project does, why it is useful, how to get started, where to get help, and who
maintains it.
- **Gate:** G1
- **Evidence:** the README, containing each of the five items.
- **Basis:** [GH-README]. Level: author's judgement (the source describes what READMEs typically include).

### DOC-9 · SHOULD · Documentation organised by reader need
Documentation SHOULD be organised by reader need into tutorials, how-to guides, reference and explanation, without mixing these
types on one page.
- **Gate:** G2
- **Evidence:** a documentation index grouped by these types.
- **Basis:** [DIATAXIS].

### DOC-10 · MUST · Decision records in the repository
Architecture decision records (required by Area 2) MUST be stored as short, numbered documents in the repository of the
application they affect, where they are versioned with the code. When a record is needed and how a changed decision supersedes
it: see ARC-1 and ARC-2.
- **Gate:** G1
- **Evidence:** a decisions folder (for example `docs/decisions/NNNN-title.md`) in each application repository.
- **Basis:** [NYGARD], [GDS-ADR], [MADR].

### DOC-11 · SHOULD · One canonical home per document
Each document SHOULD have one canonical location; other places link to it rather than copy it.
- **Gate:** G1
- **Evidence:** a documentation map; no conflicting copies of the same document.
- **Basis:** Author's judgement (no primary source found); consistent with the preference for a small set of fresh documents in
  [GDOC-BP].

### DOC-12 · SHOULD · Documentation review
Documentation changes SHOULD get a technical review for accuracy and, for documents read outside the team, an audience review for
clarity.
- **Gate:** G1
- **Evidence:** reviewers recorded on documentation pull requests.
- **Basis:** [SWE-DOC].

### DOC-13 · MUST · Onboarding path
The project MUST have a written onboarding path for newcomers: a reading order, a checklist, and set-up instructions (ENV-12) that
the most recent newcomer actually followed, updated with what they found missing.
- **Gate:** G2 · **Trigger:** each newcomer joining the project
- **Evidence:** the onboarding checklist; the date it was last updated and, once a newcomer has joined, last used.
- **Basis:** [SRE-ACC]. Applying it to all newcomers: author's judgement (the source is about engineers joining on-call).

### DOC-14 · MUST · Planned handover
When responsibility moves between people, teams or suppliers, the handover MUST follow a written knowledge-transfer plan (for
example pairing, walkthrough sessions and documentation brought up to date) that is completed before the outgoing party leaves.
- **Gate:** G1 · **Trigger:** each handover of responsibility between people, teams or suppliers
- **Evidence:** the handover plan; a record of the sessions; sign-off by the receiving party.
- **Basis:** [GOVUK-KT], [SRE-ACC]. Level: author's judgement (the GOV.UK source mandates a plan for contractors and supplier
  changes).

### DOC-15 · SHOULD · Measure documentation quality
Documentation quality SHOULD be measured at an interval the project sets, for example with a short team survey on whether docs
are easy to find and reliable.
- **Gate:** G3
- **Evidence:** the interval, recorded in the documentation lifecycle (DOC-6); survey results or other documentation metrics, with
  dates within that interval.
- **Basis:** [DORA-DOC].

### DOC-16 · MAY · Documentation checks in CI
Documentation MAY be linted and link-checked in CI, with merges blocked when a feature lacks documentation.
- **Gate:** G1
- **Evidence:** a CI job for documentation checks.
- **Basis:** [WTD-DAC].

## Failure modes
- A wiki or shared drive with no owners or review mechanism, so its content goes stale [AWS-KM].
- Docs updated "later", separately from the code, and drifting out of date [GDOC-BP].
- Large design documents that nobody maintains [NYGARD].
- Tutorial, how-to, reference and explanation mixed on one page, so no reader is served well [DIATAXIS].
- Knowledge held in one person's head that surfaces only at handover [SRE-ACC], [GOVUK-KT].
- Keeping wrong documents instead of deleting them [WTD-PRIN].

## References
- **[AWS-KM]** "OPS11-BP04 Perform knowledge management", AWS Well-Architected Framework, Operational Excellence Pillar. Amazon
  Web Services. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_knowledge_management.html.
  Accessed 2026-10-31.
  > "You have a self-hosted wiki but no mechanisms to manage information, resulting in outdated information." (Common anti-patterns)
  > "Mechanisms exist to create new information, update existing information, and archive outdated information." (introduction)
- **[DIATAXIS]** *Diátaxis*. Daniele Procida. https://diataxis.fr/. Accessed 2026-10-31.
  > "Diátaxis identifies four distinct needs, and four corresponding forms of documentation - tutorials, how-to guides, technical reference and explanation."
- **[DORA-DOC]** "Documentation quality". DORA (Google Cloud). https://dora.dev/capabilities/documentation-quality/.
  Accessed 2026-10-31.
  > "Analysis by DORA has found a clear link between documentation quality and organizational performance" (introduction)
  > "Documentation needs to be actively created and maintained, which takes work." (Creating quality documentation)
- **[GDOC-BP]** "Documentation Best Practices", Google Style Guides (docguide). Google.
  https://google.github.io/styleguide/docguide/best_practices.html. Accessed 2026-10-31.
  > "Change your documentation in the same CL as the code change." (Update Docs with Code)
  > "Dead docs are bad." (Delete Dead Documentation)
  > "Default to delete" (Delete Dead Documentation)
  > "A small set of fresh and accurate docs is better than a large assembly of" (Minimum Viable Documentation)
- **[GDS-ADR]** "Architecture decisions", The GDS Way. UK Government Digital Service.
  https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html. Accessed 2026-10-31.
  > "Architecture decisions should be stored in version control so there is a record of what was changed, who by, and when." (How to document decisions)
  > "Decisions that affect a specific application should be in that application’s code repository." (How to document decisions)
- **[GH-README]** "About READMEs", GitHub Docs. GitHub.
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes.
  Accessed 2026-10-31.
  > "README files typically include information on:" (introduction)
  > "What the project does" (introduction)
  > "Why the project is useful" (introduction)
  > "How users can get started with the project" (introduction)
  > "Where users can get help with your project" (introduction)
  > "Who maintains and contributes to the project" (introduction)
- **[GOVUK-KT]** "Working with contractors or third parties", GOV.UK Service Manual (last updated 17 October 2024). Government
  Digital Service. https://www.gov.uk/service-manual/the-team/working-contractors-third-parties. Accessed 2026-10-31.
  > "You must make sure you have a plan to pass knowledge from contractors to the rest of your team. This is particularly important when you move from one phase to another, or if you change supplier." (Transferring knowledge)
  > "make sure any documentation is in a good state" (Transferring knowledge)
- **[MADR]** "MADR: Markdown Architectural Decision Records". adr.github.io. https://adr.github.io/madr/. Accessed 2026-10-31.
  > "Create folder docs/decisions in your project." (Initialization)
  > "where NNNN indicates the next number in sequence." (Manual approach)
- **[NYGARD]** "Documenting Architecture Decisions", 15 November 2011. Michael Nygard, Cognitect.
  https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions. Accessed 2026-10-31.
  > "Large documents are never kept up to date. Small, modular documents have at least a chance at being updated." (Context)
  > "If a decision is reversed, we will keep the old one around, but mark it as superseded." (introduction)
- **[SRE-ACC]** "Accelerating SREs to On-Call and Beyond", *Site Reliability Engineering*, ch. 28. Google.
  https://sre.google/sre-book/accelerating-sre-on-call/. Accessed 2026-10-31.
  > "Put some amount of learning order into your system(s) so that your new SREs see a path before them." (Ch. 28, Learning Paths That Are Cumulative and Orderly)
  > "Newbie SREs are much more in need of up-to-date documentation" (Ch. 28, Documentation as Apprenticeship)
  > "Creating experts on the team whose techniques and knowledge are compartmentalized" (Ch. 28, You’ve Hired Your Next SRE(s), Now What?)
- **[SWE-DOC]** "Documentation", *Software Engineering at Google*, ch. 10. Tom Manshreck (O'Reilly 2020).
  https://abseil.io/resources/swe-book/html/ch10.html. Accessed 2026-10-31.
  > "Be placed under source control" (Documentation Is Like Code)
  > "Have clear ownership responsible for maintaining the docs" (Documentation Is Like Code)
  > "Undergo reviews for changes (and change with the code it documents)" (Documentation Is Like Code)
  > "A technical review, for accuracy." (Documentation Reviews)
  > "An audience review, for clarity." (Documentation Reviews)
  > "will send email reminders when the document hasn’t been touched in, for example, three months." (Deprecating Documents)
- **[WTD-DAC]** "Docs as Code". Write the Docs. https://www.writethedocs.org/guide/docs-as-code/. Accessed 2026-10-31.
  > "writing documentation with the same tools as code" (introduction)
  > "You can block merging of new features if they don’t include documentation" (introduction)
- **[WTD-PRIN]** "Documentation principles". Write the Docs. https://www.writethedocs.org/guide/writing/docs-principles/.
  Accessed 2026-10-31.
  > "Consider incorrect documentation to be worse than missing documentation."
