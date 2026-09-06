# Identity, permission, and delegation

## The guarantee is a relation, not a boolean adjective

Authentication establishes an identity under a stated authentication mechanism.
Authorization decides whether a principal may perform an action on an object in
a context. A proof of the first does not settle the second. Conversely, a difference
in tenant identity is not automatically unauthorized when explicit sharing exists.

A useful model is `permit(principal, action, object, context)`. The arguments matter.
A permission to read a summary may not include export, mutation, or every stored
field. A workspace-level role may require an object relation as well. Determine the
actual combining rule rather than assuming any deny or any allow always dominates.

## Follow delegated responsibility

A service may execute using a worker identity while acting for a human requestor.
The worker's technical ability to fetch data is not the requestor's entitlement to
receive it. Equally, a service performing an administrative operation under its
own explicitly granted authority is not necessarily impersonation. Read the contract.

In supplied source, identify where the relevant principal and object are resolved,
where the permission relation is decided, and which projection is emitted. Active
composition connects those responsibilities. A shared repository adapter can enforce
object access correctly even when the handler is deliberately thin.

## Contrast

A fictional portal allows the owner and an explicitly shared viewer to read a
public projection. `handler -> permission_adapter -> projection` is the complete
selected composition. A handler excerpt alone omits the rule; that is missing context.
With the adapter's source and active binding, the rule can be assessed. With only an
unselected adapter example, the same source does not establish runtime enforcement.

If the share relation includes READ but not EXPORT, applying the READ conclusion to
EXPORT would change the proposition. If the contract authorizes both, the same
cross-workspace access can be intended. The decisive distinction is permission scope,
not whether the situation resembles a familiar vulnerability name.

## Evidence that matters and its limits

A policy table explains intended behavior. Selected code explains an implementation.
A correlated decision record establishes one actual decision if its provenance and
meaning are settled. A successful login does not establish object permission. A deny
for an anonymous fixture may never exercise the object-level decision at all.

Ask what proves the particular operation used the supplied rule and whether any
stated exceptions apply. Do not invent a hidden guard to rescue a mismatch, and do
not infer a missing guard from an incomplete excerpt. Avoid concluding all routes
are equivalent from one sibling's result.

## Transfer question

Move enforcement from middleware to a storage adapter without changing the relation.
Which source locators change, and which property stays the same? A sound assessment
tracks the authoritative relation across the move rather than treating the absence
of a local function call as the property itself.
