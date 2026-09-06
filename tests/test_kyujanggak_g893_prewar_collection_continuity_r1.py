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

    def test_collection_continuity_does_not_become_item_identity(self) -> None:
        self.assertEqual(
            self.data["adjudication"]["collection_level_continuity"],
            "SUPPORTED_BY_OFFICIAL_SNU_HISTORY",
        )
        self.assertEqual(
            self.data["adjudication"]["exact_item_continuity_to_current_gk00893_00"],
            "UNRESOLVED",
        )
        self.assertFalse(
            self.data["prewar_object_family_witness"]["exact_identity_to_current_object"]
        )
        self.assertEqual(
            self.data["epistemic_boundaries"]["collection_continuity_as_individual_copy_identity"],
            "FORBIDDEN",
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

    def test_1930_catalog_is_directly_accessible_but_entry_is_still_unread(self) -> None:
        locator = self.data["prewar_catalog_locator"]
        self.assertEqual(locator["catalog_identifier"], "奎26775-v.1-7")
        access = locator["direct_digital_object_access"]
        self.assertEqual(access["book_cd"], "GK26775_00")
        self.assertEqual(access["item_cd"], "BBG")
        self.assertEqual(access["volume_ids"], ["0001","0002","0003","0004","0005","0006","0007"])
        self.assertTrue(access["renderer_bound"])
        self.assertFalse(access["ocr_used"])
        self.assertFalse(locator["g893_internal_entry_directly_read"])
        self.assertEqual(
            self.data["adjudication"]["prewar_catalog_digital_object_access"],
            "DIRECTLY_BOUND",
        )
        self.assertEqual(
            self.data["adjudication"]["exact_item_continuity_to_current_gk00893_00"],
            "UNRESOLVED",
        )
        self.assertEqual(
            self.data["epistemic_boundaries"]["prewar_catalog_locator_as_unread_item_binding"],
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
