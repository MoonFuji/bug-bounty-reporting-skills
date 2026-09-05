# Multi-artifact reasoning and compositional assurance

Use this guide to assess a supplied implementation, configuration, contract, and
recorded outcome together. It does not direct discovery or traffic against a
system. The examples are fictional; locators describe teaching artifacts.

## A conclusion is an argument, not an accumulation of citations

An artifact has an identity, a provenance, and a limited proposition it can
support. More citations do not repair a missing relationship between artifacts.
For the proposition "the supplied release enforced policy P for operation O," a
small argument might require all of the following:

- The contract identifies P as applicable to O.
- The deployment record binds the release to the implementation being inspected.
- The effective configuration selects the relevant implementation path.
- The recorded decision describes O, not another attempt or an earlier revision.
- The outcome being discussed is the authoritative outcome under that contract.

This is a dependency argument, not a universal checklist. A proposition about a
source-level rule need not claim anything about a deployment or runtime event.
Only request the premises the actual conclusion needs.

### Worked example: the unconnected helper

`route.md` says the export handler calls `load_visible`. `storage.md` specifies
that `load_visible` enforces the tenant relation. `wiring.md` says the deployed
export handler receives the legacy adapter, whose implementation was not supplied.

The first two documents establish a useful intended contract. They do not show
that the legacy adapter satisfies it. Do not conclude either that the handler is
unsafe or that the helper protects it. The runtime binding is the missing link.

Now replace the wiring document with an immutable build manifest and a complete
binding record selecting the supplied implementation. The same source argument
can become applicable. Nothing about the model's rhetorical confidence changed;
the premise connecting source to the reviewed release changed.

## Different evidence answers different questions

| Evidence | Usually establishes | Does not establish on its own |
|---|---|---|
| Written policy | Intended permission or behavior | Enforcement by every implementation |
| Complete source model | Behavior under its stated inputs and semantics | That an unseen release runs that model |
| Deployment binding | Which artifact/configuration was selected | Correctness of that artifact |
| Instrumented trace | Recorded observations for correlated operations | Unobserved paths or future behavior |
| Test assertion | The property the test author chose to check | That the property matches the security contract |
| Reviewer summary | The reviewer's interpretation | Independent evidence beyond its underlying sources |

"Source is stronger" and "runtime is stronger" are incomplete claims. Evidence
strength is relative to a proposition. A finite runtime example can refute a
universal claim; it cannot normally prove that universal claim. A complete finite
model can support a universal statement *inside that model*, not outside it.

## Read composed behavior, not only a local function

In supplied code, a decision may depend on callers, decorators, injected services,
transaction boundaries, exception behavior, or runtime configuration. Resolve
those relationships when they are necessary to the stated claim. Do not infer
missing behavior from a function name such as `safe_load` or `authorize`.

A useful public explanation is short:

> The handler delegates the object decision to the injected policy service. The
> release binding selects implementation R. R uses the request principal and the
> canonical object identity. Therefore this source argument applies to the
> supplied release. The packet contains no evidence about any other release.

This explains the dependency, rather than listing every file read or exposing
private reasoning. A long call graph without the decisive applicability link is
not a stronger assessment.

## Composition rules are part of the specification

Suppose one policy permits and another denies. The result depends on the stated
combining rule: deny precedence, permit precedence, intersection, or a specific
ordered rule. Never import a rule from a familiar platform into a fictional or
unseen implementation.

Similarly, two locally correct components need not establish an end-to-end
property if they disagree on principal, object, time, or representation. The
composition claim needs a shared interpretation, not just two passing unit tests.
An unknown input to a required decision is not automatically a denial or permit;
the handling of unknown values is itself part of the contract.

## Necessary, sufficient, and irrelevant facts

A necessary condition must hold for the conclusion to hold. A sufficient
condition establishes the conclusion under the specified premises. One fact can
be necessary without being sufficient. A cryptographic integrity check can
establish integrity under its key assumptions while leaving authorization
unanswered. A version match can establish relevance without proving the defect.

An impressive but irrelevant artifact should receive no additional evidential
weight. Another team's large test suite is not evidence for the specific path
unless its assertions, environment, and coverage connect to that path.

## Corroboration needs provenance

Three reviews quoting one log are not three independent observations. Two
independent captures can share a faulty clock, parser, or event source. Describe
independence at the level actually established: acquisition, interpretation, or
underlying event. Do not multiply confidence as though repeated summaries were
fresh samples.

When sources conflict, first check whether they describe the same revision,
configuration, object generation, operation attempt, and observation interval.
Different true statements about different systems are not necessarily a conflict.
If equally applicable evidence remains inconsistent, preserve the conflict and
seek adjudication; do not vote among documents or let the newest prose win.

## Quantifiers determine the burden of proof

"This trace contains a violation" is existential. One applicable, reliable
counterexample can settle it. "Every allowed operation preserves P" is universal.
A few successful runs do not settle it. "No retained log contains X" describes
the retained logs; it is not equivalent to "X never occurred."

Write the quantifier explicitly before evaluating the evidence. Where an early
contradiction settles a proposition, do not force unrelated report work. Where
one essential premise is absent, do not replace that absence with a guessed
framework behavior.

## Transfer exercise

Explain which conclusion changes when only the build binding is replaced, and
which conclusions about the source contract remain valid. Then explain why
renaming a helper from `load` to `secure_load` changes none of them.

Related: [advanced worked lessons](advanced-worked-lessons.md),
[temporal authority](temporal-authority.md), and [source provenance](sources.md).
