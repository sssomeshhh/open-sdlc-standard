# Research D: areas 13–16

- **Scope:** 13 Observability and telemetry; 14 Data lifecycle and integration; 15 User experience; 16 Documentation and knowledge management.
- **Accessed:** all sources 2026-10-31.
- **Method:** each page was fetched, and every quotation below was checked word for word against the fetched page text with a string match (curl + script). Differences are limited to whitespace and the page's own curly quotes. Laws were checked against the e-Gov 法令 API XML.
- **Labels:** "[judgement]" marks a requirement with no source behind it; "[inference]" marks a conclusion drawn from sources that do not state it directly.

---

## Area 13: Observability and telemetry

### Candidate requirements

1. **MUST**: The service emits the three core telemetry signals (logs, metrics, traces), or records why one is not needed. *Evidence:* instrumentation code or config; a sample of each signal from production. *Sources:* OTEL-PRIMER.
2. **MUST**: Logs are written as a structured, time-ordered event stream to stdout/stderr or a collector, not to files the app manages itself. *Evidence:* logger config; one JSON/key-value log line; no log rotation code in the app. *Sources:* 12F-LOGS, OTEL-LOGS.
3. **MUST**: Every user-facing service measures the four golden signals: latency (with percentiles, not only averages), traffic, errors and saturation. *Evidence:* a dashboard or metric list showing all four; latency shown as p50/p95/p99. *Sources:* SRE-MON.
4. **MUST**: Every alert that pages a human is actionable and is tied to a symptom users feel, or to an SLO burn rate. *Evidence:* alert rules; each one linked to a runbook entry; a page history showing no recurring alerts that need no action. *Sources:* SRE-MON, SRE-ALERT.
5. **SHOULD**: Alerting on SLOs uses error-budget burn rates over more than one window, and alert precision and recall are reviewed. *Evidence:* burn-rate alert definitions; a review record. *Sources:* SRE-ALERT.
6. **MUST**: Security-relevant events are logged with when, where, who and what: authentication successes and failures, authorisation failures and input-validation failures. *Evidence:* the logging spec or code; sample entries for a failed login and a denied access. *Sources:* OWASP-LOG, NIST-92.
7. **MUST**: Logs and telemetry exclude passwords, session tokens and unneeded personal data (mask or hash them), and instrumentation libraries are reviewed for what they collect. *Evidence:* redaction config or tests; a grep of a log sample shows no tokens or e-mail addresses unless justified. *Sources:* OWASP-LOG, OTEL-SENS.
8. **MUST**: Clocks are synchronised and timestamps use an unambiguous international format with offset or UTC. *Evidence:* NTP/time-sync config; log timestamps in RFC 3339 form. *Sources:* OWASP-LOG, RFC3339 (Area 14).
9. **SHOULD**: Request context (trace ID) is propagated across service boundaries with W3C Trace Context and written into every log record, so logs and traces can be correlated. *Evidence:* a `traceparent` header on outbound calls; a log line carrying `trace_id`. *Sources:* W3C-TC, OTEL-LOGS.
10. **SHOULD**: Attribute and metric names follow OpenTelemetry semantic conventions, or one documented naming scheme. *Evidence:* attribute names in emitted data (e.g. `http.request.method`); a naming doc. *Sources:* OTEL-SEMCONV.
11. **MUST**: Audit and security logs are protected from tampering and have restricted, reviewed read access, with a defined retention period. *Evidence:* storage settings (write-once storage or tamper detection); IAM policy; a retention value in config. *Sources:* OWASP-LOG, NIST-92.
12. **SHOULD**: The organisation has a written log-management plan saying which logs are kept, where, for how long and who reviews them. *Evidence:* the plan document. *Sources:* NIST-92, NIST-92R1.
13. **SHOULD**: Product/usage telemetry measures the outcomes in the success criteria (KPIs), and the team uses it to decide changes. *Evidence:* a metric definition per KPI; a dashboard; decisions that cite the data. *Sources:* GOVUK-P10.
14. **MUST**: Usage telemetry follows data minimisation, and where users' terminals send data to third parties (analytics tags), the legally required notice or consent is given (in Japan, the 電気通信事業法 external-transmission rule, *where it applies*). *Evidence:* the analytics data inventory; a privacy notice; a consent mechanism where required. *Sources:* OTEL-SENS, SOUMU-GAIBU. Whether the rule applies to a given product is an [inference] that needs legal confirmation.
15. **SHOULD**: Dashboards answer basic service questions (golden signals first) and are kept as code or exported config. *Evidence:* the dashboard definition in the repository. *Sources:* SRE-MON; "as code" is [judgement].

### Failure modes

- Paging on causes (CPU, a single host) rather than symptoms, which produces alert fatigue and pages that need no action (SRE-MON: "Every page should be actionable.").
- Reporting average latency only, which hides tail latency (SRE-MON: "hopeful thinking").
- Logs from separate components with no shared request ID, which cannot be correlated (OTEL-LOGS).
- Tokens, passwords or personal data written into logs or traces, including by third-party instrumentation (OWASP-LOG, OTEL-SENS).
- Audit logs kept in the same writable store that the application and its admins can change, so tampering cannot be detected (OWASP-LOG).
- Usage analytics added with no KPI behind it, or with no privacy notice (GOVUK-P10, SOUMU-GAIBU).

### Sources

- **SRE-MON**: "Monitoring Distributed Systems", *Site Reliability Engineering* (Google, O'Reilly 2016), ch. 6. https://sre.google/sre-book/monitoring-distributed-systems/ (accessed 2026-10-31)
  - "If you can only measure four metrics of your user-facing system, focus on these four."
  - "Every page should be actionable." / "Every page response should require intelligence."
  - "Your monitoring system should address two questions: what's broken, and why?"
  - "the idea that most of your requests are near the mean is just hopeful thinking"
  - "Dashboards should answer basic questions about your service, and normally include some form of the four golden signals"
- **SRE-ALERT**: "Alerting on SLOs", *The Site Reliability Workbook* (Google), ch. 5. https://sre.google/workbook/alerting-on-slos/ (accessed 2026-10-31)
  - Precision: "The proportion of events detected that were significant." Recall: "The proportion of significant events detected."
  - "We have found that alerting based on multiple burn rates is a powerful way to implement SLO-based alerting."
- **OTEL-PRIMER**: "Observability primer", OpenTelemetry (CNCF). https://opentelemetry.io/docs/concepts/observability-primer/ (accessed 2026-10-31)
  - "Observability lets you understand a system from the outside by letting you ask questions about that system without knowing its inner workings."
  - "To ask those questions about your system, your application must be properly instrumented."
- **OTEL-SEMCONV**: "Semantic Conventions", OpenTelemetry. https://opentelemetry.io/docs/concepts/semantic-conventions/ (accessed 2026-10-31)
  - Semantic conventions "specify common names for different kinds of operations and data."
  - "The benefit of using Semantic conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms."
- **OTEL-LOGS**: "OpenTelemetry Logging" (specification), OpenTelemetry. https://opentelemetry.io/docs/specs/otel/logs/ (accessed 2026-10-31)
  - "OpenTelemetry extends this practice to logs where possible by including TraceId and SpanId in the LogRecords."
  - "This makes it nearly impossible to perform trace context correlation for system logs."
- **OTEL-SENS**: "Handling sensitive data", OpenTelemetry. https://opentelemetry.io/docs/security/handling-sensitive-data/ (accessed 2026-10-31)
  - "you are responsible for understanding and reviewing the telemetry data emitted by any instrumentation libraries you use"
  - "Only collect data that serves an observability purpose."
- **12F-LOGS**: "XI. Logs", The Twelve-Factor App (Adam Wiggins). https://12factor.net/logs (accessed 2026-10-31)
  - "Logs are the stream of aggregated, time-ordered events"
  - "A twelve-factor app never concerns itself with routing or storage of its output stream."
- **W3C-TC**: *Trace Context*, W3C Recommendation, 23 November 2021. https://www.w3.org/TR/trace-context/ (accessed 2026-10-31)
  - "This specification defines standard HTTP headers and a value format to propagate context information"
- **OWASP-LOG**: "Logging Cheat Sheet", OWASP Cheat Sheet Series. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html (accessed 2026-10-31)
  - Events to log include "Authentication successes and failures" and "Authorization (access control) failures".
  - Data to exclude includes "Session identification values" and "Sensitive personal data and some forms of personally identifiable information (PII)".
  - "Synchronize time across all servers and devices"; "Log date and time (international format)"
  - "Build in tamper detection so you know if a record has been modified or deleted"
- **NIST-92**: NIST SP 800-92, *Guide to Computer Security Log Management*, September 2006 (final). https://csrc.nist.gov/pubs/sp/800/92/final (accessed 2026-10-31)
  - "This publication seeks to assist organizations in understanding the need for sound computer security log management."
- **NIST-92R1**: NIST SP 800-92 Rev. 1 (Initial Public Draft), *Cybersecurity Log Management Planning Guide*, 11 October 2023. https://csrc.nist.gov/pubs/sp/800/92/r1/ipd (accessed 2026-10-31). Still a draft; not final.
  - "This document defines a playbook intended to help any organization plan improvements to its cybersecurity log management."
- **GOVUK-P10**: "10. Define what success looks like and publish performance data", GOV.UK Service Standard (GDS). https://www.gov.uk/service-manual/service-standard/point-10-define-success-publish-performance-data (accessed 2026-10-31)
  - Service teams should "identify metrics which will indicate how well the service is solving the problem it's meant to solve"
  - and "use performance data to make decisions about how to fix problems and improve the service"
- **SOUMU-GAIBU**: 「外部送信規律」, 総務省. https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu.html (accessed 2026-10-31)
  - 「電気通信事業を営む者（ウェブサイト運営者、アプリケーション提供者等）は、利用者の端末に外部送信を指示するプログラムを送る際は、あらかじめ、送信される利用者に関する情報の内容等を、通知・公表（利用者が容易に知り得る状態に置く）等しなければなりません。」
  - Effective date given on the page: 「改正電気通信事業法の施行（2023年6月16日）」

---

## Area 14: Data lifecycle and integration

### Candidate requirements

1. **MUST**: Each data set (including every imported feed) has a named owner who is accountable for its quality, and the owner is recorded. *Evidence:* a data inventory with owner per table/feed. *Sources:* GOVUK-DOWN.
2. **MUST**: Every integration or import has a written contract: format, schema, encoding, field meanings, frequency, and who to call on failure. *Evidence:* the contract doc or a machine-readable schema (OpenAPI/JSON Schema/CSV spec) in the repository. *Sources:* [judgement]; encoding part from RFC8259.
3. **MUST**: Inbound data from any source, internal feeds included, is validated for both syntax and meaning at the trust boundary, before business processing or storage, using an allowlist of what is accepted. *Evidence:* validation code and tests with rejected-record cases; an import report listing rejected rows. *Sources:* OWASP-IV.
4. **MUST**: Imports and other retryable writes are idempotent: re-running the same import or request has the same effect as running it once. *Evidence:* a test that runs the import twice and checks the result; idempotency keys or natural-key upserts. *Sources:* RFC9110, IDEM-DRAFT.
5. **SHOULD**: Data-quality issues are fixed at source (with the supplier), not patched downstream, and are measured on named dimensions (completeness, uniqueness, consistency, timeliness, validity, accuracy). *Evidence:* a data-quality check report; issues raised with the source owner. *Sources:* GOVUK-DQ.
6. **MUST**: Text data exchanged between systems is UTF-8. *Evidence:* encoding declared in the contract; a test with non-ASCII input (for example accented or CJK characters). *Sources:* RFC8259, W3C-ENC (Area 15).
7. **MUST**: The project has a written date/time policy: instants are stored and exchanged in UTC (or with an explicit offset) in RFC 3339 / ISO 8601 form; local time only at display. *Evidence:* the policy; DB column types (timestamp with time zone or UTC by convention); API examples. *Sources:* RFC3339, W3C-TZ.
8. **MUST**: Future or recurring wall-clock events (schedules, calendars) store the IANA time zone ID (e.g. `Europe/Berlin`), not only an offset. *Evidence:* schema has a tz-ID field; recurrence tests across a DST change. *Sources:* W3C-TZ, RFC9557, IANA-TZ.
9. **SHOULD**: The time-zone database (tzdata) is kept up to date as a dependency. *Evidence:* the tzdata/ICU version in the lockfile or base image, with an update policy. *Sources:* IANA-TZ.
10. **MUST**: Every personal-data set has a retention period, and data is deleted or anonymised when it is no longer needed (in Japan, APPI Art. 22 states this as a duty to *endeavour*, 努めなければならない). *Evidence:* a retention schedule; a deletion job and its logs. *Sources:* APPI-22.
11. **MUST**: Schema and data changes are made only by version-controlled migrations kept with the application code, tested against realistic data. *Evidence:* a migrations folder; CI runs the migrations on a copy or a seeded DB. *Sources:* FOWLER-EVODB.
12. **SHOULD**: Breaking schema changes go through a transition phase (expand–contract) where old and new access patterns both work. *Evidence:* a migration pair, or an ADR describing the transition. *Sources:* FOWLER-EVODB.
13. **SHOULD**: Destructive operations use soft or lazy deletion first, and backups are proven by tested restores. *Evidence:* soft-delete columns or a recycle period; a restore-test record. *Sources:* SRE-DI.
14. **SHOULD**: Data migrations and cut-overs have a written plan with reconciliation (counts or checksums before and after), a rollback path and sign-off by the data owner. *Evidence:* the cut-over plan; the reconciliation report. *Sources:* [judgement], partly SRE-DI (out-of-band validation).
15. **SHOULD**: Stored data is checked out-of-band (scheduled validation jobs) for integrity drift. *Evidence:* a validation job and its alerts. *Sources:* SRE-DI.

### Failure modes

- Timestamps stored as naive local time, so values become ambiguous at DST changes or across regions (W3C-TZ).
- Treating a fixed offset as a time zone for future events, so recurring events drift when rules change (W3C-TZ, IANA-TZ).
- Imports that are not idempotent, so a retry after a partial failure duplicates or half-applies data (RFC9110).
- Trusting internal or partner feeds without validation (OWASP-IV: "partner feeds").
- Patching bad source data downstream instead of fixing it at source, so the fix must be repeated on every load (GOVUK-DQ).
- No retention period: personal data from old imports is kept forever (APPI-22).
- Ad-hoc manual SQL in production in place of migrations (FOWLER-EVODB).

### Sources

- **RFC3339**: RFC 3339, *Date and Time on the Internet: Timestamps*, IETF, July 2002. https://www.rfc-editor.org/rfc/rfc3339 (accessed 2026-10-31)
  - "This document defines a date and time format for use in Internet protocols that is a profile of the ISO 8601 standard"
  - "The following profile of ISO 8601 dates SHOULD be used in new protocols on the Internet."
- **RFC9557**: RFC 9557, *Date and Time on the Internet: Timestamps with Additional Information*, IETF (Proposed Standard, 2024). https://www.rfc-editor.org/rfc/rfc9557 (accessed 2026-10-31)
  - It "defines an extension to the timestamp format defined in RFC 3339 for representing additional information, including a time zone"
  - "It updates RFC 3339 in the specific interpretation of the local offset Z"
  - Revised RFC 3339 §4.3: "If the time in UTC is known, but the offset to local time is unknown, this can be represented with an offset of "Z"." RFC 3339's original "-00:00" convention is therefore superseded, and a policy should cite both RFCs.
- **W3C-TZ**: *Working with Time and Timezones*, W3C Internationalization WG, Group Draft Note, 26 July 2025. https://www.w3.org/TR/timezone/ (accessed 2026-10-31). A Group Draft Note: not endorsed by W3C itself.
  - "When in doubt, use UTC for serializing, storing, and exchanging date and time values."
  - "you will need the time zone (and not merely the local time offset) to ensure proper time computation."
  - "Specify the use of IANA time zone IDs in standards, protocols, or document formats as the identifier for time zones."
- **IANA-TZ**: "Time Zone Database", IANA. https://www.iana.org/time-zones (accessed 2026-10-31)
  - It "contains code and data that represent the history of local time for many representative locations"
  - "It is updated periodically to reflect changes made by political bodies"
- **RFC8259**: RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*, IETF, December 2017. https://www.rfc-editor.org/rfc/rfc8259 (accessed 2026-10-31)
  - "JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8"
- **RFC9110**: RFC 9110, *HTTP Semantics*, IETF, June 2022, §9.2.2. https://www.rfc-editor.org/rfc/rfc9110 (accessed 2026-10-31)
  - "A request method is considered "idempotent" if the intended effect on the server of multiple identical requests with that method is the same as the effect for a single such request."
- **IDEM-DRAFT**: draft-ietf-httpapi-idempotency-key-header-08, *The Idempotency-Key HTTP Header Field*, IETF HTTPAPI WG, 22 October 2026 (Internet-Draft, expires 25 April 2027; work in progress, not an RFC). https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (accessed 2026-10-31)
  - "The HTTP Idempotency-Key request header field can be used to make non-idempotent HTTP methods such as POST or PATCH fault-tolerant."
- **OWASP-IV**: "Input Validation Cheat Sheet", OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html (accessed 2026-10-31)
  - "Validate data from internal APIs, partner feeds, queues, and stored records when it crosses a trust boundary."
  - "Validate both syntax (the expected type and format) and semantics (whether the value makes sense for the operation)."
  - "Define what the application accepts and reject values outside those rules."
- **GOVUK-DOWN**: "Data ownership model", GDS, GOV.UK, published 16 April 2026. https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model (accessed 2026-10-31)
  - "A data owner is a senior individual with dedicated accountabilities for data"
  - "data owners are accountable for the quality, integrity and protection of their data domain"
- **GOVUK-DQ**: "The Government Data Quality Framework", GOV.UK. https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework (accessed 2026-10-31)
  - "There are six core data quality dimensions, as defined by DAMA UK."
  - "use root cause analysis to solve data quality issues at source, rather than apply temporary fixes"
- **APPI-22**: 個人情報の保護に関する法律 第二十二条, e-Gov 法令検索 (法令ID 415AC0000000057). https://laws.e-gov.go.jp/law/415AC0000000057 (accessed 2026-10-31 via the e-Gov API)
  - 「個人情報取扱事業者は、利用目的の達成に必要な範囲内において、個人データを正確かつ最新の内容に保つとともに、利用する必要がなくなったときは、当該個人データを遅滞なく消去するよう努めなければならない。」
- **FOWLER-EVODB**: Pramod Sadalage and Martin Fowler, "Evolutionary Database Design", martinfowler.com. https://martinfowler.com/articles/evodb.html (accessed 2026-10-31)
  - "Other than updates to the database that occur due to the application software, all changes are made by migrations."
  - "A transition phase is a period of time when the database supports both the old access pattern and the new ones simultaneously"
- **SRE-DI**: "Data Integrity: What You Read Is What You Wrote", *Site Reliability Engineering* (Google), ch. 26. https://sre.google/sre-book/data-integrity/ (accessed 2026-10-31)
  - "No one really wants to make backups; what people really want are restores."
  - "Soft deletion is the primary defense against developer error and the secondary defense against user error."
  - "Out-of-band data validation is tricky to implement correctly."

---

## Area 15: User experience

### Candidate requirements

1. **MUST**: Web UIs conform to WCAG 2.2 Level AA (in Japan, also state conformance against JIS X 8341-3; see the status note under JIS-WAIC). *Evidence:* an accessibility conformance report or statement with test date, scope and results. *Sources:* WCAG22, GOVUK-ACC, JIS-WAIC, JIS-GIHYO.
2. **MUST**: Accessibility is tested with automated tools *and* manual expert review (keyboard-only, screen reader), early and throughout development. *Evidence:* automated a11y checks in CI; a manual test record per release. *Sources:* WAI-EVAL.
3. **SHOULD**: User research and usability testing include disabled people and assistive-technology users. *Evidence:* research plan or participant log. *Sources:* GOVUK-ACC.
4. **MUST**: The organisation identifies the accessibility law that applies to each audience of the product and records it in its accessibility policy. Example (Japan; unofficial summary, not legal advice, applicability needs legal review): 障害者差別解消法 makes reasonable accommodation mandatory for businesses from 2024-04-01, and its Art. 13 refers measures an employer takes toward its own workers to 障害者雇用促進法 Art. 36-3. *Evidence:* a documented accessibility policy that references the applicable law. *Sources:* CAO-SABEKAI, SABEKAI-13, KOYO-36-3. That these laws require WCAG conformance specifically is an [inference]; the laws do not name WCAG.
5. **MUST**: Each page declares its language (`lang` on `<html>` using BCP 47 tags), and passages in another language are marked. This matters for multilingual content. *Evidence:* HTML source; WCAG 3.1.1/3.1.2 checks. *Sources:* WCAG22, W3C-LANG, W3C-ISPECS.
6. **MUST**: User-visible strings are kept out of code in resource files, are not built by concatenating fragments, and support plurals and word order per locale. *Evidence:* i18n resource files; a lint/grep showing no hard-coded UI text; message-format usage. *Sources:* W3C-I18N, W3C-ISPECS.
7. **MUST**: All content and data use UTF-8. *Evidence:* `<meta charset="utf-8">`; DB/connection charset. *Sources:* W3C-ENC.
8. **SHOULD**: Dates, numbers and names are formatted per the user's locale at display time, from locale-neutral stored values. *Evidence:* use of `Intl`/CLDR-based formatting; no hard-coded formats. *Sources:* W3C-I18N, W3C-ISPECS.
9. **MUST**: Input errors are identified in text next to the field, say what went wrong and how to fix it in plain language, and avoid jargon and error codes. *Evidence:* screenshots of validation states; the error-message content guide. *Sources:* WCAG22 (3.3.1, 3.3.3), GOVUK-ERR.
10. **MUST**: Status and error messages are announced to assistive technology without moving focus. *Evidence:* `role="status"`/`aria-live` use; a screen-reader test. *Sources:* WCAG22 (4.1.3).
11. **MUST**: API errors return a consistent machine-readable format (e.g. RFC 9457 Problem Details) and never expose stack traces or implementation internals. *Evidence:* API error samples; a production config showing debug output off. *Sources:* RFC9457.
12. **SHOULD**: The UI is built from a shared design system (components, patterns, tokens) that has been tested for accessibility. *Evidence:* a component library dependency; a pattern catalogue. *Sources:* GOVUK-DS, DADS.
13. **SHOULD**: Help mechanisms (contact, help pages) appear in the same place on every page, and user documentation exists for the main tasks. *Evidence:* UI review; help pages. *Sources:* WCAG22 (3.2.6 Consistent Help).
14. **SHOULD**: Main user journeys are usability-tested with real users before release and repeatedly after. *Evidence:* test plans, session notes, findings and fixes. *Sources:* GOVUK-P4, GOVUK-UT.
15. **SHOULD**: Authentication does not depend on a cognitive function test (allow password managers and paste, or SSO). *Evidence:* login page test. *Sources:* WCAG22 (3.3.8).

### Failure modes

- Relying on an automated checker alone and calling the site "accessible" (WAI-EVAL: "no tool alone can determine…").
- Treating accessibility as a late audit rather than designing for it from the start (GOVUK-ACC, WAI-EVAL).
- Missing or wrong `lang` on multilingual pages, so screen readers read one language with another language's rules (W3C-LANG).
- Building sentences by concatenating translated fragments, which breaks in languages with different word order (W3C-ISPECS 6.6).
- Generic or technical error messages ("unspecified error", codes) with no fix (GOVUK-ERR); stack traces in API responses (RFC9457).
- Assuming Japan's 合理的配慮 law applies the same way to every audience, without checking the employment-law route (SABEKAI-13).

### Sources

- **WCAG22**: *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 12 December 2024. https://www.w3.org/TR/WCAG22/ (accessed 2026-10-31)
  - 3.3.1 (Level A): "If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text."
  - 3.1.1 (Level A): "The default human language of each web page can be programmatically determined."
  - 4.1.3 (Level AA): status messages "can be presented to the user by assistive technologies without receiving focus."
  - 3.3.8 (Level AA): "A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following"
- **WAI-EVAL**: "Evaluating Web Accessibility Overview", W3C WAI. https://www.w3.org/WAI/test-evaluate/ (accessed 2026-10-31)
  - "However, no tool alone can determine if a site meets accessibility standards. Knowledgeable human evaluation is required to determine if a site is accessible."
- **GOVUK-ACC**: "Making your service accessible: an introduction", GOV.UK Service Manual. https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction (accessed 2026-10-31)
  - Digital services must "meet level AA of the Web Content Accessibility Guidelines (WCAG) 2.2 as a minimum"
  - "When doing research, you need to include disabled people and people who use assistive technologies."
- **JIS-WAIC**: 「JIS X 8341-3:2016 解説」, ウェブアクセシビリティ基盤委員会 (WAIC). https://waic.jp/docs/jis2016/understanding/201604/ (accessed 2026-10-31)
  - 「『JIS X 8341-3:2016』は、『ISO/IEC 40500:2012』の一致規格になっている。」 (The current JIS = WCAG 2.0, not 2.2.)
- **JIS-GIHYO**: 中村直樹 (Mitsue-Links), 「2026年のWebアクセシビリティ」, gihyo.jp, 2026-01-06. https://gihyo.jp/article/2026/01/web-accessibility-prospect (accessed 2026-10-31). Secondary source by a practitioner; status of the revision not confirmed with JISC.
  - 「改正JISは、JIS X 8341-3:2016と同様に、ISO/IEC 40500:2025との国際一致規格とすることを基本として考えています。」
  - 「順調にいけば、今年中にも改正JISが発行される見込みです。」
- **CAO-SABEKAI**: 「リーフレット『令和６年４月１日から合理的配慮の提供が義務化されました』」, 内閣府. https://www8.cao.go.jp/shougai/suishin/sabekai_leaflet-r05.html (accessed 2026-10-31)
  - 「令和３年に障害者差別解消法が改正され、事業者による障害のある人への合理的配慮の提供が義務化されました。」
- **SABEKAI-13**: 障害を理由とする差別の解消の推進に関する法律 第十三条, e-Gov (法令ID 425AC0000000065). https://laws.e-gov.go.jp/law/425AC0000000065 (accessed 2026-10-31)
  - 「行政機関等及び事業者が事業主としての立場で労働者に対して行う障害を理由とする差別を解消するための措置については、障害者の雇用の促進等に関する法律（昭和三十五年法律第百二十三号）の定めるところによる。」
- **KOYO-36-3**: 障害者の雇用の促進等に関する法律 第三十六条の三, e-Gov (法令ID 335AC0000000123). https://laws.e-gov.go.jp/law/335AC0000000123 (accessed 2026-10-31)
  - 「その雇用する障害者である労働者の障害の特性に配慮した職務の円滑な遂行に必要な施設の整備、援助を行う者の配置その他の必要な措置を講じなければならない。」
- **W3C-I18N**: "Localization vs. Internationalization", W3C Internationalization. https://www.w3.org/International/questions/qa-i18n (accessed 2026-10-31)
  - "Internationalization is the design and development of a product, application or document content that enables easy localization for target audiences that vary in culture, region, or language."
  - It includes "taking care over the concatenation of strings" and "Separating localizable elements from source code or content"
- **W3C-ISPECS**: *Internationalization Best Practices for Spec Developers*, W3C Group Note, 7 August 2026. https://www.w3.org/TR/international-specs/ (accessed 2026-10-31)
  - "Specifications SHOULD NOT require the concatenation of string values to form natural language or displayable string values."
  - "Values for language declarations must use BCP 47."
- **W3C-LANG**: "Declaring language in HTML", W3C Internationalization. https://www.w3.org/International/questions/qa-html-language-declarations (accessed 2026-10-31)
  - "Always use a language attribute on the html tag to declare the default language of the text in the page."
- **W3C-ENC**: "Choosing & applying a character encoding", W3C Internationalization. https://www.w3.org/International/questions/qa-choosing-encodings (accessed 2026-10-31)
  - "Choose UTF-8 for all content and consider converting any content in legacy encodings to UTF-8."
- **GOVUK-ERR**: "Error message" component, GOV.UK Design System. https://design-system.service.gov.uk/components/error-message/ (accessed 2026-10-31)
  - "Describe what has happened and tell them how to fix it."
  - "The message must be in plain English, use positive language and get to the point."
  - Do not use "technical jargon like ‘form post error’, ‘unspecified error’ and ‘error 0x0000000643’"
- **RFC9457**: RFC 9457, *Problem Details for HTTP APIs*, IETF, July 2023 (obsoletes RFC 7807). https://www.rfc-editor.org/rfc/rfc9457 (accessed 2026-10-31)
  - "This document obsoletes RFC 7807."
  - "avoid making implementation details such as a stack dump available through the HTTP interface"
- **GOVUK-DS**: GOV.UK Design System (home). https://design-system.service.gov.uk/ (accessed 2026-10-31)
  - "Learn from the research and experience of other service teams and avoid repeating work that’s already been done."
- **DADS**: デジタル庁デザインシステムβ版 (v2.18.2), デジタル庁. https://design.digital.go.jp/ (accessed 2026-10-31)
  - 「ユーザビリティとアクセシビリティを踏まえた設計や実装のためのガイドラインから構成されるデザインアセットです。」
- **GOVUK-P4**: "4. Make the service simple to use", GOV.UK Service Standard. https://www.gov.uk/service-manual/service-standard/point-4-make-the-service-simple-to-use (accessed 2026-10-31)
  - "test for usability frequently with actual and potential users, using appropriate research techniques"
  - "so that people succeed first time, with the minimum of help"
- **GOVUK-UT**: "Using moderated usability testing", GOV.UK Service Manual. https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing (accessed 2026-10-31)
  - "Moderated usability testing is where you watch participants try to complete specific tasks using your service."

---

## Area 16: Documentation and knowledge management

### Candidate requirements

1. **MUST**: Documentation is kept in version control (docs-as-code), close to the code it describes; any docs kept elsewhere are linked from the README. *Evidence:* a `docs/` folder or root docs in the repo; README links to external locations. *Sources:* SWE-DOC, GDOC-BP, WTD-DAC.
2. **MUST**: Documentation changes in the same pull request as the code it describes, and review checks this. *Evidence:* the PR template has a docs checkbox; sample PRs touch docs and code together. *Sources:* GDOC-BP, WTD-DAC, SWE-DOC.
3. **MUST**: Every document has a named owner and a last-reviewed date, and stale docs are re-reviewed, archived or deleted. *Evidence:* front-matter or CODEOWNERS for docs; a review log; documents marked obsolete. *Sources:* SWE-DOC, AWS-KM, GDOC-BP.
4. **MUST**: The repository README states what the project does, why it is useful, how to get started, where to get help, and who maintains it. *Evidence:* the README. *Sources:* GH-README.
5. **SHOULD**: Documentation is organised by user need into tutorials, how-to guides, reference and explanation, without mixing types on one page. *Evidence:* a docs index grouped by type. *Sources:* DIATAXIS.
6. **MUST**: Significant architecture decisions are recorded as short, numbered ADRs in the repo (title, status, context, decision, consequences). Accepted ADRs are not edited; they are superseded. *Evidence:* `docs/decisions/NNNN-*.md`; a superseded ADR pointing to its replacement. *Sources:* NYGARD, GDS-ADR, FOWLER-ADR, MADR.
7. **SHOULD**: Each document type has one canonical home, and duplicates link to it rather than copy it. *Evidence:* a docs map; no conflicting copies. *Sources:* GDOC-BP, SWE-DOC.
8. **SHOULD**: Docs get technical, audience and writing review, as appropriate to the document. *Evidence:* reviewers named in PRs for docs. *Sources:* SWE-DOC.
9. **SHOULD**: Incorrect docs are treated as defects: fixed, or deleted when no longer right ("default to delete"). *Evidence:* doc issues in the tracker; deletions in history. *Sources:* GDOC-BP, WTD-PRIN.
10. **MUST**: The knowledge base has mechanisms to create, update and archive content, not only a place to store it. *Evidence:* a documented doc lifecycle and its records. *Sources:* AWS-KM.
11. **MUST**: There is a structured onboarding path (a reading order, a checklist and set-up docs that a newcomer has actually followed) so newcomers do not rely on tribal knowledge. *Evidence:* the onboarding checklist; the date it was last used and updated. *Sources:* SRE-ACC.
12. **MUST**: Handover between people, teams or suppliers follows a written knowledge-transfer plan (pairing, sessions, documentation brought up to date) that is finished before the outgoing party leaves. *Evidence:* the handover plan; a sign-off. *Sources:* GOVUK-KT, SRE-ACC.
13. **SHOULD**: Documentation quality is treated as an engineering capability and is measured, e.g. with a periodic team survey on findability and reliability. *Evidence:* survey results or metrics. *Sources:* DORA-DOC.
14. **MAY**: Docs are linted and link-checked in CI, and merges can be blocked when a feature lacks documentation. *Evidence:* a CI job for docs. *Sources:* WTD-DAC.

### Failure modes

- A wiki or shared drive with no owners or review mechanism, so it goes stale (AWS-KM anti-pattern).
- Docs updated "later", separately from the code, and drifting out of date (GDOC-BP).
- Large monolithic design documents that nobody maintains (NYGARD: "Large documents are never kept up to date.").
- Mixing tutorial, how-to, reference and explanation on one page, so no reader is served well (DIATAXIS).
- Knowledge held in one person's head, which surfaces only at handover (SRE-ACC: "compartmentalized" knowledge as an anti-pattern; GOVUK-KT).
- Keeping wrong docs rather than deleting them (WTD-PRIN: incorrect is worse than missing).

### Sources

- **SWE-DOC**: Tom Manshreck, "Documentation", *Software Engineering at Google* (O'Reilly 2020), ch. 10. https://abseil.io/resources/swe-book/html/ch10.html (accessed 2026-10-31)
  - Documentation should "Be placed under source control", "Have clear ownership responsible for maintaining the docs", "Undergo reviews for changes (and change with the code it documents)"
  - "A technical review, for accuracy." / "An audience review, for clarity."
  - Metadata "will send email reminders when the document hasn’t been touched in, for example, three months."
- **GDOC-BP**: "Documentation Best Practices", Google Style Guides (docguide). https://google.github.io/styleguide/docguide/best_practices.html (accessed 2026-10-31)
  - "Change your documentation in the same CL as the code change."
  - "Dead docs are bad." … "Default to delete"
  - "A small set of fresh and accurate docs is better than a large assembly of" … (sentence continues "'documentation' in various states of disrepair.")
- **WTD-DAC**: "Docs as Code", Write the Docs. https://www.writethedocs.org/guide/docs-as-code/ (accessed 2026-10-31)
  - Docs as Code is about "writing documentation with the same tools as code"
  - "You can block merging of new features if they don’t include documentation"
- **WTD-PRIN**: "Documentation principles", Write the Docs. https://www.writethedocs.org/guide/writing/docs-principles/ (accessed 2026-10-31)
  - "Consider incorrect documentation to be worse than missing documentation."
- **DIATAXIS**: Daniele Procida, *Diátaxis*. https://diataxis.fr/ (accessed 2026-10-31)
  - "Diátaxis identifies four distinct needs, and four corresponding forms of documentation - tutorials, how-to guides, technical reference and explanation."
- **NYGARD**: Michael Nygard, "Documenting Architecture Decisions", Cognitect, 15 November 2011. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions (accessed 2026-10-31)
  - "Large documents are never kept up to date. Small, modular documents have at least a chance at being updated."
  - "If a decision is reversed, we will keep the old one around, but mark it as superseded."
- **GDS-ADR**: "Architecture decisions", The GDS Way (UK Government Digital Service). https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html (accessed 2026-10-31)
  - "Architecture decisions should be stored in version control so there is a record of what was changed, who by, and when."
  - "Decisions that affect a specific application should be in that application’s code repository."
- **FOWLER-ADR**: Martin Fowler, "Architecture Decision Record", martinfowler.com bliki. https://martinfowler.com/bliki/ArchitectureDecisionRecord.html (accessed 2026-10-31)
  - "Once an ADR is accepted, it should never be reopened or changed - instead it should be superseded."
- **MADR**: "MADR: Markdown Architectural Decision Records", adr.github.io. https://adr.github.io/madr/ (accessed 2026-10-31)
  - "Create folder docs/decisions in your project."
  - Copy the template to `docs/decisions/NNNN-title-with-dashes.md`, "where NNNN indicates the next number in sequence."
- **GH-README**: "About READMEs", GitHub Docs. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes (accessed 2026-10-31)
  - "A README is often the first item a visitor will see when visiting your repository."
  - "README files typically include information on:" followed by the list items "What the project does", "Why the project is useful", "How users can get started with the project", "Where users can get help with your project" and "Who maintains and contributes to the project".
- **AWS-KM**: AWS Well-Architected, Operational Excellence, OPS11-BP04 "Perform knowledge management". https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_knowledge_management.html (accessed 2026-10-31)
  - Anti-pattern: "You have a self-hosted wiki but no mechanisms to manage information, resulting in outdated information."
  - "Mechanisms exist to create new information, update existing information, and archive outdated information."
- **SRE-ACC**: "Accelerating SREs to On-Call and Beyond", *Site Reliability Engineering* (Google), ch. 28. https://sre.google/sre-book/accelerating-sre-on-call/ (accessed 2026-10-31)
  - "Put some amount of learning order into your system(s) so that your new SREs see a path before them."
  - "Newbie SREs are much more in need of up-to-date documentation"
  - Anti-pattern: "Creating experts on the team whose techniques and knowledge are compartmentalized"
- **GOVUK-KT**: "Working with contractors or third parties", GOV.UK Service Manual (last updated 17 October 2024). https://www.gov.uk/service-manual/the-team/working-contractors-third-parties (accessed 2026-10-31)
  - "You must make sure you have a plan to pass knowledge from contractors to the rest of your team. This is particularly important when you move from one phase to another, or if you change supplier."
  - One listed way: "make sure any documentation is in a good state"
- **DORA-DOC**: "Documentation quality", DORA (Google Cloud). https://dora.dev/capabilities/documentation-quality/ (accessed 2026-10-31)
  - "Analysis by DORA has found a clear link between documentation quality and organizational performance"
  - "Documentation needs to be actively created and maintained, which takes work."

---

## Gaps (could not source to a primary, verified quote)

- **ISO 8601 itself:** iso.org returned 403. ISO 8601 is cited only through RFC 3339's profile of it. No ISO/IEC text was read for any area (ISO 25010 usability, ISO 9241-110/-210, ISO/IEC/IEEE 26514/26511).
- **JIS X 8341-3 revision status:** no JISC or JSA primary source was found confirming whether the WCAG 2.2-aligned revision has been published as of 2026-10-31. The only source is a secondary article from January 2026 that expects publication "within 2026". The current verified JIS is :2016 (= WCAG 2.0).
- **Japan law applicability:** whether the 電気通信事業法 external-transmission rule applies to a given product, and whether 障害者雇用促進法 Art. 36-3 creates a duty to make software used by workers accessible, are inferences that need legal review. Neither law names WCAG.
- **Data migration and cut-over (reconciliation, rollback, owner sign-off)** and **integration contracts**: no authoritative standard was found; these are marked [judgement].
- **Audit-log retention periods:** no general-purpose source gives a number. NIST SP 800-92 Rev. 1 is still only a 2023 draft.
- **Product-telemetry practice beyond KPIs** (event taxonomy, consent for product analytics): only GOV.UK and OpenTelemetry guidance were found; no standard.
- **Error-message guidance in Japanese:** no Japanese government style source (e.g. デジタル庁 design-system error guidance) was verified quote by quote; only the design system's top page was read.
- **Diátaxis "blurring boundaries" quote** was not found on the fetched home page and was dropped.
