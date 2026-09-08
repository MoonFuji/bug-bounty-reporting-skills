# Android entrypoints, delegation, and sharing

## Contents
- Exposure versus authorization
- Activities and lifecycle
- Services and Binder authority
- Providers and URI grants
- Pending operations and broadcasts

Background: [Android component and permission documentation](sources.md#android).
This is source/design assessment guidance, not component-invocation or exploitation instructions.

## Exposure versus authorization

Use the packaged manifest, merged-source provenance, runtime registrations where
supplied, and active implementation together. Distinguish activities, aliases,
services, receivers, and providers. An exported declaration describes a potential
cross-app interface; it does not establish that every caller can perform every action.
A nonexported declaration does not explain every intentionally delegated access path.

Intent routing answers where a message goes, not whether the recipient should honor
its business action. An explicit destination is not an authorization policy. An
intent filter describes matching, not all preconditions the handler enforces.
Read component permissions, code-level checks, and subsequent authoritative decisions
without treating any single layer as sufficient by name alone.

## Activities and lifecycle

A screen may be entered through ordinary navigation, a documented link, a notification,
or state restoration. Determine which initializations and checks the selected path
requires. Distinguish displaying a harmless screen from performing a protected action.
Product scope, victim participation, and actual committed effect remain separate.

Task-affinity and launch-mode flags affect activity organization. A flag alone is not
proof of impersonation or credential compromise. Establish the relevant platform,
visible behavior, and security promise before attaching an impact label.
The same care applies to screenshot or obscured-touch protections: context and actor
assumptions determine whether a missing defense is material.

## Services and Binder authority

Read which service is bound, which operations it exposes, and which caller identity
its checks actually use. Caller identity can have a limited context; deferred work
must follow the intended authority contract rather than assuming an earlier context
remains available forever. Review explicit identity capture and authorization evidence.
Do not claim a failure merely because work runs on a different thread.

A privilege-bearing service can legitimately act on behalf of another component.
The question is whether the delegation covers the particular operation and object.
A target app's own privileged debugging instrumentation is not the same actor as an
ordinary external application. A system-looking identifier in a log is not proof of
the effective caller or permission decision.

## Providers and URI grants

Content providers can expose selected data through permissions and temporary grants.
A grant is a scoped capability, not an automatic whole-sandbox disclosure. Examine
recipient, object scope, allowed modes, duration, and the code selected to resolve
the resource. Relate a FileProvider path configuration to the actual grants and
resources; configuration breadth alone does not establish unauthorized access.

Read and write permissions, path-specific policies, ownership rules, projection,
and the backend storage operation answer different questions. A query can properly
return a deliberately shared projection while keeping other fields private.
Do not assume all returned content is sensitive or all public content is harmless.

A path string and an opened object are not identical evidence. The assessment must
connect identity resolution to the actual resource and actor, not merely notice a
string manipulation or an API name.

## Pending operations and broadcasts

A PendingIntent represents delegated operation authority. Its creator, recipient,
intended operation, and permitted mutability matter together. Mutability does not
by itself establish abuse; some collaboration contracts require filling fields.
Immutability likewise does not prove the original delegated action is appropriate.
Inspect the selected construction and use under the applicable API contract.

For broadcasts, distinguish manifest and runtime registration, protected/system
signals, explicit permission checks, and actual event provenance. A test injecting
an impossible internal event is not evidence that the released app receives it from
the stated actor. Correlate supplied event records with the supported source.

Keep a compact boundary note: who supplies the input, who delegates authority,
which check applies, what object/action it covers, and what the evidence establishes.
Missing information is a named dependency, not a reason to write a guessed exploit.
