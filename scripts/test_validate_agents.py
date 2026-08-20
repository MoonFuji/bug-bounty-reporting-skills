#!/usr/bin/env python3
"""Regression tests for reporting-agent manifest validation and export."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from validate_agents import load_json, validate_manifest  # noqa: E402


def agent(doc: dict, name: str) -> dict:
    return next(entry for entry in doc["agents"] if entry["name"] == name)


def has_error(doc: dict, text: str) -> bool:
    return any(text in error for error in validate_manifest(doc, ROOT))


def main() -> int:
    manifest = load_json(ROOT / "agents" / "manifest.json")
    cases: list[tuple[str, bool]] = []
    cases.append(("valid manifest", not validate_manifest(manifest, ROOT)))

    doc = copy.deepcopy(manifest)
    agent(doc, "reporting-orchestrator")["may_certify_claim"] = True
    cases.append(("orchestrator cannot certify", has_error(doc, "may coordinate only")))

    doc = copy.deepcopy(manifest)
    agent(doc, "independent-triage-reviewer")["fresh_context"] = "recommended"
    cases.append(("claim reviewer must be fresh", has_error(doc, "must require a fresh context")))

    doc = copy.deepcopy(manifest)
    agent(doc, "canonical-report-writer")["may_certify_claim"] = True
    cases.append(("writer cannot self-certify", has_error(doc, "artifact mutator may not certify")))

    doc = copy.deepcopy(manifest)
    agent(doc, "independent-triage-reviewer")["file"] = "agents/missing.md"
    cases.append(("missing canonical prompt rejected", has_error(doc, "canonical prompt missing")))

    doc = copy.deepcopy(manifest)
    doc["core_agents"].append("proof-reproduction-verifier")
    cases.append(("class lists must match", has_error(doc, "core_agents must exactly match")))

    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "agents.json"
        proc = subprocess.run(
            [sys.executable, str(HERE / "export_agent_bundle.py"), "--format", "json", "--output", str(output)],
            capture_output=True,
            text=True,
        )
        exported = json.loads(output.read_text(encoding="utf-8")) if output.exists() else {}
        cases.append(("portable export contains every agent", proc.returncode == 0 and len(exported.get("agents", [])) == 13))

    failed = 0
    for name, passed in cases:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        failed += 0 if passed else 1
    print(f"\n{len(cases) - failed}/{len(cases)} cases passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
