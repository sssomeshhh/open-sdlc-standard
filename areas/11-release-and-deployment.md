# 11. Release and deployment

- **ID prefix:** REL
- **Status:** draft, 2026-10-31

## Purpose

This area protects against risky, manual and irreversible releases: deployments that differ per environment, what reaches
production not being what was tested, releases nobody can identify or undo, and schema changes that block a rollback. It
matters because Google's SRE book reports that roughly 70% of outages are due to changes in a live system ([SRE-INTRO]),
so the way changes reach production is where reliability is won or lost.

## Scope

Covers: the continuous delivery (CD) pipeline, build-once-promote, release identifiers and versioning, changelog and
release notes, release authorisation, rollback, rollout strategy, zero-downtime deploys, post-deploy checks, database
migrations and feature flags.

Leaves to other areas:
- Building artifacts, SBOM, pinning, provenance and the artifact registry: see Area 9.
- The pre-production environment and runtime configuration: see Area 10.
- Error budgets and whether they gate releases; incident handling after a bad release: see Area 12.
- Delivery metrics (DORA): see Area 18. Change management and formal change boards: see Area 18.
- Communicating releases to users, training and support: see Area 20.
- UAT sign-off before release: see Area 1. Test types run before release: see Area 4.
- What each release contains (issue or PR IDs): see TRC-6. Deploy records mapping environment to release: REL-4; showing the running version in each environment: see TRC-7
  (Area 17).
- Major versions for breaking API changes: see ARC-7 (Area 2).

## Requirements

### REL-1 · MUST · Automated deployment pipeline
Deployment to every environment, including production, MUST be automated through one pipeline that uses the same process
everywhere, so a deployment is a single action by an authorised person or the pipeline, not a sequence of manual steps.
- **Gate:** G2
- **Evidence:** deploy pipeline definition in version control; deploy logs for each environment produced by that pipeline;
  the release procedure contains no manual server or console steps.
- **Basis:** [DORA-DA], [AWS-REL08-05], [AWS-OPS05-04].

### REL-2 · MUST · Build once, promote the same artifact
Each environment MUST receive the same artifact, pulled from the artifact registry by its immutable identifier, rather than
a rebuild per environment.
- **Gate:** G2
- **Evidence:** deploy logs show one artifact digest moving through environments; no build step inside the deploy job.
- **Basis:** [DORA-DA].

### REL-3 · SHOULD · Deployable main branch, small releases
The main branch SHOULD be kept in a deployable state so the team can release on demand, in small batches.
- **Gate:** G2
- **Evidence:** CI status history of the main branch; release frequency and the number of changes per release.
- **Basis:** [DORA-CD], [AWS-OPS06-01].

### REL-4 · MUST · Unique, immutable, traceable releases
Every release MUST have a unique identifier, never be modified after it is created (any change is a new release), be
traceable to the commit it was built from, and have each deployment recorded with the environment and time.
- **Gate:** G2 · **Trigger:** each release and each deployment
- **Evidence:** a tag and an artifact digest per release; each tag resolves to the commit the release was built from; no
  re-pushed tags; a deploy log mapping environment → release → time for every deployment.
- **Basis:** [12F-5], [SEMVER]. Deployment record: author's judgement (no primary source states it directly).

### REL-5 · SHOULD · Semantic Versioning for public interfaces
Components with a public API or consumers outside the team (libraries, external APIs) SHOULD declare that API and number
their releases with Semantic Versioning; other applications can use any scheme that meets REL-4. Major versions for
breaking API changes: ARC-7.
- **Gate:** G2 · **Condition:** when a component gains a public API or consumers outside the team · **Trigger:** each release of the component
- **Evidence:** a declared public API; release versions in MAJOR.MINOR.PATCH form.
- **Basis:** [SEMVER]. Condition: author's judgement.

### REL-6 · SHOULD · Changelog per release
A human-readable changelog or release notes SHOULD be maintained per version: newest first, dated, grouped by type of change,
with an "Unreleased" section, and curated rather than copied from commit messages. What each release records (issue or
PR IDs): TRC-6.
- **Gate:** G2 · **Trigger:** each release
- **Evidence:** a CHANGELOG file or release pages with a dated entry for each release, newest first.
- **Basis:** [KACL].

### REL-7 · MUST · Release authorisation defined and recorded
Who is allowed to approve and perform a production deployment MUST be defined in writing, enforced by access control, and
recorded for each deployment.
- **Gate:** G3 · **Trigger:** each production deployment
- **Evidence:** protected deployment environment or required approvers in the pipeline; an audit log of who deployed
  which release, when.
- **Basis:** [SRE-RE]. The approval model (for example whether a second person has to approve): author's judgement (no
  neutral primary source found).

### REL-8 · MUST · Rollback path, exercised
The deployment mechanism MUST have a documented rollback path, exercised at least once and after any change to it; the
previous artifact remains available (BLD-12).
- **Gate:** G2 · **Trigger:** after any change to the deployment mechanism
- **Evidence:** rollback procedure in the runbooks; a dated record of a rollback exercise; previous artifacts retained
  (see BLD-12).
- **Basis:** [AWS-OPS06-01], [12F-5], [DORA-VC], [FOWLER-BG]. Exercise frequency: author's judgement.

### REL-9 · SHOULD · Safe rollout strategy with health checks
Production deploys SHOULD use a safe rollout strategy (rolling, blue-green or canary) gated by automated health checks that
stop a bad release before it replaces all healthy instances, rather than replacing everything at once.
- **Gate:** G3 · **Trigger:** each production deployment
- **Evidence:** deployment configuration (minimum healthy percentage, health-check path, failure detection); bake-time or
  canary settings.
- **Basis:** [AWS-OPS06-03], [AWS-REL08-05], [SREW-CANARY], [SRE-INTRO], [FOWLER-BG].

### REL-10 · MAY · Automatic rollback on monitored criteria
The project MAY have monitoring evaluate each release against defined success criteria and roll it back automatically on failure.
- **Gate:** G3 · **Condition:** when deployment frequency or user count exceeds the threshold the project set · **Trigger:** each release
- **Evidence:** release success criteria (error rate, latency) configured in the pipeline; records of automatic rollbacks.
- **Basis:** [AWS-OPS06-04]. Condition and Trigger: author's judgement.

### REL-11 · SHOULD · Zero-downtime deploys
Deploys SHOULD cause no user-visible downtime: processes start quickly and shut down gracefully (stop accepting new work,
finish in-flight requests and jobs, then exit) so instances can be replaced safely.
- **Gate:** G3
- **Evidence:** termination-signal handling in the code; connection draining or deregistration delay configured;
  monitoring shows no error spike during deploys.
- **Basis:** [12F-9].

### REL-12 · SHOULD · Post-deploy smoke test
Each deployment SHOULD be followed by an automated smoke test in that environment that checks the system is functioning and
its external services are reachable.
- **Gate:** G2 · **Trigger:** each deployment
- **Evidence:** smoke-test step in the pipeline after deploy; its results per deployment.
- **Basis:** [DORA-DA], [AWS-OPS06-02].

### REL-13 · MUST · Versioned database migrations
Database schema changes MUST be versioned migration scripts in version control, applied by a tool that records which
migrations each database has run, through the same pipeline as the application.
- **Gate:** G2
- **Evidence:** a migrations directory; a migration-history table in each database; a pipeline step that runs migrations.
- **Basis:** [DORA-DB], [12F-12].

### REL-14 · SHOULD · Backward-compatible schema changes
Schema changes SHOULD be backward compatible with the application version currently running (expand, migrate, then
contract), so the application can be rolled back without a database rollback; destructive changes are split across
releases.
- **Gate:** G3 · **Trigger:** each schema change
- **Evidence:** migration review checklist; examples of add-then-remove changes spread across releases.
- **Basis:** [DORA-DB].

### REL-15 · SHOULD · Review of high-impact migrations
Migrations with production impact (expected lock or run time above a threshold the project sets, or data rewrites) SHOULD
be reviewed by whoever operates the production database and rehearsed on production-sized data before release.
- **Gate:** G3 · **Trigger:** each migration with production impact
- **Evidence:** the threshold in the migration review checklist; review record on the migration change; rehearsal timing.
- **Basis:** Author's judgement (no primary source found).

### REL-16 · MAY · Feature flags with owner and expiry
Teams MAY use feature flags to separate deployment from release; each flag then has an owner and an expiry date and is
removed once no longer needed.
- **Gate:** G2 · **Trigger:** each new feature flag
- **Evidence:** a flag inventory with owner and expiry; changes that removed expired flags.
- **Basis:** [FOWLER-FT]. Owner and expiry date per flag: author's judgement (the source asks for a small flag inventory
  and removal of flags no longer needed).

## Failure modes

- Manual, multi-step deployments that differ per environment, so the production deploy is the first time the procedure
  runs ([DORA-DA]).
- Rebuilding per environment, so what reaches production is not what was tested ([DORA-DA]).
- All-at-once deploys with no bake time, so a defect reaches every user at once ([AWS-OPS06-03], [AWS-REL08-05]).
- A rollback plan that was never exercised, or that is blocked by a destructive migration already applied
  ([AWS-OPS06-01], [DORA-DB]).
- Changelogs generated from raw commit logs, too noisy for readers ([KACL]).
- Feature flags that are never removed and become permanent configuration ([FOWLER-FT]).

## References

- **[12F-5]** Adam Wiggins, The Twelve-Factor App, V. Build, release, run. https://12factor.net/build-release-run. Accessed 2026-10-31.
  > "Every release should always have a unique release ID, such as a timestamp of the release (such as 2011-04-06-20:32:17) or an incrementing number (such as v100)." (Strictly separate build and run stages)
  > "Releases are an append-only ledger and a release cannot be mutated once it is created." (Strictly separate build and run stages)
- **[12F-9]** Adam Wiggins, The Twelve-Factor App, IX. Disposability. https://12factor.net/disposability. Accessed 2026-10-31.
  > "For a web process, graceful shutdown is achieved by ceasing to listen on the service port (thereby refusing any new requests), allowing any current requests to finish, and then exiting."
- **[12F-12]** Adam Wiggins, The Twelve-Factor App, XII. Admin processes. https://12factor.net/admin-processes. Accessed 2026-10-31. The first quote is an item in the page's list of one-off
  administrative tasks.
  > "Running database migrations (e.g. `manage.py migrate` in Django, `rake db:migrate` in Rails)." (Run admin/management tasks as one-off processes)
  > "One-off admin processes should be run in an identical environment as the regular long-running processes of the app." (Run admin/management tasks as one-off processes)
  > "Admin code must ship with application code to avoid synchronization issues." (Run admin/management tasks as one-off processes)
- **[AWS-OPS05-04]** OPS05-BP04 Use build and deployment management systems. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_build_mgmt_sys.html. Accessed 2026-10-31.
  > "After compiling your code on your development system, you copy the executable onto your production systems and it fails to start." (Common anti-patterns)
- **[AWS-OPS06-01]** OPS06-BP01 Plan for unsuccessful changes. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_plan_for_unsucessful_changes.html. Accessed 2026-10-31.
  > "You have prepared a detailed recovery plan for your change in the event it is unsuccessful. In addition, you have reduced the size of your release to minimize the potential impact on other workload components."
- **[AWS-OPS06-02]** OPS06-BP02 Test deployments. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_test_val_chg.html. Accessed 2026-10-31.
  > "During production releases, untested deployments cause frequent issues that require troubleshooting and escalation."
- **[AWS-OPS06-03]** OPS06-BP03 Employ safe deployment strategies. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_deploy_mgmt_sys.html. Accessed 2026-10-31.
  > "You deploy an unsuccessful change to all of production all at once. As a result, all customers are impacted simultaneously." (Common anti-patterns)
- **[AWS-OPS06-04]** OPS06-BP04 Automate testing and rollback. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_auto_testing_and_rollback.html. Accessed 2026-10-31.
  > "Your monitoring is able to validate against your success criteria and initiate automatic rollback upon failure."
- **[AWS-REL08-05]** REL08-BP05 Deploy changes with automation. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_automated_changemgmt.html. Accessed 2026-10-31.
  > "You perform manual changes. You skip steps in your automation through manual emergency workflows." (Common anti-patterns)
  > "You perform rapid follow-on deployments without allowing for bake time." (Common anti-patterns)
- **[DORA-CD]** Capabilities: Continuous delivery. DORA. https://dora.dev/capabilities/continuous-delivery/. Accessed 2026-10-31.
  > "Continuous delivery is the ability to release changes of all kinds on demand quickly, safely, and sustainably." (introduction)
  > "Is our software in a deployable state throughout its lifecycle?" (introduction)
- **[DORA-DA]** Capabilities: Deployment automation. DORA. https://dora.dev/capabilities/deployment-automation/. Accessed 2026-10-31.
  > "Use the same deployment process for every environment, including production." (How to implement deployment automation)
  > "Use the same packages for every environment. This rule means that you should keep environment-specific configuration separate from packages." (How to implement deployment automation)
  > "Your deployment process should download the packages from an artifact repository" (introduction)
  > "Perform a deployment test to make sure that any necessary external services are reachable, and that the system is functioning." (introduction)
- **[DORA-DB]** Capabilities: Database change management. DORA. https://dora.dev/capabilities/database-change-management/. Accessed 2026-10-31.
  > "Teams that do well at continuous delivery store their database changes as scripts in version control and manage these changes in the same way they manage production application changes." (introduction)
  > "You then ensure that every database instance has a table that records which migrations have been run against that particular instance." (Treat all database schema changes as migrations)
  > "The application can then write to both old and new columns, lazily migrating the data, and also allowing for application rollback without requiring a database rollback." (Zero-downtime database changes)
- **[DORA-VC]** Capabilities: Version control. DORA. https://dora.dev/capabilities/version-control/. Accessed 2026-10-31.
  > "Storing all artifacts in version control means teams can roll back to a previously verified working state quickly and reliably."
- **[FOWLER-BG]** Martin Fowler, Blue Green Deployment, 1 March 2010. https://martinfowler.com/bliki/BlueGreenDeployment.html. Accessed 2026-10-31.
  > "Blue-green deployment also gives you a rapid way to rollback - if anything goes wrong you switch the router back to your blue environment."
- **[FOWLER-FT]** Pete Hodgson, Feature Toggles (aka Feature Flags). martinfowler.com, 9 October 2017. https://martinfowler.com/articles/feature-toggles.html. Accessed 2026-10-31.
  > "Savvy teams view their Feature Toggles as inventory which comes with a carrying cost, and work to keep that inventory as low as possible." (Managing the carrying cost of Feature Toggles)
  > "In order to keep the number of feature flags manageable a team must be proactive in removing feature flags that are no longer needed." (Managing the carrying cost of Feature Toggles)
- **[KACL]** Olivier Lacan, Keep a Changelog 1.1.0. https://keepachangelog.com/en/1.1.0/. Accessed 2026-10-31.
  > "A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project." (What is a changelog?)
  > "Keep an Unreleased section at the top to track upcoming changes." (How can I reduce the effort required to maintain a changelog?)
  > "Using commit log diffs as changelogs is a bad idea: they're full of noise." (Commit log diffs)
  > "The same types of changes should be grouped." (Guiding Principles)
  > "The latest version comes first." (Guiding Principles)
  > "The release date of each version is displayed." (Guiding Principles)
- **[SEMVER]** Tom Preston-Werner, Semantic Versioning 2.0.0. https://semver.org/. Accessed 2026-10-31.
  > "Once a versioned package has been released, the contents of that version MUST NOT be modified. Any modifications MUST be released as a new version." (Semantic Versioning Specification (SemVer))
  > "Software using Semantic Versioning MUST declare a public API." (Semantic Versioning Specification (SemVer))
- **[SRE-INTRO]** Benjamin Treynor Sloss, Introduction, Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/introduction/. Accessed 2026-10-31.
  > "SRE has found that roughly 70% of outages are due to changes in a live system."
- **[SRE-RE]** Dinah McNutt, Release Engineering, Chapter 8 of Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/release-engineering/. Accessed 2026-10-31.
  > "Several layers of security and access control determine who can perform specific operations when releasing a project."
- **[SREW-CANARY]** Canarying Releases, Chapter 16 of The Site Reliability Workbook. Google / O'Reilly, 2018. https://sre.google/workbook/canarying-releases/. Accessed 2026-10-31.
  > "We define canarying as a partial and time-limited deployment of a change in a service and its evaluation."
