# Instructor walkthrough: questions emerge from architecture

Instructor material: read after an independent attempt. No exploit procedure is
provided. These are explanations of finite fictional design/source assessments.

## Atlas

Begin with the product's sharing contract, not the phrase multi-tenant. The requestor
is a session principal, object authority is the ownership/share relation, and field
visibility is the summary projection. Assembly connects both operations to the
permission adapter. These relationships motivate questions about action-specific
permission, active enforcement, and the emitted fields.

Connect the explicit grant in records.json to the permission function and EXPORT
binding. The cross-workspace reader is allowed by the stated contract; the unrelated
visitor is denied. Read the projection rather than assuming that possession of a
record means every field is disclosed. The finite supplied design is consistent
with these properties. Do not declare future routes safe or ignore the selected
adapter because the handler is small.

This is the secure look-alike. A learner insisting that every project has a defect
will often misclassify intended sharing or invent a missing authorization layer.

## Delta

The architecture separates acceptance, attempts, identity, and commitment. The
contract and identity function establish a per-workspace logical operation, while
assembly names the complete journal as authoritative. This motivates a uniqueness
question at the effect layer, not at the receipt layer.

The two red/J7 committed rows have distinct effect IDs and the journal explicitly
rules out duplicate renderings. They contradict the one-effect promise in W4.
The blue/J7 row is a different logical operation. Acceptance messages by themselves
would not prove this conclusion. The packet contains no worker interleaving or SQL;
claiming a particular race, transaction bug, exploit method, or real-world impact
would go beyond the supplied evidence.

This is an established finite inconsistency, not an invitation to manufacture a
vulnerable service or demonstrate an offensive workflow.

## Beacon

Identify the distinct guarantees: authenticated builder statement, artifact identity,
audience-specific promotion policy, and installation. This yields questions about
selected policy and applicable release approval without presupposing a broken signature.

The build statement is verified for staging, but the retained event does not identify
the promotion audience or active policy. Approval and installed-artifact records are
also absent. Therefore production compliance is unresolved. Under the supplied
staging policy the build role could be appropriate; under production a release
approval is required. Neither possible configuration is evidence that it was active.

A good note names those missing bindings, preserves the verified build fact, and
does not infer either production authorization or a production violation.

## Cedar

Start from the SDK/native division of responsibility. The product specifies bytes,
immutable snapshot ownership, synchronous non-retention, and a separate public view.
Questions about units, lifetime, platform binding, and projection arise from these
contracts, not from a generic assertion that native code is dangerous.

The desktop encoder derives length from the exact UTF-8 byte snapshot. Both retained
examples match this local contract; metadata omits raw text. Mobile selection/source
is missing, so desktop correctness cannot be generalized to both platforms. The
native contract is a supplied premise, not cryptographically attested or empirically
verified by a Python unit test.

Cedar is a mixed outcome: settle what is established and preserve the genuinely
missing platform evidence. Blanket safe, blanket unsafe, and blanket unknown all
lose useful distinctions.
