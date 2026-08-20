# Portable reporting agents

This directory contains harness-neutral agent contracts for the vulnerability-reporting pipeline. Each Markdown file is a complete specialist prompt: mission, inputs, allowed writes, prohibitions, and handoff requirements.

The contracts are deliberately separate from runtime configuration:

- Claude Code wrappers live in `.claude/agents/`.
- Codex can use the repository-level `AGENTS.md` and delegate with the canonical agent file as the subagent prompt.
- Pi and other harnesses can register the canonical Markdown files directly and use `agents/manifest.json` for tool, sandbox, freshness, and artifact scopes.

## Core agents

| Agent | Responsibility |
|---|---|
| `reporting-orchestrator` | Route work, maintain pipeline state, and enforce separation of duties. |
| `evidence-curator` | Normalize final evidence into the portable report bundle. |
| `canonical-report-writer` | Write the canonical report and claim manifest without expanding evidence. |
| `report-hardener` | Integrate evidence-backed improvements from specialists. |
| `independent-triage-reviewer` | Fresh-context final certification; the only agent allowed to issue report `READY`. |
| `platform-submission-adapter` | Map a READY report into a live destination contract. |
| `final-package-auditor` | Verify report, review, adaptation, attachments, and redactions as one package. |

## Specialist agents

| Agent | Responsibility |
|---|---|
| `proof-reproduction-verifier` | Re-run or independently inspect the exact proof and negative controls. |
| `impact-severity-analyst` | Re-derive impact and severity from demonstrated evidence. |
| `variant-radius-analyst` | Verify affected siblings, transports, versions, and representations. |
| `remediation-engineer` | Identify the authoritative fix and regression control. |
| `novelty-route-policy-analyst` | Verify scope, ownership, proof acceptance, and closest semantic matches. |
| `disclosure-safety-reviewer` | Check secrets, private material, personal data, safe-harbor, and redaction. |

## Separation rules

1. The orchestrator coordinates but does not certify.
2. Writers and hardeners may change `report.md`; reviewers never do.
3. Specialist conclusions are artifacts, not hidden conversational advice.
4. Final triage review uses a fresh context and the finished report, not the author's advocacy narrative.
5. Only `independent-triage-reviewer` may emit `READY`, `BLOCKED`, or `PROVISIONAL` for the vulnerability report.
6. `final-package-auditor` may emit `PACKAGE_READY`, but that status means the submission package matches an already READY report; it does not re-certify the vulnerability.
7. Every handoff follows `agents/assets/handoff.template.json` and names exact input and output artifacts.

## Default graph

```text
reporting-orchestrator
        |
 evidence-curator
        |
canonical-report-writer
        |
  report-hardener
   /   |   |   \
proof severity radius remediation
   \   |   |   /
 novelty/route + disclosure-safety
        |
independent-triage-reviewer
        |
platform-submission-adapter
        |
 final-package-auditor
```

Specialists are invoked only when their evidence would change readiness, radius, proof, severity, route, remediation, or disclosure safety. The orchestrator should not spawn all specialists mechanically on trivial reports.

## Artifacts

Use stable filenames unless the user supplies another workspace contract:

```text
pipeline-state.json
report-input.json
evidence-index.json
report.md
report-manifest.json
proof-review.json
severity-review.json
radius-review.json
remediation-review.json
route-policy-review.json
safety-review.json
hardening-record.json
review.json
submission.md
adaptation-manifest.json
attachment-plan.md
package-audit.json
handoffs/*.json
```

The canonical report remains the semantic source of truth after review. Platform adaptation may change presentation, never the validated claim.
