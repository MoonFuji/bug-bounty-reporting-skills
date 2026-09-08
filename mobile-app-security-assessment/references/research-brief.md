# Research brief: mobile security assessment as a skill

## Status and question

Prepared 2026-09-08. This is an original technical synthesis and curriculum design,
**not a completed live literature review**. Web research was disabled. The requested
earlier Android/iOS research was not located in the available files or personal context.
No Exa or Context7 result was retrieved, and no external reference is marked freshly
verified. See the [source register](sources.md) for background pointers and outstanding checks.

The design question is: what mobile-specific knowledge helps an agent assess a
designated app before it is handed a suspected vulnerability? The answer is not a
catalogue of payloads. It is understanding which artifact, principal, decision,
representation, and lifecycle make a security claim applicable.

## Android and iOS require different evidence paths

| Concern | Android emphasis | iOS emphasis |
|---|---|---|
| Distribution | Base/configuration/feature splits; AAB versus installed APKs | IPA versus .app, extensions, signed device versus simulator product |
| Identity | Package/signing context, platform caller, app account, remote session | Bundle/team/signing context, entitlements, groups, app account |
| Collaboration | Components, Binder services, providers, URI/pending-operation grants | Extensions, groups, shared Keychain, system-mediated handoff |
| Local secrets | Storage/backup scope, Keystore policy, local authentication | Data Protection, Keychain attributes/groups, local authentication |
| Navigation | Intent routing, app-link association, selected handler | URL schemes, universal links, scene/extension binding |
| Runtime interpretation | DEX, native libraries, WebView, framework artifacts | Mach-O, Swift/Objective-C, WebKit, framework and extension artifacts |
| Server authority | Neither client type can establish backend object policy alone | Same responsibility distinction, different local integration |

These contrasts are a review map, not an evergreen table of platform defaults. The
references consistently require the actual runtime and current official contract for
version-dependent behavior.

## Where the curriculum adds judgment

The app-first path emphasizes responsibilities rather than broad sink searches.
A document collaboration app warrants recipient/scope analysis; a background-sync app
warrants account and commit-lifetime analysis; a hybrid app warrants a content/native
boundary explanation. A sensitive library name does not itself justify priority.

The difficult distinctions recur across real software designs: exposure versus
permission, registration versus invocation, delegation versus ambient authority,
selected build versus source intent, acceptance versus commitment, encryption versus
key-use policy, and app navigation versus server authorization. Each chapter includes
conditions and alternatives instead of absolute scanner-style verdicts.

This material can help an agent explain why a particular source/configuration question
matters. It does not establish that a model discovers more valid findings, that a program
pays for a class, or that any technique is undercrowded. Those require separate evidence.

## Deliberate boundaries

The package supports human-directed source/design assessment and bounded local metadata
intake. It does not choose public targets, install or execute unknown apps, bypass TLS
pinning or device protections, use discovered credentials, or generate exploit chains.
Backend testing is not inferred from access to an APK. Missing platform capabilities
remain explicit; the tool never substitutes a synthetic model for production proof.

The reporting skills remain unchanged. No coaching or metadata result becomes validated
reporting input automatically. The inventory has no severity output, and the exercises
have no automatic expertise score.

## What a future live research pass must verify

For platform claims, use versioned Android and Apple documentation first. Record the
selected OS/target SDK/build conditions and the exact statement the source supports.
For verification structure, inspect the applicable MASVS/MASTG revision; do not invent
requirement identifiers from memory or map every control failure to a bounty claim.

For tool use, inspect the installed tool's help and source release rather than copying
an obsolete command. For framework behavior, use the actual library/version and official
reference; a documentation search result is not proof that the app selected that API.

Public write-ups, when available, should be used to extract defensive mechanisms and
counterexamples, not copied exploit instructions. Record author, publication date,
affected revision, root cause, stated actor, missing conditions, and subsequent fix
status. Publicly disclosed examples do not establish private-duplicate visibility.

For Anthropic authoring guidance, verify the current official skill documentation.
The package already uses minimal name/description metadata, an actionable short core,
progressive references, deterministic optional tooling, and explicit triggering/evaluation
examples. That design is documented; current official conformity is not claimed.
