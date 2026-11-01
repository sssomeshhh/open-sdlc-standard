# Research C: Areas 9–12

Research notes for the Open SDLC Standard (see `../README.md`). Covers:
Area 9 Build and supply chain; Area 10 Environments, configuration and infrastructure (incl. developer experience);
Area 11 Release and deployment (incl. database migrations); Area 12 Operations and reliability.

- **Date of research and access:** 2026-10-31.
- **Method:** every quote below was taken from a copy of the page or PDF downloaded on 2026-10-31 and checked
  verbatim (whitespace normalised) against that copy. Ellipses are not used inside quotes; each quote is a contiguous
  run of the source text.
- **Levels** are proposals only, using RFC 2119 words. `[judgement]` marks a proposal with no direct primary source.
- **Source keys** are defined in each area's Sources section; a key defined in an earlier area is reused, not repeated.

---

## Area 9: Build and supply chain

### Candidate requirements

1. **MUST** — Every artifact that reaches a shared environment is built by an automated, scripted build that runs the same
   way every time (not by hand on a workstation).
   *Evidence:* build definition in version control (CI workflow, Dockerfile, build script); deploy records show artifacts come
   only from CI runs. *Sources:* SLSA-BT, SLSA-REQ, SRE-RE, AWS-OPS05-04.
2. **MUST** — All direct dependencies are declared in a manifest, and the full resolved set (including transitive) is locked
   (lockfile committed), so a build at the same commit resolves the same versions.
   *Evidence:* manifest + lockfile in the repository; CI installs in "frozen"/locked mode and fails on drift.
   *Sources:* 12F-II, RB, SRE-RE.
3. **SHOULD** — Build-time dependencies that are not covered by a lockfile (base images, CI actions, downloaded tools) are
   pinned to an immutable reference (digest or hash), not a mutable tag or range.
   *Evidence:* Dockerfile `FROM image@sha256:…`; CI actions pinned to commit SHA; OpenSSF Scorecard "Pinned-Dependencies"
   result. *Sources:* SCORECARD.
4. **SHOULD** — Builds are hermetic and aim to be reproducible: the same source, environment and instructions produce the
   same artifact; known sources of non-determinism (timestamps, paths) are controlled.
   *Evidence:* documented build environment; rebuild of a past release compares equal by hash, or a recorded list of the
   known differences. *Sources:* RB, SRE-RE.
5. **MUST** — An automated dependency-update mechanism is enabled and its update proposals are triaged within a defined time.
   *Evidence:* Dependabot/Renovate configuration; age of open update PRs. *Sources:* SCORECARD, SSDF (PW.4.4).
6. **MUST** — Known vulnerabilities in dependencies and in container images are detected automatically in the pipeline, and
   findings above an agreed severity block release or carry a recorded, time-boxed exception.
   *Evidence:* SCA/image-scan step in CI; scan reports per release; exception register (e.g. `osv-scanner.toml` with reasons).
   *Sources:* SSDF (PW.4.4), SCORECARD (Vulnerabilities), SP800-190.
7. **SHOULD** — Third-party components are evaluated before adoption (maintenance, security history, licence, fit for intended
   use) and re-evaluated if their use changes.
   *Evidence:* dependency-approval record or ADR for new significant dependencies. *Sources:* SSDF (PW.4.1).
8. **SHOULD** — A machine-readable SBOM (SPDX or CycloneDX) is generated for every release and kept with the release;
   it covers at least the NTIA minimum data fields.
   *Evidence:* SBOM file attached to each release/image; fields include supplier, component, version, unique identifier,
   dependency relationship, author, timestamp. *Sources:* NTIA, SSDF (PS.3.2), SPDX, CDX, CISA-SBOM, SCORECARD (SBOM).
9. **MUST** — The licences of all shipped dependencies are identified and checked against an organisational allow/deny
   policy; obligations (attribution, source offer) are met.
   *Evidence:* licence report generated in CI; policy file; NOTICE/third-party-licences file in the artifact.
   *Sources:* OPENCHAIN, SPDX.
10. **SHOULD** — Release artifacts carry integrity information (hash and/or signature) and build provenance that identifies
    the source commit, build platform and inputs; consumers (deploy pipeline) verify it.
    *Evidence:* signatures/attestations next to artifacts; deploy step verifies digest/signature. *Sources:* SLSA-BT (Build L1–L2),
    SLSA-REQ, SSDF (PS.2.1), SCORECARD (Signed-Releases).
11. **MAY** — Builds run on a hardened, hosted build platform that isolates runs and keeps signing material out of reach of
    user build steps (SLSA Build L3).
    *Evidence:* SLSA provenance at L3 from the build platform. *Sources:* SLSA-BT.
12. **MUST** — Artifacts are stored in a controlled artifact registry with access control; deployments pull from it; release
    artifacts and their integrity/provenance data are retained per a defined retention policy.
    *Evidence:* registry with restricted write access; retention/lifecycle rules; ability to fetch the exact artifact of any
    supported release. *Sources:* SSDF (PS.3.1), DORA-DA.
13. **MUST NOT** — Generated binaries or build outputs are committed to the source repository (except vetted, documented
    vendored code).
    *Evidence:* repository scan (Scorecard "Binary-Artifacts"); ignore rules. *Sources:* SCORECARD.
14. **MUST NOT** — Secrets are embedded in build artifacts or images; they are supplied at runtime.
    *Evidence:* image/secret scan of artifacts; build args reviewed for credentials. *Sources:* SP800-190, 12F-III.
15. **SHOULD** — Only images from an approved set of base images and registries are allowed to run; stale images are
    rebuilt regularly to pick up patches.
    *Evidence:* base-image policy; admission control or deploy check; rebuild schedule. *Sources:* SP800-190.
16. **SHOULD** — Build tools and CI are themselves kept current, changed under change control, and run with least privilege.
    *Evidence:* CI token permissions; toolchain version pins and update history. *Sources:* SSDF (PW.6.1, PO.3.2), SLSA-REQ.

### Failure modes

- Artifacts built on a developer laptop or by hand in the console, so nobody can say which commit is running
  (SLSA-BT Build L1 targets exactly "building from a commit that is not present in the upstream repo").
- Dependencies declared with open ranges and no lockfile, or a lockfile that CI ignores; a rebuild of the "same" version
  pulls different code (12F-II, RB).
- Base images and CI actions referenced by mutable tags (`latest`, `v3`), so the build changes underneath the project
  (SCORECARD Pinned-Dependencies).
- Dependency-update bot enabled but its PRs never merged; the tool "does not ensure that the tool is run or that the tool's
  pull requests are" merged (SCORECARD).
- Secrets passed as build arguments and baked into image layers (SP800-190 "Embedded clear text secrets").
- No retention rule: either the registry grows without limit, or the artifact of the release in production can no longer be
  fetched for rollback or investigation (SSDF PS.3.1) [judgement on the unlimited-growth half].

### Sources

- **SLSA-BT** — "SLSA • Build: Track Basics", SLSA specification v1.2 (Status: Approved), OpenSSF.
  https://slsa.dev/spec/v1.2/build-track-basics — accessed 2026-10-31. (v1.0 pages now show "Status: Retired".)
  - "Follow a consistent build process so that others can form expectations about what a “correct” build looks like."
  - "With verification, prevents mistakes during the release process, such as building from a commit that is not present in the upstream repo."
  - "prevent secret material used to sign the provenance from being accessible to the user-defined build steps."
- **SLSA-REQ** — "SLSA • Build: Requirements for producing artifacts", SLSA v1.2, OpenSSF.
  https://slsa.dev/spec/v1.2/build-requirements — accessed 2026-10-31.
  - "The build process MUST generate provenance that unambiguously identifies the output package by cryptographic digest and describes how that package was produced."
  - "The producer MUST distribute provenance to artifact consumers."
  - "This includes, but is not limited to, using proper access controls, securing communications, implementing proper management of cryptographic secrets, doing frequent updates, and promptly fixing known vulnerabilities."
- **SSDF** — NIST SP 800-218, "Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the
  Risk of Software Vulnerabilities", NIST, February 2022.
  https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf — accessed 2026-10-31.
  - PS.2.1: "Make software integrity verification information available to software acquirers."
  - PS.3.1: "Securely archive the necessary files and supporting data (e.g., integrity verification information, provenance data) to be retained for each software release."
  - PS.3.2: "Collect, safeguard, maintain, and share provenance data for all components of each software release (e.g., in a software bill of materials [SBOM])."
  - PW.4.1 Example 1: "Review and evaluate third-party software components in the context of their expected use."
  - PW.4.4 Example 2: "Build into the toolchain automatic detection of known vulnerabilities in software components."
  - PW.6.1 Example 2: "Follow change management processes when deploying or updating compiler, interpreter, and build tools, and audit all unexpected changes to tools."
- **NTIA** — "The Minimum Elements For a Software Bill of Materials (SBOM)", U.S. Department of Commerce / NTIA, July 2021.
  https://www.ntia.doc.gov/files/ntia/publications/sbom_minimum_elements_report.pdf — accessed 2026-10-31.
  - "Data formats used to generate and consume SBOMs include SPDX, CycloneDX, and SWID tags."
  - "If the software component is updated with a new build or release, a new SBOM must be created to reflect the new version of the software."
  - Data fields table: "Supplier Name", "Component Name", "Version of the Component", "Other Unique Identifiers", "Dependency Relationship", "Author of SBOM Data", "Timestamp".
- **CISA-SBOM** — "Software Bill of Materials (SBOM)", CISA. https://www.cisa.gov/sbom — accessed 2026-10-31.
  - "An SBOM is a nested inventory, a list of ingredients that make up software components."
- **SPDX** — "Overview", SPDX (Linux Foundation). https://spdx.dev/about/overview/ — accessed 2026-10-31.
  - "SPDX is an open standard for communicating software bill of material information, including provenance, license, security, and other related information."
  - "The SPDX specification is recognized as the international open standard for security, license compliance, and other software supply chain artifacts as ISO/IEC 5962:2021."
- **CDX** — "Specification Overview", CycloneDX (OWASP). https://cyclonedx.org/specification/overview/ — accessed 2026-10-31.
  - "At its core, CycloneDX employs a robust object model capable of capturing components, services, dependencies, and relationships across various inventory types"
- **OPENCHAIN** — "OpenChain ISO/IEC 5230 – License Compliance", OpenChain Project (Linux Foundation).
  https://openchainproject.org/license-compliance — accessed 2026-10-31.
  - "ISO/IEC 5230 defines the key requirements of a quality open source license compliance program"
  - "ISO/IEC 5230 helps organizations manage open source licensing requirements for past, current and future products or services."
- **SCORECARD** — "Check Documentation" (docs/checks.md), OpenSSF Scorecard.
  https://github.com/ossf/scorecard/blob/main/docs/checks.md (raw: https://raw.githubusercontent.com/ossf/scorecard/main/docs/checks.md) — accessed 2026-10-31.
  - Pinned-Dependencies: "A \"pinned dependency\" is a dependency that is explicitly set to a specific hash instead of allowing a mutable version or range of versions." (source uses straight double quotes around the term)
  - Dependency-Update-Tool: "Out-of-date dependencies make a project vulnerable to known flaws and prone to attacks."
  - Binary-Artifacts: "Including generated executables in the source repository increases user risk."
  - Signed-Releases: "Signed releases attest to the provenance of the artifact."
  - SBOM: "An SBOM can give users information about what dependencies your project has which allows them to identify vulnerabilities in the software supply chain."
- **RB** — "Definitions", Reproducible Builds project. https://reproducible-builds.org/docs/definition/ — accessed 2026-10-31.
  - "A build is reproducible if given the same source code, build environment and build instructions, any party can recreate bit-by-bit identical copies of all specified artifacts."
  - "Relevant attributes of the build environment would usually include dependencies and their versions, build configuration flags and environment variables as far as they are used by the build system"
- **SRE-RE** — Dinah McNutt, "Release Engineering", Chapter 8 of *Site Reliability Engineering* (Google, O'Reilly 2016).
  https://sre.google/sre-book/release-engineering/ — accessed 2026-10-31.
  - "Our builds are hermetic, meaning that they are insensitive to the libraries and other software installed on the build machine."
  - "If two people attempt to build the same product at the same revision number in the source code repository on different machines, we expect identical results."
- **SP800-190** — NIST SP 800-190, "Application Container Security Guide", NIST, September 2017.
  https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf — accessed 2026-10-31.
  - "Secrets should be stored outside of images and provided dynamically at runtime as needed."
  - "Organizations should maintain a set of trusted images and registries and ensure that only images from this set are allowed to run in their environment"
  - "organizations can configure their continuous integration processes to allow images to be signed by the authorized personnel and pushed to a registry only after they have passed a vulnerability scan and compliance assessment."
- **AWS-OPS05-04** — "OPS05-BP04 Use build and deployment management systems", AWS Well-Architected Framework, Operational
  Excellence Pillar, Amazon Web Services.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_build_mgmt_sys.html — accessed 2026-10-31.
  - Anti-pattern: "After compiling your code on your development system, you copy the executable onto your production systems and it fails to start."

---

## Area 10: Environments, configuration and infrastructure

### Candidate requirements

1. **MUST** — Production is separated from all non-production environments (separate accounts/projects or equivalent
   isolation, credentials and data); access to production is restricted and logged.
   *Evidence:* account/project map; IAM showing distinct roles per environment; no shared credentials. *Sources:* SSDF (PO.5.1),
   AWS-SEC01-01.
2. **SHOULD** — At least one pre-production environment exists in which a release is deployed and checked, using the same
   artifact and deployment process as production, before it reaches production.
   *Evidence:* environment list; pipeline shows the same artifact digest promoted from pre-prod to prod. *Sources:* DORA-DA,
   AWS-OPS06-02.
3. **SHOULD** — Development, pre-production and production are kept as similar as practical (same backing-service types and
   major versions, same OS/runtime image); known differences are documented.
   *Evidence:* parity table in docs; compose/IaC files referencing the same engine versions. *Sources:* 12F-X, SP800-190.
4. **MUST** — Config that varies between deploys (endpoints, credentials, per-environment values) is kept out of the code and
   out of the built artifact, and is supplied at deploy/run time.
   *Evidence:* the same image runs in every environment; config read from environment/config service; no environment names
   hard-coded in code paths. *Sources:* 12F-III, 12F-V, DORA-DA.
5. **MUST** — Secrets are held in a secrets store (or equivalent encrypted, access-controlled mechanism), never in source code,
   images, CI build arguments or committed config files; they can be rotated.
   *Evidence:* secrets-manager references in deploy config; secret scanning clean; rotation record. *Sources:* AWS-SEC02-03,
   12F-III, SP800-190.
6. **MUST** — Infrastructure and environment configuration are defined as code in version control, so any environment can be
   recreated from the repository.
   *Evidence:* IaC files (Terraform/CloudFormation/CDK/etc.) for all long-lived resources; a documented rebuild of an
   environment from code. *Sources:* DORA-VC, DORA-DA, CD-CM, SSDF (PS.1.1).
7. **SHOULD** — Infrastructure and configuration changes go through the same review and pipeline as application changes; manual
   console changes in production are exceptional and reconciled back into code.
   *Evidence:* IaC plan/apply in CI; drift-detection reports. *Sources:* AWS-OPS05-03, AWS-REL08-05, AWS-REL08-04.
8. **SHOULD** — Configuration is validated (schema/required keys) at start-up and fails fast with a clear error when invalid.
   *Evidence:* start-up validation code; tests for missing config. *Sources:* AWS-OPS05-03 [partly judgement].
9. **SHOULD** — Running infrastructure is immutable: changes are rolled out by replacing instances/containers, not editing them
   in place. *Evidence:* deploys create new task/instance revisions; no SSH edits in runbooks. *Sources:* AWS-REL08-04, SP800-190.
10. **MUST** — A new developer can set up a working local environment from the repository's documented steps alone, with
    dependencies declared and isolated (no reliance on unstated system-wide tools).
    *Evidence:* README "getting started" that a newcomer followed recently; time-to-first-run noted. *Sources:* 12F-II.
11. **SHOULD** — The local environment is containerised or otherwise scripted (e.g. compose file, dev container) and runs the
    same backing services as production.
    *Evidence:* `docker-compose.yml`/`devcontainer.json`; one-command bootstrap. *Sources:* SP800-190, DEVCON, 12F-X.
12. **SHOULD** — One-off administrative tasks (migrations, data fixes, consoles) run against a release in the same environment
    and config as the app, from code shipped with the app. *Evidence:* scripts in repo; run records. *Sources:* 12F-XII.
13. **SHOULD** — Every environment and resource is labelled with owner, environment and purpose so that cost, access and
    clean-up can be attributed. *Evidence:* tagging policy; tag-compliance report. *Sources:* AWS-COST03-02.
14. **MAY** — Backing services are attached via config (URL/credentials) so they can be swapped (e.g. restored database)
    without code change. *Evidence:* service handles only in config. *Sources:* 12F-IV.

### Failure modes

- "Staging" that shares the production database, account or credentials, so tests touch real data [judgement; see SSDF PO.5.1].
- Config committed to the repo, or baked into the image at build time, so a credential change needs a rebuild and the
  codebase could not be opened "without compromising any credentials" (12F-III).
- Infrastructure clicked together in a console; nobody can rebuild it, and DR depends on memory (DORA-VC, CD-CM).
- Configuration drift between environments or between primary and recovery sites (AWS-REL13-04).
- Local setup that works only on the original developer's machine; "works on my machine" (SP800-190).
- Different dev and prod backing services (e.g. SQLite locally, PostgreSQL in production) hiding defects (12F-X).

### Sources

- **12F-II / 12F-III / 12F-IV / 12F-V / 12F-IX / 12F-X / 12F-XII** — Adam Wiggins, *The Twelve-Factor App*, factors II, III, IV,
  V, IX, X, XII. https://12factor.net/dependencies, /config, /backing-services, /build-release-run, /disposability,
  /dev-prod-parity, /admin-processes — accessed 2026-10-31.
  - II: "A twelve-factor app never relies on implicit existence of system-wide packages. It declares all dependencies, completely and exactly, via a dependency declaration manifest."
  - II: "The new developer can check out the app’s codebase onto their development machine, requiring only the language runtime and dependency manager installed as prerequisites."
  - III: "An app’s config is everything that is likely to vary between deploys (staging, production, developer environments, etc)."
  - III: "A litmus test for whether an app has all config correctly factored out of the code is whether the codebase could be made open source at any moment, without compromising any credentials."
  - IV: "In both cases, only the resource handle in the config needs to change."
  - X: "Keep development, staging, and production as similar as possible"
  - X: "The tools gap: Developers may be using a stack like Nginx, SQLite, and OS X, while the production deploy uses Apache, MySQL, and Linux."
  - XII: "One-off admin processes should be run in an identical environment as the regular long-running processes of the app."
- **DORA-VC** — "Capabilities: Version control", DORA (Google Cloud). https://dora.dev/capabilities/version-control/ — accessed 2026-10-31.
  - "teams need to use version control for source code, test and deployment scripts, infrastructure and application configuration information, and the many libraries and packages they depend upon."
  - "Teams must be able to provision any environment in a fully automated fashion, and know that any new environment reproduced from the same configuration is identical."
- **DORA-DA** — "Capabilities: Deployment automation", DORA. https://dora.dev/capabilities/deployment-automation/ — accessed 2026-10-31.
  - "Use the same packages for every environment. This rule means that you should keep environment-specific configuration separate from packages."
  - "Make it possible to recreate the state of any environment from information stored in version control."
- **CD-CM** — Jez Humble, "Configuration Management", continuousdelivery.com.
  https://continuousdelivery.com/foundations/configuration-management/ — accessed 2026-10-31.
  - "we need to version control everything required to perform these processes, including source code, test and deployment scripts, infrastructure and application configuration information, and the many libraries and packages we depend upon."
- **SSDF** (defined in Area 9).
  - PO.5.1: "Separate and protect each environment involved in software development."
  - PS.1.1: "Store all forms of code – including source code, executable code, and configuration-as-code – based on the principle of least privilege"
- **SP800-190** (defined in Area 9).
  - "This solves the “works on my machine” problem since the developer, build system, and production all run the same immutable artifact."
- **AWS-SEC01-01** — "SEC01-BP01 Separate workloads using accounts", AWS Well-Architected, Security Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_multi_accounts.html — accessed 2026-10-31.
  - "An account structure that isolates cloud operations, unrelated workloads, and environments into separate accounts, increasing security across the cloud infrastructure."
- **AWS-SEC02-03** — "SEC02-BP03 Store and use secrets securely", AWS Well-Architected, Security Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_identities_secrets.html — accessed 2026-10-31.
  - Anti-patterns: "Not rotating credentials. Storing long-term credentials in source code or configuration files. Storing credentials at rest unencrypted."
- **AWS-OPS05-03** — "OPS05-BP03 Use configuration management systems", AWS Well-Architected, Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_conf_mgmt_sys.html — accessed 2026-10-31.
  - "You configure, validate, and deploy as part of your continuous integration, continuous delivery (CI/CD) pipeline. You monitor to validate configurations are correct."
- **AWS-REL08-04** — "REL08-BP04 Deploy using immutable infrastructure", AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_immutable_infrastructure.html — accessed 2026-10-31.
  - "With immutable infrastructure, no in-place modifications are allowed to run infrastructure resources within a workload."
- **AWS-REL08-05** — "REL08-BP05 Deploy changes with automation", AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_automated_changemgmt.html — accessed 2026-10-31.
  - Anti-patterns: "You perform manual changes. You skip steps in your automation through manual emergency workflows."
- **AWS-REL13-04** — "REL13-BP04 Manage configuration drift at the DR site or Region", AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_config_drift.html — accessed 2026-10-31.
  - "You fail to update recovery locations when changes are made to the primary locations, which results in outdated configurations that could hinder recovery efforts."
- **AWS-COST03-02** — "COST03-BP02 Add organization information to cost and usage", AWS Well-Architected, Cost Optimization Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_org_information.html — accessed 2026-10-31.
  - "Implement consistent tagging across all resources where possible by purpose, team, environment, or other criteria relevant to your business."
- **DEVCON** — "Development Containers" (Development Container Specification). https://containers.dev/ — accessed 2026-10-31.
  - "A development container (or dev container for short) allows you to use a container as a full-featured development environment."
- **AWS-OPS06-02** (defined in Area 11).

---

## Area 11: Release and deployment

### Candidate requirements

1. **MUST** — Deployment to every environment, including production, is automated and uses the same process and the same
   artifact; a deployment is a single action by an authorised person or pipeline, not a sequence of manual steps.
   *Evidence:* deploy pipeline definition; deploy logs show artifact digest; no manual steps in release runbook.
   *Sources:* DORA-DA, AWS-REL08-05, AWS-OPS05-04.
2. **SHOULD** — The main branch is kept in a deployable state and the team can release on demand, in small batches.
   *Evidence:* release frequency; size of releases; CI status history. *Sources:* DORA-CD, CD-PR, AWS-OPS06-01.
3. **MUST** — Every release has a unique, immutable identifier; a released version is never modified (any change is a new
   release) and is traceable to its commit.
   *Evidence:* tags/image digests per release; deploy log mapping env → version → commit. *Sources:* 12F-V, SEMVER, DORA-VC.
4. **SHOULD** — Components with a public API or consumers outside the team (libraries, external APIs) follow Semantic
   Versioning; applications MAY use another scheme as long as requirement 3 holds.
   *Evidence:* version history consistent with breaking-change rules; declared public API. *Sources:* SEMVER.
5. **SHOULD** — A human-readable changelog / release notes are maintained per version (latest first, dated, grouped by type
   of change, with an Unreleased section), not a dump of commit messages.
   *Evidence:* CHANGELOG file or release pages; entry per release. *Sources:* KAC, SRE-RE.
6. **MUST** — Who may approve and perform a production release is defined, enforced by access control, and recorded per release.
   *Evidence:* protected deploy environment / required approvers; audit log of who deployed what and when. *Sources:* SRE-RE,
   DORA-DA [approval model: judgement].
7. **MUST** — Each release has a tested rollback (or roll-forward) path, and the previous release can be restored quickly.
   *Evidence:* rollback procedure in runbook; record of a rollback exercise; previous artifacts retained. *Sources:* AWS-OPS06-01,
   12F-V, DORA-VC, FOWLER-BG.
8. **SHOULD** — Production deploys use a safe rollout strategy (rolling, blue-green or canary) with automated health checks
   that stop or roll back a bad release, rather than all-at-once replacement.
   *Evidence:* deployment configuration (min healthy %, health check path, circuit breaker); canary/bake-time settings.
   *Sources:* AWS-OPS06-03, AWS-OPS06-04, SREW-CANARY, SRE-INTRO, FOWLER-BG.
9. **SHOULD** — Deploys cause no user-visible downtime: processes start fast and shut down gracefully (stop accepting work,
   finish in-flight requests/jobs) so instances can be replaced safely.
   *Evidence:* SIGTERM handling; drain/deregistration delay; zero-error deploy in monitoring. *Sources:* 12F-IX, DORA-DB.
10. **SHOULD** — A post-deploy smoke test verifies the release in each environment. *Evidence:* smoke-test step in pipeline.
    *Sources:* DORA-DA, AWS-OPS06-02.
11. **MUST** — Database schema changes are versioned migration scripts in version control, applied by a tool that records which
    migrations each database has run, through the same pipeline as the application.
    *Evidence:* migrations directory; migration-history table; pipeline step running migrations. *Sources:* DORA-DB, 12F-XII.
12. **SHOULD** — Schema changes are backward compatible with the currently running application version (expand/contract,
    "parallel change"), so the app can be rolled back without a database rollback; destructive changes are split across releases.
    *Evidence:* migration review checklist; examples of add-then-remove across releases. *Sources:* DORA-DB.
13. **SHOULD** — Migrations with production impact (locks, long runs, large tables) are reviewed with whoever operates the
    production database before release. *Evidence:* review record on the migration PR. *Sources:* DORA-DB.
14. **MAY** — Feature flags decouple deploy from release; when used, each flag has an owner and an expiry and is removed when
    no longer needed. *Evidence:* flag inventory with owner/expiry; removal PRs. *Sources:* FOWLER-FT.
15. **MAY** — Releases are gated by the error budget: if the SLO budget is exhausted, feature releases pause in favour of
    reliability work. *Evidence:* error-budget policy; release decisions referencing it. *Sources:* SRE-RISK, SREW-SLO.
16. **SHOULD** — Delivery performance is measured with the DORA software delivery metrics (lead time, deployment frequency,
    change fail rate, failed deployment recovery time, rework rate) per service and used for improvement, not as targets.
    *Evidence:* metric dashboard or periodic report. *Sources:* DORA-MET.

### Failure modes

- Manual, multi-step deployments that differ per environment; the production deploy is the first time the procedure runs
  (DORA-DA "Use the same deployment process for every environment").
- Rebuilding per environment, so what reaches production is not what was tested (DORA-DA).
- All-at-once deploys with no bake time; a defect hits all users at once (AWS-OPS06-03, AWS-REL08-05).
- Rollback "plan" that was never exercised, or blocked by a destructive migration already applied (AWS-OPS06-01, DORA-DB).
- Changelogs generated from raw commit logs, "full of noise" (KAC).
- Feature flags that are never removed and become permanent configuration debt (FOWLER-FT).

### Sources

- **DORA-CD** — "Capabilities: Continuous delivery", DORA. https://dora.dev/capabilities/continuous-delivery/ — accessed 2026-10-31.
  - "Continuous delivery is the ability to release changes of all kinds on demand quickly, safely, and sustainably."
  - "Is our software in a deployable state throughout its lifecycle?"
- **DORA-DA** (defined in Area 10).
  - "Use the same deployment process for every environment, including production."
  - "Perform a deployment test to make sure that any necessary external services are reachable, and that the system is functioning."
  - "Your deployment process should download the packages from an artifact repository"
- **DORA-DB** — "Capabilities: Database change management", DORA. https://dora.dev/capabilities/database-change-management/ — accessed 2026-10-31.
  - "Teams that do well at continuous delivery store their database changes as scripts in version control and manage these changes in the same way they manage production application changes."
  - "You then ensure that every database instance has a table that records which migrations have been run against that particular instance."
  - "The application can then write to both old and new columns, lazily migrating the data, and also allowing for application rollback without requiring a database rollback."
- **DORA-MET** — Nathen Harvey, "DORA’s software delivery performance metrics", DORA Guides.
  https://dora.dev/guides/dora-metrics/ — accessed 2026-10-31.
  - "Change lead time: The amount of time it takes for a change to go from committed to version control to deployed in production."
  - "Setting metrics as a goal. Ignoring Goodhart’s law and making broad statements like, “Every application must deploy multiple times per day by year’s end,” increases the likelihood that teams will try to game the metrics."
- **CD-PR** — Jez Humble, "Principles", continuousdelivery.com. https://continuousdelivery.com/principles/ — accessed 2026-10-31.
  - "There are five principles at the heart of continuous delivery: Build quality in Work in small batches Computers perform repetitive tasks, people solve problems Relentlessly pursue continuous improvement Everyone is responsible" (list items run together in the source text)
- **SEMVER** — Tom Preston-Werner, "Semantic Versioning 2.0.0". https://semver.org/ — accessed 2026-10-31.
  - "Once a versioned package has been released, the contents of that version MUST NOT be modified. Any modifications MUST be released as a new version."
  - "Software using Semantic Versioning MUST declare a public API."
  - "MAJOR version when you make incompatible API changes"
- **KAC** — Olivier Lacan, "Keep a Changelog" 1.1.0. https://keepachangelog.com/en/1.1.0/ — accessed 2026-10-31.
  - "A changelog is a file which contains a curated, chronologically ordered list of notable changes for each version of a project."
  - "Keep an Unreleased section at the top to track upcoming changes."
  - "Using commit log diffs as changelogs is a bad idea: they're full of noise."
- **12F-V** (defined in Area 10).
  - "Every release should always have a unique release ID, such as a timestamp of the release (such as 2011-04-06-20:32:17) or an incrementing number (such as v100)."
  - "Releases are an append-only ledger and a release cannot be mutated once it is created."
- **12F-IX** (defined in Area 10).
  - "For a web process, graceful shutdown is achieved by ceasing to listen on the service port (thereby refusing any new requests), allowing any current requests to finish, and then exiting."
- **12F-XII** (defined in Area 10).
  - "Admin code must ship with application code to avoid synchronization issues."
- **SRE-RE** (defined in Area 9).
  - "Several layers of security and access control determine who can perform specific operations when releasing a project."
  - "Our automated release system produces a report of all changes contained in a release, which is archived with other build artifacts."
- **SRE-INTRO** — Benjamin Treynor Sloss, "Introduction", *Site Reliability Engineering* (Google, O'Reilly 2016).
  https://sre.google/sre-book/introduction/ — accessed 2026-10-31.
  - "SRE has found that roughly 70% of outages are due to changes in a live system."
  - "Implementing progressive rollouts Quickly and accurately detecting problems Rolling back changes safely when problems arise" (list items run together in the source text)
- **SREW-CANARY** — "Canarying Releases", Chapter 16 of *The Site Reliability Workbook* (Google, O'Reilly 2018).
  https://sre.google/workbook/canarying-releases/ — accessed 2026-10-31.
  - "We define canarying as a partial and time-limited deployment of a change in a service and its evaluation."
- **FOWLER-BG** — Martin Fowler, "Blue Green Deployment", 1 March 2010. https://martinfowler.com/bliki/BlueGreenDeployment.html — accessed 2026-10-31.
  - "Blue-green deployment also gives you a rapid way to rollback - if anything goes wrong you switch the router back to your blue environment."
- **FOWLER-FT** — Pete Hodgson, "Feature Toggles (aka Feature Flags)", martinfowler.com, 09 October 2017.
  https://martinfowler.com/articles/feature-toggles.html — accessed 2026-10-31.
  - "Savvy teams view their Feature Toggles as inventory which comes with a carrying cost, and work to keep that inventory as low as possible."
  - "In order to keep the number of feature flags manageable a team must be proactive in removing feature flags that are no longer needed."
- **AWS-OPS06-01** — "OPS06-BP01 Plan for unsuccessful changes", AWS Well-Architected, Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_plan_for_unsucessful_changes.html — accessed 2026-10-31.
  - "You have prepared a detailed recovery plan for your change in the event it is unsuccessful. In addition, you have reduced the size of your release to minimize the potential impact on other workload components."
- **AWS-OPS06-02** — "OPS06-BP02 Test deployments", AWS Well-Architected, Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_test_val_chg.html — accessed 2026-10-31.
  - "During production releases, untested deployments cause frequent issues that require troubleshooting and escalation."
- **AWS-OPS06-03** — "OPS06-BP03 Employ safe deployment strategies", AWS Well-Architected, Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_deploy_mgmt_sys.html — accessed 2026-10-31.
  - "You deploy an unsuccessful change to all of production all at once. As a result, all customers are impacted simultaneously."
- **AWS-OPS06-04** — "OPS06-BP04 Automate testing and rollback", AWS Well-Architected, Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_mit_deploy_risks_auto_testing_and_rollback.html — accessed 2026-10-31.
  - "Your monitoring is able to validate against your success criteria and initiate automatic rollback upon failure."
- **AWS-REL08-05**, **AWS-OPS05-04**, **DORA-VC** (defined in Areas 9–10).
  - AWS-REL08-05: "You perform rapid follow-on deployments without allowing for bake time."
  - DORA-VC: "Storing all artifacts in version control means teams can roll back to a previously verified working state quickly and reliably."
- **SRE-RISK**, **SREW-SLO** (defined in Area 12).

---

## Area 12: Operations and reliability

### Candidate requirements

1. **MUST** — Each production service has documented service-level indicators and objectives (SLIs/SLOs) based on what users
   care about, stating how each is measured, with named approvers and a review date.
   *Evidence:* SLO document; dashboard showing SLI vs SLO. *Sources:* SRE-SLO, SREW-SLO.
2. **SHOULD** — An error-budget policy, agreed by product and engineering, states what happens when the budget is spent
   (e.g. pause feature releases). *Evidence:* signed-off policy; instances of it being applied. *Sources:* SRE-RISK, SREW-SLO.
3. **MUST** — Routine and emergency operational procedures (deploy, rollback, restore, credential rotation, common alerts) are
   written as runbooks/playbooks, kept in version control and updated when the system changes.
   *Evidence:* runbook directory; last-updated dates vs. recent changes; each alert links to a runbook entry.
   *Sources:* AWS-OPS07-03, SREW-ONCALL, SRE-INTRO.
4. **MUST** — There is a documented incident-management process: when to declare an incident, severity levels, roles (incident
   commander, operations, communications), a live incident record, and stakeholder communication.
   *Evidence:* incident procedure document; incident records with timelines and roles. *Sources:* SRE-MI, AWS-OPS10-01.
5. **MUST** — Incidents that meet pre-defined criteria (user-visible impact beyond a threshold, any data loss, manual
   intervention such as rollback, monitoring failure) get a written, blameless postmortem with owned, prioritised action items
   that are tracked to completion. *Evidence:* postmortem repository; action items in the issue tracker with owners and status.
   *Sources:* SRE-PM, SREW-PM.
6. **MUST** — There is a defined on-call or support rota (who responds, when, how to escalate) proportional to the service's
   availability needs; alerts reach a named responder. *Evidence:* rota/schedule; escalation path; alert-routing config.
   *Sources:* SRE-ONCALL, AWS-REL06-03.
7. **SHOULD** — On-call load is sustainable and responders are prepared (training, practice exercises, handover).
   *Evidence:* pages per shift; training records; game-day/"Wheel of Misfortune" records. *Sources:* SRE-ONCALL.
8. **MUST** — Each workload has a recovery point objective (RPO) and recovery time objective (RTO) agreed with the business.
   *Evidence:* RPO/RTO recorded per system with business approval. *Sources:* AWS-REL13-01.
9. **MUST** — All data that cannot be reproduced is identified and backed up automatically at a frequency that meets the RPO,
   with backups protected from the same failure (and from deletion) as the source.
   *Evidence:* data inventory; backup configuration and retention; copies in a separate account/region where required.
   *Sources:* AWS-REL09-01.
10. **MUST** — Restores are tested periodically: data is actually restored, queried for correctness, and the time taken is
    compared with the RTO. *Evidence:* dated restore-test records with measured duration and verification steps. *Sources:* AWS-REL09-04.
11. **SHOULD** — A disaster-recovery plan exists and is exercised on a schedule; recovery environments are kept in configuration
    parity with production. *Evidence:* DR plan; DR exercise reports; drift checks. *Sources:* AWS-REL13-03, AWS-REL13-04, DORA-DA.
12. **SHOULD** — Capacity is planned from forecast demand (organic growth and known events) and validated by regular load
    testing; quotas and limits are monitored before they are reached.
    *Evidence:* capacity plan; load-test results; quota alarms. *Sources:* SRE-INTRO, AWS-REL01-04.
13. **SHOULD** — Running cost is attributed (tags/labels per service and environment) and reviewed periodically against
    budget. *Evidence:* cost report by tag; budget alerts. *Sources:* AWS-COST03-02.
14. **SHOULD** — Alerts are actionable: thresholds are reviewed so they are neither so high that vital alerts are missed nor
    so low that they are ignored. *Evidence:* alert inventory with owners; review records. *Sources:* AWS-REL06-03.

### Failure modes

- No SLO, so "users often develop their own beliefs about desired performance" and reliability work is unprioritised (SRE-SLO).
- Backups assumed to work but never restored: "Assuming that a backup exists" (AWS-REL09-04).
- No defined RPO/RTO, or "arbitrary recovery objectives" (AWS-REL13-01).
- Procedures that live in one person's head: "Relying on memory to complete each step of a process" (AWS-OPS07-03).
- Postmortems that assign blame or produce vague action items ("Improve", "Make better") with no owner or priority (SRE-PM, SREW-PM).
- Runbooks that drift out of date as the system changes (AWS-OPS07-03, SREW-ONCALL).

### Sources

- **SRE-SLO** — Chris Jones, John Wilkes, Niall Murphy, Cody Smith, "Service Level Objectives", Chapter 4 of *Site Reliability
  Engineering* (Google, O'Reilly 2016). https://sre.google/sre-book/service-level-objectives/ — accessed 2026-10-31.
  - "Start by thinking about (or finding out!) what your users care about, not what you can measure."
  - "For maximum clarity, SLOs should specify how they’re measured and the conditions under which they’re valid."
  - "Without an explicit SLO, users often develop their own beliefs about desired performance"
- **SRE-RISK** — Marc Alvidrez, "Embracing Risk", Chapter 3 of *Site Reliability Engineering*.
  https://sre.google/sre-book/embracing-risk/ — accessed 2026-10-31.
  - "As long as the uptime measured is above the SLO—in other words, as long as there is error budget remaining—new releases can be pushed."
  - "If SLO violations occur frequently enough to expend the error budget, releases are temporarily halted while additional resources are invested in system testing and development"
- **SREW-SLO** — "Implementing SLOs", Chapter 2 of *The Site Reliability Workbook*. https://sre.google/workbook/implementing-slos/ — accessed 2026-10-31.
  - "An appropriately defined SLO should be documented in a prominent location where other teams and stakeholders can review it."
  - "The authors of the SLO, the reviewers (who checked it for technical accuracy), and the approvers (who made the business decision about whether it is the right SLO)."
  - "The organization has committed to using the error budget for decision making and prioritizing. This commitment is formalized in an error budget policy."
- **SRE-PM** — John Lunney, Sue Lueder, "Postmortem Culture: Learning from Failure", Chapter 15 of *Site Reliability Engineering*.
  https://sre.google/sre-book/postmortem-culture/ — accessed 2026-10-31.
  - "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring."
  - "It is important to define postmortem criteria before an incident occurs so that everyone knows when a postmortem is necessary."
  - "For a postmortem to be truly blameless, it must focus on identifying the contributing causes of the incident without indicting any individual or team for bad or inappropriate behavior."
  - Trigger list includes: "Data loss of any kind" and "A monitoring failure (which usually implies manual incident discovery)".
- **SREW-PM** — "Postmortem Culture: Learning from Failure", Chapter 10 of *The Site Reliability Workbook*.
  https://sre.google/workbook/postmortem-culture/ — accessed 2026-10-31.
  - "All of the action items have been tagged with an equal priority. There’s no way to determine which action to tackle first."
  - "The first two action items in the list use ambiguous phrases like “Improve” and “Make better.” These terms are vague and open to interpretation."
- **SRE-MI** — Andrew Stribblehill, "Managing Incidents", Chapter 14 of *Site Reliability Engineering*.
  https://sre.google/sre-book/managing-incidents/ — accessed 2026-10-31.
  - "It is better to declare an incident early and then find a simple fix and close out the incident than to have to spin up the incident management framework hours into a burgeoning problem."
  - "Set clear conditions for declaring an incident."
  - "The incident commander’s most important responsibility is to keep a living incident document."
  - "Prepare.Develop and document your incident management procedures in advance, in consultation with incident participants." (no space after "Prepare." in source)
- **SRE-ONCALL** — Andrea Spadaccini, "Being On-Call", Chapter 11 of *Site Reliability Engineering*.
  https://sre.google/sre-book/being-on-call/ — accessed 2026-10-31.
  - "The most important on-call resources are:" followed by "Clear escalation paths", "Well-defined incident-management procedures", "A blameless postmortem culture".
  - "of the remainder, no more than 25% can be spent on-call, leaving up to another 25% on other types of operational, nonproject work."
- **SREW-ONCALL** — "On-Call", Chapter 8 of *The Site Reliability Workbook*. https://sre.google/workbook/on-call/ — accessed 2026-10-31.
  - "In SRE, whenever an alert is created, a corresponding playbook entry is usually created."
  - "Details in playbooks go out of date at the same rate as production environment changes."
- **SRE-INTRO** (defined in Area 11).
  - "When humans are necessary, we have found that thinking through and recording the best practices ahead of time in a \"playbook\" produces roughly a 3x improvement in MTTR as compared to the strategy of \"winging it.\"" (straight double quotes in source)
  - "Regular load testing of the system to correlate raw capacity(servers, disks, and so on) to service capacity" (no space before "(" in source)
  - "Capacity planning should take both organic growth (which stems from natural product adoption and usage by customers) and inorganic growth"
- **AWS-OPS07-03** — "OPS07-BP03 Use runbooks to perform procedures", AWS Well-Architected, Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html — accessed 2026-10-31.
  - "The runbooks contain the desired outcome, necessary tools and permissions, and instructions for error handling. They are stored in a central location (version control system) and updated frequently."
  - Anti-patterns: "Relying on memory to complete each step of a process." and "Letting runbooks drift out of sync with system changes and automation."
- **AWS-OPS10-01** — "OPS10-BP01 Use a process for event, incident, and problem management", AWS Well-Architected,
  Operational Excellence Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_event_response_event_incident_problem_process.html — accessed 2026-10-31.
  - "Your organization effectively manages operational events, incidents, and problems through well-documented and centrally stored processes."
  - Anti-pattern: "Your organization does not analyze and learn from incidents to prevent future occurrences."
- **AWS-REL13-01** — "REL13-BP01 Define recovery objectives for downtime and data loss", AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html — accessed 2026-10-31.
  - "Every workload has a designated RTO and RPO based on technical considerations and business impact."
  - Anti-patterns: "You haven't designated recovery objectives. You select arbitrary recovery objectives."
- **AWS-REL09-01** — "REL09-BP01 Identify and back up all data that needs to be backed up, or reproduce the data from sources",
  AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_identified_backups_data.html — accessed 2026-10-31.
  - "Data sources have been identified and classified based on criticality. Then, establish a strategy for data recovery based on the RPO."
  - Anti-patterns: "Not taking backups of critical data sources." and "No defined RPO, or backup frequency cannot meet RPO."
- **AWS-REL09-04** — "REL09-BP04 Perform periodic recovery of the data to verify backup integrity and processes", AWS
  Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html — accessed 2026-10-31.
  - "Data from backups is periodically recovered using well-defined mechanisms to verify that recovery is possible within the established recovery time objective (RTO) for the workload."
  - Anti-patterns: "Restoring a backup, but not querying or retrieving any data to check that the restoration is usable. Assuming that a backup exists."
- **AWS-REL13-03** — "REL13-BP03 Test disaster recovery implementation to validate the implementation", AWS Well-Architected,
  Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_dr_tested.html — accessed 2026-10-31.
  - "Regularly testing you disaster recovery plan verifies that it will work when it needs to, and that your team knows how to perform the strategy." ("you" sic in source)
- **AWS-REL01-04** — "REL01-BP04 Monitor and manage quotas", AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_manage_service_limits_monitor_manage_limits.html — accessed 2026-10-31.
  - Anti-pattern: "Not configuring monitoring to check for service quota thresholds"
- **AWS-REL06-03** — "REL06-BP03 Send notifications (Real-time processing and alarming)", AWS Well-Architected, Reliability Pillar.
  https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_monitor_aws_resources_notification_monitor.html — accessed 2026-10-31.
  - "When alarm thresholds are breached, the appropriate personnel and systems are notified so they can address underlying issues."
  - Anti-pattern: "Configuring alarms with a threshold that is too low, resulting in inaction on important alerts due to the noise of excessive notifications."
- **AWS-REL13-04**, **AWS-COST03-02**, **DORA-DA** (defined in Area 10).

---

## Gaps (could not source to a primary reference in this pass)

1. **Artifact retention periods**: SSDF PS.3.1 requires archiving per release but no source gives a retention length; the
   standard will need a [judgement] default (e.g. all releases still deployed plus N previous).
2. **Release approval model** (who signs off a production release, two-person rule, change advisory): only SRE-RE's "gated
   operations" list was found; no neutral framework text was sourced. ITIL change enablement and ISO/IEC 20000-1 are relevant
   but are paywalled and were not verified.
3. **Licence-policy content** (which licences to allow/deny): OpenChain/ISO/IEC 5230 defines a programme, not a list; the
   ISO text itself could not be fetched (bot challenge), only the OpenChain summary page.
4. **Updated SBOM minimum elements**: CISA has worked on a revision of the 2021 NTIA minimum elements; the current status of
   any revised version was not verified, so this file cites only the 2021 NTIA report.
5. **Configuration validation at start-up / fail-fast**: no primary source states it directly (AWS OPS05-BP03 is the nearest).
6. **Developer onboarding time / local-setup quality metric**: no authoritative source; 12-factor and the dev-container spec
   support the practice but not a measure.
7. **Business-hours-only support**: SRE sources assume 24/7 rotations; guidance for services that need only business-hours
   support was not found.
8. **Cost management beyond tagging** (budgets, anomaly alerts, FinOps practices): only AWS COST03-BP02 was verified; the
   FinOps Foundation framework was not fetched.
9. **Backup immutability / ransomware protection** and **NIST SP 800-34** contingency-planning text were not fetched; the
   protected-from-deletion part of the backup requirement (Area 12) is [judgement] until sourced.
