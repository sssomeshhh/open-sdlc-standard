# 14. Data lifecycle and integration

- **ID prefix:** DAT
- **Status:** draft, 2026-10-31

## Purpose
Data outlives the code that writes it, and most data defects enter at the edges: imports and integrations that are undocumented,
unvalidated or unsafe to retry, timestamps that are ambiguous, and data that is kept forever because nobody owns it. This area makes
sure each data set has an owner, each integration has a contract, inbound data is validated, retries are safe, time is recorded
unambiguously, and data is kept only as long as it is needed.

## Scope
Covers data ownership, integration and import contracts, validation of inbound data, idempotency, data quality, character
encoding, the date/time and time-zone policy, retention and archiving, safe deletion, integrity checks, and one-off data
migrations and cut-overs.

Left to other areas:
- Schema migrations as part of a release, expand–contract changes and rollback: see Area 11.
- Backups, disaster recovery and tested restores: see Area 12.
- Personal-data classification, minimisation, retention and deletion duties under privacy law: see Area 6. This area sets the
  general rule that every data set has a retention period.
- API and event contracts: see ARC-6 (Area 2). Contracts for file imports, exports and data feeds are set here (DAT-2).
- Display formatting of dates and numbers per locale: see Area 15.

## Requirements

### DAT-1 · MUST · Named data owner
Each data set, including every imported feed, MUST have a named owner, recorded in the data inventory, who is accountable for its
quality, integrity and protection.
- **Gate:** G1 · **Trigger:** each new data set or feed
- **Evidence:** a data inventory listing each table, store or feed with its owner (a role or named person).
- **Basis:** [GOVUK-DOWN]. Level: author's judgement (the source is a government ownership model, not a general mandate).

### DAT-2 · MUST · Written contract for file imports, exports and feeds
Every file import, file export or data feed MUST have a written contract stating format, schema, character encoding, field
meanings, frequency, owner and who to contact on failure, in machine-readable form where possible.
- **Gate:** G1 · **Trigger:** each new file import, file export or data feed
- **Evidence:** for each import, export or feed, the contract in the repository, as a machine-readable schema where possible (for
  example JSON Schema or a CSV specification), naming the owner and the failure contact.
- **Basis:** Author's judgement (no primary source found); the encoding element follows [RFC8259].

### DAT-3 · MUST · Validate inbound data at the trust boundary
Inbound data from any source, internal feeds and partner systems included, MUST be validated for both syntax and meaning against
an allowlist of what is accepted, at the trust boundary, before it is processed or stored.
- **Gate:** G2
- **Evidence:** validation code and tests that include rejected-record cases; an import report listing rejected records and why.
- **Basis:** [OWASP-IV].

### DAT-4 · MUST · Idempotent imports and retryable writes
Imports and any other write that can be retried MUST be idempotent: running the same import or request again has the same effect
as running it once.
- **Gate:** G2
- **Evidence:** a test that runs an import twice and checks the result is unchanged; natural-key upserts or idempotency keys in the
  code.
- **Basis:** [RFC9110]. Level: author's judgement (RFC 9110 defines idempotency for HTTP methods; applying it to imports is an
  extension).

### DAT-5 · MAY · Idempotency keys for non-idempotent HTTP methods
HTTP APIs MAY accept an idempotency key on POST or PATCH requests so clients can retry them safely.
- **Gate:** G2
- **Evidence:** API documentation and tests for repeated requests with the same key.
- **Basis:** [IDEM-DRAFT] (an IETF Internet-Draft, work in progress and not an RFC; the header name and semantics might change).

### DAT-6 · SHOULD · Fix data quality at source
Data-quality problems SHOULD be traced to their root cause and fixed at the source, with the source owner, rather than patched on
every load downstream.
- **Gate:** G3 · **Trigger:** each data-quality problem found
- **Evidence:** issues raised with the source owner; no recurring downstream correction scripts for the same defect.
- **Basis:** [GOVUK-DQ].

### DAT-7 · SHOULD · Measure data quality
Data quality SHOULD be measured against named dimensions (for example completeness, uniqueness, consistency, timeliness, validity
and accuracy), with results reported for each import.
- **Gate:** G3 · **Condition:** once the system imports data from other systems
- **Evidence:** a data-quality check report per import or per period.
- **Basis:** [GOVUK-DQ]. Condition: author's judgement.

### DAT-8 · MUST · UTF-8 for text
Text that the system stores or exchanges with other systems MUST be encoded in UTF-8; legacy encodings are converted at the
boundary.
- **Gate:** G2
- **Evidence:** the encoding stated in each integration contract; database and connection character-set settings; a test with
  non-ASCII input (for example accented or CJK characters).
- **Basis:** [RFC8259], [W3C-ENC]. Applying UTF-8 to all stored and exchanged text, beyond JSON: author's judgement, in line with
  the [W3C-ENC] recommendation (RFC 8259 covers JSON only).

### DAT-9 · MUST · Written date/time policy
The project MUST have a written date/time policy stating that instants are stored and exchanged in UTC, or with an explicit
offset, in the RFC 3339 profile of ISO 8601 as updated by RFC 9557, are converted to local time only for display, and are written
with either `Z` or `+00:00` for UTC (the policy names which).
- **Gate:** G1
- **Evidence:** the policy document, citing RFC 3339 and RFC 9557 and naming the UTC suffix used; database column types (timestamp
  with time zone, or UTC by documented convention); API examples showing timestamps.
- **Basis:** [RFC3339], [RFC9557], [W3C-TZ] (a W3C Group Draft Note, not a W3C Recommendation).
- Note: the policy cites both RFCs because RFC 9557 changes the meaning of the offset `Z`: it now means "UTC known, local offset
  unknown", which RFC 3339 originally wrote as `-00:00`, while `+00:00` keeps the meaning that UTC is the preferred reference point
  (RFC 9557 §2.3).

### DAT-10 · MUST · Time-zone IDs for future and recurring events
Future or recurring events defined in wall-clock time (schedules, calendar entries, publishing times) MUST store the IANA time-zone
ID (for example `Europe/Berlin`), not only a UTC offset.
- **Gate:** G2
- **Evidence:** a time-zone ID field in the schema; recurrence tests that cross a daylight-saving change.
- **Basis:** [W3C-TZ] (Group Draft Note), [RFC9557], [IANA-TZ]. Level: author's judgement (the W3C note recommends it and is a
  draft).

### DAT-11 · SHOULD · Keep the time-zone database current
The time-zone database (tzdata, or the ICU or runtime copy of it) SHOULD be treated as a dependency and updated within a time the
project sets after each new release of the database.
- **Gate:** G2 · **Trigger:** each new release of the time-zone database
- **Evidence:** the tzdata, ICU or runtime version in the lockfile or base image; the update time limit, recorded in the
  dependency update policy (see Area 9).
- **Basis:** [IANA-TZ].

### DAT-12 · MUST · Retention period for every data set
Every data set MUST have a defined retention period at the end of which its data is deleted, anonymised or archived. For
personal data, privacy law can set this duty (example: Japan's APPI Art. 22 asks businesses to endeavour to delete personal data
without delay once it is no longer needed); the personal-data rules are in Area 6.
- **Gate:** G3
- **Evidence:** a retention schedule per data set; the deletion or archiving job and, once it has run, its run logs.
- **Basis:** [APPI-JA] Art. 22 (jurisdiction-specific example; applicability needs legal review). Level: author's judgement for data that
  is not personal data.

### DAT-13 · SHOULD · Soft deletion first
Destructive operations on business data SHOULD use soft or delayed deletion first (a flag or a recovery period) before the data is
removed permanently.
- **Gate:** G3
- **Evidence:** soft-delete columns or a recovery period in the schema; the purge job that ends it.
- **Basis:** [SRE-DI].

### DAT-14 · SHOULD · Out-of-band integrity validation
Stored data SHOULD be checked for integrity drift by scheduled validation jobs that run separately from the application's normal
write path, with alerts on failure.
- **Gate:** G3
- **Evidence:** the validation job, its schedule and its alert rule.
- **Basis:** [SRE-DI].

### DAT-15 · SHOULD · Planned data migrations and cut-overs
One-off data migrations and cut-overs between systems SHOULD have a written plan with reconciliation (record counts or checksums
before and after), a rollback path, and sign-off by the data owner.
- **Gate:** G3 · **Trigger:** each one-off data migration or cut-over between systems
- **Evidence:** the cut-over plan; the reconciliation report; the owner's sign-off.
- **Basis:** Author's judgement (no primary source found); reconciliation is related to the out-of-band validation in [SRE-DI].

## Failure modes
- Timestamps stored as naive local time, so values become ambiguous at daylight-saving changes or across regions [W3C-TZ].
- Treating a fixed offset as a time zone for future events, so recurring events drift when time-zone rules change [W3C-TZ],
  [IANA-TZ].
- Imports that are not idempotent, so a retry after a partial failure duplicates or half-applies data [RFC9110].
- Trusting internal or partner feeds without validation [OWASP-IV].
- Patching bad source data downstream instead of fixing it at source, so the fix has to be repeated on every load [GOVUK-DQ].
- No retention period, so data from old imports, personal data included, is kept forever [APPI-JA] Art. 22.

## References
- **[APPI-JA]** 個人情報の保護に関する法律 (Act on the Protection of Personal Information), Japanese original. e-Gov 法令検索 (法令ID
  415AC0000000057). https://laws.e-gov.go.jp/law/415AC0000000057. Accessed 2026-10-31 via the e-Gov API. Jurisdiction-specific
  example; applicability needs legal review.
  > "個人情報取扱事業者は、利用目的の達成に必要な範囲内において、個人データを正確かつ最新の内容に保つとともに、利用する必要がなくなったときは、当該個人データを遅滞なく消去するよう努めなければならない。" (Art. 22)
- **[GOVUK-DOWN]** "Data ownership model", published 16 April 2026. Government Digital Service, GOV.UK.
  https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model. Accessed 2026-10-31.
  > "A data owner is a senior individual with dedicated accountabilities for data" (introduction)
  > "data owners are accountable for the quality, integrity and protection of their data domain" (Data protection roles)
- **[GOVUK-DQ]** "The Government Data Quality Framework". GOV.UK.
  https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework.
  Accessed 2026-10-31.
  > "There are six core data quality dimensions, as defined by DAMA UK." (Data quality dimensions – how to measure your data quality)
  > "use root cause analysis to solve data quality issues at source, rather than apply temporary fixes" (5.1 Plan for the future)
- **[IANA-TZ]** "Time Zone Database". IANA. https://www.iana.org/time-zones. Accessed 2026-10-31.
  > "contains code and data that represent the history of local time for many representative locations" (introduction)
  > "It is updated periodically to reflect changes made by political bodies" (introduction)
- **[IDEM-DRAFT]** draft-ietf-httpapi-idempotency-key-header-08, *The Idempotency-Key HTTP Header Field*, 22 October 2026. IETF
  HTTPAPI Working Group. https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/. Accessed 2026-10-31.
  Internet-Draft (expires 25 April 2027); work in progress, not an RFC.
  > "The HTTP Idempotency-Key request header field can be used to make non-idempotent HTTP methods such as POST or PATCH fault-tolerant."
- **[OWASP-IV]** "Input Validation Cheat Sheet". OWASP.
  https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html. Accessed 2026-10-31.
  > "Validate data from internal APIs, partner feeds, queues, and stored records when it crosses a trust boundary." (Common Pitfalls)
  > "Validate both syntax (the expected type and format) and semantics (whether the value makes sense for the operation)." (Input Validation Strategies)
  > "Define what the application accepts and reject values outside those rules." (Allowlist vs Denylist)
- **[RFC3339]** RFC 3339, *Date and Time on the Internet: Timestamps*, July 2002. IETF. https://www.rfc-editor.org/rfc/rfc3339.
  Accessed 2026-10-31.
  > "This document defines a date and time format for use in Internet protocols that is a profile of the ISO 8601 standard" (introduction)
  > "The following profile of ISO 8601 [ISO8601] dates SHOULD be used in new protocols on the Internet." (introduction)
- **[RFC8259]** RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*, December 2017. IETF.
  https://www.rfc-editor.org/rfc/rfc8259. Accessed 2026-10-31.
  > "JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8"
- **[RFC9110]** RFC 9110, *HTTP Semantics*, June 2022, §9.2.2. IETF. https://www.rfc-editor.org/rfc/rfc9110. Accessed 2026-10-31.
  > "A request method is considered "idempotent" if the intended effect on the server of multiple identical requests with that method is the same as the effect for a single such request."
- **[RFC9557]** RFC 9557, *Date and Time on the Internet: Timestamps with Additional Information*, April 2024 (Proposed Standard). IETF.
  https://www.rfc-editor.org/rfc/rfc9557. Accessed 2026-10-31.
  > "defines an extension to the timestamp format defined in RFC 3339 for representing additional information, including a time zone" (abstract)
  > "It updates RFC 3339 in the specific interpretation of the local offset Z" (abstract)
  > "If the time in UTC is known, but the offset to local time is unknown, this can be represented with an offset of "Z"." (2.2. Update to RFC 3339)
  > "Note that the semantics of the local offset +00:00 is not updated; this retains the implication that UTC is the preferred reference point for the specified time." (2.3. Notes)
- **[SRE-DI]** "Data Integrity: What You Read Is What You Wrote", *Site Reliability Engineering*, ch. 26. Google.
  https://sre.google/sre-book/data-integrity/. Accessed 2026-10-31.
  > "Soft deletion is the primary defense against developer error and the secondary defense against user error." (Ch. 26, First Layer: Soft Deletion)
  > "Out-of-band data validation is tricky to implement correctly." (Ch. 26, Out-of-band data validation)
- **[W3C-ENC]** "Choosing & applying a character encoding". W3C Internationalization.
  https://www.w3.org/International/questions/qa-choosing-encodings. Accessed 2026-10-31.
  > "Choose UTF-8 for all content and consider converting any content in legacy encodings to UTF-8."
- **[W3C-TZ]** *Working with Time and Timezones*, Group Draft Note, 26 July 2025. W3C Internationalization Working Group.
  https://www.w3.org/TR/timezone/. Accessed 2026-10-31. Draft note; not endorsed by W3C.
  > "When in doubt, use UTC for serializing, storing, and exchanging date and time values." (4.1 Timestamps)
  > "you will need the time zone (and not merely the local time offset) to ensure proper time computation." (4.2.2 Past and Future Events)
  > "Specify the use of IANA time zone IDs in standards, protocols, or document formats as the identifier for time zones." (3.3.3 Time Zone Identifiers)
