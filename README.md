# Bug Bounty Reporting Skills and Agents

A portable reporting stack for turning finalized vulnerability evidence into clear, reproducible, triager-ready disclosures.

The repository begins **after discovery**. It does not turn suspicious code into a finding and it does not lower proof, scope, ownership, novelty, or authorization gates. Give it a finalized evidence bundle or a validated candidate from an upstream hunting workflow.

## Included skills

| Skill | Job |
|---|---|
| [`write-vulnerability-report`](write-vulnerability-report/) | Turn validated evidence into one self-contained canonical report without inventing impact. |
| [`harden-vulnerability-report`](harden-vulnerability-report/) | Improve radius analysis, reproduction reliability, severity accuracy, and remediation while preserving the evidence boundary. |
| [`review-vulnerability-report`](review-vulnerability-report/) | Run a fresh-context, triager-minded final review and issue `READY`, `BLOCKED`, or `PROVISIONAL`. |
| [`adapt-vulnerability-report`](adapt-vulnerability-report/) | Adapt a canonical final report to a live platform or upstream disclosure contract without changing its claim. |

## Portable agent layer

The repository now includes 13 agent types under [`agents/`](agents/). The canonical Markdown contracts are harness-neutral; runtime adapters point to them instead of maintaining divergent prompt copies.

### Core agents

| Agent | Responsibility |
|---|---|
| `reporting-orchestrator` | Route work, persist pipeline state and handoffs, and enforce separation of duties. |
| `evidence-curator` | Normalize final evidence and identify evidence owed. |
| `canonical-report-writer` | Write `report.md` and its claim manifest. |
| `report-hardener` | Integrate evidence-backed specialist improvements. |
| `independent-triage-reviewer` | Fresh-context final certification; the only agent allowed to issue report `READY`. |
| `platform-submission-adapter` | Map a READY report to the live destination contract. |
| `final-package-auditor` | Fresh-context audit of hashes, adaptation, attachments, and redactions. |

### Specialists

| Agent | Responsibility |
|---|---|
| `proof-reproduction-verifier` | Verify the exact path, observed effect, and controls. |
| `impact-severity-analyst` | Re-derive impact and severity in either direction. |
| `variant-radius-analyst` | Verify affected siblings, transports, versions, and representations. |
| `remediation-engineer` | Identify the authoritative fix and regression control. |
| `novelty-route-policy-analyst` | Verify live scope, route, proof acceptance, current state, and semantic novelty. |
| `disclosure-safety-reviewer` | Check secrets, personal data, private material, and safe disclosure. |

Specialists are invoked only when their evidence can materially change readiness, radius, proof, severity, route, remediation, or disclosure safety.

## Recommended pipeline

```text
validated candidate / evidence bundle
                |
       reporting-orchestrator
                |
         evidence-curator
                |
    canonical-report-writer
                |
          report-hardener
        / proof | severity \
 radius | remediation | route/policy | safety
                |
 independent-triage-reviewer
                |
      READY canonical report
                |
 platform-submission-adapter
                |
      final-package-auditor
                |
 platform-ready submission package
```

The canonical report is the semantic source of truth. Platform adaptation may reorder, shorten, or split fields, but it must not add impact, broaden scope, change severity, change route, or omit limitations.

## Installation

Install the four Agent Skills:

```bash
npx skills add MoonFuji/bug-bounty-reporting-skills --list
npx skills add MoonFuji/bug-bounty-reporting-skills
```

Clone the repository when using the portable agents and adapters:

```bash
git clone https://github.com/MoonFuji/bug-bounty-reporting-skills.git
cd bug-bounty-reporting-skills
```

### Claude Code

Project subagent wrappers are committed under `.claude/agents/`. For global use:

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/*.md ~/.claude/agents/
```

The final reviewer and package auditor must start in fresh contexts.

### Codex

Codex reads the repository-level [`AGENTS.md`](AGENTS.md). Delegate with the complete canonical file from `agents/<name>.md` as the role prompt and persist a handoff artifact.

### Pi and other harnesses

Register the canonical prompts directly and configure them from [`agents/manifest.json`](agents/manifest.json). Export a bundle when useful:

```bash
python scripts/export_agent_bundle.py --format json --output build/reporting-agents.json
python scripts/export_agent_bundle.py --format jsonl --output build/reporting-agents.jsonl
python scripts/export_agent_bundle.py --format plain-dir --output build/reporting-agents
```

See [`adapters/`](adapters/) for integration guidance.

## Separation of duties

- The orchestrator coordinates but never certifies.
- Only the writer and hardener may change `report.md`.
- Specialist conclusions are persisted artifacts, not hidden conversational advice.
- The independent triage reviewer cannot edit the report it certifies.
- Only `independent-triage-reviewer` may emit `READY`.
- Only `final-package-auditor` may emit `PACKAGE_READY`, which certifies package consistency—not the underlying vulnerability again.
- A requested report change invalidates the review hash and requires a new final review.

## Canonical input

`write-vulnerability-report/assets/report-input.template.json` defines the portable evidence bundle. The writer also accepts a validated `candidate.json` from the Invariant-First Bug Bounty skill:

```bash
python write-vulnerability-report/scripts/from_invariant_candidate.py \
  candidate.json \
  report-input.json
```

The converter refuses non-reportable, self-certified, or review-owed candidates.

## Mechanical checks

```bash
python -m compileall -q .
python scripts/validate_repo.py
python scripts/validate_agents.py
python scripts/test_validate_agents.py
python scripts/test_validate_agent_handoff.py
python write-vulnerability-report/scripts/test_validate_report.py
python review-vulnerability-report/scripts/test_validate_review.py
python harden-vulnerability-report/scripts/test_validate_hardening.py
python adapt-vulnerability-report/scripts/test_validate_adaptation.py
```

Validate a persisted handoff:

```bash
python scripts/validate_agent_handoff.py handoffs/H-001.json
```

Validate a finished report and final review:

```bash
python write-vulnerability-report/scripts/validate_report.py \
  report.md \
  --manifest report-manifest.json

python review-vulnerability-report/scripts/validate_review.py \
  review.json \
  --report report.md
```

## Design rules

- **Evidence before prose.** A polished sentence cannot repair an unproven claim.
- **One canonical claim.** Title, summary, severity, reproduction, review, and platform adaptation describe the same demonstrated capability.
- **Limitations remain visible.** A load-bearing limitation blocks readiness; an ordinary limitation constrains scope or severity and stays in the report.
- **No process leakage.** Reports do not expose internal gate names, candidate fields, model deliberation, or agent metadata.
- **Stable references.** Repository links point to immutable revisions, not moving branches.
- **Fresh final review.** The author may self-edit, but final certification is performed by a separate context or a human on the frozen report.

## Scope and safety

Use these skills and agents only for authorized research and coordinated disclosure. Never include live credentials, third-party personal data, private program material, or undisclosed vulnerability details in public examples, issues, or pull requests.

## License

MIT. See [LICENSE](LICENSE).
