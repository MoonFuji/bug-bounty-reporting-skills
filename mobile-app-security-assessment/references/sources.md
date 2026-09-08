# Sources and verification register

## Status

Authoring date: 2026-09-08. Live web access was disabled; **none of these external
URLs was opened in this task**. They are background pointers, not fresh citations,
current program rules, or proof of tool availability. Earlier mobile research was
not found. No public vulnerability write-up or private report was imported.

All cases, facts inside fictional projects, instructor guidance, and examples are
original synthetic teaching material. General technical background is provisional
until checked against the applicable platform/version. Scripts establish only the
bounded behavior tested in this package. No model-performance result is claimed.

Each linked chapter states its source family here. On verification add the exact
revision or retrieval date, a supporting section/quote, applicability conditions,
and the specific curriculum statement checked. Never equate URL presence with verification.

## Mobile standards

- OWASP MASVS: https://mas.owasp.org/MASVS/
  Intended use: mobile verification requirements; pin revision before mapping IDs.
- OWASP MASTG: https://mas.owasp.org/MASTG/
  Intended use: platform concepts and assessment structure, not automatic bounty eligibility.
- OWASP MASWE: https://mas.owasp.org/MASWE/
  Intended use: weakness taxonomy; applicability still depends on the app and actor.

## Android

- Application fundamentals: https://developer.android.com/guide/components/fundamentals
- App bundles: https://developer.android.com/guide/app-bundle
- Manifest overview: https://developer.android.com/guide/topics/manifest/manifest-intro
- Permissions: https://developer.android.com/guide/topics/permissions/overview
- Content providers: https://developer.android.com/guide/topics/providers/content-providers
- File sharing: https://developer.android.com/training/secure-file-sharing
- PendingIntent API: https://developer.android.com/reference/android/app/PendingIntent
- App Links: https://developer.android.com/training/app-links
- WebView/native bridge guidance: https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges
- Network security configuration: https://developer.android.com/privacy-and-security/security-config
- Keystore: https://developer.android.com/privacy-and-security/keystore
- Backup: https://developer.android.com/identity/data/autobackup
- Biometrics: https://developer.android.com/identity/sign-in/biometric-auth
- Play Integrity: https://developer.android.com/google/play/integrity
- NDK: https://developer.android.com/ndk

Required verification selectors: device/API level, target/minimum SDK, build variant,
installed modules/ABI, library and WebView version, signing context, and relevant vendor
or compatibility behavior. Do not assume a single exported/storage/backup default.

## Apple

- Apple Platform Security: https://support.apple.com/guide/security/welcome/web
- Entitlements: https://developer.apple.com/documentation/bundleresources/entitlements
- App extensions: https://developer.apple.com/app-extensions/
- Keychain Services: https://developer.apple.com/documentation/security/keychain-services
- LocalAuthentication: https://developer.apple.com/documentation/localauthentication
- Associated domains: https://developer.apple.com/documentation/xcode/supporting-associated-domains
- WebKit: https://developer.apple.com/documentation/webkit
- App Transport Security: https://developer.apple.com/documentation/bundleresources/information-property-list/nsapptransportsecurity
- DeviceCheck/App Attest: https://developer.apple.com/documentation/devicecheck
- App privacy: https://developer.apple.com/app-store/app-privacy-details/

Required selectors: device versus simulator, OS and SDK, effective signed entitlements,
provisioning/build context, extension identity, key/data-protection attributes, and
selected framework. Source plist content is not signed capability evidence.

## Protocols

- RFC 8252, OAuth 2.0 for Native Apps: https://www.rfc-editor.org/rfc/rfc8252
- RFC 7636, Proof Key for Code Exchange: https://www.rfc-editor.org/rfc/rfc7636
- RFC 9700, OAuth 2.0 Security Best Current Practice: https://www.rfc-editor.org/rfc/rfc9700

These protocol documents have different scopes; verify applicable sections before
claiming an exact requirement. A public native client, callback binding, and backend
object authorization are not the same security problem.

## Tools

- Android APK Analyzer: https://developer.android.com/tools/apkanalyzer
- Android apksigner: https://developer.android.com/tools/apksigner
- JADX: https://github.com/skylot/jadx
- Apktool: https://apktool.org/
- MobSF: https://github.com/MobSF/Mobile-Security-Framework-MobSF
- Xcode: https://developer.apple.com/xcode/
- React Native: https://reactnative.dev/docs/security
- Flutter: https://docs.flutter.dev/security

No tool release, command syntax, public hosted scanner, or plugin's current capability
was verified. Use local approved versions; no installation or network invocation is
performed by this skill.

## Skill authoring

- Anthropic Agent Skills best-practices background:
  https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices
- Anthropic skill examples: https://github.com/anthropics/skills

These links may redirect or have moved; they are not live checked. The local
[design note](../evals/skill-design.md) records actual structural choices and testable
requirements instead of asserting current official approval.

## Repository baseline

The integration was based on MoonFuji/bug-bounty-reporting-skills at
`8962b8dfcc3e790c418dc939712cfbb853f28d2d`, read through its connected GitHub source.
This establishes the repository state and existing contracts, not mobile platform facts.
The previous reporting and coaching skills are not modified by the new skill.
