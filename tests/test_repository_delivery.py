import json
import tempfile
import unittest
from pathlib import Path

from fortune_v1.causal_use import build_run_contract, validate_causal_use
from fortune_v1.contamination import classify_repository_path, validate_runtime_object
from fortune_v1.repository_release import (
    METHOD_STAGES, build_knowledge_manifest, build_method_packet,
    build_model_release, write_object,
)
from fortune_v1.source_delivery import build_source_catalog, build_source_packet
from fortune_v1.util import FortuneError, sha256_file


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
    prompt_dir = tmp_path / "model" / "candidates" / "MODEL-R16"
    prompt_dir.mkdir(parents=True)
    prompt_text = prompt_dir / "main-prompt.txt"
    prompt_text.write_text("MAIN_PROMPT_RUNTIME_ID=MP-R16\n", encoding="utf-8")
    prompt_receipt = prompt_dir / "prompt-snapshot.json"
    write_object(prompt_receipt, {
        "schema": "MAIN-PROMPT-AUDIT-SNAPSHOT-V1",
        "runtime_id": "MP-R16",
        "snapshot_path": prompt_text.as_posix(),
        "snapshot_sha256": sha256_file(prompt_text),
        "snapshot_bytes": prompt_text.stat().st_size,
        "status": "PASS",
    })
    model = tmp_path / "model.json"
    build_model_release(
        manifest, method_path, prompt_receipt, model, model_release_id="MODEL-R16",
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
    return prediction, contract, plan, catalog, case, prompt_text


class RepositoryDeliveryTest(unittest.TestCase):
    def test_repository_packet_contract_and_causal_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            prediction, contract, *_ = fixture(Path(directory))
            receipt = validate_causal_use(prediction, contract)
            self.assertEqual(receipt["status"], "PASS")
            self.assertEqual(receipt["score_eligibility"], "ELIGIBLE")
            self.assertEqual(receipt["legacy_contamination_scan_status"], "PASS")

            body = json.loads(prediction.read_text())
            body["project_source"] = "/mnt/data/S05.txt"
            dump(prediction, body)
            failed = validate_causal_use(prediction, contract)
            self.assertEqual(failed["status"], "FAIL_CLOSED")
            self.assertEqual(failed["score_eligibility"], "PROHIBITED")
            self.assertTrue(any("PROJECT_UPLOAD_REFERENCE_DETECTED" in error for error in failed["errors"]))

    def test_causal_validation_rejects_prompt_snapshot_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            prediction, contract, _, _, _, prompt_text = fixture(Path(directory))
            prompt_text.write_text("MAIN_PROMPT_RUNTIME_ID=MP-R16\nMUTATED\n", encoding="utf-8")
            failed = validate_causal_use(prediction, contract)
            self.assertEqual(failed["status"], "FAIL_CLOSED")
            self.assertIn("MAIN_PROMPT_SNAPSHOT_HASH_MISMATCH", failed["errors"])

    def test_source_packet_rejects_winner_bias(self):
        with tempfile.TemporaryDirectory() as directory:
            _, _, plan, catalog, case, _ = fixture(Path(directory))
            biased = json.loads(plan.read_text())
            biased["top1"] = "A"
            dump(plan, biased)
            with self.assertRaises(FortuneError) as context:
                build_source_packet(catalog, plan, case, Path(directory) / "biased.json")
            self.assertEqual(context.exception.status, "SOURCE_PACKET_ANSWER_ISOLATION_FAILED")

    def test_historical_training_trace_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            prediction, contract, *_ = fixture(Path(directory))
            body = json.loads(prediction.read_text())
            body["legacy_trace"] = "reports/dev-group-002/training-regression-r16/source-excerpts.json"
            dump(prediction, body)
            failed = validate_causal_use(prediction, contract)
            self.assertEqual(failed["status"], "FAIL_CLOSED")
            self.assertEqual(failed["legacy_contamination_scan_status"], "FAIL_CLOSED")
            self.assertTrue(any("LEGACY_CONTAMINATION_REFERENCE_DETECTED" in error for error in failed["errors"]))

    def test_source_packet_rejects_selected_historical_parent_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            _, _, plan, catalog, case, _ = fixture(Path(directory))
            body = json.loads(catalog.read_text())
            selected = next(item for item in body["entries"] if item["library_id"] == "S05" and "alpha" in item["parent_text"])
            selected["parent_text"] += "\nreports/learning-cycle-v2/DEV-GROUP-002/DEV-EXAMPLE-001-Q1/postreveal-review.json\n"
            dump(catalog, body)
            with self.assertRaises(FortuneError) as context:
                build_source_packet(catalog, plan, case, Path(directory) / "contaminated-packet.json")
            self.assertEqual(context.exception.status, "SOURCE_PACKET_LEGACY_CONTAMINATION_DETECTED")

    def test_non_versioned_source_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "reports" / "legacy-sources"
            source.mkdir(parents=True)
            for i in range(20):
                lib = f"S{i:02d}"
                (source / f"{lib}_测试库.txt").write_text(f"LIBRARY_ID={lib}\n", encoding="utf-8")
            with self.assertRaises(FortuneError) as context:
                build_knowledge_manifest(
                    source, Path(directory) / "manifest.json", release_id="BAD",
                    repository="owner/repo", commit_sha="a" * 40,
                    s19_binding_sha256="b" * 64,
                )
            self.assertIn(context.exception.status, {"KNOWLEDGE_SOURCE_PATH_QUARANTINED", "KNOWLEDGE_SOURCE_PATH_INELIGIBLE"})

    def test_runtime_object_validator_classifies_research_and_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime.json"
            dump(path, {
                "source": "research/fortune-hypothesis-library/registry-v1.json",
                "audit": "reports/dev-group-002/training-regression-r18/postreveal-review.json",
            })
            receipt = validate_runtime_object(path)
            self.assertEqual(receipt["status"], "FAIL_CLOSED")
            self.assertEqual(receipt["violation_count"], 2)
            self.assertEqual(classify_repository_path("knowledge/releases/K1/S00_a.txt")["runtime_eligibility"], "ELIGIBLE_WHEN_FROZEN_AND_HASH_BOUND")


if __name__ == "__main__":
    unittest.main()
