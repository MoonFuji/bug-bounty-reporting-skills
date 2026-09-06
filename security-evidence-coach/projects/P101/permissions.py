"""Pure reference policy; no transport, credentials, or datastore implementation."""

def permitted(principal, action, record, grants):
    if action not in {"READ", "EXPORT"}:
        return False
    if principal["user_id"] == record["owner"]:
        return True
    return any(
        grant["user_id"] == principal["user_id"]
        and grant["record_id"] == record["record_id"]
        and action in grant["actions"]
        for grant in grants
    )
