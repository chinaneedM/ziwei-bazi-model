from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs" / "research" / "SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1.json"


class SillokChiljeongsanNativeDirectCollationR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        cls.by_id = {item["control_id"]: item for item in cls.data["lunar_controls"]}

    def test_scope_and_reproduction_are_fail_closed(self) -> None:
        self.assertEqual(
            self.data["schema"],
            "SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1",
        )
        self.assertFalse(self.data["ocr_used"])
        self.assertEqual(self.data["runtime_effect"], "NONE")
        self.assertEqual(self.data["audit_batch"], "BATCH-11-BAZI-JOSEON-SILLOK-NATIVE-COLLATION-O")
        self.assertFalse(self.data["algorithm_reopen_authorized"])
        self.assertEqual(self.data["reproduction"]["native_page_workflow_run_id"], 34015344051)
        self.assertEqual(self.data["reproduction"]["native_page_artifact_id"], 9983778498)
        self.assertEqual(self.data["solar_control"]["status"], "PENDING_DIRECT_SOLAR_TABLE_CONTINUATION_IMAGE")
        self.assertIsNone(self.data["solar_control"]["target_value"])
        self.assertEqual(
            self.data["solar_navigation_evidence"]["official_image_tree_walk"]["outcome"],
            "START_API_UNAVAILABLE",
        )

    def test_five_lunar_controls_are_directly_read(self) -> None:
        self.assertEqual(len(self.by_id), 5)
        expected = {
            "VAR-NUM-LUNAR-L8-LOSSGAIN": ("益一十〇分五六〇一七七五", "10.5601775"),
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING": ("五度二十〇四八一一二五", "5.20481125"),
            "VAR-NUM-LUNAR-L114-DAYRATE": ("九日三四八九", "9日3489"),
            "VAR-NUM-LUNAR-L124-JI-XINGDU": ("疾一度〇二八一", "1.0281"),
            "VAR-NUM-LUNAR-L132-LOSSGAIN": ("損七分八八六〇七五", "7.886075"),
        }
        for control_id, (surface, normalized) in expected.items():
            item = self.by_id[control_id]
            self.assertEqual(item["direct_surface"], surface)
            self.assertEqual(item["normalized_value"], normalized)
            self.assertEqual(item["reading_confidence"], "HIGH")
            self.assertEqual(item["image_size"], [2560, 3616])

    def test_l101_and_l132_preserve_explicit_zero(self) -> None:
        l101 = self.by_id["NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING"]
        self.assertEqual(l101["explicit_place_groups"], ["5", "20", "48", "11", "25"])
        self.assertIn("二十〇", l101["direct_surface"])
        l132 = self.by_id["VAR-NUM-LUNAR-L132-LOSSGAIN"]
        self.assertIn("八八六〇七五", l132["direct_surface"])

    def test_l124_is_direct_ming_lineage_counter_control(self) -> None:
        l124 = self.by_id["VAR-NUM-LUNAR-L124-JI-XINGDU"]
        self.assertEqual(l124["comparison"]["ming_1569_primary"], "1.0281")
        self.assertEqual(l124["comparison"]["goryeosa_received_facsimile"], "1.0821")
        self.assertIn("DIRECTLY_SUPPORTS_THE_1_0281", l124["finding"])

    def test_epistemic_boundaries_do_not_promote_source_or_runtime(self) -> None:
        boundaries = self.data["epistemic_boundaries"]
        for key in (
            "sillok_as_g894_same_physical_copy",
            "sillok_as_g893_same_physical_copy",
            "viewer_token_as_numeric_value",
            "value_prepopulation_into_pending_g894_or_g893",
            "source_count_as_variant_adjudication",
        ):
            self.assertEqual(boundaries[key], "FORBIDDEN")
        self.assertEqual(boundaries["algorithm_or_runtime_selection_effect"], "NONE")
        self.assertTrue(self.data["adjudication"]["g894_target_values_still_pending"])
        self.assertTrue(self.data["adjudication"]["g893_target_values_still_pending"])


if __name__ == "__main__":
    unittest.main()
