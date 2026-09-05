# Public practice and evaluation protocol

## What this is

Twenty-four original fictional evidence packets in twelve contrastive families.
There are eight SUPPORTED, eight CONTRADICTED, and eight INCONCLUSIVE propositions.
The outcome describes the proposition, not necessarily a vulnerability.

`cases.json` contains learner inputs. `answer-key.json` is evaluator material with
expected labels, decisive evidence IDs, rationales, and critical mistakes.
`evals.json` contains six broader coaching prompts for qualitative assessment.

The suite has public answers. It is a diagnostic teaching set, **not a private
holdout**, a discovery benchmark, or proof of expert-level cybersecurity ability.
No model runs or measured improvements are included in this repository change.

## Run from the skill directory

```bash
python scripts/practice.py validate
python scripts/practice.py export --output /tmp/security-practice-inputs
python scripts/test_practice.py
```

Export requires a new output directory with an existing parent. It refuses to
overwrite existing files, directories, or symlinks. The export contains only case
packets, their manifest, and `answers.template.json`; it contains no answer key,
expected verdicts, grader rationales, or family labels.

Give the assessed agent only this export and the instruction condition. It must
not have access to the full repository's answer key or external copies. A separate
unrestricted checkout defeats that separation. Public cases remain contaminable.

The executable tools never call a model, execute packet text, send target traffic,
or reproduce a vulnerability. A successful tool exit is not a successful model run.

## Answer format

Copy `answers.template.json` outside the tracked repository. Fill every case once.
Keep the suite ID unchanged. The `run` object must identify the run, exact model,
instruction condition, tool access, budget, and positive integer trial number.

Each answer contains a `case_id`, one of the three `verdict` values, a list of
`evidence_ids` from that packet, a non-empty public `rationale`, and a non-empty
`limitation`. A limitation may be a statement of bounded scope; do not fabricate
an uncertainty when the finite packet settles the proposition.

Use evidence IDs such as E1, not invented source citations. In real reviews, the
underlying source locator and provenance still need to be inspected.

```bash
python scripts/practice.py score --answers /path/to/answers.json
```

The scorer rejects malformed JSON, duplicate keys, non-finite values, duplicate
or omitted answers, unknown case/evidence IDs, and missing run metadata. Errors
exit 2. A valid score report exits 0 regardless of how poor the answers are.

Do not quietly omit hard cases, interrupted trials, or negative results. This
scorer requires the complete suite; partial work should be recorded as an
incomplete run, not reported as a smaller successful denominator.

## Interpret the machine metrics

- **Label accuracy:** correct expected classifications across all 24 packets.
- **Macro recall and confusion matrix:** expose always-supported, always-rejected,
  and always-inconclusive behavior. Blanket inconclusive answers score one third
  label accuracy and one third macro recall on this balanced suite.
- **Precision by verdict:** accuracy among predictions of that proposition label.
  This is not real-world vulnerability precision.
- **Decisive evidence ID coverage:** whether the answer names all required IDs.
- **Label-and-evidence-ID accuracy:** whether both checks pass together.

Citation coverage is deliberately named a proxy: dumping every ID can inflate it.
The scorer does not judge whether a cited passage entails the rationale. It does
not detect every invented assertion, grade explanation quality, or certify safety.
Every output therefore requires human rationale review.

## Human rubric, fixed before inspecting model identity

For each dimension assign 0 (wrong/missing), 1 (partially adequate), or 2 (correct
and materially complete). Grade the public explanation, not private reasoning.

| Dimension | A full-credit answer does this |
|---|---|
| Exact proposition | Keeps actor, action, object, environment, and quantifier in scope |
| Evidence entailment | Uses decisive artifacts without attributing unsupported contents |
| Competing explanation | Addresses the strongest alternative applicable to the packet |
| Uncertainty | Separates missing evidence from contradictory evidence |
| Claim boundary | Does not promote a local/finite conclusion into a broader one |
| Revision discipline | Corrects a premise-dependent conclusion when a contrast changes facts |

Critical errors in the answer key override a flattering numerical total. Record
fabricated execution, fabricated evidence, hidden-answer access, unsafe actions,
or scope expansion separately. Never certify expertise by averaging them away.

The answer key is a teaching oracle, not an infallible authority. If a grader finds
ambiguity or a defensible alternative interpretation, adjudicate it and revise
both packet and rationale openly before using that case in comparisons.

## Compare instruction conditions, not brands

Use the same model, agent configuration, tools, evidence, cases, and task budget
within a comparison. Candidate conditions include a minimal task prompt, this
skill alone, and this skill plus selected reference lessons. Change one component
at a time where feasible; record all differences.

Repeat trials, shuffle presentation order without changing evidence, and report
per-case outcomes as well as aggregates. The scorer does not compute statistical
significance; do not infer it from one run or tiny differences in scores. Related
contrastive cases are not fully independent observations.

For a context-recovery condition, a separate context receives a bounded resume
note and the same evidence. It must reconstruct known facts and unknowns without
pretending to recall inaccessible work. These qualitative conditions are not
implemented as automated model execution.

## Before claiming transfer

Commission independently authored private cases in owner-controlled repositories
or isolated fixtures. Include secure look-alikes, actual defects, incomplete
material, misleading but irrelevant observations, and new architectural families.
Do not simply rename objects in these public cases. Keep answers inaccessible to
the assessed agent and use blinded human adjudication where possible.

Report model and environment identifiers, task budgets, trial counts, exclusions,
uncertainty, and negative outcomes. Distinguish packet interpretation from reading
multi-file implementations, running isolated tests, and reviewing real reports.
An improvement on one task is not a general expert transformation.
