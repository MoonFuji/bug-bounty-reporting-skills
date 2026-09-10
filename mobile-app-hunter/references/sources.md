# Sources and verification register

## What changed

The original 2026-09-08 draft had unverified reading pointers. On 2026-09-10,
implementation incorporated the completed research report *Designing
`mobile-app-hunter`: Deep Research for an Anthropic-Style Android and iOS
Vulnerability-Hunting Skill*, whose stated research date is 2026-09-09.
The report attributes discovery to Exa and framework/authoring lookup to Context7.
The source URLs below were recovered from the report's citation metadata.

This is **report-backed integration**, not a second independent web verification.
A citation establishes the report's source attribution, not that the current app
uses that behavior or that the upstream page has remained unchanged. Detailed
Apple API pages and advisory leads retain their limitations rather than inheriting
a blanket verified label. Private conversation exports and identifiers are not
part of this public package.

## Status meanings

- `report_cited`: a specific statement and cited URL were present in the completed
  report; the curriculum uses that bounded summary.
- `limited_content`: the report explicitly identifies content-access limits;
  detailed API semantics are still unresolved.
- `lead_only`: identified for follow-up, but not adopted as a detailed case study.

[Source index](source-index.json) records each statement, conditions, upstream
revision where retained, and the chapters using it. Moving documentation without
a captured revision has `upstream_revision: null`, not a fabricated version.

Run `python scripts/validate_research.py` from the skill directory to check this
record offline. A passing validator means valid metadata and local references;
it **does not** authenticate the source, fetch its content, or prove its claims.
Age warnings are maintenance reminders, not dates after which platform facts become
false. Use task-specific primary documentation before relying on an exact default.

## Research-cited sources

### masvs

[MASVS coverage groups](https://mas.owasp.org/MASVS/) — `report_cited`.

Storage, cryptography, authentication/authorization, network, platform, code, resilience and privacy provide a coverage model.

**Applicability:** Map relevant product properties to categories; a category is neither a bounty policy nor a completed verification test.

### mastg

[MASTG v2.0.0 release announcement](https://mas.owasp.org/news/2026/07/04/mastg-v200-release/) — `report_cited`.

The research identifies the v2.0.0 release announcement dated 2026-07-04 and the separation of tests, techniques, demos, tools, knowledge and best practices.

**Applicability:** Use this named research baseline, not an evergreen latest claim. Pin an actual requirement/test revision before asserting conformance.

### skill-creator

[Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — `report_cited`.

The research recommends concise triggering metadata, progressive resources, deterministic helpers and comparisons against a baseline.

**Applicability:** The cited main-branch URL is moving; no upstream commit was retained. These are design choices, not official certification.

### android-bundle

[Android App Bundle](https://developer.android.com/guide/app-bundle) — `report_cited`.

A publishing bundle can produce device-specific APK sets.

**Applicability:** Bind conclusions to the installed base/configuration/feature set, build variant and ABI; one supplied APK need not represent all deliveries.

### android-intents

[Android intent redirection](https://developer.android.com/privacy-and-security/risks/intent-redirection) — `report_cited`.

The report identifies Android 16 default hardening relevant to intent redirection.

**Applicability:** Establish device API, target SDK, selected path and applicable documented behavior. This source is neither a universal immunity claim nor a reason to disable protections.

### android-bridge

[WebView native bridges](https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges) — `report_cited`.

The report describes frame-origin limitations of addJavascriptInterface and distinct origin-validation concerns for message channels.

**Applicability:** Identify the actual API, frames, content and registration lifetime. Do not transfer one bridge API contract to another.

### android-keystore

[Android Keystore](https://developer.android.com/privacy-and-security/keystore) — `report_cited`.

Keystore can keep key material non-exportable and constrain key use.

**Applicability:** Key exportability, user authentication, hardware support and business authorization are different properties; record the selected key attributes and environment.

### android-links

[Android App Links verification](https://developer.android.com/training/app-links/verify-android-applinks) — `report_cited`.

The research identifies link association and app selection as platform-specific evidence.

**Applicability:** Installed handler, domain association and OS behavior remain task-time facts; association alone does not authorize a resource.

### android-integrity

[Play Integrity overview](https://developer.android.com/google/play/integrity/overview) — `report_cited`.

Integrity signals contribute to server-side decisions.

**Applicability:** Do not substitute an integrity result for account/resource/action authorization or assume a universal device verdict.

### apple-signing

[Apple app code signing](https://support.apple.com/guide/security/app-code-signing-process-sec7c917bf14/web) — `report_cited`.

Apple app executable trust is based on code signing.

**Applicability:** Distinguish signed device app, extension, simulator, provisioning and source intent. Signing does not prove application correctness.

### apple-keychain

[Apple Keychain data protection](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web) — `report_cited`.

Keychain access and sharing depend on application identity, access groups and item protection policy.

**Applicability:** Use effective signed capabilities and item attributes; intended sharing among related apps is not by itself exposure.

### apple-data

[Apple Data Protection classes](https://support.apple.com/guide/security/data-protection-classes-secb010e978a/web) — `report_cited`.

Different protection classes intentionally have different accessibility across device-lock states.

**Applicability:** Record the actual class, relevant device state and intended availability. File Data Protection, Keychain attributes and local authentication are not interchangeable.

### apple-integrity

[Apple security overview](https://developer.apple.com/security/) — `report_cited`.

The research describes App Attest as an input to server integrity/risk decisions.

**Applicability:** This broad source does not verify a concrete App Attest API, payload format, request-binding implementation or device support matrix.

### apple-entitlements

[Apple entitlements reference](https://developer.apple.com/documentation/bundleresources/entitlements) — `limited_content`.

The report retains this official API pointer but identifies JavaScript-rendered documentation limits.

**Applicability:** Detailed entitlement semantics still require accessible version-specific source documentation.

### apple-associated

[Associated domain configuration](https://developer.apple.com/documentation/xcode/configuring-an-associated-domain) — `limited_content`.

The report retains this official API pointer but identifies JavaScript-rendered documentation limits.

**Applicability:** Do not infer a detailed association-file grammar, cache behavior or OS-version contract from pointer presence.

### apple-script-handler

[WKScriptMessageHandler](https://developer.apple.com/documentation/webkit/wkscriptmessagehandler) — `limited_content`.

The report retains this official API pointer but identifies JavaScript-rendered documentation limits.

**Applicability:** Do not infer frame/origin or content-world API behavior from the Android bridge lesson.

### react-native

[React Native security](https://reactnative.dev/docs/security) — `report_cited`.

The report says React Native provides no built-in sensitive-data store and describes Async Storage as unencrypted storage.

**Applicability:** Inspect the installed storage dependency and native adapters. Unencrypted does not mean publicly readable or sufficient proof of disclosure.

### flutter

[Flutter platform channels](https://docs.flutter.dev/platform-integration/platform-channels) — `report_cited`.

Platform channels cross between Dart and platform-native implementations; typing is not an authorization guarantee.

**Applicability:** Pin plugin/framework versions and selected Android/iOS implementations; do not presume platform parity from a shared API name.

### engagesdk

[Microsoft EngageSDK disclosure](https://www.microsoft.com/en-us/security/blog/2026/04/09/intent-redirection-vulnerability-third-party-sdk-android/) — `report_cited`.

The report describes an SDK-added exported activity in the final merged manifest and associated delegated-authority consequences.

**Applicability:** Historical affected integration only. This teaching summary does not establish that a current app/version is affected or supply reproduction steps.

### tiktok

[Microsoft TikTok Android disclosure](https://www.microsoft.com/en-us/security/blog/2022/08/31/vulnerability-in-tiktok-android-app-could-lead-to-one-click-account-hijacking/) — `report_cited`.

The report describes security consequences from composition of link handling, WebView navigation and native JavaScript interfaces.

**Applicability:** Historical disclosure, not an assertion about current TikTok. Navigation and native capability must be evaluated together without generalizing every bridge to a defect.

### home-assistant

[Home Assistant advisory lead](https://github.com/home-assistant/core/security/advisories/GHSA-68f4-97mf-f68w) — `lead_only`.

The research lists this advisory as a possible follow-up.

**Applicability:** Repository, affected component, conditions and fixed versions must be read before using this as a worked case.

### signal

[GitHub Security Lab Signal advisory lead](https://securitylab.github.com/advisories/GHSL-2026-102_Android_SignalApp/) — `lead_only`.

The research lists this advisory as a possible follow-up.

**Applicability:** A title or advisory identifier does not establish affected/fixed versions, prerequisites or a transferable case account.

## Pointers not promoted by this research

Earlier background links for detailed component permissions, provider grants,
PendingIntent options, backup defaults, biometric flags, ATS exceptions, OAuth
requirements, tool command syntax and NDK behavior are not all verified by this
report. The original mechanism chapters remain bounded background synthesis.
Read the actual API/OS/library revision for such details. In particular:

- [Android PendingIntent](https://developer.android.com/reference/android/app/PendingIntent)
- [Android backup](https://developer.android.com/identity/data/autobackup)
- [Android network security configuration](https://developer.android.com/privacy-and-security/security-config)
- [Apple ATS](https://developer.apple.com/documentation/bundleresources/information-property-list/nsapptransportsecurity)
- [RFC 8252](https://www.rfc-editor.org/rfc/rfc8252), [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636), and [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700)
- [OWASP MASWE](https://mas.owasp.org/MASWE/) and [MASTG](https://mas.owasp.org/MASTG/)

These are retained pointers, not additional research-cited entries. The MASTG
release announcement is a named baseline; it is not a pinned checkout of every
MASTG test. MASVS category mapping in this package deliberately makes no claim of
exact requirement-ID coverage or conformance.

## Updating the register

Record what actually changed: the primary section inspected, applicability and
revision where available. Do not relabel a lead because a URL resolves. When a
source contradicts an earlier lesson, revise the dependent claim and its examples.
Do not silently update the historical report date or claim a fresh retrieval from
an offline validation run. All new teaching scenarios are original fictional
material, not reproductions of the cited incidents.
