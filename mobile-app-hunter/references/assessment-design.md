# From app responsibilities to a defensible assessment

Use this guide before a suspected defect has been supplied. It implements the
research's architecture-first recommendation for human-directed assessment, not
automatic target selection or exploit construction. Platform facts and case
provenance are in [research lessons](research-integration.md).

Contents: [selection](#select-questions-from-responsibilities),
[evidence](#design-discriminating-defensive-evidence),
[depth](#deepen-understanding-not-the-claim), [continuation](#continue-without-manufacturing-closure).

## Select questions from responsibilities

Begin with the product's protected objects and actions. Connect them to the
component that decides, the state it trusts and the supplied release that selects
it. Do not begin by assigning a CWE to an API name.

A useful public argument is: the product promises P; component relationship R is
material to P; the supplied evidence establishes A but leaves B unresolved; B
matters because it can change whether P is satisfied. This explanation fits in a
few sentences. It is not a request for private chain-of-thought or a new ledger.

**Document app:** selected sharing and background preview operations may have
different recipients and lifetimes. A permission granted to one operation does
not automatically describe the other. Ask how the stated sharing promise applies
to their actual identities and data projections.

**Offline sync app:** the current UI account, queued operation account and backend
principal can be different concepts. Establish the product's cancellation and
commit rules before interpreting completion after an account change.

**Companion app:** signing an update, accepting a device model/version and allowing
an account to control the device are separate responsibilities. A certificate or
integrity result establishes only the statement it actually covers.

**Hybrid app:** shared code and selected native adapters can implement different
mechanism contracts. Evidence from one adapter should not silently clear both.

These are architecture-reading examples, not a list of vulnerabilities that must
exist. Select only relationships present in the designated material.

## Prioritize uncertainty without pretend precision

Prefer an unresolved responsibility that can materially change a protection
argument over a generic hardening observation. Explain consequence, applicable
principal, release relevance and available evidence in prose. Avoid multiplying
invented probability scores or treating novelty as proof of correctness.

Evidence that a path is selected matters more than a convincing class name.
Evidence that a property is important matters more than a large permission list.
Evidence that an uncertainty has been resolved matters more than the volume of
reading. A small source/configuration question can be higher value than a broad
sweep whose observations cannot be interpreted.

Keep hypotheses provisional. Do not demand a complete report, severity, runtime
proof or public novelty verdict just to record an unanswered design question.
Missing platform capabilities remain an assessment limit rather than an invitation
to expand permissions or use a different environment without declaring the change.

## Design discriminating defensive evidence

For a permitted owner-controlled test or supplied observation, identify what the
result would establish and what it would leave open. Work from the independent
product or mechanism contract, not an expected value copied from the implementation.

| Evidence element | What it contributes | What it does not establish |
|---|---|---|
| Baseline behavior | The ordinary supported operation is exercised | Every other principal, object or lifecycle is correct |
| Meaningful negative control | The relevant decision distinguishes an excluded case | A denial at an unrelated earlier layer is sufficient |
| Observation calibration | The instrument captured a known benign event under the relevant conditions | An inactive or incomplete instrument proves absence |
| Exact release/configuration binding | The observed implementation is applicable | Source similarity proves a signed release is identical |
| Correlated operation/effect record | The result belongs to the operation under discussion | Acceptance, delivery and committed effects are synonyms |

A developer-owned regression can compare decisions against an explicit finite
permission table without using real user data. It should establish that the
specific decision was reached, not merely that some exception occurred. A finite
state-model check can validate the supplied ordering contract without pretending
to reproduce a device's concurrency or hardware behavior.

Use synthetic objects, minimal effects and separately authorized environments.
Do not generate live attack traffic, defeat app/device protections, or turn a
hypothetical stronger effect into a test objective. Stop interpretation at what
the designated evidence supports. Report a missing observation as inconclusive
when the observation mechanism was not shown to work.

## Deepen understanding, not the claim

After settling one question, examine whether its reasoning actually transfers.
The report recommends sibling, lifecycle, build and cross-platform comparisons;
use these as **scope checks**, not an automatic escalation or exploit-chain loop.

A sibling needs its own selected route and authority argument. An iOS counterpart
needs iOS evidence, not a renamed Android assumption. A debug trace needs a release
binding before it can support a release claim. A patch and green test need an
independent oracle before they establish that the intended behavior is repaired.

Retain the strongest applicable alternative explanation. If a proposed defense
is speculative, it does not kill the question. If an alleged defect contradicts
an explicit intended sharing contract, revise the claim rather than changing the
contract to preserve the finding. Correct conclusions can become inconclusive
when provenance is withdrawn; that does not prove the opposite conclusion.

Do not generalize an unencrypted storage property into public accessibility,
absence of a pin into transport compromise, or an attestation into account
permission. Research-backed distinctions are useful because they stop these
specific inference errors, not because they supply more impressive terminology.

## Continue without manufacturing closure

For broad assignments keep a plain note of settled questions, their decisive
locators, remaining dependencies and permitted next review work. A candidate
conclusion does not certify the application. An exhausted task budget or missing
build is not evidence that the app is safe or vulnerable.

Use the [MASVS coverage map](research-integration.md#standards-as-a-coverage-backstop)
after architecture work to notice applicable categories not yet considered.
Record why a category is inapplicable rather than filling a checkbox by default.
Keep technical evidence, destination eligibility and duplicate risk separate.
The existing reporting workflow remains the authority for report handoff.

Evaluate this method with the [transfer tasks](../evals/research-transfer.md), not
by counting hypotheses or the number of tools an agent invokes.
