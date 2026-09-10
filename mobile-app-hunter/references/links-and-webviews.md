# Mobile links, native authentication, and web content

## Contents
- Navigation is not authorization
- Authentication callback binding
- Web content and native authority
- Cross-platform and lifecycle limits

Background: [Android links and WebView references](sources.md#android),
[Apple links and WebKit references](sources.md#apple),
[native OAuth background](sources.md#protocols).

## Navigation is not authorization

Separate URI registration, OS association/verification, routing to the app, parsing
inside the app, object resolution, and authorization of the eventual action.
Android App Links and iOS Universal Links are not merely custom URL schemes with
another name. Domain association is a platform relationship, not a business permission
for every path or resource. Runtime association state and user/system settings can
matter; source declarations alone may be insufficient.

Custom schemes can be legitimate routing mechanisms. Their presence alone does not
establish interception or compromise. A link that opens an intended public screen is
not a protected action. A link that names a confidential record still requires the
ordinary object permission. Review the actual selected handler and downstream policy.

Do not equate an allowlisted host string with a complete URL security contract.
Different parsers, redirects, browser state, and native routing may interpret or use
a value differently. Establish which representation each decision uses without
inventing a crafted bypass or transferring a result between unrelated parsers.

## Authentication callback binding

A native app is generally a public-client context: shipping a reusable string in its
binary does not make that string a confidential client secret. Classify its intended
role before reporting exposure. PKCE, state, nonce, issuer/audience validation, redirect
binding, and authenticated server sessions solve different problems; do not treat one
as evidence that all the others were applied. Exact protocol requirements need the
selected protocol/version and implementation documentation.

The meaningful assessment relates an initiated operation to its returned result and
the account it changes. App switching, multiple pending logins, restored state, and
embedded-browser versus system-browser execution can affect which state belongs to
which operation. Do not infer a failure merely because more than one callback exists.
Ask for relevant source and owner-provided records rather than manipulating real accounts.

An authentication callback received by an app is not itself evidence that the identity
provider, app, and backend agree on the account. Likewise, a server's rejection of a
client attempt may establish a working boundary even when the UI path looked permissive.

## Web content and native authority

Identify the actual WebView/WKWebView or browser component, its content source,
navigation policy, storage context, frame/origin distinctions, and native message
handlers. A bridge is intentionally an authority crossing. Its existence is not a
vulnerability; its permitted content and action contracts determine the assessment.

A rule on top-level navigation does not necessarily describe the origin/frame policy
of every native message. A JavaScript string appearing in a resource does not establish
execution in the privileged context. Supply the selected binding and relevant observation,
not a generic conclusion about all webviews. Local bundled content and remote content
can have different trust and update assumptions.

Review file/resource access, message parameter validation, web storage, and session
sharing only where the app uses them. A setting in an unused helper is not active policy.
Cookie presence does not prove the intended navigation sent it; a successful HTTP request
does not establish browser execution or native effect. Keep those claims separate.

## Cross-platform and lifecycle limits

React Native, Flutter, Cordova-style wrappers, and embedded SDK browsers can route the
same apparent user action through different native and network layers. The web page,
framework bridge, native plugin, and server can each own a different check.
Do not assign all behavior to the visible UI framework.

Consider which lifecycle receives the result: a recreated Android activity, iOS scene,
extension, or background continuation may not be the component shown in the initial
screen trace. This motivates an evidence question, not an assumed defect. Record a
supported result, a contract discrepancy, or an unresolved binding at the correct layer.
