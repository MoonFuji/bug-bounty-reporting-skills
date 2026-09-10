# Mobile research lessons: applicability, composition and coverage

Use this chapter when the security question depends on a platform guarantee or
on the relationship between components. It integrates the completed 2026-09-09
research, not newly executed app tests. Bracketed source IDs link to the exact
source register entry and its applicability limits. Unknown defaults stay unknown.

Contents: [applicability](#platform-applicability), [release composition](#release-composition),
[web/native trust](#web-and-native-trust), [iOS authority](#ios-authority-and-data),
[frameworks](#framework-and-sdk-contracts), [lifecycle](#lifecycle-and-request-binding),
[standards](#standards-as-a-coverage-backstop), [cases](#documented-case-lessons).

## Platform applicability

Before transferring a statement from a reference to an app, identify the property,
the source's selectors, and the evidence connecting them to this release. A
platform version is not a substitute for all the other selectors.

| Statement inherited from the research | Evidence needed for this assessment | Unjustified shortcut |
|---|---|---|
| App bundles can produce device-specific APK sets | Base, configuration and feature composition; version; ABI; distribution/build provenance | One base APK represents every deployed feature |
| Android 16 adds default intent-redirection hardening | Actual OS/API, target SDK, selected component path and applicable platform rule | Every earlier issue remains reachable, or every app is immune |
| WebView bridge APIs have different origin contracts | Bridge API, registered capabilities, frames/content, navigation policy and lifetime | A bridge name alone proves a defect or safe origin binding |
| Keystore can restrict key export/use | Key attributes, provider/device support, authentication policy and operation | Non-exportable means every use is authorized |
| Apple capabilities depend on signing and configuration | Device app and extension identities, effective signed capabilities and actual item policy | Source entitlements prove installed authority |
| Data Protection classes have different accessibility | Selected class, device state, threat model and legitimate background requirements | Any accessibility while locked is automatically a leak |
| Framework wrappers call native facilities | Installed package/plugin versions and selected adapters on both platforms | Same API name means equal security semantics |

The sources for these rows are [bundles](sources.md#android-bundle),
[intent behavior](sources.md#android-intents), [bridges](sources.md#android-bridge),
[Keystore](sources.md#android-keystore), [signing](sources.md#apple-signing),
[Data Protection](sources.md#apple-data), [React Native](sources.md#react-native)
and [Flutter](sources.md#flutter). No opt-out or bypass procedure is part of this
chapter. If a platform protection prevents an observation, document that result
under the tested conditions rather than disabling it to support a release claim.

## Release composition

The application author's manifest or source tree is an input, not the complete
release identity. The report's SDK case motivates examining the relationship:

```text
application source + dependency inputs
    -> generated/merged configuration
    -> packaged release and signed capabilities
    -> installed modules and selected runtime implementation
```

The review question is whether the supplied composition supports the product's
stated responsibilities. Explain discrepancies in terms of who may invoke which
operation, what policy applies, and which component owns the decision. Merely
finding an additional component does not answer those questions.

For Android, compare supplied source and final configuration when both are
available; preserve missing splits/build outputs as limits. For iOS, distinguish
application and extension identities and capabilities rather than copying the
Android component model. A framework packaged in the app and a separately signed
extension can require different authority arguments.

**Fictional contrast:** a collaboration app's final build includes an SDK-created
sharing entry. The product explicitly permits narrow user-selected sharing, and
the supplied selected implementation enforces that contract. The additional entry
is real, but the broad claim that all cross-app access is forbidden is wrong.
If only the dependency manifest is supplied, even the final selection remains an
open fact. [Sources: bundle composition](sources.md#android-bundle),
[signing](sources.md#apple-signing), [historical SDK case](sources.md#engagesdk).

## Web and native trust

Assess the relationship between content provenance and the native responsibilities
exposed to that content. The Android bridge documentation summarized by the report
specifically distinguishes `addJavascriptInterface` frame-origin limitations from
message-channel validation. Do not infer equivalent semantics for every JavaScript
API or for WKWebView. [Android bridge source](sources.md#android-bridge).

Four independent facts matter to a design argument: what content is selected,
which navigation policy applies, what native operation exists, and which
application/account state authorizes that operation. A valid association between
a domain and an app addresses routing; it does not establish the application's
resource permission. [App Links source](sources.md#android-links).

**Fictional contrast:** a help view with no privileged native operations and a
signed-in workflow view do not have identical responsibilities merely because
both render HTML. Conversely, a view with a native interface may be correctly
limited to trusted content and a narrowly authorized operation. Missing release
navigation evidence makes that composition unresolved; it does not make it safe
or defective by default.

The Apple `WKScriptMessageHandler` and associated-domain references have limited
content status in this research. Use those as follow-up pointers, not as proof
of a specific message-origin or content-world rule. [Apple limitations](sources.md#apple-script-handler).

## iOS authority and data

Keep four propositions separate:

1. The code has the required signature/identity for this distribution context.
2. The app or extension has the effective capability to access a class of resource.
3. A particular stored item is accessible in the relevant device state.
4. The active account is entitled to the business operation and data requested.

Evidence for one does not automatically establish the next. Apple's signing,
Keychain and Data Protection sources support these distinct mechanism models;
the app's own contract supplies its account-level requirements.
[Signing](sources.md#apple-signing), [Keychain](sources.md#apple-keychain),
[Data Protection](sources.md#apple-data).

Keychain groups deliberately support sharing under configured identities. Group
membership alone is not a data-disclosure finding. It also does not establish
that every field or account record should be shared. Determine the intended data
projection and the actual item/access-group attributes. File Data Protection and
Keychain accessibility must not be conflated just because both involve lock state.

**Fictional contrast:** a background receipt-sync feature intentionally needs an
item after first unlock, while a different secret is required only during an
interactive operation. The requirements differ. Neither an availability-oriented
class nor a strict class should be judged without the promised behavior and actor.
A simulator result cannot establish a hardware-specific claim absent separate
applicable evidence.

The report retains Entitlements and Associated Domains API pointers with retrieval
limitations. Detailed flag/default claims remain unverified here. This chapter
adds no claim of iOS parity with Android component exposure.

## Framework and SDK contracts

The research summarizes React Native's security guide as providing no built-in
sensitive-data store and describing Async Storage as unencrypted. This is a
storage-property statement, not proof that arbitrary applications or accounts
can read another app's data. Identify the selected dependency, data sensitivity,
OS protections, account scoping and native configuration. [React Native](sources.md#react-native).

Flutter platform channels connect Dart and native implementations. A typed channel
interface helps describe values; the selected native implementation still defines
what action occurs and how it is authorized. Shared code cannot prove that Android
and iOS adapters enforce identical lifetimes, data protection or account binding.
[Flutter](sources.md#flutter).

**Fictional contrast:** both platform adapters expose `saveCredential`. One owner-
supplied implementation stores account-scoped items with documented deletion;
the other adapter is missing from the package. A claim of product-wide equivalent
protection is unresolved, even if the shared tests pass. It is equally wrong to
call the absent adapter defective merely because it has not been inspected.

A lockfile, source package or SBOM can identify a dependency; selected build and
runtime evidence connect that dependency to behavior. A current advisory about a
package does not prove that the designated artifact includes an affected path.

## Lifecycle and request binding

Account identity, installation identity, device integrity, local user presence
and transaction authority are not synonyms. The report treats Play Integrity and
App Attest as inputs to server decisions, not replacements for resource permission.
[Play Integrity](sources.md#android-integrity), [Apple overview](sources.md#apple-integrity).
The overview does not verify a particular App Attest API or payload format.

For an owner-supplied asynchronous record, separate creation, authorization,
acceptance, commitment and delivery. Determine which event the product's revocation
contract governs. Completion after logout can be compatible with an operation
committed earlier; it can also conflict with a separately evidenced cancellation
promise. Do not invent either rule to force a verdict.

A device companion adds another responsibility: permission for a mobile account to
control a particular enrolled device. Authentic update bytes, update eligibility,
account ownership and version/rollback policy are separate design propositions.
An integrity result or valid signature alone does not settle all of them. This is
a mechanism lesson, not a device protocol or update-bypass procedure.

## Standards as a coverage backstop

The report identifies the MASTG v2.0.0 announcement dated 2026-07-04 and its modular
structure. Keep that as the **research baseline**, not a permanent latest claim.
MASTG techniques and tests support verification; they do not select the product's
important questions or determine payout eligibility. [MASTG source](sources.md#mastg).

Use this order: product responsibility -> grounded assessment question -> relevant
standard/category -> applicable verification material -> evidence-backed outcome.
Afterward, use categories to notice omissions. Do not run every technique merely
because it exists. [MASVS source](sources.md#masvs).

| MASVS category | Coverage question | False inference to avoid |
|---|---|---|
| STORAGE | Which protected data persists, where, and for whose account/lifecycle? | Any retained data is a leak |
| CRYPTO | Which statement/key use is protected, under which attributes? | Strong algorithm proves correct binding |
| AUTH | Who authenticates, who authorizes, and for which operation? | A session proves object permission |
| NETWORK | Which client, peer identity and transport policy apply? | An exception or absent pin alone proves compromise |
| PLATFORM | How do app/OS/extension/delegation responsibilities compose? | Exposure or intended sharing is itself a defect |
| CODE | What representation, lifetime and processing contract applies? | A parser/library name proves an affected path |
| RESILIENCE | Which integrity or resistance property is actually required? | Integrity signals establish business authority |
| PRIVACY | Is collection, projection and retention consistent with the requirement? | Permission presence proves data use |

This is a category map. It deliberately invents no requirement IDs, compliance
levels or exact test mappings. Before citing an individual control, retain the
actual versioned text and its applicability to the operation under review.

## Documented case lessons

### SDK-created release surface

Microsoft's EngageSDK disclosure, dated 2026-04-09 in the report's cited URL,
is used for one historical lesson: SDK integration can add a component to the
merged manifest that is absent from the application's own authored manifest.
The report describes an exported activity and delegated-authority consequences.
[Primary source identified by the report](sources.md#engagesdk).

Transfer the responsibility question, not the incident's payload: what did the
selected release add, what legitimate capability was intended, and what policy
limited it? A secure counterpart would establish that intended policy for the
added path. Missing merged output is an evidence gap, not a vulnerability.
No affected/fixed version claim about today's dependencies is made here.

### Composition rather than a single suspicious API

Microsoft's historical TikTok Android disclosure dated 2022-08-31 connects link
handling, WebView navigation and native JavaScript interfaces. The report's lesson
is that a capability's security meaning depends on the path that selects it and
the identity under which it operates. [Primary source identified by the report](sources.md#tiktok).

Do not infer that every deep link or bridge is defective, or that current TikTok
is affected. The secure contrast is a composition whose navigation, content trust
and native permission are all established for the selected release. This package
does not reproduce the incident or include an operational chain.

### Leads are not researched cases

The report also names Home Assistant and Signal advisory URLs. It does not supply
enough retained detail for this integration to teach their conditions or fixes
reliably. They remain `lead_only` entries, not extra counted case studies. A title,
identifier or familiar class does not replace reading the actual advisory.
