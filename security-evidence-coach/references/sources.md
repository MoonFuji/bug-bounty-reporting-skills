# Source register and provenance

## Verification status

**Live web research was unavailable during authoring.** None of the external URLs
below was opened or verified in this session. These are background reading pointers,
not evidence of current platform policy, product behavior, or model capability.
Verify availability, revision, and applicability before relying on them.

All worked lessons, fictional artifacts, case packets, and answer rationales in this
skill are original synthetic teaching material. They are not copied public reports,
private research provenance, or claims about a real vendor. No live exploit examples
or third-party vulnerability reproduction code are included.

The method is a proposal. References to learning literature motivate possible
teaching designs; they do not establish that these designs improve an LLM's security
performance. That requires the separate evaluations described in this package.

## Authorization

- OWASP Authorization Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  Background for authorization, least privilege, and enforcing the correct decision.
- MITRE CWE-863, Incorrect Authorization:
  https://cwe.mitre.org/data/definitions/863.html
  Taxonomy context, not proof that any particular handler is defective.
- OWASP Application Security Verification Standard:
  https://owasp.org/www-project-application-security-verification-standard/
  Source of verification requirements. Pin the version used; do not assume latest.

## State

- MITRE CWE-362, Concurrent Execution using Shared Resource with Improper Synchronization:
  https://cwe.mitre.org/data/definitions/362.html
  Background for concurrency reasoning; not a universal test prescription.
- MITRE CWE-367, Time-of-check Time-of-use Race Condition:
  https://cwe.mitre.org/data/definitions/367.html
  Background for distinguishing snapshots from protected transitions.
- OWASP Transaction Authorization Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html
  Background for binding authorization to intended operations.

## Measurement

- OWASP Logging Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  Background for event records, context, and handling sensitive log data.
- NIST/SEMATECH Engineering Statistics Handbook:
  https://www.itl.nist.gov/div898/handbook/
  Background for experimental design and statistical interpretation. No fixed
  significance threshold in this skill is claimed to settle security questions.

## Reporting

- FIRST CVSS:
  https://www.first.org/cvss/
  Versioned severity standards. Select the relevant specification; a platform reward
  cap and a technical score need not describe the same quantity.
- HackerOne reporting guidance:
  https://docs.hackerone.com/en/articles/8473994-submitting-reports
- Bugcrowd reporting guidance:
  https://docs.bugcrowd.com/researchers/reporting-managing-submissions/reporting-a-bug/
  The two links above are starting points only. Actual program rules and current
  forms must be verified separately; this skill states no current acceptance promise.
- NIST SP 800-218, Secure Software Development Framework:
  https://doi.org/10.6028/NIST.SP.800-218
  Background for defensive verification and secure development practices.

## Learning

- Dunlosky et al. (2013), *Improving Students' Learning With Effective Learning Techniques*:
  https://doi.org/10.1177/1529100612453266
  Human learning research, not direct evidence of model improvement. Contrastive
  packets, faded hints, and the evaluation protocol here are author-designed proposals.

## Updating this register

When a source is actually checked, record the source revision or retrieval date,
which claim it supports, and any conditions that limit applicability. Do not add a
"verified" badge merely because a URL exists. Avoid reproducing copyrighted lesson
content or publishing private program artifacts. Public links can also become stale.
