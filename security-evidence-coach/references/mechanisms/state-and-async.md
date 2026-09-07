# State, asynchronous work, and temporal guarantees

## State identity includes context

A logical operation needs an identity domain. A local key can be unique within a
workspace without being globally unique. An object name may refer to a different
generation after replacement. Review the identity that the contract actually uses,
not merely the human-facing label repeated in a log.

Delivery attempts, acknowledgments, and committed effects are distinct events.
At-least-once delivery can coexist with one committed effect when the effect layer
recognizes the same logical operation. A timeout alone establishes neither rollback
nor successful commitment. A later compensating action does not erase the fact that
an earlier effect occurred; whether compensation satisfies the contract is separate.

## Which time owns the decision?

A product might authorize at acceptance, at worker execution, or at final delivery.
It might promise immediate revocation or a documented lease interval. Those are
alternative contracts, not interchangeable best practices. An observation becomes
meaningful only relative to the selected contract and relevant event order.

Serializability concerns equivalence to a serial ordering of transactions;
linearizability additionally constrains operations by real-time order at their
interface. Do not infer either from ordinary sequential unit tests. The designated
storage and synchronization mechanisms determine which guarantee is applicable.

## Contrast

A fictional adjustment service promises one committed adjustment per `(workspace,
operation_id)`. Its complete journal records two delivery attempts referring to the
same committed effect: no duplicate effect follows. Two distinct committed entries
for that same identity contradict the stated finite property. Two records in different
workspaces do not contradict a per-workspace uniqueness contract.

If the retained artifact contains only acceptance messages, committed-effect count
remains unresolved. The proper next evidence request is the authoritative effect
record, not a declaration of either exactly-once correctness or double execution.

## Evidence dependencies

For a temporal assertion, identify the relevant event, correlated operation identity,
policy or object version, and source of order. Unsynchronized clock labels do not
supply a global ordering. A single authoritative sequence can establish an order in
a finite history without proving every possible execution follows it.

Distinguish safety (a forbidden state is not reached) from liveness (required progress
occurs). A system can preserve permissions by refusing all work and still fail its
availability or progress contract. Neither property substitutes for the other.

## Transfer question

Change a contract from acceptance-time snapshots to execution-time permission checks.
Which prior conclusions depend on the old time rule? Preserve recorded facts and
revise the compliance argument; do not rewrite timestamps or invent a grace period.
See [temporal authority](../temporal-authority.md) for additional evidence examples.
