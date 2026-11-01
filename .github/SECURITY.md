# Security policy

This repository holds a standard (text) and a few tools that check it: `tools/check_structure.py`, `tools/check_citations.py`
and the GitHub Actions workflows in `.github/workflows/`. A vulnerability here is most likely in a tool or a workflow, for
example a way to make the citation checker fetch or run something it should not, or a workflow that leaks its token.

## Supported versions

Only the latest release and the `trunk` branch are supported. Fixes are not back-ported to earlier versions: upgrade to the
latest release for fixes.

## Reporting a vulnerability

Please do not open a public issue or pull request for a vulnerability. E-mail **sssomeshhh+oss@gmail.com** instead, with:

- what is affected (file, workflow or version);
- how to reproduce it;
- what an attacker could do with it.

You will get an acknowledgement within 7 days.

## How a report is handled

1. **Triage.** Within 30 days of the report, the maintainer confirms whether it is a vulnerability and how severe it is, and
   tells you the result.
2. **Fix.** A confirmed vulnerability is fixed on `trunk` and in the next release; the fix is recorded in the
   [CHANGELOG](../CHANGELOG.md).
3. **Disclosure.** The vulnerability is described publicly once a fixed release is available, or 90 days after the report,
   whichever comes first. You are credited unless you ask not to be.

Mistakes in the standard's text or its quotes are not security issues: please use the issue templates for those.
