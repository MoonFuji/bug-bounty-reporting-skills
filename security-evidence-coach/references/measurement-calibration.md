# Measurement and confidence without false certainty

This guide interprets supplied measurements and synthetic teaching data. It does
not generate timing probes, target traffic, or an automated vulnerability test.
All numbers below are invented or derived explicitly. No empirical performance
claim is made. Background reading is listed as unverified in [sources](sources.md).

## Separate the event, the instrument, and the claim

A claim that an effect occurred, a claim that an instrument recorded it, and a
claim that a proposed mechanism caused it are not interchangeable. A positive
instrument control demonstrates some sensitivity under specified conditions; it
does not establish perfect coverage of every effect or eliminate false positives.

A negative observation requires an appropriate event class, interval, correlation,
and detection capability. A control at another layer or another time might not
establish the missing property. Preserve the exact limits instead of asserting
that "a control passed" settles the whole question.

## Zero observed events is not a zero event rate

In a **synthetic binomial model** with `n` independent, identically distributed
trials, a fixed event probability `p`, complete detection, and a predetermined
sample size, the probability of zero events is `(1-p)^n`.

After observing zero, a one-sided 95% frequentist upper bound is:

```text
p_upper = 1 - 0.05^(1/n)
```

At 30 trials this is about 9.50%; at 100 trials it is about 2.95%. This is not a
95% posterior probability about p. It is an interval procedure with the stated
coverage property under its assumptions. It does not show the event is impossible.

Do not apply this number when trials are correlated, the stopping rule was chosen
after looking at results, or detection is incomplete. With imperfect unknown
detection, the bound pertains at best to a detected-event probability, not the
unobserved event probability. The included arithmetic helper documents these
assumptions; it cannot verify that real data satisfy them.

## The base rate matters—but must not be invented

Suppose an entirely fictional classifier has 90% sensitivity and a 10% false
positive rate in a population where 1% of cases have a property. In 10,000 cases,
it would be expected to flag 90 true cases and 990 false ones. Among positive
flags, about 8.33% would be true in this model:

```text
P(property | flag) = sensitivity * prior /
                    (sensitivity * prior + false_positive_rate * (1-prior))
```

This is an illustration, not a prior for bug bounties, an LLM, or any scanner.
Do not substitute guessed sensitivity and prevalence to manufacture a precise
confidence. The practical lesson is that a suggestive signal does not carry its
own posterior probability independent of context and measurement quality.

## Repeated evidence may be dependent

Ten reviewers quoting the same event do not provide ten independent events. Ten
requests on one warm connection may not be ten independent measurements. Hundreds
of assertions generated from one fixture may exercise only one relevant condition.

The unit of analysis may be an operation, session, process, deployment, or case
family. State it. For evaluation, preserve per-run and per-family outcomes rather
than treating every related packet as an independent trial. Agreement between
models can be correlated through shared input, tool failures, or assumptions.

## Aggregates can reverse the apparent pattern

Consider these invented outcome counts:

| Stratum | Group A | Group B |
|---|---:|---:|
| Small jobs | 81/90 | 19/20 |
| Large jobs | 2/10 | 24/80 |
| Pooled | 83/100 | 43/100 |

B has a higher observed rate in each stratum: 95% versus 90%, and 30% versus 20%.
A nevertheless has the higher pooled rate because its workload mix contains many
more small jobs. The pooled comparison alone cannot establish an improvement
within comparable workloads or a causal effect of group membership.

Do not automatically adjust for every variable either: conditioning on a variable
caused by the intervention can change the question or introduce another bias.
The relevant comparison follows the design and causal assumptions, not a habit
of adding columns until the preferred result appears.

## Statistical detection is not a security consequence

A stable numerical difference can be real while unrelated to the sensitive state
or capability asserted in a report. A test must distinguish the proposed meaning
from ordinary variance, identifiers, localization, workload, and other applicable
alternatives. It is not enough that two samples differ.

An effect size, its uncertainty, and practical meaning answer different questions.
Do not infer that a tiny but well-estimated difference enables a claimed impact,
or that a poorly estimated result is proof that no effect exists.

## Selection changes interpretation

If 20 independent null comparisons each use a 5% false-positive threshold, the
chance of at least one false positive is `1 - 0.95^20`, about 64.15%. This arithmetic
assumes independence and a true null in each comparison; it is not a universal
correction for arbitrary tests. It illustrates why reporting only the most
favorable result conceals important context.

Record how many comparisons were considered, whether outcomes were selected after
inspection, and whether a new confirmation set was used. A threshold crossed
only after repeated inspection is not equivalent to a pre-specified single test.
Do not claim a statistical procedure was run unless its data and calculation exist.

## Model evaluation: calibration is not just accuracy

A classification score asks whether labels matched a reference. Calibration asks
whether stated confidence matches observed correctness across suitable repeated
cases. Neither is guaranteed by a fluent rationale. A model may improve accuracy
while becoming worse at recognizing missing evidence, or vice versa.

The practice scorer measures labels and evidence-ID coverage, not confidence
calibration. Do not relabel those metrics. Human review checks whether uncertainty
is proportionate: neither pretending an unknown is known nor listing imaginary
unknowns when the finite packet settles the proposition.

## Report an appropriate conclusion

State the population or finite packet, observational unit, comparison, assumptions,
recorded result, and remaining limitation that materially changes interpretation.
No universal sample count or significance threshold replaces this argument.

Related: [observation and causality](observation-and-causality.md),
[advanced worked lessons](advanced-worked-lessons.md), and
[defensive arithmetic models](../labs/README.md).
