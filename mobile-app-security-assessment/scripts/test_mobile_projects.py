"""Package, export, and negative-input tests; these do not grade any AI model."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import mobile_projects as mp


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / 'skill'
        shutil.copytree(mp.ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__'))
        self.output = self.base / 'export'

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, file, change):
        path = self.root / 'evals' / file
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_package_contract(self):
        result = mp.validate_package(self.root)
        self.assertEqual((result['projects'], result['artifacts']), (8, 32))
        self.assertLessEqual(result['core_lines'], 220)
        self.assertFalse(result['model_evaluation_performed'])
        self.assertFalse(result['external_sources_live_verified'])

    def test_all_exports_hashes_and_instructor_exclusion(self):
        data, _ = mp.load_data(self.root)
        for project in data['projects']:
            with self.subTest(project=project['id']):
                output = self.base / project['id']
                result = mp.export_project(project['id'], output, self.root)
                self.assertFalse(result['instructor_exported'])
                manifest = json.loads((output / 'manifest.json').read_text())
                expected = {'manifest.json', 'TASK.md'} | {'artifacts/' + a['path'] for a in project['artifacts']}
                actual = {str(p.relative_to(output)) for p in output.rglob('*') if p.is_file()}
                self.assertEqual(actual, expected)
                for ref in manifest['files']:
                    self.assertEqual(hashlib.sha256((output/ref['path']).read_bytes()).hexdigest(), ref['sha256'])
                for artifact in project['artifacts']:
                    self.assertEqual((output/'artifacts'/artifact['path']).read_text(), artifact['text'])
                self.assertNotIn('expected_assessment', json.dumps(manifest))

    def test_existing_output_is_unchanged(self):
        self.output.mkdir()
        marker = self.output/'precious.txt'
        marker.write_text('unchanged')
        with self.assertRaisesRegex(ValueError, 'must be new'):
            mp.export_project('M214', self.output, self.root)
        self.assertEqual(marker.read_text(), 'unchanged')
        self.assertEqual(list(self.output.iterdir()), [marker])

    def test_dangling_symlink_output_rejected(self):
        self.output.symlink_to(self.base/'missing')
        with self.assertRaises(ValueError):
            mp.export_project('M214', self.output, self.root)
        self.assertTrue(self.output.is_symlink())

    def test_missing_output_parent(self):
        with self.assertRaises(ValueError):
            mp.export_project('M214', self.base/'absent'/'child', self.root)

    def test_unknown_project_no_mutation(self):
        with self.assertRaisesRegex(ValueError, 'unknown project'):
            mp.export_project('M000', self.output, self.root)
        self.assertFalse(self.output.exists())

    def test_invalid_source_precedes_output_creation(self):
        self.edit('projects.json', lambda d: d['projects'][0].update(expected_assessment='must not leak'))
        with self.assertRaisesRegex(ValueError, 'learner project'):
            mp.export_project('M214', self.output, self.root)
        self.assertFalse(self.output.exists())

    def test_boolean_schema_rejected(self):
        self.edit('projects.json', lambda d: d.update(schema_version=True))
        with self.assertRaisesRegex(ValueError, 'integer 1'):
            mp.load_data(self.root)

    def test_cross_suite_key_rejected(self):
        self.edit('instructor.json', lambda d: d.update(suite_id='other'))
        with self.assertRaisesRegex(ValueError, 'suite_id'):
            mp.load_data(self.root)

    def test_duplicate_project_rejected(self):
        self.edit('projects.json', lambda d: d['projects'].append(d['projects'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate project'):
            mp.load_data(self.root)

    def test_unknown_platform_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0].update(platform='any'))
        with self.assertRaisesRegex(ValueError, 'platform'):
            mp.load_data(self.root)

    def test_nonstring_platform_rejected_cleanly(self):
        for value in ([], {}, None, True):
            self.edit('projects.json', lambda d: d['projects'][0].update(platform=value))
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'platform'):
                mp.load_data(self.root)

    def test_nonportable_paths_rejected(self):
        for value in ('con.txt', 'NUL.md', 'COM1/file.txt', 'name./file.txt'):
            with self.subTest(path=value), self.assertRaisesRegex(ValueError, 'nonportable'):
                mp.relative_path(value)

    def test_case_insensitive_prefix_collision_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0]['artifacts'].append({'path':'PRODUCT.md/child.txt','text':'different'}))
        with self.assertRaisesRegex(ValueError, 'collision'):
            mp.load_data(self.root)

    def test_task_file_is_written_as_exact_utf8_bytes(self):
        original = Path.write_text
        def checked(path, data, *args, **kwargs):
            if path.name == 'TASK.md':
                raise AssertionError('text newline translation would invalidate the hash')
            return original(path, data, *args, **kwargs)
        with patch.object(Path, 'write_text', checked):
            mp.export_project('M214', self.output, self.root)
        manifest = json.loads((self.output/'manifest.json').read_text())
        ref = next(row for row in manifest['files'] if row['path'] == 'TASK.md')
        self.assertEqual(ref['sha256'], hashlib.sha256((self.output/'TASK.md').read_bytes()).hexdigest())

    def test_empty_project_artifacts_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0].update(artifacts=[]))
        with self.assertRaisesRegex(ValueError, 'multi-file'):
            mp.load_data(self.root)

    def test_artifact_answer_field_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0]['artifacts'][0].update(answer='wrong'))
        with self.assertRaisesRegex(ValueError, 'learner artifact'):
            mp.load_data(self.root)

    def test_duplicate_artifact_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0]['artifacts'].append(d['projects'][0]['artifacts'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            mp.load_data(self.root)

    def test_case_ambiguous_artifact_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0]['artifacts'].append({'path':'PRODUCT.md','text':'different'}))
        with self.assertRaisesRegex(ValueError, 'case-ambiguous'):
            mp.load_data(self.root)

    def test_unsafe_paths_rejected(self):
        for value in ('../x.md', '/x.md', 'C:/x.md', 'a\\x.md', 'a//x.md', 'a/./x.md', 'x.py', 'a\nx.md'):
            with self.subTest(path=value), self.assertRaises(ValueError):
                mp.relative_path(value)

    def test_empty_artifact_text_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0]['artifacts'][0].update(text='  '))
        with self.assertRaisesRegex(ValueError, 'nonempty'):
            mp.load_data(self.root)

    def test_large_artifact_rejected(self):
        self.edit('projects.json', lambda d: d['projects'][0]['artifacts'][0].update(text='x'*30001))
        with self.assertRaisesRegex(ValueError, 'limits'):
            mp.load_data(self.root)

    def test_missing_instructor_rejected(self):
        self.edit('instructor.json', lambda d: d['projects'].pop())
        with self.assertRaisesRegex(ValueError, 'every project'):
            mp.load_data(self.root)

    def test_duplicate_instructor_rejected(self):
        self.edit('instructor.json', lambda d: d['projects'].append(d['projects'][0]))
        with self.assertRaisesRegex(ValueError, 'instructor id'):
            mp.load_data(self.root)

    def test_unknown_instructor_reference_rejected(self):
        self.edit('instructor.json', lambda d: d['projects'][0]['required_artifacts'].append('missing.txt'))
        with self.assertRaisesRegex(ValueError, 'artifact reference'):
            mp.load_data(self.root)

    def test_duplicate_json_keys_rejected(self):
        path = self.base/'bad.json'
        path.write_text('{"a":1,"a":2}')
        with self.assertRaisesRegex(ValueError, 'duplicate JSON'):
            mp.read_json(path)

    def test_nonfinite_json_rejected(self):
        path = self.base/'bad.json'
        path.write_text('{"a":NaN}')
        with self.assertRaisesRegex(ValueError, 'non-finite'):
            mp.read_json(path)

    def test_json_root_must_be_object(self):
        path = self.base/'bad.json'
        path.write_text('[]')
        with self.assertRaisesRegex(ValueError, 'root'):
            mp.read_json(path)

    def test_json_size_bound(self):
        path = self.base/'large.json'
        path.write_bytes(b' '*(mp.MAX_JSON_BYTES+1))
        with self.assertRaisesRegex(ValueError, 'limits'):
            mp.read_json(path)

    def test_broken_link_detected(self):
        path = self.root/'references'/'new.md'
        path.write_text('[bad](missing.md)')
        with self.assertRaisesRegex(ValueError, 'local reference'):
            mp.validate_package(self.root)

    def test_escape_link_detected(self):
        (self.root/'references'/'new.md').write_text('[bad](../../outside.md)')
        with self.assertRaisesRegex(ValueError, 'local reference'):
            mp.validate_package(self.root)

    def test_core_budget_enforced(self):
        path = self.root/'SKILL.md'
        path.write_text(path.read_text()+'\n'*221)
        with self.assertRaisesRegex(ValueError, '220-line'):
            mp.validate_package(self.root)

    def test_export_failure_removes_only_created_directory(self):
        with patch.object(Path, 'write_bytes', side_effect=OSError('synthetic write failure')):
            with self.assertRaisesRegex(OSError, 'synthetic'):
                mp.export_project('M214', self.output, self.root)
        self.assertFalse(self.output.exists())
        self.assertTrue(self.root.exists())

    def test_cli_validation(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(mp.main(['validate']), 0)
        self.assertEqual(json.loads(out.getvalue())['projects'], 8)

    def test_cli_listing_excludes_instructor_answers(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(mp.main(['list']), 0)
        self.assertEqual(set(json.loads(out.getvalue())['projects'][0]), {'id','title','platform'})

    def test_cli_export(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(mp.main(['export','--project','M214','--output',str(self.output)]), 0)
        self.assertFalse(json.loads(out.getvalue())['instructor_exported'])

    def test_cli_failure_has_no_success_output(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = mp.main(['export','--project','M000','--output',str(self.output)])
        self.assertEqual(result, 2)
        self.assertEqual(out.getvalue(), '')
        self.assertIn('unknown project', err.getvalue())


if __name__ == '__main__':
    unittest.main()
