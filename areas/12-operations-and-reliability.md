# 12. Operations and reliability

- **ID prefix:** OPS
- **Status:** draft, 2026-10-31

## Purpose

This area protects against running a production service without agreed targets, written procedures, a way to respond to
incidents, or a tested way to recover data. It matters because the cost of these gaps appears only during an outage or a
data loss, when it is too late to write the runbook, find out who is responsible, or discover that the backups never
restored.

## Scope

Covers: service-level objectives and error budgets, runbooks, incident management, postmortems and their action items,
on-call and support rotas, recovery objectives (RPO/RTO), backups, restore tests, disaster recovery, capacity planning and
cost review.

Leaves to other areas:
- Logs, metrics, traces, dashboards and alert design: see Area 13. Runbook links on paging alerts: see OBS-4. This area
  covers only that alerts reach a responder (OPS-8) and that non-paging alerts link to a runbook (OPS-4).
- Rollback and deployment safety: see Area 11. Resource tagging and recovery-environment definitions: see Area 10.
- Performance, load and resilience testing: see Area 4.
- Where documentation lives and how it is kept current in general: see Area 16.
- Tracing incidents back to requirements and changes: see Area 17. Technical debt arising from postmortems: see Area 18.
- User-facing support model and communication: see Area 20.

## Requirements

### OPS-1 · MUST · Documented service-level objectives
Each production service MUST have documented service-level indicators and objectives (SLIs/SLOs) based on what its users
care about, stating how each is measured, who approved it, and when it is next reviewed.
- **Gate:** G3
- **Evidence:** an SLO document in a place stakeholders can read; after go-live, a dashboard or report showing each SLI against its SLO.
- **Basis:** [SRE-SLO], [SREW-SLO]. Level: author's judgement (sources support SHOULD). A service with simple needs can meet
  this with one availability target and one latency target.

### OPS-2 · MAY · Error-budget policy
A service MAY adopt an error-budget policy, agreed by product and engineering, that states what happens when the budget is
spent (for example, feature releases pause in favour of reliability work).
- **Gate:** G3 · **Condition:** once a measured SLO exists
- **Evidence:** the signed-off policy; release decisions that reference it.
- **Basis:** [SRE-RISK], [SREW-SLO]. Condition: author's judgement.

### OPS-3 · MUST · Runbooks in version control
Routine and emergency operational procedures (deploy, rollback, restore, credential rotation, response to each alert) MUST
be written as runbooks, stored in version control, and updated in the same change that alters the system they describe.
- **Gate:** G2
- **Evidence:** a runbook directory; each runbook states its outcome, required permissions and error handling; last-updated
  dates line up with related system changes.
- **Basis:** [AWS-OPS07-03], [SREW-ONCALL]. "Updated in the same change": author's judgement (the sources say runbooks are
  updated frequently and drift out of sync with system changes).

### OPS-4 · SHOULD · Non-paging alerts link to a runbook entry
Alerts that notify a person without paging (for example a ticket or a chat message) SHOULD link to the runbook entry that
tells the responder what to do. Paging alerts: OBS-4.
- **Gate:** G3
- **Evidence:** non-paging alert definitions each carry a runbook link; the links resolve.
- **Basis:** [SREW-ONCALL].

### OPS-5 · MUST · Incident-management process
A documented incident-management process MUST define when to declare an incident, severity levels, roles (incident lead,
operations, communications; one person can hold several), a live incident record, and how stakeholders are informed.
- **Gate:** G3
- **Evidence:** the incident procedure; incident records with timeline, roles and communications.
- **Basis:** [SRE-MI], [AWS-OPS10-01]. Severity levels and the named roles: author's judgement (not in the cited quotes).

### OPS-6 · MUST · Blameless postmortems on defined criteria
Postmortem criteria MUST be defined in advance (at least: user-visible impact above a set threshold, any data loss, any
manual intervention such as a rollback, and any incident found by a person rather than by monitoring), and every incident
meeting them gets a written, blameless postmortem.
- **Gate:** G3 · **Trigger:** each incident that meets the postmortem criteria
- **Evidence:** the written criteria; a postmortem for each qualifying incident in the incident log.
- **Basis:** [SRE-PM]. Level: author's judgement (sources support SHOULD).

### OPS-7 · MUST · Postmortem actions owned and tracked
Each postmortem action item MUST have an owner, a priority and a ticket in the issue tracker, and be tracked to completion.
- **Gate:** G3 · **Trigger:** each postmortem
- **Evidence:** action items in the tracker linked from the postmortem, with owner, priority and status; open items
  reviewed at an interval the project sets, with dated review notes.
- **Basis:** [SREW-PM], [AWS-OPS10-01].

### OPS-8 · MUST · Defined support rota and escalation
Every production service MUST have a written rota stating who responds to alerts and incidents during which hours, and how
to escalate, with alerts routed to a named responder. Business-hours-only cover is acceptable where the SLO and the business
allow it.
- **Gate:** G3
- **Evidence:** the rota or schedule; the escalation path; alert-routing configuration that targets the rota.
- **Basis:** [SRE-ONCALL], [AWS-REL06-03]. Business-hours allowance: author's judgement (no primary source found).

### OPS-9 · SHOULD · Out-of-hours on-call when targets require it
The service SHOULD have an out-of-hours on-call rotation with handover between shifts and an on-call load kept within a share of each responder's time that the project
sets.
- **Gate:** G3 · **Condition:** when the SLO or the business needs out-of-hours response
- **Evidence:** the out-of-hours schedule; the documented maximum share; pages per shift; the share of time spent on
  on-call work.
- **Basis:** [SRE-ONCALL] (see its quoted 25% guideline). Condition: author's judgement.

### OPS-10 · MUST · Recovery objectives agreed
Each workload MUST have a recovery point objective (RPO) and recovery time objective (RTO) agreed with its business owner.
- **Gate:** G3
- **Evidence:** RPO and RTO recorded per system with the business owner's approval and date.
- **Basis:** [AWS-REL13-01].

### OPS-11 · MUST · Automated backups that meet the RPO
All data that cannot be reproduced from other sources MUST be identified and backed up automatically, at a frequency that
meets the RPO.
- **Gate:** G3
- **Evidence:** a data inventory marking what is backed up and why; backup configuration with schedule and retention.
- **Basis:** [AWS-REL09-01].

### OPS-12 · MUST · Backups protected from the same failure
Backups MUST be protected from the failures and actions that could destroy the source (for example a copy in a separate
account or region, and protection against deletion or alteration).
- **Gate:** G3
- **Evidence:** backup copy location and access policy; deletion-protection or immutability settings.
- **Basis:** Author's judgement (no primary source found).

### OPS-13 · MUST · Restore tests
Restores MUST be tested at a defined interval (at least once a year and after any change to the backup set-up): data is
actually restored, queried to confirm it is usable, and the time taken compared with the RTO.
- **Gate:** G3 · **Trigger:** after any change to the backup set-up
- **Evidence:** dated restore-test records with the verification steps and the measured duration.
- **Basis:** [AWS-REL09-04]. Minimum interval: author's judgement.

### OPS-14 · SHOULD · Disaster-recovery plan exercised
A disaster-recovery plan SHOULD exist and be exercised at an interval the project sets, with recovery environments kept in
configuration parity with production.
- **Gate:** G3
- **Evidence:** the DR plan with its exercise interval; DR exercise reports within that interval; drift checks between
  primary and recovery configuration.
- **Basis:** [AWS-REL13-03], [AWS-REL13-04].

### OPS-15 · SHOULD · Capacity planning and quota monitoring
Capacity SHOULD be planned from forecast demand (organic growth and known events), checked against load-test results (see
Area 4), with service quotas and limits monitored by alarms set below each limit.
- **Gate:** G3
- **Evidence:** a capacity plan; load-test results; quota or limit alarms with thresholds below the limits.
- **Basis:** [SRE-INTRO], [AWS-REL01-04].

### OPS-16 · SHOULD · Cost attributed and reviewed
Running cost SHOULD be attributed per service and environment (using the tags described in ENV-15) and reviewed against a
budget at an interval the project sets.
- **Gate:** G2
- **Evidence:** a cost report grouped by tag; budget alerts; dated review notes.
- **Basis:** [AWS-COST03-02]. Budget review: author's judgement (no primary source found).

## Failure modes

- No SLO, so users form their own expectations and reliability work is never prioritised ([SRE-SLO]).
- Backups assumed to work but never restored, or restored without checking the data ([AWS-REL09-04]).
- No recovery objectives, or objectives chosen arbitrarily ([AWS-REL13-01]).
- Procedures that live in one person's memory, and runbooks that drift out of date as the system changes ([AWS-OPS07-03],
  [SREW-ONCALL]).
- Postmortems that assign blame, or produce vague action items with no owner or priority ([SRE-PM], [SREW-PM]).
- Alerts tuned so noisily that responders ignore the important ones ([AWS-REL06-03]).

## References

- **[AWS-COST03-02]** COST03-BP02 Add organization information to cost and usage. AWS Well-Architected Framework, Cost Optimization Pillar. https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_monitor_usage_org_information.html. Accessed 2026-10-31.
  > "Implement consistent tagging across all resources where possible by purpose, team, environment, or other criteria relevant to your business."
- **[AWS-OPS07-03]** OPS07-BP03 Use runbooks to perform procedures. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html. Accessed 2026-10-31.
  > "The runbooks contain the desired outcome, necessary tools and permissions, and instructions for error handling. They are stored in a central location (version control system) and updated frequently." (Desired outcome)
  > "Relying on memory to complete each step of a process." (Common anti-patterns)
  > "Letting runbooks drift out of sync with system changes and automation." (Common anti-patterns)
- **[AWS-OPS10-01]** OPS10-BP01 Use a process for event, incident, and problem management. AWS Well-Architected Framework, Operational Excellence Pillar. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_event_response_event_incident_problem_process.html. Accessed 2026-10-31.
  > "Your organization effectively manages operational events, incidents, and problems through well-documented and centrally stored processes." (Desired outcome)
  > "Your organization does not analyze and learn from incidents to prevent future occurrences." (Common anti-patterns)
- **[AWS-REL01-04]** REL01-BP04 Monitor and manage quotas. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_manage_service_limits_monitor_manage_limits.html. Accessed 2026-10-31.
  > "Not configuring monitoring to check for service quota thresholds" (Common anti-patterns)
- **[AWS-REL06-03]** REL06-BP03 Send notifications (Real-time processing and alarming). AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_monitor_aws_resources_notification_monitor.html. Accessed 2026-10-31.
  > "When alarm thresholds are breached, the appropriate personnel and systems are notified so they can address underlying issues." (Desired outcome)
  > "Configuring alarms with a threshold that is too low, resulting in inaction on important alerts due to the noise of excessive notifications." (Common anti-patterns)
- **[AWS-REL09-01]** REL09-BP01 Identify and back up all data that needs to be backed up, or reproduce the data from sources. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_identified_backups_data.html. Accessed 2026-10-31.
  > "Data sources have been identified and classified based on criticality. Then, establish a strategy for data recovery based on the RPO." (Desired outcome)
  > "Not taking backups of critical data sources." (Common anti-patterns)
  > "No defined RPO, or backup frequency cannot meet RPO." (Common anti-patterns)
- **[AWS-REL09-04]** REL09-BP04 Perform periodic recovery of the data to verify backup integrity and processes. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html. Accessed 2026-10-31.
  > "Data from backups is periodically recovered using well-defined mechanisms to verify that recovery is possible within the established recovery time objective (RTO) for the workload." (Desired outcome)
  > "Restoring a backup, but not querying or retrieving any data to check that the restoration is usable. Assuming that a backup exists." (Common anti-patterns)
- **[AWS-REL13-01]** REL13-BP01 Define recovery objectives for downtime and data loss. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html. Accessed 2026-10-31.
  > "Every workload has a designated RTO and RPO based on technical considerations and business impact." (Desired outcome)
  > "You haven't designated recovery objectives. You select arbitrary recovery objectives." (Common anti-patterns)
- **[AWS-REL13-03]** REL13-BP03 Test disaster recovery implementation to validate the implementation. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_dr_tested.html. Accessed 2026-10-31.
  > "Regularly testing you disaster recovery plan verifies that it will work when it needs to, and that your team knows how to perform the strategy." (sic in source)
- **[AWS-REL13-04]** REL13-BP04 Manage configuration drift at the DR site or Region. AWS Well-Architected Framework, Reliability Pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_config_drift.html. Accessed 2026-10-31.
  > "You fail to update recovery locations when changes are made to the primary locations, which results in outdated configurations that could hinder recovery efforts."
- **[SRE-INTRO]** Benjamin Treynor Sloss, Introduction, Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/introduction/. Accessed 2026-10-31. The missing space before the parenthesis in the second quote is the source's own.
  > "Capacity planning should take both organic growth (which stems from natural product adoption and usage by customers) and inorganic growth" (Ch. 1, Demand Forecasting and Capacity Planning)
  > "Regular load testing of the system to correlate raw capacity(servers, disks, and so on) to service capacity" (Ch. 1, Demand Forecasting and Capacity Planning)
- **[SRE-MI]** Andrew Stribblehill, Managing Incidents, Chapter 14 of Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/managing-incidents/. Accessed 2026-10-31.
  > "Set clear conditions for declaring an incident." (Ch. 14, When to Declare an Incident)
  > "It is better to declare an incident early and then find a simple fix and close out the incident than to have to spin up the incident management framework hours into a burgeoning problem." (Ch. 14, When to Declare an Incident)
  > "The incident commander’s most important responsibility is to keep a living incident document." (Ch. 14, Live Incident State Document)
- **[SRE-ONCALL]** Andrea Spadaccini, Being On-Call, Chapter 11 of Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/being-on-call/. Accessed 2026-10-31.
  > "The most important on-call resources are:" (Ch. 11, Feeling Safe)
  > "Clear escalation paths" (Ch. 11, Feeling Safe)
  > "Well-defined incident-management procedures" (Ch. 11, Feeling Safe)
  > "of the remainder, no more than 25% can be spent on-call, leaving up to another 25% on other types of operational, nonproject work." (Ch. 11, Balance in Quantity)
- **[SRE-PM]** John Lunney, Sue Lueder, Postmortem Culture: Learning from Failure, Chapter 15 of Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/postmortem-culture/. Accessed 2026-10-31.
  > "A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring." (Ch. 15, Postmortem Culture: Learning from Failure)
  > "It is important to define postmortem criteria before an incident occurs so that everyone knows when a postmortem is necessary." (Ch. 15, Google’s Postmortem Philosophy)
  > "For a postmortem to be truly blameless, it must focus on identifying the contributing causes of the incident without indicting any individual or team for bad or inappropriate behavior." (Ch. 15, Google’s Postmortem Philosophy)
  > "Data loss of any kind" (Ch. 15, Google’s Postmortem Philosophy)
  > "A monitoring failure (which usually implies manual incident discovery)" (Ch. 15, Google’s Postmortem Philosophy)
- **[SRE-RISK]** Marc Alvidrez, Embracing Risk, Chapter 3 of Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/embracing-risk/. Accessed 2026-10-31.
  > "As long as the uptime measured is above the SLO—in other words, as long as there is error budget remaining—new releases can be pushed." (Ch. 3, Forming Your Error Budget)
  > "If SLO violations occur frequently enough to expend the error budget, releases are temporarily halted while additional resources are invested in system testing and development" (Ch. 3, Benefits)
- **[SRE-SLO]** Chris Jones, John Wilkes, Niall Murphy, Cody Smith, Service Level Objectives, Chapter 4 of Site Reliability Engineering. Google / O'Reilly, 2016. https://sre.google/sre-book/service-level-objectives/. Accessed 2026-10-31.
  > "Start by thinking about (or finding out!) what your users care about, not what you can measure." (Ch. 4, Objectives in Practice)
  > "For maximum clarity, SLOs should specify how they’re measured and the conditions under which they’re valid." (Ch. 4, Defining Objectives)
  > "Without an explicit SLO, users often develop their own beliefs about desired performance" (Ch. 4, Objectives)
- **[SREW-ONCALL]** On-Call, Chapter 8 of The Site Reliability Workbook. Google / O'Reilly, 2018. https://sre.google/workbook/on-call/. Accessed 2026-10-31.
  > "In SRE, whenever an alert is created, a corresponding playbook entry is usually created." (Ch. 8, Training roadmap)
  > "Details in playbooks go out of date at the same rate as production environment changes." (Ch. 8, Maintaining Playbooks)
- **[SREW-PM]** Postmortem Culture: Learning from Failure, Chapter 10 of The Site Reliability Workbook. Google / O'Reilly, 2018. https://sre.google/workbook/postmortem-culture/. Accessed 2026-10-31.
  > "All of the action items have been tagged with an equal priority. There’s no way to determine which action to tackle first."
- **[SREW-SLO]** Implementing SLOs, Chapter 2 of The Site Reliability Workbook. Google / O'Reilly, 2018. https://sre.google/workbook/implementing-slos/. Accessed 2026-10-31.
  > "An appropriately defined SLO should be documented in a prominent location where other teams and stakeholders can review it." (Ch. 2, Documenting the SLO and Error Budget Policy)
  > "The authors of the SLO, the reviewers (who checked it for technical accuracy), and the approvers (who made the business decision about whether it is the right SLO)." (Ch. 2, Documenting the SLO and Error Budget Policy)
  > "The organization has committed to using the error budget for decision making and prioritizing. This commitment is formalized in an error budget policy." (Ch. 2, Getting Started)
