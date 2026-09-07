from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-R1.json"


class ZiweiJapanMingFullbookFacsimileRoutesR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.by_id = {row["rule_id"]: row for row in cls.matrix["rows"]}
        cls.by_source = {row["source_id"]: row for row in cls.registry["sources"]}

    def test_naj_identity_is_positive_while_runner_403_is_access_only(self) -> None:
        naj = self.evidence["national_archives_japan"]
        idx = naj["official_public_search_index_observation"]
        self.assertEqual("子０６０－０００１", idx["call_number"])
        self.assertEqual("刊本:明:::", idx["bibliographic_label"])
        self.assertEqual("2冊", idx["quantity"])
        self.assertEqual("4468520", idx["first_item"]["id"])
        self.assertEqual("公開", idx["first_item"]["access_class"])
        runner = naj["github_runner_route_probe"]
        self.assertEqual(403, runner["all_routes_http_status"])
        self.assertEqual(
            "GITHUB_RUNNER_ACCESS_BOUNDARY_ONLY_NOT_ARCHIVE_CONTENT_ABSENCE",
            runner["adjudication"],
        )
        self.assertFalse(naj["target_page_observed"])

    def test_sdu_closes_formal_facsimile_route_not_target_page(self) -> None:
        sdu = self.evidence["sdu_formal_facsimile_route"]
        stmt = sdu["direct_catalog_statement"]
        self.assertEqual("《新鋟希夷陳先生紫微斗數全書》七卷", stmt["work"])
        self.assertEqual("據内閣文庫藏明刊本", stmt["base_copy"])
        self.assertEqual("影印", stmt["reproduction"])
        self.assertEqual("UNRESOLVED", sdu["exact_15_volume_set_subvolume_for_target_work"])
        self.assertFalse(sdu["target_page_observed"])
        self.assertIn("EXT-SDU-ZIHAI-NAIKAKU-ZWDSQS-FACSIMILE", self.by_source)

    def test_toyo_copy_labels_are_not_collapsed_into_print_genealogy(self) -> None:
        toyo = self.evidence["toyo_bunko_quanji_catalog_control"]
        self.assertEqual("VII-3-157", toyo["official_catalog_controls"]["callmark"])
        labels = {row["publication_label"] for row in toyo["official_catalog_controls"]["entries"]}
        self.assertEqual({"鈔本", "寫本"}, labels)
        self.assertTrue(toyo["discrepancy_with_ncku_print_genealogy"].startswith("PRESERVE_UNRESOLVED"))
        ncku = self.evidence["ncku_scholarly_genealogy"]
        self.assertFalse(ncku["visual_review"]["ocr_used"])
        self.assertEqual([60, 61], ncku["visual_review"]["reviewed_printed_pages"])

    def test_product_state_and_counts_remain_fail_closed(self) -> None:
        row = self.by_id["HPA-ZDATE-006"]
        self.assertEqual("MISSING_FROM_PRODUCT", row["audit_status"])
        self.assertEqual("NOT_OBSERVED", row["japan_target_late_zi_page_status"])
        self.assertFalse(row["algorithm_reopen_authorized"])
        audit = self.state["historical_audit"]
        self.assertEqual(198, audit["row_count"])
        self.assertEqual(166, audit["audited_row_count"])
        self.assertEqual(10, audit["current_missing_from_product_row_count"])
        self.assertEqual(14, audit["identified_missing_candidate_family_count"])
        self.assertIn("BATCH-12-ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-H", audit["completed_batches"])
        self.assertEqual("CLOSED", self.state["invariants"]["deterministic_fusion_chart_product_r1"])
        self.assertEqual(0, self.state["invariants"]["confirmed_chart_algorithm_defect_count"])
        self.assertEqual(0, self.state["invariants"]["algorithm_reopen_count"])


if __name__ == "__main__":
    unittest.main()
