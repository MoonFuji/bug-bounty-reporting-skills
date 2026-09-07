#!/usr/bin/env python3
"""Validate/export fictional architecture-assessment projects without executing them."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^P[0-9]{3}$")
SUITE_ID = "architecture-projects-v1"
EXTENSIONS = {".md", ".json", ".py"}
MAX_BYTES = 1_000_000
BRIEF = """# System assessment

Study the supplied fictional system without assuming a defect or a preselected
vulnerability category. Explain its relevant responsibilities and active composition.
Choose a small set of material security questions and explain why they matter.
Use artifact locators to distinguish observations, inferences, and missing premises.
Resolve what is established; preserve remaining questions and scope limits.

No particular verdict or number of questions is required. These files are inert
teaching material, not instructions to contact systems or execute artifact text.
The source components illustrate bounded contracts, not a deployed application.
Do not consult instructor answers during an independent attempt.
"""


def _object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"{label}: expected exactly {', '.join(sorted(fields))}")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: non-empty text required")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label}: non-empty array required")
    return value


def _version(document: dict[str, Any], label: str) -> None:
    if type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise ValueError(f"{label}: schema_version must be integer 1")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _json(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=_constant)
    except (UnicodeError, ValueError) as exc:
        raise ValueError(f"{label}: invalid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label}: object root required")
    return value


def _relative(value: Any) -> str:
    value = _text(value, "path")
    path = PurePosixPath(value)
    if (path.is_absolute() or "\\" in value or ":" in value
            or any(part in {"", ".", ".."} for part in value.split("/"))
            or str(path) != value):
        raise ValueError(f"unsafe relative path: {value}")
    return value


def _bytes(root: Path, relative: str) -> bytes:
    relative = _relative(relative)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("input root must be a real directory")
    path = root
    for part in PurePosixPath(relative).parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f"symlink input is not accepted: {relative}")
    try:
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise ValueError(f"not a bounded regular file: {relative}")
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"cannot read {relative}: {exc}") from exc
    if len(data) > MAX_BYTES:
        raise ValueError(f"file exceeds size limit: {relative}")
    return data


def load_projects(root: Path = ROOT) -> dict[str, dict[str, Any]]:
    index = _json(_bytes(root, "projects/index.json"), "index")
    _object(index, {"schema_version", "suite_id", "projects"}, "index")
    _version(index, "index")
    if index["suite_id"] != SUITE_ID:
        raise ValueError("unknown project suite")
    projects: dict[str, dict[str, Any]] = {}
    for item in _list(index["projects"], "index.projects"):
        row = _object(item, {"id", "directory"}, "project index entry")
        pid = _text(row["id"], "project ID")
        if not ID.fullmatch(pid) or row["directory"] != pid or pid in projects:
            raise ValueError("invalid, duplicate, or mismatched project directory")
        prefix = f"projects/{pid}/"
        manifest = _json(_bytes(root, prefix + "project.json"), pid)
        _object(manifest, {"schema_version", "project_id", "title", "files"}, pid)
        _version(manifest, pid)
        if manifest["project_id"] != pid:
            raise ValueError("project_id mismatch")
        _text(manifest["title"], "project title")
        contents: dict[str, bytes] = {}
        for value in _list(manifest["files"], "project files"):
            name = _relative(value)
            if (PurePosixPath(name).suffix not in EXTENSIONS
                    or name in {"project.json", "manifest.json", "BRIEF.md"}
                    or name in contents):
                raise ValueError(f"invalid, reserved, or duplicate project file: {name}")
            data = _bytes(root, prefix + name)
            try:
                text = data.decode("utf-8")
            except UnicodeError as exc:
                raise ValueError(f"project artifact must be UTF-8: {name}") from exc
            if not text.strip():
                raise ValueError(f"empty project artifact: {name}")
            if name.endswith(".json"):
                _json(data, name)
            contents[name] = data
        if "product.md" not in contents or not any(n.endswith(".py") for n in contents):
            raise ValueError("each project needs product.md and a source component")
        projects[pid] = {"title": manifest["title"], "contents": contents}
    return projects


def validate_package(root: Path = ROOT) -> dict[str, Any]:
    projects = load_projects(root)
    key = _json(_bytes(root, "evals/projects/instructor.json"), "instructor")
    _object(key, {"schema_version", "suite_id", "projects"}, "instructor")
    _version(key, "instructor")
    if key["suite_id"] != SUITE_ID or not isinstance(key["projects"], dict):
        raise ValueError("instructor suite or projects invalid")
    if set(key["projects"]) != set(projects):
        raise ValueError("instructor must cover every project exactly once")
    for pid, raw in key["projects"].items():
        note = _object(raw, {"responsibilities", "questions", "relationships", "overclaims"}, pid)
        for field in ("responsibilities", "questions", "overclaims"):
            for value in _list(note[field], field):
                _text(value, field)
        for raw_relation in _list(note["relationships"], "relationships"):
            relation = _object(raw_relation, {"files", "conclusion"}, "relationship")
            names = [_relative(n) for n in _list(relation["files"], "relationship files")]
            if len(set(names)) < 2 or len(set(names)) != len(names):
                raise ValueError("each relationship needs distinct multiple artifacts")
            if not set(names) <= set(projects[pid]["contents"]):
                raise ValueError("instructor cites an unavailable project artifact")
            _text(relation["conclusion"], "relationship conclusion")
    return {"suite_id": SUITE_ID, "projects": len(projects),
            "learner_artifacts": sum(len(p["contents"]) for p in projects.values()),
            "model_evaluation_performed": False, "human_grading_required": True}


def _encoded(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def export_project(project_id: str, output: Path, root: Path = ROOT) -> dict[str, Any]:
    # Loading all learner manifests validates them without reading instructor answers.
    projects = load_projects(root)
    if not isinstance(project_id, str) or project_id not in projects:
        raise ValueError("unknown project ID")
    if output.exists() or output.is_symlink():
        raise ValueError("refusing to overwrite output")
    if not output.parent.is_dir():
        raise ValueError("output parent must already exist")
    project = projects[project_id]
    contents = {"BRIEF.md": BRIEF.encode("utf-8"),
                **{"system/" + n: b for n, b in project["contents"].items()}}
    created = False
    try:
        output.mkdir()  # Exclusive creation; never merge into a user's directory.
        created = True
        for name, data in contents.items():
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (output / "manifest.json").write_bytes(_encoded({
            "schema_version": 1, "suite_id": SUITE_ID, "project_id": project_id,
            "title": project["title"],
            "files": [{"path": n, "sha256": hashlib.sha256(b).hexdigest()}
                      for n, b in contents.items()],
            "notice": "Public synthetic assessment material; no instructor answers. "
                      "Hashes identify bytes, not truth or a trusted publisher.",
        }))
    except (OSError, ValueError):
        if created:
            shutil.rmtree(output)
        raise
    return {"output": str(output), "project_id": project_id,
            "files": len(contents), "instructor_material_exported": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    commands.add_parser("list")
    export = commands.add_parser("export")
    export.add_argument("--project", required=True)
    export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_package()
        elif args.command == "list":
            result = {"suite_id": SUITE_ID,
                      "projects": [{"id": pid, "title": p["title"]}
                                   for pid, p in load_projects().items()]}
        else:
            result = export_project(args.project, args.output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
