from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

PREBLIND_STATUS = "READY_FOR_PREBLIND_MODELING"
POSTBLIND_RELEASED = "POSTBLIND_OPTION_CHALLENGE_RELEASED"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _object_hash(value: dict[str, Any]) -> str:
    body = deepcopy(value)
    body.pop("object_hash", None)
    return hashlib.sha256(_canonical_bytes(body)).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str | Path, value: dict[str, Any], *, replace: bool = False) -> None:
    target = Path(path)
    if target.exists() and not replace:
        raise RuntimeError(f"immutable staged-access output exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    body = deepcopy(value)
    body["object_hash"] = _object_hash(body)
    target.write_text(json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _unique(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for path in paths:
        text = str(Path(path))
        if text not in seen:
            seen.add(text)
            output.append(text)
    return output


def _safe_question_rows(case: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"question_id": row["question_id"], "stem": row.get("stem", "")}
        for row in case.get("questions", {}).get("parsed", [])
    ]


def _option_rows(case: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "question_id": row["question_id"],
            "options": deepcopy(row.get("options", [])),
        }
        for row in case.get("questions", {}).get("parsed", [])
    ]


def harden_clean_start(result: dict[str, Any]) -> dict[str, Any]:
    clean_path = Path(result["clean_start_path"])
    clean = _read_json(clean_path)
    output_root = clean_path.parent
    original_allowed = list(clean.get("retrieval_policy", {}).get("exact_allowed_paths", []))

    safe_case_paths: list[str] = []
    withheld_paths: list[str] = []
    source_case_paths: set[str] = set()
    unsafe_skeleton_paths: set[str] = set()

    for case_row in clean["cases"]:
        source_case_path = Path(case_row["input_path"])
        source_case_paths.add(str(source_case_path))
        case = _read_json(source_case_path)
        case_id = case_row["case_id"]

        preblind_path = output_root / "preblind-inputs" / f"{case_id}.json"
        option_path = output_root / "withheld-options" / f"{case_id}.json"
        blind_skeleton_path = output_root / "preblind-skeletons" / f"{case_id}.json"
        postblind_template_path = output_root / "withheld-postblind-templates" / f"{case_id}.json"

        preblind_input = {
            "schema": "PREBLIND-CASE-INPUT-V1",
            "case_id": case_id,
            "dataset_type": case.get("dataset_type"),
            "binding": deepcopy(clean.get("active_runtime_binding") or case.get("binding", {})),
            "answer_data_available": False,
            "option_visibility": "WITHHELD",
            "bazi": deepcopy(case.get("bazi", {})),
            "ziwei": deepcopy(case.get("ziwei", {})),
            "question_stems": _safe_question_rows(case),
        }
        _write_json(preblind_path, preblind_input)

        option_payload = {
            "schema": "POSTBLIND-OPTION-PAYLOAD-V1",
            "case_id": case_id,
            "run_id": case_row["case_run_id"],
            "answer_data_available": False,
            "release_condition": "ALL_QUESTIONS_HAVE_MACHINE_VALID_ZIWEI_AND_BAZI_PREBLIND_SEALS",
            "questions": _option_rows(case),
            "status": "WITHHELD_UNTIL_PREBLIND_SEALS_PASS",
        }
        _write_json(option_path, option_payload)

        old_skeleton_path = Path(case_row["skeleton_path"])
        unsafe_skeleton_paths.add(str(old_skeleton_path))
        old_skeleton = _read_json(old_skeleton_path)
        _write_json(postblind_template_path, old_skeleton)

        blind_skeleton = {
            "schema": "PREBLIND-PREDICTION-SKELETON-V1",
            "case_id": case_id,
            "dataset_type": case.get("dataset_type"),
            "run_id": case_row["case_run_id"],
            "binding": deepcopy(clean.get("active_runtime_binding") or case.get("binding", {})),
            "answer_data_available": False,
            "option_visibility": "WITHHELD",
            "questions": [
                {
                    "question_id": row["question_id"],
                    "ziwei_blind_axis_model": None,
                    "bazi_blind_axis_model": None,
                    "ziwei_preblind_seal": None,
                    "bazi_preblind_seal": None,
                    "sealed_before_option_access": False,
                }
                for row in _safe_question_rows(case)
            ],
            "status": PREBLIND_STATUS,
        }
        _write_json(blind_skeleton_path, blind_skeleton)
        old_skeleton_path.unlink()

        case_row.clear()
        case_row.update({
            "case_id": case_id,
            "case_run_id": blind_skeleton["run_id"],
            "source_input_sha256": _sha256_file(source_case_path),
            "preblind_input_path": str(preblind_path),
            "preblind_input_sha256": _sha256_file(preblind_path),
            "preblind_skeleton_path": str(blind_skeleton_path),
            "preblind_skeleton_sha256": _sha256_file(blind_skeleton_path),
            "withheld_option_payload_hash": _sha256_file(option_path),
            "withheld_postblind_template_hash": _sha256_file(postblind_template_path),
            "postblind_locator_visibility": "NOT_EXPOSED_IN_PREBLIND_CASE_ROW",
        })
        safe_case_paths.extend([str(preblind_path), str(blind_skeleton_path)])
        withheld_paths.extend([str(option_path), str(postblind_template_path)])

    safe_allowed = [
        path for path in original_allowed
        if path not in source_case_paths and path not in unsafe_skeleton_paths
    ]
    safe_allowed = _unique(safe_allowed + safe_case_paths)
    clean["retrieval_policy"]["exact_allowed_paths"] = safe_allowed
    clean["retrieval_policy"]["staged_access"] = {
        "current_stage": "PREBLIND",
        "preblind_allowed_paths": safe_allowed,
        "withheld_path_hashes": [
            {"sha256": _sha256_file(Path(path)), "role": "POSTBLIND_ONLY"}
            for path in withheld_paths
        ],
        "withheld_paths_not_disclosed_to_prediction_context": True,
        "release_receipt_schema": "POSTBLIND-ACCESS-RECEIPT-V1",
        "release_requires": "MACHINE_VALID_DUAL_TRACK_PREBLIND_SEALS_FOR_ALL_QUESTIONS",
    }
    clean["contamination_policy"]["on_preblind_option_visibility"] = "FAIL_CLOSED_NEW_GROUP_RUN_REQUIRED"
    clean["status"] = PREBLIND_STATUS
    _write_json(clean_path, clean, replace=True)

    hardened = _read_json(clean_path)
    return {
        **hardened,
        "clean_start_path": str(clean_path),
        "clean_start_sha256": _sha256_file(clean_path),
    }


def _source_case_map(clean: dict[str, Any]) -> dict[str, str]:
    manifest_path = Path(clean["group_manifest"]["path"])
    manifest = _read_json(manifest_path)
    return {row["case_id"]: row["path"] for row in manifest["cases"]}


def build_legacy_runtime_inputs(request_path: str | Path, temp_root: str | Path) -> tuple[Path, Path]:
    request_path = Path(request_path)
    request = _read_json(request_path)
    clean_path = Path(request["clean_start_path"])
    clean = _read_json(clean_path)
    source_map = _source_case_map(clean)

    legacy_clean = deepcopy(clean)
    legacy_clean["status"] = "READY_FOR_CLEAN_GROUP_PREDICTION"
    for row in legacy_clean["cases"]:
        row["input_path"] = source_map[row["case_id"]]
        row["input_sha256"] = _sha256_file(Path(row["input_path"]))
        row["skeleton_path"] = row["preblind_skeleton_path"]
        row["skeleton_sha256"] = row["preblind_skeleton_sha256"]

    temp_root = Path(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)
    legacy_clean_path = temp_root / "legacy-clean-start.json"
    legacy_request_path = temp_root / "legacy-runtime-request.json"
    _write_json(legacy_clean_path, legacy_clean)
    legacy_request = deepcopy(request)
    legacy_request["clean_start_path"] = str(legacy_clean_path)
    _write_json(legacy_request_path, legacy_request)
    return legacy_request_path, clean_path


def _safe_text_by_question(preblind: dict[str, Any]) -> dict[str, str]:
    chart_text = json.dumps({"bazi": preblind.get("bazi", {}), "ziwei": preblind.get("ziwei", {})}, ensure_ascii=False)
    return {
        row["question_id"]: f"{row.get('stem', '')}\n{chart_text}"
        for row in preblind.get("question_stems", [])
    }


def _preblind_source_packet(full_packet: dict[str, Any], preblind: dict[str, Any]) -> dict[str, Any]:
    safe_text = _safe_text_by_question(preblind)
    selected: list[dict[str, Any]] = []
    for item in full_packet.get("items", []):
        qids = item.get("target_question_ids", [])
        matched = item.get("matched_keywords", [])
        safe_qids = [qid for qid in qids if any(keyword in safe_text.get(qid, "") for keyword in matched)]
        if not safe_qids:
            continue
        safe_item = deepcopy(item)
        safe_item["target_question_ids"] = safe_qids
        safe_item["selection_basis"] = "QUESTION_STEM_AND_FROZEN_CHART_ONLY"
        selected.append(safe_item)

    route_counts: dict[str, int] = {}
    for item in selected:
        route_counts[item["library_id"]] = route_counts.get(item["library_id"], 0) + 1
    route_rows = []
    for row in full_packet.get("route_rows", []):
        safe_row = deepcopy(row)
        safe_row["selected_item_count"] = route_counts.get(row["library_id"], 0)
        safe_row["route_status"] = "PREBLIND_ITEMS_SELECTED" if safe_row["selected_item_count"] else "NO_SAFE_PREBLIND_MATCH"
        route_rows.append(safe_row)

    question_coverage = {}
    for qid in safe_text:
        question_coverage[qid] = {
            "selection_basis": "QUESTION_STEM_AND_FROZEN_CHART_ONLY",
            "packet_item_ids": [item["packet_item_id"] for item in selected if qid in item.get("target_question_ids", [])],
        }

    return {
        "schema": "FORTUNE-PREBLIND-SOURCE-PACKET-V1",
        "status": "PREBLIND_READY",
        "case_id": full_packet["case_id"],
        "run_id": full_packet["run_id"],
        "group_run_id": full_packet["group_run_id"],
        "knowledge_release_id": full_packet["knowledge_release_id"],
        "knowledge_manifest_path": full_packet["knowledge_manifest_path"],
        "knowledge_manifest_object_hash": full_packet["knowledge_manifest_object_hash"],
        "answer_data_available": False,
        "option_visibility": "WITHHELD",
        "route_rows": route_rows,
        "items": selected,
        "question_coverage": question_coverage,
    }


def harden_runtime_packets(legacy_result: dict[str, Any], request_path: str | Path, canonical_clean_path: str | Path) -> dict[str, Any]:
    request = _read_json(request_path)
    clean_path = Path(canonical_clean_path)
    clean = _read_json(clean_path)
    output_root = Path(request["output_root"])
    preblind_allowed = list(clean["retrieval_policy"]["exact_allowed_paths"])
    withheld: list[str] = []
    safe_generated: list[str] = []
    preblind_counts: dict[str, int] = {}

    case_lookup = {row["case_id"]: row for row in clean["cases"]}
    for case_id, case_row in case_lookup.items():
        case_root = output_root / "runtime-packets" / case_id
        sidecar_root = output_root / "case-input-sidecars" / case_id
        full_source_path = case_root / "source-packet.json"
        postblind_source_path = case_root / "withheld-postblind-source-packet.json"
        preblind_source_path = case_root / "preblind-source-packet.json"
        method_packet_path = case_root / "method-packet.json"
        run_contract_path = case_root / "run-contract.json"
        questions_sidecar = sidecar_root / "questions.json"
        ziwei_sidecar = sidecar_root / "ziwei.txt"
        bazi_sidecar = sidecar_root / "bazi.json"

        full_packet = _read_json(full_source_path)
        postblind_source_path.parent.mkdir(parents=True, exist_ok=True)
        full_source_path.replace(postblind_source_path)
        preblind = _read_json(case_row["preblind_input_path"])
        safe_packet = _preblind_source_packet(full_packet, preblind)
        _write_json(preblind_source_path, safe_packet)
        preblind_counts[case_id] = len(safe_packet["items"])
        if questions_sidecar.exists():
            questions_sidecar.unlink()

        option_path = output_root / "withheld-options" / f"{case_id}.json"
        postblind_template_path = output_root / "withheld-postblind-templates" / f"{case_id}.json"
        stage_plan_path = case_root / "stage-access-plan.json"
        stage_plan = {
            "schema": "FORTUNE-STAGED-ACCESS-PLAN-V1",
            "status": PREBLIND_STATUS,
            "case_id": case_id,
            "run_id": case_row["case_run_id"],
            "group_run_id": clean["group_run_id"],
            "answer_data_available": False,
            "current_stage": "PREBLIND",
            "preblind_allowed_paths": _unique([
                case_row["preblind_input_path"],
                case_row["preblind_skeleton_path"],
                str(ziwei_sidecar),
                str(bazi_sidecar),
                str(preblind_source_path),
                str(method_packet_path),
                str(run_contract_path),
            ]),
            "postblind_withheld_paths": [str(option_path), str(postblind_template_path), str(postblind_source_path)],
            "release_condition": "ALL_QUESTION_ROWS_HAVE_ZIWEI_AND_BAZI_PREBLIND_SEAL_PASS_AND_NO_OPTION_ACCESS_BEFORE_SEAL",
            "release_receipt_schema": "POSTBLIND-ACCESS-RECEIPT-V1",
        }
        _write_json(stage_plan_path, stage_plan)

        contract = _read_json(run_contract_path)
        contract["status"] = PREBLIND_STATUS
        contract["input_snapshot"] = {
            "preblind_input_path": case_row["preblind_input_path"],
            "preblind_input_sha256": case_row["preblind_input_sha256"],
            "ziwei_sidecar_path": str(ziwei_sidecar),
            "ziwei_sidecar_sha256": _sha256_file(ziwei_sidecar),
            "bazi_sidecar_path": str(bazi_sidecar),
            "bazi_sidecar_sha256": _sha256_file(bazi_sidecar),
            "option_visibility": "WITHHELD",
        }
        contract["source_packet_path"] = str(preblind_source_path)
        contract["postblind_source_packet_status"] = "WITHHELD"
        contract["prediction_skeleton_path"] = case_row["preblind_skeleton_path"]
        contract["stage_access_plan_path"] = str(stage_plan_path)
        contract["postblind_release_condition"] = stage_plan["release_condition"]
        _write_json(run_contract_path, contract, replace=True)

        safe_generated.extend(stage_plan["preblind_allowed_paths"] + [str(stage_plan_path)])
        withheld.extend(stage_plan["postblind_withheld_paths"])

    transport_path = Path(legacy_result["transport_plan_path"])
    transport = _read_json(transport_path)
    unsafe_suffixes = (
        "/questions.json",
        "/source-packet.json",
        "/withheld-postblind-source-packet.json",
        "/withheld-options/",
        "/withheld-postblind-templates/",
    )
    safe_existing = []
    for path in transport.get("exact_allowed_paths", []):
        if path in withheld:
            continue
        if any(suffix in path for suffix in unsafe_suffixes):
            continue
        if path.startswith("training-data/") and "/cases/" in path:
            continue
        if path.startswith("data/group-clean-starts/") and "/case-skeletons/" in path:
            continue
        safe_existing.append(path)
    transport["status"] = PREBLIND_STATUS
    transport["current_stage"] = "PREBLIND"
    transport["exact_allowed_paths"] = _unique(preblind_allowed + safe_existing + safe_generated)
    transport["generated_paths"] = _unique(safe_generated)
    transport["withheld_path_hashes"] = [
        {"sha256": _sha256_file(Path(path)), "role": "POSTBLIND_ONLY"}
        for path in withheld
    ]
    transport["postblind_release_receipt_required"] = True
    transport["postblind_release_receipt_schema"] = "POSTBLIND-ACCESS-RECEIPT-V1"
    transport["parent_clean_start_path"] = str(clean_path)
    _write_json(transport_path, transport, replace=True)

    clean["runtime_stage"] = {
        "status": PREBLIND_STATUS,
        "retrieval_transport_plan_path": str(transport_path),
        "postblind_release_receipt_required": True,
    }
    _write_json(clean_path, clean, replace=True)

    return {
        "schema": "GROUP-STAGED-RUNTIME-PACKET-BUILD-RESULT-V1",
        "status": PREBLIND_STATUS,
        "group_run_id": clean["group_run_id"],
        "case_count": len(case_lookup),
        "preblind_source_packet_item_counts": preblind_counts,
        "transport_plan_path": str(transport_path),
        "generated_path_count": len(_unique(safe_generated)) + 1,
        "withheld_path_count": len(withheld),
        "answer_data_available": False,
        "option_visibility": "WITHHELD",
    }


def release_postblind_stage(stage_plan_path: str | Path, seal_bundle_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    plan = _read_json(stage_plan_path)
    seals = _read_json(seal_bundle_path)
    if plan.get("schema") != "FORTUNE-STAGED-ACCESS-PLAN-V1" or plan.get("status") != PREBLIND_STATUS:
        raise RuntimeError("invalid staged access plan")
    if seals.get("schema") != "PREBLIND-SEAL-BUNDLE-V1" or seals.get("status") != "PASS":
        raise RuntimeError("invalid preblind seal bundle")
    if seals.get("case_id") != plan.get("case_id") or seals.get("run_id") != plan.get("run_id"):
        raise RuntimeError("seal identity mismatch")
    if seals.get("option_access_before_all_seals") is not False:
        raise RuntimeError("option access occurred before all seals")

    rows = seals.get("questions", [])
    if not rows:
        raise RuntimeError("missing question seal rows")
    for row in rows:
        if row.get("sealed_before_option_access") is not True:
            raise RuntimeError(f"question not sealed before option access: {row.get('question_id')}")
        for track in ("ziwei", "bazi"):
            receipt = row.get(track, {})
            if receipt.get("status") != "PASS" or not receipt.get("model_hash") or not receipt.get("seal_hash"):
                raise RuntimeError(f"invalid {track} seal: {row.get('question_id')}")

    receipt = {
        "schema": "POSTBLIND-ACCESS-RECEIPT-V1",
        "status": POSTBLIND_RELEASED,
        "case_id": plan["case_id"],
        "run_id": plan["run_id"],
        "group_run_id": plan["group_run_id"],
        "preblind_stage_plan_sha256": _sha256_file(Path(stage_plan_path)),
        "preblind_seal_bundle_sha256": _sha256_file(Path(seal_bundle_path)),
        "option_access_before_all_seals": False,
        "released_paths": plan["postblind_withheld_paths"],
        "allowed_paths_after_release": _unique(plan["preblind_allowed_paths"] + plan["postblind_withheld_paths"]),
        "answer_data_available": False,
    }
    _write_json(output_path, receipt)
    return _read_json(output_path)
