---
status: accepted
date: 2026-11-01
decision-makers: SomesH S (owner of the standard)
---

# Rules for applying the standard and auditing against it

## Context and Problem Statement

The areas say *what* a project must do. A project that adopts the standard, and an auditor who checks it, also need to know
*how* it applies: to what unit, by when, what counts as an acceptable deviation, how an audit is graded and what may be claimed.
Twenty such questions were identified. Without answers, two auditors could grade the same project
differently, and a project could set aside a MUST without anyone accountable deciding it.

This record states the decision taken on each question. The rules themselves are in the [README](../../README.md), "Applying
the standard" and "This standard"; where this record and the README differ, the README is authoritative.

## Decision Drivers

- An auditor can check every rule yes or no from the project's records.
- A MUST is never set aside silently, and never indefinitely for something the project or its organisation could change.
- The rules are generic: they work for any size of project and any organisation, and assume no particular tool.
- The standard can change without breaking projects that already use it.

## Considered Options

For each question, the option chosen is listed in "Decision Outcome". Where an alternative was considered and rejected, it is
named there; where none is named, no alternative was recorded.

## Decision Outcome

Chosen: the rules below, as written in the README.

### Scope

1. **Not applicable**. Only when the requirement's subject does not exist in the system; the project records the reason and
   the auditor confirms it. Effort or cost is never a reason: that needs a gap waiver (MUST) or a tailoring entry (SHOULD).
2. **Unit of adoption**. One *system*, with its records in one home repository. Rejected: one repository = one project;
   each project chooses.
3. **Libraries, tools and modules**. A system in their own right: go-live (G3) is the first release used by others, and
   requirements about a running service are not applicable when nothing is run on their behalf. Rejected: out of scope; a
   separate profile.

### Gates

4. **Gates**. Five gates, G0 Inception to G4 Retirement; every requirement names its gate, and some carry a Condition or a
   Trigger. By its gate a MUST is met or covered by a valid waiver, a SHOULD is met or in the tailoring record; a MAY never blocks.
5. **Lapses**. A requirement that stops being met is unmet from when it stopped (or when found), both dates recorded; it is
   remediated and blocks the next gate; a gate already passed is never reopened. Rejected: a lapse reopens the gate.

### Deviations and waivers

6. **Who approves**. SHOULD deviations: one tailoring record per system, approved by the project lead. MUST waivers: a
   separate record, accepted by a person accountable for the system outside the delivery team, for at most 12 months.
7. **Two kinds of MUST waiver**.
   - *Gap* (the project can meet the MUST but has not yet): carries the remediation plan; its target date is the remediation due
     date; accepted only before that date; never renewed or replaced. No new gap waiver for the same MUST within 12 months of the
     acceptance of its previous one, and missed occurrences of a Trigger within 12 months count as one gap.
   - *Conflict* (law or a contract prevents the MUST): names the obligation; renewed by adding entries to the same record while
     the conflict lasts; ends when the conflict ends.
8. **Conflicts with other obligations**. Law always applies. Where a contract, an organisational
   policy or a customer requirement asks less, the standard still applies and the difference is recorded. Where law or a contract (including a customer requirement
   written into a contract) prevents a MUST, the project follows it under a conflict waiver. An organisational policy or a
   customer requirement outside a contract is not a binding obligation under this rule: the MUST is unmet and the remediation is
   to have it corrected (a gap waiver may cover it meanwhile). Rejected: contracts always win.
9. **Change of ownership**. Records move with the system. When the accountable owner changes, or a waiver's acceptor leaves
   the role, each open waiver is re-confirmed within 30 days without changing its terms, or it ends. Rejected: waivers run to
   expiry regardless.
10. **Rules that need a second person**. Nobody approves their own work; a fallback reviewer from outside the team is named
    in advance; an emergency change may be reviewed afterwards within a set time; for AI-written changes, the person who directed
    the tool is the author.

### Dependencies outside the project

11. **Organisation-level policies**: linked where they exist; otherwise a minimal project version, and the gap recorded for
    the organisation. **Requirements controlled by another team**: met with that team's evidence; gaps recorded against
    the project and escalated. **Records outside the repository**: kept in one named, access-controlled place and linked
    from the home repository. **Project-defined terms**: defined once, in one document, which is itself audited.

### Auditing and claims

12. **Results and grading**. Met / partly met / not met / not applicable per requirement; Evidence is illustrative; a pass
    needs every MUST met, not applicable, or covered by a valid waiver.
13. **History**. A new project is judged on its whole history; a later adopter
    starts with a gap analysis; a missed one-time record is produced now, dated when it is made and noting the moment it should
    have preceded; requirements that apply to each occurrence of an event apply from adoption onwards.
14. **Who audits**. Self-assessments are allowed and do not replace formal audits. Formal audits are
    a requirement (GOV-17), by an assessor who was not in the delivery team, did not write, approve or review the work, and does
    not report to the system's lead or owner (basis: NIST SP 800-53 CA-2 and CA-2(1)). Rejected: leave it to each organisation.
15. **Remediation**. Every unmet MUST gets an owner and a due date; a missed due date is recorded as overdue and never moved.
16. **Claims**. "Adopts" needs records and one self-assessment; "Conforms (audited date)" needs a
    passing formal audit at most 12 months old and no MUST known to have been unmet since without a valid waiver. Never
    "certified" or "compliant". Rejected: no rules on claims.

### This standard

17. **Versions**. One version for the standard and its tools. Each system states the version it applies and moves to a new
    one within 90 days, as a whole version. A stricter rule or requirement is MINOR; a relaxed one, or any other change of
    meaning, is MAJOR. Rejected: always the newest version.
18. **Modified versions**. Allowed under CC BY 4.0; a modified version should be described as "based on the Open SDLC Standard vX.Y.Z", with the modifier
    and the changes named; claims apply only to the unmodified standard. Rejected: licence terms only.

### Consequences

- Good: every rule can be checked from records; no MUST can be waived indefinitely except where law or a contract requires it;
  claims stay true between audits.
- Bad: rules are stricter than many organisations' habits (an outside acceptor for every MUST waiver, one-off gap waivers, an
  independent formal audit), so small teams will often have unmet MUSTs on record. That is intended: the record is honest, and
  "Adopts" remains available while they are fixed.
- This repository is itself affected: SCM-6 and GOV-17 are unmet because it has one maintainer (see
  [docs/sdlc](../sdlc/README.md)).

### Confirmation

The structure check (`tools/check_structure.py`) and two separate AI-assisted reviews of the README on 2026-11-01,
directed by the owner (not independent while SCM-6 is unmet), checked that the rules agree with each other; the first self-assessment (due 2026-11-15) applies them to this repository.
