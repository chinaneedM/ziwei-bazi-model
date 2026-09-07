from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json"


class ZiweiQuanjiLianyuangeLateZiCollationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_lianyuange_route_is_bound_without_target_glyph_claim(self) -> None:
        pub = self.evidence["publisher_lianyuange_route"]
        self.assertEqual(200, pub["http_status"])
        self.assertTrue(pub["lianyuange_present"])
        self.assertTrue(pub["quanji_present"])
        idx = self.evidence["google_books_jielan_index"]
        self.assertEqual(["PT176", "PT177"], idx["lianyuange_query"]["page_ids"])
        self.assertFalse(idx["physical_lianyuange_target_page_observed"])
        self.assertIn("EXT-XINYITANG-JIELAN-LIANYUANGE-QUANJI-COLLATION", self.by_source)
        self.assertIn("EXT-GOOGLE-BOOKS-JIELAN-LIANYUANGE-QUANJI-INDEX", self.by_source)

    def test_received_quanji_text_is_secondary_and_mechanically_distinct(self) -> None:
        received = self.evidence["received_quanji_transcription_control"]
        self.assertEqual(
            "SECONDARY_RECEIVED_TRANSCRIPTION_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY",
            received["authority"],
        )
        self.assertTrue(received["controls"]["ten_ke_present"])
        self.assertTrue(received["controls"]["upper_five_previous_night_present"])
        self.assertTrue(received["controls"]["lower_five_current_night_zi_present"])
        phil = self.evidence["philological_adjudication"]
        self.assertEqual("PARALLEL_BUT_NOT_MECHANICALLY_IDENTICAL", phil["relation_to_nanyangtang_fullbook"])
        self.assertFalse(phil["new_candidate_row_authorized"])
        self.assertFalse(phil["hpa_zdate_006_reclassification_authorized"])

    def test_index_mismatch_and_zero_results_do_not_become_textual_proof(self) -> None:
        idx = self.evidence["google_books_jielan_index"]
        self.assertEqual("FORBIDDEN", idx["zero_result_as_negative_textual_proof"])
        anomaly = idx["ten_ke_query_anomaly"]
        self.assertEqual("PT88", anomaly["page_id"])
        self.assertFalse(anomaly["snippet_contains_query_term"])
        self.assertFalse(anomaly["positive_target_evidence_authorized"])

    def test_product_counts_and_candidate_state_remain_unchanged(self) -> None:
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertEqual(
            "NOT_AUTHORIZED_PENDING_DIRECT_PHYSICAL_TARGET_PAGE",
            row["quanji_candidate_formalization_status"],
        )
        self.assertFalse(row["algorithm_reopen_authorized"])
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertIn("BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G", audit["completed_batches"])
        self.assertEqual("CLOSED", self.state["invariants"]["deterministic_fusion_chart_product_r1"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])


if __name__ == "__main__":
    unittest.main()
