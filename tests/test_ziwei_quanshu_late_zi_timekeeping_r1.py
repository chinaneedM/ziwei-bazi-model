from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
BATCH12A = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-LATE-ZI-TIMEKEEPING-COLLATION-R1.json"

class ZiweiQuanshuLateZiTimekeepingR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.batch12a = json.loads(BATCH12A.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_timekeeping_sources_are_role_separated(self) -> None:
        for source_id in (
            "EXT-CTEXT-SMTHE-SIKU-V2",
            "EXT-CTEXT-RIZHILU-BAIKE",
            "EXT-NAOJ-KOYOMI-TEIJI-SHICHEN",
            "EXT-WIKISOURCE-ZWDSQS-V3-LATE-ZI",
            "EXT-SHIDIAN-ZWDSQS-LATE-ZI",
        ):
            self.assertIn(source_id, self.by_source)
        for witness in self.evidence["timekeeping_witnesses"]:
            self.assertEqual("FORBIDDEN", witness["doctrinal_import_to_ziwei"])

    def test_upper_lower_half_orientation_is_closed_only_generically(self) -> None:
        adjudication = self.evidence["adjudication"]
        self.assertEqual("BEFORE_MIDNIGHT_PREVIOUS_DAY", adjudication["upper_half_orientation"])
        self.assertEqual("AFTER_MIDNIGHT_CURRENT_DAY", adjudication["lower_half_orientation"])
        self.assertEqual("REJECTED", adjudication["ten_ke_equal_duration_interpretation"])
        modern = adjudication["generic_fixed_shichen_modern_translation"]
        self.assertEqual("APPROX_23:00-24:00", modern["upper_half"])
        self.assertEqual("APPROX_00:00-01:00", modern["lower_half"])
        self.assertEqual("UNRESOLVED", adjudication["runtime_time_standard_binding"])

    def test_direct_facsimile_still_controls_glyphs(self) -> None:
        controls = {row["source_id"]: row for row in self.evidence["received_text_controls"]}
        self.assertEqual(
            "AGREES_AT_CRITICAL_UPPER_FIVE_LOWER_FIVE_WORDING",
            controls["EXT-SHIDIAN-ZWDSQS-LATE-ZI"]["relation_to_facsimile"],
        )
        self.assertEqual(
            "DIFFERS_FROM_DIRECT_FACSIMILE_AT 五/午 GLYPH",
            controls["EXT-WIKISOURCE-ZWDSQS-V3-LATE-ZI"]["relation_to_facsimile"],
        )
        self.assertEqual(
            "NOT_OBSERVED_ON_DIRECT_TARGET_SECTION_PAGE",
            self.batch12a["direct_collation"]["s01_claimed_sentence_status"],
        )

    def test_candidate_remains_missing_and_unselected(self) -> None:
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("CLOSED_AT_GENERIC_FIXED_SHICHEN_LEVEL", row["timekeeping_orientation_status"])
        self.assertEqual(
            "UNRESOLVED_DO_NOT_CHOOSE_CIVIL_MEAN_OR_APPARENT_SOLAR_TIME_FROM_TIMEKEEPING_TRANSLATION",
            row["runtime_time_standard_binding"],
        )
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertFalse(row["algorithm_reopen_authorized"])
        self.assertFalse(self.evidence["adjudication"]["runtime_selection_authorized"])

    def test_accounting_and_closed_product_are_unchanged(self) -> None:
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertEqual("BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B", audit["completed_batches"][-1])
        self.assertEqual(
            "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B.md",
            audit["latest_batch_doc"],
        )
        self.assertEqual("CLOSED", self.state["invariants"]["deterministic_fusion_chart_product_r1"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])

if __name__ == "__main__":
    unittest.main()
