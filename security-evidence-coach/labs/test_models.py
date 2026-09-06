#!/usr/bin/env python3
"""Specification examples for safe finite models; no target or model API calls."""
from __future__ import annotations
import itertools
import unittest
from policy_model import Principal, ReadGrant, Record, may_read
from transition_model import Ledger, apply_adjustment


class PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.owner = Principal("owner", "tenant-a")
        self.reader = Principal("reader", "tenant-b")
        self.record = Record("record-1", self.owner)
        self.grant = ReadGrant("record-1", self.reader, self.owner)

    def test_owner_allowed(self) -> None:
        self.assertTrue(may_read(self.owner, self.record))

    def test_authenticated_nonowner_is_not_automatically_allowed(self) -> None:
        self.assertFalse(may_read(self.reader, self.record))

    def test_explicit_cross_tenant_share_allowed(self) -> None:
        self.assertTrue(may_read(self.reader, self.record, [self.grant]))

    def test_anonymous_denied_even_with_share(self) -> None:
        self.assertFalse(may_read(None, self.record, [self.grant]))

    def test_inactive_grant_denied(self) -> None:
        expired = ReadGrant("record-1", self.reader, self.owner, False)
        self.assertFalse(may_read(self.reader, self.record, [expired]))

    def test_unrelated_object_grant_denied(self) -> None:
        other = ReadGrant("record-2", self.reader, self.owner)
        self.assertFalse(may_read(self.reader, self.record, [other]))

    def test_same_name_other_tenant_is_different_principal(self) -> None:
        other = Principal(self.reader.name, "tenant-c")
        self.assertFalse(may_read(other, self.record, [self.grant]))

    def test_nonowner_issuer_does_not_grant_authority(self) -> None:
        other = ReadGrant("record-1", self.reader, Principal("other", "tenant-a"))
        self.assertFalse(may_read(self.reader, self.record, [other]))

    def test_finite_permission_matrix_against_explicit_specification(self) -> None:
        stranger = Principal("stranger", "tenant-a")
        # Expected relation comes from the written lesson contract, not the code's branches.
        expected = {self.owner, self.reader}
        for actor in (None, self.owner, self.reader, stranger):
            with self.subTest(actor=actor):
                self.assertEqual(may_read(actor, self.record, [self.grant]), actor in expected)


class TransitionTests(unittest.TestCase):
    def test_one_adjustment(self) -> None:
        self.assertEqual(apply_adjustment(Ledger(), "A", 7).balance, 7)

    def test_same_identity_same_amount_is_idempotent(self) -> None:
        state = apply_adjustment(Ledger(), "A", 7)
        self.assertEqual(apply_adjustment(state, "A", 7), state)

    def test_same_identity_different_amount_rejected(self) -> None:
        state = apply_adjustment(Ledger(), "A", 7)
        with self.assertRaisesRegex(ValueError, "conflicts"):
            apply_adjustment(state, "A", 8)
        self.assertEqual(state.balance, 7)

    def test_input_state_is_unchanged(self) -> None:
        before = Ledger()
        after = apply_adjustment(before, "A", 7)
        self.assertEqual(before, Ledger())
        self.assertNotEqual(before, after)

    def test_empty_identity_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-empty"):
            apply_adjustment(Ledger(), " ", 7)

    def test_boolean_amount_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "integer"):
            apply_adjustment(Ledger(), "A", True)

    def test_distinct_identity_permutations_preserve_total(self) -> None:
        operations = (("A", 7), ("B", -2), ("C", 4))
        for ordering in itertools.permutations(operations):
            state = Ledger()
            for oid, amount in ordering:
                state = apply_adjustment(state, oid, amount)
            self.assertEqual(state.balance, 9)
            self.assertEqual(len(state.entries), 3)

    def test_repeated_sequence_does_not_double_total(self) -> None:
        state = Ledger()
        operations = (("A", 7), ("B", -2), ("C", 4))
        for oid, amount in operations * 3:
            state = apply_adjustment(state, oid, amount)
        self.assertEqual(state.balance, 9)
        self.assertEqual(len(state.entries), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
