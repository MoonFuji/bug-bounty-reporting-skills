"""Selected composition for the finite Atlas teaching project."""
from permissions import permitted


def summary(record):
    return {"record_id": record["record_id"], "title": record["title"]}


def read_summary(principal, record, grants):
    if not permitted(principal, "READ", record, grants):
        raise PermissionError("not permitted")
    return summary(record)


def export_summary(principal, record, grants):
    if not permitted(principal, "EXPORT", record, grants):
        raise PermissionError("not permitted")
    return summary(record)
