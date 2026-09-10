#!/usr/bin/env python3
"""Bounded, read-only mobile ZIP metadata inventory; never extracts or runs members."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
from typing import BinaryIO

MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
MAX_DIRECTORY_BYTES = 8 * 1024 * 1024
MAX_ENTRIES = 20000
MAX_NAME_BYTES = 1024
EOCD = struct.Struct('<4s4H2IH')
CENTRAL = struct.Struct('<4s6H3I5H2I')


def safe_name(name: str) -> str:
    """Reject ambiguous/path-like metadata without ever extracting a member."""
    if not name or len(name.encode('utf-8')) > MAX_NAME_BYTES:
        raise ValueError('empty or oversized member name')
    if name.endswith('//') or '\\' in name or any(ord(c) < 32 or ord(c) == 127 for c in name):
        raise ValueError('ambiguous member name')
    parts = name.rstrip('/').split('/')
    if name.startswith('/') or any(p in {'', '.', '..'} or ':' in p for p in parts):
        raise ValueError('unsafe member path')
    return '/'.join(parts)


def read_exact(handle: BinaryIO, count: int) -> bytes:
    data = handle.read(count)
    if len(data) != count:
        raise ValueError('truncated metadata')
    return data


def directory_bounds(handle: BinaryIO, size: int) -> tuple[int, int, int]:
    length = min(size, EOCD.size + 65535)
    handle.seek(size - length)
    tail = read_exact(handle, length)
    end = len(tail)
    while True:
        offset = tail.rfind(b'PK\x05\x06', 0, end)
        if offset < 0:
            raise ValueError('ordinary ZIP end record not found')
        if offset + EOCD.size <= len(tail):
            values = EOCD.unpack_from(tail, offset)
            if offset + EOCD.size + values[-1] == len(tail):
                break
        end = offset
    _, disk, start_disk, disk_count, count, cd_size, cd_offset, _ = values
    if disk or start_disk or disk_count != count:
        raise ValueError('multidisk ZIP is unsupported')
    if count == 65535 or cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        raise ValueError('ZIP64 is unsupported')
    absolute_end = size - length + offset
    if count > MAX_ENTRIES or cd_size > MAX_DIRECTORY_BYTES:
        raise ValueError('ZIP metadata exceeds intake limits')
    if cd_offset + cd_size != absolute_end or count * CENTRAL.size > cd_size:
        raise ValueError('inconsistent or unsupported central directory layout')
    return cd_offset, cd_size, count


def parse_directory(data: bytes, expected_count: int) -> list[dict]:
    entries = []
    seen: set[str] = set()
    offset = 0
    for _ in range(expected_count):
        if len(data) - offset < CENTRAL.size:
            raise ValueError('truncated central directory')
        row = CENTRAL.unpack_from(data, offset)
        if row[0] != b'PK\x01\x02':
            raise ValueError('invalid central directory signature')
        flags, method, compressed, expanded = row[3], row[4], row[8], row[9]
        name_len, extra_len, comment_len = row[10:13]
        disk, external, local_offset = row[13], row[15], row[16]
        if disk or 0xFFFFFFFF in (compressed, expanded, local_offset):
            raise ValueError('ZIP64 or multidisk entry is unsupported')
        if not 0 < name_len <= MAX_NAME_BYTES:
            raise ValueError('empty or oversized member name')
        end = offset + CENTRAL.size + name_len + extra_len + comment_len
        if end > len(data):
            raise ValueError('truncated member metadata')
        raw = data[offset + CENTRAL.size:offset + CENTRAL.size + name_len]
        try:
            name = raw.decode('utf-8' if flags & 0x800 else 'cp437')
        except UnicodeError as exc:
            raise ValueError('invalid member-name encoding') from exc
        normalized = safe_name(name)
        if normalized in seen:
            raise ValueError('duplicate or ambiguous member path')
        seen.add(normalized)
        kind = stat.S_IFMT(external >> 16)
        if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
            raise ValueError('non-regular archive member is unsupported')
        is_dir = name.endswith('/')
        if (kind == stat.S_IFDIR and not is_dir) or (kind == stat.S_IFREG and is_dir):
            raise ValueError('inconsistent member type')
        entries.append({'name': name, 'directory': is_dir, 'compressed_bytes': compressed,
                        'declared_bytes': expanded, 'method': method,
                        'zip_encrypted': bool(flags & 1)})
        offset = end
    if offset != len(data):
        raise ValueError('unparsed central directory metadata')
    # Reject file/directory collisions even when no explicit directory entry exists.
    files = {e['name'] for e in entries if not e['directory']}
    for entry in entries:
        path = PurePosixPath(entry['name'])
        if any(str(parent) in files for parent in path.parents if str(parent) != '.'):
            raise ValueError('file and directory prefix collision')
    return entries


def summarize(entries: list[dict]) -> dict:
    names = {e['name'] for e in entries if not e['directory']}
    shapes = []
    if 'AndroidManifest.xml' in names:
        shapes.append('android-apk-like')
    if 'BundleConfig.pb' in names and 'base/manifest/AndroidManifest.xml' in names:
        shapes.append('android-aab-like')
    if 'toc.pb' in names and any(n.endswith('.apk') for n in names):
        shapes.append('android-apks-like')
    bundles = sorted({PurePosixPath(n).parts[1] for n in names
                      if len(PurePosixPath(n).parts) >= 3
                      and PurePosixPath(n).parts[0] == 'Payload'
                      and PurePosixPath(n).parts[1].endswith('.app')})
    if bundles:
        shapes.append('ios-ipa-like')
    return {
        'shape_hints': shapes or ['unrecognized'],
        'ambiguous_shape': len(shapes) > 1 or len(bundles) > 1,
        'member_count': len(entries),
        'dex_members': sum(bool(re.fullmatch(r'classes(?:\d+)?\.dex', n)) for n in names),
        'native_so_members': sum(n.startswith('lib/') and n.endswith('.so') for n in names),
        'nested_apk_members': sum(n.endswith('.apk') for n in names),
        'ios_top_level_app_count': len(bundles),
        'zip_encrypted_members': sum(e['zip_encrypted'] for e in entries),
        'declared_expanded_bytes': sum(e['declared_bytes'] for e in entries),
        'member_sample': sorted(names)[:40],
        'member_sample_truncated': len(names) > 40,
    }


def inventory(path: Path) -> dict:
    if path.is_symlink():
        raise ValueError('input symlinks are not accepted')
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, 'rb') as handle:
        before = os.fstat(handle.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise ValueError('input must be a regular file')
        if not EOCD.size <= before.st_size <= MAX_ARCHIVE_BYTES:
            raise ValueError('archive size is outside intake limits')
        cd_offset, cd_size, count = directory_bounds(handle, before.st_size)
        handle.seek(cd_offset)
        entries = parse_directory(read_exact(handle, cd_size), count)
        handle.seek(0)
        digest = hashlib.sha256()
        remaining = before.st_size
        while remaining:
            chunk = handle.read(min(1024 * 1024, remaining))
            if not chunk:
                raise ValueError('input changed while being read')
            digest.update(chunk)
            remaining -= len(chunk)
        after = os.fstat(handle.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError('input changed while being read')
    return {
        'schema_version': 1, 'file_name': path.name, 'bytes': before.st_size,
        'sha256': digest.hexdigest(), **summarize(entries),
        'limitations': [
            'Metadata only; member contents and local headers were not validated.',
            'No signature, publisher trust, installation completeness, or vulnerability verdict.',
            'ZIP encryption flags do not establish iOS executable encryption status.',
            'Hashing is not an atomic snapshot; assess an immutable isolated copy.',
            'Names and declared sizes are untrusted archive metadata.',
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact', type=Path)
    args = parser.parse_args(argv)
    try:
        result = inventory(args.artifact)
    except (OSError, ValueError, struct.error) as exc:
        print(f'INTAKE UNAVAILABLE: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
