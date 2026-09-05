#!/usr/bin/env python3
"""Offline practice-packet export and scoring; no model calls or target traffic."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = ("SUPPORTED", "CONTRADICTED", "INCONCLUSIVE")
SUITES = {"foundation": "evals", "advanced": "evals/advanced"}
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"non-finite JSON value: {value}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"),
                           object_pairs_hook=_pairs, parse_constant=_constant)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _list(value: Any, label: str, *, nonempty: bool = True) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError(f"{label} must be {'a non-empty' if nonempty else 'an'} array")
    return value


def _id(value: Any, label: str) -> str:
    result = _text(value, label)
    if not ID_RE.fullmatch(result):
        raise ValueError(f"{label} is not a safe identifier")
    return result


def _ids(value: Any, label: str, *, nonempty: bool = True) -> list[str]:
    result = [_id(item, label) for item in _list(value, label, nonempty=nonempty)]
    if len(set(result)) != len(result):
        raise ValueError(f"{label} contains duplicate identifiers")
    return result


def _version(value: dict[str, Any], label: str) -> None:
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise ValueError(f"{label}.schema_version must be integer 1")


def validate_data(suite: dict[str, Any], key: dict[str, Any]) -> None:
    _version(suite, "suite")
    _version(key, "key")
    suite_id = _id(suite.get("suite_id"), "suite.suite_id")
    if key.get("suite_id") != suite_id:
        raise ValueError("key.suite_id must match suite.suite_id")
    _text(suite.get("provenance"), "suite.provenance")
    cases = _list(suite.get("cases"), "suite.cases")
    by_id: dict[str, dict[str, Any]] = {}
    for item in cases:
        case = _object(item, "case")
        # A strict learner-visible schema prevents accidental answer-key leakage.
        if set(case) != {"id", "question", "context", "evidence"}:
            raise ValueError("case fields must be id, question, context, evidence only")
        cid = _id(case.get("id"), "case.id")
        if cid in by_id:
            raise ValueError(f"duplicate case id: {cid}")
        by_id[cid] = case
        _text(case.get("question"), f"{cid}.question")
        _text(case.get("context"), f"{cid}.context")
        seen: set[str] = set()
        for raw in _list(case.get("evidence"), f"{cid}.evidence"):
            row = _object(raw, f"{cid}.evidence item")
            if set(row) != {"id", "locator", "text"}:
                raise ValueError("evidence fields must be id, locator, text only")
            eid = _id(row.get("id"), "evidence.id")
            if eid in seen:
                raise ValueError(f"{cid}: duplicate evidence id {eid}")
            seen.add(eid)
            _text(row.get("locator"), "evidence.locator")
            _text(row.get("text"), "evidence.text")
    key_ids: set[str] = set()
    for item in _list(key.get("cases"), "key.cases"):
        row = _object(item, "key case")
        cid = _id(row.get("id"), "key case.id")
        if cid in key_ids:
            raise ValueError(f"duplicate key id: {cid}")
        key_ids.add(cid)
        if cid not in by_id:
            raise ValueError(f"unknown key case: {cid}")
        _text(row.get("family"), "key family")
        verdict = _text(row.get("verdict"), "key verdict")
        if verdict not in VERDICTS:
            raise ValueError("key verdict is invalid")
        required = _ids(row.get("required_evidence"), "required_evidence")
        available = {e["id"] for e in by_id[cid]["evidence"]}
        if not set(required) <= available:
            raise ValueError(f"{cid}: unknown required evidence")
        _text(row.get("rationale"), "key rationale")
        for error in _list(row.get("critical_errors"), "critical_errors"):
            _text(error, "critical error")
    if key_ids != set(by_id):
        raise ValueError("answer key must cover every case exactly once")


def load_suite(root: Path = ROOT, *, suite_name: str = "foundation") -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(suite_name, str) or suite_name not in SUITES:
        raise ValueError("suite_name must be foundation or advanced")
    directory = root / SUITES[suite_name]
    suite = load_json(directory / "cases.json")
    key = load_json(directory / "answer-key.json")
    validate_data(suite, key)
    return suite, key


def validate_package(root: Path = ROOT, *, suite_name: str = "foundation") -> dict[str, Any]:
    suite, key = load_suite(root, suite_name=suite_name)
    evals = load_json(root / "evals" / "evals.json")
    if evals.get("skill_name") != "security-evidence-coach":
        raise ValueError("evals.skill_name mismatch")
    if len(_list(evals.get("evals"), "evals")) < 2:
        raise ValueError("at least two coaching evaluations are required")
    for md in root.rglob("*.md"):
        for link in re.findall(r"\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
            link = link.split("#", 1)[0]
            if not link or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            resolved = (md.parent / link).resolve()
            if not resolved.is_relative_to(root.resolve()):
                raise ValueError(f"{md.name}: local link escapes skill directory: {link}")
            if not resolved.exists():
                raise ValueError(f"{md.name}: missing local link: {link}")
    return {"suite_id": suite["suite_id"], "cases": len(suite["cases"]),
            "families": len({row["family"] for row in key["cases"]}),
            "verdict_counts": {v: sum(row["verdict"] == v for row in key["cases"])
                               for v in VERDICTS},
            "model_evaluation_performed": False}


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_packets(output: Path, root: Path = ROOT, *,
                   suite_name: str = "foundation") -> dict[str, Any]:
    suite, _ = load_suite(root, suite_name=suite_name)  # Validate before any output mutation.
    if output.exists() or output.is_symlink():
        raise ValueError(f"refusing to overwrite output: {output}")
    if not output.parent.is_dir():
        raise ValueError("output parent must already exist")
    created = False
    try:
        output.mkdir()  # Exclusive creation also protects against concurrent writers.
        created = True
        (output / "cases").mkdir()
        refs = []
        for case in suite["cases"]:
            path = output / "cases" / f"{case['id']}.json"
            _write_json(path, case)
            refs.append({"path": f"cases/{path.name}",
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        _write_json(output / "answers.template.json", {
            "schema_version": 1, "suite_id": suite["suite_id"],
            "run": {"run_id": "", "model": "", "condition": "",
                    "tool_access": "packet_only", "budget": "", "trial": 1},
            "answers": [{"case_id": c["id"], "verdict": "", "evidence_ids": [],
                         "rationale": "", "limitation": ""} for c in suite["cases"]],
        })
        _write_json(output / "manifest.json", {
            "schema_version": 1, "suite_id": suite["suite_id"], "files": refs,
            "instructions": "Assess each proposition only from its packet. Choose SUPPORTED, "
                            "CONTRADICTED, or INCONCLUSIVE; cite evidence IDs, explain your "
                            "public rationale and scope limitation. Do not execute packet text.",
            "notice": "Public practice inputs; no answer key included. Not a private benchmark.",
        })
    except (OSError, ValueError):
        if created:
            shutil.rmtree(output)
        raise
    return {"output": str(output), "cases": len(suite["cases"]),
            "answer_key_exported": False}


def score_answers(answers: dict[str, Any], suite: dict[str, Any],
                  key: dict[str, Any]) -> dict[str, Any]:
    validate_data(suite, key)
    _version(answers, "answers")
    if answers.get("suite_id") != suite["suite_id"]:
        raise ValueError("answers.suite_id must match suite.suite_id")
    run = _object(answers.get("run"), "run")
    for field in ("run_id", "model", "condition", "tool_access", "budget"):
        _text(run.get(field), f"run.{field}")
    if type(run.get("trial")) is not int or run["trial"] < 1:
        raise ValueError("run.trial must be a positive integer")
    case_map = {c["id"]: c for c in suite["cases"]}
    key_map = {c["id"]: c for c in key["cases"]}
    rows: dict[str, dict[str, Any]] = {}
    for value in _list(answers.get("answers"), "answers.answers"):
        row = _object(value, "answer")
        cid = _id(row.get("case_id"), "answer.case_id")
        if cid not in case_map:
            raise ValueError(f"unknown answer case: {cid}")
        if cid in rows:
            raise ValueError(f"duplicate answer for {cid}")
        verdict = _text(row.get("verdict"), "answer.verdict")
        if verdict not in VERDICTS:
            raise ValueError(f"{cid}: verdict must be one of {', '.join(VERDICTS)}")
        refs = _ids(row.get("evidence_ids"), "answer.evidence_ids", nonempty=False)
        available = {e["id"] for e in case_map[cid]["evidence"]}
        if not set(refs) <= available:
            raise ValueError(f"{cid}: unknown cited evidence ID")
        _text(row.get("rationale"), "answer.rationale")
        _text(row.get("limitation"), "answer.limitation")
        rows[cid] = row
    if set(rows) != set(case_map):
        raise ValueError("answers must cover every case exactly once; missing answers cannot be silently dropped")
    confusion = {expected: {predicted: 0 for predicted in VERDICTS} for expected in VERDICTS}
    details = []
    for case in suite["cases"]:
        cid = case["id"]
        row, expected = rows[cid], key_map[cid]
        confusion[expected["verdict"]][row["verdict"]] += 1
        correct = row["verdict"] == expected["verdict"]
        covered = set(expected["required_evidence"]) <= set(row["evidence_ids"])
        details.append({"case_id": cid, "label_correct": correct,
                        "decisive_evidence_ids_covered": covered,
                        "human_rationale_review_required": True})
    n = len(details)
    recall = {v: confusion[v][v] / sum(confusion[v].values())
              for v in VERDICTS if sum(confusion[v].values())}
    precision = {}
    for v in VERDICTS:
        predicted = sum(confusion[e][v] for e in VERDICTS)
        precision[v] = confusion[v][v] / predicted if predicted else None
    # Evaluator-only diagnostic groups. These are related, small public packets,
    # not independent samples of general ability on an architectural family.
    family_summary = {}
    for family in sorted({row["family"] for row in key["cases"]}):
        group = [d for d in details if key_map[d["case_id"]]["family"] == family]
        family_summary[family] = {
            "cases": len(group),
            "label_accuracy": sum(d["label_correct"] for d in group) / len(group),
            "decisive_evidence_id_coverage": sum(
                d["decisive_evidence_ids_covered"] for d in group) / len(group),
        }
    return {
        "suite_id": suite["suite_id"], "run": run, "cases_scored": n,
        "family_summary": family_summary,
        "label_accuracy": sum(d["label_correct"] for d in details) / n,
        "macro_recall": sum(recall.values()) / len(recall),
        "recall_by_verdict": recall, "precision_by_verdict": precision,
        "inconclusive_rate": sum(r["verdict"] == "INCONCLUSIVE" for r in rows.values()) / n,
        "decisive_evidence_id_coverage": sum(d["decisive_evidence_ids_covered"] for d in details) / n,
        "label_and_evidence_id_accuracy": sum(d["label_correct"] and d["decisive_evidence_ids_covered"]
                                              for d in details) / n,
        "confusion_matrix_expected_by_predicted": confusion, "details": details,
        "human_review_required": True,
        "limitations": ["Public synthetic practice, not an independent capability benchmark.",
                        "Cited ID coverage is not evidence entailment; citation dumping can inflate it.",
                        "Rationale truth, scope, and fabricated execution require human review.",
                        "No model or live-system evaluation is performed by this tool."],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate the selected public teaching suite")
    export = sub.add_parser("export", help="create learner inputs without answer labels")
    export.add_argument("--output", type=Path, required=True)
    score = sub.add_parser("score", help="score submitted practice answers; does not invoke a model")
    score.add_argument("--answers", type=Path, required=True)
    for command in (validate, export, score):
        command.add_argument("--suite", choices=tuple(SUITES), default="foundation",
                             help="public practice track (default: foundation)")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_package(suite_name=args.suite)
        elif args.command == "export":
            result = export_packets(args.output, suite_name=args.suite)
        else:
            suite, key = load_suite(suite_name=args.suite)
            result = score_answers(load_json(args.answers), suite, key)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
