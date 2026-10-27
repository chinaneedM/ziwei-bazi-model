from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-MF-PDF-ROUTE-R1.json"
BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-MF-PDF-ROUTE-V.md"


class KyujanggakG893MfPdfRouteR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_route_is_distinct_and_closed_without_pdf(self) -> None:
        self.assertEqual(
            self.data["status"],
            "DIRECT_MF_PDF_ROUTE_CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
        )
        self.assertEqual(
            self.data["route_scope"],
            "KYUJANGGAK_MF_PDF_LIST_AND_DIRECT_PDF_ENDPOINT_ONLY_NOT_RENDERER_RETRY",
        )
        adjudication = self.data["adjudication"]
        self.assertEqual(
            adjudication["mf_pdf_route_status"],
            "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
        )
        self.assertFalse(adjudication["renderer_route_retried"])

    def test_list_response_reconfirms_object_but_not_pdf(self) -> None:
        initial = self.data["direct_provider_probe"]["initial_list_probe"]
        self.assertTrue(initial["list_transport_http_200"])
        self.assertEqual(initial["list_result"], "ERROR - DIR NOT EXIST")
        returned = initial["returned_volume"]
        self.assertEqual(returned["CALL_NUM"], "奎貴893")
        self.assertEqual(returned["ORI_TIT"], "授時曆立成")
        self.assertEqual(returned["BOOK_CD"], "GK00893_00")
        self.assertEqual(returned["ITEM_CD"], "SIC")
        self.assertEqual(returned["VOL_NO"], "0001")
        self.assertIsNone(returned["IS_PDF"])

    def test_direct_pdf_endpoint_did_not_return_pdf_magic(self) -> None:
        direct = self.data["direct_provider_probe"]["direct_pdf_control"]
        self.assertTrue(direct["direct_transport_http_200"])
        self.assertFalse(direct["direct_pdf_magic"])
        self.assertFalse(direct["direct_pdf_returned"])
        self.assertEqual(direct["is_pdf_values"], [None])

    def test_six_targets_remain_fail_closed(self) -> None:
        self.assertEqual(self.data["target_status"], "ALL_SIX_PENDING_DIRECT_TARGET_PAGE")
        self.assertEqual(len(self.data["target_controls"]), 6)
        self.assertEqual(self.data["adjudication"]["target_numeric_effect"], "NONE")
        self.assertEqual(
            self.data["epistemic_boundaries"]["technical_endpoint_success_as_target_glyph_authority"],
            "FORBIDDEN",
        )

    def test_batch_doc_preserves_key_boundaries(self) -> None:
        text = BATCH.read_text(encoding="utf-8")
        for fragment in (
            "ERROR - DIR NOT EXIST",
            "IS_PDF = Y",
            "direct_pdf_returned = false",
            "M/F73-102-37-A",
            "PENDING_DIRECT_TARGET_PAGE",
            "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
        ):
            self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
