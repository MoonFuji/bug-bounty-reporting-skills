# Worked contrasts: facts that change mobile conclusions

## Contents
1. Exported sharing interface
2. Base APK and missing feature
3. Local login screen and server authority
4. Provider grant scope
5. Pending operation delegation
6. Debug trust versus release trust
7. Link association versus authorization
8. Web frame versus native authority
9. Account switch and queued work
10. Key storage versus key-use policy
11. iOS groups and extensions
12. Plist versus entitlements
13. TLS and pins
14. Attestation and backend enforcement
15. Native diagnostics and consequence
16. Cross-platform equivalence

All examples are original, fictional teaching cases, not reproduced vulnerabilities.
No target, payload, or exploit recipe is supplied. Relevant technical background is
listed with verification limits in [sources](sources.md).

## 1. Exported sharing interface

A packaged component is exported. Product documentation permits sharing one selected
public document. Supplied records show the intended recipient received only that
projection under the sharing contract. Exported is not an authorization failure.
If a supplied record instead establishes delivery of a forbidden private field,
that finite discrepancy matters. If code-level policy and outcome are missing,
exposure is established but access-control correctness is inconclusive.

**Transfer:** moving the policy into a shared service changes its locator, not the
requirement to connect it to the operation.

## 2. Base APK and missing feature

The inventory finds no implementation of a dynamic module in a base APK. A release
record lists that feature as a separate installed split. The absence in the base does
not settle the installed app's behavior. Obtain the relevant owner-provided module
rather than recreating a supposed implementation or declaring the feature safe.

**Transfer:** a missing iOS extension in a partial bundle creates the same evidence
completeness issue, not the same platform implementation.

## 3. Local login screen and server authority

A screen hides an operation from a low-privilege account. That does not establish the
server's authorization. In one finite owner record the server independently denies
an unauthorized object action; in another the server outcome was never retained.
The first supports that bounded denial; the second remains unknown. Neither follows
from the button's visibility alone.

**Transfer:** successful authentication is not permission to a particular object.

## 4. Provider grant scope

The app intentionally grants a collaborator read access to one document. A matching
read is intended delegation. An observation of that read is not whole-directory
access. A broad path configuration motivates a scope question, but a path declaration
alone is not evidence of every resource being granted to every recipient.

**Transfer:** app-group access on iOS has different mechanics but also needs a
recipient/object contract rather than an assumption that sharing is inherently wrong.

## 5. Pending operation delegation

A collaboration feature permits specified fields to be supplied later. Mutability
can be necessary for that contract. Inspect the operation authority and bounds, not
just a flag. Conversely, an immutable pending operation can still represent the wrong
initial business action. A flag is not the entire permission argument.

**Transfer:** an approved workflow handle is not unlimited authority for arbitrary work.

## 6. Debug trust versus release trust

A connection in a debug build trusts an owner test certificate. The released build's
configuration is different and no released-path observation exists. The debug record
does not prove release transport failure. Preserve the useful debug evidence with its
scope instead of discarding it or promoting it beyond its conditions.

**Transfer:** changing a signer or provisioning context can invalidate other platform
comparisons even when source code looks identical.

## 7. Link association versus authorization

A universal/app link is associated with the intended application. This supports a
routing relationship. The action still depends on operation and account authorization.
In a fictional app, opening a public help page is intended. Naming a private object
requires a different permission decision. Association does not settle that decision.

**Transfer:** successful callback delivery does not establish identity binding.

## 8. Web frame versus native authority

A supplied navigation policy restricts the main page. A native-message handler applies
an additional explicit frame/origin contract, and finite records show it denies an
unapproved context. The handler's policy, not the top-level URL alone, supports that
outcome. If the handler configuration is absent, do not invent either its protection
or its failure. A bridge being present is not enough for either verdict.

**Transfer:** a shared SDK browser may use a different handler from the visible app WebView.

## 9. Account switch and queued work

The contract binds queued work to the account captured when it was created. A later
UI switch does not change that identity. A supplied journal with matching captured
identity complies for the recorded job. A journal assigning that same job to another
account contradicts the contract. A progress notification without a committed record
settles neither. Preserve job and object identity across the comparison.

**Transfer:** a cancellation acknowledgment need not mean a committed effect was undone.

## 10. Key storage versus key-use policy

Source stores a key through a platform key API. That does not establish hardware
protection or per-operation user presence. One owner diagnostic identifies the intended
key attributes and operation; another contains only a generic success message. The
latter is insufficient for the stronger protection claim, not proof of a defect.

**Transfer:** local biometric success and server transaction approval are different assurances.

## 11. iOS groups and extensions

A host and extension have effective signed access to the declared shared group and
use an approved minimal projection. Their collaboration is intended. A source file
mentioning the group in an unrelated app does not establish that app's effective access.
The reader set must come from actual signing/permission context and behavior.

**Transfer:** two similar group names do not imply a shared authorization domain.

## 12. Plist versus entitlements

A project plist declares a feature. The signed entitlement record for the distributed
extension is not supplied. The plist cannot settle its effective capability. If the
signed record later identifies the expected capability, that resolves the declaration
question, not every object-level use. New evidence should change only dependent claims.

**Transfer:** packaged Android declarations and runtime permission state also differ.

## 13. TLS and pins

No custom pinning code appears in the available source, while the selected client
uses its documented normal certificate and hostname verification. Absence of an
additional pin is not proof of cleartext or arbitrary trust. If the selected client
cannot be identified, say so instead of generalizing from another library's defaults.

**Transfer:** a native SDK may use a different network stack from the host app.

## 14. Attestation and backend enforcement

An app obtains an integrity signal. The backend contract requires a separate policy
decision using it. Client invocation alone cannot establish that server step. A
simulator failure may reflect a platform limitation. Do not turn either observation
into a bypass or an account-compromise claim.

**Transfer:** cryptographic validity and authority for a business action remain distinct.

## 15. Native diagnostics and consequence

A supplied diagnostic reports a native bounds error in a designated owner build.
That supports the specific diagnostic under its conditions. It does not establish
arbitrary code execution or the ability of an ordinary remote actor to trigger it.
A platform-specific adapter missing from the evidence limits the assessment further.

**Transfer:** a correct pure reference model does not prove compiled FFI equivalence.

## 16. Cross-platform equivalence

Android and iOS share a protocol schema but use different local storage and callback
implementations. A settled Android observation does not prove iOS parity. A shared
server permission decision can still be the same root cause across both clients.
Distinguish shared contract, shared implementation, and separately established behavior.

**Transfer:** version names alone do not bind an OTA resource to a native wrapper.
