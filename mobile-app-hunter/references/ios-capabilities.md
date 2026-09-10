# iOS capabilities, data lifetime, and local authentication

## Contents
- Keychain and data protection
- Shared containers and extensions
- Local authentication versus transaction authority
- Retention, notifications, and privacy surfaces

Background: [Apple security and API references](sources.md#apple),
[OWASP mobile standards](sources.md#mobile-standards).

## Keychain and data protection

Keychain is not a single undifferentiated security guarantee. Item accessibility,
access-control constraints, access-group identity, synchronization policy, and the
specific operation matter. Determine whether the source configuration, owner diagnostic,
and observed item refer to the same build and principal. Do not read one successful
Keychain call as proof of all protection attributes.

Data Protection classes concern availability of protected file data under device
conditions. File location, protection class, unlocked/locked state, and existing open
handles can affect interpretation. Do not claim a universal before-first-unlock or
after-lock property without the applicable API contract and relevant observations.
Encryption does not itself establish correct object authorization or secret lifetime.

Do not assume uninstall deletes every Keychain item or that a particular retention
behavior automatically violates the product contract. Account identity, logout promises,
reuse after reinstall, accessibility, and backend session invalidation are distinct.
An app may intentionally retain a non-sensitive preference while promising to delete
confidential content. Classify the object, not just the storage API.

## Shared containers and extensions

Use effective signed entitlements for both collaborators. A shared App Group can be
appropriate for a host and its extension. The important questions are permitted
membership, intended shared data, access lifetime, and how each process authenticates
business identity when consuming that data.

Keychain access groups and App Groups are not synonyms. A file-container permission
does not establish permission to a particular Keychain item. A matching string in
two project files is not proof of effective signed group membership in production.
Also distinguish local container authorization from server-side account permissions.

An extension may read a smaller projection of an object than the host. Review the
actual fields and approved use rather than declaring every interprocess copy a leak.
If the supplied contract forbids a field and the supplied finite records show that
field was retained in an unauthorized destination, preserve that narrow discrepancy.
Do not invent additional readers or exfiltration channels.

## Local authentication versus transaction authority

LocalAuthentication may mediate user presence or device-owner authentication under
a selected policy. That is not automatically a signature over a particular operation
or proof that a remote service authorized the named account. Distinguish a UI result,
Keychain access control, key-use authorization, and server transaction validation.

The policy may intentionally permit a passcode alternative. Calling that an unexpected
bypass without checking the product promise and selected policy is a false conclusion.
A successful prompt likewise does not prove that its result is correctly bound to a
later operation. Source binding and operation identity are required evidence.

App Attest or another attestation signal is a separate server-consumed assurance.
Its presence in the app does not show that the backend verifies the relevant context,
freshness, identity, or policy. A failure on an unsupported simulator is not evidence
that the released service is insecure. Record which layer remains unassessed.

## Retention, notifications, and privacy surfaces

Trace confidential objects through files, caches, backups, web storage, logs, crash
records, notifications, pasteboard, and shared extensions where the app uses them.
OS controls and user settings may change visibility; verify the selected environment
rather than asserting an evergreen default.

Privacy manifests, permission purpose strings, and consent UI document or request
behavior. They are not substitutes for an access-control mechanism or proof of actual
network/data behavior. Conversely, a missing optional hardening flag is not automatically
a bounty-eligible privacy disclosure. Keep compliance and demonstrated security effects
separate while documenting both accurately.

For logout and deletion claims, examine the exact promised lifecycle: local cache
removal, revoking remote sessions, cancelling pending tasks, and expiring shared state
need not happen through the same component. A disappeared screen settles none of the
others by itself. Use owner-controlled records without retaining personal data.
