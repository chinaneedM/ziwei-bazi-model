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
        self.assertTrue(self.data["target_values_authorized_by_page_binding"])

    def test_all_six_controls_have_exact_provider_pages(self) -> None:
        expected = {
            "VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE": ("009b", "十六日"),
            "VAR-NUM-LUNAR-L8-LOSSGAIN": ("019b", "八限"),
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING": ("032a", "一百〇一限"),
            "VAR-NUM-LUNAR-L114-DAYRATE": ("034a", "一百一十四限"),
            "VAR-NUM-LUNAR-L124-JI-XINGDU": ("035a", "一百二十四限"),
            "VAR-NUM-LUNAR-L132-LOSSGAIN": ("036b", "一百三十二限"),
        }
        self.assertEqual(set(self.by_id), set(expected))
        for control_id, (page, heading) in expected.items():
            item = self.by_id[control_id]
            self.assertEqual(item["volume"], "0001")
            self.assertEqual(item["provider_page_id"], page)
            self.assertEqual(item["target_heading_visible"], heading)
            self.assertEqual(len(item["image_sha256"]), 64)
            self.assertIn(page, item["direct_renderer_img_path"])

    def test_direct_lunar_readings_are_closed(self) -> None:
        expected = {
            "VAR-NUM-LUNAR-L8-LOSSGAIN": ("益一十〇分五六〇一七七五", "10.5601775"),
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING": ("五度二十〇四八一一二五", "5.20481125"),
            "VAR-NUM-LUNAR-L114-DAYRATE": ("九日三四八九", "9日3489"),
            "VAR-NUM-LUNAR-L124-JI-XINGDU": ("疾一度〇二八一", "1.0281"),
            "VAR-NUM-LUNAR-L132-LOSSGAIN": ("損七分八八六〇七五", "7.886075"),
        }
        for control_id, (surface, normalized) in expected.items():
            item = self.by_id[control_id]
            self.assertEqual(item["target_value_status"], "DIRECT_NATIVE_GLYPH_READING_COMPLETE")
            self.assertEqual(item["direct_surface"], surface)
            self.assertEqual(item["normalized_value"], normalized)
            self.assertEqual(item["reading_confidence"], "HIGH")
            self.assertTrue(item["field_identity_status"].startswith("DIRECTLY_MAPPED"))

    def test_solar_d16_is_structurally_noncomparable(self) -> None:
        item = self.by_id["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"]
        self.assertEqual(item["field_identity_status"], "TARGET_SECOND_NUMERIC_DIFFERENCE_COLUMN_STRUCTURALLY_ABSENT")
        self.assertEqual(item["target_value_status"], "STRUCTURALLY_NONCOMPARABLE_NO_G894_VALUE")
        self.assertIsNone(item["target_value"])
        self.assertEqual(item["substitution_for_missing_field"], "FORBIDDEN")

    def test_correct_six_column_header_is_preserved(self) -> None:
        table = self.data["table_identity_observation"]
        self.assertEqual(table["directly_visible_title"], "大陰限數遲疾度")
        self.assertEqual(
            table["directly_visible_field_labels"],
            ["限數", "遲疾曆日率", "損益分", "遲疾度", "疾曆限行度", "遲曆限行度"],
        )

    def test_epistemic_firewalls_remain_closed(self) -> None:
        boundaries = self.data["epistemic_boundaries"]
        for key in (
            "renderer_page_id_as_numeric_value",
            "img_filename_pattern_as_unobserved_page_evidence",
            "g894_as_g893",
            "g894_as_sillok_same_physical_or_glyph_copy",
            "value_prepopulation_from_ming_goryeosa_sillok_ogawa",
            "source_count_as_variant_adjudication",
            "structurally_absent_field_as_zero_blank_or_neighboring_column",
        ):
            self.assertEqual(boundaries[key], "FORBIDDEN")
        adjudication = self.data["adjudication"]
        self.assertEqual(adjudication["exact_target_page_binding_count"], 6)
        self.assertEqual(adjudication["directly_mapped_lunar_field_count"], 5)
        self.assertEqual(adjudication["direct_numeric_target_reading_count"], 5)
        self.assertEqual(adjudication["structurally_noncomparable_control_count"], 1)
        self.assertEqual(adjudication["page_binding_gap_count"], 0)
        self.assertEqual(adjudication["field_identity_gap_count"], 0)


if __name__ == "__main__":
    unittest.main()
