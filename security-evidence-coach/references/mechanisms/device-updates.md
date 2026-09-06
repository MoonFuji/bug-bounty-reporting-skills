# Device updates and attestation assurances

## An update has several distinct acceptance questions

Authenticity of a package, identity of its contents, compatibility with a device,
authority to deploy it, freshness or rollback policy, and safe activation are separate
responsibilities. An authentic older package may or may not be permitted by policy.
A newer package is not automatically authentic or compatible. State the device class,
component, version domain, and selected acceptance policy.

A root of trust identifies the basis of a verification argument. It does not answer
every operational question after verification. A measured state, approved state,
installed state, and actively executing state can be different propositions. Read
what an attestation actually measures and when, and what the relying party authorizes.

## Time and recovery are part of the contract

Rollback prevention can be strict, conditional, or explicitly permit recovery images.
An update interrupted before activation may leave the old version active by design.
A receipt saying stored does not establish activated. A recovery mechanism is not
necessarily a bypass; its intended authority and exceptions need their own evidence.

Do not infer hardware protections, fuse settings, boot behavior, or isolation from
an emulator alone. Emulation and mocked verification can establish a software model's
behavior while leaving hardware-bound guarantees unresolved. Missing hardware is an
assessment limitation, not proof of either safety or failure.

## Contrast

A fictional controller accepts a signed package for device family F and component C,
with an approved version under its recovery policy. A measurement record identifies
what actually booted. These artifacts can support different parts of the acceptance
argument. A signature for F does not establish compatibility with another family G,
and a stored-package receipt does not establish which component is executing.

If a recovery exception explicitly authorizes version V under a recorded operator
approval, merely observing V does not contradict strict normal-update monotonicity:
first establish which policy mode governed the operation. Without the mode binding,
the compliance question can remain unresolved.

## Evidence that connects the assurances

Relevant supplied artifacts can include the package subject, trusted key policy,
device identity, selected compatibility rule, monotonic state, recovery approval,
and post-activation measurement. No one artifact should be relabelled as all of them.
A signed measurement of a narrow component does not attest to an entire product.

This chapter is a conceptual assessment aid, not firmware exploitation or device
control guidance. The project track uses fictional records, not device commands.

## Transfer question

A relying service changes from accepting an approved package identity to requiring
an observed boot identity. Which artifact is newly necessary? Explain why unchanged
signature verification does not, by itself, satisfy the changed question.
