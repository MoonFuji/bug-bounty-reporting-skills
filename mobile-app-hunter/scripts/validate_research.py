#!/usr/bin/env python3
"""Validate imported research metadata offline; never certify or retrieve sources."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 1024 * 1024
STATUSES = {'report_cited', 'limited_content', 'lead_only'}
SOURCE_TYPES = {'platform', 'standard', 'framework', 'authoring', 'first_party_case'}
TOP_FIELDS = {'schema_version', 'research_title', 'research_as_of', 'integrated_on',
              'provenance', 'independently_retrieved_in_integration',
              'tool_attribution', 'sources'}
SOURCE_FIELDS = {'id', 'source_type', 'url', 'title', 'status', 'claim',
                 'applicability', 'upstream_revision', 'used_by'}


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    return value


def parse_date(value: Any) -> date:
    value = text(value, 'date')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('date must use YYYY-MM-DD')
    return date.fromisoformat(value)


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def finite(value: str) -> None:
    raise ValueError(f'non-finite JSON number: {value}')


def load_index(path: Path) -> dict[str, Any]:
    with path.open('rb') as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('source index exceeds size limit')
    result = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=finite)
    if not isinstance(result, dict):
        raise ValueError('source index must be an object')
    return result


def validate_index(data: dict[str, Any], root: Path = ROOT, *,
                   as_of: date | None = None, max_age_days: int = 180) -> dict[str, Any]:
    today = as_of if as_of is not None else datetime.now(timezone.utc).date()
    if type(today) is not date:
        raise ValueError('as_of must be a date')
    if type(max_age_days) is not int or max_age_days < 1:
        raise ValueError('max_age_days must be a positive integer')
    if not isinstance(data, dict) or set(data) != TOP_FIELDS:
        raise ValueError('invalid source-index fields')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('schema_version must be integer 1')
    for field in ('research_title', 'tool_attribution'):
        text(data[field], field)
    if data['provenance'] != 'completed_research_report':
        raise ValueError('provenance must identify the completed research report')
    if data['independently_retrieved_in_integration'] is not False:
        raise ValueError('this report-backed index cannot claim independent retrieval')
    researched, integrated = parse_date(data['research_as_of']), parse_date(data['integrated_on'])
    # Authoring dates are calendar dates, potentially one day ahead of UTC.
    if researched > integrated or integrated > today + timedelta(days=1):
        raise ValueError('research/integration dates are future or out of order')
    rows = data['sources']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 200:
        raise ValueError('sources must be a bounded nonempty array')
    ids: set[str] = set()
    urls: set[str] = set()
    counts = {status: 0 for status in sorted(STATUSES)}
    root = root.resolve()
    for row in rows:
        if not isinstance(row, dict) or set(row) != SOURCE_FIELDS:
            raise ValueError('invalid source row fields')
        ident = text(row['id'], 'source.id')
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', ident) or ident in ids:
            raise ValueError('invalid or duplicate source id')
        ids.add(ident)
        if not isinstance(row['status'], str) or row['status'] not in STATUSES:
            raise ValueError('invalid source status')
        if not isinstance(row['source_type'], str) or row['source_type'] not in SOURCE_TYPES:
            raise ValueError('invalid source type')
        counts[row['status']] += 1
        for field in ('title', 'claim', 'applicability'):
            text(row[field], field)
        url = text(row['url'], 'url')
        parsed = urlsplit(url)
        if (parsed.scheme != 'https' or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or any(c.isspace() or ord(c) < 32 for c in url)):
            raise ValueError('source URL must be credential-free HTTPS')
        if url in urls:
            raise ValueError('duplicate source URL')
        urls.add(url)
        if row['upstream_revision'] is not None:
            text(row['upstream_revision'], 'upstream_revision')
        used = row['used_by']
        if not isinstance(used, list) or not used:
            raise ValueError('used_by must be a nonempty array')
        seen_paths: set[str] = set()
        for value in used:
            value = text(value, 'used_by path')
            path = Path(value)
            if (value in seen_paths or '\\' in value or path.is_absolute()
                    or any(part in {'', '.', '..'} for part in value.split('/'))
                    or path.suffix != '.md'):
                raise ValueError('used_by must contain unique relative Markdown paths')
            seen_paths.add(value)
            resolved = (root / path).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError('used_by reference is missing or escapes skill directory')
    warnings = []
    age = (today - researched).days
    if age > max_age_days:
        warnings.append(f'Research snapshot is {age} days old; review applicability before reuse.')
    return {'sources': len(rows), 'status_counts': counts, 'research_as_of': researched.isoformat(),
            'warnings': warnings, 'metadata_valid': True, 'source_truth_verified': False,
            'external_retrieval_performed': False, 'model_evaluation_performed': False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', type=Path, default=ROOT / 'references' / 'source-index.json')
    parser.add_argument('--as-of', help='YYYY-MM-DD maintenance date; defaults to UTC today')
    args = parser.parse_args(argv)
    try:
        result = validate_index(load_index(args.index), as_of=parse_date(args.as_of) if args.as_of else None)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
