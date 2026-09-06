from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs" / "research" / "KYUJANGGAK-G894-LUNAR-FIELD-SEMANTIC-BRIDGE-R1.json"


class KyujanggakG894LunarFieldSemanticBridgeR1Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        cls.by_field = {item["g894_field"]: item for item in cls.data["field_bridge"]}

    def test_direct_header_is_six_columns(self) -> None:
        self.assertEqual(
            self.data["direct_header"]["columns"],
            ["限數", "遲疾曆日率", "損益分", "遲疾度", "疾曆限行度", "遲曆限行度"],
        )
        correction = self.data["direct_header"]["correction_to_prior_in_progress_artifact"]
        self.assertEqual(correction["incorrect_label"], "遲疾益分")
        self.assertEqual(correction["corrected_label"], "損益分")
        self.assertEqual(correction["omitted_label_restored"], "遲疾度")

    def test_g894_own_method_prose_closes_mechanics(self) -> None:
        headings = {item["heading"]: item for item in self.data["direct_method_fragments"]}
        self.assertIn("求經朔弦望入遲疾曆及限數", headings)
        self.assertIn("求遲疾差", headings)
        self.assertIn("求加減差", headings)
        self.assertIn("損益分乘之如八百二十而一", headings["求遲疾差"]["stable_surface"])
        self.assertIn("以八百二十乘之", headings["求加減差"]["stable_surface"])
        self.assertIn("遲疾限下行度除之", headings["求加減差"]["stable_surface"])

    def test_active_control_fields_have_direct_mechanical_identity(self) -> None:
        expected = {
            "遲疾曆日率": "LUNAR_LIMIT_DAY_RATE_ANCHOR",
            "損益分": "LUNAR_WITHIN_LIMIT_INTERPOLATION_INCREMENT",
            "遲疾度": "LUNAR_LIMIT_BASE_CHIJI_CORRECTION",
            "疾曆限行度": "LUNAR_JI_HALF_LIMIT_LINE_SPEED_DENOMINATOR",
        }
        for field, identity in expected.items():
            self.assertEqual(self.by_field[field]["mechanical_identity"], identity)

    def test_solar_d16_missing_field_is_not_synthesized(self) -> None:
        solar = self.data["solar_d16_scope"]
        self.assertEqual(solar["target_field_presence"], "STRUCTURALLY_ABSENT_IN_G894_SOLAR_TABLE")
        self.assertIsNone(solar["direct_numeric_reading"])
        self.assertIn("DO_NOT_SUBSTITUTE", solar["disposition"])

    def test_no_runtime_or_witness_collapse(self) -> None:
        self.assertEqual(self.data["runtime_effect"], "NONE")
        self.assertFalse(self.data["algorithm_reopen_authorized"])
        boundaries = self.data["epistemic_boundaries"]
        self.assertEqual(boundaries["g894_as_g893"], "FORBIDDEN")
        self.assertEqual(boundaries["g894_as_sillok_same_glyph_surface"], "FORBIDDEN")
        self.assertEqual(boundaries["source_count_as_variant_adjudication"], "FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
