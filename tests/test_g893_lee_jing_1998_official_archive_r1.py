from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "research" / "G893-LEE-JING-1998-OFFICIAL-JOURNAL-ARCHIVE-R1.json"
BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-LEE-JING-1998-OFFICIAL-ARCHIVE-W.md"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"


class G893LeeJing1998OfficialArchiveR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_official_record_is_directly_bound(self) -> None:
        self.assertEqual(
            self.data["status"],
            "DIRECT_OFFICIAL_JOURNAL_RECORD_AND_ABSTRACT_BOUND_FULLTEXT_REMAINS_CNKI_ROUTED_NO_TARGET_PAGE_EXPOSED",
        )
        archive = self.data["official_archive"]
        self.assertEqual(archive["paper_uuid"], "5c4276d953bd47ca2679c70209d179cf")
        self.assertEqual(archive["cnki_node_id"], "ZGKS802.008")
        self.assertEqual(archive["title"], "朝鲜奎章阁本的《授时历立成》")
        self.assertEqual(archive["authors"], ["李银姬", "景冰"])

    def test_fulltext_and_target_pages_remain_fail_closed(self) -> None:
        access = self.data["access_boundary"]
        self.assertTrue(access["official_portal_abstract_visible"])
        self.assertFalse(access["official_portal_fulltext_visible"])
        self.assertFalse(access["public_target_figure_exposed_on_official_portal"])
        self.assertFalse(access["full_article_directly_retrieved"])
        self.assertFalse(self.data["paywall_or_auth_bypass_attempted"])
        self.assertEqual(self.data["target_status"], "ALL_SIX_PENDING_DIRECT_TARGET_PAGE")
        self.assertEqual(len(self.data["target_controls"]), 6)

    def test_exact_copy_year_is_not_silently_closed(self) -> None:
        self.assertEqual(
            self.data["adjudication"]["exact_surviving_copy_print_year_effect"],
            "NONE_SEJONG_REIGN_ONLY_NOT_EXACT_1434_OR_1444",
        )
        self.assertEqual(
            self.data["epistemic_boundaries"]["specialist_article_claim_as_exact_print_year"],
            "FORBIDDEN",
        )

    def test_source_registry_is_upgraded_to_official_record(self) -> None:
        item = next(
            source
            for source in self.registry["sources"]
            if source["source_id"] == "EXT-LEE-JING-KYUJANGGAK-SHOUSHI-LICHENG-1998"
        )
        self.assertEqual(item["official_archive_binding"]["paper_uuid"], "5c4276d953bd47ca2679c70209d179cf")
        self.assertEqual(item["official_archive_binding"]["cnki_node_id"], "ZGKS802.008")
        self.assertFalse(item["access_boundary"]["full_article_directly_retrieved"])
        self.assertEqual(item["target_effect"], "NONE_ALL_SIX_PENDING_DIRECT_TARGET_PAGE")

    def test_batch_doc_preserves_u_v_w_boundaries(self) -> None:
        text = BATCH.read_text(encoding="utf-8")
        for fragment in (
            "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
            "1930_GENERIC_MAIN_NUMBER_893_AS_CURRENT_奎貴893=DISPROVEN",
            "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
            "ZGKS802.008",
            "PENDING_DIRECT_TARGET_PAGE",
            "PAYWALL_OR_AUTH_BYPASS_ATTEMPTED=false",
        ):
            self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
