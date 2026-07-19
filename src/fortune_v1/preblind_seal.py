from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, canonical_bytes, read_json, sha256_bytes, sha256_file, utc_now


def require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def resolve_within(root: Path, value: str | Path, status: str) -> Path:
    root = root.resolve()
    path = Path(value).resolve()
    require(root == path or root in path.parents, f"path escapes run root: {value}", status)
    return path


def with_hash(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_hash", None)
    body["object_hash"] = sha256_bytes(canonical_bytes(body))
    return body


def seal_basis(plan: dict[str, Any], question_id: str, track: str, model_hash: str) -> dict[str, Any]:
    return {
        "schema": "PREBLIND-TRACK-SEAL-BASIS-V1",
        "case_id": plan["case_id"],
        "run_id": plan["run_id"],
        "group_run_id": plan["group_run_id"],
        "question_id": question_id,
        "track": track,
        "model_hash": model_hash,
        "sealed_before_option_access": True,
        "option_access_before_all_seals": False,
    }


def validate_model(path: Path, plan: dict[str, Any], question_id: str, track: str) -> tuple[str, str]:
    model = read_json(path)
    require(model.get("schema") == "PREBLIND-TRACK-MODEL-V1", "model schema invalid", "PREBLIND_MODEL_SCHEMA_INVALID")
    require(model.get("status") == "READY_FOR_SEAL", "model status invalid", "PREBLIND_MODEL_NOT_READY")
    expected = {
        "case_id": plan["case_id"],
        "run_id": plan["run_id"],
        "group_run_id": plan["group_run_id"],
        "question_id": question_id,
        "track": track,
    }
    for field, value in expected.items():
        require(model.get(field) == value, f"model {field} mismatch", "PREBLIND_MODEL_IDENTITY_MISMATCH")
    require(model.get("answer_data_available") is False, "answer data available", "ANSWER_ISOLATION_FAILED")
    require(model.get("option_visibility") == "WITHHELD", "option visibility invalid", "PREBLIND_OPTION_VISIBILITY_FAILED")
    require(model.get("option_accessed") is False, "option accessed before seal", "PREBLIND_OPTION_ACCESS_CONTAMINATION")
    require(isinstance(model.get("blind_axis_model"), dict) and bool(model["blind_axis_model"]), "blind model missing", "PREBLIND_MODEL_PAYLOAD_INCOMPLETE")
    coverage = model.get("complete_knowledge_coverage_plan")
    require(isinstance(coverage, dict) and coverage.get("status") in {"PASS", "COMPLETE"}, "coverage incomplete", "PREBLIND_COVERAGE_PLAN_INCOMPLETE")
    require(isinstance(model.get("source_route_plan"), list), "source route plan missing", "PREBLIND_SOURCE_ROUTE_PLAN_MISSING")
    model_hash = sha256_file(path)
    seal_hash = sha256_bytes(canonical_bytes(seal_basis(plan, question_id, track, model_hash)))
    return model_hash, seal_hash


def write_new_or_same(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    expected = with_hash(value)
    if path.exists():
        actual = read_json(path)
        require(actual == expected, f"immutable object conflict: {path}", "IMMUTABLE_OBJECT_CONFLICT")
        return actual
    atomic_write_json(path, expected)
    return expected


def prepare_group_seals(request_path: str | Path, derived_request_path: str | Path) -> dict[str, Any]:
    request = read_json(request_path)
    require(request.get("schema") == "GROUP-PREBLIND-SEAL-AND-RELEASE-REQUEST-V1", "request schema invalid", "PREBLIND_SEAL_REQUEST_INVALID")
    require(request.get("status") == "REQUESTED", "request status invalid", "PREBLIND_SEAL_REQUEST_INVALID")
    clean_path = Path(request["clean_start_path"]).resolve()
    clean = read_json(clean_path)
    require(clean.get("status") == "READY_FOR_PREBLIND_MODELING", "clean start not PREBLIND", "CLEAN_START_STAGE_INVALID")
    require(clean.get("answer_data_available") is False, "answer data available", "ANSWER_ISOLATION_FAILED")
    require(clean.get("group_run_id") == request.get("group_run_id"), "group mismatch", "PREBLIND_SEAL_REQUEST_IDENTITY_MISMATCH")
    run_root = clean_path.parent.resolve()
    require(Path(request.get("output_root") or run_root).resolve() == run_root, "output root mismatch", "PREBLIND_SEAL_OUTPUT_PATH_INVALID")
    cases = {row["case_id"]: row for row in clean.get("cases", [])}
    submissions = request.get("case_model_submissions", [])
    require({row.get("case_id") for row in submissions} == set(cases), "case set mismatch", "PREBLIND_MODEL_CASE_SET_MISMATCH")

    release_rows = []
    seal_rows = []
    for submission in submissions:
        case_id = submission["case_id"]
        case = cases[case_id]
        plan_path = resolve_within(run_root, submission.get("stage_plan_path") or run_root / "runtime-packets" / case_id / "stage-access-plan.json", "STAGE_PLAN_PATH_INVALID")
        skeleton_path = resolve_within(run_root, case["preblind_skeleton_path"], "PREBLIND_SKELETON_PATH_INVALID")
        require(plan_path.is_file(), f"stage plan missing: {plan_path}", "STAGE_PLAN_MISSING")
        require(skeleton_path.is_file(), f"skeleton missing: {skeleton_path}", "PREBLIND_SKELETON_MISSING")
        plan = read_json(plan_path)
        skeleton = read_json(skeleton_path)
        require(plan.get("schema") == "FORTUNE-STAGED-ACCESS-PLAN-V1", "stage plan schema invalid", "STAGE_PLAN_SCHEMA_INVALID")
        require(plan.get("status") == "READY_FOR_PREBLIND_MODELING", "stage plan status invalid", "STAGE_PLAN_STATUS_INVALID")
        require(plan.get("case_id") == case_id and plan.get("run_id") == case["case_run_id"] and plan.get("group_run_id") == clean["group_run_id"], "stage plan identity mismatch", "STAGE_PLAN_IDENTITY_MISMATCH")
        expected_qids = [str(row["question_id"]) for row in skeleton.get("questions", [])]
        question_rows = submission.get("questions", [])
        require([str(row.get("question_id")) for row in question_rows] == expected_qids, "question order mismatch", "PREBLIND_MODEL_QUESTION_SET_MISMATCH")
        sealed_questions = []
        for row in question_rows:
            qid = str(row["question_id"])
            tracks = {}
            for track in ("ziwei", "bazi"):
                model_path = resolve_within(run_root, row[f"{track}_model_path"], "PREBLIND_MODEL_PATH_INVALID")
                require(model_path.is_file(), f"model missing: {model_path}", "PREBLIND_MODEL_MISSING")
                model_hash, seal_hash = validate_model(model_path, plan, qid, track)
                tracks[track] = {
                    "status": "PASS",
                    "model_path": str(model_path),
                    "model_hash": model_hash,
                    "seal_hash": seal_hash,
                }
            require(tracks["ziwei"]["model_hash"] != tracks["bazi"]["model_hash"], "tracks are not independent", "TRACK_INDEPENDENCE_FAILED")
            sealed_questions.append({
                "question_id": qid,
                "sealed_before_option_access": True,
                "ziwei": tracks["ziwei"],
                "bazi": tracks["bazi"],
            })
        bundle_path = run_root / "preblind-seals" / f"{case_id}.json"
        bundle = write_new_or_same(bundle_path, {
            "schema": "PREBLIND-SEAL-BUNDLE-V1",
            "status": "PASS",
            "case_id": case_id,
            "run_id": case["case_run_id"],
            "group_run_id": clean["group_run_id"],
            "option_access_before_all_seals": False,
            "questions": sealed_questions,
            "sealed_at": request.get("requested_at") or utc_now(),
        })
        release_rows.append({"case_id": case_id, "seal_bundle_path": str(bundle_path), "stage_plan_path": str(plan_path)})
        seal_rows.append({"case_id": case_id, "path": str(bundle_path), "sha256": sha256_file(bundle_path), "object_hash": bundle["object_hash"], "question_count": len(sealed_questions)})

    derived = {
        "schema": "GROUP-POSTBLIND-RELEASE-REQUEST-V1",
        "status": "REQUESTED",
        "group_run_id": clean["group_run_id"],
        "clean_start_path": str(clean_path),
        "output_root": str(run_root),
        "case_seal_bundles": release_rows,
        "requested_at": request.get("requested_at") or utc_now(),
    }
    atomic_write_json(derived_request_path, derived)
    return with_hash({
        "schema": "GROUP-PREBLIND-SEAL-MATERIALIZATION-RECEIPT-V1",
        "status": "PASS",
        "group_run_id": clean["group_run_id"],
        "case_count": len(seal_rows),
        "question_count": sum(row["question_count"] for row in seal_rows),
        "seals": seal_rows,
        "derived_release_request_path": str(derived_request_path),
        "answer_data_available": False,
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prepare-preblind-seals")
    parser.add_argument("--request", required=True)
    parser.add_argument("--derived-request", required=True)
    args = parser.parse_args(argv)
    try:
        result = prepare_group_seals(args.request, args.derived_request)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
