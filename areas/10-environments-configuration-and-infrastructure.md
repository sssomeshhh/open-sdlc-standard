# 10. Environments, configuration and infrastructure

- **ID prefix:** ENV
- **Status:** draft, 2026-10-31

## Purpose

This area protects against environments that nobody can rebuild, test environments that touch production data, settings
and credentials baked into code or images, and local set-ups that only work on one person's machine. It matters because
every release, recovery and new team member depends on being able to recreate an environment from what is written down
and versioned, not from memory.

## Scope

Covers: environment separation and inventory, pre-production and parity, runtime configuration, the secrets store and
rotation mechanism, infrastructure as code and drift, immutable infrastructure, one-off administrative tasks, resource
tagging, and reproducible local development (developer experience).

Leaves to other areas:
- Secrets policy (what counts as a secret, who can see it, rotation frequency): see Area 5. Secrets kept out of code and
  committed configuration: SEC-7. Rotation procedure: SEC-8.
- Secrets inside build artifacts and images: see BLD-13 (Area 9).
- Onboarding path for newcomers: see DOC-13 (Area 16).
- Deployment process, database migrations and rollback: see Area 11.
- Backups, disaster recovery and cost review: see Area 12.
- Logs, metrics and audit-trail mechanics for environment access: see Area 13.
- Personal data in non-production environments and test data: see Area 6.

## Requirements

### ENV-1 · MUST · Production is isolated
Production MUST be separated from every non-production environment by account, project or equivalent isolation, with
distinct credentials and no shared data stores.
- **Gate:** G2
- **Evidence:** account or project map showing a separate production boundary; access roles per environment; no credential
  or connection string valid in both production and non-production.
- **Basis:** [SSDF] (PO.5.1), [AWS-SEC01-01]. "Distinct credentials" and "no shared data stores": author's judgement (the
  cited sources require separation, not these specific means).

### ENV-2 · SHOULD · Environment inventory
The project SHOULD keep a written inventory of its environments, updated with each environment change: purpose, location (account, region, URL), owner,
who has access, and what class of data each holds.
- **Gate:** G2 · **Trigger:** each environment change
- **Evidence:** the inventory document in the repository or documentation system; it matches the environments that
  actually exist and is no older than the most recent environment change.
- **Basis:** Author's judgement (no primary source found).

### ENV-3 · SHOULD · Pre-production environment
At least one pre-production environment SHOULD exist where each release is deployed and checked, using the same artifact
and the same deployment process as production, before it reaches production.
- **Gate:** G3 · **Trigger:** each release
- **Evidence:** environment inventory lists it; pipeline history shows the same artifact digest deployed to pre-production
  and then to production.
- **Basis:** [DORA-DA], [AWS-OPS06-02].

### ENV-4 · SHOULD · Environment parity
Development, pre-production and production SHOULD be kept as similar as practical (same backing-service types and major
versions, same runtime image), with every known difference documented.
- **Gate:** G2
- **Evidence:** a parity table in the documentation; local, pre-production and production definitions reference the same
  engine versions.
- **Basis:** [12F-10], [SP800-190].

### ENV-5 · MUST · Configuration outside code and artifact
Configuration that varies between deploys (endpoints, credentials, per-environment values) MUST be kept out of the source
code and out of the built artifact and supplied at deploy or run time, so the same artifact runs in every environment.
- **Gate:** G2
- **Evidence:** one artifact digest deployed to several environments; configuration read from environment variables or a
  configuration service; no environment names hard-coded in code paths.
- **Basis:** [12F-3], [DORA-DA].

### ENV-6 · MUST · Secrets held in a secrets store
Secrets used at deploy or run time MUST be held in a secrets store or an equivalent encrypted, access-controlled mechanism.
Note: keeping secrets out of code and committed configuration is SEC-7; out of artifacts and images, BLD-13.
- **Gate:** G2
- **Evidence:** deploy configuration references secrets by name from the store; store access policy lists who and what can
  read each secret; encryption at rest enabled on the store.
- **Basis:** [AWS-SEC02-03].

### ENV-7 · SHOULD · Secrets can be rotated
Every secret SHOULD be rotatable without a code change or rebuild. Rotation procedure: SEC-8.
- **Gate:** G2
- **Evidence:** a rotation record per secret type showing that the rotation needed only a store update and a restart or
  redeploy.
- **Basis:** [AWS-SEC02-03].

### ENV-8 · MUST · Infrastructure as code
Infrastructure and environment configuration MUST be defined as code in version control, so that any environment can be
recreated from the repository.
- **Gate:** G2
- **Evidence:** infrastructure-as-code files (for example Terraform, CloudFormation or Pulumi) for all long-lived resources;
  a recorded rebuild of an environment from code.
- **Basis:** [DORA-VC], [DORA-DA], [CD-CM], [SSDF] (PS.1.1).

### ENV-9 · SHOULD · Infrastructure changes through review and pipeline
Infrastructure and configuration changes SHOULD go through the same review and pipeline as application changes; manual
changes in production are exceptional, recorded, and reconciled back into code, with drift checked at an interval the
project sets.
- **Gate:** G2
- **Evidence:** infrastructure plan and apply steps in CI; the documented drift-check interval and drift-detection reports
  within it; a log of emergency manual changes and the commits that reconciled them.
- **Basis:** [AWS-OPS05-03], [AWS-REL08-05], [AWS-REL13-04].

### ENV-10 · SHOULD · Configuration validated at start-up
The application SHOULD validate its configuration (required keys, types, allowed values) at start-up and refuse to start
with a clear error when it is invalid.
- **Gate:** G2
- **Evidence:** start-up validation code; a test that starts the application with a missing or invalid value and expects
  failure.
- **Basis:** Author's judgement (no primary source found; nearest is [AWS-OPS05-03]).

### ENV-11 · SHOULD · Immutable infrastructure
Running infrastructure SHOULD be changed by replacing instances or containers with new ones, not by editing them in place.
- **Gate:** G2
- **Evidence:** deploys create new instance, task or container revisions; runbooks contain no in-place edits on servers.
- **Basis:** [AWS-REL08-04].

### ENV-12 · MUST · Documented local set-up
A new developer MUST be able to set up a working local environment from the repository's documented steps alone, with all
dependencies declared and no reliance on unstated system-wide tools. The wider onboarding path: DOC-13.
- **Gate:** G1
- **Evidence:** a "getting started" section that the most recent newcomer (once there is one) followed without outside help; a record of the
  date and any fixes made.
- **Basis:** [12F-2].

### ENV-13 · SHOULD · Scripted, containerised local environment
The local environment SHOULD be scripted or containerised (for example a compose file or a dev container) so that it
starts with a single documented command. Parity of backing services with production: ENV-4.
- **Gate:** G1
- **Evidence:** compose or dev-container definition in the repository; a single documented bootstrap command.
- **Basis:** [DEVCON], [SP800-190].

### ENV-14 · SHOULD · One-off admin tasks from shipped code
One-off administrative tasks (data fixes, maintenance scripts, consoles) SHOULD run from code shipped with the application
release, in the same environment and configuration as the running application.
- **Gate:** G2
- **Evidence:** admin scripts in the repository and in the artifact; run records naming the release used.
- **Basis:** [12F-12].

### ENV-15 · SHOULD · Resources tagged
Every cloud resource SHOULD carry consistent tags or labels for owner, environment and purpose, so cost, access and clean-up
can be attributed.
- **Gate:** G2
- **Evidence:** written tagging policy; tag-compliance report with no untagged long-lived resources.
- **Basis:** [AWS-COST03-02].

### ENV-16 · MAY · Backing-service swap demonstrated
A project MAY demonstrate that a backing service (database, queue, cache, external API) can be swapped, for example for a
restored database, by changing only its configuration handle (URL and credentials), without a code change.
- **Gate:** G2
- **Evidence:** a recorded swap (for example during a restore test) whose change touched configuration only.
- **Basis:** [12F-4].

## Failure modes

- A "staging" environment that shares the production database, account or credentials, so tests touch real data
  ([SSDF] PO.5.1; the example is author's judgement).
- Configuration committed to the repository or baked into the image at build time, so a credential change needs a rebuild
  and the code could not be published without exposing credentials ([12F-3]).
- Infrastructure created by hand in a console; nobody can rebuild it, and recovery depends on memory ([DORA-VC], [CD-CM]).
- Configuration drift between environments, or between the primary and recovery sites ([AWS-REL13-04]).
- A local set-up that works only on the original developer's machine ([SP800-190]).
- Different backing services in development and production (for example an embedded database locally and a server
  database in production) hiding defects until release ([12F-10]).

## References

- **[12F-2]** Adam Wiggins, The Twelve-Factor App, II. Dependencies. https://12factor.net/dependencies. Accessed 2026-10-31.
  > "A twelve-factor app never relies on implicit existence of system-wide packages. It declares all dependencies, completely and exactly, via a dependency declaration manifest." (Explicitly declare and isolate dependencies)
  > "The new developer can check out the app’s codebase onto their development machine, requiring only the language runtime and dependency manager installed as prerequisites." (Explicitly declare and isolate dependencies)
- **[12F-3]** Adam Wiggins, The Twelve-Factor App, III. Config. https://12factor.net/config. Accessed 2026-10-31.
  > "An app’s config is everything that is likely to vary between deploys (staging, production, developer environments, etc)." (Store config in the environment)
  > "A litmus test for whether an app has all config correctly factored out of the code is whether the codebase could be made open source at any moment, without compromising any credentials." (Store config in the environment)
- **[12F-4]** Adam Wiggins, The Twelve-Factor App, IV. Backing services. https://12factor.net/backing-services. Accessed 2026-10-31.
  > "In both cases, only the resource handle in the config needs to change."
- **[12F-10]** Adam Wiggins, The Twelve-Factor App, X. Dev/prod parity. https://12factor.net/dev-prod-parity. Accessed 2026-10-31.
  > "Keep development, staging, and production as similar as possible" (Keep development, staging, and production as similar as possible)
  > "The tools gap: Developers may be using a stack like Nginx, SQLite, and OS X, while the production deploy uses Apache, MySQL, and Linux." (Keep development, staging, and production as similar as possible)
- **[12F-12]** Adam Wiggins, The Twelve-Factor App, XII. Admin processes. https://12factor.net/admin-processes. Accessed 2026-10-31.
  > "One-off admin processes should be run in an identical environment as the regular long-running processes of the app." (Run admin/management tasks as one-off processes)
  > "Admin code must ship with application code to avoid synchronization issues." (Run admin/management tasks as one-off processes)
- **[AWS-COST03-02]** COST03-BP02 Add organization information to cost and usage. AWS Well-Architected Framework, Cost Optimization Pillar. https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_org_information.html. Accessed 2026-10-31.
  > "Implement consistent tagging across all resources where possible by purpose, team, environment, or other criteria relevant to your business."
- **[AWS-OPS05-03]** OPS05-BP03 Use configuration management systems. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_conf_mgmt_sys.html. Accessed 2026-10-31.
  > "You configure, validate, and deploy as part of your continuous integration, continuous delivery (CI/CD) pipeline. You monitor to validate configurations are correct."
- **[AWS-OPS06-02]** OPS06-BP02 Test deployments. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_test_val_chg.html. Accessed 2026-10-31.
  > "During production releases, untested deployments cause frequent issues that require troubleshooting and escalation."
- **[AWS-REL08-04]** REL08-BP04 Deploy using immutable infrastructure. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_immutable_infrastructure.html. Accessed 2026-10-31.
  > "With immutable infrastructure, no in-place modifications are allowed to run infrastructure resources within a workload."
- **[AWS-REL08-05]** REL08-BP05 Deploy changes with automation. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_automated_changemgmt.html. Accessed 2026-10-31.
  > "You perform manual changes. You skip steps in your automation through manual emergency workflows." (Common anti-patterns)
- **[AWS-REL13-04]** REL13-BP04 Manage configuration drift at the DR site or Region. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_config_drift.html. Accessed 2026-10-31.
  > "You fail to update recovery locations when changes are made to the primary locations, which results in outdated configurations that could hinder recovery efforts."
- **[AWS-SEC01-01]** SEC01-BP01 Separate workloads using accounts. AWS Well-Architected Framework, Security Pillar. https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_multi_accounts.html. Accessed 2026-10-31.
  > "An account structure that isolates cloud operations, unrelated workloads, and environments into separate accounts, increasing security across the cloud infrastructure."
- **[AWS-SEC02-03]** SEC02-BP03 Store and use secrets securely. AWS Well-Architected Framework, Security Pillar. https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_identities_secrets.html. Accessed 2026-10-31.
  > "Not rotating credentials. Storing long-term credentials in source code or configuration files. Storing credentials at rest unencrypted." (Common anti-patterns)
- **[CD-CM]** Jez Humble, Configuration Management. continuousdelivery.com. https://continuousdelivery.com/foundations/configuration-management/. Accessed 2026-10-31.
  > "we need to version control everything required to perform these processes, including source code, test and deployment scripts, infrastructure and application configuration information, and the many libraries and packages we depend upon."
- **[DEVCON]** Development Containers (Development Container Specification). https://containers.dev/. Accessed 2026-10-31.
  > "A development container (or dev container for short) allows you to use a container as a full-featured development environment."
- **[DORA-DA]** Capabilities: Deployment automation. DORA. https://dora.dev/capabilities/deployment-automation/. Accessed 2026-10-31.
  > "Use the same packages for every environment. This rule means that you should keep environment-specific configuration separate from packages." (How to implement deployment automation)
  > "Make it possible to recreate the state of any environment from information stored in version control." (How to implement deployment automation)
  > "Use the same deployment process for every environment, including production." (How to implement deployment automation)
- **[DORA-VC]** Capabilities: Version control. DORA. https://dora.dev/capabilities/version-control/. Accessed 2026-10-31.
  > "teams need to use version control for source code, test and deployment scripts, infrastructure and application configuration information, and the many libraries and packages they depend upon." (introduction)
  > "Teams must be able to provision any environment in a fully automated fashion, and know that any new environment reproduced from the same configuration is identical." (introduction)
- **[SP800-190]** NIST SP 800-190, Application Container Security Guide. NIST, September 2017. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf. Accessed 2026-10-31.
  > "This solves the “works on my machine” problem since the developer, build system, and production all run the same immutable artifact." (2.4)
  > "Secrets should be stored outside of images and provided dynamically at runtime as needed." (4.1.4)
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST, February 2022. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf. Accessed 2026-10-31.
  > "Separate and protect each environment involved in software development." (PO.5.1)
  > "Store all forms of code – including source code, executable code, and configuration-as-code – based on the principle of least privilege" (PS.1.1)
