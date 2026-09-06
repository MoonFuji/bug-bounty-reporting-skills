"""Regression checks for public advanced practice, not measurements of a model."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

import practice as p
from test_practice import oracle_answers


class AdvancedPracticeTests(unittest.TestCase):
    def setUp(self):
        self.suite, self.key = p.load_suite(suite_name='advanced')
        self.answers = oracle_answers(self.suite, self.key)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.tmp = Path(self.temp.name)

    def score(self):
        return p.score_answers(self.answers, self.suite, self.key)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(Path(p.__file__)), *map(str, args)],
                              capture_output=True, text=True, check=False)

    def test_original_suite_identity_and_bytes_preserved(self):
        old, _ = p.load_suite()
        self.assertEqual(old['suite_id'], 'security-evidence-practice-v1')
        # These are original Git blob identifiers, not hashes of generated data.
        for name, expected in [('cases.json', '6db0bde8a862052afd7e4fef9e6cc7ecec7aac79'),
                               ('answer-key.json', '3777629d196ff4971d6c070c7de9a5a8a7ab71c1')]:
            data = (p.ROOT / 'evals' / name).read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            self.assertEqual(actual, expected)

    def test_advanced_package_is_balanced_and_distinct(self):
        result = p.validate_package(suite_name='advanced')
        self.assertEqual(result['suite_id'], 'security-evidence-advanced-v1')
        self.assertEqual(result['cases'], 24)
        self.assertEqual(result['families'], 8)
        self.assertEqual(result['verdict_counts'], {v: 8 for v in p.VERDICTS})
        self.assertFalse(result['model_evaluation_performed'])
        original, _ = p.load_suite()
        self.assertTrue({c['id'] for c in original['cases']}.isdisjoint(c['id'] for c in self.suite['cases']))

    def test_each_family_has_one_of_each_verdict(self):
        for family in {c['family'] for c in self.key['cases']}:
            counts = Counter(c['verdict'] for c in self.key['cases'] if c['family'] == family)
            self.assertEqual(counts, {v: 1 for v in p.VERDICTS})

    def test_packets_require_multiple_distinct_artifact_roles(self):
        by_id = {c['id']: c for c in self.suite['cases']}
        for answer in self.key['cases']:
            case = by_id[answer['id']]
            self.assertGreaterEqual(len(case['evidence']), 4)
            self.assertGreaterEqual(len(answer['required_evidence']), 2)
            self.assertEqual(len({e['locator'] for e in case['evidence']}), len(case['evidence']))

    def test_oracle_only_checks_score_arithmetic(self):
        result = self.score()
        self.assertEqual(result['label_accuracy'], 1)
        self.assertEqual(result['cases_scored'], 24)
        self.assertTrue(result['human_review_required'])
        self.assertEqual(len(result['family_summary']), 8)
        self.assertTrue(all(row['cases'] == 3 and row['label_accuracy'] == 1
                            for row in result['family_summary'].values()))

    def test_family_failure_not_hidden_by_aggregate(self):
        key = {c['id']: c for c in self.key['cases']}
        for row in self.answers['answers']:
            if key[row['case_id']]['family'] == 'repair-evidence':
                verdict = row['verdict']
                row['verdict'] = p.VERDICTS[(p.VERDICTS.index(verdict) + 1) % 3]
        result = self.score()
        self.assertEqual(result['family_summary']['repair-evidence']['label_accuracy'], 0)
        self.assertEqual(result['label_accuracy'], 21 / 24)
        self.assertTrue(all(row['label_accuracy'] == 1 for family, row in result['family_summary'].items()
                            if family != 'repair-evidence'))

    def test_all_inconclusive_remains_one_third(self):
        for row in self.answers['answers']:
            row['verdict'] = 'INCONCLUSIVE'
        result = self.score()
        self.assertAlmostEqual(result['label_accuracy'], 1 / 3)
        self.assertAlmostEqual(result['macro_recall'], 1 / 3)
        self.assertTrue(all(row['label_accuracy'] == 1 / 3 for row in result['family_summary'].values()))

    def test_decisive_citation_omission_visible_in_family(self):
        row = self.answers['answers'][0]
        family = next(k['family'] for k in self.key['cases'] if k['id'] == row['case_id'])
        row['evidence_ids'] = []
        result = self.score()
        self.assertEqual(result['label_accuracy'], 1)
        self.assertEqual(result['family_summary'][family]['decisive_evidence_id_coverage'], 2 / 3)
        self.assertTrue(result['human_review_required'])

    def test_cross_suite_answer_files_rejected(self):
        old, key = p.load_suite()
        with self.assertRaisesRegex(ValueError, 'suite_id'):
            p.score_answers(oracle_answers(old, key), self.suite, self.key)
        with self.assertRaisesRegex(ValueError, 'suite_id'):
            p.score_answers(self.answers, old, key)

    def test_omitted_advanced_answer_rejected(self):
        self.answers['answers'].pop()
        with self.assertRaisesRegex(ValueError, 'every case'):
            self.score()

    def test_unknown_suite_cannot_be_used_as_path(self):
        for suite in ('../elsewhere', '/tmp', 'unknown', None, ['advanced']):
            with self.subTest(suite=suite), self.assertRaisesRegex(ValueError, 'suite_name'):
                p.load_suite(suite_name=suite)

    def test_export_has_distinct_suite_and_no_evaluator_metadata(self):
        output = self.tmp / 'advanced'
        p.export_packets(output, suite_name='advanced')
        manifest = p.load_json(output / 'manifest.json')
        self.assertEqual(manifest['suite_id'], self.suite['suite_id'])
        blank = p.load_json(output / 'answers.template.json')
        self.assertEqual(blank['suite_id'], self.suite['suite_id'])
        self.assertTrue(all(row['verdict'] == '' for row in blank['answers']))
        self.assertEqual(len(manifest['files']), 24)
        for ref in manifest['files']:
            file = output / ref['path']
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), ref['sha256'])
            packet = p.load_json(file)
            self.assertEqual(set(packet), {'id', 'question', 'context', 'evidence'})
        self.assertFalse(any('answer-key' in x.name for x in output.rglob('*')))

    def test_advanced_export_refuses_existing_output(self):
        output = self.tmp / 'advanced'
        output.mkdir()
        sentinel = output / 'keep.txt'
        sentinel.write_text('keep')
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            p.export_packets(output, suite_name='advanced')
        self.assertEqual(sentinel.read_text(), 'keep')

    def test_invalid_suite_does_not_create_output(self):
        output = self.tmp / 'invalid'
        with self.assertRaises(ValueError):
            p.export_packets(output, suite_name='invalid')
        self.assertFalse(output.exists())

    def test_export_failure_preserves_unrelated_files(self):
        output = self.tmp / 'advanced'
        sentinel = self.tmp / 'keep.txt'
        sentinel.write_text('keep')
        with patch.object(p, '_write_json', side_effect=OSError('no storage')):
            with self.assertRaises(OSError):
                p.export_packets(output, suite_name='advanced')
        self.assertFalse(output.exists())
        self.assertEqual(sentinel.read_text(), 'keep')

    def test_answer_leak_field_is_rejected(self):
        for field in ('verdict', 'family', 'rationale', 'critical_errors'):
            suite = copy.deepcopy(self.suite)
            suite['cases'][0][field] = 'unwanted evaluator data'
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'fields must be'):
                p.validate_data(suite, self.key)

    def test_cli_validate_selects_advanced(self):
        result = self.cli('validate', '--suite', 'advanced')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['families'], 8)

    def test_cli_export_and_score_advanced(self):
        out = self.tmp / 'packet'
        result = self.cli('export', '--suite', 'advanced', '--output', out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)['answer_key_exported'])
        answers = self.tmp / 'answers.json'
        answers.write_text(json.dumps(self.answers))
        score = self.cli('score', '--suite', 'advanced', '--answers', answers)
        self.assertEqual(score.returncode, 0, score.stderr)
        data = json.loads(score.stdout)
        self.assertEqual(data['run']['model'], 'no-model-invoked')
        self.assertEqual(data['label_accuracy'], 1)
        self.assertTrue(data['human_review_required'])

    def test_cli_default_refuses_advanced_answers(self):
        answers = self.tmp / 'answers.json'
        answers.write_text(json.dumps(self.answers))
        result = self.cli('score', '--answers', answers)
        self.assertEqual(result.returncode, 2)
        self.assertIn('suite_id', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_cli_bad_suite_is_usage_error(self):
        result = self.cli('validate', '--suite', '../advanced')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
