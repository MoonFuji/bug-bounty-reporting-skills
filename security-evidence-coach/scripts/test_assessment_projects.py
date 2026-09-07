#!/usr/bin/env python3
"""Offline regressions for project integrity, exports, and finite teaching contracts."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import assessment_projects as ap


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "skill"
        shutil.copytree(ap.ROOT / "projects", self.root / "projects")
        shutil.copytree(ap.ROOT / "evals/projects", self.root / "evals/projects")

    def change(self, relative, change):
        path = self.root / relative
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data) + "\n")

    def manifest(self, change):
        self.change("projects/P101/project.json", change)

    def test_all_projects_validate(self):
        result = ap.validate_package(self.root)
        self.assertEqual(result["projects"], 4)
        self.assertEqual(result["learner_artifacts"], 19)
        self.assertFalse(result["model_evaluation_performed"])
        self.assertTrue(result["human_grading_required"])

    def test_foundation_and_advanced_are_not_project_inputs(self):
        loaded = ap.load_projects(self.root)
        self.assertEqual(set(loaded), {"P101", "P202", "P303", "P404"})
        self.assertFalse((self.root / "evals/cases.json").exists())

    def test_boolean_version_rejected(self):
        self.manifest(lambda d: d.update(schema_version=True))
        with self.assertRaisesRegex(ValueError, "integer 1"):
            ap.load_projects(self.root)

    def test_duplicate_json_keys_rejected(self):
        (self.root / "projects/index.json").write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            ap.load_projects(self.root)

    def test_nonfinite_json_rejected(self):
        (self.root / "projects/index.json").write_text('{"score":NaN}')
        with self.assertRaisesRegex(ValueError, "non-finite"):
            ap.load_projects(self.root)

    def test_nonobject_json_rejected(self):
        (self.root / "projects/index.json").write_text('[]')
        with self.assertRaisesRegex(ValueError, "object root"):
            ap.load_projects(self.root)

    def test_duplicate_project_id_rejected(self):
        self.change("projects/index.json", lambda d: d["projects"].append(d["projects"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            ap.load_projects(self.root)

    def test_index_cannot_carry_answer_metadata(self):
        self.change("projects/index.json", lambda d: d.update(expected="safe"))
        with self.assertRaisesRegex(ValueError, "expected exactly"):
            ap.load_projects(self.root)

    def test_manifest_cannot_carry_answer_metadata(self):
        self.manifest(lambda d: d.update(verdict="SUPPORTED"))
        with self.assertRaisesRegex(ValueError, "expected exactly"):
            ap.load_projects(self.root)

    def test_index_directory_must_match_id(self):
        self.change("projects/index.json", lambda d: d["projects"][0].update(directory="../evals"))
        with self.assertRaisesRegex(ValueError, "mismatched"):
            ap.load_projects(self.root)

    def test_manifest_id_must_match_directory(self):
        self.manifest(lambda d: d.update(project_id="P999"))
        with self.assertRaisesRegex(ValueError, "project_id mismatch"):
            ap.load_projects(self.root)

    def test_empty_title_rejected(self):
        self.manifest(lambda d: d.update(title=" "))
        with self.assertRaisesRegex(ValueError, "non-empty text"):
            ap.load_projects(self.root)

    def test_duplicate_artifact_rejected(self):
        self.manifest(lambda d: d["files"].append(d["files"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate project file"):
            ap.load_projects(self.root)

    def test_unsafe_artifact_paths_rejected(self):
        for name in ("../instructor.json", "/tmp/a.py", "a//b.py", "./a.py", "x\\y.py", "C:a.py"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "unsafe relative"):
                    ap._relative(name)

    def test_unsupported_extension_rejected(self):
        self.manifest(lambda d: d["files"].append("binary.so"))
        with self.assertRaisesRegex(ValueError, "invalid, reserved"):
            ap.load_projects(self.root)

    def test_reserved_output_name_rejected(self):
        self.manifest(lambda d: d["files"].append("BRIEF.md"))
        with self.assertRaisesRegex(ValueError, "reserved"):
            ap.load_projects(self.root)

    def test_missing_artifact_rejected_before_export(self):
        (self.root / "projects/P101/product.md").unlink()
        out = self.base / "export"
        with self.assertRaisesRegex(ValueError, "cannot read"):
            ap.export_project("P101", out, self.root)
        self.assertFalse(out.exists())

    def test_symlink_file_rejected(self):
        file = self.root / "projects/P101/product.md"
        file.unlink()
        file.symlink_to(self.root / "projects/P202/product.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            ap.load_projects(self.root)

    def test_symlink_project_directory_rejected(self):
        shutil.rmtree(self.root / "projects/P101")
        (self.root / "projects/P101").symlink_to(self.root / "projects/P202", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            ap.load_projects(self.root)

    def test_directory_instead_of_file_rejected(self):
        file = self.root / "projects/P101/product.md"
        file.unlink()
        file.mkdir()
        with self.assertRaisesRegex(ValueError, "regular file"):
            ap.load_projects(self.root)

    def test_oversized_file_rejected(self):
        (self.root / "projects/P101/product.md").write_bytes(b"x" * (ap.MAX_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "bounded regular"):
            ap.load_projects(self.root)

    def test_invalid_utf8_rejected(self):
        (self.root / "projects/P101/product.md").write_bytes(b"\xff")
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            ap.load_projects(self.root)

    def test_empty_artifact_rejected(self):
        (self.root / "projects/P101/product.md").write_text("\n")
        with self.assertRaisesRegex(ValueError, "empty project artifact"):
            ap.load_projects(self.root)

    def test_contract_and_source_are_required(self):
        self.manifest(lambda d: d.update(files=["assembly.json", "records.json"]))
        with self.assertRaisesRegex(ValueError, "product.md and a source"):
            ap.load_projects(self.root)

    def test_instructor_must_cover_every_project(self):
        self.change("evals/projects/instructor.json", lambda d: d["projects"].pop("P101"))
        with self.assertRaisesRegex(ValueError, "cover every"):
            ap.validate_package(self.root)

    def test_instructor_cannot_cite_missing_file(self):
        self.change("evals/projects/instructor.json", lambda d: d["projects"]["P101"]["relationships"][0].update(files=["product.md", "missing.py"]))
        with self.assertRaisesRegex(ValueError, "unavailable"):
            ap.validate_package(self.root)

    def test_relationships_need_multiple_distinct_artifacts(self):
        self.change("evals/projects/instructor.json", lambda d: d["projects"]["P101"]["relationships"][0].update(files=["product.md", "product.md"]))
        with self.assertRaisesRegex(ValueError, "distinct multiple"):
            ap.validate_package(self.root)

    def test_unknown_project_export_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown project"):
            ap.export_project("P999", self.base / "out", self.root)
        self.assertFalse((self.base / "out").exists())

    def test_export_excludes_instructor_and_unlisted_files(self):
        # Even a stray answer file in the project is not copied unless allowlisted.
        (self.root / "projects/P101/unlisted.txt").write_text("DO_NOT_EXPORT")
        out = self.base / "out"
        result = ap.export_project("P101", out, self.root)
        self.assertFalse(result["instructor_material_exported"])
        expected = {"BRIEF.md", "manifest.json"} | {"system/" + n for n in ap.load_projects(self.root)["P101"]["contents"]}
        actual = {str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()}
        self.assertEqual(actual, expected)
        self.assertNotIn("DO_NOT_EXPORT", "".join(p.read_text() for p in out.rglob("*") if p.is_file()))

    def test_export_does_not_need_or_read_instructor_answers(self):
        (self.root / "evals/projects/instructor.json").unlink()
        ap.export_project("P101", self.base / "out", self.root)
        self.assertTrue((self.base / "out/BRIEF.md").is_file())

    def test_all_exported_hashes_identify_the_copied_bytes(self):
        for pid in ap.load_projects(self.root):
            out = self.base / pid
            ap.export_project(pid, out, self.root)
            manifest = json.loads((out / "manifest.json").read_text())
            self.assertEqual(manifest["project_id"], pid)
            for ref in manifest["files"]:
                self.assertEqual(hashlib.sha256((out / ref["path"]).read_bytes()).hexdigest(), ref["sha256"])
            self.assertEqual((out / "BRIEF.md").read_text(), ap.BRIEF)

    def test_export_never_executes_source_text(self):
        marker = self.base / "executed"
        (self.root / "projects/P101/permissions.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n")
        ap.export_project("P101", self.base / "out", self.root)
        self.assertFalse(marker.exists())

    def test_export_refuses_existing_directory_unchanged(self):
        out = self.base / "out"
        out.mkdir()
        (out / "sentinel").write_text("keep")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            ap.export_project("P101", out, self.root)
        self.assertEqual((out / "sentinel").read_text(), "keep")
        self.assertEqual(len(list(out.iterdir())), 1)

    def test_export_refuses_existing_file_unchanged(self):
        out = self.base / "out"
        out.write_text("keep")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            ap.export_project("P101", out, self.root)
        self.assertEqual(out.read_text(), "keep")

    def test_export_refuses_dangling_symlink(self):
        out = self.base / "out"
        out.symlink_to(self.base / "missing")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            ap.export_project("P101", out, self.root)
        self.assertTrue(out.is_symlink())

    def test_export_requires_parent_without_creating_it(self):
        out = self.base / "missing/out"
        with self.assertRaisesRegex(ValueError, "parent"):
            ap.export_project("P101", out, self.root)
        self.assertFalse(out.parent.exists())

    def test_write_failure_removes_only_the_new_export(self):
        out = self.base / "out"
        sentinel = self.base / "sentinel"
        sentinel.write_text("keep")
        with patch.object(Path, "write_bytes", side_effect=OSError("disk unavailable")):
            with self.assertRaisesRegex(OSError, "disk unavailable"):
                ap.export_project("P101", out, self.root)
        self.assertFalse(out.exists())
        self.assertEqual(sentinel.read_text(), "keep")

    def test_cli_lists_no_expected_outcomes(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(ap.main(["list"]), 0)
        data = json.loads(output.getvalue())
        self.assertEqual(len(data["projects"]), 4)
        self.assertTrue(all(set(p) == {"id", "title"} for p in data["projects"]))

    def test_cli_export_and_invalid_id(self):
        script = Path(ap.__file__)
        out = self.base / "cli"
        valid = subprocess.run([sys.executable, str(script), "export", "--project", "P202", "--output", str(out)], capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        invalid = subprocess.run([sys.executable, str(script), "export", "--project", "P000", "--output", str(self.base / "bad")], capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("unknown project", invalid.stderr)
        self.assertFalse((self.base / "bad").exists())


class TeachingContractTests(unittest.TestCase):
    """Tests only selected, pure fictional reference components and finite records."""
    def module(self, pid, file):
        path = ap.ROOT / "projects" / pid / file
        spec = importlib.util.spec_from_file_location("fixture_" + pid + "_" + path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_atlas_grants_are_action_and_object_specific(self):
        p = self.module("P101", "permissions.py")
        data = json.loads((ap.ROOT / "projects/P101/records.json").read_text())
        record = data["records"][0]
        owner, reader, visitor = data["principals"]
        for action in ("READ", "EXPORT"):
            self.assertTrue(p.permitted(owner, action, record, []))
            self.assertTrue(p.permitted(reader, action, record, data["grants"]))
            self.assertFalse(p.permitted(visitor, action, record, data["grants"]))
        read_only = [{**data["grants"][0], "actions": ["READ"]}]
        self.assertFalse(p.permitted(reader, "EXPORT", record, read_only))
        self.assertFalse(p.permitted(reader, "READ", {**record, "record_id": "D2"}, data["grants"]))
        self.assertFalse(p.permitted(owner, "DELETE", record, []))

    def test_atlas_composition_projects_only_approved_fields(self):
        permissions = self.module("P101", "permissions.py")
        with patch.dict(sys.modules, {"permissions": permissions}):
            views = self.module("P101", "views.py")
        data = json.loads((ap.ROOT / "projects/P101/records.json").read_text())
        record = data["records"][0]
        for operation in (views.read_summary, views.export_summary):
            result = operation(data["principals"][1], record, data["grants"])
            self.assertEqual(result, {"record_id": "D1", "title": "Quarterly summary"})
            with self.assertRaises(PermissionError):
                operation(data["principals"][2], record, data["grants"])

    def test_delta_journal_supports_only_the_scoped_finite_inconsistency(self):
        identity = self.module("P202", "identity.py").logical_identity
        data = json.loads((ap.ROOT / "projects/P202/journal.json").read_text())
        groups = {}
        for row in data["committed_effects"]:
            key = identity(row["workspace_id"], row["operation_id"])
            groups.setdefault(key, []).append(row["effect_id"])
        self.assertEqual(groups[("red", "J7")], ["E1", "E2"])
        self.assertEqual(groups[("blue", "J7")], ["E3"])
        self.assertEqual(data["compensations"], [])

    def test_delta_receipt_does_not_claim_commitment(self):
        receipt = self.module("P202", "receipts.py").receipt("A", "W", "J")
        self.assertEqual(receipt["status"], "accepted")
        self.assertNotIn("effect_id", receipt)
        self.assertNotIn("committed", receipt)

    def test_beacon_valid_signature_is_not_the_only_policy_condition(self):
        permits = self.module("P303", "approval.py").permits
        p = json.loads((ap.ROOT / "projects/P303/policies.json").read_text())
        r = json.loads((ap.ROOT / "projects/P303/release-record.json").read_text())
        statement, digest = r["signed_statement"], r["artifact_digest"]
        self.assertTrue(permits(statement, p["staging"], p["roles"], digest))
        self.assertFalse(permits(statement, p["production"], p["roles"], digest))
        release = {**statement, "audience": "production", "signer": "approver-1"}
        self.assertTrue(permits(release, p["production"], p["roles"], digest))
        self.assertFalse(permits(release, p["production"], p["roles"], "other-digest"))
        self.assertFalse(permits({**release, "signature_verified": False}, p["production"], p["roles"], digest))

    def test_cedar_lengths_describe_the_same_byte_snapshot(self):
        snapshot = self.module("P404", "encoding.py").snapshot
        rows = json.loads((ap.ROOT / "projects/P404/checks.json").read_text())["desktop_observations"]
        for row in rows:
            data, length = snapshot(row["input"])
            self.assertIsInstance(data, bytes)
            self.assertEqual(data.hex(), row["bytes_hex"])
            self.assertEqual(length, row["length_bytes"])
        data, length = snapshot("")
        self.assertEqual((data, length), (b"", 0))

    def test_cedar_metadata_is_a_projection_not_rendered_text(self):
        metadata = self.module("P404", "view.py").metadata
        self.assertEqual(metadata({"document_id": "N", "title": "T", "text": "body"}),
                         {"document_id": "N", "title": "T"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
