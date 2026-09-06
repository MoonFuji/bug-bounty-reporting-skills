# Evidence and uncertainty

This is a reasoning reference, not a discovery checklist. Apply it to supplied
material. The examples and rules of inference here are original teaching content;
[the source register](sources.md) provides background reading, not current policy.

## A claim has dependencies

Suppose a report's conclusion requires A, B, and C. Evidence for A and C does not
establish the conclusion while B is unknown. A detailed discussion of C cannot
compensate for missing B. Write the dependency in ordinary language:

> The record was confidential; this caller lacked permission; the returned data
> was that record; the result came from the supplied revision.

A missing dependency is not necessarily false. It is a reason to keep the current
claim inconclusive. Conversely, a conclusive contradiction of one necessary
premise can defeat that claim without completing unrelated reporting work.

Do not confuse necessary with sufficient evidence. Authentication is necessary
for some permitted actions but does not by itself authorize every object action.
A failing test may be necessary to support a specific regression allegation, but
a failure without the asserted security consequence is not sufficient.

## Evidence strength depends on the question

A runtime observation can establish a particular effect but not every possible
execution. A source-level argument can establish a property of all paths within
an explicitly complete model, but not an unseen deployment. Policy text can
establish intended behavior, not necessarily actual implementation behavior.

There is no universal ladder where runtime always beats source or newer prose
always beats an older artifact. Ask what proposition each artifact supports.
Record revision, environment, and scope when they materially change that answer.

A tool's successful exit establishes that the tool completed under its own
success definition. It does not establish that the security proposition is true.

## Distinguish three kinds of absence

1. **Not supplied:** the excerpt omits the relevant component.
2. **Searched but not found:** a specified search did not find a relevant item.
3. **Excluded by evidence:** the complete applicable model or a decisive artifact
   rules the item out for the proposition being assessed.

Only the third is a basis for a strong absence claim. The second needs search
coverage and limitations. The first is an unknown, not a negative finding.

An inaccessible issue tracker is not an empty issue tracker. A nonexistent log
entry is not proof of a nonexistent action when logging coverage is unknown.

## Refutation must be falsifiable too

A useful objection has an applicability argument: which component, revision,
principal, and operation make it relevant? "The framework handles this" and
"there is probably a gateway" are unsupported until connected to the supplied
execution path. An objection is not stronger because it is phrased confidently.

Do not make an earlier classification irreversible. New target-owned evidence
may show that a supposed defense does not apply. Retain the old conclusion and
why it changed; do not silently relabel an inconvenient premise.

When several explanations survive the evidence, state the most important
unresolved distinction. Do not invent numeric confidence from prose alone.

## Contradictions and revisions

When two artifacts disagree, compare their revision, provenance, measurement
scope, and definitions before choosing one. A current deployment manifest and a
historical source snapshot may both be accurate while describing different
systems. A test fixture may deliberately disable a condition that production
requires. Preserve both facts rather than averaging them into a narrative.

A corrected assessment should say what premise changed and which conclusions
must be reconsidered. Do not restart the entire assessment when an unrelated
fact changes. Do not preserve dependent conclusions after their premise fails.

## Appropriate stopping

A review can end because the proposition is supported, contradicted, or cannot
be settled from accessible material. These are distinct from an environment
failure, a permission boundary, or a task-budget limit. Record those limits.

For an early rejection, preserve the decisive evidence and its scope. Do not
require a completed report, severity score, proof command, or duplicate search
for a proposition already contradicted on a narrower ground.

For an incomplete assessment, name the missing dependency rather than claiming
that the system is secure. For a completed assessment, state its quantified
scope: this record, this path, this revision, or the explicitly supplied model.
A finite collection of closed notes does not prove complete system coverage.

## Feedback question

Could another reviewer reconstruct the conclusion from the cited artifacts
without trusting your confidence? If not, improve the dependency argument or
acknowledge the unknown. More adjectives are not more evidence.
