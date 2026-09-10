# Network, sessions, and server authority

## Contents
- Client policy versus observed transport
- Pinning and modified environments
- Session and object authority
- Attestation and integrity signals
- Ownership and reportability

Background: [Android networking](sources.md#android), [Apple ATS and networking](sources.md#apple),
[native protocol background](sources.md#protocols). No current platform defaults are asserted.

## Client policy versus observed transport

Map each observed request to its actual client implementation and destination policy.
An app may use platform networking, native libraries, WebViews, and multiple SDK clients.
An Android network-security configuration or iOS ATS dictionary may not govern every
one of these paths in the same way. A domain exception and a global exception are
not interchangeable. Debug-only overrides cannot silently be treated as release policy.

Distinguish transport encryption, certificate-chain validation, hostname validation,
application-level authentication, and object authorization. HTTPS in a URL string is
not proof the selected client enforced all relevant checks. A supplied successful
connection does not reveal unobserved failure behavior. On the other hand, a broad
configuration warning does not prove confidential data actually used that path.

For a supplied TLS observation retain build identity, client path, peer context, trust
store modifications, debug status, and what the observation establishes. Do not upload
raw authenticated traffic or credentials. Use owner-provided redacted records when
runtime access is unavailable.

## Pinning and modified environments

Certificate/public-key pinning is an additional policy, not a synonym for TLS. Its
absence is not automatically a confidentiality vulnerability. Its presence is not
proof the app correctly authorizes records or that every network stack applies it.
Evaluate the actual product requirement and threat model.

Bypassing a protection with a rooted/jailbroken device or modified binary does not
establish that an ordinary external actor can do the same. This skill does not provide
pinning-bypass, hooking, or jailbreak instructions. When inspection needs a different
build or trust configuration, obtain an owner-authorized development artifact and
label the limitation. A laboratory modification must not disappear from the report.

## Session and object authority

Mobile clients cannot be assumed to enforce the server's object or role policy.
A local UI restriction may be usability or defense in depth rather than the authoritative
control. Seeing an operation identifier or hidden button in a binary is not evidence
that the backend accepts unauthorized operations.

Distinguish access-token lifetime, refresh-token lifetime, local logout, remote revocation,
account switching, and offline retry behavior. A token-like string is not proof it is
usable; do not try discovered credentials. Read server contracts or supplied owner
records when the claim depends on server validation. Unknown server behavior stays unknown.

For an observed cross-account result establish the principal, object ownership,
app-selected account, server-authorized identity, and returned projection. Shared/public
objects and stale UI display are alternatives to evaluate, not excuses to assume away
an actual documented boundary failure.

## Attestation and integrity signals

Play Integrity, App Attest, device checks, and signature verification can contribute
signals under defined contracts. A client invoking an API does not prove the server
uses its result correctly. A local check's absence does not by itself establish server
compromise, and a negative result on an unsupported device does not prove a defect.

Identify the proposition: app artifact provenance, device state, request binding,
freshness, or business authorization. Those are different assurances. Do not transform
an attestation concern into an account or payment claim without separate evidence.
Do not generate an operational bypass to resolve missing documentation.

## Ownership and reportability

Separate the app, OS, SDK provider, identity provider, and backend. The component that
contains a string is not necessarily the owner of the defective decision. A shared
backend issue observed on two clients is not automatically two distinct root causes.
A third-party SDK version identifies a dependency, not proof that a cited advisory's
necessary path and configuration exist in the assessed app.

Current scope and proof acceptance must come from the current program, not this guide.
Keep a technical impact assessment distinct from reward caps, exclusions, and likelihood
of payment. No universal mobile severity or bounty table is provided here.
