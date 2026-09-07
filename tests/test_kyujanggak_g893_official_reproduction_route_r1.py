from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-OFFICIAL-REPRODUCTION-ROUTE-R1.json"
BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-OFFICIAL-REPRODUCTION-ROUTE-X.md"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
TOPOLOGY = ROOT / "docs" / "research" / "KYUJANGGAK-G893-IMAGE-ACCESS-TOPOLOGY-R1.json"

class KyujanggakG893OfficialReproductionRouteR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.topology = json.loads(TOPOLOGY.read_text(encoding="utf-8"))

    def test_object_specific_official_route_is_bound(self) -> None:
        self.assertEqual(self.data["status"], "OFFICIAL_REPRODUCTION_APPLICATION_ROUTE_DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED")
        obj = self.data["g893_object"]
        self.assertEqual(obj["catalog_identifier"], "奎貴893")
        self.assertEqual(obj["book_cd"], "GK00893_00")
        self.assertEqual(obj["microfilm_number"], "M/F73-102-37-A")
        self.assertTrue(obj["reproduction_request_ui_visible"])

    def test_service_policy_records_pdf_homepage_publication(self) -> None:
        obs = self.data["official_service_notice"]["direct_observations"]
        self.assertEqual(obs["microfilm_method"], "MICROFILM_SCAN_PDF_UPLOADED_TO_HOMEPAGE")
        self.assertEqual(obs["procedure"], ["HOMEPAGE","SEARCH_MATERIAL","REPRODUCTION_REQUEST","CHECK_APPROVAL_EMAIL"])
        self.assertEqual(obs["normal_processing_period"], "WITHIN_2_WEEKS_OF_APPLICATION_UNLESS_DELAY_SEPARATELY_NOTIFIED")
        self.assertEqual(self.data["nonmember_cart_surface"]["observed_service_change_effective_date"], "2024-02-01")

    def test_no_application_or_fulfillment_is_claimed(self) -> None:
        self.assertFalse(self.data["external_application_submitted"])
        self.assertFalse(self.data["approval_received"])
        route = self.data["route_adjudication"]
        self.assertEqual(route["g893_request_acceptance"], "UNTESTED")
        self.assertEqual(route["whole_volume_vs_selected_pages"], "UNRESOLVED_UNTIL_REQUEST_FORM_OR_APPROVAL")
        self.assertEqual(route["fee_or_charge"], "NOT_STATED_IN_REVIEWED_OFFICIAL_NOTICE_DO_NOT_INFER_FREE")

    def test_targets_remain_fail_closed(self) -> None:
        self.assertEqual(self.data["target_status"], "ALL_SIX_PENDING_DIRECT_TARGET_PAGE")
        self.assertEqual(len(self.data["target_controls"]), 6)
        self.assertEqual(self.data["route_adjudication"]["target_numeric_effect"], "NONE")

    def test_registry_and_topology_preserve_route_boundary(self) -> None:
        item = next(x for x in self.registry["sources"] if x["source_id"] == "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893")
        self.assertEqual(item["official_reproduction_route"]["status"], "DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED")
        self.assertFalse(item["official_reproduction_route"]["request_submitted"])
        self.assertEqual(self.topology["official_reproduction_route"]["status"], "DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED")
        self.assertEqual(self.topology["target_status"], "ALL_SIX_PENDING_DIRECT_TARGET_PAGE")

    def test_batch_keeps_v_x_distinction(self) -> None:
        text = BATCH.read_text(encoding="utf-8")
        for fragment in ("CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED","DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED","2024-02-01","M/F73-102-37-A","PENDING_DIRECT_TARGET_PAGE","G893_FEE_STATUS=UNKNOWN_DO_NOT_INFER_FREE"):
            self.assertIn(fragment, text)

if __name__ == "__main__":
    unittest.main()
