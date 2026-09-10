# Android platform: separate the authorities

## Contents
- Security responsibility map
- Platform and release applicability
- Identity is not a UI state
- Deriving review questions

Background: [Android official references](sources.md#android). Exact defaults and
API requirements must be checked for the selected platform and target SDK.

## Security responsibility map

Begin with the product's protected records and consequential operations. Map the
application's processes, Android components, native libraries, embedded web content,
SDKs, and external services only as far as the chosen question requires.

The OS can mediate app identity, permissions, files, and interprocess calls. The
application still owns its object-level business rules. The server owns remote
object authorization and session policy. These controls are complementary: a valid
OS caller can still lack the right product role, and a logged-in product user does
not automatically gain another app's OS identity.

App sandboxing is not a statement that all app data is confidential against the
user controlling a privileged or modified device. State the actor and privilege
assumptions before evaluating local evidence. Conversely, ordinary sandboxing is
not an excuse to dismiss a sharing or IPC path that intentionally crosses it.

Permissions can guard a component or API without implementing account/tenant policy.
Signature-based collaboration must be evaluated using its declared trust model and
actual signing relationship, not merely an app name or a permission string.
A granted dangerous permission records a platform authorization; it does not grant
every business action associated with the underlying data.

## Platform and release applicability

Keep OS/API level and target SDK separate. Manifest attributes, exported defaults,
permission behavior, storage access, background execution, pending operations,
backup behavior, and WebView policies have version-dependent details. Do not place
an evergreen table of guessed defaults into a finding.

Read explicit packaged declarations and the applicable official API contract.
Where the installed runtime differs from the declared configuration, preserve both
observations and identify which actually governs the operation. Source comments
and scanner rules are weaker than the relevant selected implementation.

Permission review is not a count of requested permissions. A feature can legitimately
request a sensitive permission, while an ordinary permission may protect a critical
workflow poorly. Assess the actual data and decision at the crossing.

## Identity is not a UI state

Separate OS app identity, an in-app selected account, a service's session identity,
and the object owner. Account switching may update one before another. The meaningful
question is which identity is bound to the eventual operation and whether that
binding matches the product's promise. Do not infer a defect merely from asynchronous
execution or a cached value; lifetime and ownership contracts matter.

Lifecycle transitions are architectural facts: activity recreation, process death,
background work, persisted jobs, notification actions, and restored state can each
outlive a screen. The UI being locked, hidden, or logged out does not establish the
status of a server session. Likewise, a valid server token does not establish that
local sensitive content should remain displayed after logout.

## Deriving review questions

Use evidence from this app, not a mandatory bug-class sweep. A document-sharing
product motivates a recipient and scope question. An offline worker motivates a
logical-operation and account-snapshot question. A login callback motivates an
operation-binding question. A native parser used only for trusted assets calls for
a different assessment than a parser fed external documents.

For each question identify the product guarantee, selected component, governing
policy, evidence available, and missing relationship. Choose material uncertainties
rather than maximizing the number of manifest warnings. A finding is not required
for a successful assessment.

An exported component, a deep link, a permission request, and a native library are
review context. None is intrinsically a defect. Read the applicable mechanism chapter
only after the architecture gives it a purpose.
