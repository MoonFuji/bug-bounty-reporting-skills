# iOS platform: artifacts, identity, and composition

## Contents
- App bundle versus runtime
- Signing, entitlements, and provisioning
- Processes and collaboration
- Platform and device assumptions

Background pointers: [Apple platform security and developer documentation](sources.md#apple).
Do not substitute remembered OS defaults for the applicable signed build and runtime.

## App bundle versus runtime

An IPA is packaging, not a declaration that every contained executable is available
for unrestricted inspection or that every resource governs the active feature.
Distinguish the main app, embedded frameworks, extensions, resources, native code,
and cross-platform runtime. Source and symbols supplied by the owner may be more
informative than a partial binary, but must be bound to the assessed revision.

An Info.plist entry, class symbol, selector name, imported framework, and executed
implementation are different evidence. Objective-C/Swift metadata can aid navigation;
stripping, optimization, and bridging can complicate interpretation. A missing method
name in a tool's output does not prove the behavior is absent.

The ability to inspect a simulator build on a development host does not establish
device behavior. Do not infer effective Keychain, signing, attestation, hardware,
or data-protection properties solely from simulator success. Treat inability to
inspect a distribution executable as a limitation; use owner-supplied material,
not protection-bypass or decryption instructions.

## Signing, entitlements, and provisioning

Code signing connects an artifact to signing and policy context. Entitlements describe
specific capabilities granted to signed code. A source entitlement file is not proof
of the distribution artifact's effective entitlements. A provisioning record, signed
entitlement dump, and runtime behavior should refer to the same app identity and build.

A bundle identifier is not a complete authority identity. Team relationships, allowed
application identifiers, keychain access groups, and app groups may matter depending
on the feature. App Group collaboration is intentional sharing, not evidence that
unrelated apps can read the group. Determine which members are authorized and which
objects the product intends to share.

An entitlement can be necessary without sufficient proof of the actual sensitive
operation. App-level policy, user consent, object ownership, and server authorization
may still govern the operation. Conversely, a reassuring signing statement does not
settle the app's business authorization.

## Processes and collaboration

An extension has its own entrypoint, lifecycle, configuration, and capabilities.
A share extension's data path can differ from the host app's normal screen flow.
Widgets, notification service extensions, document providers, and other extensions
should be considered only when present and relevant to the product's promises.
Do not copy the main app's effective settings into every extension assumption.

Inter-app handoff, universal links, custom URL schemes, shared containers, pasteboard,
and system-mediated document access each establish different forms of collaboration.
Navigation to an app does not authenticate a business operation. Access to a shared
container is not permission for every remote object named in it.

Review the active delegate/scene or extension binding for the selected lifecycle.
A security check in one view controller is not evidence of every entrypoint, and a
missing local check is not proof that the shared service layer omits it. Identify
the authoritative layer and connect it to the operation in question.

## Platform and device assumptions

Preserve app build, device family, OS version, simulator/device distinction,
lock state, provisioning/signing context, and owner-applied modifications when they
matter. Do not treat jailbreak-only or debug-only access as an ordinary-app capability.
The existence of platform protections is not permission to assume a particular
application applied the relevant data-protection or authorization policy correctly.

For distribution/update concerns, distinguish packaging identity, code-signing
acceptance, update approval, and server trust. An app can have a valid signature while
its business workflow still needs an independent authorization decision.

The objective is an evidence-backed responsibility map. Keep the conclusion at the
layer you actually observed; do not turn a client-side observation into an OS compromise
or server-side flaw without evidence of that separate boundary.
