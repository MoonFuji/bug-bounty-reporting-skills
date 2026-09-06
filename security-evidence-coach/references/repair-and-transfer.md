# Repair evidence, relational properties, and transfer

This guide reviews existing remediation evidence and isolated teaching artifacts.
It does not supply vulnerability payloads, reproduction recipes, or autonomous
research workflows. The goal is to decide what a defensive result establishes.

## Start from a behavioral contract independent of the patch

A test that restates the implementation can agree with the implementation while
both violate the intended contract. State the required behavior from policy or
specification before inspecting whether the patch and tests satisfy it.

For a fictional owner-scoped read, a finite permission table can be an independent
oracle: owner allowed, explicitly shared reader allowed, unrelated reader denied.
A test that merely expects whatever `may_read()` returned is not an oracle.
A test that verifies the presence of a helper call is not necessarily a test of
its effective decision or applicability.

Keep two questions separate: does the test fail for the behavior it is intended
to detect, and does the corrected implementation satisfy the applicable contract?
A test failure caused by missing dependencies or setup does not establish a
security regression. A green test after removing an assertion establishes even
less. Do not alter the contract to make the implementation look correct.

## A patch is not proof of cause, completeness, or deployment

A patch changing three components and making one test green may establish that
something in the combined change affected the observed behavior. It does not
identify one unique cause without additional isolating evidence.

A regression test can establish one corrected case without establishing every
sibling operation, supported representation, or deployment. Conversely, an
unrelated untested component need not block a claim scoped to the tested case.

A release note says a fix was intended or announced. A build artifact binds code
to an artifact. A deployment record binds an artifact to an environment. None of
those links should be invented. An installed but inactive component does not
necessarily protect the path under review.

### Worked contrast

A supplied contract requires two operations to enforce the same owner relation.
The patch changes both; a recorded table independently checks the six defined
principal/operation combinations at revision R. The deployment manifest selects
R. This supports the finite contract for those combinations and that deployment.

Now remove the second operation from the test record. The evidence can still
support the first operation, but not the original two-operation claim. It does
not prove the second is defective. Narrow the conclusion without laundering the
missing coverage into "tested elsewhere."

## Some properties compare executions

A single execution can show a returned value. A relational property compares
executions or states: the same public inputs should produce the same approved
public observation despite a difference in protected state, for example.

In a fictional deterministic finite model, let public input be identical in two
worlds and protected state differ. If the declared public observations differ,
the stated equality property is contradicted for that pair. If observations match,
the property holds for that pair; it does not follow that it holds for all inputs.

Specify the observer. Equal response bodies do not establish equality of timing,
headers, logs, or later effects unless those are in the defined observation.
Likewise, a difference explicitly allowed by the contract is not a violation of
that contract. A hash equality argument requires assumptions about what bytes
were hashed and what equality is relevant.

This is a lesson about quantified evidence, not a prescription to extract hidden
state from a live service.

## Metamorphic expectations need a justification

When a full expected output is inconvenient, a contract may still imply relations:
reordering independent operations preserves the final total; repeating a recorded
idempotent operation preserves the state; renaming a display label preserves
permission when labels are not identities.

A metamorphic relation is an oracle only when the contract actually implies it.
Not all operations commute; a revoke and a read can be order-dependent by design.
Normalizing case is not a valid equivalence for an identity contract that preserves
case. Do not impose a convenient mathematical property on the wrong system.

The teaching models use finite inputs and explicit assumptions. Passing them does
not verify concurrency, transport, authentication, persistence, or product use.

## Transfer requires structural variation

Changing a tenant name in a memorized example tests recognition more than transfer.
A stronger teaching change moves the authoritative check from a handler to a
shared layer, changes the policy composition rule, or alters what the observation
mechanism can establish. The correct conclusion should follow the facts, not the
surface vocabulary or the presence of a familiar function name.

Use secure examples, incorrect implementations described by supplied evidence,
and unresolved cases. Include conclusions that stay the same when irrelevant
facts change, and conclusions that must change when a necessary premise changes.
Do not force every new artifact to reverse the verdict; sometimes it strengthens
a premise without changing the classification.

## Feedback should target the error, not add generic warnings

If a learner confuses authentication with permission, teach that distinction.
If it misses an object-generation binding, explain identity continuity. If it
correctly identifies an unknown but invents an action, correct the capability
boundary. Do not respond to every error with a longer universal checklist.

A useful correction names the mistaken premise, shows the decisive artifact, and
asks the learner to apply the corrected distinction to one changed example. A
second attempt after feedback is training, not an independent evaluation sample.

Related: [multi-artifact reasoning](multi-artifact-reasoning.md),
[revision drills](../evals/revision-drills.md), and
[teaching and evaluation](teaching-and-evaluation.md).
