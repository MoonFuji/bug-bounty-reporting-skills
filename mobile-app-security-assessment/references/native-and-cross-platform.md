# Native, cross-platform, and SDK boundaries

## Contents
- Know which representation you are reading
- Interface contracts and memory lifetime
- Framework and update composition
- Dependency applicability

Background: [Android native and build references](sources.md#android),
[Apple developer references](sources.md#apple), [framework and tooling pointers](sources.md#tools).

## Know which representation you are reading

An Android app can combine DEX bytecode, native ELF libraries, resources, generated
bindings, and framework-specific code. An iOS app can combine Mach-O code, Swift and
Objective-C metadata, embedded frameworks, extensions, and interpreted resources.
A decompiler's failure to render a feature is not evidence that it does not exist.

Obfuscation and symbol stripping make navigation less convenient; they do not prove
security or insecurity. Preserve immutable artifact identity, ABI/architecture,
library/module location, symbol or address locator, and analysis-tool version.
A readable pseudocode function may omit relevant calling conventions, exceptions,
compiler transformations, or ownership behavior. Do not silently treat it as source.

## Interface contracts and memory lifetime

Across JNI, FFI, Objective-C/Swift bridging, and native plugins, review the stated
units and ownership: byte count versus character count, encoding, buffer lifetime,
nullability, copying versus borrowing, and error propagation. Relate those contracts
to the selected caller and callee. A cast or manual allocation is not itself a defect.

A native crash record can support a bounded reliability observation. It does not
establish memory corruption, exploitability, arbitrary execution, or persistence.
Even a sanitizer diagnostic needs artifact binding and appropriate interpretation.
Use supplied diagnostics or owner-controlled defensive tests; this package does not
supply memory-corruption payloads or exploitation procedures.

A safe reference model establishes its own contract, not that a compiled platform
adapter uses the same units or lifetime. Missing native source is a named assessment
limit, not permission to invent a model that reproduces the desired conclusion.

## Framework and update composition

For Flutter, distinguish the Dart/runtime representation and native plugins from
Android/iOS wrapper code. For React Native, distinguish JavaScript or Hermes artifacts,
native modules, bridge configuration, and backend behavior. For embedded web wrappers,
content provenance and native bridge permissions matter. Missing conventional Java
or Objective-C business logic does not make the application empty or clean.

An over-the-air resource update can change a subset of code or content without changing
the store binary version. Record the actual update channel/version when relevant.
Do not assume that a signed native wrapper authenticates every later script or content
package. Conversely, the existence of dynamic content does not itself establish an
untrusted update path. The selected verification and distribution contract matters.

Common libraries may use different platform adapters. A secure Android implementation
does not establish iOS equivalence. A logic discrepancy in a shared layer can have
multiple affected clients but a single root cause and responsible owner.

## Dependency applicability

A dependency name or advisory match is only an applicability lead. Determine the
actual included version, patch status or vendored modifications, selected feature,
input provenance, and relevant configuration from supplied evidence. An unused or
unreachable bundled library is not automatically an application vulnerability.

Do not infer a current shipped revision from a package manager manifest alone. Build
outputs, lockfiles, vendored code, and release records can differ. If the available
records cannot identify the shipped code, preserve that uncertainty.

When a remediation changes several layers, green tests do not isolate which change
was necessary. Judge expected behavior against an independent product contract and
report only the causal relationship the evidence supports. Do not claim new exploit
variants from analogous source shape alone.
