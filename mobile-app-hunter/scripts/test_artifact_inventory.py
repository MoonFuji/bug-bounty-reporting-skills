"""Synthetic ordinary ZIP tests; no real apps, target traffic, or member execution."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import artifact_inventory as ai


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = self.root / 'sample.apk'

    def tearDown(self):
        self.tmp.cleanup()

    def archive(self, names, *, comment=b'', compression=zipfile.ZIP_STORED):
        with zipfile.ZipFile(self.path, 'w', compression=compression) as archive:
            for name in names:
                archive.writestr(name, 'fictional metadata fixture')
            archive.comment = comment
        return self.path

    def test_apk_shape_hash_and_no_writes(self):
        self.archive(['AndroidManifest.xml', 'classes.dex', 'classes2.dex', 'lib/arm64-v8a/libx.so'])
        before = self.path.read_bytes()
        result = ai.inventory(self.path)
        self.assertEqual(result['sha256'], hashlib.sha256(before).hexdigest())
        self.assertEqual(result['shape_hints'], ['android-apk-like'])
        self.assertEqual((result['dex_members'], result['native_so_members']), (2, 1))
        self.assertEqual(list(self.root.iterdir()), [self.path])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotIn('severity', result)

    def test_ipa_shape_does_not_claim_signature_or_encryption(self):
        self.archive(['Payload/Example.app/Info.plist', 'Payload/Example.app/Example'])
        result = ai.inventory(self.path)
        self.assertEqual(result['shape_hints'], ['ios-ipa-like'])
        self.assertEqual(result['ios_top_level_app_count'], 1)
        self.assertIn('No signature', ' '.join(result['limitations']))
        self.assertIn('executable encryption', ' '.join(result['limitations']))

    def test_aab_shape(self):
        self.archive(['BundleConfig.pb', 'base/manifest/AndroidManifest.xml'])
        self.assertEqual(ai.inventory(self.path)['shape_hints'], ['android-aab-like'])

    def test_apks_shape(self):
        self.archive(['toc.pb', 'splits/base.apk', 'splits/lang.apk'])
        result = ai.inventory(self.path)
        self.assertEqual(result['shape_hints'], ['android-apks-like'])
        self.assertEqual(result['nested_apk_members'], 2)

    def test_suffix_is_not_shape_evidence(self):
        self.archive(['notes.txt'])
        self.assertEqual(ai.inventory(self.path)['shape_hints'], ['unrecognized'])

    def test_mixed_shapes_are_ambiguous(self):
        self.archive(['AndroidManifest.xml', 'Payload/App.app/Info.plist'])
        self.assertTrue(ai.inventory(self.path)['ambiguous_shape'])

    def test_multiple_top_level_ios_apps_are_ambiguous(self):
        self.archive(['Payload/A.app/Info.plist', 'Payload/B.app/Info.plist'])
        self.assertTrue(ai.inventory(self.path)['ambiguous_shape'])

    def test_nested_extension_does_not_count_as_another_main_app(self):
        self.archive(['Payload/A.app/Info.plist', 'Payload/A.app/PlugIns/W.appex/Info.plist'])
        self.assertEqual(ai.inventory(self.path)['ios_top_level_app_count'], 1)

    def test_member_contents_are_never_decompressed(self):
        self.archive(['AndroidManifest.xml', 'assets/test.txt'], compression=zipfile.ZIP_DEFLATED)
        with patch.object(zipfile.ZipFile, 'open', side_effect=AssertionError('must not decompress')):
            self.assertEqual(ai.inventory(self.path)['member_count'], 2)

    def test_empty_archive_is_unrecognized_not_vulnerable(self):
        self.archive([])
        self.assertEqual(ai.inventory(self.path)['member_count'], 0)

    def test_truncated_archive_rejected(self):
        self.path.write_bytes(b'PK' * 50)
        with self.assertRaisesRegex(ValueError, 'end record'):
            ai.inventory(self.path)

    def test_short_archive_rejected(self):
        self.path.write_bytes(b'PK')
        with self.assertRaisesRegex(ValueError, 'size'):
            ai.inventory(self.path)

    def test_size_limit_precedes_metadata_read(self):
        self.archive(['AndroidManifest.xml'])
        with patch.object(ai, 'MAX_ARCHIVE_BYTES', 30):
            with self.assertRaisesRegex(ValueError, 'size'):
                ai.inventory(self.path)

    def test_directory_budget_precedes_directory_parse(self):
        self.archive(['AndroidManifest.xml'])
        with patch.object(ai, 'MAX_DIRECTORY_BYTES', 10):
            with self.assertRaisesRegex(ValueError, 'limits'):
                ai.inventory(self.path)

    def test_entry_budget(self):
        self.archive(['A', 'B'])
        with patch.object(ai, 'MAX_ENTRIES', 1):
            with self.assertRaisesRegex(ValueError, 'limits'):
                ai.inventory(self.path)

    def patch_end(self, index, value):
        data = bytearray(self.path.read_bytes())
        values = list(ai.EOCD.unpack_from(data, len(data) - ai.EOCD.size))
        values[index] = value
        data[-ai.EOCD.size:] = ai.EOCD.pack(*values)
        self.path.write_bytes(data)

    def test_zip64_explicitly_unsupported(self):
        self.archive([])
        self.patch_end(5, 0xFFFFFFFF)
        with self.assertRaisesRegex(ValueError, 'ZIP64'):
            ai.inventory(self.path)

    def test_multidisk_explicitly_unsupported(self):
        self.archive([])
        self.patch_end(1, 1)
        with self.assertRaisesRegex(ValueError, 'multidisk'):
            ai.inventory(self.path)

    def test_inconsistent_directory_offset(self):
        self.archive(['A'])
        self.patch_end(6, 0)
        with self.assertRaisesRegex(ValueError, 'layout'):
            ai.inventory(self.path)

    def test_signature_like_text_in_comment(self):
        self.archive(['A'], comment=b'comment PK\x05\x06 with no full record')
        self.assertEqual(ai.inventory(self.path)['member_count'], 1)

    def test_ambiguous_paths_rejected(self):
        for name in ('../A', '/A', 'a//', 'a//b', 'a/./b', 'C:/b', 'a\\b', 'a\x00b', 'a\nb'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                ai.safe_name(name)

    def test_duplicate_path_rejected(self):
        with zipfile.ZipFile(self.path, 'w') as archive:
            archive.writestr('a/', '')
            archive.writestr('a', 'not a directory')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            ai.inventory(self.path)

    def test_prefix_collision_rejected(self):
        self.archive(['a', 'a/b'])
        with self.assertRaisesRegex(ValueError, 'prefix collision'):
            ai.inventory(self.path)

    def test_directory_and_child_are_valid(self):
        self.archive(['a/', 'a/b'])
        self.assertEqual(ai.inventory(self.path)['member_count'], 2)

    def test_archive_symlink_entry_rejected(self):
        entry = zipfile.ZipInfo('link')
        entry.create_system = 3
        entry.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(self.path, 'w') as archive:
            archive.writestr(entry, 'somewhere')
        with self.assertRaisesRegex(ValueError, 'non-regular'):
            ai.inventory(self.path)

    def test_input_symlink_rejected(self):
        self.archive([])
        alias = self.root / 'alias'
        alias.symlink_to(self.path)
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            ai.inventory(alias)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO unavailable')
    def test_fifo_is_not_read_or_blocked(self):
        os.mkfifo(self.path)
        with self.assertRaisesRegex(ValueError, 'regular file'):
            ai.inventory(self.path)

    def test_member_sample_is_bounded(self):
        self.archive([f'resources/{i}.txt' for i in range(41)])
        result = ai.inventory(self.path)
        self.assertEqual(len(result['member_sample']), 40)
        self.assertTrue(result['member_sample_truncated'])

    def test_cli_reports_error_without_success_output(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = ai.main([str(self.root / 'absent')])
        self.assertEqual(result, 2)
        self.assertEqual(out.getvalue(), '')
        self.assertIn('INTAKE UNAVAILABLE', err.getvalue())

    def test_cli_success_outputs_json(self):
        self.archive(['AndroidManifest.xml'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(ai.main([str(self.path)]), 0)
        self.assertEqual(json.loads(out.getvalue())['member_count'], 1)


if __name__ == '__main__':
    unittest.main()
