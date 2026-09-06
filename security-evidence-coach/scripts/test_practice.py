#!/usr/bin/env python3
"""Tests of the offline tools, not a model capability evaluation."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import practice as p


def oracle_answers(suite: dict, key: dict) -> dict:
    """Known answers used only to check scoring arithmetic and validation."""
    by_id = {row["id"]: row for row in key["cases"]}
    return {
        "schema_version": 1, "suite_id": suite["suite_id"],
        "run": {"run_id": "unit-test-only", "model": "no-model-invoked",
                "condition": "software-oracle", "tool_access": "none",
                "budget": "not-applicable", "trial": 1},
        "answers": [{"case_id": c["id"], "verdict": by_id[c["id"]]["verdict"],
                     "evidence_ids": by_id[c["id"]]["required_evidence"].copy(),
                     "rationale": "Software fixture; no model reasoning was performed.",
                     "limitation": "Only this fictional proposition is assessed."}
                    for c in suite["cases"]],
    }


class PracticeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.suite, self.key = p.load_suite()
        self.answers = oracle_answers(self.suite, self.key)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.tmp = Path(self.temp.name)

    def score(self) -> dict:
        return p.score_answers(self.answers, self.suite, self.key)

    def test_package_validates_with_balanced_public_cases(self) -> None:
        result = p.validate_package()
        self.assertEqual(result["cases"], 24)
        self.assertEqual(result["families"], 12)
        self.assertEqual(set(result["verdict_counts"].values()), {8})
        self.assertFalse(result["model_evaluation_performed"])

    def test_software_oracle_scores_expected_arithmetic(self) -> None:
        result = self.score()
        self.assertEqual(result["label_accuracy"], 1.0)
        self.assertEqual(result["label_and_evidence_id_accuracy"], 1.0)
        self.assertTrue(result["human_review_required"])

    def test_blanket_inconclusive_is_not_perfect(self) -> None:
        for row in self.answers["answers"]:
            row["verdict"] = "INCONCLUSIVE"
        result = self.score()
        self.assertAlmostEqual(result["label_accuracy"], 1 / 3)
        self.assertAlmostEqual(result["macro_recall"], 1 / 3)
        self.assertEqual(result["inconclusive_rate"], 1)
        self.assertIsNone(result["precision_by_verdict"]["SUPPORTED"])

    def test_blanket_supported_is_not_perfect(self) -> None:
        for row in self.answers["answers"]:
            row["verdict"] = "SUPPORTED"
        self.assertAlmostEqual(self.score()["macro_recall"], 1 / 3)

    def test_missing_citations_reduce_only_evidence_proxy(self) -> None:
        self.answers["answers"][0]["evidence_ids"] = []
        result = self.score()
        self.assertEqual(result["label_accuracy"], 1)
        self.assertAlmostEqual(result["decisive_evidence_id_coverage"], 23 / 24)
        self.assertAlmostEqual(result["label_and_evidence_id_accuracy"], 23 / 24)

    def test_citation_dumping_does_not_remove_human_review(self) -> None:
        for row, case in zip(self.answers["answers"], self.suite["cases"]):
            row["evidence_ids"] = [e["id"] for e in case["evidence"]]
        result = self.score()
        self.assertEqual(result["decisive_evidence_id_coverage"], 1)
        self.assertTrue(result["human_review_required"])
        self.assertTrue(any("dumping" in text for text in result["limitations"]))

    def test_missing_answer_cannot_shrink_denominator(self) -> None:
        self.answers["answers"].pop()
        with self.assertRaisesRegex(ValueError, "every case"):
            self.score()

    def test_duplicate_answer_rejected(self) -> None:
        self.answers["answers"].append(self.answers["answers"][0])
        with self.assertRaisesRegex(ValueError, "duplicate answer"):
            self.score()

    def test_unknown_case_rejected(self) -> None:
        self.answers["answers"][0]["case_id"] = "Unknown"
        with self.assertRaisesRegex(ValueError, "unknown answer"):
            self.score()

    def test_unknown_citation_rejected(self) -> None:
        self.answers["answers"][0]["evidence_ids"] = ["E999"]
        with self.assertRaisesRegex(ValueError, "unknown cited"):
            self.score()

    def test_duplicate_citation_rejected(self) -> None:
        self.answers["answers"][0]["evidence_ids"] = ["E1", "E1"]
        with self.assertRaisesRegex(ValueError, "duplicate identifiers"):
            self.score()

    def test_invalid_verdict_shape_is_clean_error(self) -> None:
        self.answers["answers"][0]["verdict"] = {"not": "a string"}
        with self.assertRaisesRegex(ValueError, "non-empty string"):
            self.score()

    def test_empty_rationale_rejected(self) -> None:
        self.answers["answers"][0]["rationale"] = " "
        with self.assertRaisesRegex(ValueError, "rationale"):
            self.score()

    def test_empty_limitation_rejected(self) -> None:
        self.answers["answers"][0]["limitation"] = ""
        with self.assertRaisesRegex(ValueError, "limitation"):
            self.score()

    def test_missing_metadata_rejected(self) -> None:
        del self.answers["run"]["model"]
        with self.assertRaisesRegex(ValueError, "run.model"):
            self.score()

    def test_boolean_is_not_trial_integer(self) -> None:
        self.answers["run"]["trial"] = True
        with self.assertRaisesRegex(ValueError, "positive integer"):
            self.score()

    def test_wrong_suite_rejected(self) -> None:
        self.answers["suite_id"] = "different"
        with self.assertRaisesRegex(ValueError, "suite_id"):
            self.score()

    def test_duplicate_json_keys_rejected(self) -> None:
        path = self.tmp / "bad.json"
        path.write_text('{"x":1,"x":2}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            p.load_json(path)

    def test_non_finite_json_rejected(self) -> None:
        path = self.tmp / "bad.json"
        path.write_text('{"x":NaN}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "non-finite"):
            p.load_json(path)

    def test_invalid_utf8_rejected(self) -> None:
        path = self.tmp / "bad.json"
        path.write_bytes(b'\xff')
        with self.assertRaisesRegex(ValueError, "cannot read"):
            p.load_json(path)

    def test_array_root_rejected(self) -> None:
        path = self.tmp / "bad.json"
        path.write_text('[]', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "root must be"):
            p.load_json(path)

    def test_answer_key_coverage_checked(self) -> None:
        self.key["cases"].pop()
        with self.assertRaisesRegex(ValueError, "every case"):
            p.validate_data(self.suite, self.key)

    def test_unknown_key_evidence_rejected(self) -> None:
        self.key["cases"][0]["required_evidence"] = ["E999"]
        with self.assertRaisesRegex(ValueError, "unknown required"):
            p.validate_data(self.suite, self.key)

    def test_duplicate_case_id_rejected(self) -> None:
        self.suite["cases"].append(copy.deepcopy(self.suite["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate case"):
            p.validate_data(self.suite, self.key)

    def test_case_id_cannot_escape_export_directory(self) -> None:
        self.suite["cases"][0]["id"] = "../outside"
        with self.assertRaisesRegex(ValueError, "safe identifier"):
            p.validate_data(self.suite, self.key)

    def test_learner_schema_rejects_answer_leak(self) -> None:
        self.suite["cases"][0]["verdict"] = "SUPPORTED"
        with self.assertRaisesRegex(ValueError, "fields must be"):
            p.validate_data(self.suite, self.key)

    def test_export_has_no_answer_key_or_outcome_labels(self) -> None:
        out = self.tmp / "learner"
        p.export_packets(out)
        self.assertFalse((out / "answer-key.json").exists())
        packets = list((out / "cases").glob("*.json"))
        self.assertEqual(len(packets), 24)
        for path in packets:
            obj = p.load_json(path)
            self.assertEqual(set(obj), {"id", "question", "context", "evidence"})
        blank = p.load_json(out / "answers.template.json")
        self.assertTrue(all(row["verdict"] == "" for row in blank["answers"]))
        self.assertEqual(len(p.load_json(out / "manifest.json")["files"]), 24)

    def test_export_refuses_existing_directory_unchanged(self) -> None:
        out = self.tmp / "learner"
        out.mkdir()
        sentinel = out / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            p.export_packets(out)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertEqual(list(out.iterdir()), [sentinel])

    def test_export_refuses_existing_file(self) -> None:
        out = self.tmp / "learner"
        out.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            p.export_packets(out)
        self.assertEqual(out.read_text(encoding="utf-8"), "keep")

    def test_export_refuses_dangling_symlink(self) -> None:
        out = self.tmp / "learner"
        out.symlink_to(self.tmp / "missing")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            p.export_packets(out)
        self.assertTrue(out.is_symlink())

    def test_export_io_failure_cleans_only_new_output(self) -> None:
        out = self.tmp / "learner"
        keep = self.tmp / "keep.txt"
        keep.write_text("keep", encoding="utf-8")
        with patch.object(p, "_write_json", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(OSError, "disk full"):
                p.export_packets(out)
        self.assertFalse(out.exists())
        self.assertEqual(keep.read_text(encoding="utf-8"), "keep")

    def test_cli_success_and_fail_closed_errors(self) -> None:
        script = Path(p.__file__)
        valid = subprocess.run([sys.executable, script, "validate"], text=True,
                               capture_output=True, check=False)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(json.loads(valid.stdout)["cases"], 24)
        bad = self.tmp / "bad.json"
        bad.write_text('[]', encoding="utf-8")
        failed = subprocess.run([sys.executable, script, "score", "--answers", bad],
                                text=True, capture_output=True, check=False)
        self.assertEqual(failed.returncode, 2)
        self.assertIn("ERROR:", failed.stderr)
        self.assertNotIn("Traceback", failed.stderr)
        self.assertEqual(failed.stdout, "")

    def test_cli_scores_oracle_without_claiming_model_execution(self) -> None:
        path = self.tmp / "answers.json"
        path.write_text(json.dumps(self.answers), encoding="utf-8")
        result = subprocess.run([sys.executable, Path(p.__file__), "score", "--answers", path],
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        scored = json.loads(result.stdout)
        self.assertTrue(scored["human_review_required"])
        self.assertEqual(scored["run"]["model"], "no-model-invoked")


if __name__ == "__main__":
    unittest.main(verbosity=2)
