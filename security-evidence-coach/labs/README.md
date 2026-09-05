# Defensive specification models

These two small, correct-by-contract teaching models contain no intentionally
vulnerable counterpart, exploit payload, network client, or third-party target.
They make abstract distinctions executable without teaching vulnerability
reproduction. They are not production security libraries.

```bash
python labs/test_models.py
```

Run from the skill directory. All operations are in-memory and use the Python
standard library. The tests exercise finite contract examples; no model is called.

## Permission model

[policy_model.py](policy_model.py) represents owners and explicitly shared reads.
An authenticated principal is not automatically entitled to another record. An
explicit applicable share can authorize a cross-tenant read. Principal identity
includes tenant as well as name.

The model assumes already-verified principal and grant records. It does **not**
verify authentication, cryptographic signatures, grant issuance, revocation timing,
network requests, or persistence. Constructing a ReadGrant object in an application
would not authenticate a grant. Do not use this model as deployable middleware.

Compare the finite expected permission relation in [test_models.py](test_models.py)
with the implementation. The oracle comes from the written contract, not a copied
implementation expression. Explain which assertion isolates each property and
which unmodeled layers would remain unknown in a real review.

## Transition model

[transition_model.py](transition_model.py) describes a pure, sequential adjustment
ledger. An operation identity commits once; a conflicting amount is rejected.
Distinct adjustments preserve the intended total irrespective of sequential order.

Tests check idempotency, conflict rejection, immutable input state, and permutations
of a finite set. This is a specification model, not a database transaction or a
concurrent implementation. Passing it does not prove race freedom, crash durability,
isolation, or correct operation identity in a deployed service.

## Suggested teaching discussion

Explain why the permission matrix can support its finite contract without certifying
an unseen HTTP handler. Explain why sequential idempotency does not establish
concurrent atomicity. Identify the observation and specification used by each test.

Do not create an exploit version to make the exercise more exciting. The point is
to learn what a defensive argument establishes and where its premises stop.
