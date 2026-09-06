# Temporal authority, revocation, and state interpretation

Use supplied contracts and recorded histories. These are defensive reasoning
lessons, not concurrency probes or instructions for attacking running services.
No universal consistency or authorization policy is assumed.

## A permission is about more than a principal name

An applicability argument may depend on actor, action, object identity, object
generation, policy version, and decision time. Which dimensions matter is defined
by the actual contract. A read grant need not authorize export. A grant for an old
object need not authorize a replacement that reuses the same display identifier.
A tenant name alone need not identify the resource's ownership domain.

Treat identifiers according to the system's declared identity relation. Do not
assume all strings should be lowercased, all aliases are equivalent, or every
representation difference is a security difference. Canonicalization must preserve
the intended distinctions as well as collapse intended equivalences.

### Worked example: reuse is not continuity

A fictional catalogue identifies documents by `(workspace, number, generation)`.
Document `(W, 7, 2)` is deleted and `(W, 7, 3)` later appears. The contract states
that grants bind all three components. A permission for generation 2 is not
permission for generation 3. This is a statement about the contract, not proof
that an implementation mishandles reuse.

If the only supplied record contains number 7 without a generation, an assessment
of grant applicability is unresolved. Do not guess the generation from order of
presentation or reuse a previous assessment's object identity.

## Revocation needs a time contract

"Revocation works" is underspecified. A contract might require new operations to
be denied after an authoritative revocation barrier, permit already-authorized
operations to finish, or allow an explicitly bounded propagation interval. These
are different guarantees. The reviewer must not silently switch between them.

For the fictional contract "operations beginning after barrier B use policy
version 12 or later," a trace needs an order relating operation start to B and a
record of the effective policy version. A wall-clock label alone may not provide
that order when clocks or buffering differ.

A barrier record is useful only if the supplied system defines what it orders.
An application log saying "revoked" is not automatically a barrier across every
replica, cache, worker, and outstanding request.

### Contrastive history

History A has a single authoritative sequencer: barrier B at sequence 80,
operation start at 81, decision under policy version 12 denying the revoked grant.
This supports compliance for that operation under the stated contract.

History B records a request accepted before B and a response after B. The contract
allows pre-barrier work to finish. Completion after B alone does not establish a
revocation failure.

History C has timestamps from two uncorrelated clocks and no effective policy
version. Ordering and applicability remain unknown. Neither favorable prose nor
an arbitrary grace period can settle it.

## Happens-before is not log-file order

Logs can be buffered, duplicated, sampled, or merged. Sequence numbers establish
order only within their documented domain. Per-worker sequences do not define a
global order without additional relationships. Causal dependency and a confirmed
acknowledgment chain can establish a partial order even when wall clocks differ.

Keep three questions separate: what was requested, what was decided, and what
became authoritative state. A total order is not required for every question;
use only the order relationships the proposition needs.

## At-most-once effects are not exactly-once delivery

Two message deliveries may produce one effect. One acknowledgment may precede no
effect. A timeout can occur after a durable effect, and a retry can return the
stored result without repeating it. Count authoritative effects under the
contract's operation identity, not response lines or delivery attempts.

A durable idempotency record may be scoped to a namespace, principal, or request
body. Its lifetime and conflict semantics matter. A statement that an identifier
is "the same" needs the full domain in which equality is defined.

A sequential reference model proves neither concurrent atomicity nor recovery
across a process crash. Those are separate implementation obligations. Do not
infer them from one-thread tests or from the name of a database transaction.

## Cache correctness is relational

A cache hit needs to be applicable to the same decision question as a fresh
calculation. Depending on the contract, this can require matching principal,
resource generation, action, policy epoch, and environment. A cache key's visible
length is not proof of correctness; omitted dimensions may be carried elsewhere,
or may genuinely be absent. The supplied composition evidence must settle that.

A stale positive permission and a stale display label are not the same failure.
Describe the security-relevant decision that depends on cached state. Do not
classify ordinary eventual consistency as an authorization failure without the
relevant guarantee and consequence.

## Rollback and compensation are different

A rolled-back operation never becomes committed state in the specified store. A
compensated operation committed and was later offset. Compensation can restore a
balance without undoing every externally observed consequence. Conversely, an
intent record alone does not prove a committed change.

For a supplied incident history, distinguish intent, acceptance, commit, delivery,
compensation, and final observation. Missing one event does not imply it never
occurred unless the retained record is complete for that event class and interval.

## What an expert answer should contain

Name the identity and time relation the proposition uses, cite the applicable
contract and correlated records, and limit the conclusion to that history. Do
not demand a complete distributed-system proof for a finite factual question.
Do not let a finite factual answer imply a universal guarantee.

Related: [state and representations](state-and-representations.md),
[multi-artifact reasoning](multi-artifact-reasoning.md), and
[advanced worked lessons](advanced-worked-lessons.md).
