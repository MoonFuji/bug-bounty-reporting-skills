#!/usr/bin/env python3
"""Validate a persisted handoff between portable reporting agents."""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from validate_agents import DEFAULT_MANIFEST, load_json

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def iso(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty ISO-8601 timestamp")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path} must be ISO-8601")


def string_array(value: object, path: str, errors: list[str], *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return []
    if nonempty and not value:
        errors.append(f"{path} must contain at least one item")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}[{index}] must be a non-empty string")
        else:
            result.append(item)
    return result


def declared_output(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def validate_handoff(document: dict, manifest: dict) -> list[str]:
    errors: list[str] = []
    agents = manifest.get("agents")
    by_name = {
        entry.get("name"): entry
        for entry in agents if isinstance(agents, list) and isinstance(entry, dict) and isinstance(entry.get("name"), str)
    } if isinstance(agents, list) else {}

    if document.get("schema_version") != 1:
        errors.append("handoff.schema_version must be 1")
    for key in ("handoff_id", "pipeline_id", "from_agent", "to_agent", "task", "next_action"):
        if not isinstance(document.get(key), str) or not document[key].strip():
            errors.append(f"handoff.{key} must be a non-empty string")
    iso(document.get("created_at"), "handoff.created_at", errors)
    if not isinstance(document.get("fresh_context"), bool):
        errors.append("handoff.fresh_context must be a boolean")

    from_name = document.get("from_agent")
    to_name = document.get("to_agent")
    from_agent = by_name.get(from_name)
    to_agent = by_name.get(to_name)
    if from_agent is None:
        errors.append("handoff.from_agent is not in the manifest")
    if to_agent is None:
        errors.append("handoff.to_agent is not in the manifest")
    if from_name == to_name and isinstance(from_name, str):
        errors.append("handoff may not delegate to the same agent")
    if to_agent is not None and to_agent.get("fresh_context") == "required" and document.get("fresh_context") is not True:
        errors.append(f"handoff to {to_name} requires fresh_context true")

    inputs = string_array(document.get("inputs"), "handoff.inputs", errors, nonempty=True)
    expected = string_array(document.get("outputs_expected"), "handoff.outputs_expected", errors, nonempty=True)
    string_array(document.get("constraints"), "handoff.constraints", errors, nonempty=False)
    blockers = string_array(document.get("blockers"), "handoff.blockers", errors, nonempty=False)
    outputs = string_array(document.get("output_artifacts"), "handoff.output_artifacts", errors, nonempty=False)
    _ = inputs, expected

    status = document.get("status")
    if from_agent is not None:
        allowed_statuses = from_agent.get("terminal_statuses", [])
        if status not in allowed_statuses:
            errors.append(f"handoff.status {status!r} is not allowed for {from_name}")
        declared = from_agent.get("writes", [])
        if isinstance(declared, list):
            for artifact in outputs:
                if not declared_output(artifact, [value for value in declared if isinstance(value, str)]):
                    errors.append(f"{from_name} may not hand off undeclared output artifact: {artifact}")

    if status in {"COMPLETE", "READY", "PACKAGE_READY"} and blockers:
        errors.append(f"handoff.status {status} requires blockers to be empty")
    if status == "BLOCKED" and not blockers:
        errors.append("handoff.status BLOCKED requires at least one blocker")

    certifier = manifest.get("certification_agent")
    auditor = manifest.get("package_auditor")
    if status == "READY" and from_name != certifier:
        errors.append("only certification_agent may emit READY")
    if status == "PACKAGE_READY" and from_name != auditor:
        errors.append("only package_auditor may emit PACKAGE_READY")

    snapshot = document.get("claim_snapshot")
    if not isinstance(snapshot, dict):
        errors.append("handoff.claim_snapshot must be an object")
    else:
        for key in ("attacker_model", "demonstrated_impact"):
            if not isinstance(snapshot.get(key), str):
                errors.append(f"handoff.claim_snapshot.{key} must be a string")
        for key in ("report_sha256", "manifest_sha256"):
            value = snapshot.get(key)
            if value not in (None, "") and (not isinstance(value, str) or not SHA256_RE.fullmatch(value)):
                errors.append(f"handoff.claim_snapshot.{key} must be empty or a lowercase SHA-256 digest")
        if status in {"READY", "PACKAGE_READY"}:
            digest = snapshot.get("report_sha256")
            if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                errors.append(f"handoff.status {status} requires claim_snapshot.report_sha256")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        document = load_json(args.handoff)
        manifest = load_json(args.manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_handoff(document, manifest)
    if errors:
        for error in dict.fromkeys(errors):
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"HANDOFF {document['status']}: {args.handoff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
