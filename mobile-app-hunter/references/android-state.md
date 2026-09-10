# Android data, keys, and local state

## Contents
- Data lifecycle and readers
- Storage and backup
- Key management and authentication
- Account state and persistence
- Logs, UI surfaces, and SDK copies

Background: [Android storage, backup, and Keystore references](sources.md#android),
[OWASP mobile standards](sources.md#mobile-standards). Version-specific behavior is
not freshly verified in this package.

## Data lifecycle and readers

Classify what the app stores, why, for how long, and which actor is forbidden from
reading or changing it. Track the protected object across creation, caching,
sharing, logout, deletion, backup, restore, and background use only where relevant.
This yields more useful questions than searching for every string named token.

App-private data being readable by the app is expected. Reading it through root,
an instrumented process, or an owner-supplied debug interface changes the actor
model. Do not present that access as available to an ordinary unrelated app.
At the same time, a product may promise protection against certain device states;
judge those explicit promises with the appropriate evidence.

## Storage and backup

SharedPreferences, databases, files, caches, and external/shared storage have
separate access and retention properties. Serialization format is not an access
control. Encryption at rest and app sandbox isolation answer different questions.
A file's apparent location must be connected to the actual platform access rules.

Backup and device-to-device transfer are distinct paths whose rules can depend on
OS, target SDK, build configuration, and vendor behavior. A single manifest flag
is not a universal statement about every transfer. Review applicable exclusion
rules and supplied observations. A test on one device does not establish all vendor
behavior. Restore may also reintroduce stale identifiers or invalidate key references;
separate failed recovery from a security failure.

## Key management and authentication

A cryptographic API name does not establish key origin, lifecycle, nonce handling,
permitted operations, hardware protection, or user-authentication binding. Keystore
use does not imply every secret is hardware-backed, nor that authorized app code
cannot request permitted operations. Identify the protection the product actually
claims and the relevant key properties in supplied source or owner diagnostics.

Local biometric success is evidence of a local authentication result under a stated
policy. It is not automatically a cryptographic binding to a specific server action.
Distinguish a UI gate from access-control policy on key use and from server-side
authorization. Do not turn the absence of a biometric prompt into an account-takeover
claim. Avoid treating the mere presence of BiometricPrompt as sufficient protection.

A bundled API identifier or public verification key is not necessarily a secret.
Classify intended role and authority before calling a string a credential. A genuine
secret exposure still does not authorize using it. Preserve minimal redacted evidence
and route it through the responsible owner rather than testing its power live.

## Account state and persistence

An offline queue may outlive logout or account switching. Determine the intended
identity binding of queued operations: captured account, current account, or an
explicit reauthorization requirement. Read persistence and ownership metadata,
not only the current UI account. In supplied records, correlate the logical job,
object owner, server decision, and committed outcome.

A cancellation signal, acceptance status, retry counter, and committed operation
are different events. Stale local display, duplicate delivery, and duplicate committed
effects are different claims. Preserve operation identity and declared retention
semantics before concluding replay or cross-account impact.

## Logs, UI surfaces, and SDK copies

Sensitive data may have additional lifecycles in crash reports, analytics, notifications,
clipboard content, recent-task snapshots, web storage, or third-party SDK caches.
Determine recipient and actual visibility instead of treating all logging or clipboard
use as an automatic vulnerability. Background readers and foreground permissions
are platform-dependent and must be verified for the stated environment.

A scanner identifying a logging call provides a source lead; an actual confidential
value reaching an unintended reader is a different fact. Respect privacy when retaining
records. Demonstrations should use non-sensitive owner-provided markers; never publish
real user data to make a report look stronger.
