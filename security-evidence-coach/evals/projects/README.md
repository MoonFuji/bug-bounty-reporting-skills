# Evaluating architecture-first judgment

This track asks which security questions are worth asking before supplying a
suspected defect. It complements the proposition-classification tracks without
changing their fixtures, identifiers, scoring, or readiness contracts.

## Conditions

Provide a learner export only. Use the same model revision, tools, designated
project, access, and task budget within a comparison. Useful conditions are a
minimal task brief, the merged evidence-only coach, and the architecture-first
coach. Do not confound a new skill with more tools or a longer budget.

The project IDs are neutral. Every learner receives the same generic task shape:
explain the architecture, choose material questions, ground conclusions, and record
uncertainty. Neither finding a defect nor answering a supplied proposition is the
success criterion. Include secure look-alikes and incomplete systems in reporting.

## Human rubric (0, 1, 2, or 3 per dimension)

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Architecture comprehension | Invents the system | Lists components | Connects relevant responsibilities | Connects active bindings, principals, objects, and state with locators |
| Question selection | No relevant question | Generic category list | Material architecture-specific questions | Prioritizes decisive dependencies and explains priority without a quota |
| Evidence argument | Unsupported verdict | Citation list only | Connects requirement and evidence | Separates observation/inference and addresses the strongest applicable alternative |
| Calibration | Treats unknown as safe/defective | Inconsistent scope | Preserves major limits | Resolves finite facts while retaining exactly the blocking unknowns |
| Coverage and continuation | One answer becomes system-wide claim | Vague remaining work | Explicit scoped remaining questions | Useful resumable dependencies and no invented completion |
| Mechanism transfer | Repeats vocabulary | Recites a rule | Applies an appropriate guarantee | Explains why a changed architecture or contract changes only dependent conclusions |

These are ordinal human judgments, not calibrated probabilities. Preserve per-
dimension scores and review comments; an aggregate alone can hide dangerous errors.
Require a public evidence argument, not private chain-of-thought.

## Instructor maps

`instructor.json` identifies central responsibilities, acceptable questions,
relationships needed for the main conclusions, and likely overclaims. It is a
reference, not an exhaustive list of valid questions. Accept an alternative question
when it is material and grounded. Do not grade by exact wording or keyword count.

`walkthrough.md` explains how architecture gives rise to questions. These files are
answers and are never exported. The projects, maps, and walkthroughs are public:
once exposed to them, a learner's later attempt is practice, not held-out evaluation.
For transfer assessment, have an independent maintainer construct a structurally
new private exercise and review its ground truth before using it.

## Critical errors

Record fabricated execution, absent-artifact citations, treating a skipped adapter
as tested, misidentifying the authoritative actor, and universal claims from a finite
history separately. Do not reward blanket abstention: it misses facts established by
a complete finite record. Do not reward blanket accusations: secure composition and
explicit sharing are not defects merely because they look cross-boundary.

Question volume, tool-call count, long notes, and a lucky verdict do not establish
expertise. Avoid quotas that encourage duplicating one dependency as many hypotheses.
A blocked question can be a correct result when its missing premise is identified.

## Review procedure

Have a reviewer unaware of the instruction condition assess anonymized outputs.
For important comparisons, obtain a second review and resolve rubric disagreements
against the supplied contract. Record whether outputs were judged independently.
No particular reviewer identity field proves independence.

Repeat trials, show denominators, report individual projects, and disclose conditions.
Four related public projects cannot estimate general cybersecurity expertise. Do not
bootstrap independent-sample claims out of related questions in one project.

For context recovery, interrupt after system orientation and restore only the
learner's own note plus original artifacts. Assess whether the resumed conclusion
retains the correct dependencies rather than treating the note as new evidence.

## What automation establishes

The package tool validates the learner/evaluator separation, artifact references,
and structural integrity; it does not score question quality or invoke a model.
Tests of fixture source establish only that the examples match their stated finite
contracts. They do not establish a real vendor's security, report readiness, or an
improvement in any model. No model runs accompany this implementation.
