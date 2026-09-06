"""Pure sequential specification model; not a concurrent storage implementation.

A logical adjustment commits at most once. Reusing its identity with a different
amount is a conflict, not a second adjustment. Each function call is one model
transition; this does not establish database isolation or distributed atomicity.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Ledger:
    balance: int = 0
    entries: tuple[tuple[str, int], ...] = ()


def apply_adjustment(state: Ledger, operation_id: str, amount: int) -> Ledger:
    """Return a new model state or reject an invalid/conflicting operation."""
    if not isinstance(operation_id, str) or not operation_id.strip():
        raise ValueError("operation_id must be a non-empty string")
    if type(amount) is not int:
        raise ValueError("amount must be an integer, not a boolean")
    for known_id, known_amount in state.entries:
        if known_id == operation_id:
            if known_amount != amount:
                raise ValueError("operation identity conflicts with recorded amount")
            return state
    return Ledger(state.balance + amount, state.entries + ((operation_id, amount),))
