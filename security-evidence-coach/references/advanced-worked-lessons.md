# Advanced worked lessons: the fact that changes the answer

These eight additional lesson families use original fictional multi-artifact
packets. They teach applicability, quantified conclusions, and evidence revision,
not live vulnerability reproduction. No external report was copied or verified.

The [advanced practice set](../evals/advanced/README.md) contains unlabelled
counterparts. These worked explanations are training material and disclose their
logic. Reading them first makes later scores practice outcomes, not independent
validation of capability. Do not give the answer key to an assessed learner.

## 13. A correct helper that was never selected

**Proposition:** supplied implementation A governed the object decision for O.
The source tree contains A and B. The handler accepts a resolver from a factory.
A enforces a permission relation; B follows a legacy contract.

**Tempting mistake:** treating A's complete source listing as evidence that A was
used, or concluding a defect merely because the handler lacks a local check.

**Decisive relationship:** the active binding and correlated call record identify
the selected implementation. In packet A417 they identify A. In A862 they identify
B. In A295 the factory selection was not retained.

**Justified conclusions:** supported, contradicted, and inconclusive respectively.
None of those labels alone establishes whether the selected implementation is
secure. Selection and correctness are different propositions.

**Transfer:** move the guard into a decorator or shared storage adapter. What
artifact would make the source argument applicable? Renaming `load` to `safe_load`
is irrelevant without the implementation and its binding.

## 14. Two correct rules, one missing composition contract

**Proposition:** the combined policy decision is PERMIT. Rule P permits and rule Q
denies. Both apply; their individual results are settled.

**Tempting mistake:** imposing the reviewer's preferred deny-by-default behavior
instead of reading the stated rule-combining semantics.

**Decisive relationship:** packet A673 selects permit precedence, so the
proposition is supported. A128 selects deny precedence, so it is contradicted.
A954 omits the selected mode, so it is inconclusive.

**Why this matters:** determining actual behavior is not endorsing its design.
The contract may be inappropriate for a separate requirement, but that is another
claim requiring its own evidence. Likewise, two passing local policy tests do not
establish their composition without the combining rule.

**Transfer:** replace rule composition with scope intersection or an ordered rule
list. Does the same evidence determine the result? Which fact must change?

## 15. Revocation timing without invented clock agreement

**Proposition:** every post-barrier operation in a finite history used policy
version 12 or later. The contract permits pre-barrier operations to finish under
their original snapshot.

**Tempting mistake:** judging by response completion time, or comparing clock
labels from uncorrelated machines as though they supplied a global order.

**Decisive relationship:** in A386 a single authoritative sequence places O1
after the barrier and its decision uses version 12. In A741 the same ordering
establishes a post-barrier decision under version 11. In A509 the independent
clocks cannot settle whether O1 started before or after the barrier.

**Justified conclusions:** the first finite history complies; the second contains
a counterexample; the third is unresolved. Do not invent a grace period to save
the second case, or assume a globally instantaneous revocation rule absent from
the supplied contract.

**Transfer:** a lease-based contract permits a defined propagation interval. Which
part of the earlier conclusion changes? The observed timestamps remain facts;
the applicability of the compliance criterion changes.

## 16. Attempts, effects, and a misleading processed message

**Proposition:** logical adjustment `(W, J)` produced exactly one committed effect.
The specification distinguishes message delivery from committed balance changes.

**Tempting mistake:** equating two attempts with two effects, or equating one
acknowledgment with one effect. A timeout is not automatically a rollback.

**Decisive relationship:** A230 contains a complete journal with one committed
row and duplicate references to it. A815 contains two distinct, uncompensated
effects for the same operation identity. A462 retains only acceptance messages
and no authoritative effect record.

**Justified conclusions:** exactly one effect, not exactly one effect, and
inconclusive. The effect journal's declared completeness is load-bearing. The
records in these fictional packets establish it; real reviews must not assume it.

**Transfer:** change the identity domain so key J is scoped per workspace. Two
rows with different workspaces are not necessarily duplicates. A repeated display
key is not a complete operation-identity argument.

## 17. The pooled winner loses inside both strata

**Proposition:** B has a higher observed success rate within each job-size stratum.

**Facts in A591:** for small jobs A is 81/90 and B is 19/20; for large jobs A is
2/10 and B is 24/80. B is higher in both strata, while the pooled totals favor A,
83/100 versus 43/100. Workload composition accounts for the reversal.

**Tempting mistake:** using the pooled rate to answer the within-stratum question,
or treating the higher descriptive rate as a causal improvement.

**Contrast:** A347 reverses the groups. B then wins in the pool but loses within
each stratum. A908 supplies only pooled totals, so within-stratum comparison
remains unknown. Do not assert a reversal happened when the strata are missing.

**Transfer:** replace job size with task family in a model evaluation. Does a better
aggregate score establish improvement in every family? No; examine the appropriate
breakdown without pretending related cases are independent samples.

## 18. Agreement without independent acquisition

**Proposition:** the package contains two independently acquired records of X.
Here acquisition independence means neither record derives from the other or a
shared retained capture; it does not imply freedom from all common bias.

**Tempting mistake:** counting reviewers, citations, or different phrasings as
independent observations. Repeated summaries can all inherit one mistaken source.

**Decisive relationship:** A756 supplies a provenance audit connecting two captures
to separate direct acquisitions. A183 shows two reviews deriving solely from one
capture. A624 lacks origin metadata despite different wording.

**Justified conclusions:** supported under the narrow definition, contradicted,
and inconclusive. Dependent evidence does not make X false. Independent acquisition
does not make X true by itself. Preserve both distinctions.

**Transfer:** two tools use the same parser and clock. What kind of independence
has actually been established, and which systematic uncertainty remains?

## 19. Green tests that encode the wrong contract

**Proposition:** R satisfied a six-row permission table for READ and EXPORT. The
independent contract allows owner and explicitly shared reader, and denies the
unrelated reader for both operations.

**Tempting mistake:** accepting a successful CI exit as stronger evidence than an
explicit mismatch between the required behavior and the observed decision.

**Decisive relationship:** A439 records all six expected effective decisions at
R. In A970, EXPORT allows the unrelated reader and its test incorrectly expects
allow, explaining green CI. In A256 the EXPORT fixture is unavailable and its
rows were skipped.

**Justified conclusions:** supported for the finite table; contradicted by one
row; and inconclusive for the two-operation proposition. Skipped tests do not
prove a defect. A wrong expected value does not change the intended contract.

**Transfer:** an implementation and its test share the same normalization helper.
Why is their agreement not automatically independent verification of the intended
identity relation? Explain the missing oracle without creating an exploit variant.

## 20. One execution is not a relational property

**Proposition:** two supplied executions have equal approved public observations.
The contract defines the observation as `(body, receipt label)` and gives no
exception for either component. Public input is equal; protected state differs.

**Tempting mistake:** looking only at the body or generalizing one equal pair into
a universal confidentiality guarantee.

**Decisive relationship:** A803 captures both equal components; A564 has matching
bodies but different receipt labels; A319 omits the labels from the retained data.

**Justified conclusions:** equal for this pair, unequal for this pair, and
inconclusive. Do not invent an out-of-scope channel to undermine a settled finite
proposition; do not ignore an included component to manufacture equality.

**Transfer:** the contract explicitly permits a status difference under a named
public condition. Does raw inequality still contradict that revised property?
Read the revised relation rather than reusing the old verdict.

## How to use these lessons

Teach the decisive distinction, ask for a concise public argument on the unlabelled
counterpart, then give feedback. Next use a structurally changed example—not only
new identifiers. For a learner who already gets the distinction, skip the lesson.

Use [revision drills](../evals/revision-drills.md) to test whether new evidence
changes the right conclusions without changing unrelated ones. Use the human
rubric in [the evaluation protocol](../evals/README.md), not label accuracy alone.
