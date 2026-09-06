# Claim discipline for bug-bounty reporting

This companion does not validate a new live target or replace the reporting
pipeline. It teaches how to preserve the meaning of supplied evidence.
Background: [reporting and severity sources](sources.md#reporting).

## Separate four questions

**Technical behavior:** what happened under the recorded conditions?
**Security meaning:** which protected property and actor capability changed?
**Disclosure ownership:** which project or destination owns the relevant fix?
**Program treatment:** what rules apply to submission, severity, or reward?

These questions interact but are not interchangeable. A low reward cap does not
reduce demonstrated technical impact. A valid technical concern does not establish
that a particular bounty program accepts it. A public repository is not evidence
of permission for live testing.

## Describe the smallest complete claim

An executable effect does not automatically establish a service-level consequence.
A source defect in a dependency does not prove reachability in every consumer.
A local process result does not establish higher privilege or host-level impact.

Narrowing is justified only when a smaller **security-relevant** proposition is
supported. It is not a way to preserve a finding after its entire security meaning
has disappeared. Keep the dropped extension explicit; do not retain its language
in the title or severity justification.

Do not treat an evidence-level enum as a substitute for this reasoning. Different
properties need different evidence. Some can be established by a complete source
argument; others depend on runtime conditions that source alone cannot settle.
The destination's proof requirements remain a separate question.

## Limitations versus blocking unknowns

An ordinary limitation bounds a supported claim: the supplied evidence covers
one revision, one operation, or one configuration. A blocking unknown is a missing
premise of the claim itself: whether the caller had permission, whether the exact
operation occurred, or whether the tested code is the claimed deployment.

Preserve this distinction even in unstructured notes. Putting both into a string
list does not make them equivalent. A report should not state an unknown as a
fact and then attempt to repair it with a contradictory footnote.

## Related work and duplicates

A matching title, weakness label, endpoint, or payload shape does not by itself
establish a duplicate. Compare the security boundary, cause, violated invariant,
affected revision, and effect at the granularity justified by the artifacts.
Different surface wording can describe the same cause; similar wording can hide
a material implementation difference.

Record whether a search completed, returned a relevant match, or was unavailable.
An attempted request is not a completed search. A clean public search cannot
establish the contents of a private duplicate pool. Treat private visibility as
unknown rather than converting it to an invented zero or a confident risk score.

When a close match exists, explain the material similarity or distinction using
both artifacts. When evidence is insufficient, say so. A plausible differentiator
is not evidence that no other researcher submitted the same issue privately.

A fix on a newer branch and a deployed older revision can coexist. State which
revision each artifact covers before deciding whether a concern is already fixed.
Do not automatically discard an affected supported release solely because a future
or unrelated branch differs; do not claim a current defect from an old snapshot.

## Semantic consistency is not substring consistency

The report title, effect description, severity, reproduction record, limitations,
and remediation must describe the same proposition. Merely containing the right
sentence somewhere does not make the rest of a report consistent with it.

Likewise, a matching SHA-256 can establish byte identity when the digest provenance
is trusted. It does not establish evidence truth, reviewer independence, or
correct severity. Final review must inspect the actual report, not just its hash.

## Remediation and regression interpretation

A recommended fix should restore the identified property at its authoritative
layer while preserving intended behavior. A passing regression check supports
only what its assertions and exercised paths actually cover.

A test that repeats the implementation's assumption can pass while missing the
specification. A test that changes the expected answer to match current behavior
has not independently validated the intended property. Explain the oracle: what
contract makes the asserted result correct?

## Handoff

Transfer observed facts, established inferences, artifact locators, and visible
limitations to the existing reporting skills. Keep practice scores and coaching
notes out of a real submission. Do not fabricate a validated input bundle merely
because a training packet received the label SUPPORTED.
