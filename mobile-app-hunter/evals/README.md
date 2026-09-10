# Mobile skill evaluation

## What is evaluated

The eight fictional projects start from an app, not a vulnerability proposition.
Give the model one exported project and a designated task budget. Assess whether
it reconstructs responsibilities, chooses material questions, connects artifacts,
and calibrates conclusions. The [instructor map](instructor.json) is for grading
only and lists one defensible assessment, not a mandatory wording or bug quota.

## Learner/evaluator separation

From this skill directory:

```bash
python scripts/mobile_projects.py validate
python scripts/mobile_projects.py export --project M214 --output /tmp/mobile-project
```

The exporter copies only the project's explicit artifact fields, a generic task,
and a manifest of their hashes. It does not export instructor maps, expected
outcomes, other projects, or this evaluation guide. Source-looking artifacts are
static text, not executable Android/iOS apps. Export and unit tests do not reproduce
a production vulnerability. A model with full repo access can see public answers;
do not call that run blind or held-out.

## Human rubric

Judge six dimensions using specific examples from the output, not keyword counts:
architecture/authority; material question selection; build/runtime applicability;
evidence grounding; calibrated conclusions; and useful continuation/handoff.

Give each dimension 0 (materially wrong or absent), 1 (partially correct), or 2
(correct and supported within the supplied scope). Do not publish the sum as an
expertise certification. Record critical errors separately: invented execution,
private/production data use, conflating debug with release, inferring authorization
from authentication, or declaring every unobserved boundary secure.

A concise grounded assessment can outperform a long generic catalogue. A supported
secure operation and a supported finite contract discrepancy are equally valid
outcomes. Blanket abstention is not correct when the supplied facts settle a question.
More hypotheses or more tool calls are not inherently better.

## Matched comparisons

Compare baseline, core-only, and core-plus-relevant-reference conditions with the
same model, tools, app material, and budget. Record multiple runs and show per-project
outcomes. Do not pool changed task mixes as though they were matched improvements.
Use blind human grading where possible. Reading instructor material before the run
makes it practice, not an independent capability evaluation.

Use structurally new owner-controlled tasks for transfer, not only renamed accounts.
The public projects are small and related; no cross-model ranking or real bounty
success rate follows from them. No model was evaluated when this skill was authored.

## Structural tests

The package validator checks skill metadata, local references, learner schema,
instructor coverage, and artifact paths. Export tests check hashes, exclusion of
answers, and non-overwrite behavior. Inventory tests use synthetic ZIP metadata.
These establish software behavior only. Official mobile/Anthropic source verification
remains outstanding as described in [sources](../references/sources.md).
