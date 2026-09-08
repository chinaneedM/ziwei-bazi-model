from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-WENGUANG-GOOGLE-INDEX-PREVIEW-R1.json"

class ZiweiQuanshuWenguangGoogleIndexPreviewR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_exact_google_distribution_volume_and_target_index_are_bound(self) -> None:
        volume = self.evidence["distribution_volume"]
        self.assertEqual("aIRbDgAAQBAJ", volume["volume_id"])
        self.assertEqual("9789888266944", volume["isbn"])
        self.assertEqual(266, volume["declared_page_count"])
        self.assertTrue(volume["free_sample_marker_present"])
        index = self.evidence["public_search_index"]
        self.assertEqual("PT165", index["target_heading_query"]["target_page_id"])
        self.assertIn("上五刻", index["target_index_reading"])
        self.assertIn("亥時", index["target_index_reading"])
        self.assertEqual(
            "SEARCH_INDEX_TEXT_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY",
            index["target_index_reading_authority"],
        )

    def test_zero_search_result_is_not_promoted_to_negative_textual_proof(self) -> None:
        index = self.evidence["public_search_index"]
        self.assertEqual(0, index["s01_claimed_sentence_result_count_in_reviewed_runs"])
        self.assertFalse(index["negative_textual_claim_authorized"])
        self.assertIn("INSTABILITY", index["reason_negative_claim_forbidden"])

    def test_official_viewer_does_not_claim_direct_target_glyphs(self) -> None:
        viewer = self.evidence["embedded_viewer_control"]
        self.assertTrue(viewer["viewer_loaded"])
        self.assertTrue(viewer["go_to_pt165_returned"])
        self.assertEqual("PT166", viewer["after_page_id"])
        self.assertFalse(viewer["target_page_directly_observed"])
        self.assertEqual(
            "UNAVAILABLE_PREVIEW_PLACEHOLDERS_VISIBLE_NO_ANCIENT_PAGE_GLYPHS",
            viewer["screenshot_visual_review"],
        )
        self.assertEqual("NONE_FROM_THIS_VIEWER_RUN", viewer["glyph_authority"])

    def test_public_xinyi_samples_are_no_target_controls_only(self) -> None:
        samples = self.evidence["xinyi_public_sample_control"]
        self.assertEqual(7, samples["public_sample_image_count"])
        self.assertEqual(7, len(samples["sample_sha256"]))
        self.assertFalse(samples["target_page_observed"])
        source = self.by_source["EXT-XINYI-ZWDSQS-WENGUANG-PUBLIC-SAMPLES-2021"]
        self.assertFalse(source["target_page_observed"])

    def test_hpa_zdate_006_remains_missing_and_cross_edition_glyph_unresolved(self) -> None:
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertEqual(
            "TARGET_PASSAGE_CORROBORATED_AT_PUBLIC_SEARCH_INDEX_LEVEL_NOT_GLYPH_AUTHORITY",
            row["combined_facsimile_index_text_status"],
        )
        self.assertEqual(
            "UNRESOLVED_DUNHUATANG_VS_JISHUTANG",
            row["combined_facsimile_base_copy_identity_for_pt165"],
        )
        self.assertIn(
            "EXPLICIT_HAI_IS_NOT_UNIVERSAL_ACROSS_BROADER_RECEIVED_ZIWEI_TRANSMISSION",
            row["hai_glyph_cross_edition_status"],
        )
        self.assertIn(
            "WITHIN_FULLBOOK_EDITION_FAMILY_STABILITY_REMAINS_UNRESOLVED",
            row["hai_glyph_cross_edition_status"],
        )
        self.assertFalse(row["algorithm_reopen_authorized"])

    def test_batch_is_zero_count_effect_and_product_remains_closed(self) -> None:
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertIn("BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D", audit["completed_batches"])
        self.assertTrue(audit["latest_batch_doc"].startswith("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-"))
        self.assertEqual("CLOSED", self.state["invariants"]["deterministic_fusion_chart_product_r1"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])

if __name__ == "__main__":
    unittest.main()
