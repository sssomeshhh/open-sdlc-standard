# 5. Security

- **ID prefix:** SEC
- **Status:** draft, 2026-10-31

## Purpose

This area protects the system, its users and its data against unauthorised access, leaked credentials, known-vulnerable
components and insecure configuration. Most serious incidents trace back to a small set of design and configuration
mistakes (broken access control, hardcoded secrets, unpatched dependencies, debug features left on); the requirements
below make each of these visible and checkable.

## Scope

Covers threat modelling, authentication and authorisation, session handling, the secrets policy, secure defaults, what
vulnerability, dependency and secret scanning are needed and why, which security events to audit-log, security
review, and vulnerability reporting.

Left to other areas:

- Running scans as pipeline gates: see Area 8.
- Secrets store and configuration management, environment separation: see Area 10.
- Personal data (classification, minimisation, logging of personal data, data in repositories, test data and AI
  prompts): see Area 6.
- Code review guidelines: see Area 3. Required reviews and branch protection: see Area 7.
- Security testing as a test type: see Area 4.
- Dependency pinning, SBOM and provenance: see Area 9.
- Log, metric and trace mechanics, retention and alerting: see Area 13; protection of audit logs: OBS-11. Incident
  management: see Area 12.

## Requirements

### SEC-1 · MUST · Threat model kept with the system

The project MUST have a threat model created at design time and revisited whenever data flows, trust boundaries or
access controls change.

- **Gate:** G1 · **Trigger:** each change to data flows, trust boundaries or access controls
- **Evidence:** a dated threat model (for example a data-flow diagram, threats and mitigations) stored with the system's
  documentation; its change history shows a revision after each such design change.
- **Basis:** [SSDF], [OWASP-CS-THREAT], [T10-A06]. Level: author's judgement (sources support SHOULD).

### SEC-2 · MUST · Authorisation rules documented

The authorisation rules (which roles or users are allowed to perform which actions on which data) MUST be written down.

- **Gate:** G1
- **Evidence:** an authorisation matrix or policy document covering every role and every protected function and data
  type; it matches the roles defined in code.
- **Basis:** [ASVS5] 8.1.1.

### SEC-3 · MUST · Authorisation enforced server-side, deny by default

Authorisation MUST be enforced on a trusted server-side layer on every request, denying access unless a rule grants it.

- **Gate:** G2
- **Evidence:** central server-side authorisation checks in code; no endpoint relies on client-side checks; automated
  tests for denied cases, both horizontal (another user's data) and vertical (a higher role's function).
- **Basis:** [ASVS5] 8.3.1, [OWASP-CS-AUTHZ], [T10-A01].

### SEC-4 · MUST · Vetted authentication mechanism

Users MUST authenticate through a vetted mechanism (for example the organisation's single sign-on) rather than a
home-grown one. Failure messages: see SEC-17.

- **Gate:** G2
- **Evidence:** an authentication design note naming the mechanism and the reason it is considered vetted.
- **Basis:** Author's judgement (no primary source found).

### SEC-5 · MUST · Multi-factor authentication

User authentication MUST require multi-factor authentication, either in the application or through the identity
provider.

- **Gate:** G3
- **Evidence:** identity-provider or application configuration showing MFA enforced for all users; any exempt group is
  covered by a valid waiver (README, "Deviations and waivers"); a gap waiver is one-off and time-limited.
- **Basis:** [OWASP-CS-AUTHN]. Level: author's judgement (sources support SHOULD).

### SEC-6 · MUST · Server-side session expiry

Sessions MUST be controlled server-side so that they end after an idle timeout or an absolute timeout, or at logout,
and cannot be used afterwards. Session identifier renewal: see SEC-18.

- **Gate:** G2
- **Evidence:** session configuration with idle and absolute timeout values and their rationale; a test or manual check
  that a session token is rejected after logout and after expiry.
- **Basis:** [OWASP-CS-SESSION], [ASVS5] 7.4.1.

### SEC-7 · MUST · No secrets in code or logs

Secrets (passwords, API keys, tokens, signing keys) MUST NOT appear in source code, configuration files under version
control, or logs. Build artifacts and images: see BLD-13.

- **Gate:** G1
- **Evidence:** a clean secret-scan report over the full repository history (see SEC-9); application code reads secrets
  from the environment or a secrets store (see Area 10); a sample of logs contains no tokens or credentials.
- **Basis:** [ASVS5] 13.3.1, [OWASP-CS-SECRETS], [OWASP-CS-LOGGING].

### SEC-8 · MUST · Secret rotation, and revoke first on exposure

Every secret MUST have a documented rotation procedure, which is applied to an exposed secret first, before any
clean-up such as history rewriting.

- **Gate:** G2 · **Trigger:** each exposure of a secret
- **Evidence:** a secrets inventory with owner and rotation procedure per secret; for each past exposure, a record
  showing rotation at or before the clean-up.
- **Basis:** [OWASP-CS-SECRETS], [GH-SENSITIVE].

### SEC-9 · MUST · Secret scanning enabled

Automated secret scanning MUST be enabled on every repository, covering the full history, with every alert triaged.

- **Gate:** G1 · **Trigger:** each secret-scanning alert
- **Evidence:** secret scanning enabled in the repository settings or an equivalent scanner configuration; the alert
  list shows no untriaged alerts.
- **Basis:** [GH-SECRETSCAN]. "Every alert triaged": author's judgement (the quote describes what scanning covers).

### SEC-10 · SHOULD · Secrets blocked before they reach the repository

Pushes or commits that contain secrets SHOULD be blocked before they reach the shared repository (for example push
protection or a pre-commit hook).

- **Gate:** G1
- **Evidence:** push protection enabled, or a committed pre-commit configuration with a secret detector.
- **Basis:** [GH-PUSHPROT], [OWASP-CS-SECRETS].

### SEC-11 · MUST · Dependency vulnerabilities monitored and fixed on a schedule

Dependencies MUST be monitored for known vulnerabilities and fixed within written, risk-based remediation time frames
per severity.

- **Gate:** G1 · **Trigger:** each new dependency vulnerability alert
- **Evidence:** dependency vulnerability alerts enabled; a written remediation time frame per severity; no open alert
  older than its time frame.
- **Basis:** [ASVS5] 15.1.1, 15.2.1, [GH-DEPENDABOT], [SSDF].

### SEC-12 · SHOULD · Static analysis with tracked findings

Code SHOULD be analysed by static application security testing (SAST), with findings recorded and triaged in the
issue tracker.

- **Gate:** G1 · **Trigger:** each new static-analysis finding
- **Evidence:** a SAST configuration; findings linked to issues and closed or accepted with a reason.
- **Basis:** [SSDF], [GH-CODESCAN].

### SEC-13 · MUST · Secure defaults in production

Production MUST run with secure defaults: debug modes off, no default accounts, no reachable source-control metadata,
and generic error messages to users.

- **Gate:** G3
- **Evidence:** production configuration review; checks that `/.git`, debug pages and similar paths are not reachable;
  error responses contain no stack traces; no default credentials exist.
- **Basis:** [SSDF], [ASVS5] 13.4.1, 13.4.2, 16.5.1, [T10-A02].

### SEC-14 · MUST · Security events audit-logged

The system MUST log security events (authentication successes and failures, authorisation failures, administrative
actions) with who, what and when. Protection, retention and tamper evidence of these logs: see OBS-11.

- **Gate:** G3
- **Evidence:** a list of logged security events; sample entries showing actor, action and time.
- **Basis:** [ASVS5] 16.3.1, 16.3.2, [T10-A01], [T10-A09]. Administrative actions as events: author's judgement.

### SEC-15 · SHOULD · Security review of sensitive changes

Changes that touch authentication, authorisation, secrets, personal data or external interfaces SHOULD receive a
security-focused review before release.

- **Gate:** G1 · **Trigger:** each change touching authentication, authorisation, secrets, personal data or external interfaces
- **Evidence:** a label or checklist item marking security-relevant pull requests; a recorded security review on each.
- **Basis:** Author's judgement (no primary source found).

### SEC-16 · MUST · Vulnerability reporting route and handling policy

The project MUST publish how to report a vulnerability and have a policy for triage, remediation and disclosure.

- **Gate:** G3 · **Trigger:** each vulnerability report received
- **Evidence:** a `SECURITY.md` (or equivalent) with a contact and expected response time; for internet-facing services,
  a `/.well-known/security.txt`; a written triage and remediation policy.
- **Basis:** [SSDF], [GH-SECPOL], [OWASP-CS-VULN], [RFC9116].

### SEC-17 · MUST · Generic authentication failure messages

Authentication MUST answer every failed attempt with the same generic message, so that it does not reveal whether the
account exists.

- **Gate:** G2
- **Evidence:** login and password-reset failure messages are identical for unknown accounts and wrong credentials.
- **Basis:** [OWASP-CS-AUTHN].

### SEC-18 · MUST · Session identifier renewed on privilege change

A new session identifier MUST be issued after login and after any other privilege-level change.

- **Gate:** G2
- **Evidence:** a test or manual check that the session identifier differs before and after login and after a role
  change, and that the old identifier is rejected.
- **Basis:** [OWASP-CS-SESSION].

## Failure modes

- Authorisation enforced only in the user interface, or access granted by default. [T10-A01], [ASVS5]
- Secrets hardcoded in source or configuration files, then leaked through history or images. [OWASP-CS-SECRETS]
- A leaked secret "fixed" by rewriting history without rotating it, while old clones re-push it. [GH-SENSITIVE]
- Only successful logins logged, so attacks go unnoticed. [T10-A09]
- Default accounts, debug mode or verbose errors left on in production. [T10-A02]
- A threat model written once and never updated. [OWASP-CS-THREAT]

## References

- **[ASVS5]** OWASP Application Security Verification Standard 5.0.0. OWASP Foundation, 30 May 2025.
  https://github.com/OWASP/ASVS/tree/master/5.0/en (project page
  https://owasp.org/www-project-application-security-verification-standard/). Accessed 2026-10-31.
  > "Verify that authorization documentation defines rules for restricting function-level and data-specific access based on consumer permissions and resource attributes." (V8.1 Authorization Documentation)

  > "Verify that the application enforces authorization rules at a trusted service layer and doesn't rely on controls that an untrusted consumer could manipulate, such as client-side JavaScript." (V8.3 Operation Level Authorization)

  > "Verify that when session termination is triggered (such as logout or expiration), the application disallows any further use of the session." (V7.4 Session Termination)

  > "Secrets must not be included in application source code or included in build artifacts." (V13.3 Secret Management)

  > "Verify that the application is deployed either without any source control metadata, including the .git or .svn folders, or in a way that these folders are inaccessible both externally and to the application itself." (V13.4 Unintended Information Leakage)

  > "Verify that debug modes are disabled for all components in production environments to prevent exposure of debugging features and information leakage." (V13.4 Unintended Information Leakage)

  > "Verify that application documentation defines risk based remediation time frames for 3rd party component versions with vulnerabilities and for updating libraries in general" (V15.1 Secure Coding and Architecture Documentation)

  > "Verify that all authentication operations are logged, including successful and unsuccessful attempts." (V16.3 Security Events)

  > "Verify that failed authorization attempts are logged." (V16.3 Security Events)

  > "Verify that the application only contains components which have not breached the documented update and remediation time frames." (V15.2 Security Architecture and Dependencies)

  > "Verify that a generic message is returned to the consumer when an unexpected or security-sensitive error occurs" (V16.5 Error Handling)
- **[GH-CODESCAN]** About code scanning. GitHub Docs.
  https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning . Accessed 2026-10-31.
  > "Code scanning is a feature that you use to analyze the code in a GitHub repository to find security vulnerabilities and coding errors."
- **[GH-DEPENDABOT]** About Dependabot alerts. GitHub Docs.
  https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts . Accessed 2026-10-31.
  > "Dependabot alerts notify you about vulnerable dependencies so you can upgrade to secure versions and protect your project."
- **[GH-PUSHPROT]** About push protection. GitHub Docs.
  https://docs.github.com/en/code-security/concepts/secret-security/push-protection . Accessed 2026-10-31.
  > "Rather than alerting you to credential leaks after the fact, push protection blocks pushes that contain secrets before they reach your repository."
- **[GH-SECPOL]** Adding a security policy to your repository. GitHub Docs.
  https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy .
  Accessed 2026-10-31.
  > "In the new SECURITY.md file, add information about supported versions of your project and how to report a vulnerability."
- **[GH-SECRETSCAN]** About secret scanning. GitHub Docs.
  https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning . Accessed 2026-10-31.
  > "Secret scanning scans your entire Git history on all branches of your repository for hardcoded credentials, including API keys, passwords, tokens, and other known secret types."
- **[GH-SENSITIVE]** Removing sensitive data from a repository. GitHub Docs.
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository .
  Accessed 2026-10-31.
  > "if the sensitive data you need to remove is a secret (e.g. password/token/credential), as is often the case, then as a first step you need to revoke and/or rotate that secret." (About removing sensitive data from a repository)

  > "If a fellow developer has a clone from before your rewrite, and after your rewrite simply runs git pull followed by git push , the sensitive data will return." (Side effects of rewriting history)
- **[OWASP-CS-AUTHN]** Authentication Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html . Accessed 2026-10-31.
  > "an application must respond with a generic error message regardless of whether: The user ID or password was incorrect." (Authentication Responses)

  > "Multi-factor authentication (MFA) is by far the best defense against the majority of password-related attacks" (Multi-Factor Authentication)
- **[OWASP-CS-AUTHZ]** Authorization Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html . Accessed 2026-10-31.
  > "Permission should be validated correctly on every request, regardless of whether the request was initiated by an AJAX script, server-side, or any other source." (Validate the Permissions on Every Request)

  > "Least Privileges must be applied both horizontally and vertically." (Enforce Least Privileges)
- **[OWASP-CS-LOGGING]** Logging Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . Accessed 2026-10-31. The three items after
  the sentence are quoted from the list that follows it.
  > "The following should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted:" (Data to exclude)
  > "Access tokens" (Data to exclude)
  > "Authentication passwords" (Data to exclude)
  > "Encryption keys and other primary secrets" (Data to exclude)
- **[OWASP-CS-SECRETS]** Secrets Management Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html . Accessed 2026-10-31.
  > "Many organizations have them hardcoded within the source code in plaintext, littered throughout configuration files and configuration management tools." (1 Introduction)

  > "It is therefore better to automate the rotation of keys or at least ensure that the process is sufficiently supported by IT." (2.4 Automate Secrets Management)

  > "Consider enabling secrets detection at the developer level to avoid checking secrets into code before commit/PR either in the IDE, as part of test-driven development, or via pre-commit hook." (8.1 General detection approaches)
- **[OWASP-CS-SESSION]** Session Management Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html . Accessed 2026-10-31.
  > "The session ID must be renewed or regenerated by the web application after any privilege level change within the associated user session." (Renew the Session ID After Any Privilege Level Change)

  > "Session timeout management and expiration must be enforced server-side." (Idle Timeout)

  > "All sessions should implement an absolute timeout, regardless of session activity." (Absolute Timeout)
- **[OWASP-CS-THREAT]** Threat Modeling Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html . Accessed 2026-10-31.
  > "Threat modeling is ideally performed early in the SDLC, such as during the design phase." (Overview)

  > "A threat model is something that should be maintained, updated and refined alongside the system." (Overview)
- **[OWASP-CS-VULN]** Vulnerability Disclosure Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html . Accessed 2026-10-31.
  > "Provide a clear method for researchers to securely report vulnerabilities." (Introduction)

  > "Acknowledge the vulnerability details and provide a timeline to carry out triage." (Communicating With Researchers)
- **[RFC9116]** RFC 9116: A File Format to Aid in Security Vulnerability Disclosure. IETF (Foudil, Shafranovich), April
  2022. https://www.rfc-editor.org/rfc/rfc9116.html . Accessed 2026-10-31.
  > "This document defines a machine-parsable format ("security.txt") to help organizations describe their vulnerability disclosure practices to make it easier for researchers to report vulnerabilities."
- **[SSDF]** NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1. NIST (Souppaya, Scarfone,
  Dodson), February 2022. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf
  (landing page: https://csrc.nist.gov/pubs/sp/800/218/final). Accessed 2026-10-31.
  > "PW.1.1: Use forms of risk modeling – such as threat modeling, attack modeling, or attack surface mapping – to help assess the security risk for the software." (PW.1.1)

  > "RV.1.1: Gather information from software acquirers, users, and public sources on potential vulnerabilities in the software and third-party components that the software uses, and investigate all credible reports." (RV.1.1)

  > "record and triage all discovered issues and recommended remediations in the development team’s workflow or issue tracking system." (PW.7.2)

  > "PW.9.1: Define a secure baseline by determining how to configure each setting that has an effect on security or a security-related setting so that the default settings are secure" (PW.9.1)

  > "RV.1.3: Have a policy that addresses vulnerability disclosure and remediation, and implement the roles, responsibilities, and processes needed to support that policy." (RV.1.3)
- **[T10-A01]** OWASP Top 10:2025, A01 Broken Access Control. OWASP Top 10 Team.
  https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/ . Accessed 2026-10-31.
  > "Except for public resources, deny by default." (How to prevent)

  > "Log access control failures, alert admins when appropriate (e.g., repeated failures)." (How to prevent)
- **[T10-A02]** OWASP Top 10:2025, A02 Security Misconfiguration. OWASP Top 10 Team.
  https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ . Accessed 2026-10-31.
  > "Default accounts and their passwords are still enabled and unchanged." (Description)

  > "Error handling reveals stack traces or other overly informative error messages to users." (Description)
- **[T10-A06]** OWASP Top 10:2025, A06 Insecure Design. OWASP Top 10 Team.
  https://top10.owasp.org/2025/A06_2025-Insecure_Design/ . Accessed 2026-10-31.
  > "Threat modeling should be integrated into refinement sessions (or similar activities); look for changes in data flows and access control or other security controls."
- **[T10-A09]** OWASP Top 10:2025, A09 Security Logging and Alerting Failures. OWASP Top 10 Team.
  https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/ . Accessed 2026-10-31.
  > "Auditable events, such as logins, failed logins, and high-value transactions, are not logged or logged inconsistently"
