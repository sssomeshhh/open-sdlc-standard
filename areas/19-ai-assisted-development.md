# 19. AI-assisted development

- **ID prefix:** AI
- **Status:** draft, 2026-10-31

## Purpose
AI coding assistants and agents can write code, run commands and read the repository. Used without rules, they
introduce unreviewed or invented code, packages that do not exist, inconsistent behaviour across the team, and
agents with more access than any person would be given. This area sets the tooling rules that keep AI-assisted work
reviewable, reproducible and within least privilege, with a human accountable for every change.

## Scope
The project's AI-use stance and tool inventory, shared and versioned agent configuration, enforcement of hard rules,
review and gating of AI-generated code, agent permissions, untrusted input to agents, and provenance of AI-generated
changes. It leaves to other areas:

- No personal or confidential data in prompts or agent context: see Area 6. This area only adds technical controls
  that support that rule (AI-7).
- Secrets policy: see Area 5.
- Code review guidelines: see Area 3. Required reviews and branch protection: see Area 7.
- Running scans and tests as CI gates: see Area 8.
- Dependency pinning and provenance of build artifacts: see Area 9.
- Assessing AI providers as third-party suppliers: see Area 20.

## Requirements

### AI-1 · MUST · Published AI-use stance
The project MUST publish its AI-use stance: which AI tools are allowed, allowed with guardrails, or prohibited, and
which data classifications each allowed tool is permitted to receive (the data rule itself is in Area 6).
- **Gate:** G1
- **Evidence:** a written, dated policy with the stance per tool and a tool-to-data-classification mapping, stored
  where the team can find it. The inventory of tools in use, with owners and approved providers: AI-2.
- **Basis:** [DORA-AI], [AI600] (GV-3.2-003), [OWASP-LLM02]. Level: author's judgement (sources support SHOULD).

### AI-2 · MUST · Inventory of AI tools and providers
AI tools, models and services in use MUST be listed in an inventory with an owner per entry, with use limited to
approved providers.
- **Gate:** G1 · **Trigger:** each new AI tool, model or provider
- **Evidence:** the inventory with an owner per entry; the approved-provider list; no tools in use that are missing
  from either. Supplier terms: GOV-4.
- **Basis:** [AI600] (GV-1.6-001, GV-6.1-007).

### AI-3 · MUST · Agent instructions versioned in the repository
Project-level agent instructions (for example `AGENTS.md`, `CLAUDE.md` or `.github/copilot-instructions.md`) MUST be
stored in the repository and changed only through the normal review process.
- **Gate:** G1
- **Evidence:** the instruction files in version control; their history shows changes made through reviewed pull
  requests.
- **Basis:** [CC-MEMORY], [GH-INSTR].

### AI-4 · SHOULD · Shared agent configuration committed
Shared agent configuration (permissions, hooks, allowed tools) SHOULD be committed for the whole team, with personal
overrides kept out of version control.
- **Gate:** G1
- **Evidence:** a committed shared settings file; personal or local settings files listed in the ignore rules.
- **Basis:** [CC-SETTINGS], [CC-SEC].

### AI-5 · SHOULD · Instruction files concise and reviewed
Agent instruction files SHOULD be kept concise and reviewed periodically to remove outdated or conflicting rules.
- **Gate:** G1
- **Evidence:** file length within the tool vendor's guidance; a review date or review history.
- **Basis:** [CC-MEMORY].

### AI-6 · MUST · Hard rules enforced by tooling
Critical rules MUST be enforced by tooling (permissions, hooks, CI checks or branch protection), not only by
natural-language instructions to the agent.
- **Gate:** G1
- **Evidence:** a list of the project's critical rules; for each, a matching deny rule, hook or CI check.
- **Basis:** [CC-MEMORY]. The source states that instructions are not enforced; requiring enforcement by tooling is
  the author's judgement.

### AI-7 · MUST · Agents blocked from secret and sensitive files
Technical controls MUST stop agents from reading secrets and sensitive files (for example deny rules for `.env`
files, or content exclusion), with the known limits of those controls written down.
- **Gate:** G1
- **Evidence:** committed deny or exclusion configuration; a note of known gaps.
- **Basis:** [CC-SETTINGS], [GH-EXCL]. Level: author's judgement (sources describe the controls; the MUST enforces PRV-11). See Area 5 for secrets and Area 6 for personal data.

### AI-8 · MUST · Human review of AI-generated code
AI-generated code MUST be reviewed by a human to at least the same standard as human-written code before merge, and
the person who approves the merge is accountable for it.
- **Gate:** G1
- **Evidence:** human approvals on agent-authored pull requests; a review policy that states accountability.
- **Basis:** [AI600] (MS-2.6-004), [GH-AGENT], [CC-SEC], [GH-BP]. "At least the same standard" and the approver's
  accountability: author's judgement.

### AI-9 · MUST · Same automated gates
AI-generated changes MUST pass the same automated gates (tests, lint, type checks, security and licence scans) as
any other change, with no bypass.
- **Gate:** G1
- **Evidence:** CI runs recorded on agent-authored pull requests; no bypass permission granted to agents.
- **Basis:** [GH-BP], [OWASP-LLM09].

### AI-10 · MUST · AI-suggested dependencies verified
Any dependency suggested by an AI tool MUST be checked to exist and to be the intended package before it is added.
- **Gate:** G1 · **Trigger:** each dependency suggested by an AI tool
- **Evidence:** dependency review step in the change process; lockfile changes reviewed in the pull request.
- **Basis:** [OWASP-LLM09]. The existence check as the control: author's judgement.

### AI-11 · MUST · Least privilege for agents
Coding agents MUST run with the minimum tools and permissions needed, which excludes production credentials.
- **Gate:** G1
- **Evidence:** agent permission configuration; sandbox or network settings; CI secrets and production credentials not
  exposed to agent runs.
- **Basis:** [OWASP-LLM06], [GH-AGENT], [CC-SEC]. Excluding production credentials: author's judgement.

### AI-12 · MUST · Human approval for high-impact agent actions
High-impact agent actions (deploys, data changes, pushes to protected branches) MUST require explicit human approval
before they run.
- **Gate:** G1 · **Trigger:** each high-impact agent action
- **Evidence:** permission configuration that requires approval for these actions; no auto-approve setting for them.
- **Basis:** [OWASP-LLM06], [CC-SEC].

### AI-13 · SHOULD · Untrusted input and tool servers
Untrusted content given to agents (web pages, issues, third-party files) SHOULD be treated as a prompt-injection
risk, with only trusted tool servers (for example MCP servers) enabled.
- **Gate:** G1
- **Evidence:** an allowlist of enabled tool servers; guidance on untrusted input in the AI-use policy.
- **Basis:** [OWASP-LLM01], [CC-SEC], [OWASP-LLM02].

### AI-14 · SHOULD · AI-produced claims verified
Factual or design claims produced by AI in documents SHOULD be checked against primary sources before use.
- **Gate:** G0
- **Evidence:** a review checklist item; citations in AI-assisted documents.
- **Basis:** [AI600] (Confabulation), [OWASP-LLM09].

### AI-15 · MAY · Record of AI-generated changes
The project MAY mark changes that were substantially AI-generated (for example with a commit trailer or label) to
support later review, provenance and intellectual-property questions.
- **Gate:** G1
- **Evidence:** a documented trailer or label convention, applied in recent history.
- **Basis:** [AI600] (GV-6.1-008). Applying it to code is the author's judgement.

## Failure modes
- Over-reliance: AI output merged without verification [OWASP-LLM09].
- Hallucinated or typo-squatted packages added from AI suggestions: "Attackers experiment with popular coding
  assistants to find commonly hallucinated package names." [OWASP-LLM09].
- Secrets or personal data readable by an agent from `.env` files [CC-SETTINGS]; see Area 6 for the data rule.
- An agent given broad credentials or auto-approval for destructive actions [OWASP-LLM06].
- Critical rules written only in an instruction file, which the tool treats "as context, not enforced
  configuration" [CC-MEMORY].
- Per-developer, unversioned agent setups, so behaviour differs across the team and cannot be reviewed. (Author's
  judgement.)

## References
- **[AI600]** NIST AI 600-1, Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence
  Profile. NIST, July 2024. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf (overview:
  https://www.nist.gov/itl/ai-risk-management-framework). Accessed 2026-10-31.
  > "The production of confidently stated but erroneous or false content (known colloquially as “hallucinations” or “fabrications”)" (Confabulation)
  > "Review GAI system outputs for validity and safety: Review generated code to assess risks that may arise from unreliable downstream decision-making." (MS-2.6-004)
  > "Enumerate organizational GAI systems for incorporation into AI system inventory" (GV-1.6-001)
  > "Inventory all third-party entities with access to organizational content and establish approved GAI technology and service provider lists." (GV-6.1-007)
  > "Define acceptable use policies for GAI interfaces, modalities, and human-AI configurations" (GV-3.2-003)
  > "Maintain records of changes to content made by third parties to promote content provenance, including sources, timestamps, metadata." (GV-6.1-008)
- **[CC-MEMORY]** How Claude remembers your project. Claude Code Docs, Anthropic. https://code.claude.com/docs/en/memory.
  Accessed 2026-10-31. Cited as an example of vendor guidance; the rules apply to any agent tool.
  > "These instructions are shared with your team through version control, so focus on project-level standards rather than personal preferences." (Set up a project CLAUDE.md)
  > "Claude treats them as context, not enforced configuration." (CLAUDE.md vs auto memory)
  > "Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions." (Write effective instructions)
  > "target under 200 lines per CLAUDE.md file." (Write effective instructions)
- **[CC-SEC]** Security. Claude Code Docs, Anthropic. https://code.claude.com/docs/en/security. Accessed 2026-10-31.
  > "You're responsible for reviewing proposed code and commands for safety before approval." (User responsibility)
  > "Share approved permission configurations through version control" (Team security)
  > "We encourage either writing your own MCP servers or using MCP servers from providers that you trust." (MCP security)
- **[CC-SETTINGS]** Settings files and precedence. Claude Code Docs, Anthropic. https://code.claude.com/docs/en/settings.
  Accessed 2026-10-31. The second quote introduces the page's example of deny rules for `.env` files.
  > "Commit `.claude/settings.json` so everyone who clones the repository gets the same permissions, hooks, and plugins." (Share settings with your team)
  > "For example, to let Claude Code run your lint and test commands without asking and stop it reading `.env` files, add this to `~/.claude/settings.json`:" (Edit a settings file)
- **[DORA-AI]** Capabilities: Clear and communicated AI stance. DORA (AI Capabilities Model).
  https://dora.dev/capabilities/clear-and-communicated-ai-stance/. Accessed 2026-10-31.
  > "Is it clear which tools are permitted?" (The AI Angle: Psychological safety as an enabler)
  > "which data classification levels are appropriate for which tools" (The AI Angle: Psychological safety as an enabler)
  > "Publish it as a living document in a central, searchable developer hub." (Publish as a “living document”)
- **[GH-AGENT]** Responsible use of Copilot coding agent. GitHub Docs.
  https://docs.github.com/en/copilot/responsible-use/copilot-coding-agent. Accessed 2026-10-31.
  > "You should review all outputs generated by the agent thoroughly prior to merging." (7. Limitations)
  > "The agent does not have access to Actions organization or repository secrets" (Copilot in the cloud)
- **[GH-BP]** Best practices for using GitHub Copilot. GitHub Docs.
  https://docs.github.com/en/copilot/get-started/best-practices. Accessed 2026-10-31.
  > "Understand suggested code before you implement it." (Check Copilot's work)
  > "Use automated tests and tooling to check Copilot's work." (Check Copilot's work)
- **[GH-EXCL]** Content exclusion for GitHub Copilot. GitHub Docs.
  https://docs.github.com/en/copilot/concepts/context/content-exclusion. Accessed 2026-10-31.
  > "You can use content exclusion to configure Copilot to ignore certain files." (About content exclusion for Copilot)
  > "Content exclusion is a guardrail for the tools that GitHub controls." (Limitations of content exclusion)
- **[GH-INSTR]** Adding repository custom instructions for GitHub Copilot. GitHub Docs.
  https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions. Accessed
  2026-10-31.
  > "These are specified in a `copilot-instructions.md` file in the `.github` directory of the repository." (Creating custom instructions)
  > "You can create one or more `AGENTS.md` files, stored anywhere within the repository." (Creating custom instructions)
- **[OWASP-LLM01]** LLM01:2025 Prompt Injection. OWASP GenAI Security Project.
  https://genai.owasp.org/llmrisk/llm01-prompt-injection/. Accessed 2026-10-31.
  > "Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files." (Indirect Prompt Injections)
  > "Separate and clearly denote untrusted content to limit its influence on user prompts." (6. Segregate and identify external content)
- **[OWASP-LLM02]** LLM02:2025 Sensitive Information Disclosure. OWASP Top 10 for LLM Applications 2025, OWASP GenAI
  Security Project. https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/. Accessed 2026-10-31.
  > "Provide guidance on avoiding the input of sensitive information." (1. Educate Users on Safe LLM Usage)
  > "such restrictions may not always be honored and could be bypassed via prompt injection or other methods." (introduction)
- **[OWASP-LLM06]** LLM06:2025 Excessive Agency. OWASP GenAI Security Project.
  https://genai.owasp.org/llmrisk/llm062025-excessive-agency/. Accessed 2026-10-31.
  > "Limit the extensions that LLM agents are allowed to call to only the minimum necessary." (1. Minimize extensions)
  > "Utilise human-in-the-loop control to require a human to approve high-impact actions before they are taken." (6. Require user approval)
- **[OWASP-LLM09]** LLM09:2025 Misinformation. OWASP GenAI Security Project.
  https://genai.owasp.org/llmrisk/llm092025-misinformation/. Accessed 2026-10-31.
  > "Attackers experiment with popular coding assistants to find commonly hallucinated package names." (Scenario #1)
  > "Establish secure coding practices to prevent the integration of vulnerabilities due to incorrect code suggestions." (6. Secure Coding Practices)
