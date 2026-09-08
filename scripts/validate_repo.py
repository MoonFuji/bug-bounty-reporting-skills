#!/usr/bin/env python3
"""Validate the reporting-skills repository using only the Python standard library."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "write-vulnerability-report",
    "harden-vulnerability-report",
    "review-vulnerability-report",
    "adapt-vulnerability-report",
    "security-evidence-coach",
    "mobile-app-security-assessment",
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError(f"{path}: malformed frontmatter") from exc
    data: dict[str, str] = {}
    current: str | None = None
    for raw in block.splitlines():
        if raw.startswith("  ") and current:
            data[current] = (data[current] + " " + raw.strip()).strip()
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        current = key.strip()
        data[current] = value.strip().strip('"')
    return data


def main() -> int:
    errors: list[str] = []
    for skill in SKILLS:
        directory = ROOT / skill
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing {skill_file.relative_to(ROOT)}")
            continue
        try:
            meta = frontmatter(skill_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if meta.get("name") != skill:
            errors.append(f"{skill}/SKILL.md: name must equal directory name")
        if not NAME_RE.fullmatch(meta.get("name", "")):
            errors.append(f"{skill}/SKILL.md: invalid skill name")
        if len(meta.get("description", "")) < 50:
            errors.append(f"{skill}/SKILL.md: description is too weak for reliable triggering")
        line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            errors.append(f"{skill}/SKILL.md: {line_count} lines exceeds the 500-line target")
        eval_file = directory / "evals" / "evals.json"
        if not eval_file.is_file():
            errors.append(f"missing {eval_file.relative_to(ROOT)}")
        else:
            try:
                payload = json.loads(eval_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{eval_file.relative_to(ROOT)}: {exc}")
            else:
                if payload.get("skill_name") != skill:
                    errors.append(f"{eval_file.relative_to(ROOT)}: skill_name mismatch")
                if not isinstance(payload.get("evals"), list) or len(payload["evals"]) < 2:
                    errors.append(f"{eval_file.relative_to(ROOT)}: at least two evals required")

    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"REPOSITORY READY: {len(SKILLS)} skills validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
