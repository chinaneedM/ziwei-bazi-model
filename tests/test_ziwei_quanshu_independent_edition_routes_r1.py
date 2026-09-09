from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-R1.json"

class ZiweiQuanshuIndependentEditionRoutesR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_official_independent_edition_routes_are_registered(self) -> None:
        for source_id in (
            "EXT-XINYITANG-ZWDSQS-WENGUANG-FACSIMILE-2017",
            "EXT-XINYITANG-ZWDSQS-WENCHENGTANG-COLLATION",
        ):
            self.assertIn(source_id, self.by_source)
        wenguang = self.evidence["heart_one_wenguangtang_facsimile"]
        self.assertEqual("9789888266944", wenguang["isbn"])
        self.assertEqual(200, wenguang["official_probe"]["http_status"])
        self.assertEqual(
            {"敦化堂刊本", "繼述堂刊本"},
            {row["name"] for row in wenguang["publisher_described_base_copies"]},
        )
        wencheng = self.evidence["wenchengtang_route"]
        self.assertEqual(200, wencheng["official_probe"]["http_status"])
        self.assertEqual(
            "SEPARATE_QING_FULLBOOK_EDITION_ROUTE",
            wencheng["relation_to_wenguangtang_family"],
        )

    def test_no_public_target_page_is_claimed(self) -> None:
        controls = self.evidence["public_preview_controls"]
        self.assertEqual("HTTP_403_FORBIDDEN", controls["books_product_route"]["status"])
        self.assertEqual(13, controls["books_preview_image_urls"]["attempted_count"])
        self.assertEqual(13, controls["books_preview_image_urls"]["http_403_count"])
        self.assertEqual(0, controls["books_preview_image_urls"]["saved_image_count"])
        self.assertFalse(controls["books_preview_image_urls"]["target_page_observed"])
        self.assertEqual(
            "NO_INDEPENDENT_TARGET_PAGE_OBSERVED",
            self.evidence["adjudication"]["independent_physical_target_page_status"],
        )

    def test_secondary_wenshengtang_route_stays_secondary(self) -> None:
        row = self.evidence["wenshengtang_secondary_locator"]
        self.assertEqual("SECONDARY_UNVERIFIED_LOCATOR_ONLY", row["authority"])
        self.assertFalse(row["target_page_exposed"])
        source = self.by_source["EXT-SKYLIGHT-ZWDSQS-WENSHENG-JISHU-COMPARISON-2017"]
        self.assertIn("SECONDARY", source["source_role"])

    def test_hai_glyph_stability_preserves_broader_variant_and_fullbook_agreement(self) -> None:
        adjudication = self.evidence["adjudication"]
        self.assertEqual(
            "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES",
            adjudication["hai_glyph_stability_across_physical_editions"],
        )
        self.assertFalse(adjudication["candidate_selection_authorized"])
        self.assertFalse(adjudication["algorithm_reopen_authorized"])
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertIn(
            "EXPLICIT_HAI_IS_NOT_UNIVERSAL_ACROSS_BROADER_RECEIVED_ZIWEI_TRANSMISSION",
            row["hai_glyph_cross_edition_status"],
        )
        self.assertIn(
            "NANYANGTANG_AND_GUANGYI_DIRECT_PHYSICAL_FULLBOOK_EDITIONS_BOTH_HAVE",
            row["hai_glyph_cross_edition_status"],
        )
        self.assertIn(
            "GLOBAL_ALL_FULLBOOK_EDITION_STABILITY_NOT_CLAIMED",
            row["hai_glyph_cross_edition_status"],
        )
        self.assertFalse(row["algorithm_reopen_authorized"])

    def test_batch_is_provenance_only_and_counts_do_not_move(self) -> None:
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertIn("BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C", audit["completed_batches"])
        self.assertTrue(audit["latest_batch_doc"].startswith("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-"))
        self.assertEqual("CLOSED", self.state["invariants"]["deterministic_fusion_chart_product_r1"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])

if __name__ == "__main__":
    unittest.main()
