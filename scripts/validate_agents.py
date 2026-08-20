#!/usr/bin/env python3
"""Validate portable reporting-agent contracts, adapters, and separation rules."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "agents" / "manifest.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRESHNESS = {"required", "recommended", "not_required"}
CLASSES = {"core", "specialist"}
SANDBOXES = {"read_only", "workspace_write"}
REQUIRED_AGENTS = {
    "reporting-orchestrator",
    "evidence-curator",
    "canonical-report-writer",
    "report-hardener",
    "proof-reproduction-verifier",
    "impact-severity-analyst",
    "variant-radius-analyst",
    "remediation-engineer",
    "novelty-route-policy-analyst",
    "disclosure-safety-reviewer",
    "independent-triage-reviewer",
    "platform-submission-adapter",
    "final-package-auditor",
}
ALLOWED_REPORT_MUTATORS = {"canonical-report-writer", "report-hardener"}


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


def frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    pieces = text.split("---\n", 2)
    if len(pieces) < 3:
        raise ValueError(f"{path}: malformed YAML frontmatter")
    result: dict[str, str] = {}
    for line in pieces[1].splitlines():
        if line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def nonempty_strings(value: object, path: str, errors: list[str], *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return []
    if not allow_empty and not value:
        errors.append(f"{path} must contain at least one item")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}[{index}] must be a non-empty string")
        else:
            result.append(item)
    return result


def validate_manifest(manifest: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("manifest.schema_version must be 1")

    for key in ("entry_agent", "certification_agent", "package_auditor", "handoff_schema", "pipeline_state_schema"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            errors.append(f"manifest.{key} must be a non-empty string")

    for key in ("handoff_schema", "pipeline_state_schema"):
        value = manifest.get(key)
        if isinstance(value, str) and value and not (root / value).is_file():
            errors.append(f"manifest.{key} does not exist: {value}")

    entries = manifest.get("agents")
    if not isinstance(entries, list):
        return errors + ["manifest.agents must be an array"]

    by_name: dict[str, dict] = {}
    known_skills = {path.parent.name for path in root.glob("*/SKILL.md")}
    for index, entry in enumerate(entries):
        path = f"manifest.agents[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{path} must be an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{path}.name must be kebab-case")
            continue
        if name in by_name:
            errors.append(f"duplicate agent name: {name}")
            continue
        by_name[name] = entry

        if entry.get("class") not in CLASSES:
            errors.append(f"{name}: class must be core or specialist")
        if entry.get("fresh_context") not in FRESHNESS:
            errors.append(f"{name}: fresh_context must be required, recommended, or not_required")
        if entry.get("sandbox") not in SANDBOXES:
            errors.append(f"{name}: sandbox must be read_only or workspace_write")
        if not isinstance(entry.get("role"), str) or not entry["role"].strip():
            errors.append(f"{name}: role must be a non-empty string")

        skills = nonempty_strings(entry.get("skills"), f"{name}.skills", errors)
        unknown_skills = sorted(set(skills) - known_skills)
        if unknown_skills:
            errors.append(f"{name}: unknown skills {unknown_skills}")
        nonempty_strings(entry.get("tools"), f"{name}.tools", errors)
        nonempty_strings(entry.get("reads"), f"{name}.reads", errors)
        writes = nonempty_strings(entry.get("writes"), f"{name}.writes", errors)
        statuses = nonempty_strings(entry.get("terminal_statuses"), f"{name}.terminal_statuses", errors)

        for boolean in ("may_mutate_report", "may_certify_claim", "may_certify_package"):
            if not isinstance(entry.get(boolean), bool):
                errors.append(f"{name}: {boolean} must be a boolean")

        if entry.get("may_mutate_report") is True and name not in ALLOWED_REPORT_MUTATORS:
            errors.append(f"{name}: only writer and hardener may mutate report.md")
        if "report.md" in writes and entry.get("may_mutate_report") is not True:
            errors.append(f"{name}: writes report.md but may_mutate_report is false")
        if entry.get("may_mutate_report") is True and (
            entry.get("may_certify_claim") is True or entry.get("may_certify_package") is True
        ):
            errors.append(f"{name}: an artifact mutator may not certify the same workflow")
        if entry.get("may_certify_claim") is True and "READY" not in statuses:
            errors.append(f"{name}: claim certifier must support READY")
        if entry.get("may_certify_package") is True and "PACKAGE_READY" not in statuses:
            errors.append(f"{name}: package certifier must support PACKAGE_READY")

        file_value = entry.get("file")
        if not isinstance(file_value, str) or not file_value.strip():
            errors.append(f"{name}: file must be a non-empty string")
            continue
        canonical = root / file_value
        if not canonical.is_file():
            errors.append(f"{name}: canonical prompt missing: {file_value}")
        else:
            try:
                meta = frontmatter(canonical)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if meta.get("name") != name:
                    errors.append(f"{name}: canonical frontmatter name mismatch")
                if meta.get("role") != entry.get("role"):
                    errors.append(f"{name}: canonical role does not match manifest")
                if meta.get("fresh_context") != entry.get("fresh_context"):
                    errors.append(f"{name}: canonical fresh_context does not match manifest")
                if len(meta.get("description", "")) < 50:
                    errors.append(f"{name}: description is too weak for reliable selection")
            if len(canonical.read_text(encoding="utf-8").splitlines()) > 220:
                errors.append(f"{name}: canonical prompt exceeds 220 lines")

        wrapper = root / ".claude" / "agents" / f"{name}.md"
        if not wrapper.is_file():
            errors.append(f"{name}: Claude Code wrapper missing")
        else:
            try:
                wrapper_meta = frontmatter(wrapper)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if wrapper_meta.get("name") != name:
                    errors.append(f"{name}: Claude wrapper name mismatch")
            if f"agents/{name}.md" not in wrapper.read_text(encoding="utf-8"):
                errors.append(f"{name}: Claude wrapper must point to canonical prompt")

    names = set(by_name)
    if names != REQUIRED_AGENTS:
        errors.append(
            f"manifest agent set mismatch; missing={sorted(REQUIRED_AGENTS - names)}, extra={sorted(names - REQUIRED_AGENTS)}"
        )

    core = set(nonempty_strings(manifest.get("core_agents"), "manifest.core_agents", errors))
    specialists = set(nonempty_strings(manifest.get("specialist_agents"), "manifest.specialist_agents", errors))
    actual_core = {name for name, entry in by_name.items() if entry.get("class") == "core"}
    actual_specialists = {name for name, entry in by_name.items() if entry.get("class") == "specialist"}
    if core != actual_core:
        errors.append("manifest.core_agents must exactly match agents with class core")
    if specialists != actual_specialists:
        errors.append("manifest.specialist_agents must exactly match agents with class specialist")
    if core & specialists:
        errors.append("core_agents and specialist_agents must not overlap")

    entry_agent = manifest.get("entry_agent")
    if entry_agent not in by_name or by_name.get(entry_agent, {}).get("role") != "orchestrator":
        errors.append("entry_agent must name the orchestrator")
    cert_name = manifest.get("certification_agent")
    claim_certifiers = [name for name, entry in by_name.items() if entry.get("may_certify_claim") is True]
    if claim_certifiers != [cert_name]:
        errors.append("exactly certification_agent may certify the vulnerability claim")
    elif by_name[cert_name].get("fresh_context") != "required":
        errors.append("certification_agent must require a fresh context")
    elif by_name[cert_name].get("may_mutate_report") is not False:
        errors.append("certification_agent may not mutate report.md")

    package_name = manifest.get("package_auditor")
    package_certifiers = [name for name, entry in by_name.items() if entry.get("may_certify_package") is True]
    if package_certifiers != [package_name]:
        errors.append("exactly package_auditor may certify the submission package")
    elif by_name[package_name].get("fresh_context") != "required":
        errors.append("package_auditor must require a fresh context")
    elif by_name[package_name].get("may_mutate_report") is not False:
        errors.append("package_auditor may not mutate report.md")

    orchestrator = by_name.get("reporting-orchestrator", {})
    if any(orchestrator.get(key) is True for key in ("may_mutate_report", "may_certify_claim", "may_certify_package")):
        errors.append("reporting-orchestrator may coordinate only; it may not mutate or certify")

    pipeline = manifest.get("pipeline")
    if not isinstance(pipeline, list) or not pipeline:
        errors.append("manifest.pipeline must contain at least one edge")
    else:
        for index, edge in enumerate(pipeline):
            path = f"manifest.pipeline[{index}]"
            if not isinstance(edge, dict):
                errors.append(f"{path} must be an object")
                continue
            if edge.get("from") not in by_name:
                errors.append(f"{path}.from names an unknown agent")
            if edge.get("to") not in by_name:
                errors.append(f"{path}.to names an unknown agent")
            if not isinstance(edge.get("condition"), str) or not edge["condition"].strip():
                errors.append(f"{path}.condition must be a non-empty string")

    evals_path = root / "agents" / "evals" / "evals.json"
    if not evals_path.is_file():
        errors.append("agents/evals/evals.json is missing")
    else:
        try:
            evals = load_json(evals_path)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if not isinstance(evals.get("evals"), list) or len(evals["evals"]) < 3:
                errors.append("agents/evals/evals.json requires at least three evals")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_json(args.manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    root = args.manifest.resolve().parents[1]
    errors = validate_manifest(manifest, root)
    if errors:
        for error in dict.fromkeys(errors):
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"AGENTS READY: {len(manifest['agents'])} validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
