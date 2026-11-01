# 7. Source control and repository hygiene

- **ID prefix:** SCM
- **Status:** draft, 2026-10-31

## Purpose

This area makes the repository the single, trustworthy record of the system: complete enough to build from, protected
against unreviewed or destructive changes, and free of anything that does not belong in it. Without it, changes reach
the main branch unreviewed, history is lost to force-pushes, and the repository fills with build outputs, data exports
and stray files that slow everyone down and leak information.

## Scope

Covers what goes into version control, repository access, the branching and pull-request workflow, branch protection,
required reviews, CODEOWNERS, pull-request and issue templates, contribution rules, ignore and attribute files, a lean
repository, history rewriting and commit signing.

Left to other areas:

- Code review guidelines (what reviewers check): see Area 3. Dead-code detection: see Area 3.
- Secrets in repositories and secret scanning: see Area 5. Personal data in repositories: see Area 6 (PRV-9).
- CI checks required before merge: see Area 8.
- Dependency pinning and artifact registries: see Area 9. Versioning, tags and release branches: see Area 11.

## Requirements

### SCM-1 · MUST · Everything needed to build is versioned, nothing built is

Everything needed to build, test and deploy the system (source, schema migrations, build and pipeline definitions,
infrastructure configuration) MUST be in version control.

- **Gate:** G1
- **Evidence:** a fresh clone builds and tests with the documented commands.
- **Basis:** [FOWLER-CI].
- **Note:** build outputs stay out of version control through the ignore rules (SCM-10).

### SCM-2 · MUST · Least-privilege repository access

Repository access MUST follow least privilege, with membership reviewed at least yearly and whenever someone leaves the
team.

- **Gate:** G1 · **Trigger:** each person leaving the team
- **Evidence:** the collaborator and team list with roles; a dated record of the latest access review.
- **Basis:** [SSDF]. Review frequency: author's judgement (no primary source found).

### SCM-3 · MUST · Main branch changed only through pull requests

The main branch MUST change only through merged pull requests, never by direct push.

- **Gate:** G1
- **Evidence:** branch protection or ruleset requiring a pull request; every commit on main belongs to a merged pull
  request.
- **Basis:** [GH-PROTECTED], [GH-FLOW].

### SCM-4 · SHOULD · Short-lived branches, deleted after merge

Work branches SHOULD be deleted after merge and stay within a project-set maximum age and number of active branches
(DORA suggests three or fewer active branches).

- **Gate:** G1
- **Evidence:** the limits recorded in the contribution rules (SCM-9); branch list with last-commit dates within them;
  automatic branch deletion after merge enabled.
- **Basis:** [GH-FLOW], [DORA-TBD].

### SCM-5 · MUST · Protected main branch without bypass

The main branch (and any release branch) MUST be protected against force-push and deletion, with no bypass for
administrators.

- **Gate:** G1
- **Evidence:** exported branch protection or ruleset settings showing force-push and deletion blocked and
  administrator bypass disabled.
- **Basis:** [GH-PROTECTED], [GH-RULESETS].

### SCM-6 · MUST · Independent approving review, re-approved after changes

Every pull request to a protected branch MUST be merged only with an approving review from someone other than the
author, given after the last change to the diff.

- **Gate:** G1
- **Evidence:** ruleset with at least one required approval and stale-review dismissal (or "approval by someone other
  than the last pusher"); a sample of merged pull requests.
- **Basis:** [GH-PROTECTED]. What reviewers check: see Area 3.

### SCM-7 · SHOULD · Code owners for sensitive paths

The repository SHOULD have a CODEOWNERS file, with code-owner review required for sensitive paths (authentication,
permissions, CI configuration, infrastructure, migrations).

- **Gate:** G1
- **Evidence:** a `CODEOWNERS` file (for example in `.github/`, the root or `docs/`); "require review from code owners"
  (or equivalent) enabled.
- **Basis:** [GH-CODEOWNERS], [GH-PROTECTED].

### SCM-8 · SHOULD · Pull-request and issue templates

The repository SHOULD provide a pull-request template (summary, linked issue, test evidence, risk and rollback,
security and privacy checklist) and issue templates or forms.

- **Gate:** G1
- **Evidence:** `.github/pull_request_template.md` and `.github/ISSUE_TEMPLATE/` (or equivalent); sampled pull requests
  have the template filled in.
- **Basis:** [GH-TEMPLATES], [GH-PRTEMPLATE], [GH-ISSUEFORMS]. The template's contents: author's judgement.

### SCM-9 · SHOULD · Written contribution rules

Contribution rules (branch naming, commit messages, review expectations, how to run checks locally) SHOULD be written
down, for example in `CONTRIBUTING.md`.

- **Gate:** G1
- **Evidence:** a `CONTRIBUTING.md` or equivalent linked from the README, whose check commands match those the CI
  pipeline runs.
- **Basis:** [GH-CONTRIB], [GH-FLOW].

### SCM-10 · MUST · Committed ignore rules, applied to tracked files

Build outputs, installed dependencies, local environment files (such as `.env`), editor files, logs and data exports
MUST be kept out of the repository by a committed `.gitignore` that no tracked file matches.

- **Gate:** G1
- **Evidence:** `.gitignore` in the repository; `git ls-files -ci --exclude-standard` returns nothing.
- **Basis:** [GIT-IGNORE], [GH-IGNORE].

### SCM-11 · SHOULD · Nothing tracked that should not be

The repository SHOULD contain only files the project needs: no generated artefacts, scratch files, local notes, office
documents or data dumps that are not part of the product or its documentation.

- **Gate:** G1
- **Evidence:** a review of `git ls-files` (at least before each release) with every top-level path accounted for in
  the README or documentation; no unexplained files.
- **Basis:** [FOWLER-CI]. Review before each release: author's judgement. Secrets: see SEC-7. Personal data: see PRV-9.

### SCM-12 · SHOULD · No large binaries in Git

Binary files above a project-set size (for example 50 MB) SHOULD be kept in Git LFS or an artifact store instead of
being committed to Git.

- **Gate:** G1
- **Evidence:** the size limit recorded in the contribution rules; a largest-blob report with no blob above it outside
  LFS; repository size under 1 GB.
- **Basis:** [GH-LARGE]. GitHub warns at 50 MiB and blocks files over 100 MiB; the 50 MB example: author's judgement
  based on that warning.

### SCM-13 · SHOULD · Line endings normalised

Line endings and text attributes SHOULD be normalised through a committed `.gitattributes`, so that edits on different
platforms do not rewrite whole files.

- **Gate:** G1
- **Evidence:** `.gitattributes` with `* text=auto` or explicit rules; no whole-file line-ending churn in recent diffs.
- **Basis:** [GIT-ATTR].

### SCM-14 · MUST · Shared history not rewritten

History that others might have based work on (shared and protected branches) MUST NOT be rewritten, except to remove
leaked data under a documented procedure.

- **Gate:** G1 · **Trigger:** each history rewrite to remove leaked data
- **Evidence:** force-push disabled on protected branches (SCM-5); a record for each rewrite, with its reason and the
  steps taken.
- **Basis:** [PROGIT], [GH-PROTECTED], [GH-SENSITIVE].

### SCM-15 · SHOULD · Conversations resolved before merge

All review conversations on a pull request SHOULD be resolved before it is merged.

- **Gate:** G1
- **Evidence:** the ruleset setting requiring conversation resolution; sampled pull requests.
- **Basis:** [GH-PROTECTED].

### SCM-16 · MAY · Signed commits

Protected branches MAY require signed commits.

- **Gate:** G1
- **Evidence:** "require signed commits" enabled; commits shown as verified.
- **Basis:** [GH-PROTECTED], [GH-SIGN], [SSDF].

## Failure modes

- Branch protection exists but administrators can bypass it, so required review is optional in practice.
  [GH-PROTECTED]
- `.gitignore` added after the files were committed; Git keeps tracking them. [GIT-IGNORE]
- Stray exports and scratch files accumulate in the working tree and get committed. Author's judgement.
- Long-lived feature branches and many active branches cause painful merges. [DORA-TBD]
- Force-pushing or rebasing shared branches, losing others' work. [PROGIT]
- An approved pull request changed after approval without re-review. [GH-PROTECTED]

## References

- **[DORA-TBD]** Capabilities: Trunk-based development. DORA (Google Cloud).
  https://dora.dev/capabilities/trunk-based-development/ . Accessed 2026-10-31.
  > "Have three or fewer active branches in the application’s code repository."
- **[FOWLER-CI]** Continuous Integration. Martin Fowler, martinfowler.com, revised 18 January 2024.
  https://martinfowler.com/articles/continuousIntegration.html . Accessed 2026-10-31.
  > "In general we should store in source control everything we need to build anything, but nothing that we actually build."
- **[GH-CODEOWNERS]** About code owners. GitHub Docs.
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners .
  Accessed 2026-10-31.
  > "Code owners are automatically requested for review when someone opens a pull request that modifies code that they own." (introduction)

  > "create a new file called CODEOWNERS in the .github/ , root, or docs/ directory of the repository" (CODEOWNERS file location)
- **[GH-CONTRIB]** Setting guidelines for repository contributors. GitHub Docs.
  https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors .
  Accessed 2026-10-31.
  > "For the repository owner, contribution guidelines are a way to communicate how people should contribute."
- **[GH-FLOW]** GitHub flow. GitHub Docs. https://docs.github.com/en/get-started/using-github/github-flow . Accessed
  2026-10-31.
  > "A short, descriptive branch name enables your collaborators to see ongoing work at a glance." (Create a branch)

  > "After you merge your pull request, delete your branch." (Delete your branch)
- **[GH-IGNORE]** Ignoring files. GitHub Docs. https://docs.github.com/en/get-started/git-basics/ignoring-files .
  Accessed 2026-10-31.
  > "To share the ignore rules with other users who clone the repository, commit the .gitignore file into your repository."
- **[GH-ISSUEFORMS]** Configuring issue templates for your repository. GitHub Docs.
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository .
  Accessed 2026-10-31.
  > "You can encourage contributors to include specific, structured information by using issue forms in your repository."
- **[GH-LARGE]** About large files on GitHub. GitHub Docs.
  https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github .
  Accessed 2026-10-31.
  > "We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended." (Repository size limits)

  > "If you attempt to add or update a file that is larger than 50 MiB, you will receive a warning from Git." (File size limits)

  > "GitHub blocks files larger than 100 MiB." (File size limits)
- **[GH-PROTECTED]** About protected branches. GitHub Docs.
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches .
  Accessed 2026-10-31.
  > "can require that all pull requests receive a specific number of approving reviews before someone merges the pull request into a protected branch." (Require pull request reviews before merging)

  > "By default, the restrictions of a branch protection rule do not apply to people with admin permissions to the repository" (About branch protection rules)

  > "If you are concerned about pull requests being "hijacked" (where unapproved content is added to approved pull requests), it is safer to dismiss stale reviews." (Require pull request reviews before merging)

  > "If you do, any pull request that affects code with a code owner must be approved by that code owner before the pull request can be merged into the protected branch." (Require pull request reviews before merging)

  > "By default, each branch protection rule disables force pushes to the matching branches and prevents the matching branches from being deleted." (About branch protection rules)

  > "Requires all comments on the pull request to be resolved before it can be merged to a protected branch." (Require conversation resolution before merging)

  > "When you enable required commit signing on a branch, contributors and bots can only push commits that have been signed and verified to the branch." (Require signed commits)
- **[GH-PRTEMPLATE]** Creating a pull request template for your repository. GitHub Docs.
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository .
  Accessed 2026-10-31.
  > "To store your file in a hidden directory, name the pull request template .github/pull_request_template.md ."
- **[GH-RULESETS]** About rulesets. GitHub Docs.
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets .
  Accessed 2026-10-31.
  > "A ruleset is a named list of rules that applies to a repository or to multiple repositories in an organization"
- **[GH-SENSITIVE]** Removing sensitive data from a repository. GitHub Docs.
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository .
  Accessed 2026-10-31.
  > "If a fellow developer has a clone from before your rewrite, and after your rewrite simply runs git pull followed by git push , the sensitive data will return."
- **[GH-SIGN]** About commit signature verification. GitHub Docs.
  https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification .
  Accessed 2026-10-31.
  > "These tags or commits are marked as verified on GitHub so other people can be confident that the changes come from a trusted source."
- **[GH-TEMPLATES]** About issue and pull request templates. GitHub Docs.
  https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates .
  Accessed 2026-10-31.
  > "When you add a pull request template to your repository, project contributors will automatically see the template's contents in the pull request body."
- **[GIT-ATTR]** gitattributes documentation. Git project. https://git-scm.com/docs/gitattributes . Accessed
  2026-10-31.
  > "When text=auto conversion is enabled in a cross-platform project using push and pull to a central repository the text files containing CRLFs should be normalized."
- **[GIT-IGNORE]** gitignore documentation. Git project. https://git-scm.com/docs/gitignore . Accessed 2026-10-31.
  > "A gitignore file specifies intentionally untracked files that Git should ignore. Files already tracked by Git are not affected" (DESCRIPTION)

  > "To stop tracking a file that is currently tracked, use git rm --cached to remove the file from the index." (NOTES)
- **[PROGIT]** Pro Git (2nd ed.), §3.6 "Git Branching – Rebasing". Scott Chacon and Ben Straub.
  https://git-scm.com/book/en/v2/Git-Branching-Rebasing . Accessed 2026-10-31.
  > "Do not rebase commits that exist outside your repository and that people may have based work on."
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST, February 2022.
  https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf
  (landing page: https://csrc.nist.gov/pubs/sp/800/218/final). Accessed 2026-10-31.
  > "PS.1.1: Store all forms of code – including source code, executable code, and configuration-as-code – based on the principle of least privilege so that only authorized personnel, tools, services, etc. have access." (PS.1.1)

  > "Use commit signing for code repositories." (PS.1.1)
