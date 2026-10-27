from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs"/"research"/"KANG-BO-SHOUSHI-JIEFA-LICHENG-PUBLIC-MEDIA-WITNESS-R1.json"

class KangBoShoushiJiefaLichengPublicMediaWitnessR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))

    def test_public_media_bind_surviving_object_without_ocr(self) -> None:
        self.assertEqual(self.data["title"],"《授時曆捷法立成》")
        self.assertEqual(self.data["author"],"姜保")
        self.assertEqual(len(self.data["public_media"]),3)
        self.assertTrue(all(x["direct_pixels_observed"] for x in self.data["public_media"]))
        self.assertTrue(all(x["ocr_used"] is False for x in self.data["public_media"]))
        self.assertEqual(
            {x["media_role"] for x in self.data["public_media"]},
            {"VOLUME_UPPER_OPENING_PAGE","COVER","DOUBLE_PAGE_TABLE_SPREAD"},
        )

    def test_two_textual_volumes_and_one_bound_book_are_not_forced_into_conflict(self) -> None:
        rel=self.data["philological_relation"]
        self.assertIn("two-volume",rel["li_2023_description"])
        self.assertIn("one bound book",rel["aks_entry_description"])
        self.assertFalse(rel["same_text_as_g893"])
        self.assertIn("TWO_TEXTUAL_VOLUMES_CAN_BE_BOUND_AS_ONE_PHYSICAL_BOOK",rel["reconciliation"])

    def test_derived_korean_witness_cannot_replace_g893_or_ming_primary(self) -> None:
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["sample_media_as_complete_book_collation"],"FORBIDDEN")
        self.assertEqual(b["kang_bo_derived_table_as_g893_target_value"],"FORBIDDEN")
        self.assertEqual(b["derived_korean_work_as_ming_1569_edition_authority"],"FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"],"NONE")

if __name__=="__main__":
    unittest.main()
