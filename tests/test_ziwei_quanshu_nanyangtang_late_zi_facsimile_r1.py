from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json"
NATAL = ROOT / "src" / "fortune_training" / "ziwei_chart" / "natal.py"

class ZiweiQuanshuNanyangtangLateZiFacsimileR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_direct_facsimile_identity_is_bound_without_ocr(self) -> None:
        source = self.evidence["source_object"]
        self.assertEqual("32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7", source["pdf_sha256"])
        self.assertEqual(527, source["pdf_page_count"])
        self.assertFalse(source["ocr_used"])
        direct = self.evidence["direct_collation"]
        self.assertEqual(320, direct["pdf_page_1_based"])
        self.assertEqual("論人生時要審的確", direct["heading"])
        self.assertIn("如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時", direct["verbatim_lines"])

    def test_s01_exact_quote_remains_narrowly_quarantined(self) -> None:
        direct = self.evidence["direct_collation"]
        self.assertEqual("NOT_OBSERVED_ON_DIRECT_TARGET_SECTION_PAGE", direct["s01_claimed_sentence_status"])
        self.assertFalse(direct["whole_volume_negative_claim_authorized"])
        row = self.by_id["HPA-ZIWEI-001"]
        self.assertEqual("NOT_OBSERVED_ON_DIRECT_TARGET_SECTION_PAGE", row["facsimile_adjudication"]["s01_exact_sentence_status"])

    def test_new_candidate_is_missing_from_product_not_a_default_reopen(self) -> None:
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertEqual("NANYANGTANG-FULLBOOK-ZI-TEN-KE-HAI-SPLIT-R1", row["candidate_method_id"])
        self.assertFalse(row["algorithm_reopen_authorized"])
        self.assertEqual("NOT_YET_FORMALIZED", self.evidence["philological_adjudication"]["modern_clock_mapping_status"])
        self.assertFalse(self.evidence["philological_adjudication"]["runtime_selection_authorized"])

    def test_runtime_gap_is_real_and_scoped(self) -> None:
        source = NATAL.read_text(encoding="utf-8")
        self.assertIn("# 子 covers 23:00..00:59", source)
        self.assertIn("return ((local_apparent_solar_datetime.hour + 1) // 2) % 12", source)
        self.assertEqual("NO_PROFILE_CAN_EXPRESS_SOURCE_SCOPED_HALF_ZI_TO_HAI_BRANCH_RECLASSIFICATION", self.evidence["runtime_gap"]["gap"])

    def test_registry_state_and_accounting_are_synchronized(self) -> None:
        source = self.by_source["EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN"]
        self.assertEqual("32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7", source["pdf_sha256"])
        self.assertEqual(320, source["direct_target_page_1_based"])
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertIn("BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A", audit["completed_batches"])
        self.assertIn("BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A", audit["completed_batches"])
        self.assertTrue(audit["latest_batch_doc"].startswith("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-"))
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])

if __name__ == "__main__":
    unittest.main()
