from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"
TEMPORAL_AUX = ROOT / "src" / "fortune_training" / "ziwei_chart" / "temporal_auxiliary.py"


class HistoricalProvenanceAuditMatrixR1Test(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.rows = self.payload["rows"]

    def test_inventory_is_broad_and_unique(self) -> None:
        self.assertGreaterEqual(len(self.rows), 100)
        ids = [row["rule_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for module in (
            "Time / Calendar", "四柱本命", "八字派生字段", "大运", "小运", "神煞",
            "八字动态时限", "紫微本命", "十二宫", "主星", "辅星", "杂曜", "四化",
            "庙旺落陷", "大限", "流年", "流月", "流日", "流时", "动态辅助星",
            "Structural R1–R8", "Combined Fusion", "candidate/profile rules",
            "provenance / hashes / lineage",
        ):
            self.assertIn(module, {row["module"] for row in self.rows})

    def test_closed_product_and_unformalized_direction_are_preserved(self) -> None:
        self.assertEqual(self.payload["deterministic_product_state"], "CLOSED")
        self.assertEqual(self.payload["self_inward_transformation_state"], "NOT_YET_FORMALIZED")
        self.assertTrue(all(row["algorithm_reopen_authorized"] is False for row in self.rows))
        row = next(row for row in self.rows if row["rule_id"] == "HPA-ZT-016")
        self.assertEqual(row["audit_status"], "NOT_YET_FORMALIZED")

    def test_modern_compatibility_is_not_historical_authority(self) -> None:
        self.assertEqual(
            self.payload["external_reference_policy"],
            "WENMO_WENZHEN_COMPATIBILITY_ONLY_NOT_HISTORICAL_AUTHORITY",
        )
        modern = [row for row in self.rows if row["audit_status"] == "MODERN_COMPATIBILITY_ONLY"]
        self.assertTrue(modern)

    def test_machine_gate_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/verify-fusion-chart-historical-provenance-audit-r1.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        receipt = json.loads(completed.stdout)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["row_count"], len(self.rows))
        self.assertEqual(receipt["algorithm_reopen_authorized_count"], 0)
        self.assertGreaterEqual(receipt["historical_research_batch_count"], 1)
        self.assertGreaterEqual(receipt["historical_research_batch_count"], 15)
        self.assertGreaterEqual(receipt["audited_row_count"], 136)
        self.assertEqual(receipt["confirmed_chart_algorithm_defect_count"], 0)
        self.assertGreaterEqual(receipt["confirmed_provenance_metadata_defect_count"], 7)
        self.assertGreaterEqual(receipt["repaired_provenance_metadata_defect_count"], 7)
        self.assertGreaterEqual(receipt["historical_candidate_registry_count"], 1)
        self.assertGreaterEqual(receipt["historical_candidate_runtime_resolver_count"], 1)
        self.assertGreaterEqual(receipt["identified_missing_candidate_family_count"], 8)

    def test_batch_07b_early_print_minor_rows_are_closed_without_reopen(self) -> None:
        expected = {f"HPA-ZMINOR-{index:03d}" for index in range(9, 20)}
        by_id = {row["rule_id"]: row for row in self.rows}
        self.assertTrue(expected.issubset(by_id))
        for rule_id in expected:
            row = by_id[rule_id]
            self.assertEqual(row["audit_batch"], "BATCH-07-ZIWEI-MINOR-STARS-B")
            self.assertEqual(row["audit_status"], "HISTORICALLY_SUPPORTED")
            self.assertFalse(row["algorithm_reopen_authorized"])
            self.assertIn("EXT-ZIWEI-JIELAN-1581", row["primary_source"])
        xunkong = by_id["HPA-ZMINOR-011"]
        self.assertIn("PRIMARY_SECONDARY_DISPLAY_ORDER_NOT_UPGRADED", xunkong["current_implementation_match"])
        xianchi = by_id["HPA-ZMINOR-016"]
        self.assertIn("LABEL_IS_A_DOCUMENTED_NORMALIZATION_BRIDGE", xianchi["current_implementation_match"])

    def test_batch_07c_completes_minor_star_family_decomposition(self) -> None:
        expected = {f"HPA-ZMINOR-{index:03d}" for index in range(20, 27)}
        by_id = {row["rule_id"]: row for row in self.rows}
        self.assertTrue(expected.issubset(by_id))
        self.assertEqual(by_id["HPA-ZMINOR-021"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-ZMINOR-022"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        for rule_id in ("HPA-ZMINOR-020", "HPA-ZMINOR-023", "HPA-ZMINOR-024", "HPA-ZMINOR-025", "HPA-ZMINOR-026"):
            self.assertEqual(by_id[rule_id]["audit_status"], "SOURCE_INSUFFICIENT")
            self.assertFalse(by_id[rule_id]["algorithm_reopen_authorized"])
        parent = by_id["HPA-ZIWEI-008"]
        self.assertEqual(parent["audit_status"], "SOURCE_INSUFFICIENT")
        self.assertIn("FULLY_DECOMPOSED", parent["current_implementation_match"])

    def test_batch_08a_dynamic_auxiliary_authority_is_scoped(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        expected = {f"HPA-ZAUX-{index:03d}" for index in range(1, 9)}
        self.assertTrue(expected.issubset(by_id))
        self.assertEqual(by_id["HPA-ZAUX-001"]["audit_status"], "HISTORICALLY_SUPPORTED")
        for rule_id in ("HPA-ZAUX-002", "HPA-ZAUX-003", "HPA-ZAUX-004", "HPA-ZAUX-005", "HPA-ZAUX-007", "HPA-ZAUX-008"):
            self.assertEqual(by_id[rule_id]["audit_status"], "SUPPORTED_BUT_SCHOOL_SPECIFIC")
        self.assertEqual(by_id["HPA-ZAUX-006"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertEqual(by_id["HPA-ZT-011"]["defect_id"], "PROV-DEFECT-007")
        source = TEMPORAL_AUX.read_text(encoding="utf-8")
        self.assertNotIn('authority_status="CANONICAL_SOURCE_TABLE"', source)
        self.assertIn('authority_status="S01_STRICT_PROJECT_CORPUS_METHOD"', source)
        self.assertIn('TEMPORAL_KUI_YUE_ALGORITHM_VERSION = "1.0.1"', source)
        self.assertIn('TEMPORAL_AUXILIARY_CANDIDATE_SET_HASH_VERSION = "1.2.0"', source)

    def test_batch_08b_temporal_philology_preserves_distinct_mechanics(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        expected = {f"HPA-ZTEMP-{index:03d}" for index in range(1, 7)}
        self.assertTrue(expected.issubset(by_id))
        for rule_id in ("HPA-ZTEMP-001", "HPA-ZTEMP-002", "HPA-ZTEMP-003"):
            self.assertEqual(by_id[rule_id]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-ZTEMP-004"]["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertEqual(by_id["HPA-ZTEMP-005"]["audit_status"], "SUPPORTED_BUT_SCHOOL_SPECIFIC")
        self.assertEqual(by_id["HPA-ZTEMP-006"]["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertEqual(by_id["HPA-ZT-015"]["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertEqual(by_id["HPA-ZT-014"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")

    def test_batch_08c_time_standards_are_not_conflated(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        self.assertEqual(by_id["HPA-ZTIME-001"]["audit_status"], "SUPPORTED_BUT_SCHOOL_SPECIFIC")
        self.assertEqual(by_id["HPA-ZTIME-002"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertEqual(by_id["HPA-TIME-003"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertIn("NO_EQUATION_OF_TIME_IS_ADDED", by_id["HPA-ZTIME-001"]["current_implementation_match"])
        self.assertIn("ASTRONOMICAL_DEFINITION_MATCH", by_id["HPA-ZTIME-002"]["current_implementation_match"])
        self.assertEqual(by_id["HPA-ZT-014"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")

    def test_batch_08d_date_index_and_late_zi_are_separate_axes(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        expected = {f"HPA-ZDATE-{index:03d}" for index in range(1, 6)}
        self.assertTrue(expected.issubset(by_id))
        self.assertEqual(by_id["HPA-TIME-009"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        self.assertEqual(by_id["HPA-ZDATE-001"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertEqual(by_id["HPA-ZDATE-002"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertEqual(by_id["HPA-ZDATE-003"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        self.assertEqual(by_id["HPA-ZDATE-004"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertIn("Jielan", by_id["HPA-TIME-009"]["proposed_action"])
        self.assertIn("INDEPENDENCE_TESTED", by_id["HPA-ZDATE-005"]["current_implementation_match"])

    def test_batch_09a_astronomy_and_bazi_doctrine_are_separate(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        expected = {f"HPA-BTIME-{index:03d}" for index in range(1, 5)}
        self.assertTrue(expected.issubset(by_id))
        self.assertEqual(by_id["HPA-TIME-005"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertEqual(by_id["HPA-TIME-006"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BTIME-001"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        for rule_id in ("HPA-BTIME-002", "HPA-BTIME-003", "HPA-BTIME-004"):
            self.assertEqual(by_id[rule_id]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertIn("HALF_OPEN_INSTANT_BOUNDARY_MATCH", by_id["HPA-BTIME-004"]["current_implementation_match"])

    def test_batch_09b_dayun_sequence_closes_without_jiaoyun_reopen(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        self.assertEqual(by_id["HPA-DAYUN-004"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertIn("first formal Dayun", by_id["HPA-DAYUN-004"]["current_implementation_match"])
        for rule_id in ("HPA-DAYUN-SEQ-001", "HPA-DAYUN-SEQ-002"):
            self.assertEqual(by_id[rule_id]["audit_status"], "HISTORICALLY_SUPPORTED")
            self.assertFalse(by_id[rule_id]["algorithm_reopen_authorized"])
        self.assertIn("EXACT_ADJACENT_FIRST_STEP_MATCH", by_id["HPA-DAYUN-SEQ-001"]["current_implementation_match"])
        self.assertIn("EXACT_MOD60_STEP_SEQUENCE_MATCH", by_id["HPA-DAYUN-SEQ-002"]["current_implementation_match"])

    def test_readme_and_ci_bind_the_audit_stage(self) -> None:
        readme = README.read_text(encoding="utf-8")
        ci = CI.read_text(encoding="utf-8")
        self.assertIn("FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS", readme)
        self.assertIn("HISTORICAL_PROVENANCE_INVENTORY=COMPLETE", readme)
        self.assertIn("DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED", readme)
        self.assertIn("ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED", readme)
        self.assertIn("verify-fusion-chart-historical-provenance-audit-r1.py", ci)
        self.assertIn("test_fusion_chart_historical_provenance_audit_matrix_r1.py", ci)


if __name__ == "__main__":
    unittest.main()
