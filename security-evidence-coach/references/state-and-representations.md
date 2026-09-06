# State, time, and identity representations

This reference explains why local observations may not establish whole-system
properties. Use supplied state diagrams, source contracts, and recorded traces.
Background: [state and concurrency references](sources.md#state).

## A snapshot is not a transition guarantee

"The state was valid when read" and "the operation preserves the invariant" are
different propositions. A system can validate a condition and later act under a
different state. Alternatively, an authoritative atomic operation may preserve
the property despite a stale preliminary read.

For a supplied state argument distinguish the precondition, transition, commit
point, and postcondition. The unit that must be indivisible is the unit protecting
the invariant, not necessarily the whole user-facing workflow.

The existence of a lock, transaction, or retry is not proof by itself. Its scope,
shared resource, isolation contract, and effect on the supplied transition matter.
Avoid universal claims about all databases or all transaction isolation levels.

## Acceptance, commitment, and observation

An asynchronous acknowledgment can mean queued, accepted for validation, or
completed. Determine which meaning the contract assigns to the observed event.
Do not infer a committed effect from an acceptance status. Do not infer failure
from an early empty read when visibility may legitimately lag commitment.

An event trace needs correlation with the operation and revision being assessed.
An unrelated successful event is not a substitute. An error after a committed
effect does not undo the effect unless an authoritative rollback is established.

## Idempotency is a scoped property

Idempotency means repeating an operation has the intended repeat behavior within
its defined identity and retention domain. A key's existence does not prove that
the effect and the key are committed consistently. Two operations that merely
share a string are not necessarily the same logical operation.

Review supplied contracts for what defines identity, when a result is final, and
what a retry is allowed to repeat. Do not equate "the service retries" with
"duplicate effects are possible," or "the key was recorded" with "duplicates
are impossible." Both need the relevant transition argument.

## Identity is an equivalence relation, not a cosmetic choice

Let x ~ y mean that the contract treats two representations as the same logical
object. Every security-relevant use of that identity must respect the intended
equivalence, or explicitly operate in a different namespace.

The important comparison is between the identities used by the decision and the
effect. It is not simply whether a normalization function exists. Normalizing an
opaque identifier can itself merge objects that should remain distinct.

Do not assume every string should be lowercased, decoded, trimmed, or normalized.
First establish the namespace contract. A human-readable name, a signed byte
sequence, and an opaque identifier can have different equivalence rules.

## Caches and derived state

A derived view is trustworthy only for the properties its invalidation and
freshness contract preserve. Caching an object and caching a permission decision
are not identical operations. A stale view may be a permitted display limitation
or a security-relevant failure, depending on which authoritative decision uses it.

Distinguish the cached value, namespace, subject, policy revision, and intended
lifetime. A cache key that looks elaborate is not automatically adequate. A short
key is not automatically incorrect when a surrounding cache instance supplies
the missing namespace. Supplied architecture matters.

## Bounded reasoning exercise

Given a trace where two observers read the same initial state, do not conclude
that both later effects committed. Look for the authoritative final transition
record in the packet. When it is missing, preserve the ambiguity. When a complete
atomic-transition contract excludes the second effect, do not invent a failure
outside that model to avoid changing your conclusion.

## Limits of generalization

One successful run can demonstrate one outcome. It cannot prove the absence of
all scheduling-sensitive failures. Conversely, a complete proof over a small
formal transition model does not automatically cover the production system.
State exactly which model, implementation revision, and environmental premises
make the conclusion valid. This is precision, not timid wording.
