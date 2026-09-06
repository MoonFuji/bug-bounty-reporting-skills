# Authority and security boundaries

Use this to understand supplied access-control evidence. It is not a recipe for
probing another user's resources. Background: [authorization guidance](sources.md#authorization).

## Identity is not entitlement

Authentication answers which principal a request is attributed to. Authorization
answers whether that principal may perform this action on this object under the
relevant conditions. An authenticated request can still exceed its permissions.

For an access claim identify the tuple:

> principal, action, object, tenant or namespace, relevant context.

"It works while signed in and stops after logout" says nothing decisive about
object authorization. "The returned identifier matches the input" does not
establish that protected object content was returned. "The account is an admin"
does not identify whether it is a tenant admin or a platform admin.

Do not call all cross-tenant behavior incorrect. Explicit sharing or delegation
may authorize it. The supplied contract and grant state determine the claim.

## Find the authoritative decision

A local handler may delegate a check. Conversely, a check existing somewhere in
the repository does not prove it applies here. Establish from supplied material
whether the relevant path invokes the decision, which inputs it authorizes, and
whether the effect uses the same object and principal.

A useful defensive sketch is:

```text
resolved principal + resolved object + requested action
                    |
            authoritative policy
                    |
             permitted effect
```

The sketch is not proof of any implementation. The burden is connecting these
nodes in the particular evidence packet. Treat omitted middleware, generated
routes, and framework callbacks as unknowns until inspected, not as automatic
vulnerabilities or automatic protections.

A UI visibility rule may improve usability without enforcing a security
boundary. A database constraint may enforce integrity even if the application
omits a preliminary check. Name the property's actual enforcement mechanism.

## Authority across time and delegation

A decision made for one principal, object, action, or time does not automatically
apply to another. A background operation may carry a stored decision or require
re-evaluation; the intended contract determines which is correct. A token's
integrity does not by itself establish that the issuer had authority to grant
the action or that the grant is still applicable.

Separate "the message is authentic" from "the operation is authorized." Separate
"the request was accepted" from "the protected effect happened." These are
different propositions and may need different artifacts.

For delegated systems, identify who is allowed to delegate what, whether the
recipient may further delegate, and which component enforces that contract.
Do not infer platform-wide authority from a scoped service identity.

## Process and deployment boundaries

A process action occurs under a runtime principal and its effective permissions.
An effect permitted to that principal is not automatically a privilege increase.
A local fixture proving a behavior does not establish that a managed service
exposes the same input or has the same privileges.

Record the exact claim boundary: library contract, executable, local service,
managed deployment, tenant, host, or sandbox. Do not borrow a more dramatic
boundary from a deployment that was not part of the evidence.

Operator-controlled configuration requires careful interpretation. A supported
configuration can be a legitimate assessment condition. A deliberately weakened
fixture may test a mechanism but cannot establish that the normal deployment
exposes it. The important question is what the precondition already permits,
not whether the word "configuration" appears.

## Positive and negative teaching contrasts

**Contrast A:** confidential record, no applicable grant, authenticated caller.
Authentication alone cannot establish permission.

**Contrast B:** same confidential record, explicit applicable share grant.
Tenant separation alone cannot establish that access is forbidden.

**Contrast C:** handler delegates authorization; complete supplied binding shows
that it applies before the effect. The handler's lack of an inline check is not
by itself a defect.

**Contrast D:** handler delegates authorization but the binding is absent from
the material. The conclusion is incomplete, not automatically positive or safe.

## Reviewer self-check

Can you identify the exact authority relied on, the operation it covers, and the
artifact that establishes its applicability? Could the same local code be correct
under a different contract? State that distinction before deciding the claim.
