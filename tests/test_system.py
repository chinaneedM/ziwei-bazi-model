from __future__ import annotations

import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from fortune_v1.audit import BINDING_HEADER, audit_sources, import_source_package, migrate_verified_sources
from fortune_v1.bazi import freeze_transcription
from fortune_v1.ingest import ingest_zip
from fortune_v1.group import authorize_group_reveal, create_dev_group, record_patch_round
from fortune_v1.knowledge import build_locator_index, read_parent_segment
from fortune_v1.patching import scan_patch
from fortune_v1.prediction import freeze_prediction, prepare_run_contract
from fortune_v1.prompt_snapshot import create_prompt_snapshot
from fortune_v1.regression import execute_regression, select_regression
from fortune_v1.reporting import installation_check
from fortune_v1.scoring import grade_frozen_prediction, literal_replay, minimum_correct
from fortune_v1.snapshot import freeze_static_cache, generate_prediction_snapshot
from fortune_v1.state import transition
from fortune_v1.util import FortuneError, atomic_write_json, read_json, sha256_bytes, sha256_file


def write_json(path: Path, value) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


class FortuneSystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _config(self, expected_hash="0" * 64):
        return {
            "schema_version": "FORTUNE-AUTOMATION-V1",
            "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260715-R16",
            "expected_s19_binding_hash": expected_hash,
            "required_libraries": [f"S{i:02d}" for i in range(20)],
            "knowledge_index_scope": [f"S{i:02d}" for i in range(1, 19)],
            "expected_control_roots": {"S00": "ROOT00", "S01": "ROOT01", "S18": "ROOT18", "S19": "ROOT19"},
        }

    def test_source_audit_and_exact_migration(self):
        source = self.root / "sources"; source.mkdir()
        rows = []
        for i in range(19):
            lib = f"S{i:02d}"
            marker = {"S00": "ROOT00", "S01": "ROOT01", "S18": "ROOT18"}.get(lib, f"PATCH-{lib}")
            body = f"LIBRARY_ID={lib}\nPATCH_ID={marker}\n正文{i}\n".encode()
            name = f"{lib}_source.txt"
            path = source / name; path.write_bytes(body)
            rows.append(f"{lib}\tFILE-{lib}\t{name}\t{sha256_bytes(body)}\t{len(body)}")
        block = BINDING_HEADER + "\n" + "\n".join(rows) + "\n"
        binding_hash = sha256_bytes(block.encode())
        s19 = (f"LIBRARY_ID=S19\nPATCH_ID=ROOT19\nACTIVE_BINDING_TABLE_SHA256_UTF8_LF={binding_hash}\n"
               f"ACTIVE_BINDING_TABLE_HASH_METHOD=SHA256_OF_HEADER_AND_S00_TO_S18_ROWS_UTF8_LF_TRAILING_LF\n"
               f"{block}")
        (source / "S19_source.txt").write_text(s19, encoding="utf-8")
        config = self._config(binding_hash); config_path = write_json(self.root / "config.json", config)
        report = audit_sources(source, config_path, self.root / "audit.json")
        self.assertEqual(report["status"], "PASS")
        manifest = migrate_verified_sources(self.root / "audit.json", self.root / "base")
        self.assertEqual(len(manifest["files"]), 20)
        for item in manifest["files"]:
            self.assertEqual(sha256_file(item["path"]), item["sha256"])

    def test_duplicate_and_missing_source_hold(self):
        source = self.root / "sources"; source.mkdir()
        (source / "transport(8).txt").write_text("LIBRARY_ID=S02\na", encoding="utf-8")
        (source / "transport(9).txt").write_text("LIBRARY_ID=S02\nb", encoding="utf-8")
        config_path = write_json(self.root / "config.json", self._config())
        report = audit_sources(source, config_path, self.root / "audit.json")
        self.assertEqual(report["status"], "HOLD_SOURCE_BASELINE_UNVERIFIED")
        self.assertIn("S00", report["missing"])
        self.assertIn("S02", report["duplicates"])
        with self.assertRaises(FortuneError):
            migrate_verified_sources(self.root / "audit.json", self.root / "base")

    def test_source_package_identity_ignores_transport_suffix_and_quarantines_old_version(self):
        source_bytes, rows, manifest_rows = {}, [], []
        for i in range(19):
            lib = f"S{i:02d}"
            marker = {"S00": "ROOT00", "S01": "ROOT01", "S18": "ROOT18"}.get(lib, f"PATCH-{lib}")
            body = f"LIBRARY_ID={lib}\nPATCH_ID={marker}\n正文{i}\n".encode()
            canonical = f"{lib}_canonical.txt"
            source_bytes[lib] = body
            rows.append(f"{lib}\tFILE-{lib}\t{canonical}\t{sha256_bytes(body)}\t{len(body)}")
            manifest_rows.append({"library_id": lib, "canonical_filename": canonical,
                                  "sha256": sha256_bytes(body), "size_bytes": len(body)})
        block = BINDING_HEADER + "\n" + "\n".join(rows) + "\n"
        binding_hash = sha256_bytes(block.encode())
        s19 = (f"LIBRARY_ID=S19\nPATCH_ID=ROOT19\nACTIVE_BINDING_TABLE_SHA256_UTF8_LF={binding_hash}\n"
               f"ACTIVE_BINDING_TABLE_HASH_METHOD=SHA256_OF_HEADER_AND_S00_TO_S18_ROWS_UTF8_LF_TRAILING_LF\n{block}").encode()
        manifest_rows.append({"library_id": "S19", "canonical_filename": "S19_canonical.txt",
                              "sha256": sha256_bytes(s19), "size_bytes": len(s19)})
        package = self.root / "transport-name(42).zip"
        with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
            for lib, body in source_bytes.items():
                suffix = "(9)" if lib == "S02" else "(17)"
                archive.writestr(f"sources/{lib}_upload{suffix}.txt", body)
            old = b"LIBRARY_ID=S02\nPATCH_ID=OLD\nold"
            archive.writestr("sources/S02_upload(8).txt", old)
            archive.writestr("sources/S19_upload(59).txt", s19)
            archive.writestr("source-baseline-manifest.json", json.dumps({
                "files": manifest_rows, "excluded_or_quarantined": []}, ensure_ascii=False))
            archive.writestr("README.txt", "synthetic")
        config = self._config(binding_hash)
        config_path = write_json(self.root / "source-config.json", config)
        result = import_source_package(package, sha256_file(package), config_path,
                                       self.root / "import", self.root / "reports", self.root / "base")
        self.assertEqual(result["status"], "PASS")
        normalized = read_json(self.root / "reports" / "normalization-map.json")
        s02 = next(row for row in normalized["files"] if row["library_id"] == "S02")
        self.assertEqual(s02["canonical_filename"], "S02_canonical.txt")
        quarantine = read_json(self.root / "reports" / "duplicate-and-quarantine-report.json")
        self.assertEqual(quarantine["quarantined_or_historical"][0]["status"], "HISTORICAL_AUDIT_ONLY")

    def _make_zip(self) -> Path:
        package = self.root / "group.zip"
        questions = "题目1：性情？\nA. 甲\nB. 乙\nC. 丙\nD. 丁\n题目2：事业？\nA. 一\nB. 二\nC. 三\nD. 四\n"
        with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("C001_紫微.txt", "紫微文字盘，不含揭盲内容")
            z.writestr("C001_八字.png", b"\x89PNG\r\n\x1a\nSYNTHETIC")
            z.writestr("C001_题目.txt", questions)
            z.writestr("C001_答案.txt", "A,B")
            z.writestr("C001_备注.txt", "合成客观备注")
        return package

    def _transcription(self, runtime: Path) -> Path:
        image = next((runtime / "cases" / "DEV" / "C001" / "input" / "bazi_image").iterdir())
        fields = {
            "solar_term_pillars": {"value": ["甲子", "乙丑", "丙寅", "丁卯"], "state": "VERIFIED"},
            "hidden_stems": {"value": {}, "state": "VERIFIED"},
            "ten_gods": {"value": {}, "state": "VERIFIED"},
            "start_luck_age": {"value": 6, "state": "VERIFIED"},
            "handover_time": {"value": "2000-01-01", "state": "VERIFIED"},
            "major_luck_cycles": {"value": ["戊辰"], "state": "VERIFIED"},
        }
        source = write_json(self.root / "transcription-input.json", {"versions": [{"version_id": "V1", "fields": fields}]})
        output = self.root / "transcription.json"
        result = freeze_transcription("C001", image, source, output)
        self.assertEqual(result["overall_status"], "VALID")
        return output

    def _run_question(self, qid, options, top1, top2):
        evidence = [{"evidence_family": f"F{i}", "text": f"e{i}"} for i in range(1, 4)]
        ledger = []
        for i, lib in enumerate(["S05", "S08", "S11"], 1):
            ledger.append({"track": "ZIWEI" if i < 3 else "BAZI", "source_library": lib, "method": "M", "knowledge_point": f"K{i}",
                           "source_root_atom": "R", "parent_segment": "P", "physical_selector": "S", "conditions": [],
                           "limitations_negations_exceptions": [], "target_atom": "T", "semantic_direction": "SUPPORT",
                           "capability_ceiling": "RELATIVE", "temporal_role": "STATIC", "evidence_family": f"F{i}",
                           "dedup_status": "UNIQUE", "downstream_effect": "CHANGED_RANK"})
        pairwise = []
        for i, left in enumerate(options):
            for right in options[i + 1:]: pairwise.append({"left": left, "right": right, "winner": top1 if top1 in {left, right} else left, "comparison": "literal"})
        return {"question_id": qid, "option_ids": options, "top1": top1, "top2": top2, "confidence": 0.65,
                "blind_core": "sealed blind structure", "public_evidence": evidence, "strongest_competitor_reason": "less coverage",
                "most_important_unverified_atom": "formal endpoint", "ziwei_track": {"validation_status": "PASS", "local_seal": True,
                "parent_libraries": ["S05", "S08"], "blind_model_hash": "z" * 64, "top1": top1},
                "bazi_track": {"validation_status": "PASS", "local_seal": True, "parent_libraries": ["S11", "S13"],
                "blind_model_hash": "b" * 64, "top1": top1}, "fusion": {"status": "ZERO_GAIN_SAME_SELECTION"},
                "coverage_plan": {"required_families": ["stable", "dynamic", "endpoint"], "status": "COMPLETE"},
                "evidence_ledger": ledger, "direction_matrix": {o: {"support": [], "contradict": []} for o in options},
                "compound_coverage": {o: {"status": "CHECKED"} for o in options}, "formal_exact_assertion": None,
                "pairwise_rows": pairwise}

    def test_synthetic_end_to_end_and_answer_isolation(self):
        runtime, vault = self.root / "runtime", self.root / "vault"
        receipt = ingest_zip(self._make_zip(), runtime, vault, "DEV")
        self.assertEqual(receipt["status"], "PASS")
        self.assertTrue(receipt["raw_package_read_only"])
        runtime_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in runtime.rglob("*") if p.is_file())
        self.assertNotIn("A,B", runtime_text)
        answer_path = vault / "answers" / "C001" / "answer.txt"
        self.assertTrue(answer_path.exists())
        transcription = self._transcription(runtime)
        normalized = runtime / "cases" / "DEV" / "C001" / "normalized-case.json"
        snapshot = generate_prediction_snapshot(normalized, self.root / "snapshots", transcription)
        self.assertEqual(snapshot["answer_scan"]["status"], "PASS")
        config = self._config("1" * 64); config_path = write_json(self.root / "runtime.json", config)
        contract_path = self.root / "contract.json"
        contract = prepare_run_contract(Path(self.root / "snapshots" / snapshot["snapshot_id"] / "manifest.json"), config_path, "abc123", contract_path)
        run = {"schema": "PREDICTION-RUN-V1", "run_id": "RUN-C001-001", "case_id": "C001", "dataset_type": "DEV",
               "binding": contract["binding"], "input_snapshot": {"path": contract["snapshot"]["path"], "sha256": contract["snapshot"]["sha256"]},
               "questions": [self._run_question("Q1", ["A", "B", "C", "D"], "A", "B"), self._run_question("Q2", ["A", "B", "C", "D"], "B", "A")],
               "runtime_validation": {"status": "PASS", "checks": []}, "cold_start": True}
        run_path = write_json(self.root / "run.json", run)
        frozen = freeze_prediction(run_path, contract_path, self.root / "frozen")
        with self.assertRaises(FortuneError): freeze_prediction(run_path, contract_path, self.root / "frozen")
        gates = {key: True for key in ["answer_isolation", "cold_start", "runtime_object_complete", "dual_track_independent", "patch_leak_free", "historical_regression_no_damage"]}
        reveal = grade_frozen_prediction(self.root / "frozen" / "RUN-C001-001" / "freeze-receipt.json", answer_path, self.root / "reveal.json", gates)
        self.assertEqual(reveal["status"], "CASE_PASS")
        self.assertEqual(reveal["score"]["top1_correct"], 2)
        self.assertFalse(reveal["score"]["top2_is_formal_score"])

    def test_grade_before_freeze_is_blocked(self):
        fake = write_json(self.root / "fake.json", {"schema": "not-freeze"})
        answer = self.root / "a.txt"; answer.write_text("A", encoding="utf-8")
        with self.assertRaises(FortuneError) as ctx:
            grade_frozen_prediction(fake, answer, self.root / "out.json")
        self.assertEqual(ctx.exception.status, "GRADING_BEFORE_FREEZE_BLOCKED")

    def test_literal_replay_and_thresholds(self):
        answer = self.root / "answer.txt"; answer.write_text(" A，B / C \n", encoding="utf-8")
        replay = literal_replay(answer, [["A", "B"], ["A", "B"], ["A", "B", "C"]])
        self.assertEqual(replay["parser_a"], ["A", "B", "C"])
        self.assertEqual(replay["parser_a"], replay["parser_b"])
        self.assertEqual([minimum_correct(i) for i in [1, 4, 5, 6, 10]], [1, 4, 4, 5, 8])

    def test_static_cache_invalidation_key(self):
        manifest = write_json(self.root / "snapshot.json", {"case_id": "C", "case_input_hash": "a" * 64})
        ziwei = {k: {} for k in ["twelve_palaces", "base_chart_id", "sixty_star_system", "borrowed_stars", "opposite_and_trines", "stable_natures", "birth_transformations", "palace_stem_transformations", "self_transformations_and_lines", "person_coordinates"]}
        bazi = {k: {} for k in ["solar_term_versions", "hidden_stems_ten_gods", "month_command_roots_qi", "relation_graph", "method_competition", "luck_coordinates"]}
        obj = write_json(self.root / "static.json", {"ziwei": ziwei, "bazi": bazi})
        one = freeze_static_cache(manifest, obj, "1" * 64, "V1", self.root / "cache")
        two = freeze_static_cache(manifest, obj, "2" * 64, "V1", self.root / "cache")
        self.assertNotEqual(one["cache_key"], two["cache_key"])

    def test_knowledge_index_reads_exact_parent_and_excludes_s19(self):
        sources = self.root / "base"; sources.mkdir()
        (sources / "S01.txt").write_text("根原子。若条件成立；不得越级。\n\n另一段，否则替代。\n", encoding="utf-8")
        (sources / "S19.txt").write_text("governance", encoding="utf-8")
        index = build_locator_index(sources, "f" * 64, self.root / "index.json", "commit1")
        self.assertFalse(index["s19_indexed"])
        self.assertTrue(all(e["library_id"] != "S19" for e in index["entries"]))
        parent = read_parent_segment(self.root / "index.json", index["entries"][0]["entry_id"])
        self.assertIn("不得越级", parent["text"])
        self.assertEqual(parent["source_git_commit"], "commit1")

    def test_patch_leak_scan(self):
        clean = write_json(self.root / "clean.json", {"universal_parent_chain": [{"source": "S18", "rule": "generic"}], "changes": [{"rule": "validate pairwise count"}]})
        result = scan_patch(clean, self.root / "clean-scan.json")
        self.assertEqual(result["status"], "PASS")
        leaky = self.root / "leaky.txt"; leaky.write_text("这个案例优先选A CASE-20260715-SECRET", encoding="utf-8")
        result = scan_patch(leaky, self.root / "leaky-scan.json")
        self.assertEqual(result["status"], "PATCH_REJECTED_CASE_SPECIFIC")

    def test_regression_without_runner_holds_and_state_machines_isolate(self):
        manifest = write_json(self.root / "reg.json", {"current_dev_group": "G1", "cases": [{"case_id": "C1", "role": "DEFECT_REPRODUCTION", "dataset_type": "DEV", "group": "G1", "tags": ["time"], "previous_status": "FAIL", "core": True}]})
        selection = select_regression(manifest, ["time"], full=True)
        result = execute_regression(selection, None, "cand", "base", self.root / "reg-out.json")
        self.assertEqual(result["decision"], "GROUP_HOLD")
        log = self.root / "state.json"
        transition(log, "DEV", "G1", "INGESTED")
        transition(log, "FROZEN_EVAL", "B1", "FROZEN_BLOCK_OPEN")
        with self.assertRaises(FortuneError): transition(log, "DEV", "G1", "RUNNING")

    def test_prompt_snapshot_is_not_runtime_authority(self):
        prompt = self.root / "prompt.txt"; prompt.write_text("exact audit text", encoding="utf-8")
        result = create_prompt_snapshot("MP-X", prompt, self.root / "prompt-snapshot")
        self.assertEqual(result["authority_statement"], "AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY")

    def test_dev_group_blocks_early_reveal_and_stop_policy(self):
        binding = {"library_binding_hash": "a" * 64, "main_prompt_runtime_id": "MP", "prompt_snapshot_sha256": None, "code_commit": "c", "schema_version": "V1"}
        create_dev_group("G1", ["C1", "C2", "C3", "C4", "C5"], binding, self.root / "groups")
        group_root = self.root / "groups" / "G1"
        with self.assertRaises(FortuneError) as ctx:
            authorize_group_reveal(group_root)
        self.assertEqual(ctx.exception.status, "GROUP_REVEAL_BEFORE_ALL_BASELINES_BLOCKED")
        one = record_patch_round(group_root, 0, 0, "D1")
        self.assertEqual(one["status"], "RETESTING")
        two = record_patch_round(group_root, 0, 0, "D1")
        self.assertEqual(two["status"], "GROUP_HOLD")
        self.assertIn("NO_IMPROVEMENT_LIMIT", two["hold_reasons"])


if __name__ == "__main__":
    unittest.main()
