"""Arithmetic for fictional evidence lessons, not a security-confidence estimator.

Inputs are explicitly supplied assumptions. These helpers cannot establish sample
independence, measurement completeness, applicability, or any real vulnerability.
No data collection, network access, or model invocation occurs here.
"""
from __future__ import annotations

import math
from collections.abc import Iterable


def _probability(value: float, name: str) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{name} must be a finite number in [0, 1], not a boolean")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} must be a finite probability") from exc
    if not math.isfinite(result) or not 0 <= result <= 1:
        raise ValueError(f"{name} must be a finite number in [0, 1]")
    return result


def zero_event_upper_bound(trials: int, alpha: float = 0.05) -> float:
    """One-sided (1-alpha) binomial upper bound after zero detected events.

    Requires IID fixed-probability trials, predetermined n, and complete detection.
    No inference of those assumptions is performed. Counts are limited to the
    exact integer range of binary64, the arithmetic used by this teaching helper.
    This is a frequentist bound, not a posterior probability or proof of absence.
    """
    if type(trials) is not int or not 1 <= trials <= 2**53:
        raise ValueError("trials must be an integer from 1 through 2**53")
    a = _probability(alpha, "alpha")
    if not 0 < a < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    # expm1 preserves accuracy when the bound is close to zero.
    return -math.expm1(math.log(a) / trials)


def posterior_after_positive(prior: float, sensitivity: float,
                             false_positive_rate: float) -> float:
    """Bayes arithmetic under explicitly supplied fictional rates.

    Does not estimate these rates or recommend priors for security findings.
    Conditioning on an impossible positive event is rejected as undefined.
    Log-domain arithmetic avoids underflow of very small nonzero products.
    """
    p = _probability(prior, "prior")
    s = _probability(sensitivity, "sensitivity")
    f = _probability(false_positive_rate, "false_positive_rate")
    positive = p > 0 and s > 0
    negative = p < 1 and f > 0
    if not positive and not negative:
        raise ValueError("conditioning event has zero probability")
    if not positive:
        return 0.0
    if not negative:
        return 1.0
    log_true = math.log(p) + math.log(s)
    log_false = math.log1p(-p) + math.log(f)
    difference = log_false - log_true
    if difference >= 0:
        ratio = math.exp(-difference)
        return ratio / (1 + ratio)
    return 1 / (1 + math.exp(difference))


def pooled_rate(strata: Iterable[tuple[int, int]]) -> float:
    """Observed total successes / total trials, not a causal comparison.

    A pooled rate can reverse within-stratum ordering when group mixtures differ.
    Count pairs must have positive denominators; no missing stratum is imputed.
    """
    successes = trials = 0
    for row in strata:
        if not isinstance(row, (tuple, list)) or len(row) != 2:
            raise ValueError("each stratum must be a (successes, trials) pair")
        hit, count = row
        if type(hit) is not int or type(count) is not int or not 0 <= hit <= count or count <= 0:
            raise ValueError("counts must be integers with 0 <= successes <= positive trials")
        successes += hit
        trials += count
    if not trials:
        raise ValueError("at least one nonempty stratum is required")
    return successes / trials
