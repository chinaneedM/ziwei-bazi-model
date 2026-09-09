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
BAZI_RELATION_CANDIDATES = ROOT / "src" / "fortune_training" / "bazi_chart" / "historical_relation_candidates.py"
BAZI_TEMPORAL_ANNOTATIONS = ROOT / "src" / "fortune_training" / "bazi_application" / "temporal_annotations.py"
HISTORICAL_CALENDAR_CONTRACT = ROOT / "src" / "fortune_training" / "historical_calendar" / "contract.py"


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
        self.assertGreaterEqual(receipt["historical_research_batch_count"], 21)
        self.assertGreaterEqual(receipt["audited_row_count"], 165)
        self.assertEqual(receipt["confirmed_chart_algorithm_defect_count"], 0)
        self.assertGreaterEqual(receipt["confirmed_provenance_metadata_defect_count"], 10)
        self.assertGreaterEqual(receipt["repaired_provenance_metadata_defect_count"], 10)
        self.assertGreaterEqual(receipt["historical_candidate_registry_count"], 2)
        self.assertGreaterEqual(receipt["historical_candidate_runtime_resolver_count"], 2)
        self.assertGreaterEqual(receipt["identified_missing_candidate_family_count"], 13)

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
        self.assertEqual(by_id["HPA-ZTEMP-004"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-ZTEMP-005"]["audit_status"], "SUPPORTED_BUT_SCHOOL_SPECIFIC")
        self.assertEqual(by_id["HPA-ZTEMP-006"]["audit_status"], "SUPPORTED_BUT_SCHOOL_SPECIFIC")
        self.assertEqual(
            by_id["HPA-ZTEMP-004"]["selection_status"],
            "PRESERVED_NOT_SELECTED",
        )
        self.assertEqual(
            by_id["HPA-ZTEMP-006"]["selection_status"],
            "PRESERVED_NOT_SELECTED",
        )
        self.assertEqual(
            by_id["HPA-ZTEMP-004"]["candidate_method_id"],
            "JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1",
        )
        self.assertEqual(
            by_id["HPA-ZTEMP-006"]["candidate_method_id"],
            "ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1",
        )
        self.assertIn(
            "ZHONGZHOU_FIXED_BRANCH_CASE_REMAINS_SEPARATE",
            by_id["HPA-ZTEMP-004"]["current_implementation_match"],
        )
        self.assertIn(
            "DAILY_ACTIVE_ADDRESS_NOT_EMITTED",
            by_id["HPA-ZTEMP-006"]["current_implementation_match"],
        )
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

    def test_batch_10a_raw_relations_and_affinity_preserve_philology(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        expected = {"HPA-BAFF-001", "HPA-BAFF-002"} | {f"HPA-BREL-{index:03d}" for index in range(1, 8)}
        self.assertTrue(expected.issubset(by_id))
        self.assertEqual(by_id["HPA-BAZI-004"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BAZI-013"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BAZI-005"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        for rule_id in ("HPA-BREL-001", "HPA-BREL-002", "HPA-BREL-003", "HPA-BREL-004", "HPA-BREL-005", "HPA-BREL-006"):
            self.assertEqual(by_id[rule_id]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BREL-007"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertIn("LIUHAI_ALIAS_RECORDED_IN_PROVENANCE_ONLY", by_id["HPA-BREL-004"]["current_implementation_match"])
        self.assertIn("RUNTIME_AVOIDS_DISPUTED_CATEGORY_LABELS", by_id["HPA-BREL-006"]["current_implementation_match"])
        self.assertIn("arity-4", by_id["HPA-BREL-007"]["current_implementation"])

    def test_batch_10b_excluded_relations_preserve_source_scope(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        expected = {f"HPA-BREL-{index:03d}" for index in range(8, 13)}
        self.assertTrue(expected.issubset(by_id))
        for rule_id in ("HPA-BREL-008", "HPA-BREL-009", "HPA-BREL-012"):
            self.assertEqual(by_id[rule_id]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BREL-010"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        self.assertEqual(by_id["HPA-BREL-011"]["audit_status"], "MODERN_COMPATIBILITY_ONLY")
        self.assertIn("DIFFERENT_WORDING_SAME_MECHANICAL_RULE", by_id["HPA-BREL-008"]["school_attribution"])
        self.assertIn("EARLY_FOUR_BREAK_METHOD", by_id["HPA-BREL-009"]["school_attribution"])
        self.assertIn("same-pillar", by_id["HPA-BREL-012"]["rule_or_field"].lower())

    def test_batch_10c_productizes_candidates_without_core_mutation(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        for rule_id in ("HPA-BREL-007", "HPA-BREL-008", "HPA-BREL-009", "HPA-BREL-012"):
            self.assertEqual(by_id[rule_id]["audit_status"], "HISTORICALLY_SUPPORTED")
            self.assertIn("PRESERVED_NOT_SELECTED", by_id[rule_id]["current_profile"])
        self.assertEqual(by_id["HPA-BAZI-005"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        self.assertEqual(by_id["HPA-BCAND-001"]["audit_status"], "DISPUTED_MULTIPLE_CANDIDATES")
        self.assertEqual(by_id["HPA-BREL-012"]["defect_id"], "PROV-DEFECT-008")
        self.assertEqual(by_id["HPA-BREL-012"]["repair_status"], "REPAIRED_FORWARD_ONLY_DURING_BATCH_10C")
        source = BAZI_RELATION_CANDIDATES.read_text(encoding="utf-8")
        self.assertIn("PRESERVED_NOT_SELECTED", source)
        self.assertIn("FOUR_EARTH_BUREAU", source)
        self.assertIn("BRANCH_BREAK_EARLY_FOUR", source)
        self.assertIn("STEM_HIDDEN_COMBINATION", source)

    def test_batch_11a_hidden_stem_order_is_lineage_not_strength(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        self.assertEqual(by_id["HPA-BHIDDEN-001"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BHIDDEN-002"]["audit_status"], "SOURCE_INSUFFICIENT")
        self.assertEqual(by_id["HPA-BHIDDEN-003"]["audit_status"], "SUPPORTED_BUT_SCHOOL_SPECIFIC")
        self.assertEqual(by_id["HPA-BAZI-015"]["audit_status"], "SOURCE_INSUFFICIENT")
        self.assertIn("FULLY_DECOMPOSED", by_id["HPA-BAZI-015"]["current_implementation_match"])
        self.assertEqual(by_id["HPA-BAZI-FLOW-003"]["audit_status"], "HISTORICALLY_SUPPORTED")
        self.assertEqual(by_id["HPA-BAZI-FLOW-003"]["defect_id"], "PROV-DEFECT-009")
        self.assertEqual(by_id["HPA-BAZI-FLOW-003"]["repair_status"], "REPAIRED_FORWARD_ONLY_DURING_BATCH_11A")
        source = BAZI_TEMPORAL_ANNOTATIONS.read_text(encoding="utf-8")
        self.assertIn('TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION = "1.0.2"', source)
        self.assertIn('TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION = "1.0.1"', source)
        self.assertIn('"hidden_stem_registry_order"', source)

    def test_batch_11c_historical_calendar_contract_stays_fail_closed(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        for rule_id in ("HPA-DAYUN-CAL-002", "HPA-DAYUN-CAL-003", "HPA-DAYUN-CAL-004"):
            self.assertEqual(by_id[rule_id]["audit_status"], "MISSING_FROM_PRODUCT")
            self.assertEqual(
                by_id[rule_id]["adapter_contract_id"],
                "HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1",
            )
        self.assertIn("MING_DATONG", by_id["HPA-DAYUN-CAL-002"]["calendar_regime_context"])
        source = HISTORICAL_CALENDAR_CONTRACT.read_text(encoding="utf-8")
        self.assertIn("MING-DATONG-CALENDAR-CONTEXT-R1", source)
        self.assertIn("QING-SHIXIAN-1645-CALENDAR-CONTEXT-R1", source)
        self.assertIn("MODERN_CHINESE_CALENDAR_FALLBACK_FORBIDDEN", source)


    def test_batch_12ac_pt165_page_object_is_not_glyph_authority(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertEqual(
            row["batch_12ac_wenguang_pt165_public_viewer_response_artifact"],
            "docs/research/ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-R1.json",
        )
        self.assertEqual(
            row["wenguang_pt165_click3_target_record"],
            {"pid": "PT165", "flags": 8, "order": 165},
        )
        self.assertEqual(row["wenguang_pt165_click3_returned_page_record_count"], 209)
        self.assertEqual(row["wenguang_pt165_click3_source_emitted_image_url_count"], 0)
        self.assertFalse(row["wenguang_pt165_direct_target_image_observed_batch_12ac"])
        self.assertTrue(row["wenguang_pt165_page_object_is_not_glyph_authority"])
        self.assertEqual(row["independent_textual_witness_count_added_batch_12ac"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12ac"], 0)
        self.assertFalse(row["algorithm_reopen_authorized"])

    def test_batch_12ag_jiaojingshanfang_is_provenance_only(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertEqual(
            row["batch_12ag_jiaojingshanfang_hanauction_physical_edition_artifact"],
            "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json",
        )
        self.assertEqual(row["jiaojingshanfang_hanauction_exact_stable_object_ids"], ["101926", "27427"])
        self.assertEqual(
            row["jiaojingshanfang_2012_detail_photo_visual_review_status"],
            "DIRECTLY_REVIEWED_AND_RECLASSIFIED_AS_AUCTION_EVENT_MEDIA_NOT_TARGET_OBJECT",
        )
        self.assertEqual(row["jiaojingshanfang_target_page_status"], "PENDING_DIRECT_VISUAL_TARGET_PAGE")
        self.assertEqual(row["independent_textual_witness_count_added_batch_12ag"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12ag"], 0)
        self.assertFalse(row["algorithm_reopen_authorized"])


    def test_batch_12ah_jiaojingshanfang_event_media_scope_is_repaired(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(
            row["batch_12ah_jiaojingshanfang_detail_photo_visual_adjudication_artifact"],
            "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-R1.json",
        )
        self.assertEqual(row["defect_id"], "PROV-DEFECT-010")
        self.assertEqual(row["defect_type"], "EVIDENCE_SCOPE_MISCLASSIFICATION")
        self.assertEqual(row["repair_status"], "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AH")
        self.assertEqual(
            row["jiaojingshanfang_2012_detail_photo_context_status"],
            "AUCTION_ROUND_EVENT_SCENERY_MEDIA_NOT_LOT_173_OBJECT_PHOTOS",
        )
        self.assertEqual(row["independent_textual_witness_count_added_batch_12ah"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12ah"], 0)
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["algorithm_reopen_authorized"])


    def test_batch_12ai_ziwei_late_zi_time_coordinate_is_narrowed_not_selected(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(
            row["batch_12ai_ziwei_late_zi_time_coordinate_artifact"],
            "docs/research/ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json",
        )
        self.assertEqual(row["historical_time_coordinate_family"], "LOCAL_OBSERVATIONAL_ASTRONOMICAL_TIME_COORDINATE")
        self.assertEqual(row["historical_daytime_time_basis"], "SUNDIAL_TRUE_SUN")
        self.assertEqual(row["historical_nighttime_time_basis"], "STELLAR_TIME_READING_WITH_CLEPSYDRA_AS_SUPPLEMENT")
        self.assertEqual(row["historical_clock_geographic_dependence"], "DIRECTLY_ATTESTED")
        self.assertEqual(
            row["local_apparent_solar_time_historical_binding"],
            "STRONGEST_MODERN_DAYTIME_TRANSLATION_NOT_NATAL_RUNTIME_WINNER",
        )
        self.assertEqual(row["historical_nighttime_to_runtime_apparent_solar_equivalence"], "UNRESOLVED")
        self.assertEqual(row["natal_birthplace_time_coordinate_binding"], "UNRESOLVED")
        self.assertEqual(row["runtime_time_standard_binding_status_batch_12ai"], "PARTIALLY_NARROWED_NOT_CLOSED")
        self.assertFalse(row["candidate_selected_batch_12ai"])
        self.assertFalse(row["candidate_collapsed_batch_12ai"])
        self.assertEqual(row["independent_textual_witness_count_added_batch_12ai"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12ai"], 0)
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["algorithm_reopen_authorized"])


    def test_batch_12aj_fullbook_luojing_is_directional_not_a_clock(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(
            row["batch_12aj_fullbook_luojing_timekeeping_semantics_artifact"],
            "docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json",
        )
        self.assertEqual(
            row["fullbook_luojing_phrase"],
            "如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣",
        )
        self.assertEqual(
            row["fullbook_luojing_phrase_direct_physical_edition_agreement"],
            "CONFIRMED_NANYANGTANG_AND_GUANGYI",
        )
        self.assertEqual(row["fullbook_luojing_phrase_direct_physical_route_count"], 2)
        self.assertEqual(
            row["fullbook_luojing_term_mechanical_concept"],
            "MAGNETIC_COMPASS_DIRECTION_AND_MERIDIAN_ORIENTATION_INSTRUMENT_FAMILY",
        )
        self.assertEqual(
            row["fullbook_luojing_standalone_timekeeper_equivalence"],
            "REJECTED_BY_CONTEMPORANEOUS_TECHNICAL_CONTROL",
        )
        self.assertEqual(row["fullbook_luojing_direct_true_solar_time_equivalence"], "NOT_ESTABLISHED")
        self.assertEqual(
            row["fullbook_vs_ming_technical_instrument_semantic_relation"],
            "REAL_TENSION_PRESERVE_DO_NOT_HARMONIZE_BY_ASSUMPTION",
        )
        self.assertFalse(row["local_apparent_solar_time_runtime_winner_selected"])
        self.assertFalse(row["luojing_means_true_solar_time"])
        self.assertEqual(
            row["runtime_time_standard_binding_status_batch_12aj"],
            "PARTIALLY_NARROWED_WITH_FULLBOOK_INSTRUMENT_SEMANTIC_TENSION_NOT_CLOSED",
        )
        self.assertEqual(row["independent_textual_witness_count_added_batch_12aj"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12aj"], 0)
        self.assertFalse(row["candidate_selected_batch_12aj"])
        self.assertFalse(row["candidate_collapsed_batch_12aj"])
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["algorithm_reopen_authorized"])


    def test_batch_12ak_gaohou_mengqiu_is_later_operational_bridge_only(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(
            row["batch_12ak_gaohou_mengqiu_operational_bridge_artifact"],
            "docs/research/ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-R1.json",
        )
        self.assertEqual(row["batch_12ak_primary_physical_source_id"], "EXT-WASEDA-GAOHOU-MENGQIU-1807-1809")
        self.assertEqual(
            row["batch_12ak_waseda_pdf_sha256"],
            "53ee7b0e59fbb92304af08d6f1b58226bee6fff85f23e5b43e830b76b967f1e4",
        )
        self.assertEqual(row["batch_12ak_waseda_pdf_page_count"], 221)
        self.assertEqual(row["batch_12ak_direct_physical_review_pages"], [130, 131, 132, 143, 194, 195])
        self.assertEqual(
            row["batch_12ak_luojing_pinggui_status"],
            "DIRECT_PHYSICAL_CONFIRMED_COMPASS_ORIENTATION_COMPONENT_INSIDE_SUNDIAL",
        )
        self.assertEqual(
            row["batch_12ak_inclement_zi_hai_status"],
            "DIRECT_PHYSICAL_CONFIRMED_CLOCK_SECTION_PURPOSE_INCLUDES_INCLEMENT_DARK_CONDITIONS_AND_BIAN_ZI_HAI_DING_ZHIGAN",
        )
        self.assertEqual(
            row["batch_12ak_historical_scope"],
            "QING_JIAQING_LATER_OPERATIONAL_BRIDGE_NOT_MING_FULLBOOK_AUTHORIAL_SPECIFICATION",
        )
        self.assertFalse(row["batch_12ak_fullbook_inheritance_proven"])
        self.assertFalse(row["batch_12ak_true_solar_runtime_selected"])
        self.assertFalse(row["batch_12ak_local_apparent_solar_runtime_selected"])
        self.assertEqual(row["independent_textual_witness_count_added_batch_12ak"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12ak"], 0)
        self.assertEqual(row["later_operational_bridge_increment_batch_12ak"], 1)
        self.assertFalse(row["candidate_selected_batch_12ak"])
        self.assertFalse(row["candidate_collapsed_batch_12ak"])
        self.assertEqual(
            row["runtime_time_standard_binding_status_batch_12ak"],
            "LATER_OPERATIONAL_BRIDGE_CONFIRMED_FULLBOOK_SOURCE_SPECIFIC_BINDING_STILL_OPEN",
        )
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["algorithm_reopen_authorized"])


    def test_batch_12al_korea_target_section_proves_broader_variant_only(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(
            row["batch_12al_korea_cnts_full_target_section_recollation_artifact"],
            "docs/research/ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-R1.json",
        )
        self.assertTrue(row["batch_12al_korea_same_physical_object_recount_forbidden"])
        self.assertEqual(row["batch_12al_korea_direct_pages"], [125, 126])
        self.assertEqual(
            row["batch_12al_korea_target_surface"],
            "命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜",
        )
        self.assertFalse(row["batch_12al_korea_explicit_hai_glyph_observed"])
        self.assertFalse(row["batch_12al_korea_fullbook_luojing_clause_at_target_location"])
        self.assertFalse(row["batch_12al_korea_p126_target_continuation"])
        self.assertEqual(
            row["batch_12al_page_local_negative_scope"],
            "TARGET_LOCATION_AND_ADJACENT_PAGE_ONLY_NOT_WHOLE_MANUSCRIPT",
        )
        self.assertFalse(row["batch_12al_fullbook_luojing_clause_global_universality"])
        self.assertEqual(
            row["batch_12al_within_reviewed_fullbook_luojing_clause_stability"],
            "CONFIRMED_NANYANGTANG_AND_GUANGYI",
        )
        self.assertFalse(row["batch_12al_fullbook_interpolation_claim_authorized"])
        self.assertFalse(row["batch_12al_korea_omission_error_claim_authorized"])
        self.assertEqual(row["batch_12al_exact_stemmatic_direction"], "UNRESOLVED")
        self.assertEqual(row["batch_12al_new_physical_witness_increment"], 0)
        self.assertEqual(row["batch_12al_new_target_section_clause_variant_dimension_increment"], 1)
        self.assertEqual(row["independent_textual_witness_count_added_batch_12al"], 0)
        self.assertEqual(row["independent_hai_glyph_witness_count_added_batch_12al"], 0)
        self.assertFalse(row["candidate_selected_batch_12al"])
        self.assertFalse(row["candidate_collapsed_batch_12al"])
        self.assertEqual(
            row["runtime_time_standard_binding_status_batch_12al"],
            "BROADER_ZIWEI_TRANSMISSION_VARIANT_CONFIRMED_FULLBOOK_OPERATIONAL_PROCEDURE_REMAINS_SOURCE_SCOPED_AND_RUNTIME_UNRESOLVED",
        )
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["algorithm_reopen_authorized"])


    def test_batch_12am_renzi_xuzhi_is_early_shushu_semantic_bridge_only(self) -> None:
        by_id = {row["rule_id"]: row for row in self.rows}
        row = by_id["HPA-ZDATE-006"]
        self.assertEqual(
            row["batch_12am_renzi_xuzhi_luojing_gnomon_bridge_artifact"],
            "docs/research/ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-R1.json",
        )
        self.assertEqual(row["batch_12am_primary_physical_source_id"], "EXT-COMMONS-GGZBCK411-RENZI-XUZHI-1569-1583")
        self.assertEqual(row["batch_12am_bibliographic_source_id"], "EXT-CINII-BB17866565-RENZI-XUZHI-1583")
        self.assertEqual(row["batch_12am_pdf_sha256"], "80de366d62066bf73046834771a43976fdf353de6ea1704d06c46dfa568a44ba")
        self.assertEqual(row["batch_12am_pdf_page_count"], 510)
        self.assertEqual(row["batch_12am_direct_physical_review_pages"], [414, 415, 416])
        self.assertEqual(row["batch_12am_direct_heading"], "正針縫針")
        self.assertEqual(row["batch_12am_decisive_direct_readings"], ["臬測以景針以氣故不能符", "推七政之纏次皆准於臬"])
        self.assertFalse(row["batch_12am_luojing_standalone_clock_equivalence"])
        self.assertFalse(row["batch_12am_luojing_equals_true_solar_time"])
        self.assertFalse(row["batch_12am_luojing_equals_local_apparent_solar_runtime"])
        self.assertFalse(row["batch_12am_fullbook_authorial_inheritance_proven"])
        self.assertFalse(row["batch_12am_fullbook_inclement_time_generation_procedure_closed"])
        self.assertEqual(row["batch_12am_target_leaf_printing_phase"], "UNRESOLVED_WITHIN_LONGQING_3_WANLI_11_COMPOSITE_EDITION")
        self.assertEqual(row["batch_12am_new_fullbook_textual_witness_increment"], 0)
        self.assertEqual(row["batch_12am_new_hai_glyph_witness_increment"], 0)
        self.assertEqual(row["batch_12am_new_early_ming_shushu_semantic_control_increment"], 1)
        self.assertFalse(row["candidate_selected_batch_12am"])
        self.assertFalse(row["candidate_collapsed_batch_12am"])
        self.assertEqual(
            row["runtime_time_standard_binding_status"],
            "EARLY_MING_SHUSHU_GNOMON_NEEDLE_SEMANTIC_SEPARATION_CONFIRMED_FULLBOOK_INCLEMENT_TIME_REALIZATION_AND_RUNTIME_BINDING_STILL_OPEN",
        )
        self.assertEqual(row["audit_status"], "MISSING_FROM_PRODUCT")
        self.assertFalse(row["algorithm_reopen_authorized"])


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
