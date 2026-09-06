# Architecture-first assessment

Use this when the input is a designated system, not a suspected vulnerability.
The output is a grounded understanding of security responsibilities and worthwhile
assessment questions. It is not a target acquisition, scanning, or exploitation plan.

## The difference from claim review

Claim review asks whether X follows from the evidence. Architecture assessment must
first decide which X matters. A catalogue of bug names cannot make that decision.
Begin with the product's promised behavior and the components that jointly deliver
it. Then identify the assumptions connecting those components.

A shared-document product, for example, may intentionally permit cross-workspace
sharing. "A different workspace read an object" is not its security property.
"The effective share or ownership relation authorizes this action and projection"
is closer to a usable property. The contract determines which relation is intended.

A release service protects a different object: authority to promote an identified
artifact for a particular audience. Reusing a tenant-isolation checklist would miss
that responsibility even if it produced many questions.

## Make a small system sketch

Read the supplied product behavior, active assembly or routing, and the components
needed to understand the important operation. A useful sketch records the actor,
protected object, operation, deciding component, authoritative state, and locator.
Keep it small enough to revise. An invented complete architecture is worse than an
explicitly partial sketch grounded in the available files.

Names such as `safe`, `verified`, `internal`, and `trusted` are claims, not findings.
Locate what the implementation guarantees and why it is selected. Similarly,
"the middleware probably handles it" is not evidence. A route binding and applicable
middleware implementation can establish something a framework name cannot.

Distinguish planes. Configuration selects behavior; a request asks for an action;
a worker may commit an effect; an audit stream observes selected events. Evidence
from one plane does not automatically establish what happened in another.

## Derive a property before calling something a concern

Translate each material promise into actor, operation, object, context, and time.
Where relevant, include the field projection or identity generation. Avoid universal
quantifiers unless the reviewed scope supports them. "These two entrypoints select
the same permission adapter at R" is a finite composition claim, not a proof about
all future integrations.

Questions can come from a cross-component assumption, a mismatch between contract
and retained observation, or an important responsibility whose selected enforcement
is not visible. Missing visibility justifies a question, not an accusation.

For a hypothetical queued document export, authorization at enqueue and permission
at delivery are different contracts. Determine which one the product promises.
Only then can a retained job history be assessed. An explicit snapshot contract
must not be silently replaced with an immediate-revocation contract or vice versa.

## Select useful questions without a score theatre

Prefer a question when it affects a material product guarantee, is anchored in the
actual architecture, and resolving it will remove a consequential uncertainty.
Distinguish importance from ease of reading. An easy peripheral check should not
crowd out the central responsibility, but an unavailable central artifact should
not prevent recording a useful answer elsewhere.

Group questions with the same unresolved premise. Ten different phrasings of
"which policy implementation is active?" are one dependency, not ten independent
hypotheses. A valid short question set is better than a mandatory quota.

Do not put hypothetical severity, creativity, or duplicate probability into an
arbitrary multiplication formula. Those quantities are often not calibrated and
can make speculation look measured. Explain priority in one sentence instead.

## A disciplined pass resolves dependencies

For a question about a composed guarantee, connect the requirement, implementation,
active selection, and applicable observation. A citation list is not the connection.
Explain what each artifact contributes and what still does not follow.

Suppose a selected service applies a permission relation and then serializes an
approved projection. A handler without a local check is not an independent omission
if the complete supplied composition requires that service. Conversely, an unused
correct service does not establish the active route's behavior. Review the binding,
not just the attractive function.

Use a concise argument that another reviewer could check. Do not require private
chain-of-thought. For a permitted local specification test, state the expected
property independently of the implementation, which path the fixture reaches,
and which result was actually observed. A mock replacing the deciding component
cannot establish that component's behavior.

## Choose a conclusion at the appropriate level

A complete finite record may establish a concrete contract inconsistency. It does
not establish arbitrary reachability, repeated exploitation, or a broader impact.
A supplied secure composition can answer a scoped concern without certifying the
entire repository. An absent runtime binding can make an otherwise strong source
argument inconclusive without proving either a defect or a defense.

Preserve those three outcomes. Do not compensate for unresolved evidence with
more forceful language. Do not turn honest limits into reasons to discard a
separately established, narrower fact.

## Continue intelligently

When evidence settles a question, record why and consider other in-scope questions
under the user's task limit. When it does not, name the missing artifact and retain
the dependency. A stopped tool run, missing device, or inaccessible configuration
is a limitation of the assessment, not a result about the product.

At a context boundary retain the system sketch and the relationships already
established. Resume by checking the relevant artifacts rather than treating a
previous summary as a new source of truth. Useful depth reduces uncertainty; more
files opened, more categories named, or longer notes do not measure it.

## Using the mechanism library

Read [the mechanism index](mechanisms/README.md) only as a router. Pick the chapter
that explains the unknown guarantee. Experienced agents can skip explanations they
can already apply correctly. A learner should be able to say why the mechanism
matters in this architecture, and give a situation where the same principle would
not justify the same conclusion.

Keep operational notes separate from [project grading](../evals/projects/README.md).
The assessment should not need an answer template or a rubric score to proceed.
