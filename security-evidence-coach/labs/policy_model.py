"""Finite teaching model, not deployable authentication or authorization middleware.

Principals and grants are already-verified, trusted records supplied by the owner.
This model does not authenticate grants or prove how they were issued.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Iterable


@dataclass(frozen=True)
class Principal:
    name: str
    tenant: str


@dataclass(frozen=True)
class Record:
    key: str
    owner: Principal


@dataclass(frozen=True)
class ReadGrant:
    record_key: str
    recipient: Principal
    issued_by: Principal
    active: bool = True


def may_read(principal: Principal | None, record: Record,
             grants: Iterable[ReadGrant] = ()) -> bool:
    """Owners and recipients of applicable active owner grants may read."""
    if principal is None:
        return False
    if principal == record.owner:
        return True
    return any(grant.record_key == record.key
               and grant.recipient == principal
               and grant.issued_by == record.owner
               and grant.active is True for grant in grants)
