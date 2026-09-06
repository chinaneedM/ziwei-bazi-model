from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs" / "research" / "KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1.json"


class KyujanggakG894DirectTargetPageBindingR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        cls.by_id = {item["control_id"]: item for item in cls.data["target_pages"]}

    def test_provider_object_identity_and_scope(self) -> None:
        self.assertEqual(self.data["schema"], "KYUJANGGAK-G894-DIRECT-TARGET-PAGE-BINDING-R1")
        self.assertEqual(self.data["catalog_identifier"], "奎貴894-v.1-3")
        self.assertEqual(self.data["book_cd"], "GK00894_00")
        self.assertEqual(self.data["item_cd"], "GJB")
        self.assertEqual(self.data["publication_year"], 1444)
        self.assertFalse(self.data["ocr_used"])
        self.assertEqual(self.data["runtime_effect"], "NONE")
        self.assertFalse(self.data["algorithm_reopen_authorized"])
        self.assertFalse(self.data["target_values_authorized_by_page_binding"])

    def test_all_six_controls_have_exact_provider_pages(self) -> None:
        expected = {
            "VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE": ("009b", "十六日"),
            "VAR-NUM-LUNAR-L8-LOSSGAIN": ("019b", "八限"),
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING": ("032a", "一百〇一限"),
            "VAR-NUM-LUNAR-L114-DAYRATE": ("034a", "一百一十四限"),
            "VAR-NUM-LUNAR-L124-JI-XINGDU": ("035a", "一百二十四限"),
            "VAR-NUM-LUNAR-L132-LOSSGAIN": ("036a", "一百三十二限"),
        }
        self.assertEqual(set(self.by_id), set(expected))
        for control_id, (page, heading) in expected.items():
            item = self.by_id[control_id]
            self.assertEqual(item["volume"], "0001")
            self.assertEqual(item["provider_page_id"], page)
            self.assertEqual(item["target_heading_visible"], heading)
            self.assertEqual(item["target_value_status"], "NOT_READ")
            self.assertEqual(len(item["image_sha256"]), 64)
            self.assertIn(page, item["direct_renderer_img_path"])

    def test_field_identity_is_not_silently_equated(self) -> None:
        table = self.data["table_identity_observation"]
        self.assertEqual(table["directly_visible_title"], "大陰限數遲疾度")
        self.assertIn("遲疾曆日率", table["directly_visible_field_labels"])
        self.assertIn("遲曆限行度", table["directly_visible_field_labels"])
        self.assertIn("疾曆限行度", table["directly_visible_field_labels"])
        self.assertEqual(table["same_table_family_as_identical_mechanical_field"], "NOT_ASSUMED")
        for item in self.data["target_pages"]:
            self.assertTrue(item["field_identity_status"].startswith("PENDING"))

    def test_epistemic_firewalls_remain_closed(self) -> None:
        boundaries = self.data["epistemic_boundaries"]
        for key in (
            "renderer_page_id_as_numeric_value",
            "img_filename_pattern_as_unobserved_page_evidence",
            "same_limit_number_as_same_field_semantics",
            "same_or_similar_field_name_as_mechanical_identity_without_contextual_philology",
            "g894_as_g893",
            "g894_as_sillok_same_physical_or_glyph_copy",
            "value_prepopulation_from_ming_goryeosa_sillok_ogawa",
            "source_count_as_variant_adjudication",
        ):
            self.assertEqual(boundaries[key], "FORBIDDEN")
        adjudication = self.data["adjudication"]
        self.assertEqual(adjudication["exact_target_page_binding_count"], 6)
        self.assertEqual(adjudication["direct_numeric_target_reading_count"], 0)
        self.assertEqual(adjudication["page_binding_gap_count"], 0)
        self.assertEqual(adjudication["field_identity_gap_count"], 6)


if __name__ == "__main__":
    unittest.main()
