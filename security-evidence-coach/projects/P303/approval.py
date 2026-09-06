"""Consume already established verification facts under an explicit policy.

This pure model is not a cryptographic verifier or deployment tool.
"""

def permits(statement, selected_policy, roles, digest):
    return (
        statement["signature_verified"] is True
        and statement["digest"] == digest
        and statement["audience"] == selected_policy["audience"]
        and selected_policy["required_role"] in roles.get(statement["signer"], [])
    )
