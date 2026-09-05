# Teaching judgment and measuring transfer

The methods below are design proposals, not measured claims about any model.
The package has not been evaluated on GPT, Claude, GLM, or other model families.
Background reading is recorded in [sources](sources.md#learning).

## Teach decisions, not slogans

An instruction to "be skeptical" is underspecified. Show what the competing
explanations are, why a tempting shortcut fails, and which fact changes the
conclusion. Explain the public argument; do not ask for hidden chain-of-thought.

Use three stages:

1. Explain a single distinction with one worked contrast.
2. Present a changed example without a verdict and obtain an evidence-based answer.
3. Give feedback on the decisive premise, then use a structurally different case.

A learner that repeats the original verdict has not demonstrated transfer. A
learner that recognizes why a changed premise changes the outcome has provided
more useful evidence of understanding.

## Contrastive teaching

Pair superficially similar records with different security meanings. Pair a
plausible concern with an authoritative protection, an observation failure with
a valid negative result, and a local effect with an unsupported stronger claim.

Do not arrange every pair so the first case is defective and the second safe.
Do not put verdicts or "secure/vulnerable" labels in learner-visible filenames.
Do not define every example so continued effort necessarily produces a finding.

Include supported, contradicted, and inconclusive propositions. These labels refer
to the proposition, not universally to a vulnerability: a supported proposition
may establish that a particular protection applies.

## Fade scaffolding, not evidence standards

A beginner may need a glossary and explicit dependency questions. A stronger
reviewer may need only the evidence and the task. Keep the same conclusion
standards while removing redundant hints.

Do not infer ability from branding. Record the exact model identifier, agent
configuration, accessible tools, instruction condition, and task budget for each
comparison. An unavailable tool should be represented as unavailable, not silently
replaced with imagined execution.

## Retrieval by uncertainty

Choose references based on the missing concept. Consult authority guidance when
identity and permission are conflated; observation guidance when a negative result
is being treated as proof; state guidance when a snapshot is used as a transition
guarantee. Reading every reference for every case is not necessary.

A useful micro-lesson states the concept, its applicability conditions, the common
false positive, the common false negative, and one changed example. Avoid growing
a list of universal rules from a single incident.

## Evaluate behavior separately from software

A unit test establishes a property of the exporter or scorer. It does not establish
that a model can analyze a real codebase. A correct label on a supplied packet is
not evidence of independent discovery or safe live-system operation.

The [evaluation protocol](../evals/README.md) separates machine-checkable results
from human judgment. Do not announce "expert-level performance" from CI success.

Public practice exercises can diagnose common errors. They cannot serve as a
secret holdout, and rewording their nouns does not make them independent cases.
Before making capability claims, have an independent author prepare new private
owner-controlled cases, including different architectures and incomplete evidence.

## Fair comparisons and leakage

Compare matched conditions: model, tools, case set, accessible evidence, and budget.
Change one instruction component at a time where feasible. Use repeated trials;
record failed or interrupted runs instead of quietly removing them.

The assessed model must not receive the answer key. Running it in a checkout that
contains the key invalidates a blind evaluation unless access is independently
restricted. Exported inputs reduce accidental leakage, not deliberate access by a
model with a separate unrestricted checkout.

Human graders should use a predeclared rubric and, where practical, be blind to the
model and instruction condition. Disagreements should be adjudicated on artifacts,
not resolved by counting model votes.

## Error-directed maintenance

Classify errors before changing the skill: missing domain knowledge, missed supplied
artifact, invalid inference, premature certainty, fabricated execution, or scope
confusion. Fix the smallest reusable teaching gap and add a regression case.

Measure whether the correction harms other cases. More instructions can create
anchoring and contradictions. Preserve a correction history so the next edit does
not remove a distinction merely because it looks bureaucratic.

## Context recovery

A compact resume note should preserve artifact locators and unresolved dependencies,
not just a verdict. Evaluate resumption with a new context given only that note and
the same permitted evidence. Check whether it reconstructs the scope and unknowns
without inventing work from the missing context.

This supports continuity; it is not an instruction to run indefinitely or continue
an offensive workflow. A well-justified stop is sometimes the correct outcome.
