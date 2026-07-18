import json
from pathlib import Path

import pytest

from fortune_v1.causal_use import build_run_contract, validate_causal_use
from fortune_v1.repository_release import (
    METHOD_STAGES, build_knowledge_manifest, build_method_packet,
    build_model_release, write_object,
)
from fortune_v1.source_delivery import build_source_catalog, build_source_packet
from fortune_v1.util import FortuneError


def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fixture(tmp_path: Path):
    source = tmp_path / "knowledge" / "base"
    source.mkdir(parents=True)
    for i in range(20):
        lib = f"S{i:02d}"
        (source / f"{lib}_测试库.txt").write_text(
            f"LIBRARY_ID={lib}\nSOURCE_FAMILY_ID={lib}-FAMILY\n\n"
            f"{lib} parent alpha 条件必须保留；不得越级。\n",
            encoding="utf-8",
        )
    manifest = tmp_path / "manifest.json"
    build_knowledge_manifest(
        source, manifest, release_id="K-R16", repository="owner/repo",
        commit_sha="a" * 40, s19_binding_sha256="b" * 64, release_kind="BASE",
    )
    method_path = tmp_path / "method.json"
    stages = []
    for n, stage in enumerate(METHOD_STAGES, 1):
        stages.append({
            "stage_id": stage,
            "rules": [{
                "rule_id": f"R{n:02d}", "source_authority": "S00",
                "requirement": stage, "failure_status": "FAIL_CLOSED",
            }],
        })
    write_object(method_path, {
        "schema": "FORTUNE-METHOD-RELEASE-V1",
        "method_release_id": "M-R16", "stages": stages,
    })
    method_packet = tmp_path / "method-packet.json"
    build_method_packet(method_path, method_packet)
    model = tmp_path / "model.json"
    build_model_release(
        manifest, method_path, model, model_release_id="MODEL-R16",
        main_prompt_runtime_id="MP-R16", code_commit_sha="c" * 40,
    )
    catalog = tmp_path / "catalog.json"
    build_source_catalog(manifest, source, catalog)
    case = tmp_path / "case.json"
    dump(case, {"case_id": "CASE-1", "case_input_hash": "d" * 64})
    plan = tmp_path / "plan.json"
    dump(plan, {
        "required_source_family_rows": [{
            "route_id": "S05-ROUTE", "library_id": "S05", "query_terms": ["alpha"],
        }],
        "conditional_source_family_rows": [],
    })
    packet = tmp_path / "source-packet.json"
    source_packet = build_source_packet(catalog, plan, case, packet)
    contract = tmp_path / "contract.json"
    build_run_contract(
        model, packet, method_packet, case, contract,
        run_id="RUN-1", case_id="CASE-1", dataset_type="DEV",
        question_rows=[{
            "question_id": "Q1", "option_ids": ["A", "B"],
            "required_pairwise_rows": 1,
        }],
    )
    binding = json.loads(contract.read_text())["binding"]
    item = source_packet["items"][0]
    prediction = tmp_path / "prediction.json"
    dump(prediction, {
        "run_id": "RUN-1", "case_id": "CASE-1", "binding": binding,
        "questions": [{
            "question_id": "Q1",
            "evidence_ledger": [{
                "packet_item_id": item["packet_item_id"],
                "source_library": item["library_id"],
                "source_file_sha256": item["source_sha256"],
                "source_root_atom": item["source_root_atom"],
            }],
            "method_stage_receipts": [{
                "stage_id": stage, "status": "EXECUTED",
                "method_rule_ids": [f"R{n:02d}"],
            } for n, stage in enumerate(METHOD_STAGES, 1)],
        }],
    })
    return prediction, contract, plan, catalog, case


def test_repository_packet_contract_and_causal_validation(tmp_path):
    prediction, contract, *_ = fixture(tmp_path)
    receipt = validate_causal_use(prediction, contract)
    assert receipt["status"] == "PASS"
    assert receipt["score_eligibility"] == "ELIGIBLE"

    body = json.loads(prediction.read_text())
    body["project_source"] = "/mnt/data/S05.txt"
    dump(prediction, body)
    failed = validate_causal_use(prediction, contract)
    assert failed["status"] == "FAIL_CLOSED"
    assert failed["score_eligibility"] == "PROHIBITED"
    assert any("PROJECT_UPLOAD_REFERENCE_DETECTED" in error for error in failed["errors"])


def test_source_packet_rejects_winner_bias(tmp_path):
    _, _, plan, catalog, case = fixture(tmp_path)
    biased = json.loads(plan.read_text())
    biased["top1"] = "A"
    dump(plan, biased)
    with pytest.raises(FortuneError) as exc:
        build_source_packet(catalog, plan, case, tmp_path / "biased.json")
    assert exc.value.status == "SOURCE_PACKET_ANSWER_ISOLATION_FAILED"
