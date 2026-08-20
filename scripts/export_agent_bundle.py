#!/usr/bin/env python3
"""Export canonical reporting-agent contracts for external harnesses."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "agents" / "manifest.json"


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def build_bundle(manifest_path: Path) -> list[dict]:
    manifest = load_json(manifest_path)
    base = manifest_path.resolve().parents[1]
    agents = manifest.get("agents")
    if not isinstance(agents, list):
        raise ValueError("manifest.agents must be an array")
    bundle: list[dict] = []
    for entry in agents:
        if not isinstance(entry, dict):
            raise ValueError("every manifest agent must be an object")
        name = entry.get("name")
        file_value = entry.get("file")
        if not isinstance(name, str) or not name:
            raise ValueError("agent.name must be a non-empty string")
        if not isinstance(file_value, str) or not file_value:
            raise ValueError(f"{name}: file must be a non-empty string")
        prompt_path = base / file_value
        try:
            prompt = prompt_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"{name}: cannot read {prompt_path}: {exc}") from exc
        bundle.append({
            "name": name,
            "class": entry.get("class"),
            "role": entry.get("role"),
            "skills": entry.get("skills", []),
            "fresh_context": entry.get("fresh_context"),
            "sandbox": entry.get("sandbox"),
            "tools": entry.get("tools", []),
            "reads": entry.get("reads", []),
            "writes": entry.get("writes", []),
            "may_mutate_report": entry.get("may_mutate_report", False),
            "may_certify_claim": entry.get("may_certify_claim", False),
            "may_certify_package": entry.get("may_certify_package", False),
            "terminal_statuses": entry.get("terminal_statuses", []),
            "prompt": prompt,
        })
    return bundle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--format", choices=("json", "jsonl", "plain-dir"), default="json")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        bundle = build_bundle(args.manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        args.output.write_text(json.dumps({"schema_version": 1, "agents": bundle}, indent=2) + "\n", encoding="utf-8")
    elif args.format == "jsonl":
        args.output.write_text("".join(json.dumps(agent) + "\n" for agent in bundle), encoding="utf-8")
    else:
        args.output.mkdir(parents=True, exist_ok=True)
        for agent in bundle:
            (args.output / f"{agent['name']}.md").write_text(agent["prompt"], encoding="utf-8")
        (args.output / "manifest.json").write_text(
            json.dumps({"schema_version": 1, "agents": [{k: v for k, v in a.items() if k != "prompt"} for a in bundle]}, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"EXPORTED {len(bundle)} AGENTS: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
