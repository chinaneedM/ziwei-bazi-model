from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs" / "research" / "KYUJANGGAK-G893-PREWAR-COLLECTION-CONTINUITY-R1.json"


class KyujanggakG893PrewarCollectionContinuityR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(PATH.read_text(encoding="utf-8"))

    def test_current_object_identity_is_explicit(self) -> None:
        current = self.data["current_object"]
        self.assertEqual(current["catalog_identifier"], "奎貴893")
        self.assertEqual(current["book_cd"], "GK00893_00")
        self.assertEqual(current["extent"], "1冊(102張)")
        self.assertEqual(current["microfilm"], "M/F73-102-37-A")

    def test_collection_continuity_alone_does_not_become_item_identity(self) -> None:
        self.assertEqual(
            self.data["adjudication"]["collection_level_continuity"],
            "SUPPORTED_BY_OFFICIAL_SNU_HISTORY",
        )
        self.assertFalse(
            self.data["prewar_object_family_witness"]["exact_identity_to_current_object"]
        )
        self.assertEqual(
            self.data["epistemic_boundaries"]["collection_continuity_as_individual_copy_identity"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["adjudication"]["exact_item_continuity_to_current_gk00893_00"],
            "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL_BY_1940_PRECIOUS_BOOK_NUMBER_893_TITLE_BINDING",
        )

    def test_rufus_witness_is_object_family_only(self) -> None:
        witness = self.data["prewar_object_family_witness"]
        self.assertEqual(
            witness["source_id"],
            "EXT-RASKB-RUFUS-ASTRONOMY-KOREA-1936",
        )
        self.assertIn("title 授時曆立成", witness["directly_reported_properties"])
        self.assertIn("credited to Wang Xun", witness["directly_reported_properties"])
        self.assertIn("current call number 奎貴893", witness["missing_item_identifiers"])
        self.assertEqual(
            self.data["epistemic_boundaries"]["same_title_and_attribution_as_individual_copy_identity"],
            "FORBIDDEN",
        )

    def test_1930_catalog_numeric_shortcut_is_disproved(self) -> None:
        locator = self.data["prewar_catalog_locator"]
        self.assertEqual(locator["catalog_identifier"], "奎26775-v.1-7")
        access = locator["direct_digital_object_access"]
        self.assertEqual(access["book_cd"], "GK26775_00")
        self.assertEqual(access["item_cd"], "BBG")
        self.assertEqual(access["volume_ids"], ["0001","0002","0003","0004","0005","0006","0007"])
        self.assertTrue(access["renderer_bound"])
        self.assertFalse(access["ocr_used"])
        self.assertTrue(locator["g893_internal_entry_directly_read"])
        self.assertIn(
            "1930_GENERIC_MAIN_NUMBER_893_IS_NOT_CURRENT_PRECIOUS_G893",
            locator["g893_internal_entry_result"],
        )
        self.assertEqual(
            self.data["adjudication"]["prewar_catalog_digital_object_access"],
            "DIRECTLY_BOUND",
        )
        self.assertEqual(
            self.data["epistemic_boundaries"]["prewar_catalog_locator_as_unread_item_binding"],
            "FORBIDDEN",
        )

    def test_1908_precious_catalog_is_negative_title_witness_only(self) -> None:
        self.assertEqual(self.data["schema_version"], "1.3.0")
        controls = {x["source_id"]: x for x in self.data["early_catalog_controls"]}
        witness = controls["EXT-KYUJANGGAK-PRECIOUS-CATALOG-1908"]
        self.assertEqual(witness["book_cd"], "GR35006_00")
        self.assertEqual(witness["item_cd"], "BBG")
        self.assertEqual(
            witness["direct_pdf"]["sha256"],
            "b4b7b14229a82f3f5da12dc069cf8943b1d4c1ff7ca0aa87e85eb3e5d2b06328",
        )
        self.assertFalse(witness["direct_pdf"]["ocr_used"])
        self.assertEqual(witness["direct_visual_review"]["visible_result"], "NOT_SEEN")
        self.assertEqual(
            witness["adjudication"]["negative_catalog_witness"],
            "SUPPORTED_FOR_1908_PRECIOUS_CATALOG_TITLE_PRESENCE_ONLY",
        )
        self.assertEqual(
            witness["adjudication"]["physical_absence_of_g893_in_1908"],
            "NOT_PROVEN",
        )
        b = self.data["epistemic_boundaries"]
        self.assertEqual(b["negative_catalog_witness_as_physical_absence"], "FORBIDDEN")
        self.assertEqual(b["current_precious_status_backprojection_to_1908"], "FORBIDDEN")
        self.assertEqual(b["negative_catalog_witness_as_exact_item_identity"], "FORBIDDEN")
        self.assertEqual(b["negative_catalog_witness_as_target_value_evidence"], "FORBIDDEN")


    def test_1940_precious_catalog_closes_catalog_item_identity(self) -> None:
        witness = self.data["prewar_precious_catalog_1940"]
        self.assertEqual(witness["book_cd"], "GK26786_00")
        self.assertEqual(witness["item_cd"], "BBG")
        self.assertEqual(witness["renderer_page_count"], 148)
        header = witness["internal_catalog"]
        self.assertEqual(header["page_id"], "0125")
        self.assertEqual(header["title"], "奎章閣貴重圖書目錄")
        self.assertEqual(header["section"], "朝鮮本（一）")
        self.assertEqual(header["field_headers"], ["書名", "圖書番號", "冊數", "備考"])
        self.assertFalse(header["ocr_used"])
        entry = witness["target_entry"]
        self.assertEqual(entry["page_id"], "0129")
        self.assertEqual(entry["title"], "授時曆立成")
        self.assertEqual(entry["book_number"], 893)
        self.assertEqual(entry["volume_count"], 1)
        adjacent = witness["adjacent_control_entry"]
        self.assertEqual(adjacent["title"], "授時曆捷法立成")
        self.assertEqual(adjacent["book_number"], 892)
        self.assertEqual(witness["current_binding"]["current_catalog_identifier"], "奎貴893")
        self.assertEqual(witness["current_binding"]["current_book_cd"], "GK00893_00")
        self.assertEqual(
            witness["current_binding"]["status"],
            "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
        )
        self.assertEqual(
            self.data["adjudication"]["physical_leaf_or_seal_chain"],
            "NOT_SEPARATELY_PROVEN",
        )
        self.assertEqual(
            self.data["epistemic_boundaries"]["catalog_item_continuity_as_target_glyph_authority"],
            "FORBIDDEN",
        )

    def test_all_six_targets_remain_pending_with_zero_runtime_effect(self) -> None:
        self.assertEqual(len(self.data["target_controls"]), 6)
        self.assertEqual(self.data["target_status"], "ALL_SIX_PENDING_DIRECT_TARGET_PAGE")
        self.assertEqual(self.data["adjudication"]["target_folio_effect"], "NONE")
        self.assertEqual(self.data["adjudication"]["target_glyph_effect"], "NONE")
        self.assertEqual(
            self.data["epistemic_boundaries"]["algorithm_or_runtime_selection_effect"],
            "NONE",
        )


if __name__ == "__main__":
    unittest.main()
