"""Regression tests for source provenance, local references and offline validation."""
from __future__ import annotations

import copy
from datetime import date
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from validate_research import ROOT, load_index, validate_index

TODAY = date(2026, 9, 10)


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.data = load_index(ROOT / 'references' / 'source-index.json')

    def validate(self, data=None, **kwargs):
        return validate_index(self.data if data is None else data, as_of=TODAY, **kwargs)

    def reject(self, fragment):
        with self.assertRaisesRegex(ValueError, fragment):
            self.validate()

    def test_real_registry(self):
        result = self.validate()
        self.assertEqual(result['sources'], 22)
        self.assertEqual(result['status_counts'], {'report_cited': 17, 'limited_content': 3, 'lead_only': 2})
        self.assertFalse(result['source_truth_verified'])
        self.assertFalse(result['external_retrieval_performed'])
        self.assertFalse(result['model_evaluation_performed'])

    def test_missing_top_field(self):
        del self.data['provenance']; self.reject('fields')

    def test_unknown_top_field(self):
        self.data['verified'] = True; self.reject('fields')

    def test_version_bool(self):
        self.data['schema_version'] = True; self.reject('integer 1')

    def test_independent_retrieval_not_fabricated(self):
        self.data['independently_retrieved_in_integration'] = True
        self.reject('cannot claim independent')

    def test_provenance_not_relabelled(self):
        self.data['provenance'] = 'live_verified'; self.reject('completed research')

    def test_research_date_not_reset(self):
        self.data['research_as_of'] = '2026-09-11'; self.reject('dates')

    def test_future_integration(self):
        self.data['integrated_on'] = '2026-09-12'; self.reject('dates')

    def test_local_calendar_date_may_lead_utc(self):
        result = validate_index(self.data, as_of=date(2026, 9, 9))
        self.assertTrue(result['metadata_valid'])

    def test_out_of_order_dates(self):
        self.data['integrated_on'] = '2026-09-08'; self.reject('dates')

    def test_date_format(self):
        self.data['research_as_of'] = '20260909'; self.reject('YYYY-MM-DD')

    def test_impossible_date(self):
        self.data['research_as_of'] = '2026-02-30'; self.reject('day')

    def test_old_snapshot_warns_without_claiming_falsity(self):
        result = validate_index(self.data, as_of=date(2027, 9, 10))
        self.assertTrue(result['metadata_valid'])
        self.assertEqual(len(result['warnings']), 1)
        self.assertFalse(result['source_truth_verified'])

    def test_empty_sources(self):
        self.data['sources'] = []; self.reject('nonempty array')

    def test_sources_wrong_shape(self):
        self.data['sources'] = {}; self.reject('nonempty array')

    def test_unknown_status(self):
        self.data['sources'][0]['status'] = 'verified'; self.reject('status')

    def test_status_wrong_type(self):
        self.data['sources'][0]['status'] = []; self.reject('status')

    def test_unknown_type(self):
        self.data['sources'][0]['source_type'] = 'anonymous'; self.reject('type')

    def test_duplicate_id(self):
        self.data['sources'][1]['id'] = self.data['sources'][0]['id']; self.reject('duplicate source id')

    def test_duplicate_url(self):
        self.data['sources'][1]['url'] = self.data['sources'][0]['url']; self.reject('duplicate source URL')

    def test_non_https_url(self):
        self.data['sources'][0]['url'] = 'file:///etc/passwd'; self.reject('HTTPS')

    def test_url_credentials(self):
        self.data['sources'][0]['url'] = 'https://user:secret@example.org'; self.reject('credential-free')

    def test_url_whitespace(self):
        self.data['sources'][0]['url'] = 'https://example.org/\n'; self.reject('HTTPS')

    def test_empty_applicability(self):
        self.data['sources'][0]['applicability'] = ''; self.reject('applicability')

    def test_empty_revision(self):
        self.data['sources'][0]['upstream_revision'] = ''; self.reject('upstream_revision')

    def test_extra_row_fields(self):
        self.data['sources'][0]['verified_by_model'] = True; self.reject('source row')

    def test_missing_local_reference(self):
        self.data['sources'][0]['used_by'] = ['references/missing.md']; self.reject('missing')

    def test_parent_path(self):
        self.data['sources'][0]['used_by'] = ['../outside.md']; self.reject('relative Markdown')

    def test_absolute_path(self):
        self.data['sources'][0]['used_by'] = ['/tmp/outside.md']; self.reject('relative Markdown')

    def test_duplicate_reference(self):
        self.data['sources'][0]['used_by'] *= 2; self.reject('unique')

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory) / 'outside.md'; outside.write_text('unrelated')
            link = ROOT / 'references' / 'temp-research-link.md'
            try:
                link.symlink_to(outside)
                self.data['sources'][0]['used_by'] = ['references/temp-research-link.md']
                self.reject('escapes')
            finally:
                link.unlink(missing_ok=True)

    def test_no_network_needed(self):
        with patch('socket.socket', side_effect=AssertionError('network is not permitted')):
            self.assertTrue(self.validate()['metadata_valid'])

    def test_loader_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'index.json'; p.write_text('{"x":1,"x":2}')
            with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
                load_index(p)

    def test_loader_nonfinite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'index.json'; p.write_text('{"x":NaN}')
            with self.assertRaisesRegex(ValueError, 'non-finite'):
                load_index(p)

    def test_loader_size_bound(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'index.json'; p.write_bytes(b' '*(1024*1024+1))
            with self.assertRaisesRegex(ValueError, 'size limit'):
                load_index(p)

    def test_loader_nonobject(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'index.json'; p.write_text('[]')
            with self.assertRaisesRegex(ValueError, 'object'):
                load_index(p)

    def test_core_budget_and_direct_references(self):
        core=(ROOT/'SKILL.md').read_text()
        self.assertLessEqual(len(core.splitlines()), 220)
        for name in ('research-integration.md', 'assessment-design.md', 'source-index.json'):
            self.assertIn(f'(references/{name})', core)
        self.assertIn('(evals/research-transfer.md)', core)

    def test_cli_valid(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate_research.py'),
                                 '--as-of', '2026-09-10'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)['source_truth_verified'])

    def test_cli_invalid(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate_research.py'),
                                 '--as-of', 'not-a-date'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
