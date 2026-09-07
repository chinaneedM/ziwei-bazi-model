from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-R1.json"

class ZiweiQuanshuJingluntangPhysicalRouteR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_shlib_official_jingluntang_identity_is_bound(self) -> None:
        shlib = self.evidence["shanghai_library"]
        self.assertEqual("1pjr6vy1ffsq3l1y", shlib["instance_id"])
        self.assertEqual("子30814110", shlib["identifier"])
        self.assertEqual("清經綸堂刻本", shlib["edition_label"])
        self.assertEqual("新鋟希夷陳先生紫微斗數全書四卷", shlib["title"])
        self.assertEqual(200, shlib["public_content_negotiation"]["jsonld"]["http_status"])
        self.assertIn("EXT-SHLIB-ZWDSQS-JINGLUNTANG-QING", self.by_source)

    def test_shlib_page_route_remains_fail_closed(self) -> None:
        shlib = self.evidence["shanghai_library"]
        self.assertFalse(shlib["target_page_observed"])
        self.assertEqual(412, shlib["anonymous_route_controls"]["dhapi_pdfview_root"]["http_status"])
        self.assertFalse(shlib["public_metadata_token_scan"]["iiif"])
        self.assertFalse(shlib["public_metadata_token_scan"]["manifest"])
        self.assertFalse(shlib["public_metadata_token_scan"]["itemId"])
        self.assertIn("NO_SHLIB_ITEMID_GUESSING", self.evidence["scope_firewalls"])

    def test_kumyo_physical_copy_has_eight_unique_reviewed_images(self) -> None:
        kumyo = self.evidence["kumyo_physical_copy"]
        self.assertEqual("BBAA18036", kumyo["auction_no"])
        self.assertEqual(8, kumyo["unique_embedded_physical_image_count"])
        self.assertEqual(8, len(kumyo["unique_image_sha256"]))
        self.assertTrue(kumyo["jingluntang_label_visibly_observed"])
        self.assertFalse(kumyo["target_heading_observed"])
        self.assertFalse(kumyo["target_passage_observed"])
        self.assertFalse(kumyo["target_hai_glyph_observed"])
        self.assertIn("EXT-KUMYO-ZWDSQS-JINGLUNTANG-19C-PHYSICAL", self.by_source)

    def test_hpa_zdate_006_stays_missing_and_hai_unresolved(self) -> None:
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertEqual(
            "EIGHT_UNIQUE_PHYSICAL_IMAGES_DIRECTLY_REVIEWED_NO_TARGET_SECTION",
            row["jingluntang_public_image_review_status"],
        )
        self.assertEqual(
            "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES",
            row["hai_glyph_cross_edition_status"],
        )
        self.assertFalse(row["algorithm_reopen_authorized"])
        adjudication = self.evidence["adjudication"]
        self.assertFalse(adjudication["candidate_selection_authorized"])
        self.assertFalse(adjudication["algorithm_reopen_authorized"])

    def test_batch_has_zero_count_effect_and_product_stays_closed(self) -> None:
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertIn("BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E", audit["completed_batches"])
        self.assertEqual(
            "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E.md",
            audit["latest_batch_doc"],
        )
        self.assertEqual("CLOSED", self.state["invariants"]["deterministic_fusion_chart_product_r1"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])
        self.assertEqual(0, self.state["invariants"]["candidate_collapse_count"])

if __name__ == "__main__":
    unittest.main()
