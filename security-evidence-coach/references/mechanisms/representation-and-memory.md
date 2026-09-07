# Representation, canonical identity, and native interfaces

## Meaning must survive the boundary

Two strings can denote the same logical object, and the same displayed name can
refer to different generations or contexts. A system's validation, permission,
storage, cache, and consuming layers need an applicable identity relation. They do
not necessarily need byte-for-byte equality everywhere; the contract defines what
transformations preserve meaning.

Canonicalization is not a magic guarantee. Determine which representation the rule
covers and which representation the consumer uses. A serializer preserving the
intended logical identity is different from a second parser applying an unrelated
interpretation. Do not infer a defect merely because two libraries represent a value
differently; establish the security-relevant semantic requirement.

## Types can clarify or hide assumptions

At an SDK/native interface, identify units and ownership. A length can count bytes,
characters, elements, or capacity. A buffer may be immutable, borrowed, owned, or
retained by an asynchronous operation. A range check does not establish that the
buffer remains alive; safe ownership does not establish that a separate length uses
the correct unit.

Bounds, lifetimes, arithmetic, and authorization are distinct properties. Memory-safe
application code can still violate a permission contract. A native boundary can be
correct when its explicit bounds and ownership requirements are satisfied. The
presence of a native call is not evidence of a memory defect.

## Contrast

A fictional adapter constructs an immutable byte snapshot, derives its length in
bytes from that same snapshot, and transfers both under a documented synchronous
ownership rule. The provided implementation can support that local contract. If a
platform adapter is missing, the contract for that adapter remains unknown rather
than inheriting the result of the one supplied.

A separate logical-key example defines identity as `(workspace, normalized_name)`.
Different workspaces do not collide under that relation. A display-only normalization
cannot establish the storage key's identity. Look for the stated relation and selected
conversion, not a list of unusual input encodings.

## Evidence and test scope

An interface header expresses a contract; binding code connects values to it;
consumer documentation supplies retention semantics. A unit test with only basic
text may establish less than its name suggests. A correct test of the selected
conversion still does not validate an unavailable native implementation.

Tests should specify the expected relation independently and include relevant normal
boundary conditions of the contract in isolated models. Do not treat test mutation or
an invented replacement implementation as proof about the designated product.

## Transfer question

Keep the type `length` but change its documented unit from bytes to elements. Which
composition argument breaks, and which observations remain true? The point is unit
consistency, not the spelling of the parameter or the confidence of a type annotation.
