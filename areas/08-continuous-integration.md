# 8. Continuous integration

- **ID prefix:** CI
- **Status:** draft, 2026-10-31

## Purpose

This area makes sure every change is built and checked automatically before it reaches the main branch, so defects are
found within minutes of being made, while they are cheap to fix. It also treats the pipeline itself as an attack
surface: a CI system holds credentials and produces what is deployed, so a poorly secured pipeline is a route into
production.

## Scope

Covers the CI pipeline: triggers, build, tests, lint, format and type checks, security checks run as gates, required
status checks, keeping the main branch green, feedback speed, visibility, and the security of the pipeline itself.

Left to other areas:

- Coding guidelines and lint rules themselves: see Area 3. Test types and test strategy: see Area 4.
- Vulnerability, dependency and secret scanning, and why: see Area 5.
- Branch protection and required reviews: see Area 7.
- Reproducible builds, dependency pinning (including pinning third-party pipeline components, BLD-3), SBOM and
  provenance: see Area 9.
- Secrets store and configuration: see Area 10. Continuous delivery and deployment: see Area 11.
- Delivery metrics: see Area 18.

## Requirements

### CI-1 · MUST · Pipeline as code on every change

Every push and every pull request MUST trigger an automated CI pipeline that is defined as code in the repository.

- **Gate:** G1
- **Evidence:** workflow files (for example `.github/workflows/*.yml`) triggered on push and pull request; run history
  shows a run for each recent pull request.
- **Basis:** [FOWLER-CI], [GH-CI], [SSDF].

### CI-2 · MUST · Build and tests; any failure fails the run

The pipeline MUST build the software and run the automated test suite, failing the run if any test fails.

- **Gate:** G1
- **Evidence:** build and test steps in the workflow; a run with a failing test is marked failed.
- **Basis:** [FOWLER-CI], [DORA-CI], [GH-CI].

### CI-3 · MUST · Lint, format and type checks for every component

The pipeline MUST run the lint, format and (where the language has one) type checks for every component in the
repository, not only the tests.

- **Gate:** G1
- **Evidence:** a check step per component; no component lacks one. The rules themselves: see Area 3.
- **Basis:** Naming lint, format and type checks as gates: author's judgement (no primary source
  found; sources speak of automated code analysis [SSDF]).

### CI-4 · MUST · CI results are required checks

The CI checks MUST be required status checks on the protected main branch, so a pull request cannot merge until they
pass.

- **Gate:** G1
- **Evidence:** branch protection or ruleset listing the required checks by name; no merged pull request with failed
  required checks.
- **Basis:** [GH-STATUS], [GH-PROTECTED].

### CI-5 · SHOULD · Security checks as pipeline gates

The pipeline SHOULD run secret detection, static analysis and dependency vulnerability review on every change (and
infrastructure-as-code or container image scanning where relevant), as required checks.

- **Gate:** G1
- **Evidence:** a workflow job for each check; results shown on pull requests; the dependency review check required.
  What each scan covers: see SEC-9 to SEC-12.
- **Basis:** [CS-CICD], [GH-DEPREVIEW], [SSDF].

### CI-6 · MUST · Main kept green

A failure on the main branch MUST be fixed, or the change that caused it reverted, before other work continues.

- **Gate:** G1 · **Trigger:** each failure on the main branch
- **Evidence:** main-branch pass rate and time to restore after each failure, from CI history.
- **Basis:** [FOWLER-CI], [DORA-CI].

### CI-7 · SHOULD · Feedback within about ten minutes

The checks that gate a pull request SHOULD complete in about ten minutes or less.

- **Gate:** G1
- **Evidence:** median and 90th-percentile pipeline duration from CI history.
- **Basis:** [FOWLER-CI], [DORA-CI].

### CI-8 · SHOULD · Integrate at least daily

Developers SHOULD integrate their work into the main branch at least daily, through small pull requests.

- **Gate:** G1
- **Evidence:** pull-request age and size from the repository history; branch age.
- **Basis:** [FOWLER-CI], [DORA-TBD].

### CI-9 · SHOULD · Status visible to the team

CI status SHOULD be visible to the whole team (pull-request checks, notifications to a team channel, or a status
badge).

- **Gate:** G1
- **Evidence:** a notification channel or dashboard receiving CI failures; status shown on pull requests.
- **Basis:** [FOWLER-CI], [DORA-CI].

### CI-10 · MUST · Least-privilege pipeline credentials

Pipelines MUST run with least privilege: read-only default token permissions, secrets available only to the jobs that
need them, and no secret written in plaintext in workflow files.

- **Gate:** G1
- **Evidence:** explicit permission blocks in workflows; the default token permission set to read; the list of
  pipeline secrets and the jobs that use them; no credentials in workflow files.
- **Basis:** [GH-SECUREUSE]. Secrets limited to the jobs that need them: author's judgement (no primary source found).

### CI-11 · MUST · No untrusted code with privileged triggers

Pipelines MUST NOT run untrusted pull-request code under privileged triggers or with access to secrets.

- **Gate:** G1
- **Evidence:** workflow review shows no privileged trigger (for example `pull_request_target`) that checks out or runs
  pull-request code.
- **Basis:** [GH-SECUREUSE]; [OWASP-CICD10] is cited for the risk name only (CICD-SEC-4, a heading).

### CI-12 · SHOULD · Third-party pipeline components kept up to date

Third-party actions and plugins used by the pipeline SHOULD be kept up to date by automation. Pinning them to an
immutable version: see BLD-3.

- **Gate:** G1
- **Evidence:** an automated update tool configured for pipeline components; its update pull requests merged or closed
  with a reason.
- **Basis:** [GH-DEPVER].

### CI-13 · SHOULD · Numbered runs traceable to commits

Each pipeline run SHOULD carry a unique number linked to the commit it built. Clean runs: see CI-16. Reproducible
builds: see Area 9.

- **Gate:** G1
- **Evidence:** run identifiers linked to commit SHAs.
- **Basis:** [DORA-CI].

### CI-14 · SHOULD · Run history kept and attributable

CI logs and run history SHOULD be retained for audit, with each run attributable to the person or event that
triggered it.

- **Gate:** G1
- **Evidence:** the log retention setting; run records naming the trigger and actor.
- **Basis:** [CS-SECRETS]; [OWASP-CICD10] is cited for the risk name only (CICD-SEC-10, a heading). Retention for
  audit: author's judgement.

### CI-15 · MAY · Merge queue on busy branches

A merge queue MAY be used on busy branches so that combinations of individually green pull requests cannot break the
main branch.

- **Gate:** G1
- **Evidence:** merge queue enabled; CI triggered for merge-queue groups.
- **Basis:** [GH-MERGEQ].

### CI-16 · SHOULD · Clean runs from the repository

Each pipeline run SHOULD start in a clean environment and use only the repository and its declared, locked
dependencies.

- **Gate:** G1
- **Evidence:** fresh runners or containers per run; dependencies installed from lockfiles; no state carried over
  from earlier runs other than declared caches.
- **Basis:** Author's judgement (no primary source found; [DORA-CI] asks for builds that are "repeatable").

## Failure modes

- CI exists but is not a required check, or administrators bypass it, so failing code merges anyway. [GH-STATUS],
  [GH-PROTECTED]
- Only one part of a multi-component repository is checked (for example one component is tested, another is
  never type-checked). Author's judgement.
- The main branch stays red for days, and "mostly green" is accepted. [FOWLER-CI]
- Slow pipelines push developers to batch changes and skip checks. [DORA-CI], [FOWLER-CI]
- Over-privileged tokens, unpinned third-party actions (BLD-3) and privileged triggers on untrusted code turn CI into a
  supply-chain entry point. [GH-SECUREUSE], [OWASP-CICD10]

## References

- **[CS-CICD]** CI/CD Security Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html . Accessed 2026-10-31.
  > "Incorporate language appropriate SAST, DAST, IaC vulnerability scanning and related tools into the pipeline."
- **[CS-SECRETS]** Secrets Management Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html . Accessed 2026-10-31.
  > "Additionally, a CI/CD pipeline run should be easily attributable to the one who has defined the job or triggered it to detect who has tried to exfiltrate secrets or manipulate them."
- **[DORA-CI]** Capabilities: Continuous integration. DORA (Google Cloud).
  https://dora.dev/capabilities/continuous-integration/ . Accessed 2026-10-31.
  > "Each commit should trigger a series of automated tests that provide feedback in a few minutes." (How to implement CI)

  > "If the build can’t be fixed in a few minutes, the change that caused the build to break should be identified and reverted." (Common pitfalls)

  > "The tests should not take more than a few minutes to run, with an upper limit of about 10 minutes according to DORA’s research (PDF)." (Common pitfalls)

  > "These builds should be numbered and repeatable." (How to implement CI)

  > "The system should also make the status visible to the team." (How to implement CI)
- **[DORA-TBD]** Capabilities: Trunk-based development. DORA (Google Cloud).
  https://dora.dev/capabilities/trunk-based-development/ . Accessed 2026-10-31.
  > "Merge branches to trunk at least once a day."
- **[FOWLER-CI]** Continuous Integration. Martin Fowler, martinfowler.com, revised 18 January 2024.
  https://martinfowler.com/articles/continuousIntegration.html . Accessed 2026-10-31.
  > "Continuous Integration is a software development practice where each member of a team merges their changes into a codebase together with their colleagues changes at least daily." (introduction)

  > "any test failing is enough to fail the build, 99.9% green is still red." (Make the Build Self-Testing)

  > "Continuous Integration can only work if the mainline is kept in a healthy state." (Fix Broken Builds Immediately)

  > "For most projects, however, the XP guideline of a ten minute build is perfectly within reason." (Keep the Build Fast)

  > "Continuous Integration is all about communication, so we want to ensure that everyone can easily see the state of the system" (Everyone can see what's happening)
- **[GH-CI]** About continuous integration with GitHub Actions. GitHub Docs.
  https://docs.github.com/en/actions/get-started/continuous-integration . Accessed 2026-10-31.
  > "When you commit code to your repository, you can continuously build and test the code to make sure that the commit doesn't introduce errors."
- **[GH-DEPREVIEW]** About dependency review. GitHub Docs.
  https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review . Accessed 2026-10-31.
  > "A failed check blocks a pull request from being merged when the repository owner requires the dependency review check to pass."
- **[GH-DEPVER]** About Dependabot version updates. GitHub Docs.
  https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates . Accessed
  2026-10-31.
  > "Dependabot version updates are automated pull requests that keep your dependencies updated, even when they don’t have any vulnerabilities."
- **[GH-MERGEQ]** Managing a merge queue. GitHub Docs.
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue .
  Accessed 2026-10-31.
  > "A merge queue helps increase velocity by automating pull request merges into a busy branch and ensuring the branch is never broken by incompatible changes."
- **[GH-PROTECTED]** About protected branches. GitHub Docs.
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches .
  Accessed 2026-10-31.
  > "By default, the restrictions of a branch protection rule do not apply to people with admin permissions to the repository"
- **[GH-SECUREUSE]** Secure use reference. GitHub Docs. https://docs.github.com/en/actions/reference/security/secure-use .
  Accessed 2026-10-31.
  > "Therefore, you should ensure that the credentials being used within workflows have the least privileges required." (Use secrets for sensitive information)

  > "It's good security practice to set the default permission for the GITHUB_TOKEN to read access only for repository contents." (Use secrets for sensitive information)

  > "Sensitive data should never be stored as plaintext in workflow files." (Use secrets for sensitive information)

  > "Avoid using the pull_request_target and workflow_run workflow triggers with untrusted pull requests or code content." (Good practices)
- **[GH-STATUS]** About status checks. GitHub Docs. https://docs.github.com/en/pull-requests/reference/status-checks .
  Accessed 2026-10-31.
  > "If status checks are required for a protected branch, they must pass before the pull request can be merged."
- **[OWASP-CICD10]** OWASP Top 10 CI/CD Security Risks. OWASP. https://owasp.org/www-project-top-10-ci-cd-security-risks/ .
  Accessed 2026-10-31.
  > "CICD-SEC-4: Poisoned Pipeline Execution (PPE)" (Top 10 risks)

  > "CICD-SEC-10: Insufficient Logging and Visibility" (Top 10 risks)
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST, February 2022.
  https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf
  (landing page: https://csrc.nist.gov/pubs/sp/800/218/final). Accessed 2026-10-31.
  > "Example 3: Use code-based configuration for toolchains (e.g., pipelines-as-code, toolchains-as-code)." (PO.3.2)

  > "Configure the toolchain to perform automated code analysis and testing on a regular or continuous basis for all supported releases." (RV.1.2)
