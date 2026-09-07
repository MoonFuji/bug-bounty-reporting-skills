# Process authority, files, and resource lifetimes

## Names are not authority

A path names a resource under a resolution context. Effective access depends on the
runtime principal, permissions, namespace, and applicable isolation. A privileged-
sounding helper name does not establish privilege. A process running with more
permissions does not establish that an arbitrary caller can exercise them.

Separate the caller's permission, the helper's effective authority, the requested
operation, and the resource actually selected. An administrative action performed
for an already authorized administrator is not automatically a privilege gain.
A sandbox's existence is not proof that it contains the relevant resource or action.

## Resource identity has a lifetime

A pathname and an already acquired resource handle need not have the same identity
semantics over time. A snapshot, descriptor, or borrowed object is meaningful only
under its ownership and lifetime contract. Review which object an approval covers
and which object the operation uses; do not infer equality from repeated text alone.

At a native or process boundary, copying versus borrowing and synchronous versus
asynchronous use determine who keeps the referenced object alive. A type name or a
length check alone does not establish lifetime. A valid lifetime does not itself
establish that the caller was authorized to request the operation.

## Contrast

A fictional file service accepts only an opaque handle created by its permission
adapter. The selected helper operates on that handle for the approved action. An
assessment of this composition differs from one where only an uncorrelated pathname
appears in both a permission note and an operation record. The latter may need more
identity evidence; it is not automatically proof of a resource-switching defect.

If the product intentionally allows the account owner to modify files within its own
workspace, a modification there can be expected behavior. The relevant question is
which boundary the product promises, not whether file mutation occurred at all.

## Evidence discipline

Use supplied runtime identity, selected helper implementation, resource binding,
and contract. A local run under the reviewer's account cannot establish a production
service's authority. Permission bits in a repository are not the same as a deployed
filesystem's effective policy. Avoid asserting a hidden privilege transition.

The teaching projects do not manipulate the host filesystem, launch helpers, or
reproduce third-party failures. These concepts help interpret designated source and
existing records and choose the right evidence request.

## Transfer question

Change a contract from owned immutable data to borrowed mutable data across an async
boundary. Which lifetime assumption needs to be re-established? Explain separately
from any claim about privilege, execution, or another user's resources.
