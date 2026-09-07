from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
DOC = ROOT / "docs" / "ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-PRODUCTIZATION-R1.md"
CORE = ROOT / "src" / "fortune_training" / "ziwei_chart" / "temporal_historical_candidates.py"
BROWSER = ROOT / "src" / "fortune_training" / "combined_chart_application" / "target_flow_ziwei_projection_assets.py"


class ZiweiTemporalHistoricalCandidateProductizationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}

    def test_two_previously_missing_rows_are_productized_without_selection(self) -> None:
        hour = self.by_id["HPA-ZTEMP-004"]
        leap = self.by_id["HPA-ZTEMP-006"]
        self.assertEqual("HISTORICALLY_SUPPORTED", hour["audit_status"])
        self.assertEqual("SUPPORTED_BUT_SCHOOL_SPECIFIC", leap["audit_status"])
        self.assertEqual("PRESERVED_NOT_SELECTED", hour["selection_status"])
        self.assertEqual("PRESERVED_NOT_SELECTED", leap["selection_status"])
        self.assertEqual(
            "JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1",
            hour["candidate_method_id"],
        )
        self.assertEqual(
            "ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1",
            leap["candidate_method_id"],
        )
        self.assertFalse(hour["algorithm_reopen_authorized"])
        self.assertFalse(leap["algorithm_reopen_authorized"])

    def test_accounting_separates_cumulative_discovery_from_current_gap_rows(self) -> None:
        summary = self.matrix["audit_summary"]
        self.assertEqual(13, summary["identified_missing_candidate_family_count"])
        self.assertEqual(9, summary["current_missing_from_product_row_count"])
        self.assertEqual(9, sum(
            row["audit_status"] == "MISSING_FROM_PRODUCT"
            for row in self.matrix["rows"]
        ))
        self.assertEqual(6, summary["historical_candidate_extension_count"])
        self.assertEqual(3, summary["historical_candidate_registry_count"])
        self.assertEqual(3, summary["historical_candidate_runtime_resolver_count"])
        self.assertEqual(88, self.matrix["inventory_summary"]["status_counts"]["HISTORICALLY_SUPPORTED"])
        self.assertEqual(18, self.matrix["inventory_summary"]["status_counts"]["SUPPORTED_BUT_SCHOOL_SPECIFIC"])

    def test_state_preserves_closed_product_and_g893_boundaries(self) -> None:
        audit = self.state["historical_audit"]
        self.assertEqual(9, audit["current_missing_from_product_row_count"])
        self.assertEqual(13, audit["identified_missing_candidate_family_count"])
        self.assertEqual(6, audit["historical_candidate_extension_count"])
        self.assertEqual(3, audit["historical_candidate_registry_count"])
        self.assertEqual(3, audit["historical_candidate_runtime_resolver_count"])
        self.assertTrue(self.state["invariants"]["deterministic_fusion_chart_product_r1_closed"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])
        focus = "\n".join(audit["current_focus"])
        for fragment in (
            "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
            "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
            "5c4276d953bd47ca2679c70209d179cf",
            "ZGKS802.008",
            "M/F73-102-37-A",
            "PENDING_DIRECT_TARGET_PAGE",
        ):
            self.assertIn(fragment, focus)

    def test_runtime_and_browser_keep_candidate_families_separate(self) -> None:
        core = CORE.read_text(encoding="utf-8")
        browser = BROWSER.read_text(encoding="utf-8")
        for token in (
            "ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1",
            "ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1",
            "JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1",
            "ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1",
            "NOT_CLOSED_BY_THIS_MONTH_POLICY_API",
        ):
            self.assertIn(token, core)
        self.assertIn("historical_hourly_method_candidates", browser)
        self.assertIn("leap_month_method_candidates", browser)
        self.assertIn("PRESERVED_NOT_SELECTED", browser)
        self.assertNotIn("five_rats_hour_pillar", browser)
        self.assertNotIn("branch_index(", browser)

    def test_productization_doc_is_not_a_new_historical_batch(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("This document records productization only", text)
        self.assertIn("Historical authority remains Batch 08B", text)
        self.assertIn("CURRENT_MISSING_FROM_PRODUCT_ROWS=9", text)


if __name__ == "__main__":
    unittest.main()
