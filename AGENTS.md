# Reporting-agent orchestration

This repository contains portable Agent Skills and specialist agent contracts for authorized vulnerability-report writing. It begins after discovery: do not use it to turn an unvalidated suspicion into a report.

## When running the reporting pipeline

1. Read `agents/manifest.json`.
2. Use `reporting-orchestrator` as the parent role.
3. Delegate with the complete canonical prompt from `agents/<agent-name>.md`.
4. Persist every delegation in a handoff artifact following `agents/assets/handoff.template.json`.
5. Respect each role's read/write scope and freshness requirement.
6. Keep the canonical attacker model and demonstrated impact stable across handoffs.
7. Do not flatten the independent triage reviewer into the author's context.
8. Allow platform adaptation only after a hash-matching `READY` review.
9. Allow `PACKAGE_READY` only after the final package auditor checks the complete attachment set.

## Certification boundary

- Only `independent-triage-reviewer` may issue vulnerability-report `READY`.
- Only `final-package-auditor` may issue `PACKAGE_READY`.
- Neither agent may edit the artifact it certifies.
- The orchestrator, writer, hardener, and specialists never self-certify.

## Agent selection

Always use:

```text
reporting-orchestrator
evidence-curator
canonical-report-writer
report-hardener
independent-triage-reviewer
```

Use specialists only when material:

```text
proof-reproduction-verifier   exact-path proof or controls are uncertain
impact-severity-analyst       impact or rating may change
variant-radius-analyst        affected radius matters or is disputed
remediation-engineer          authoritative fix is unclear
novelty-route-policy-analyst  scope, route, policy, current state, or novelty needs live evidence
disclosure-safety-reviewer    report or attachments may contain sensitive material
```

After a READY review, use `platform-submission-adapter`, then `final-package-auditor`.

## Codex and other harnesses

Treat each canonical Markdown file as the subagent's developer/system prompt. Start a new isolated task for roles whose manifest entry says `fresh_context: required`. Give the reviewer only final artifacts and raw evidence—not the author's hidden deliberation or desired verdict.

## Repository development

When modifying this repository rather than running a report workflow:

- preserve standard-library-only validators;
- keep agent prompts harness-neutral;
- update `agents/manifest.json`, adapters, tests, README, and CI together;
- never add private program material or undisclosed vulnerability details to examples.
