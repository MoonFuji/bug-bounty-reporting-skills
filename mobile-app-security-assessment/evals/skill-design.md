# Skill design and authoring checks

The user requested an Anthropic-style Agent Skill. Live official documentation could
not be retrieved. These are explicit design choices, not a claim of current Anthropic
review or approval. External pointers are in [sources](../references/sources.md#skill-authoring).

## Progressive disclosure

The only required instruction file is SKILL.md with lowercase hyphenated `name` and
a descriptive `description`. It names Android APK/splits/AAB and iOS IPA/source, when
the skill should trigger, and the work it does. No provider-specific tool identifier
or agent API is required. Optional agents/openai.yaml is metadata, not a dependency.

The core gives the app-first path and routes directly to one-level reference files.
It does not require reading every mechanism, completing a classroom exercise, or
creating a JSON ledger before assessment. Each substantial reference has a short
contents section. An experienced reader can consult one uncertainty; a novice can use
a worked contrast without inheriting a new mandatory workflow.

## Degrees of freedom

Architecture explanation and question selection allow judgment and evidence-backed
alternatives. Byte hashing and learner export are deterministic optional scripts.
Neither their exit status nor a populated note certifies vulnerabilities. No script
runs shell commands, installs apps, invokes models, or executes exercise text.

## Acceptance tests for the skill, not claims of expertise

Structural tests check metadata, core size, local links, source-status honesty,
project coverage, safe exports, and tool behavior. Human evaluation checks whether
a model identifies relevant questions in unfamiliar designated mobile material.
Passing software tests does not establish model skill.

## Trigger and non-trigger examples

Should trigger: assess this designated APK; review these iOS entitlements with app
source; explain whether a split set is complete; assess a supplied mobile claim.
Should not replace: ordinary app feature work; web-only report formatting; provider
account support; public target acquisition; autonomous exploitation or submission.

## Change management

Keep original exercises stable once published. Add new project IDs for structural
variants. Do not rebrand public answers as a private benchmark. Prefer a measured
improvement on fixed tasks over more pages or stronger claims in the description.
