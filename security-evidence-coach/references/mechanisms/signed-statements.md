# Signed statements, identities, and authorization

## What signature verification establishes

Under the algorithm's assumptions and the selected key, verification binds a signed
message to that key. It does not, by itself, establish the signer's organizational
role, permission to approve this action, freshness, audience, or suitability of the
signed artifact. Those conclusions depend on additional trusted bindings and policy.

Separate the signed bytes, the claimed subject, the verification key, the identity
bound to that key, and the authority assigned to that identity. These are related
facts, not synonyms for `verified = true`. A valid statement can be irrelevant to the
current decision without any cryptographic algorithm being broken.

## Context matters

An approval for a staging artifact is not necessarily approval for a production
promotion. A signature over metadata about artifact A does not identify artifact B.
An expired policy can change whether a key's endorsement is accepted without changing
whether a signature mathematically verifies. Explicit domain, audience, subject,
version, and validity rules establish applicability when the system requires them.

Do not manufacture claims about algorithms or protocol implementations from this
conceptual model. Use the actual designated verifier, trust configuration, and
statement format. A test double returning true for verification cannot establish a
cryptographic guarantee; it can test how an already settled result is consumed.

## Contrast

A fictional promotion service receives an authenticated statement from an identity
whose allowed role is BUILD. The statement identifies artifact D. The production
contract separately requires a RELEASE approval for D and its production audience.
If the package contains that approval and its active policy binding, the role
requirement can be assessed. With only the build statement, production approval is
not established. An explicit staging-only deployment would answer a different question.

An artifact hash is useful for identity, but hashing an untrusted file does not make
it safe, approved, or reproducibly built. A trusted expected digest and an observed
digest establish equality of identified bytes, not every property of those bytes.

## Useful assessment distinctions

Ask which authority defines accepted issuers, which consumer selects the policy,
and what exact statement the consumer evaluates. Treat a library's verification
result and an application's acceptance decision as different responsibilities.
Key rotation and revocation need their own time semantics; do not assume a universal
instantaneous revocation rule or an automatic perpetual-validity rule.

## Transfer question

Two valid signed statements use the same key but refer to different audiences.
Can one satisfy the other's approval contract? Explain what additional binding is
needed without assuming verification alone decides application authorization.
