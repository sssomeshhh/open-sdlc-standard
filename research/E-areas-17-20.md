# Research E: Areas 17–20

Prepared 2026-10-31. All quotes were checked on the page or document named in
Sources on that date. Quotes are verbatim; some are a fragment of a longer sentence, marked with "…" only where text
was left out in the middle. Requirement wording is a candidate wording, not the source's; the areas set the final wording and levels.

Source keys shared across areas are defined once, in the area where they are first used, and reused by key.

---

## Area 17: Traceability (cross-cutting)

### Candidate requirements

1. **MUST** — Every requirement has a stable identifier that later artifacts (design notes, issues, commits, tests,
   release notes) can reference. *Evidence:* requirement/issue IDs exist and appear in PRs and tests; a sample of 10
   merged PRs each references at least one ID. *Sources:* NASA-SWE052, IEEE-29148.
2. **MUST** — Traceability is bi-directional: from each requirement forward to its design, code and tests, and from
   each change and test back to the requirement that justifies it. *Evidence:* a traceability matrix or a query
   (issue tracker ↔ PR ↔ test) that runs both ways; no orphan code changes and no untested requirements in a sample.
   *Sources:* NASA-SWE052.
3. **MUST** — Each code change (PR/merge request) is linked to the issue or requirement it addresses.
   *Evidence:* PR template field or closing keyword; repository rule or CI check that flags PRs without a link.
   *Sources:* GH-LINK, NASA-SWE052.
4. **SHOULD** — Each requirement's acceptance criteria are covered by at least one test whose name or metadata cites
   the requirement ID. *Evidence:* test-to-requirement mapping; coverage report per requirement for critical rules.
   *Sources:* NASA-SWE052, IEEE-29148.
5. **MUST** — Security requirements, risks and design decisions are recorded and kept current, so the reason for a
   control can be traced. *Evidence:* risk/decision log entries linked to requirements and to code.
   *Sources:* SSDF (PW.1.2).
6. **MUST** — Each release is identified by an immutable version, and the release records which changes (issues/PRs)
   it contains. *Evidence:* tags; changelog or release notes listing issue/PR IDs per version; a released version is
   never re-used. *Sources:* SEMVER, KACL, SSDF (PS.3.1).
7. **SHOULD** — Build provenance links each released artifact to the exact source revision and build that produced
   it. *Evidence:* provenance attestation or build metadata (commit SHA, build ID) attached to each artifact.
   *Sources:* SLSA-PROV, SSDF (PS.3.2).
8. **SHOULD** — The running production system exposes which version/commit is deployed, so an incident can be traced
   to a release. *Evidence:* version endpoint, image tag or deploy log mapping environment → version at a given time.
   [judgement], supported in part by SLSA-PROV.
9. **MUST** — Incidents and defects found in production are traced to a root cause, and the fix is traced back to
   the change or requirement gap that caused it. *Evidence:* post-incident record linking incident → root cause →
   fixing PR → regression test. *Sources:* SSDF (RV.3.1), SRE-PM.
10. **SHOULD** — Lessons from incidents and user feedback flow back into the requirements backlog and the process
    itself. *Evidence:* backlog items created from post-mortems/feedback, with a link to the source record; process
    change log. *Sources:* SSDF (RV.3.4), DORA-FEEDBACK.
11. **SHOULD** — Changes to requirements are themselves tracked (who, when, why) so that design and tests can be
    re-checked when a requirement changes. *Evidence:* requirement history in the tracker; impacted tests updated in
    the same change. *Sources:* NASA-SWE052 (rationale on refinement), IEEE-29148.
12. **MAY** — The project generates its traceability report automatically from tool data (tracker, VCS, CI) instead
    of maintaining it by hand. *Evidence:* script or dashboard; report date matches latest release. [judgement]

### Failure modes

- Matrix maintained by hand drifts from reality and is only refreshed before an audit. [judgement]
- PRs with no issue link ("drive-by" fixes), so the reason for a change is lost; plain `git blame` cannot recover it
  once history is rewritten. [judgement]
- Requirements refined or reinterpreted without trace, so the built feature diverges from the request (NASA-SWE052
  rationale: traceability makes it "less likely that requirements are misinterpreted as they are refined").
- Released artifacts cannot be tied to a commit (mutable `latest` tags, re-used version numbers) — contrary to SEMVER
  rule 3 and SLSA-PROV.
- Post-mortem findings never become backlog items, so the same root cause recurs (SSDF RV.3.4; SRE-PM: "An
  unreviewed postmortem might as well never have existed.").

### Sources

- **NASA-SWE052** — *SWE-052 – Bidirectional Traceability*, NASA Software Engineering Handbook (implements NPR 7150.2
  §3.12.1), NASA. https://swehb.nasa.gov/display/SWEHBVD/SWE-052+-+Bidirectional+Traceability — accessed 2026-10-31.
  - "The project manager shall perform, record, and maintain bi-directional traceability"
  - "Bidirectional traceability matrices also make it less likely that requirements are misinterpreted as they are refined."
- **IEEE-29148** — *ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements
  engineering*, IEEE SA catalogue page (paywalled; abstract only).
  https://standards.ieee.org/ieee/29148/6937/ — accessed 2026-10-31. (iso.org catalogue page returned HTTP 403.)
  - "It defines the construct of a good requirement, provides attributes and characteristics of requirements,"
  - "and discusses the iterative and recursive application of requirements processes throughout the life cycle."
- **GH-LINK** — *Linking a pull request to an issue*, GitHub Docs.
  https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue —
  accessed 2026-10-31.
  - "When you link a pull request to the issue the pull request addresses, collaborators can see that someone is working on the issue."
  - "When you merge a linked pull request into the default branch of a repository, its linked issue is automatically closed."
- **SSDF** — *NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1*, NIST, February 2022.
  https://doi.org/10.6028/NIST.SP.800-218 — accessed 2026-10-31.
  - PW.1.2: "Track and maintain the software’s security requirements, risks, and design decisions."
  - PS.3.1: "Securely archive the necessary files and supporting data (e.g., integrity verification information, provenance data) to be retained for each software release."
  - PS.3.2: "Collect, safeguard, maintain, and share provenance data for all components of each software release (e.g., in a software bill of materials [SBOM])."
  - RV.3.1: "Analyze identified vulnerabilities to determine their root causes." Example: "Record the root cause of discovered issues."
  - RV.3.4: "Review the SDLC process, and update it if appropriate to prevent (or reduce the likelihood of) the root cause recurring"
  - PO.2.1: "Periodically review and maintain the defined roles and responsibilities, updating them as needed."
- **SEMVER** — *Semantic Versioning 2.0.0*, Tom Preston-Werner. https://semver.org/ — accessed 2026-10-31.
  - "Once a versioned package has been released, the contents of that version MUST NOT be modified."
  - "Any modifications MUST be released as a new version."
- **KACL** — *Keep a Changelog 1.1.0*, Olivier Lacan. https://keepachangelog.com/en/1.1.0/ — accessed 2026-10-31.
  - "A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project"
  - "Changelogs are for humans, not machines."
- **SLSA-PROV** — *SLSA v1.0 Provenance*, OpenSSF SLSA. https://slsa.dev/spec/v1.0/provenance — accessed 2026-10-31.
  - "Provenance is an attestation that a particular build platform produced a set of software artifacts"
  - "The BuildDefinition describes all of the inputs to the build."
- **SRE-PM** — *Postmortem Culture: Learning from Failure*, Site Reliability Engineering (book), Google.
  https://sre.google/sre-book/postmortem-culture/ — accessed 2026-10-31.
  - "A blamelessly written postmortem assumes that everyone involved in an incident had good intentions."
  - "An unreviewed postmortem might as well never have existed."
  - Review criterion: "Is the action plan appropriate and are resulting bug fixes at appropriate priority?"
- **DORA-FEEDBACK** — *Capabilities: Customer feedback*, DORA. https://dora.dev/capabilities/customer-feedback/ —
  accessed 2026-10-31.
  - "Seek out and attend to customer feedback on product and feature quality."
  - "Delivery teams must be empowered to make changes to the design or specification of the system in response to feedback"

---

## Area 18: Process, planning and team

### Candidate requirements

1. **MUST** — All planned work, defects and change requests are recorded in a single issue tracker that is the
   project's ordered backlog. *Evidence:* tracker exists; work merged in the last release maps to tracker items;
   backlog has an explicit order/priority. *Sources:* SCRUM, GH-LINK.
2. **MUST** — Changes to the production system follow a defined change-control process: change types are defined,
   each change is reviewed and approved with its impact considered, and the decision is recorded and retained.
   *Evidence:* written change process; PR reviews/approvals; change records retained for a defined period.
   *Sources:* SP800-53 (CM-3, CM-4).
3. **SHOULD** — Routine change approval is done by peer review at code check-in rather than by an external change
   board, with the same fast process used for emergency changes. *Evidence:* branch protection requiring review;
   no separate manual CAB gate for standard changes; emergency changes go through the same pipeline.
   *Sources:* DORA-CA.
4. **MUST** — Roles and responsibilities across the life cycle (who decides, approves, builds, reviews, operates)
   are defined, named, and reviewed periodically. *Evidence:* roles/RACI document with named people; review date.
   *Sources:* SSDF (PO.2.1), SP800-53 (SA-3).
5. **MUST** — The project keeps a risk register: risks are identified, assessed for likelihood and impact, owned,
   reviewed on a schedule and updated on significant change. *Evidence:* register with owner, rating, response and
   last-review date per entry. *Sources:* NISTIR8286, SP800-53 (RA-3, PM-9).
6. **SHOULD** — Work is broken into small batches that can be completed and checked in days, not weeks.
   *Evidence:* median issue cycle time / PR size; items larger than a week are split. *Sources:* DORA-BATCH.
7. **SHOULD** — Estimates and capacity plans are recorded and compared with actuals so planning improves over time.
   *Evidence:* sprint/iteration plans with estimates and completed work; variance reviewed. [judgement]
8. **MUST** — The team holds regular retrospectives and tracks the resulting improvement actions to completion.
   *Evidence:* retrospective notes with dated actions and owners; actions visible in the tracker.
   *Sources:* SCRUM.
9. **MUST** — Known technical debt is recorded as backlog items with its cost ("interest") and is repaid on a
   planned basis. *Evidence:* debt label/items in tracker; a share of capacity or explicit items scheduled each
   period. *Sources:* CUNNINGHAM-DEBT; [judgement] for the capacity mechanism.
10. **SHOULD** — The project measures software delivery performance with the DORA metrics (change lead time,
    deployment frequency, change fail rate, failed deployment recovery time, deployment rework rate) at the
    application/service level. *Evidence:* metric definitions and a dashboard/report with history.
    *Sources:* DORA-METRICS.
11. **MUST** — Delivery metrics are used to improve a team's own performance over time, not to rank teams or as
    targets in themselves. *Evidence:* metric policy;
    no team league tables; several metrics in tension are tracked together. *Sources:* DORA-METRICS, DORA-VM.
12. **SHOULD** — Work in progress is visible to the whole team (board), with WIP limits. *Evidence:* board shows
    current state; WIP limits configured. *Sources:* DORA-VM.
13. **SHOULD** — A shared Definition of Done states the quality bar every increment must meet before it counts as
    complete. *Evidence:* written DoD; PR template/checklist references it. *Sources:* SCRUM.

### Failure modes

- Heavyweight external change approval (CAB) that slows delivery without lowering failure rates (DORA-CA: "these
  approaches have a negative impact on software delivery performance").
- Metrics turned into mandates or team comparisons, which invites gaming (DORA-METRICS: mandates increase "the
  likelihood that teams will try to game the metrics").
- Large batches that take weeks to finish and review (DORA-BATCH: "Any batch of code that takes longer than a week
  to complete and check is too big.").
- Retrospectives held but actions never tracked or closed. [judgement]
- Technical debt kept as tribal knowledge, not as backlog items, so the "interest" grows unseen (CUNNINGHAM-DEBT).
- Risk register written once at project start and never reviewed. [judgement], cf. RA-3 "Update the risk assessment".

### Sources

- **SCRUM** — *The Scrum Guide* (2020), Ken Schwaber and Jeff Sutherland. https://scrumguides.org/scrum-guide.html —
  accessed 2026-10-31.
  - "The Product Backlog is an emergent, ordered list of what is needed to improve the product."
  - "The purpose of the Sprint Retrospective is to plan ways to increase quality and effectiveness."
  - "The Definition of Done is a formal description of the state of the Increment"
- **SP800-53** — *NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations*,
  NIST. Control text taken from NIST's official OSCAL catalog (release 5.2.0):
  https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
  ; publication page https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final — accessed 2026-10-31.
  - CM-3: "Review proposed configuration-controlled changes to the system and approve or disapprove such changes with explicit consideration for security and privacy impact analyses;"
  - CM-3: "Document configuration change decisions associated with the system;"
  - CM-4: "Analyze changes to the system to determine potential security and privacy impacts prior to change implementation."
  - SA-3: "Define and document information security and privacy roles and responsibilities throughout the system development life cycle;"
  - RA-3: "Document risk assessment results in" … / "Review risk assessment results" (organisation-defined document and frequency).
  - PM-9: "Review and update the risk management strategy" (organisation-defined frequency).
- **DORA-CA** — *Capabilities: Streamlining change approval*, DORA. https://dora.dev/capabilities/streamlining-change-approval/
  — accessed 2026-10-31.
  - "However, DORA's research shows that these approaches have a negative impact on software delivery performance."
  - "change approvals are best implemented through peer review during the development process"
  - "Moving to a peer-review based process for individual changes, enforced at code check-in time"
- **NISTIR8286** — *NIST IR 8286 Rev. 1, Integrating Cybersecurity and Enterprise Risk Management (ERM)*, NIST,
  December 2025. https://csrc.nist.gov/pubs/ir/8286/r1/final — accessed 2026-10-31.
  - "This document includes guidance on the use of risk registers to set out cybersecurity risk"
- **DORA-BATCH** — *Capabilities: Working in small batches*, DORA. https://dora.dev/capabilities/working-in-small-batches/
  — accessed 2026-10-31.
  - "Any batch of code that takes longer than a week to complete and check is too big."
  - "Application features are sliced in a way that lets developers complete the work in one week or less."
- **CUNNINGHAM-DEBT** — Ward Cunningham, *The WyCash Portfolio Management System*, OOPSLA '92 Experience Report.
  https://c2.com/doc/oopsla92.html — accessed 2026-10-31.
  - "Shipping first time code is like going into debt."
  - "Every minute spent on not-quite-right code counts as interest on that debt."
- **DORA-METRICS** — *DORA's software delivery performance metrics*, DORA.
  https://dora.dev/guides/dora-metrics-four-keys/ — accessed 2026-10-31.
  - "The amount of time it takes for a change to go from committed to version control to deployed in production."
  - "The goal is to improve your team's performance over time, not to compete against other teams or organizations."
  - "Teams should identify multiple metrics, including some with a healthy amount of tension between them."
  - Note: the page names five metrics (incl. deployment rework rate), although its URL still says "four keys".
- **DORA-VM** — *Capabilities: Visual management*, DORA. https://dora.dev/capabilities/visual-management/ — accessed 2026-10-31.
  - "Visual management boards can create a shared understanding of where the team is"
  - "Displays should be used to drive improvements (fix the problem), not become a goal in themselves (keep the board green)."
- **SSDF**, **GH-LINK** — see Area 17.

---

## Area 19: AI-assisted development

### Candidate requirements

1. **MUST** — The organisation/project publishes an AI-use stance: which AI tools are allowed, allowed with
   guardrails, or prohibited, and for which data classifications. *Evidence:* written policy with an approved-tools
   list and data-classification mapping; date of last update. *Sources:* DORA-AI, AI600 (GV-3.2-003, GV-6.1-007).
2. **MUST** — AI tools and services in use are inventoried, and third-party AI providers are assessed before
   adoption (security, data privacy, IP terms). *Evidence:* inventory of tools/models with owner and terms;
   vendor assessment record. *Sources:* AI600 (GV-1.6-001, GV-6.1-007, GV-6.1-009).
3. **MUST** — Confidential data, personal data and secrets are not placed in prompts or agent context unless the
   policy explicitly permits that tool for that data class. *Evidence:* policy clause; training record; technical
   controls (see 4). *Sources:* OWASP-LLM02, AI600 (Data Privacy), DORA-AI.
4. **SHOULD** — Technical controls stop agents from reading secrets and sensitive files (e.g. deny rules for `.env`,
   content exclusion), and their limits are documented. *Evidence:* committed deny/exclusion configuration; note of
   known gaps. *Sources:* CC-SETTINGS, GH-EXCL.
5. **MUST** — Project-level agent instructions (e.g. `CLAUDE.md`/`AGENTS.md`, `.github/copilot-instructions.md`) are
   stored in the repository, version-controlled and reviewed like code. *Evidence:* file in repo; changes via PR.
   *Sources:* CC-MEMORY, GH-INSTR.
6. **SHOULD** — Shared agent configuration (permissions, hooks) is committed for the team, while personal overrides
   stay out of version control. *Evidence:* committed `.claude/settings.json` (or equivalent); `*.local.*` ignored.
   *Sources:* CC-SETTINGS, CC-SEC.
7. **SHOULD** — Agent instruction files are kept concise and reviewed periodically to remove outdated or conflicting
   rules. *Evidence:* file size within vendor guidance; review history. *Sources:* CC-MEMORY.
8. **MUST** — Hard rules that must never be broken are enforced by tooling (permissions, hooks, CI, branch
   protection), not only by natural-language instructions. *Evidence:* deny rules/hooks/CI checks for each critical
   rule. *Sources:* CC-MEMORY ("context, not enforced configuration").
9. **MUST** — AI-generated code receives the same or stricter human review as human-written code before merge; the
   human who merges is accountable for it. *Evidence:* PR approvals by a human on agent-authored PRs; review policy.
   *Sources:* AI600 (MS-2.6-004), GH-AGENT, CC-SEC, GH-BP.
10. **MUST** — AI-generated code passes the same automated gates (tests, lint, type checks, security and licence
    scans) as any other change. *Evidence:* CI runs on agent PRs; no bypass. *Sources:* GH-BP, OWASP-LLM09.
11. **MUST** — Dependencies suggested by AI are verified to exist and be the intended package before they are added
    (hallucinated-package risk). *Evidence:* dependency review step; lockfile diff reviewed. *Sources:* OWASP-LLM09.
12. **MUST** — Coding agents run with least privilege: minimum tools and permissions, no production credentials, and
    human approval for high-impact actions (deploys, data changes, pushes to protected branches). *Evidence:*
    agent permission config; sandbox/network settings; CI secrets not exposed to agent runs. *Sources:* OWASP-LLM06,
    GH-AGENT, CC-SEC.
13. **SHOULD** — Untrusted content (web pages, issues, third-party files, MCP servers) given to agents is treated as
    a prompt-injection risk; only trusted MCP servers/tools are enabled. *Evidence:* allowlisted MCP servers;
    guidance in policy. *Sources:* CC-SEC, OWASP-LLM02.
14. **SHOULD** — Factual or design claims produced by AI in documents are verified against primary sources before
    use (confabulation risk). *Evidence:* review checklist; citations in AI-assisted documents. *Sources:* AI600
    (Confabulation), OWASP-LLM09.
15. **MAY** — The project records which changes were substantially AI-generated (e.g. commit trailer) to support
    later review, provenance and IP questions. *Evidence:* trailer/label convention. *Sources:* AI600 (GV-6.1-008,
    content provenance) — application to code is [judgement].

### Failure modes

- Over-reliance: AI output merged without verification (OWASP-LLM09: "Overreliance occurs when users place excessive
  trust in LLM-generated content, failing to verify its accuracy.").
- Hallucinated or typo-squatted packages added from AI suggestions (OWASP-LLM09).
- Secrets or personal data pasted into prompts or readable by an agent from `.env` files (OWASP-LLM02; CC-SETTINGS
  deny-rule example).
- Agent given broad credentials or auto-approval for destructive actions (OWASP-LLM06 "Excessive Agency").
- Critical rules written only in `CLAUDE.md`, which the tool treats as context, not enforced configuration (CC-MEMORY).
- Per-developer, unversioned agent setups, so behaviour differs across the team and is not reviewable. [judgement]

### Sources

- **AI600** — *NIST AI 600-1, Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence
  Profile*, NIST, July 2024. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf (overview:
  https://www.nist.gov/itl/ai-risk-management-framework) — accessed 2026-10-31.
  - Data Privacy: "Impacts due to leakage and unauthorized use, disclosure, or de-anonymization of biometric, health, location, or other personally identifiable information or sensitive data."
  - Confabulation: "The production of confidently stated but erroneous or false content (known colloquially as “hallucinations” or “fabrications”)"
  - MS-2.6-004: "Review GAI system outputs for validity and safety: Review generated code to assess risks that may arise from unreliable downstream decision-making."
  - GV-1.6-001: "Enumerate organizational GAI systems for incorporation into AI system inventory"
  - GV-6.1-007: "Inventory all third-party entities with access to organizational content and establish approved GAI technology and service provider lists."
  - GV-3.2-003: "Define acceptable use policies for GAI interfaces, modalities, and human-AI configurations"
  - GV-6.1-008: "Maintain records of changes to content made by third parties to promote content provenance, including sources, timestamps, metadata."
- **AIRMF** — *AI Risk Management Framework* (overview page), NIST. https://www.nist.gov/itl/ai-risk-management-framework
  — accessed 2026-10-31.
  - "is intended for voluntary use and to improve the ability to incorporate trustworthiness considerations"
  - The Generative AI Profile "can help organizations identify unique risks posed by generative AI"
- **OWASP-LLM02** — *LLM02:2025 Sensitive Information Disclosure*, OWASP Top 10 for LLM Applications 2025, OWASP GenAI
  Security Project. https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ — accessed 2026-10-31.
  - "Provide guidance on avoiding the input of sensitive information."
  - "such restrictions may not always be honored and could be bypassed via prompt injection or other methods."
- **OWASP-LLM06** — *LLM06:2025 Excessive Agency*, OWASP. https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
  — accessed 2026-10-31.
  - "Limit the extensions that LLM agents are allowed to call to only the minimum necessary."
  - "Utilise human-in-the-loop control to require a human to approve high-impact actions before they are taken."
- **OWASP-LLM09** — *LLM09:2025 Misinformation*, OWASP. https://genai.owasp.org/llmrisk/llm092025-misinformation/ —
  accessed 2026-10-31.
  - "Attackers experiment with popular coding assistants to find commonly hallucinated package names."
  - "Establish secure coding practices to prevent the integration of vulnerabilities due to incorrect code suggestions."
- **DORA-AI** — *Capabilities: Clear and communicated AI stance*, DORA (AI Capabilities Model).
  https://dora.dev/capabilities/clear-and-communicated-ai-stance/ — accessed 2026-10-31.
  - "Is it clear which tools are permitted?"
  - "which data classification levels are appropriate for which tools"
  - "Publish it as a living document in a central, searchable developer hub."
- **CC-MEMORY** — *How Claude remembers your project*, Claude Code Docs, Anthropic. https://code.claude.com/docs/en/memory
  — accessed 2026-10-31.
  - "These instructions are shared with your team through version control, so focus on project-level standards rather than personal preferences."
  - "Claude treats them as context, not enforced configuration."
  - "Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions."
  - "target under 200 lines per CLAUDE.md file."
- **CC-SETTINGS** — *Settings files and precedence*, Claude Code Docs, Anthropic. https://code.claude.com/docs/en/settings
  — accessed 2026-10-31.
  - "Commit `.claude/settings.json` so everyone who clones the repository gets the same permissions, hooks, and plugins."
  - Example deny rules shown on the page: `"Read(./.env)"`, `"Read(./.env.*)"` (to "stop it reading `.env` files").
- **CC-SEC** — *Security*, Claude Code Docs, Anthropic. https://code.claude.com/docs/en/security — accessed 2026-10-31.
  - "You're responsible for reviewing proposed code and commands for safety before approval."
  - "Share approved permission configurations through version control"
  - "We encourage either writing your own MCP servers or using MCP servers from providers that you trust."
- **GH-INSTR** — *Adding repository custom instructions for GitHub Copilot*, GitHub Docs.
  https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions — accessed 2026-10-31.
  - "These are specified in a `copilot-instructions.md` file in the `.github` directory of the repository."
  - "You can create one or more `AGENTS.md` files, stored anywhere within the repository."
- **GH-EXCL** — *Content exclusion for GitHub Copilot*, GitHub Docs.
  https://docs.github.com/en/copilot/concepts/context/content-exclusion — accessed 2026-10-31.
  - "You can use content exclusion to configure Copilot to ignore certain files."
  - "Content exclusion is a guardrail for the tools that GitHub controls."
- **GH-BP** — *Best practices for using GitHub Copilot*, GitHub Docs.
  https://docs.github.com/en/copilot/get-started/best-practices — accessed 2026-10-31.
  - "Understand suggested code before you implement it."
  - "Use automated tests and tooling to check Copilot's work."
- **GH-AGENT** — *Responsible use of Copilot coding agent*, GitHub Docs.
  https://docs.github.com/en/copilot/responsible-use/copilot-coding-agent — accessed 2026-10-31.
  - "You should review all outputs generated by the agent thoroughly prior to merging."
  - "The agent does not have access to Actions organization or repository secrets"

---

## Area 20: Governance, compliance and sustainability

### Candidate requirements

1. **MUST** — A named accountable owner (business/system owner) formally accepts the system before it goes into
   operation, against agreed acceptance criteria, and the acceptance is recorded. *Evidence:* signed/recorded
   go-live approval referencing acceptance criteria and UAT results. *Sources:* SP800-53 (CA-6, SA-4).
2. **SHOULD** — Authorisation to operate is revisited on significant change, not given once forever. *Evidence:*
   re-approval records for major releases/architecture changes. *Sources:* SP800-53 (CA-6 "Update the
   authorizations").
3. **MUST** — Third-party suppliers and external services (cloud, SaaS, contractors, AI providers) are identified,
   assessed for risk before use, bound by contract to the organisation's security and privacy requirements, and
   monitored. *Evidence:* supplier list with risk rating; contract clauses; periodic review records.
   *Sources:* SP800-161, SP800-53 (SA-9, SR-6, SA-4).
4. **SHOULD** — The project keeps a supply-chain risk management plan covering acquisition through to disposal, and
   reviews it on change. *Evidence:* C-SCRM plan with review date. *Sources:* SP800-53 (SR-2), SP800-161.
5. **MUST** — An inventory of system components (including third-party software and services) is kept accurate and
   reviewed. *Evidence:* component inventory/SBOM plus service list; review date. *Sources:* SP800-53 (CM-8),
   SSDF (PS.3.2).
6. **MUST** — Components that lose vendor support (end of life) are replaced, or an alternative support source is
   arranged; EOL dates are tracked ahead of time. *Evidence:* EOL register for runtimes, frameworks, OS images,
   managed services; upgrade plans. *Sources:* SP800-53 (SA-22).
7. **MUST** — Each release to users is accompanied by release communication (what changed, who is affected) and
   updated user and administrator documentation. *Evidence:* release notes/announcements per release; user and
   admin guides versioned with the release. *Sources:* KACL, SP800-53 (SA-5).
8. **SHOULD** — Users receive training or guidance appropriate to new or changed functionality before or at release.
   *Evidence:* training material, sessions log, in-app help updates. [judgement]; SA-5 covers documentation only.
9. **MUST** — A support model is defined: how users get help, who handles which level, and expected response times.
   *Evidence:* published support route and ownership; ticket statistics. [judgement] — ITIL practice guides are
   paywalled; see Gaps.
10. **MUST** — User feedback and support data are collected and fed into the backlog. *Evidence:* feedback channel;
    backlog items linked to feedback. *Sources:* DORA-FEEDBACK.
11. **MUST** — Long-term maintenance is planned: who maintains the system after the project ends, how corrective,
    preventive, adaptive and perfective changes are handled, and with what budget. *Evidence:* maintenance plan;
    named maintaining team; handover record. *Sources:* IEEE-14764, IEEE-12207 (maintenance stage in scope);
    category names are [judgement] pending the 14764 text.
12. **MUST** — Retirement/decommissioning is planned before it happens: users told in advance, how their need will
    be met afterwards, data retained/migrated/deleted per policy, credentials and infrastructure removed, residual
    risks recorded. *Evidence:* decommissioning plan and closure checklist; data disposition record.
    *Sources:* GOVUK-RETIRE, SP800-53 (SR-12), IEEE-12207 (disposal in scope).
13. **SHOULD** — Data, documentation and components are disposed of securely whenever they leave use, not only at
    final retirement. *Evidence:* disposal procedure; records of key/secret revocation and storage deletion.
    *Sources:* SP800-53 (SR-12 guidance).
14. **SHOULD** — The project follows a recognised life-cycle process model (e.g. ISO/IEC/IEEE 12207) and records how
    its own process maps to it. *Evidence:* process description with mapping. *Sources:* IEEE-12207.

### Failure modes

- No named owner after the delivery team leaves; the system runs unowned until something breaks. [judgement]
- Vendor/SaaS adopted by a single team without assessment or contract terms on security and data (SP800-161 abstract:
  "decreased visibility into and understanding of how the technology they acquire is developed").
- Runtimes and base images left past end of support (SP800-53 SA-22 guidance: unsupported components "can result in
  an opportunity for adversaries to exploit weaknesses").
- Releases shipped silently: users learn about changes from errors, and support is not briefed. [judgement]
- "Switch-off" decommissioning: servers stopped but data, DNS, credentials and backups left behind (SR-12; GOVUK-RETIRE:
  "You should have a plan for securing the information you've got about your users.").

### Sources

- **SP800-53** — see Area 18. Additional controls used here (verbatim, from the OSCAL catalog release 5.2.0):
  - CA-6: "Ensure that the authorizing official for the system, before commencing operations:" … "Authorizes the system to operate;"
  - SA-4: "Allocation of responsibility or identification of parties responsible for information security, privacy, and supply chain risk management; and" / "Acceptance criteria."
  - SA-9: "Require that providers of external system services comply with organizational security and privacy requirements and employ the following controls:"
  - SR-6: "Assess and review the supply chain-related risks associated with suppliers or contractors and the system, system component, or system service they provide"
  - SR-2: "Develop a plan for managing supply chain risks associated with the research and development, design, manufacturing, acquisition, delivery, integration, operations and maintenance, and disposal"
  - CM-8: "Develop and document an inventory of system components that:" … "Accurately reflects the system;"
  - SA-22: "Replace system components when support for the components is no longer available from the developer, vendor, or manufacturer; or"
  - SA-5: "Obtain or develop user documentation for the system, system component, or system service that describes:"
  - SR-12 guidance: "Data, documentation, tools, or system components can be disposed of at any time during the system development life cycle"
- **SP800-161** — *NIST SP 800-161 Rev. 1 (update 1), Cybersecurity Supply Chain Risk Management Practices for Systems and
  Organizations*, NIST, May 2022 (updated November 2024). https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final —
  accessed 2026-10-31.
  - "The publication integrates cybersecurity supply chain risk management (C-SCRM) into risk management activities"
  - "decreased visibility into and understanding of how the technology they acquire is developed"
- **IEEE-12207** — *ISO/IEC/IEEE 12207:2017 Systems and software engineering — Software life cycle processes*, IEEE SA
  catalogue page (paywalled; abstract only). https://standards.ieee.org/ieee/12207/5672/ — accessed 2026-10-31. The
  page marks the 2017 edition as superseded. The successor, ISO/IEC/IEEE 12207:2026 (published 2026-04), is listed on
  the ISO catalogue; see ISO12207 in research A.
  - "This International Standard establishes a common framework for software life cycle processes"
  - "during the supply, development, operation, maintenance and disposal of software products"
- **IEEE-14764** — *ISO/IEC/IEEE 14764:2022 (IEEE 14764-2021) Software engineering — Software life cycle processes —
  Maintenance*, IEEE SA catalogue page (paywalled; abstract only). https://standards.ieee.org/ieee/14764/7701/ —
  accessed 2026-10-31.
  - "This standard describes an iterative process for managing and executing software maintenance activities."
  - "Use of this standard is not restricted by size, complexity, criticality, or application of the software product."
- **GOVUK-RETIRE** — *Retiring your service*, GOV.UK Service Manual, UK Government Digital Service.
  https://www.gov.uk/service-manual/phases/retirement — accessed 2026-10-31.
  - "When retiring a service you should consider user needs in the same way you did when you built the service."
  - "You need to consider how the user need your service met will be met after your service is retired."
  - "You should have a plan for securing the information you've got about your users."
- **KACL**, **SSDF** — see Area 17. **DORA-FEEDBACK** — see Area 17.

---

## Gaps (could not source with a verified quote)

- **SWEBOK v4.0a** — not quoted in this file. The guide (v4.0a, PDF title page "Released August 2026") is cited and
  quoted in research A (key SWEBOK); its maintenance categories and process/measurement KAs were not used here.
- **ISO catalogue pages (www.iso.org)** refuse automated access; IEEE SA pages were used instead. ISO 31000 (risk) abstract not
  verified.
- **ISO/IEC/IEEE 14764 maintenance categories** (corrective, preventive, adaptive, perfective) — not visible in the
  public abstract; the maintenance-plan requirement uses them as [judgement].
- **ITIL 4** (change enablement, service desk, release management, support model) — practice guides are paywalled; no
  free primary text found. The support model and training candidates remain [judgement].
- **Estimation / capacity planning** and **RACI** as a named technique — no primary standard with free text found;
  covered by [judgement] and by SSDF PO.2.1 / SP 800-53 SA-3 for roles.
- **Production version ↔ incident tracing** — no single primary source states it; partly supported by SLSA.
- **12207 newer edition** — the IEEE page says the 2017 edition is superseded. The successor, ISO/IEC/IEEE 12207:2026,
  is listed on the ISO catalogue (see research A); this file quotes only the 2017 abstract.
- **GOV.UK Security guidance on decommissioning** (security.gov.uk) returned HTTP 403; not used.
