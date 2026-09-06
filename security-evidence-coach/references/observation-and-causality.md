# Observation, controls, and causal judgment

Interpret existing evidence or isolated teaching measurements. This reference
does not prescribe attack traffic. Background: [measurement and logging](sources.md#measurement).

## The observation mechanism is part of the argument

An observation requires an event, an instrument capable of detecting it, and a
record correlated with the event. Missing any link weakens both positive and
negative conclusions.

For a negative result ask: was the instrument active, did it cover the relevant
path, and was the observation interval appropriate? A failed capture cannot
establish that no event occurred. A callback absent from an unverified listener
is inconclusive, not proof of safety.

For a positive result ask: could this be a stale artifact, another operation, or
a benign event with the same appearance? A log line is evidence of what the
logger recorded, not automatically of the downstream effect described in prose.

## Controls have different jobs

**Instrument control:** establishes that the observation mechanism can detect a
known benign event under the relevant conditions.

**Baseline:** characterizes ordinary behavior so unrelated variation is visible.

**Property control:** distinguishes the proposed explanation from an alternative
within the supplied experiment.

**Environment check:** establishes that revision, configuration, and dependency
assumptions match the material under assessment.

Calling an artifact "negative_control.txt" does not perform any of these jobs.
The reviewer must explain what it controls and what uncertainty it leaves.

## Correlation does not assign cause

Suppose two response bodies differ. The difference could encode a sensitive
state, a request identifier, localization, timing, or unrelated formatting.
The observed difference alone cannot establish which explanation is correct.
Likewise, identical status codes do not establish identical data or behavior.

A strong comparison changes the relevant condition while keeping competing
explanations controlled. In a teaching packet, read the conditions actually
recorded; do not assume that everything else was held constant.

An intervention that changes several conditions at once may repair behavior
without identifying the unique cause. Explain that limitation rather than
claiming that the result proved the precise root cause.

## Time and repeated measurements

Averages can hide variance, drift, caching, and different populations. A few
large differences are not a universal proof of a timing distinction. A fixed
sample count or a single threshold cannot settle every measurement problem.

When reviewing a supplied statistical claim, look for the design, matched
conditions, ordering, variability, effect size, and uncertainty. Repeated
selection of the most favorable comparison needs to be disclosed. Correlated
observations are not independent evidence merely because there are many rows.

Do not invent significance calculations, confidence intervals, or sample sizes.
The practice suite contains qualitative evidence judgments, not a timing tool.

## No output versus no effect

A return code may describe the final stage while an earlier effect already
committed. An acknowledgment may describe acceptance before any effect happens.
A browser navigation can create a new execution context; a transient variable
from an old context is not persistent evidence of a later event.

Reason about the authoritative event and its ordering, not just the last visible
message. Where the record omits ordering, keep that dependency unresolved.

## What a failed reproduction establishes

At most, it establishes that the recorded conditions did not reproduce the
claimed result as observed by the recorded instrument. It can refute a precisely
matched deterministic claim when the setup and observation are established.
It does not refute a different configuration, incomplete setup, or broader
possibility outside those conditions.

Equally, do not preserve a claim indefinitely by inventing ever-changing
conditions after contrary evidence. Fix the proposition before evaluating it;
record an explicit revision if its premises change.

## Teaching check

For each test record, finish these sentences:

> The observed result supports ___ because ___.
> It does not establish ___ because ___ remains uncontrolled or unobserved.

The second sentence is not an invitation to list every imaginable unknown. Name
only limitations that materially affect the proposition under review.
