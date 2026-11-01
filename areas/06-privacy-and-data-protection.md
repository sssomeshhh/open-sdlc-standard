# 6. Privacy and data protection

- **ID prefix:** PRV
- **Status:** draft, 2026-10-31

## Purpose

This area protects the people whose personal data the system holds, and the organisation from breaching privacy law.
Personal data that nobody has inventoried, that is kept forever, copied into test systems, committed to repositories or
pasted into external AI tools cannot be protected, deleted on request or reported correctly after a leak.

## Scope

Covers applicable law, the personal-data inventory and classification, purpose of use, minimisation, retention and
deletion, protection and access logging of personal data, personal data in logs, repositories, test data and AI
prompts, processors and staff who handle the data, breach reporting, data-subject requests and privacy impact
assessment.

Left to other areas:

- General security controls (authentication, authorisation, secrets, which security events to log): see Area 5.
- Log mechanics and retention of logs: see Area 13. Incident management process: see Area 12.
- Data ownership, import contracts and archiving: see Area 14.
- AI tooling rules and agent configuration: see Area 19 (this area owns only the rule on what data may go into prompts).
- Vendor and third-party risk in general: see Area 20.

**Legal note.** Quotes from Japan's Act on the Protection of Personal Information (APPI) below are from the English
translation. Only the Japanese text has legal effect [PPC-LEGAL]. GDPR is cited as a comparison and baseline, not as law that
necessarily applies; whether any law applies to a project is a question for the organisation's privacy or legal
function. This standard is not legal advice.

## Requirements

### PRV-1 · MUST · Applicable privacy law identified

The project MUST record which privacy laws apply to the system (for example Japan's APPI, or the EU GDPR, whose
territorial scope is set by its Article 3), and who owns compliance.

- **Gate:** G0
- **Evidence:** an applicability statement in the project documentation, naming the laws and the owner, reviewed by the
  organisation's privacy or legal function.
- **Basis:** [APPI], [GDPR] Art. 3. The applicability statement as a document: author's judgement (no primary source found).

### PRV-2 · MUST · Personal-data inventory and classification

The project MUST keep an inventory of the personal data it handles (fields, purpose, source, storage location, who can
access it, retention), classified by protection level, with sensitive personal information flagged.

- **Gate:** G1
- **Evidence:** an inventory table that matches the data schema of the latest release; each field has a classification; sensitive
  categories are marked.
- **Basis:** [ASVS5] 14.1.1, [GDPR] Art. 30(1), [APPI] Art. 2(3).

### PRV-3 · MUST · Purpose of use specified and respected

Personal data MUST be used only within the documented purpose of use for its category, unless a lawful basis such as
consent covers the wider use.

- **Gate:** G3
- **Evidence:** a purpose column in the inventory; a privacy notice; no feature reads personal data for a purpose not
  listed.
- **Basis:** [APPI] Art. 17(1), Art. 18(1).

### PRV-4 · MUST · Data minimisation by design and by default

The system MUST collect, store, return and display only the personal data needed for the documented purpose.

- **Gate:** G2
- **Evidence:** schema and API review shows no fields without a purpose; API responses return only the fields the
  caller needs; default settings expose the least data.
- **Basis:** [GDPR] Art. 5(1)(c), Art. 25(2), [APPI] Art. 18(1).

### PRV-5 · MUST · Retention defined and deletion carried out

Each personal-data category MUST have a defined retention period, after which the data is deleted or anonymised by an
automated job or a documented procedure.

- **Gate:** G3
- **Evidence:** a retention schedule; the deletion job or procedure; once it has run, a record of at least one run.
- **Basis:** [APPI] Art. 22, [GDPR] Art. 5(1)(e), [ASVS5] 14.2.7 (an ASVS Level 3 requirement). APPI Art. 22 is a
  best-efforts duty ("must endeavor"); the fixed retention period and the MUST: author's judgement.

### PRV-6 · MUST · Protection proportionate to the data

Personal data MUST be protected by security measures proportionate to its classification, including access control
and encryption in transit and at rest.

- **Gate:** G3
- **Evidence:** a control list per classification level; encryption settings; access lists for stores holding personal
  data and a record of their review.
- **Basis:** [APPI] Art. 23, [PPC-PAW], [GDPR] Art. 32(1). Encryption at rest as a fixed measure: author's judgement
  (GDPR Art. 32(1) lists encryption as one possible measure).

### PRV-7 · SHOULD · Access to personal data logged

Access to personal data SHOULD be logged (at least privileged and bulk access), without writing the personal data
itself to the log.

- **Gate:** G3 · **Condition:** once the system holds sensitive personal data or personal data about many people
- **Evidence:** audit-log entries for administrative and bulk reads; sampled entries contain identifiers of the actor
  and record, not the data.
- **Basis:** [ASVS5] 16.3.2 (logging of sensitive-data access applies at ASVS Level 3). Condition: author's judgement.

### PRV-8 · MUST · No personal data in logs, URLs or trackers

Personal data MUST NOT be written to application logs, placed in URLs or query strings, or sent to third-party trackers,
unless the inventory explicitly permits it for that data class.

- **Gate:** G3
- **Evidence:** log sampling; review of URL patterns; analytics and tracker configuration review.
- **Basis:** [ASVS5] 14.2.1, 14.2.3, [CS-LOGGING].

### PRV-9 · MUST · No personal data in source control

Personal data (including exports, spreadsheets, office documents, fixtures and documentation containing real people's
data) MUST NOT be committed to source repositories, and any accidental commit is handled as a privacy incident.

- **Gate:** G1 · **Trigger:** each accidental commit of personal data
- **Evidence:** a scan of the repository and its history for personal-data patterns; ignore rules covering export
  folders (see Area 7); an incident record for each past exposure.
- **Basis:** [GH-SENSITIVE] for removal and its limits; [APPI] Art. 23 for the underlying security
  duty. The explicit rule: author's judgement (no primary source found).

### PRV-10 · MUST · Synthetic or anonymised test data

Development and test environments MUST use synthetic or anonymised data, except where a documented approval covers a
specific use of live personal data. Protecting such an environment: see PRV-16.

- **Gate:** G1 · **Trigger:** each use of live personal data in a development or test environment
- **Evidence:** seed and fixture data is synthetic; an approval record for each use of a production copy.
- **Basis:** [SP800-53] SA-3(2) (a). Applying it to every project: author's judgement (SA-3(2) is an optional control
  enhancement).

### PRV-11 · MUST · No personal or confidential data in AI prompts

Personal or confidential data MUST NOT be entered into AI tools (prompts, uploaded files or agent context) unless the
tool is approved for that data class and the use is within the documented purpose.

- **Gate:** G1
- **Evidence:** an AI usage policy naming approved tools per data class; where the tool supports it, configuration that
  excludes sensitive files from AI context (see Area 19 for tooling rules).
- **Basis:** [OWASP-LLM02], [AI600], [GH-EXCL]; [APPI] Art. 18(1), Art. 27(1) by inference: whether sending data to an
  AI service is provision to a third party or entrustment needs legal review. Level: author's judgement (sources
  support SHOULD).

### PRV-12 · MUST · Staff and processors supervised

Everyone who handles the personal data (employees, contractors and entrusted service providers, including cloud and AI
services) MUST be under documented supervision: access with a role justification, and a data-handling agreement with
each external party.

- **Gate:** G3 · **Trigger:** each new person or external service given access to the personal data
- **Evidence:** an access list with role justification; contracts or data-processing agreements with each processor; a
  list of external services that receive personal data.
- **Basis:** [APPI] Art. 24, Art. 25, Art. 27(5)(i), [GDPR] Art. 28(3).

### PRV-13 · MUST · Breach procedure that meets reporting duties

The project MUST have a breach procedure that meets the legal duties to report leaks to the authority and notify
affected people.

- **Gate:** G3 · **Trigger:** each personal-data breach
- **Evidence:** an incident runbook with a privacy branch, contacts and deadlines confirmed by the privacy or legal
  function; a drill or past record.
- **Basis:** [APPI] Art. 26(1), 26(2), [GDPR] Art. 33(1), Art. 34(1). Both laws limit these duties to defined
  situations (APPI: those prescribed by PPC order; GDPR Art. 34: likely high risk). APPI reporting deadlines are set in
  subordinate rules not quoted here; confirm them before writing them into the runbook.

### PRV-14 · MUST · Data-subject requests supported

The project MUST have a documented procedure and tooling to find, disclose, correct, stop using and delete one
person's data on request, within the time the applicable law sets.

- **Gate:** G3 · **Trigger:** each data-subject request
- **Evidence:** the procedure; an admin function or script that locates and exports or deletes a single person's data.
- **Basis:** [APPI] Art. 33(1)–(2) (disclosure), Art. 34(1) (correction), Art. 35(1) (ceasing use or deletion, where the
  data is handled in breach of the Act). The procedure and tooling as the means of meeting these duties: author's judgement.

### PRV-15 · SHOULD · Privacy impact assessment for high-risk processing

A privacy impact assessment SHOULD be carried out and signed off before launching processing likely to be high-risk
(new technology, sensitive data, large scale, profiling).

- **Gate:** G3 · **Trigger:** each new processing likely to be high-risk
- **Evidence:** a signed-off assessment dated before go-live.
- **Basis:** [GDPR] Art. 35(1). Not an explicit APPI duty in the quoted text; comparison baseline.

### PRV-16 · MUST · Pre-production holding live personal data protected like production

A development or test environment that holds live personal data MUST be protected at the same level as production.

- **Gate:** G2 · **Trigger:** each time live personal data is placed in a development or test environment
- **Evidence:** access controls, encryption and logging settings of that environment match production's.
- **Basis:** [SP800-53] SA-3(2) (b).

## Failure modes

- No inventory, so nobody can say what personal data is held, where and why when a request or breach arrives. [ASVS5],
  [GDPR]
- Personal-data exports left in the working tree or committed to the repository; history rewrites do not reach old
  clones. [GH-SENSITIVE]
- Production databases copied into development or test without approval or equal protection. [SP800-53]
- Full request bodies or tokens logged, so logs become an uncontrolled personal-data store. [CS-LOGGING]
- Keep everything forever: no retention period and no deletion, contrary to GDPR storage limitation and short of
  APPI's best-efforts duty to delete data no longer needed. [GDPR], [APPI]
- A leak treated as purely technical, missing the legal reporting duty. [APPI], [GDPR]

## References

- **[AI600]** NIST AI 600-1, Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence
  Profile. NIST, July 2024. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf . Accessed 2026-10-31.
  > "Impacts due to leakage and unauthorized use, disclosure, or de-anonymization of biometric, health, location, or other personally identifiable information or sensitive data."
- **[APPI]** Act on the Protection of Personal Information (Act No. 57 of 2003), English translation (last version: Act
  No. 37 of 2021). Japanese Law Translation (Ministry of Justice), linked from the Personal Information Protection
  Commission (PPC). https://www.japaneselawtranslation.go.jp/en/laws/view/4241/en ; PPC page
  https://www.ppc.go.jp/en/legal/ . Accessed 2026-10-31.
  > "personal information as to an identifiable person's race, creed, social status, medical history, criminal record, the fact of having suffered damage by a crime" (Art. 2)

  > "the business handling personal information must specify as much as possible the purpose for which it uses that information" (Art. 17)

  > "A business handling personal information must not handle personal information beyond the scope necessary for achieving the purpose of use" (Art. 18)

  > "An identifiable person may request that a business handling personal information disclose personal data the business holds that can identify that person" (Art. 33)

  > "When having received a request under the preceding paragraph, a business handling personal information must disclose personal data the business holds to an identifiable person without delay" (Art. 33)

  > "the person may request that the business handling personal information make a correction, addition, or deletion" (Art. 34)

  > "Identifiable persons may request that a business handling personal information cease to use or delete the personal data the business holds that can be used to identify that person" (Art. 35)

  > "must endeavor to keep the content of personal data accurate and up to date, within the scope necessary for achieving the purpose of use, and delete the personal data without delay if they no longer require it." (Art. 22)

  > "Businesses handling personal information must take the necessary and appropriate measures for managing the security of personal data including preventing the leaking, loss or damage of the personal data they handle." (Art. 23)

  > "businesses handling personal information must exercise the necessary and adequate supervision over that employee to ensure the secure management of the personal data." (Art. 24)

  > "it must exercise the necessary and adequate supervision over the person it entrusts, so as to ensure the secure management of the personal data" (Art. 25)

  > "businesses handling personal information must report leaks, loss or damage and other situations concerning the security of the personal data they handle" (Art. 26)

  > "In cases prescribed in the preceding paragraph, businesses handling personal information (excluding those that have given a notice under the proviso of that paragraph) must notify the identifiable person of the occurrence of the situation" (Art. 26)

  > "Businesses handling personal information must not provide personal data to a third party without obtaining the identifiable person's consent in advance, except cases set forth below" (Art. 27)

  > "In the following cases, a person receiving personal data is not to fall under a third party … (i) the businesses handling personal information entrusts a person with all or part of the handling of personal data within the scope necessary for achieving the purpose of use" (Art. 27)
- **[ASVS5]** OWASP Application Security Verification Standard 5.0.0. OWASP Foundation, 30 May 2025.
  https://github.com/OWASP/ASVS/tree/master/5.0/en . Accessed 2026-10-31.
  > "Verify that all sensitive data created and processed by the application has been identified and classified into protection levels." (V14.1 Data Protection Documentation)

  > "the URL and query string do not contain sensitive information, such as an API key or session token." (V14.2 General Data Protection)

  > "Verify that defined sensitive data is not sent to untrusted parties (e.g., user trackers)" (V14.2 General Data Protection)

  > "Verify that sensitive information is subject to data retention classification, ensuring that outdated or unnecessary data is deleted automatically, on a defined schedule, or as the situation requires." (V14.2 General Data Protection)

  > "including logging when sensitive data is accessed (without logging the sensitive data itself)." (V16.3 Security Events)
- **[CS-LOGGING]** Logging Cheat Sheet. OWASP Cheat Sheet Series.
  https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . Accessed 2026-10-31. The item after the
  sentence is quoted from the list that follows it.
  > "The following should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted:" (Data to exclude)
  > "Sensitive personal data and some forms of personally identifiable information (PII) e.g. health, government identifiers, vulnerable people" (Data to exclude)
- **[GDPR]** Regulation (EU) 2016/679 (General Data Protection Regulation), OJ L 119, 4.5.2016.
  https://eur-lex.europa.eu/eli/reg/2016/679/oj (text as fetched from
  http://publications.europa.eu/resource/celex/32016R0679). Accessed 2026-10-31.
  > "This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not." (Art. 3)

  > "adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed (‘data minimisation’)" (Art. 5)

  > "kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed" (Art. 5)

  > "The controller shall implement appropriate technical and organisational measures for ensuring that, by default, only personal data which are necessary for each specific purpose of the processing are processed." (Art. 25)

  > "Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility." (Art. 30)

  > "the pseudonymisation and encryption of personal data" (Art. 32)

  > "the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority" (Art. 33)

  > "When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay." (Art. 34)

  > "Processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller" (Art. 28)

  > "Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk" (Art. 35)
- **[GH-EXCL]** Content exclusion for GitHub Copilot. GitHub Docs.
  https://docs.github.com/en/copilot/concepts/context/content-exclusion . Accessed 2026-10-31.
  > "You can use content exclusion to configure Copilot to ignore certain files." (About content exclusion for Copilot)

  > "Content exclusion is a guardrail for the tools that GitHub controls." (Limitations of content exclusion)
- **[GH-SENSITIVE]** Removing sensitive data from a repository. GitHub Docs.
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository .
  Accessed 2026-10-31.
  > "If a fellow developer has a clone from before your rewrite, and after your rewrite simply runs git pull followed by git push , the sensitive data will return."
- **[OWASP-LLM02]** LLM02:2025 Sensitive Information Disclosure, OWASP Top 10 for LLM Applications 2025. OWASP GenAI
  Security Project. https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ . Accessed 2026-10-31.
  > "Provide guidance on avoiding the input of sensitive information." (1. Educate Users on Safe LLM Usage)

  > "such restrictions may not always be honored and could be bypassed via prompt injection or other methods." (introduction)
- **[PPC-LEGAL]** Laws and Policies. Personal Information Protection Commission, Japan. https://www.ppc.go.jp/en/legal/ .
  Accessed 2026-10-31.
  > "Only the original Japanese texts of the laws and regulations have legal effect, and the translations are to be used solely as reference materials to aid in the understanding of Japanese laws and regulations."
- **[PPC-PAW]** Privacy Awareness Week 2024. Personal Information Protection Commission, Japan.
  https://www.ppc.go.jp/en/aboutus/roles/international/conferences/PAW2024e/ . Accessed 2026-10-31.
  > "For business operators, please take necessary and appropriate security control measures to prevent leaks of personal information." (Message from the Chairperson of the PPC Japan)

  > "Implement appropriate access control." (Message from the Chairperson of the PPC Japan)
- **[SP800-53]** NIST SP 800-53 Rev. 5, Security and Privacy Controls for Information Systems and Organizations. NIST.
  https://doi.org/10.6028/NIST.SP.800-53r5 . Accessed 2026-10-31.
  > "(a) Approve, document, and control the use of live data in preproduction environments for the system, system component, or system service" (SA-3)

  > "(b) Protect preproduction environments for the system, system component, or system service at the same impact or classification level as any live data in use within the preproduction environments." (SA-3)
