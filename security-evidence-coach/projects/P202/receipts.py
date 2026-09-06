"""Acceptance formatting, not a committed-effect implementation."""

def receipt(attempt_id, workspace_id, operation_id):
    return {"attempt_id": attempt_id, "workspace_id": workspace_id,
            "operation_id": operation_id, "status": "accepted"}
