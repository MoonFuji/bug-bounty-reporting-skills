# Bug Bounty Reporting Skills

A portable Agent Skills collection for turning validated vulnerability evidence into clear, reproducible, triager-ready disclosures.

The reporting pipeline deliberately starts **after discovery**. It does not decide whether a suspicious behavior is a vulnerability and it does not lower proof, scope, ownership, or novelty gates. Give it a finalized evidence bundle or a validated candidate from an upstream hunting workflow. The optional Security Evidence Coach teaches assessment judgment separately; a practice result is not validated reporting input.

## Included skills

| Skill | Job |
|---|---|
| [`write-vulnerability-report`](write-vulnerability-report/) | Turn validated evidence into one self-contained canonical report without inventing impact. |
| [`harden-vulnerability-report`](harden-vulnerability-report/) | Improve radius analysis, reproduction reliability, severity accuracy, and remediation while preserving the evidence boundary. |
| [`review-vulnerability-report`](review-vulnerability-report/) | Run a fresh-context, triager-minded final review and issue `READY`, `BLOCKED`, or `PROVISIONAL`. |
| [`adapt-vulnerability-report`](adapt-vulnerability-report/) | Adapt a canonical final report to a live platform or upstream disclosure contract without changing its claims. |
| [`security-evidence-coach`](security-evidence-coach/) | Teach evidence-based security judgment with contrastive lessons, fictional practice packets, and defensive specification models; never certify expertise or report readiness. |

## Recommended pipeline

```text
validated candidate / evidence bundle
                |
    write-vulnerability-report
                |
   harden-vulnerability-report
                |
   review-vulnerability-report
                |
    READY canonical report
                |
    adapt-vulnerability-report
                |
 platform-ready submission package
```

The canonical report is the source of truth. Platform adaptation may reorder, shorten, or split fields, but it must not add impact, broaden scope, change severity, or omit load-bearing limitations.

## Optional learning companion

[`security-evidence-coach/SKILL.md`](security-evidence-coach/SKILL.md) is a separate teaching and defensive-review aid, not an extra mandatory pipeline gate or an autonomous hunting workflow. Its short core routes a model to deeper explanations only when relevant.

It includes twelve worked contrastive families, 24 fictional evidence packets, six qualitative evaluation prompts, an evaluator-only answer key, an offline exporter/scorer, and two executable defensive specification models. It distinguishes observed facts, inferences, and unknowns; authentication from authorization; missing observations from valid negative results; and technical impact from program treatment.

```text
Use $security-evidence-coach to assess this supplied security claim.
Cite the decisive artifacts, explain the strongest alternative,
and separate blocking unknowns from ordinary limitations.
```

From the repository root:

```bash
python security-evidence-coach/scripts/practice.py validate
python security-evidence-coach/scripts/practice.py export --output /tmp/security-practice-inputs
python security-evidence-coach/scripts/test_practice.py
python security-evidence-coach/labs/test_models.py
```

Give assessed agents only the export and the chosen instruction condition, not the answer key. The public cases are teaching material, not a private capability benchmark. The scorer does not invoke models or grade the truth of prose; human rationale review is required. No measured improvement on any model is claimed. See the [evaluation protocol](security-evidence-coach/evals/README.md).

Live web research was unavailable when this companion was authored. Its [source register](security-evidence-coach/references/sources.md) labels external reading links as unverified; examples are original and synthetic, not copied bounty reports.

## Installation

After the repository is published:

```bash
npx skills add MoonFuji/bug-bounty-reporting-skills --list
npx skills add MoonFuji/bug-bounty-reporting-skills
```

Each skill is self-contained and can also be copied individually into an Agent Skills directory.

## Canonical input

`write-vulnerability-report/assets/report-input.template.json` defines the portable evidence bundle. The writer also accepts a validated `candidate.json` from the Invariant-First Bug Bounty skill; use:

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
python write-vulnerability-report/scripts/test_validate_report.py
python review-vulnerability-report/scripts/test_validate_review.py
```

Validate a finished report:

```bash
python write-vulnerability-report/scripts/validate_report.py \
  report.md \
  --manifest report-manifest.json
```

Validate an independent review:

```bash
python review-vulnerability-report/scripts/validate_review.py \
  review.json \
  --report report.md
```

## Design rules

- **Evidence before prose.** A polished sentence cannot repair an unproven claim.
- **One canonical claim.** Every title, summary, severity statement, reproduction step, and platform adaptation must describe the same demonstrated capability.
- **Limitations remain visible.** A load-bearing limitation blocks readiness; an ordinary limitation constrains scope or severity and stays in the report.
- **No process leakage.** Reports do not expose internal gate names, candidate field names, model deliberation, or agent metadata.
- **Stable references.** Repository links point to immutable revisions, not moving branches.
- **Fresh final review.** The author may self-edit, but final certification is performed by a separate context or a human on the final report.

## Scope and safety

Use these skills only for authorized research and coordinated disclosure. Never include live credentials, third-party personal data, private program material, or undisclosed vulnerability details in public examples, issues, or pull requests.

## License

MIT. See [LICENSE](LICENSE).
