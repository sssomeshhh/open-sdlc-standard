# Research B: Areas 5–8 (Security; Privacy and data protection; Source control and repository hygiene; Continuous integration)

- **Prepared:** 2026-10-31, for the Open SDLC Standard (see `../README.md`).
- **Method:** every quote below was fetched from the cited URL on 2026-10-31 and checked by exact string match against
  the page text (HTML tags stripped, whitespace collapsed). PDFs (NIST, PPC) were converted with `pdftotext`. Quotes are
  verbatim; `…` is never used inside a quote. Levels are candidate levels; the areas set the final ones.
- **Level key:** MUST / SHOULD / MAY per RFC 2119 / RFC 8174. "[judgement]" = no source found that states it; author's call.
- **Versions used:** OWASP Top 10:2025 (current release), OWASP ASVS 5.0.0 (published 30 May 2025), NIST SP 800-218
  SSDF v1.1 (February 2022), NIST SP 800-53 Rev. 5.

---

## Area 5: Security

### Candidate requirements

1. **MUST** — Threat-model each system at design time and whenever data flows, trust boundaries or access controls change; keep the model with the system.
   *Evidence:* a dated threat model (data-flow diagram, threats, mitigations) in the repo or wiki; change history showing it was revisited when the design changed. *Sources:* SSDF (PW.1.1), CS-THREAT, T10-A06.
2. **MUST** — Document the authorisation rules (who may do what to which data) and enforce them server-side, deny-by-default, on every request.
   *Evidence:* an authorisation matrix/policy document; code showing central server-side checks; tests for denied cases (horizontal and vertical). *Sources:* ASVS5 (8.1.1, 8.2.1, 8.3.1), CS-AUTHZ, T10-A01.
3. **MUST** — Authenticate users through a vetted mechanism (prefer organisational SSO/MFA); authentication responses must not reveal whether the account exists.
   *Evidence:* auth design note; IdP configuration showing MFA; login/reset error messages are generic. *Sources:* ASVS5 (6.3.3), CS-AUTHN.
4. **MUST** — Manage sessions securely: server-side validation, regenerate session ID on login/privilege change, idle and absolute timeouts, real invalidation on logout, cookies `Secure`/`HttpOnly`/`SameSite`.
   *Evidence:* session config (TTL values with rationale), logout invalidates server-side, cookie flags in responses. *Sources:* ASVS5 (7.2.1, 7.3.1, 7.3.2, 7.4.1), CS-SESSION.
5. **MUST** — Keep secrets (passwords, API keys, tokens, signing keys) out of source code, images and build artifacts; hold them in a secrets manager with least-privilege access and a rotation process.
   *Evidence:* no secrets in repo/history (scanner report); secrets referenced from a vault/managed store; access list; rotation log or runbook. *Sources:* ASVS5 (13.3.1), CS-SECRETS, GH-SECUREUSE.
6. **MUST** — When a secret is exposed (committed, logged, shared), revoke/rotate it first; history rewriting is secondary.
   *Evidence:* incident record showing rotation timestamp before/alongside clean-up. *Sources:* GH-SENSITIVE.
7. **MUST** — Enable automated secret scanning on the repository, and SHOULD block pushes that contain secrets (push protection or pre-commit hook).
   *Evidence:* secret scanning / push protection enabled in repo settings, or a pre-commit config + CI job; alert list triaged. *Sources:* GH-SECRETSCAN, GH-PUSHPROT, CS-SECRETS.
8. **MUST** — Monitor dependencies for known vulnerabilities and remediate within documented, risk-based time frames.
   *Evidence:* dependency alerts enabled; written remediation SLA per severity; open alerts older than SLA = finding. *Sources:* ASVS5 (15.1.1, 15.2.1), GH-DEPENDABOT, SSDF (RV.1.1).
9. **SHOULD** — Run static analysis (SAST) and dependency review on every pull request, and record/triage findings in the issue tracker.
   *Evidence:* code-scanning workflow; dependency-review required check; findings tracked to closure. *Sources:* SSDF (PW.7.2, RV.1.2), GH-CODESCAN, GH-DEPREVIEW, CS-CICD.
10. **MUST** — Ship secure defaults: debug off, no default accounts, no exposed internal docs/monitoring endpoints or source-control metadata, generic error messages to users.
    *Evidence:* production config review; HTTP checks for `/.git`, debug pages, API docs; error responses contain no stack traces. *Sources:* SSDF (PW.9.1), ASVS5 (13.4.1, 13.4.2, 13.4.5, 16.5.1), T10-A02.
11. **MUST** — Log security events (authentication success/failure, authorisation failures, admin actions) with who/what/when/where; protect logs from tampering and unauthorised access; never log secrets or session tokens in clear.
    *Evidence:* log inventory; sample log entries; log store access controls and retention; grep of logs for tokens. *Sources:* ASVS5 (16.1.1, 16.2.1, 16.2.5, 16.3.1, 16.3.2, 16.4.2), CS-LOGGING, T10-A09.
12. **SHOULD** — Alert on suspicious security events (e.g. repeated access-control failures) and have an incident response plan.
    *Evidence:* alert rules; incident runbook; at least one exercised/real incident record. *Sources:* T10-A01, T10-A09.
13. **MUST** — Publish how to report a vulnerability (e.g. `SECURITY.md`, and `security.txt` for web-facing services) and have a policy for triage, remediation and disclosure.
    *Evidence:* `SECURITY.md` in repo; `/.well-known/security.txt` with Contact and Expires; documented triage SLA. *Sources:* SSDF (RV.1.3), GH-SECPOL, RFC9116, CS-VULN.
14. **SHOULD** — Perform a security review (code review with a security lens and/or security testing) for changes touching authentication, authorisation, secrets, personal data or external interfaces, before release.
    *Evidence:* PR label/checklist for security-relevant changes; review records; pen-test or DAST report for major releases. *Sources:* SSDF (PW.7.1, PW.7.2, PW.8.2).
15. **SHOULD** — Separate and protect development, test and production environments (MFA, network segmentation, least privilege).
    *Evidence:* access lists per environment; MFA enforced; no shared prod credentials in dev. *Sources:* SSDF (PO.5.1). (Overlaps Area 10.)
16. **SHOULD** — Give everyone who builds the software role-appropriate secure-development training.
    *Evidence:* training records per team member. *Sources:* SSDF (PO.2.2).

### Failure modes

- Authorisation enforced only in the UI or inconsistently per endpoint; access granted by default. (T10-A01: "Violation of the principle of least privilege, commonly known as deny by default, where access should only be granted for particular capabilities, roles, or users, but is available to anyone.")
- Secrets hardcoded in source or config files, then leaked via history or images. (CS-SECRETS: "Many organizations have them hardcoded within the source code in plaintext, littered throughout configuration files and configuration management tools.")
- Leaked secret "fixed" by rewriting history without rotating it; old clones re-push it. (GH-SENSITIVE)
- Only successful logins logged, or no alerting, so attacks go unnoticed. (T10-A09)
- Default accounts, debug mode or verbose errors left on in production. (T10-A02)
- Threat model written once and never updated. (CS-THREAT: "A threat model is something that should be maintained, updated and refined alongside the system.")

### Sources

- **SSDF** — *NIST SP 800-218, Secure Software Development Framework (SSDF) Version 1.1*, NIST (Souppaya, Scarfone, Dodson), Feb 2022. https://csrc.nist.gov/pubs/sp/800/218/final (PDF: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf). Accessed 2026-10-31.
  - "PW.1.1: Use forms of risk modeling – such as threat modeling, attack modeling, or attack surface mapping – to help assess the security risk for the software."
  - "RV.1.3: Have a policy that addresses vulnerability disclosure and remediation, and implement the roles, responsibilities, and processes needed to support that policy."
  - "PW.9.1: Define a secure baseline by determining how to configure each setting that has an effect on security or a security-related setting so that the default settings are secure"
  - "PO.5.1: Separate and protect each environment involved in software development."
  - "PO.2.2: Provide role-based training for all personnel with responsibilities that contribute to secure development."
  - "record and triage all discovered issues and recommended remediations in the development team’s workflow or issue tracking system." (PW.7.2)
  - "Configure the toolchain to perform automated code analysis and testing on a regular or continuous basis for all supported releases." (RV.1.2, Example 1)
  - "RV.1.1: Gather information from software acquirers, users, and public sources on potential vulnerabilities in the software and third-party components that the software uses, and investigate all credible reports."
- **ASVS5** — *OWASP Application Security Verification Standard 5.0.0*, OWASP Foundation, published 30 May 2025. Project page https://owasp.org/www-project-application-security-verification-standard/ ; requirement text from the official source repo https://github.com/OWASP/ASVS/tree/master/5.0/en (chapters V6, V7, V8, V13, V14, V15, V16). Accessed 2026-10-31.
  - 8.1.1: "Verify that authorization documentation defines rules for restricting function-level and data-specific access based on consumer permissions and resource attributes."
  - 8.3.1: "Verify that the application enforces authorization rules at a trusted service layer and doesn't rely on controls that an untrusted consumer could manipulate, such as client-side JavaScript."
  - 7.4.1: "Verify that when session termination is triggered (such as logout or expiration), the application disallows any further use of the session."
  - 13.3.1: "Secrets must not be included in application source code or included in build artifacts."
  - 13.4.1: "Verify that the application is deployed either without any source control metadata, including the .git or .svn folders, or in a way that these folders are inaccessible both externally and to the application itself."
  - 13.4.2: "Verify that debug modes are disabled for all components in production environments to prevent exposure of debugging features and information leakage."
  - 15.1.1: "Verify that application documentation defines risk based remediation time frames for 3rd party component versions with vulnerabilities and for updating libraries in general"
  - 16.3.1: "Verify that all authentication operations are logged, including successful and unsuccessful attempts."
  - 16.4.2: "Verify that logs are protected from unauthorized access and cannot be modified."
  - 16.5.1: "Verify that a generic message is returned to the consumer when an unexpected or security-sensitive error occurs"
- **T10-A01** — *OWASP Top 10:2025, A01 Broken Access Control*, OWASP Top 10 Team. https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/ (redirected from https://owasp.org/Top10/2025/). Accessed 2026-10-31.
  - "Except for public resources, deny by default."
  - "Log access control failures, alert admins when appropriate (e.g., repeated failures)."
- **T10-A02** — *OWASP Top 10:2025, A02 Security Misconfiguration*. https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ . Accessed 2026-10-31.
  - "Default accounts and their passwords are still enabled and unchanged."
  - "Error handling reveals stack traces or other overly informative error messages to users."
- **T10-A06** — *OWASP Top 10:2025, A06 Insecure Design*. https://top10.owasp.org/2025/A06_2025-Insecure_Design/ . Accessed 2026-10-31.
  - "Threat modeling should be integrated into refinement sessions (or similar activities); look for changes in data flows and access control or other security controls."
- **T10-A09** — *OWASP Top 10:2025, A09 Security Logging and Alerting Failures*. https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/ . Accessed 2026-10-31.
  - "Auditable events, such as logins, failed logins, and high-value transactions, are not logged or logged inconsistently"
  - "Establish or adopt an incident response and recovery plan, such as National Institute of Standards and Technology (NIST) 800-61r2 or later."
- **CS-THREAT** — *Threat Modeling Cheat Sheet*, OWASP Cheat Sheet Series. https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html . Accessed 2026-10-31.
  - "Threat modeling is ideally performed early in the SDLC, such as during the design phase."
  - "A threat model is something that should be maintained, updated and refined alongside the system."
- **CS-AUTHZ** — *Authorization Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html . Accessed 2026-10-31.
  - "Permission should be validated correctly on every request, regardless of whether the request was initiated by an AJAX script, server-side, or any other source."
  - "Least Privileges must be applied both horizontally and vertically."
- **CS-AUTHN** — *Authentication Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html . Accessed 2026-10-31.
  - "an application must respond with a generic error message regardless of whether: The user ID or password was incorrect."
  - "Multi-factor authentication (MFA) is by far the best defense against the majority of password-related attacks"
- **CS-SESSION** — *Session Management Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html . Accessed 2026-10-31.
  - "The session ID must be renewed or regenerated by the web application after any privilege level change within the associated user session."
  - "Session timeout management and expiration must be enforced server-side."
  - "All sessions should implement an absolute timeout, regardless of session activity."
- **CS-SECRETS** — *Secrets Management Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html . Accessed 2026-10-31.
  - "Consider enabling secrets detection at the developer level to avoid checking secrets into code before commit/PR either in the IDE, as part of test-driven development, or via pre-commit hook."
  - "It is therefore better to automate the rotation of keys or at least ensure that the process is sufficiently supported by IT."
- **CS-LOGGING** — *Logging Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . Accessed 2026-10-31.
  - "The following should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted:" (list includes "Access tokens" and "Sensitive personal data")
  - "The logging mechanisms and collected event data must be protected from mis-use such as tampering in transit, and unauthorized access, modification and deletion once stored."
- **CS-VULN** — *Vulnerability Disclosure Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html . Accessed 2026-10-31.
  - "Provide a clear method for researchers to securely report vulnerabilities."
  - "Acknowledge the vulnerability details and provide a timeline to carry out triage."
- **RFC9116** — *RFC 9116: A File Format to Aid in Security Vulnerability Disclosure*, IETF (Foudil, Shafranovich), April 2022. https://www.rfc-editor.org/rfc/rfc9116.html . Accessed 2026-10-31.
  - "This document defines a machine-parsable format ("security.txt") to help organizations describe their vulnerability disclosure practices to make it easier for researchers to report vulnerabilities."
- **GH-SECPOL** — *Adding a security policy to your repository*, GitHub Docs. https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy . Accessed 2026-10-31.
  - "In the new SECURITY.md file, add information about supported versions of your project and how to report a vulnerability."
- **GH-SECRETSCAN** — *About secret scanning*, GitHub Docs. https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning . Accessed 2026-10-31.
  - "Secret scanning scans your entire Git history on all branches of your repository for hardcoded credentials, including API keys, passwords, tokens, and other known secret types."
- **GH-PUSHPROT** — *About push protection*, GitHub Docs. https://docs.github.com/en/code-security/concepts/secret-security/push-protection . Accessed 2026-10-31.
  - "Rather than alerting you to credential leaks after the fact, push protection blocks pushes that contain secrets before they reach your repository."
- **GH-DEPENDABOT** — *About Dependabot alerts*, GitHub Docs. https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts . Accessed 2026-10-31.
  - "Dependabot alerts notify you about vulnerable dependencies so you can upgrade to secure versions and protect your project."
- **GH-CODESCAN** — *About code scanning*, GitHub Docs. https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning . Accessed 2026-10-31.
  - "Code scanning is a feature that you use to analyze the code in a GitHub repository to find security vulnerabilities and coding errors."
- **GH-DEPREVIEW** — *About dependency review*, GitHub Docs. https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review . Accessed 2026-10-31.
  - "A failed check blocks a pull request from being merged when the repository owner requires the dependency review check to pass."
- **GH-SENSITIVE** — *Removing sensitive data from a repository*, GitHub Docs. https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository . Accessed 2026-10-31.
  - "if the sensitive data you need to remove is a secret (e.g. password/token/credential), as is often the case, then as a first step you need to revoke and/or rotate that secret."
  - "If a fellow developer has a clone from before your rewrite, and after your rewrite simply runs git pull followed by git push , the sensitive data will return."
- **GH-SECUREUSE** — see Area 8.
- **CS-CICD** — see Area 8.

---

## Area 6: Privacy and data protection

Legal note: the APPI quotes are from the English translation linked by the Personal Information Protection Commission
(PPC), which states that only the Japanese text has legal effect. The English text calls 要配慮個人情報 "sensitive personal
information". GDPR is included as a comparison/baseline, not as law that necessarily applies; applicability is a legal
question for each project.

### Candidate requirements

1. **MUST** — Identify the privacy law(s) that apply to the system (for Japan: APPI; GDPR if EU data subjects are in scope) and record the result and the owner.
   *Evidence:* a privacy/applicability statement in the project docs, reviewed by the organisation's privacy/legal function. *Sources:* APPI (Art. 2, 23), GDPR (Art. 5). [Applicability statement as an artefact: judgement]
2. **MUST** — Keep an inventory of personal data the system handles (fields, purpose, source, where stored, who can access, retention), and classify it, flagging sensitive personal information.
   *Evidence:* data inventory / classification table; matches the schema. *Sources:* ASVS5 (14.1.1), GDPR (Art. 30), APPI (Art. 2(3)).
3. **MUST** — Specify and document the purpose of use for each category of personal data, and do not use data beyond that purpose without consent.
   *Evidence:* purpose column in the inventory; privacy notice text; no feature uses data outside documented purposes. *Sources:* APPI (Art. 17, 18, 21).
4. **MUST** — Collect, process, return and display only the personal data needed for the purpose (minimisation by design and by default).
   *Evidence:* schema/API review shows no unneeded fields; API responses return minimum fields; defaults are least-exposing. *Sources:* GDPR (Art. 5(1)(c), Art. 25), ASVS5 (14.2.6).
5. **MUST** — Define retention for each personal-data category and delete (or anonymise) data when no longer needed, by an automated job or documented procedure.
   *Evidence:* retention schedule; deletion job or runbook; evidence of a run. *Sources:* APPI (Art. 22), GDPR (Art. 5(1)(e)), ASVS5 (14.2.7).
6. **MUST** — Apply security controls proportionate to the data (access control, encryption, logging of access) as part of the APPI security-management duty.
   *Evidence:* control list per data classification; encryption at rest/in transit; access reviews. *Sources:* APPI (Art. 23), GDPR (Art. 32), ASVS5 (14.2.4), PPC-PAW.
7. **SHOULD** — Log access to personal data (at least privileged/bulk access and failed attempts) without writing the personal data itself to the log.
   *Evidence:* audit log entries for admin/bulk reads; log samples free of PII. *Sources:* ASVS5 (16.3.2), CS-LOGGING.
8. **MUST** — Keep personal data out of application logs, URLs/query strings and third-party trackers unless explicitly permitted for that data class.
   *Evidence:* log sampling; URL patterns; analytics configuration review. *Sources:* ASVS5 (14.2.1, 14.2.3, 16.2.5), CS-LOGGING.
9. **MUST** — Do not commit personal data to source repositories (including exports, spreadsheets, fixtures and docs); treat any accidental commit as an incident (remove, and assess history and clones).
   *Evidence:* repo scan for PII patterns; `.gitignore` covers export folders; incident record for any past exposure. *Sources:* GH-SENSITIVE (process), APPI (Art. 23). [Explicit "no PII in repos" rule: judgement — no primary source states it in these words]
10. **MUST** — Use synthetic or anonymised data in development and test; any use of live personal data in pre-production must be approved, documented, and protected to production level.
    *Evidence:* seed/fixture data is synthetic; approval record for any production copy; pre-prod access controls equal to prod. *Sources:* NIST-80053 (SA-3(2)).
11. **MUST** — Supervise everyone who handles the personal data — employees and contractors/vendors (including cloud and AI services) — and record data-handling agreements.
    *Evidence:* access list with role justification; contracts/DPAs with processors; vendor list. *Sources:* APPI (Art. 24, 25, 27, 28), GDPR (Art. 30).
12. **MUST** — Have a breach procedure that meets legal reporting duties (summary, not legal advice: APPI Art. 26 asks for qualifying leaks to be reported to the PPC and individuals to be notified; GDPR Art. 33 sets a deadline for notifying the supervisory authority).
    *Evidence:* incident runbook with privacy branch, contacts and timelines; drill or past record. *Sources:* APPI (Art. 26), GDPR (Art. 33).
13. **SHOULD** — Support data-subject requests (disclosure, correction, cessation of use/deletion) with a documented procedure and tooling.
    *Evidence:* procedure; admin function or script to locate/export/delete one person's data. *Sources:* APPI (Art. 33, 35).
14. **SHOULD** — Carry out a privacy impact assessment before launching processing that is likely high-risk (new technology, sensitive data, large scale, profiling).
    *Evidence:* PIA/DPIA document signed off before go-live. *Sources:* GDPR (Art. 35). [Not an explicit APPI duty — comparison/best practice]
15. **MUST** — Do not paste personal or confidential data into external AI tools/prompts unless the tool is approved for that data class and the use is within the purpose of use.
    *Evidence:* AI usage policy; approved-tools list. *Sources:* APPI (Art. 18, 27, 28) by inference. [judgement — official PPC English text on generative AI not located; cross-reference Area 19]

### Failure modes

- No inventory, so nobody can answer what personal data is held, where, and why, when a request or breach arrives. (ASVS5 14.1.1; GDPR Art. 30)
- Personal-data exports left in the working tree or committed to the repository. (GH-SENSITIVE: history rewrites do not reach old clones.)
- Copying production databases into dev/test without approval or equal protection. (NIST-80053 SA-3(2))
- Logging full request bodies or tokens, so logs become an uncontrolled personal-data store. (CS-LOGGING; ASVS5 16.2.5)
- Keep-everything-forever: no retention or deletion, contrary to APPI Art. 22 and GDPR storage limitation.
- Treating a leak as purely technical and missing the legal reporting duty. (APPI Art. 26; GDPR Art. 33)

### Sources

- **APPI** — *Act on the Protection of Personal Information (Act No. 57 of 2003)*, English translation (Last Version: Act No. 37 of 2021), Japanese Law Translation (Ministry of Justice), linked from the PPC's English "Laws and Policies" page. https://www.japaneselawtranslation.go.jp/en/laws/view/4241/en ; PPC page https://www.ppc.go.jp/en/legal/ . Accessed 2026-10-31.
  - Art. 17(1): "the business handling personal information must specify as much as possible the purpose for which it uses that information"
  - Art. 18(1): "A business handling personal information must not handle personal information beyond the scope necessary for achieving the purpose of use"
  - Art. 22: "delete the personal data without delay if they no longer require it."
  - Art. 23: "Businesses handling personal information must take the necessary and appropriate measures for managing the security of personal data including preventing the leaking, loss or damage of the personal data they handle."
  - Art. 24: "businesses handling personal information must exercise the necessary and adequate supervision over that employee to ensure the secure management of the personal data."
  - Art. 25: "it must exercise the necessary and adequate supervision over the person it entrusts, so as to ensure the secure management of the personal data"
  - Art. 26(1): "businesses handling personal information must report leaks, loss or damage and other situations concerning the security of the personal data they handle"
  - Art. 27(1): "Businesses handling personal information must not provide personal data to a third party without obtaining the identifiable person's consent in advance, except cases set forth below"
  - Art. 2(3) defines sensitive personal information as: "personal information as to an identifiable person's race, creed, social status, medical history, criminal record, the fact of having suffered damage by a crime"
  - PPC page note: "Only the original Japanese texts of the laws and regulations have legal effect, and the translations are to be used solely as reference materials"
- **PPC-PAW** — *Privacy Awareness Week 2024*, Personal Information Protection Commission, Japan. https://www.ppc.go.jp/en/aboutus/roles/international/conferences/PAW2024e/ . Accessed 2026-10-31.
  - "For business operators, please take necessary and appropriate security control measures to prevent leaks of personal information."
  - "Implement appropriate access control."
- **GDPR** — *Regulation (EU) 2016/679 (General Data Protection Regulation)*, OJ L 119, 4.5.2016. Canonical: https://eur-lex.europa.eu/eli/reg/2016/679/oj ; text fetched from the EU Publications Office (EUR-Lex returned a bot challenge): http://publications.europa.eu/resource/celex/32016R0679 . Accessed 2026-10-31.
  - Art. 5(1)(c): "adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed (‘data minimisation’)"
  - Art. 5(1)(e): "kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed"
  - Art. 25(2): "The controller shall implement appropriate technical and organisational measures for ensuring that, by default, only personal data which are necessary for each specific purpose of the processing are processed."
  - Art. 30(1): "Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility."
  - Art. 32(1)(a),(d): "the pseudonymisation and encryption of personal data" ; "a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing."
  - Art. 33(1): "the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority"
  - Art. 35(1): "Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk"
- **NIST-80053** — *NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations*, NIST. https://doi.org/10.6028/NIST.SP.800-53r5 (PDF https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf). Accessed 2026-10-31.
  - SA-3(2): "(a) Approve, document, and control the use of live data in preproduction environments for the system, system component, or system service"
  - SA-3(2): "(b) Protect preproduction environments for the system, system component, or system service at the same impact or classification level as any live data in use within the preproduction environments."
- **ASVS5** — as Area 5 (chapter V14 Data Protection, V16).
  - 14.1.1: "Verify that all sensitive data created and processed by the application has been identified and classified into protection levels."
  - 14.2.1: "the URL and query string do not contain sensitive information, such as an API key or session token."
  - 14.2.3: "Verify that defined sensitive data is not sent to untrusted parties (e.g., user trackers)"
  - 14.2.7: "Verify that sensitive information is subject to data retention classification, ensuring that outdated or unnecessary data is deleted automatically, on a defined schedule, or as the situation requires."
  - 16.3.2: "including logging when sensitive data is accessed (without logging the sensitive data itself)."
- **CS-LOGGING**, **GH-SENSITIVE** — as Area 5.

---

## Area 7: Source control and repository hygiene

### Candidate requirements

1. **MUST** — Keep everything needed to build, test and deploy the system in version control (code, schema migrations, build and pipeline definitions, infrastructure config), and nothing that the build produces.
   *Evidence:* a fresh clone builds with documented commands; no build outputs tracked. *Sources:* FOWLER-CI, SSDF (PS.1.1, PO.3.2).
2. **MUST** — Restrict repository access by least privilege, and review membership periodically.
   *Evidence:* collaborator/team list with roles; access review record. *Sources:* SSDF (PS.1.1).
3. **MUST** — Change the main branch only through pull requests from short-lived branches; delete branches after merge.
   *Evidence:* branch protection/rulesets; commit history shows merge/squash via PRs; count of stale branches. *Sources:* GH-FLOW, DORA-TBD.
4. **MUST** — Protect the main (and release) branches: block force-push and deletion, require PR review approval and passing status checks, and do not let administrators bypass.
   *Evidence:* exported branch protection/ruleset settings; "Do not allow bypassing" enabled; audit log of bypasses. *Sources:* GH-PROTECTED, GH-RULESETS.
5. **MUST** — Require at least one approving review by someone other than the author; dismiss stale approvals when new commits change the diff.
   *Evidence:* ruleset shows required approvals ≥1 and stale-review dismissal (or the setting requiring approval from someone other than the last pusher); sample PRs. *Sources:* GH-PROTECTED, SSDF (PW.7.2 Example 1).
6. **SHOULD** — Maintain a CODEOWNERS file so owners are auto-requested, and require code-owner review for sensitive paths (auth, permissions, CI, infrastructure, migrations).
   *Evidence:* `CODEOWNERS` in `.github/`, root or `docs/`; "Require review from Code Owners" enabled. *Sources:* GH-CODEOWNERS, GH-PROTECTED.
7. **SHOULD** — Provide a PR template (summary, linked issue, test evidence, risk/rollback, security/privacy checklist) and issue templates/forms.
   *Evidence:* `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/`; PRs actually filled in. *Sources:* GH-TEMPLATES, GH-PRTEMPLATE, GH-ISSUEFORMS.
8. **SHOULD** — Document contribution rules (branch naming, commit messages, review expectations, how to run checks locally) in `CONTRIBUTING.md`.
   *Evidence:* `CONTRIBUTING.md` present and current. *Sources:* GH-CONTRIB, GH-FLOW.
9. **MUST** — Commit a `.gitignore` that excludes build outputs, dependencies, local environment files (`.env`), IDE files, logs and data exports; untrack anything already tracked that it should exclude.
   *Evidence:* `.gitignore` present; `git ls-files` shows no `.env`, build outputs, dumps. *Sources:* GIT-IGNORE, GH-IGNORE.
10. **MUST** — Track nothing that should not be there: no secrets, no personal data, no production data dumps, no generated artefacts; verify continuously with scanning (see Areas 5 and 6).
    *Evidence:* secret-scanning results clean; periodic `git ls-files` review. *Sources:* GH-SECRETSCAN, ASVS5 (13.3.1), FOWLER-CI.
11. **SHOULD** — Keep the repository lean: no large binaries in Git (use Git LFS or an artefact store), and keep total size small.
    *Evidence:* repo size; largest-blob report; LFS config if binaries are needed. *Sources:* GH-LARGE.
12. **SHOULD** — Normalise line endings and text attributes via `.gitattributes` so cross-platform edits don't rewrite whole files.
    *Evidence:* `.gitattributes` with `* text=auto` (or explicit rules); no whole-file EOL churn in diffs. *Sources:* GIT-ATTR.
13. **MUST** — Never rewrite history that others may have based work on (shared/protected branches); history rewrites for data removal follow a documented procedure.
    *Evidence:* force-push disabled on protected branches; rewrite incidents documented. *Sources:* PROGIT, GH-PROTECTED, GH-SENSITIVE.
14. **MAY** — Require signed commits on protected branches.
    *Evidence:* "Require signed commits" enabled; commits show Verified. *Sources:* GH-PROTECTED, GH-SIGN, SSDF (PS.1.1, Example 3: "Use commit signing for code repositories.").
15. **SHOULD** — Require all PR conversations to be resolved before merge.
    *Evidence:* ruleset setting; sample PRs. *Sources:* GH-PROTECTED.

### Failure modes

- Branch protection exists but admins can bypass it (the GitHub default), so "required review" is optional in practice. (GH-PROTECTED)
- `.gitignore` added after files were committed; Git keeps tracking them. (GIT-IGNORE: "Files already tracked by Git are not affected")
- Stray exports and scratch files accumulate in the working tree and get committed.
- Long-lived feature branches and many active branches cause painful merges and code freezes. (DORA-TBD)
- Force-pushing or rebasing shared branches, losing others' work. (PROGIT)
- Approved PR changed after approval without re-review ("hijacked" PR). (GH-PROTECTED)

### Sources

- **GH-PROTECTED** — *About protected branches*, GitHub Docs. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches . Accessed 2026-10-31.
  - "can require that all pull requests receive a specific number of approving reviews before someone merges the pull request into a protected branch."
  - "By default, the restrictions of a branch protection rule do not apply to people with admin permissions to the repository"
  - "If you are concerned about pull requests being "hijacked" (where unapproved content is added to approved pull requests), it is safer to dismiss stale reviews."
  - "If you do, any pull request that affects code with a code owner must be approved by that code owner before the pull request can be merged into the protected branch."
  - "By default, each branch protection rule disables force pushes to the matching branches and prevents the matching branches from being deleted."
  - "Requires all comments on the pull request to be resolved before it can be merged to a protected branch."
  - "When you enable required commit signing on a branch, contributors and bots can only push commits that have been signed and verified to the branch."
- **GH-RULESETS** — *About rulesets*, GitHub Docs. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets . Accessed 2026-10-31.
  - "A ruleset is a named list of rules that applies to a repository or to multiple repositories in an organization"
- **GH-CODEOWNERS** — *About code owners*, GitHub Docs. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners . Accessed 2026-10-31.
  - "Code owners are automatically requested for review when someone opens a pull request that modifies code that they own."
  - "create a new file called CODEOWNERS in the .github/ , root, or docs/ directory of the repository"
- **GH-TEMPLATES** — *About issue and pull request templates*, GitHub Docs. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates . Accessed 2026-10-31.
  - "When you add a pull request template to your repository, project contributors will automatically see the template's contents in the pull request body."
- **GH-PRTEMPLATE** — *Creating a pull request template for your repository*, GitHub Docs. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository . Accessed 2026-10-31.
  - "To store your file in a hidden directory, name the pull request template .github/pull_request_template.md ."
- **GH-ISSUEFORMS** — *Configuring issue templates for your repository*, GitHub Docs. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository . Accessed 2026-10-31.
  - "You can encourage contributors to include specific, structured information by using issue forms in your repository."
- **GH-CONTRIB** — *Setting guidelines for repository contributors*, GitHub Docs. https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors . Accessed 2026-10-31.
  - "For the repository owner, contribution guidelines are a way to communicate how people should contribute."
- **GH-FLOW** — *GitHub flow*, GitHub Docs. https://docs.github.com/en/get-started/using-github/github-flow . Accessed 2026-10-31.
  - "A short, descriptive branch name enables your collaborators to see ongoing work at a glance."
  - "After you merge your pull request, delete your branch."
- **GIT-IGNORE** — *gitignore documentation*, Git project. https://git-scm.com/docs/gitignore . Accessed 2026-10-31.
  - "A gitignore file specifies intentionally untracked files that Git should ignore. Files already tracked by Git are not affected"
  - "To stop tracking a file that is currently tracked, use git rm --cached to remove the file from the index."
- **GH-IGNORE** — *Ignoring files*, GitHub Docs. https://docs.github.com/en/get-started/git-basics/ignoring-files . Accessed 2026-10-31.
  - "To share the ignore rules with other users who clone the repository, commit the .gitignore file into your repository."
- **GH-LARGE** — *About large files on GitHub*, GitHub Docs. https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github . Accessed 2026-10-31.
  - "We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended."
  - "GitHub blocks files larger than 100 MiB."
- **GIT-ATTR** — *gitattributes documentation*, Git project. https://git-scm.com/docs/gitattributes . Accessed 2026-10-31.
  - "When text=auto conversion is enabled in a cross-platform project using push and pull to a central repository the text files containing CRLFs should be normalized."
- **PROGIT** — *Pro Git* (2nd ed.), §3.6 "Git Branching – Rebasing", Scott Chacon and Ben Straub. https://git-scm.com/book/en/v2/Git-Branching-Rebasing . Accessed 2026-10-31.
  - "Do not rebase commits that exist outside your repository and that people may have based work on."
- **GH-SIGN** — *About commit signature verification*, GitHub Docs. https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification . Accessed 2026-10-31.
  - "These tags or commits are marked as verified on GitHub so other people can be confident that the changes come from a trusted source."
- **SSDF** — as Area 5.
  - "PS.1.1: Store all forms of code – including source code, executable code, and configuration-as-code – based on the principle of least privilege so that only authorized personnel, tools, services, etc. have access."
- **DORA-TBD** — *Capabilities: Trunk-based development*, DORA (Google Cloud). https://dora.dev/capabilities/trunk-based-development/ . Accessed 2026-10-31.
  - "Have three or fewer active branches in the application’s code repository."
  - "Merge branches to trunk at least once a day."
- **FOWLER-CI**, **GH-SECRETSCAN**, **GH-SENSITIVE**, **ASVS5** — see Areas 5 and 8.

---

## Area 8: Continuous integration

### Candidate requirements

1. **MUST** — Every push and every pull request triggers an automated CI pipeline defined as code in the repository.
   *Evidence:* workflow files (e.g. `.github/workflows/*.yml`) triggered on `push` and `pull_request`; run history for recent PRs. *Sources:* FOWLER-CI, GH-CI, SSDF (PO.3.2 Example 3).
2. **MUST** — The pipeline builds the software and runs the automated test suite; any failing test fails the build.
   *Evidence:* pipeline steps for build + tests; a red run blocks merge. *Sources:* FOWLER-CI, DORA-CI.
3. **MUST** — The pipeline also runs lint/format check and type check for every component, not only tests.
   *Evidence:* pipeline steps per component; no component without a check. *Sources:* SSDF (PW.7.1/PW.7.2 code analysis). [Per-tool enumeration (lint, type-check) is judgement; sources speak of "code analysis"]
4. **MUST** — CI results are required status checks on the protected main branch; a PR cannot merge unless they pass.
   *Evidence:* branch protection lists the required checks; job names unique. *Sources:* GH-STATUS, GH-PROTECTED.
5. **SHOULD** — The pipeline runs security checks on every change: secret detection, SAST, dependency/vulnerability review (and IaC/container scanning where relevant).
   *Evidence:* workflow jobs for these; results visible on PR. *Sources:* CS-CICD, GH-CODESCAN, GH-DEPREVIEW, SSDF (RV.1.2).
6. **MUST** — Keep main green: a broken main build is fixed or the offending change reverted immediately, ahead of other work.
   *Evidence:* main-branch pass rate; time-to-restore after red builds. *Sources:* FOWLER-CI, DORA-CI.
7. **SHOULD** — Keep the commit-stage feedback fast: about 10 minutes or less.
   *Evidence:* median pipeline duration from CI history. *Sources:* FOWLER-CI, DORA-CI.
8. **SHOULD** — Integrate to main at least daily via small PRs.
   *Evidence:* PR age/size metrics; branch age. *Sources:* FOWLER-CI, DORA-TBD, DORA-CI.
9. **SHOULD** — Make CI status visible to the whole team (PR checks, notifications, badge).
   *Evidence:* notification channel or dashboard; badge in README. *Sources:* FOWLER-CI, DORA-CI.
10. **MUST** — Run CI with least privilege: minimal token permissions (read-only by default), secrets scoped to the jobs that need them, never plaintext in workflow files.
    *Evidence:* `permissions:` blocks in workflows; org/repo default token = read; secrets list. *Sources:* GH-SECUREUSE, GH-ACTIONS-SECRETS, CS-CICD.
11. **SHOULD** — Pin third-party CI actions/plugins to an immutable version (full commit SHA) and keep them updated by automation.
    *Evidence:* `uses:` lines pinned to SHAs; Dependabot (or similar) updating actions. *Sources:* GH-SECUREUSE, GH-DEPVER, CS-CICD.
12. **MUST** — Do not run untrusted PR code with privileged triggers or secrets (e.g. `pull_request_target` with checkout of PR head).
    *Evidence:* workflow review; no privileged triggers on untrusted code. *Sources:* GH-SECUREUSE, OWASP-CICD10 (CICD-SEC-4 Poisoned Pipeline Execution).
13. **SHOULD** — Builds are numbered and repeatable, and run in a clean environment from the repository alone.
    *Evidence:* build IDs traceable to commits; pipeline uses clean runners and lockfiles. *Sources:* DORA-CI, FOWLER-CI. (Overlaps Area 9.)
14. **MAY** — Use a merge queue on busy branches so main is never broken by incompatible merges.
    *Evidence:* merge queue enabled; CI triggered on `merge_group`. *Sources:* GH-MERGEQ.
15. **SHOULD** — Keep CI logs and run history for audit, and make each run attributable to who triggered it.
    *Evidence:* retention setting; audit log. *Sources:* CS-SECRETS (CI/CD attribution), SSDF (PO.3.3), OWASP-CICD10 (CICD-SEC-10).

### Failure modes

- CI exists but is not a required check, or admins bypass it, so red code merges anyway. (GH-STATUS; GH-PROTECTED)
- Only one part of a multi-component repository is checked (for example one component is tested, another is never type-checked). [judgement]
- Main stays red for days; "99% green" accepted. (FOWLER-CI: "any test failing is enough to fail the build, 99.9% green is still red.")
- Slow pipelines push developers to batch changes and skip local checks. (DORA-CI; FOWLER-CI ten-minute guideline)
- Over-privileged tokens, unpinned third-party actions and `pull_request_target` misuse turn CI into a supply-chain entry point. (GH-SECUREUSE; OWASP-CICD10)
- Secrets printed to logs (e.g. structured secrets that defeat redaction). (GH-SECUREUSE: "Never use structured data as a secret")

### Sources

- **FOWLER-CI** — *Continuous Integration*, Martin Fowler, martinfowler.com, first published 10 Sep 2000, revised 18 Jan 2024. https://martinfowler.com/articles/continuousIntegration.html . Accessed 2026-10-31.
  - "Continuous Integration is a software development practice where each member of a team merges their changes into a codebase together with their colleagues changes at least daily."
  - "In general we should store in source control everything we need to build anything, but nothing that we actually build."
  - "any test failing is enough to fail the build, 99.9% green is still red."
  - "Continuous Integration can only work if the mainline is kept in a healthy state."
  - "For most projects, however, the XP guideline of a ten minute build is perfectly within reason."
  - "Continuous Integration is all about communication, so we want to ensure that everyone can easily see the state of the system"
- **DORA-CI** — *Capabilities: Continuous integration*, DORA (Google Cloud). https://dora.dev/capabilities/continuous-integration/ . Accessed 2026-10-31.
  - "Each commit should trigger a series of automated tests that provide feedback in a few minutes."
  - "If the build can’t be fixed in a few minutes, the change that caused the build to break should be identified and reverted."
  - "The tests should not take more than a few minutes to run, with an upper limit of about 10 minutes according to DORA’s research (PDF)."
  - "These builds should be numbered and repeatable."
  - "The system should also make the status visible to the team."
- **GH-CI** — *About continuous integration with GitHub Actions*, GitHub Docs. https://docs.github.com/en/actions/get-started/continuous-integration . Accessed 2026-10-31.
  - "When you commit code to your repository, you can continuously build and test the code to make sure that the commit doesn't introduce errors."
- **GH-STATUS** — *About status checks*, GitHub Docs. https://docs.github.com/en/pull-requests/reference/status-checks . Accessed 2026-10-31.
  - "If status checks are required for a protected branch, they must pass before the pull request can be merged."
- **GH-MERGEQ** — *Managing a merge queue*, GitHub Docs. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue . Accessed 2026-10-31.
  - "A merge queue helps increase velocity by automating pull request merges into a busy branch and ensuring the branch is never broken by incompatible changes."
- **GH-SECUREUSE** — *Secure use reference* (formerly titled Security hardening for GitHub Actions), GitHub Docs. https://docs.github.com/en/actions/reference/security/secure-use . Accessed 2026-10-31.
  - "Therefore, you should ensure that the credentials being used within workflows have the least privileges required."
  - "It's good security practice to set the default permission for the GITHUB_TOKEN to read access only for repository contents."
  - "Sensitive data should never be stored as plaintext in workflow files."
  - "Pin references to actions to a commit SHA in your workflow files."
  - "Avoid using the pull_request_target and workflow_run workflow triggers with untrusted pull requests or code content."
- **GH-ACTIONS-SECRETS** — *Using secrets in GitHub Actions*, GitHub Docs. https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets . Accessed 2026-10-31.
  - "This causes the value to be treated as a secret and redacted from logs."
- **GH-DEPVER** — *About Dependabot version updates*, GitHub Docs. https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates . Accessed 2026-10-31.
  - "Dependabot version updates are automated pull requests that keep your dependencies updated, even when they don’t have any vulnerabilities."
- **CS-CICD** — *CI/CD Security Cheat Sheet*, OWASP. https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html . Accessed 2026-10-31.
  - "Incorporate language appropriate SAST, DAST, IaC vulnerability scanning and related tools into the pipeline."
  - "Version pinning should be performed, the version chosen for pinning must be one that is known to be valid and secure"
- **OWASP-CICD10** — *OWASP Top 10 CI/CD Security Risks*, OWASP (project leaders Daniel Krivelevich, Omer Gil). https://owasp.org/www-project-top-10-ci-cd-security-risks/ . Accessed 2026-10-31.
  - "CICD-SEC-4: Poisoned Pipeline Execution (PPE)"
  - "CICD-SEC-10: Insufficient Logging and Visibility"
- **CS-SECRETS** (CI/CD): "Additionally, a CI/CD pipeline run should be easily attributable to the one who has defined the job or triggered it to detect who has tried to exfiltrate secrets or manipulate them."
- **SSDF** (CI/toolchain):
  - "Example 3: Use code-based configuration for toolchains (e.g., pipelines-as-code, toolchains-as-code)." (PO.3.2)
  - "PO.3.3: Configure tools to generate artifacts 6 of their support of secure software development practices as defined by the organization." (the "6" is a footnote marker in the PDF text)
- **DORA-TBD**, **GH-PROTECTED**, **GH-CODESCAN**, **GH-DEPREVIEW** — see Areas 5 and 7.

---

## Gaps (could not source to the standard required)

1. **ISO/IEC 27001:2022** — the iso.org catalogue page returned HTTP 403 to automated fetch; no quote taken. Controls such as 8.4 (access to source code), 8.25 (secure development life cycle), 8.33 (test information) are paywalled; cite the catalogue page manually if wanted.
2. **PPC General Guidelines (security control measures, 講ずべき安全管理措置)** — no official English version of the general (non-sectoral) guidelines was found on ppc.go.jp; only finance-sector English guidelines exist on japaneselawtranslation.go.jp. Detailed APPI security measures therefore rest on Art. 23 plus the PPC PAW page; the Japanese guidelines would need a native-reader citation.
3. **PPC generative-AI alert (June 2023)** — official English text not located on ppc.go.jp (only secondary law-firm summaries, not used). The candidate rule on personal data in AI prompts is marked judgement.
4. **"No personal data in repositories"** — no primary source states this rule directly; it is derived from APPI Art. 23 / GDPR Art. 5(1)(f) and GitHub's removal guidance. Marked judgement.
5. **Lint/type-check as named CI gates** — primary sources speak of code analysis and automated builds and tests; the explicit enumeration is judgement.
6. **CIS benchmarks** (e.g. CIS Software Supply Chain Security Guide) — not fetched; require registration for download.
7. **APPI breach-report thresholds and deadlines** are set in the PPC Enforcement Rules, not the Act. They were not verified and are not stated here; check the PPC Enforcement Rules (https://www.ppc.go.jp/en/legal/) before relying on any deadline.
