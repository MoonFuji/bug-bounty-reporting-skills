# Mobile assessment evidence and responsible conclusions

## Contents
- What is established at each stage
- Build and actor fidelity
- Controls and negative observations
- Continuing without inventing progress
- Handoff to reporting

Background for verification structure: [OWASP MASVS/MASTG](sources.md#mobile-standards).
This chapter proposes an assessment method; it does not certify a program's acceptance policy.

## What is established at each stage

An archive inventory establishes metadata for supplied bytes. Decoded declarations
establish configuration in that artifact. Source or decompiled analysis explains a
possible path under its assumptions. A selected runtime binding connects that path to
an operation. An observation establishes the bounded effect it actually captured.
No earlier stage silently implies every later stage.

For a material question connect product contract, principal, object, active component,
policy, state transition, and observation. Some claims can be settled in supplied source;
others need runtime evidence. Be explicit about which kind of conclusion is justified.
A model's confident annotation is not a substitute for reading the relevant material.

## Build and actor fidelity

Separate ordinary user, another unprivileged app, device owner, debug operator,
root/jailbreak instrumentation, app process, and server administrator. Do not transfer
capabilities between these actors. A changed signer can alter platform relationships;
a debug build can change network trust; a missing split can omit the assessed feature.
Record material deviations rather than burying them in a footnote.

The product may have legitimate sharing or delegation. An unusual path is not
necessarily unauthorized. Conversely, authentication success is not evidence of
object permission. The contract and effective principal decide the question.

## Controls and negative observations

For supplied tests ask what was supposed to vary, which behavior the test actually
reached, and what its observation mechanism could detect. A fixture rejected at login
does not test later object authorization. A missing callback from an unverified capture
is inconclusive. A 200 response can be an echo or public content; an error can occur after
a committed effect. Retain operation identity and ordering where relevant.

Negative evidence is strongest when the bounded observation channel is applicable,
functioning, and complete for the exact proposition. None of those qualities comes
from a file named proof.txt. Do not require infinite proof of absence: scope the
conclusion to the available record and identify the remaining dependency.

A secure implementation and a recorded discrepancy are both legitimate learning outcomes.
Do not require every exercise or app review to yield a finding. Do not reward blanket
abstention when the supplied facts settle the question.

## Continuing without inventing progress

Resolve an uncertainty rather than repeatedly listing generic mobile weaknesses.
When one question settles, preserve its evidence and the next relevant open question.
Do not duplicate the campaign skill's state machine. A normal note with immutable
locators is enough for context recovery.

If a required permission, device, release artifact, or server record is unavailable,
continue on independent questions within scope and mark the blocked one explicitly.
Do not classify missing capability as a disproved vulnerability or bypass an access
restriction to make the assessment look complete.

## Handoff to reporting

Report observed configuration separately from established security significance.
Distinguish a local app behavior, an OS property, an SDK integration issue, and backend
object authorization. A warning about an optional defense is not a demonstrated impact.
A signed artifact's identity is not a claim about all published versions.

A final report needs the exact app/build/runtime, relevant actor and object, supported
path, evidence, limitations, responsible owner, and current disclosure contract.
Redact tokens and personal data while keeping reproducibility of the explanation.
Do not attach a private binary or third-party account dump to a public issue.

Current scope, proof acceptance, and novelty must be checked separately. Shared
root causes across Android/iOS or multiple surfaces are not automatically separate
findings. A public no-match result says nothing definitive about private submissions.
The reporting skills retain their own input and final-review requirements; this skill
never declares submission readiness from its metadata tools or practice results.
