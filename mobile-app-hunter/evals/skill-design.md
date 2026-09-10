# Skill design and authoring checks

## Research basis

The completed 2026-09-09 research cites Anthropic's `skill-creator` for concise
triggering metadata, progressive disclosure, deterministic helpers and baseline
comparisons. [Source and limits](../references/sources.md#skill-creator).
The URL points to a moving branch; no upstream commit was retained. This package
therefore documents its concrete choices instead of claiming official approval
or a complete audit against every current Anthropic requirement.

## Operational core

The pre-install skill name is `mobile-app-hunter`: the research proposed that name,
and it better matches the intended role of architecture-first hunting judgment.
Because the skill had not been merged, released, or installed under the earlier
working name, no compatibility alias is retained. Its scope remains Android-first
with a distinct iOS path. The description should trigger for APK, AAB, IPA,
entitlement review, mobile bug-bounty assessment, architecture-first hypothesis
generation, and mobile threat modeling before a suspected vulnerability is supplied.
Ordinary feature work and report-formatting tasks should not be diverted here.

The core stays below the existing package's 220-line budget. This is a local
maintenance choice, not a universal Anthropic requirement. References are directly
linked from SKILL.md. The main task never requires a quiz, answer key or source
registry form; those support teaching and maintenance separately.

## Degrees of freedom

Allow judgment when explaining responsibilities and choosing material questions.
Use deterministic code for metadata validation, byte hashing and learner exports.
Do not replace mechanism knowledge with rigid vulnerability-name checklists.
Explain why a rule matters and what evidence would make it applicable.

No helper invokes a model, executes evidence text, contacts targets, installs apps
or obtains credentials. The research validator checks source metadata, dates and
local references; it cannot certify source truth, freshness or app behavior.
A valid hash establishes bytes, not independent review.

## Progressive teaching

A reader who already understands a mechanism can skip its worked examples. A
less-experienced reader can use one relevant contrast, then apply the principle
to a changed architecture. Keep actual source limits close to the claim. Do not
teach an Android bridge guarantee as an Apple rule or conflate intended sharing
with broken isolation.

[Research transfer tasks](research-transfer.md) begin with a system rather than
an identified bug. Copy only that learner document for an initial attempt; retain
[the instructor guide](research-transfer-instructor.md) separately. Public tasks
are not held-out benchmarks after their explanations have been read.

## Evaluation and maintenance

Compare with-skill and baseline runs using matched model, tools, revision, task,
resource budget and output format. Repeat runs; inspect variation and concentrated
errors. Human review should reward relevant question selection and defensible
arguments, not response length, tool count or the number of findings.

The original eight-project corpus and existing test contracts are preserved.
The new paper exercises supplement rather than silently alter those test inputs.
No model run or measured capability gain is claimed. Software tests cover the
package; research status records what was actually sourced and what remains open.
