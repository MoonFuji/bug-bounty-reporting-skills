"""Tests of mathematical contracts, not model ability or real security evidence."""
from __future__ import annotations

import math
import unittest
from decimal import Decimal, localcontext

from evidence_math import pooled_rate, posterior_after_positive, zero_event_upper_bound


class BinomialBoundTests(unittest.TestCase):
    def test_single_trial_has_exact_elementary_result(self):
        self.assertAlmostEqual(zero_event_upper_bound(1), 0.95)

    def test_thirty_trials_match_independent_decimal_formula(self):
        with localcontext() as ctx:
            ctx.prec = 50
            expected = 1 - (Decimal('0.05').ln() / Decimal(30)).exp()
        self.assertAlmostEqual(zero_event_upper_bound(30), float(expected), places=14)
        self.assertAlmostEqual(float(expected), 0.09503385285530419)

    def test_bound_inverts_zero_event_probability(self):
        for n in (2, 10, 30, 100, 10000):
            with self.subTest(n=n):
                bound = zero_event_upper_bound(n)
                self.assertAlmostEqual(n * math.log1p(-bound), math.log(0.05), places=12)

    def test_more_trials_tighten_bound_under_identical_assumptions(self):
        self.assertGreater(zero_event_upper_bound(30), zero_event_upper_bound(100))
        self.assertGreater(zero_event_upper_bound(100), 0)

    def test_higher_coverage_widens_bound(self):
        self.assertGreater(zero_event_upper_bound(30, 0.01), zero_event_upper_bound(30, 0.05))

    def test_large_count_remains_positive(self):
        self.assertGreater(zero_event_upper_bound(2**53), 0)

    def test_invalid_counts_rejected(self):
        for n in (0, -1, True, 2.5, '30', 2**53 + 1):
            with self.subTest(n=n), self.assertRaises(ValueError):
                zero_event_upper_bound(n)

    def test_invalid_alpha_rejected(self):
        for a in (0, 1, -0.1, 2, True, None, math.nan, math.inf, -math.inf):
            with self.subTest(a=a), self.assertRaises(ValueError):
                zero_event_upper_bound(30, a)


class PosteriorTests(unittest.TestCase):
    def test_fictional_ten_thousand_case_counts(self):
        self.assertAlmostEqual(posterior_after_positive(0.01, 0.9, 0.1), 90 / (90 + 990))

    def test_uninformative_measurement_preserves_prior(self):
        for prior in (0.01, 0.25, 0.5, 0.9):
            self.assertAlmostEqual(posterior_after_positive(prior, 0.3, 0.3), prior)

    def test_perfect_measurement(self):
        self.assertEqual(posterior_after_positive(0.01, 1, 0), 1)

    def test_zero_prior_when_positive_event_is_possible(self):
        self.assertEqual(posterior_after_positive(0, 0.8, 0.1), 0)

    def test_certain_prior_when_positive_event_is_possible(self):
        self.assertEqual(posterior_after_positive(1, 0.8, 0.1), 1)

    def test_zero_sensitivity_with_false_positives(self):
        self.assertEqual(posterior_after_positive(0.5, 0, 0.1), 0)

    def test_impossible_conditioning_rejected(self):
        for values in ((0, 1, 0), (1, 0, 1), (0.5, 0, 0)):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, 'zero probability'):
                posterior_after_positive(*values)

    def test_small_products_do_not_create_false_undefined_result(self):
        self.assertAlmostEqual(posterior_after_positive(1e-200, 1e-200, 1e-300), 1e-100, delta=1e-112)

    def test_invalid_rates_rejected(self):
        for index in range(3):
            for bad in (-0.01, 1.01, True, None, math.nan, math.inf, 10**400):
                values = [0.5, 0.9, 0.1]
                values[index] = bad
                with self.subTest(index=index, value=bad), self.assertRaises(ValueError):
                    posterior_after_positive(*values)


class AggregationTests(unittest.TestCase):
    def test_weighted_pool_is_not_mean_of_rates(self):
        self.assertAlmostEqual(pooled_rate([(81, 90), (2, 10)]), 0.83)
        self.assertNotAlmostEqual(pooled_rate([(81, 90), (2, 10)]), (0.9 + 0.2) / 2)

    def test_reversal_described_in_lesson(self):
        self.assertLess(81 / 90, 19 / 20)
        self.assertLess(2 / 10, 24 / 80)
        self.assertGreater(pooled_rate([(81, 90), (2, 10)]), pooled_rate([(19, 20), (24, 80)]))

    def test_sequence_order_does_not_change_pool(self):
        self.assertEqual(pooled_rate([(1, 2), (3, 4)]), pooled_rate([(3, 4), (1, 2)]))

    def test_generator_supported(self):
        self.assertEqual(pooled_rate((row for row in [(1, 2), (2, 4)])), 0.5)

    def test_zero_success_is_not_missing(self):
        self.assertEqual(pooled_rate([(0, 10)]), 0)

    def test_empty_and_invalid_strata_rejected(self):
        for rows in ([], [(0, 0)], [(2, 1)], [(-1, 2)], [(True, 2)], [(1, True)], [(1.5, 2)], ['1/2'], [(1, 2, 3)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                pooled_rate(rows)

    def test_multiple_comparison_example_is_explicit_derivation(self):
        self.assertAlmostEqual(1 - 0.95**20, 0.6415140775914581)


if __name__ == '__main__':
    unittest.main(verbosity=2)
