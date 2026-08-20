#!/usr/bin/env python3
"""Regression tests for reporting-agent handoff validation."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from validate_agent_handoff import validate_handoff  # noqa: E402
from validate_agents import load_json  # noqa: E402

DIGEST = "a" * 64


def base() -> dict:
    return {
        "schema_version": 1,
        "handoff_id": "H-001",
        "pipeline_id": "P-001",
        "from_agent": "canonical-report-writer",
        "to_agent": "report-hardener",
        "created_at": "2026-08-20T12:00:00Z",
        "fresh_context": False,
        "task": "Harden the validated canonical report.",
        "claim_snapshot": {
            "report_sha256": DIGEST,
            "manifest_sha256": "b" * 64,
            "attacker_model": "Tenant A reads tenant B report",
            "demonstrated_impact": "Cross-tenant disclosure"
        },
        "inputs": ["report.md", "report-manifest.json"],
        "outputs_expected": ["hardening-record.json"],
        "constraints": ["Do not expand demonstrated impact"],
        "status": "COMPLETE",
        "blockers": [],
        "output_artifacts": ["report.md", "report-manifest.json"],
        "next_action": "Run report hardening."
    }


def has_error(doc: dict, manifest: dict, text: str) -> bool:
    return any(text in error for error in validate_handoff(doc, manifest))


def main() -> int:
    manifest = load_json(ROOT / "agents" / "manifest.json")
    cases: list[tuple[str, bool]] = []
    cases.append(("valid writer handoff", not validate_handoff(base(), manifest)))

    doc = base()
    doc["status"] = "READY"
    cases.append(("non-reviewer cannot emit READY", has_error(doc, manifest, "only certification_agent")))

    doc = base()
    doc.update({
        "from_agent": "independent-triage-reviewer",
        "to_agent": "platform-submission-adapter",
        "fresh_context": False,
        "status": "READY",
        "output_artifacts": ["review.json", "review.md"]
    })
    cases.append(("fresh target context enforced", has_error(doc, manifest, "requires fresh_context true")))

    doc["fresh_context"] = True
    cases.append(("valid READY reviewer handoff", not validate_handoff(doc, manifest)))

    package = base()
    package.update({
        "from_agent": "final-package-auditor",
        "to_agent": "reporting-orchestrator",
        "fresh_context": True,
        "status": "PACKAGE_READY",
        "output_artifacts": ["package-audit.json"]
    })
    cases.append(("valid PACKAGE_READY handoff", not validate_handoff(package, manifest)))

    doc = base()
    doc["status"] = "BLOCKED"
    cases.append(("BLOCKED requires blockers", has_error(doc, manifest, "requires at least one blocker")))

    doc = base()
    doc["output_artifacts"] = ["review.json"]
    cases.append(("undeclared output rejected", has_error(doc, manifest, "undeclared output artifact")))

    doc = base()
    doc["created_at"] = "yesterday"
    cases.append(("invalid timestamp rejected", has_error(doc, manifest, "must be ISO-8601")))

    failed = 0
    for name, passed in cases:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        failed += 0 if passed else 1
    print(f"\n{len(cases) - failed}/{len(cases)} cases passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
