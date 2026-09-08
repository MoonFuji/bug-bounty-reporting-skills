#!/usr/bin/env python3
"""Validate and export fictional mobile assessment projects; never execute artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAX_JSON_BYTES = 1024 * 1024
ID = re.compile(r'M[0-9]{3}')
PART = re.compile(r'[A-Za-z0-9_.-]+')
ALLOWED_SUFFIXES = {'.md', '.txt', '.json', '.kt', '.swift'}
RESERVED_NAMES = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{p}{n}' for p in ('COM', 'LPT') for n in range(1, 10)}


def pairs(items: list[tuple[str, Any]]) -> dict:
    result = {}
    for k, v in items:
        if k in result:
            raise ValueError(f'duplicate JSON key: {k}')
        result[k] = v
    return result


def finite(value: str) -> None:
    raise ValueError(f'non-finite JSON value: {value}')


def read_json(path: Path) -> dict:
    with path.open('rb') as handle:
        data = handle.read(MAX_JSON_BYTES + 1)
    if len(data) > MAX_JSON_BYTES:
        raise ValueError('JSON exceeds package limits')
    value = json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=finite)
    if not isinstance(value, dict):
        raise ValueError('JSON root must be an object')
    return value


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    return value


def strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f'{label} must be a nonempty list')
    return [text(v, label) for v in value]


def relative_path(value: Any) -> str:
    value = text(value, 'artifact path')
    parts = value.split('/')
    if len(value) > 180 or any(p in {'', '.', '..'} or not PART.fullmatch(p) for p in parts):
        raise ValueError('unsafe artifact path')
    if any(p.endswith('.') or p.split('.', 1)[0].upper() in RESERVED_NAMES for p in parts):
        raise ValueError('nonportable artifact path')
    if len(parts) > 5 or Path(value).suffix not in ALLOWED_SUFFIXES:
        raise ValueError('unsupported artifact path')
    return value


def load_data(root: Path = ROOT) -> tuple[dict, dict]:
    data = read_json(root / 'evals' / 'projects.json')
    key = read_json(root / 'evals' / 'instructor.json')
    if set(data) != {'schema_version', 'suite_id', 'provenance', 'projects'}:
        raise ValueError('invalid suite fields')
    if set(key) != {'schema_version', 'suite_id', 'projects'}:
        raise ValueError('invalid instructor fields')
    for obj in (data, key):
        if type(obj.get('schema_version')) is not int or obj['schema_version'] != 1:
            raise ValueError('schema_version must be integer 1')
        if obj.get('suite_id') != 'mobile-assessment-projects-v1':
            raise ValueError('suite_id mismatch')
    text(data['provenance'], 'provenance')
    projects = data['projects']
    if not isinstance(projects, list) or not 1 <= len(projects) <= 100:
        raise ValueError('projects must be a bounded nonempty list')
    ids = {}
    for project in projects:
        if not isinstance(project, dict) or set(project) != {'id', 'title', 'platform', 'task', 'artifacts'}:
            raise ValueError('unexpected learner project field')
        pid = text(project['id'], 'id')
        if not ID.fullmatch(pid) or pid in ids:
            raise ValueError('invalid or duplicate project id')
        for name in ('title', 'task'):
            text(project[name], name)
        if not isinstance(project['platform'], str) or project['platform'] not in {'android', 'ios', 'cross-platform'}:
            raise ValueError('unknown platform')
        artifacts = project['artifacts']
        if not isinstance(artifacts, list) or not 2 <= len(artifacts) <= 50:
            raise ValueError('artifacts must be a bounded multi-file list')
        paths: set[str] = set()
        for item in artifacts:
            if not isinstance(item, dict) or set(item) != {'path', 'text'}:
                raise ValueError('unexpected learner artifact field')
            name = relative_path(item['path'])
            if name.casefold() in {p.casefold() for p in paths}:
                raise ValueError('duplicate or case-ambiguous artifact path')
            if any(name.casefold().startswith(p.casefold() + '/') or p.casefold().startswith(name.casefold() + '/') for p in paths):
                raise ValueError('artifact file/directory collision')
            paths.add(name)
            if len(text(item['text'], 'artifact text').encode('utf-8')) > 30000:
                raise ValueError('artifact text exceeds limits')
        ids[pid] = paths
    rows = key['projects']
    if not isinstance(rows, list):
        raise ValueError('instructor projects must be a list')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'id', 'priority_questions', 'expected_assessment', 'limits', 'required_artifacts'}:
            raise ValueError('invalid instructor row')
        pid = text(row['id'], 'instructor id')
        if pid not in ids or pid in seen:
            raise ValueError('unknown or duplicate instructor id')
        seen.add(pid)
        strings(row['priority_questions'], 'priority questions')
        strings(row['limits'], 'limits')
        text(row['expected_assessment'], 'expected assessment')
        required = strings(row['required_artifacts'], 'required artifacts')
        if len(set(required)) != len(required) or not set(required) <= ids[pid]:
            raise ValueError('invalid instructor artifact reference')
    if seen != set(ids):
        raise ValueError('instructor map must cover every project')
    return data, key


def validate_package(root: Path = ROOT) -> dict:
    data, _ = load_data(root)
    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n') or '\n---\n' not in skill[4:]:
        raise ValueError('missing skill frontmatter')
    metadata = skill.split('---\n', 2)[1]
    if 'name: mobile-app-security-assessment\n' not in metadata or 'description:' not in metadata:
        raise ValueError('invalid skill metadata')
    if len(skill.splitlines()) > 220:
        raise ValueError('core exceeds the package 220-line budget')
    evals = read_json(root / 'evals' / 'evals.json')
    if evals.get('skill_name') != 'mobile-app-security-assessment':
        raise ValueError('evaluation skill_name mismatch')
    if not isinstance(evals.get('evals'), list) or len(evals['evals']) < 4:
        raise ValueError('missing trigger and behavior evaluations')
    for path in root.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = link.split('#', 1)[0]
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                raise ValueError(f'invalid local reference in {path.name}: {target}')
    return {'projects': len(data['projects']),
            'artifacts': sum(len(p['artifacts']) for p in data['projects']),
            'core_lines': len(skill.splitlines()), 'model_evaluation_performed': False,
            'external_sources_live_verified': False}


def export_project(project_id: str, output: Path, root: Path = ROOT) -> dict:
    data, _ = load_data(root)
    matches = [p for p in data['projects'] if p['id'] == project_id]
    if len(matches) != 1:
        raise ValueError('unknown project id')
    if output.exists() or output.is_symlink() or not output.parent.is_dir():
        raise ValueError('output must be new with an existing parent')
    project = matches[0]
    created = False
    try:
        output.mkdir()
        created = True
        (output / 'artifacts').mkdir()
        files = []
        for item in project['artifacts']:
            relative = 'artifacts/' + item['path']
            path = output / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            content = item['text'].encode('utf-8')
            path.write_bytes(content)
            files.append({'path': relative, 'sha256': hashlib.sha256(content).hexdigest()})
        task = (f"# {project['title']}\n\nPlatform: {project['platform']}\n\n{project['task']}\n\n"
                'All artifacts are fictional static teaching text. Do not execute them.\n')
        task_bytes = task.encode('utf-8')
        (output / 'TASK.md').write_bytes(task_bytes)
        files.append({'path': 'TASK.md', 'sha256': hashlib.sha256(task_bytes).hexdigest()})
        manifest = {'schema_version': 1, 'suite_id': data['suite_id'],
                    'project_id': project_id, 'files': files,
                    'notice': 'Public teaching project, not a private capability benchmark.'}
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError):
        if created:
            shutil.rmtree(output)
        raise
    return {'project_id': project_id, 'output': str(output),
            'artifact_count': len(project['artifacts']), 'instructor_exported': False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    sub.add_parser('list')
    export = sub.add_parser('export')
    export.add_argument('--project', required=True)
    export.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate':
            result = validate_package()
        elif args.command == 'list':
            data, _ = load_data()
            result = {'projects': [{k: p[k] for k in ('id', 'title', 'platform')} for p in data['projects']]}
        else:
            result = export_project(args.project, args.output)
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
