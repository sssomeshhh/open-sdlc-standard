# 13. Observability and telemetry

- **ID prefix:** OBS
- **Status:** draft, 2026-10-31

## Purpose
A system that cannot be observed fails silently: problems reach users before the team knows, and incidents take longer to diagnose
because nobody can ask the system what happened. This area makes sure every service emits the logs, metrics and traces needed to
answer "what's broken, and why?" [SRE-MON], alerts people only when action is needed, keeps telemetry free of secrets and needless
personal data, and measures whether the product achieves what it was built for.

## Scope
Covers the mechanics of logs, metrics and traces; dashboards; alerting; protection and retention of logs (including audit logs);
time synchronisation of telemetry; and product/usage telemetry.

Left to other areas:
- Which events are audit-logged (authentication, authorisation, administrative actions): see SEC-14 (Area 5). This area covers
  how those logs are written, protected and retained (OBS-11, OBS-12).
- Service-level objectives, runbooks, incident management and on-call: see Area 12. Runbook links on paging alerts are set here
  (OBS-4); on non-paging alerts, see OPS-4.
- Personal-data classification, minimisation and applicable privacy law: see Area 6.
- Date/time format and time-zone policy: see DAT-9 (Area 14).
- Success criteria (KPIs) themselves: see Area 1.

## Requirements

### OBS-1 · MUST · Core telemetry signals
Each service MUST emit logs, metrics and traces, or record in its documentation why one of these signals is not needed (an exemption the requirement itself allows, distinct from "not applicable"; for
example, a single-process batch job with no remote calls might not need traces).
- **Gate:** G3
- **Evidence:** instrumentation code or configuration for each signal; a sample of each signal from production; or a written
  reason for any signal left out.
- **Basis:** [OTEL-PRIMER]. Level: author's judgement (the source explains why instrumentation is needed; it does not set a level).

### OBS-2 · MUST · Structured logs as an event stream
Applications MUST write logs as a structured (for example JSON or key-value), time-ordered event stream to stdout/stderr or to a
log collector, leaving log files, routing and rotation to the environment rather than managing them in the application.
- **Gate:** G2
- **Evidence:** logger configuration; one sample log line in structured form; no log-rotation or log-file code in the application.
- **Basis:** [12F-11]. Level: author's judgement for the structured format (the source covers the event stream and routing).

### OBS-3 · MUST · Golden signals
Every user-facing service MUST measure the four golden signals: latency (reported as percentiles, for example p50/p95/p99, not
only as an average), traffic, errors and saturation.
- **Gate:** G3
- **Evidence:** a dashboard or metric list showing all four signals; latency shown as percentiles.
- **Basis:** [SRE-MON]. Level: author's judgement (the source recommends the four signals; it does not mandate them).

### OBS-4 · MUST · Actionable, symptom-based paging
Every alert that pages a human MUST be actionable, based on a symptom users feel (or on an SLO burn rate), and linked to a
runbook entry (runbooks: see Area 12). Alerts that need no action are removed or demoted to non-paging notifications.
- **Gate:** G3
- **Evidence:** alert rule definitions, each with a runbook link; page history showing no recurring pages that needed no action.
- **Basis:** [SRE-MON], [SRE-ALERT], [SREW-ONCALL]. Symptom basis: author's judgement (the cited quotes support actionable
  pages and burn-rate alerting). Runbook link — Level: author's judgement (source supports SHOULD).
- Note: this is the single rule for runbook links on paging alerts; OPS-4 (Area 12) covers non-paging alerts.

### OBS-5 · SHOULD · Burn-rate alerting on SLOs
Where a service has SLOs (see Area 12), alerting SHOULD use error-budget burn rates over more than one window, with the precision
and recall of alerts reviewed at an interval the project sets.
- **Gate:** G3
- **Evidence:** burn-rate alert definitions with at least two windows; the review interval, recorded in the log-management plan
  (OBS-13) or the alerting documentation; a dated review record of alert precision and recall within that interval.
- **Basis:** [SRE-ALERT].

### OBS-6 · MUST · Redaction before telemetry is written
The telemetry pipeline MUST remove, mask or hash secrets (SEC-7), session identifiers [OWASP-CS-LOGGING] and personal data not
permitted by PRV-8 before logs, metrics and traces are written or exported.
- **Gate:** G2
- **Evidence:** redaction configuration or tests; a search of a production log sample showing no tokens or session IDs, and no
  personal data such as e-mail addresses except where the inventory permits it (PRV-8).
- **Basis:** [OWASP-CS-LOGGING], [OTEL-SENS].

### OBS-7 · SHOULD · Review what instrumentation libraries collect
Before a third-party instrumentation or analytics library is adopted, and when it is upgraded, the team SHOULD review what
telemetry it emits and configure it to drop data that OBS-6 excludes.
- **Gate:** G1 · **Trigger:** each time an instrumentation or analytics library is adopted or upgraded
- **Evidence:** a review note per library (in the PR or a decision record); the resulting configuration.
- **Basis:** [OTEL-SENS].

### OBS-8 · MUST · Synchronised clocks and unambiguous timestamps
All hosts that produce telemetry MUST synchronise their clocks to a common time source and write every log and telemetry
timestamp in an international format with UTC or an explicit offset (format details: see DAT-9).
- **Gate:** G2
- **Evidence:** time-synchronisation (for example NTP) configuration or the platform's documented equivalent; log timestamps in
  RFC 3339 form.
- **Basis:** [OWASP-CS-LOGGING].

### OBS-9 · SHOULD · Correlated logs and traces
Request context SHOULD be propagated across service boundaries with W3C Trace Context, with the trace and span IDs written into
every log record produced while handling that request.
- **Gate:** G3 · **Condition:** once the system is made of more than one service
- **Evidence:** a `traceparent` header on outbound calls; a log line carrying a trace ID that matches a trace.
- **Basis:** [W3C-TC], [OTEL-LOGS]. Condition: author's judgement.

### OBS-10 · SHOULD · Consistent telemetry naming
Attribute and metric names SHOULD follow the OpenTelemetry semantic conventions, or one documented naming scheme used across the
project.
- **Gate:** G2
- **Evidence:** attribute names in emitted data (for example `http.request.method`); the naming document if a custom scheme is used.
- **Basis:** [OTEL-SEMCONV].

### OBS-11 · MUST · Tamper-evident, access-controlled audit logs
Audit and security logs (content defined in SEC-14, Area 5) MUST be stored so that modification or deletion is prevented or
detected, with read access restricted to named roles.
- **Gate:** G3
- **Evidence:** storage settings (write-once storage, or tamper detection such as hash chaining); the access policy listing who can
  read and who can delete; audit logs stored apart from the application's own writable data.
- **Basis:** [OWASP-CS-LOGGING]. Restriction to named roles: author's judgement (the source asks for restricted, periodically reviewed
  read privileges).
- Note: this is the single rule for protecting audit logs; SEC-14 points here.

### OBS-12 · MUST · Defined retention for every log store
Every log and telemetry store MUST have a defined retention period, set in configuration and justified by operational, security or
legal need.
- **Gate:** G3
- **Evidence:** retention values in the storage or platform configuration; the written justification.
- **Basis:** [SP800-92], [OWASP-CS-LOGGING]. Level: author's judgement; no general-purpose source gives a retention period, so the period
  itself is set per project.

### OBS-13 · SHOULD · Written log-management plan
The project SHOULD have a written log-management plan stating which logs are kept, where, for how long, and who reviews them.
- **Gate:** G3
- **Evidence:** the plan document, linked from the project documentation.
- **Basis:** [SP800-92], [SP800-92R1] (the Rev. 1 planning guide is an initial public draft, not a final publication).

### OBS-14 · SHOULD · Product telemetry tied to success criteria
Product and usage telemetry SHOULD measure the success criteria defined for the product (Area 1), with that data used when
deciding what to change.
- **Gate:** G3
- **Evidence:** a metric definition for each KPI; a dashboard showing them; decisions or backlog items that cite the data.
- **Basis:** [GOVUK-P10].

### OBS-15 · MUST · Minimal usage telemetry
Usage telemetry MUST collect only data needed for a stated purpose.
- **Gate:** G3
- **Evidence:** an inventory of analytics data, each item with its purpose and recipients.
- **Basis:** [OTEL-SENS]. Applying the source's observability rule to product analytics: author's judgement.

### OBS-16 · SHOULD · Service dashboards
Each service SHOULD have a dashboard that answers basic questions about its health, starting with the four golden signals.
- **Gate:** G3
- **Evidence:** the dashboard, showing the signals from OBS-3.
- **Basis:** [SRE-MON].

### OBS-17 · MUST · Notice or consent for third-party transmission where law requires
Where the user's device sends usage data to a third party (for example an analytics tag), the project MUST give any notice, obtain
any consent or offer any opt-out that applicable law requires.
- **Gate:** G3
- **Evidence:** the inventory from OBS-15 showing third-party recipients; the privacy notice; a consent or opt-out mechanism where
  required; a record of the legal review.
- **Basis:** [SOUMU-GAIBU]. Applicability of jurisdiction-specific law: author's inference, needs legal confirmation (see also
  Area 6).
- Note: example (Japan; the author's unofficial summary, not legal advice): the external-transmission rule of the
  Telecommunications Business Act (電気通信事業法, in force since 2023-06-16) asks for one of notice or publication, consent, or an
  opt-out measure; whether it applies to a given product needs legal review.

## Failure modes
- Paging on causes (CPU, a single host) rather than on symptoms users feel, which produces alert fatigue and pages that need no
  action [SRE-MON].
- Reporting average latency only, which hides slow tail requests [SRE-MON].
- Logs from separate components with no shared request ID, so they cannot be correlated [OTEL-LOGS].
- Tokens, passwords or personal data written into logs or traces, including by third-party instrumentation [OWASP-CS-LOGGING], [OTEL-SENS].
- Audit logs kept in the same writable store that the application and its administrators can change, so tampering cannot be
  detected [OWASP-CS-LOGGING].
- Usage analytics added with no KPI behind it, or with no privacy notice [GOVUK-P10], [SOUMU-GAIBU].

## References
- **[12F-11]** "XI. Logs", The Twelve-Factor App. Adam Wiggins. https://12factor.net/logs. Accessed 2026-10-31.
  > "Logs are the stream of aggregated, time-ordered events" (Treat logs as event streams)
  > "A twelve-factor app never concerns itself with routing or storage of its output stream." (Treat logs as event streams)
- **[GOVUK-P10]** "10. Define what success looks like and publish performance data", GOV.UK Service Standard. Government Digital
  Service. https://www.gov.uk/service-manual/service-standard/point-10-define-success-publish-performance-data. Accessed 2026-10-31.
  > "identify metrics which will indicate how well the service is solving the problem it's meant to solve" (What it means)
  > "use performance data to make decisions about how to fix problems and improve the service" (What it means)
- **[OTEL-LOGS]** "OpenTelemetry Logging" (specification). OpenTelemetry. https://opentelemetry.io/docs/specs/otel/logs/.
  Accessed 2026-10-31.
  > "OpenTelemetry extends this practice to logs where possible by including TraceId and SpanId in the LogRecords." (Log Correlation)
  > "This makes it nearly impossible to perform trace context correlation for system logs." (System Logs)
- **[OTEL-PRIMER]** "Observability primer". OpenTelemetry (CNCF). https://opentelemetry.io/docs/concepts/observability-primer/.
  Accessed 2026-10-31.
  > "Observability lets you understand a system from the outside by letting you ask questions about that system without knowing its inner workings." (What is Observability?)
  > "To ask those questions about your system, your application must be properly instrumented." (What is Observability?)
- **[OTEL-SEMCONV]** "Semantic Conventions". OpenTelemetry. https://opentelemetry.io/docs/concepts/semantic-conventions/.
  Accessed 2026-10-31.
  > "specify common names for different kinds of operations and data." (introduction)
  > "The benefit of using Semantic conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms." (introduction)
- **[OTEL-SENS]** "Handling sensitive data". OpenTelemetry. https://opentelemetry.io/docs/security/handling-sensitive-data/.
  Accessed 2026-10-31.
  > "you are responsible for understanding and reviewing the telemetry data emitted by any instrumentation libraries you use" (Your responsibility)
  > "Only collect data that serves an observability purpose." (Data minimization)
- **[OWASP-CS-LOGGING]** "Logging Cheat Sheet", OWASP Cheat Sheet Series. OWASP.
  https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html. Accessed 2026-10-31.
  > "Session identification values" (Data to exclude)
  > "Sensitive personal data and some forms of personally identifiable information (PII)" (Data to exclude)
  > "Synchronize time across all servers and devices" (Event collection)
  > "Log date and time (international format)" (Event attributes)
  > "Build in tamper detection so you know if a record has been modified or deleted" (Protection)
  > "The privileges to read log data should be restricted and reviewed periodically" (Protection)
  > "Log data, temporary debug logs, and backups/copies/extractions, must not be destroyed before the duration of the required data retention period, and must not be kept beyond this time." (Disposal of logs)
- **[SOUMU-GAIBU]** 「外部送信規律」 (external-transmission rule). Ministry of Internal Affairs and Communications (総務省), Japan.
  https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu.html. Accessed 2026-10-31. Jurisdiction-specific
  example; applicability needs legal review.
  > "電気通信事業を営む者（ウェブサイト運営者、アプリケーション提供者等）は、利用者の端末に外部送信を指示するプログラムを送る際は、あらかじめ、送信される利用者に関する情報の内容等を、通知・公表（利用者が容易に知り得る状態に置く）等しなければなりません。" (introduction)
  > "改正電気通信事業法の施行（2023年6月16日）" (introduction)
  > "通知又は公表（利用者が容易に知り得る状態に置く）、同意取得、オプトアウト措置のいずれかを、利用者に対して行ってください。" (introduction)
- **[SP800-92]** NIST SP 800-92, *Guide to Computer Security Log Management*, September 2006 (final). NIST.
  https://csrc.nist.gov/pubs/sp/800/92/final (full text: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf).
  Accessed 2026-10-31.
  > "This publication seeks to assist organizations in understanding the need for sound computer security log management." (1.2)
  > "System-level administrators need to configure log sources so that they capture the needed information in the desired format and locations, as well as retain the information for the appropriate period of time." (5.7)
- **[SP800-92R1]** NIST SP 800-92 Rev. 1 (Initial Public Draft), *Cybersecurity Log Management Planning Guide*, 11 October 2023.
  NIST. https://csrc.nist.gov/pubs/sp/800/92/r1/ipd. Accessed 2026-10-31. Draft; not final.
  > "This document defines a playbook intended to help any organization plan improvements to its cybersecurity log management."
- **[SRE-ALERT]** "Alerting on SLOs", *The Site Reliability Workbook*, ch. 5. Google. https://sre.google/workbook/alerting-on-slos/.
  Accessed 2026-10-31.
  > "The proportion of events detected that were significant." (Ch. 5, Alerting Considerations)
  > "The proportion of significant events detected." (Ch. 5, Alerting Considerations)
  > "We have found that alerting based on multiple burn rates is a powerful way to implement SLO-based alerting." (Ch. 5, 6: Multiwindow, Multi-Burn-Rate Alerts)
- **[SRE-MON]** "Monitoring Distributed Systems", *Site Reliability Engineering*, ch. 6. Google (O'Reilly 2016).
  https://sre.google/sre-book/monitoring-distributed-systems/. Accessed 2026-10-31.
  > "If you can only measure four metrics of your user-facing system, focus on these four." (Ch. 6, The Four Golden Signals)
  > "Every page should be actionable." (Ch. 6, Tying These Principles Together)
  > "Every page response should require intelligence." (Ch. 6, Tying These Principles Together)
  > "Your monitoring system should address two questions: what's broken, and why?" (Ch. 6, Symptoms Versus Causes)
  > "the idea that most of your requests are near the mean is just hopeful thinking" (Ch. 6, Conclusion)
  > "Dashboards should answer basic questions about your service, and normally include some form of the four golden signals" (Ch. 6, Why Monitor?)
- **[SREW-ONCALL]** On-Call, Chapter 8 of The Site Reliability Workbook. Google / O'Reilly, 2018. https://sre.google/workbook/on-call/. Accessed 2026-10-31.
  > "In SRE, whenever an alert is created, a corresponding playbook entry is usually created."
- **[W3C-TC]** *Trace Context*, W3C Recommendation, 23 November 2021. W3C. https://www.w3.org/TR/trace-context/. Accessed 2026-10-31.
  > "This specification defines standard HTTP headers and a value format to propagate context information"
