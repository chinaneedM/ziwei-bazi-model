from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READING = ROOT / "docs" / "research" / "KYUSHU-OGAWA-1673-SHOUSHI-LICHENG-DIRECT-COLLATION-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
SCRIPT = ROOT / "scripts" / "research_kyushu_ogawa_shoushi_licheng_target_pages.py"


class KyushuOgawa1673ShoushiLichengDirectCollationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(READING.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_exact_reproduction_is_no_ocr_and_bound_to_successful_artifact(self) -> None:
        self.assertEqual(self.data["source_id"], "EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673")
        self.assertEqual(self.data["publication_date"], "寛文13年 [1673]")
        self.assertFalse(self.data["ocr_used"])
        self.assertFalse(self.data["cross_copy_page_offset_used"])
        r = self.data["reproduction"]
        self.assertEqual(r["head_sha"], "8cd6d20dda9c7038daac3db884c3c1ea6b86c6f9")
        self.assertEqual(r["workflow_run_id"], 34010515542)
        self.assertEqual(r["workflow_conclusion"], "success")
        self.assertEqual(r["artifact_id"], 9982311056)
        self.assertEqual(
            r["artifact_digest"],
            "sha256:bf85126c4d4a16ad4be17e28b089d921b8f7f1b986bf4bd2f480b4a308bb5944",
        )
        self.assertEqual(r["native_page_size"], [6592, 4672])
        self.assertFalse(r["target_values_authorized_by_fetch"])

    def test_source_registry_distinguishes_ndl_and_kyushu_holdings(self) -> None:
        by_id = {x["source_id"]: x for x in self.registry["sources"]}
        self.assertIn("EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673", by_id)
        self.assertIn("EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673", by_id)
        kyushu = by_id["EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673"]
        self.assertTrue(kyushu["public_domain"])
        self.assertEqual(kyushu["workflow_run_id"], 34010515542)
        self.assertIn("DIRECT_PUBLIC_DOMAIN_IIIF_IMAGE_WITNESS", kyushu["source_role"])

    def test_d16_is_independently_structural_not_numeric(self) -> None:
        d16 = self.data["findings"]["solar_d16"]
        self.assertEqual(d16["visible_table"], "太陽盈縮立成")
        self.assertEqual(d16["result"], "FIELD_STRUCTURALLY_NOT_DIRECTLY_COMPARABLE")
        self.assertIsNone(d16["direct_raw_target_value"])
        self.assertIn("neither 5.1362 nor 5.2362", d16["finding"])

    def test_same_copy_symmetry_controls_are_explicit_and_not_over_normalized(self) -> None:
        f = self.data["findings"]
        self.assertIn("IDENTICAL", f["l8_l159_symmetry"]["relation"])
        self.assertEqual(f["l8_l159_symmetry"]["normalized_value"], "NOT_FORCED_FROM_PHOTOGRAPH_ALONE")
        self.assertIn("IDENTICAL", f["l35_l132_symmetry"]["relation"])
        self.assertEqual(f["l35_l132_symmetry"]["normalized_value"], "NOT_FORCED_FROM_PHOTOGRAPH_ALONE")
        self.assertIn("DIFFERENT_VISIBLE_ZERO_PLACE_GROUP_SURFACE", f["l67_l101_positional"]["relation"])
        self.assertEqual(f["l67_l101_positional"]["normalized_value"], "NOT_REDERIVED_FROM_PHOTOGRAPH_ALONE")

    def test_l114_direct_reading_is_3489(self) -> None:
        l114 = self.data["findings"]["l114"]
        self.assertEqual(l114["direct_surface"], "九日三四八九")
        self.assertEqual(l114["normalized_value"], "9日3489")
        self.assertEqual(l114["reading_confidence"], "HIGH")

    def test_limit_xingdu_table_is_typed_as_derived_layer_not_raw_xingdu(self) -> None:
        schema = self.data["findings"]["lunar_limit_xingdu_schema"]
        self.assertEqual(schema["visible_table_title"], "遲疾限行度")
        self.assertEqual(schema["visible_fields"], ["疾曆限行度", "遲曆限行度"])
        self.assertEqual(schema["initial_limit_direct_normalized_controls"]["疾曆限行度"], "0.0679314")
        self.assertEqual(schema["initial_limit_direct_normalized_controls"]["遲曆限行度"], "0.0832064")
        self.assertIn("RECIPROCAL_SHORTCUT_NOT_RAW", schema["ming_1569_correspondence"]["relation"])

    def test_l124_is_derived_lineage_control_and_excludes_received_counterfactual(self) -> None:
        l124 = self.data["findings"]["l124"]
        self.assertFalse(l124["raw_ji_xingdu_directly_printed"])
        self.assertIsNone(l124["direct_raw_ji_xingdu_value"])
        self.assertEqual(l124["direct_derived_values"]["疾曆限行度"], "0.0797587")
        self.assertEqual(l124["direct_derived_values"]["遲曆限行度"], "0.0704164")
        self.assertEqual(l124["ming_1569_link"]["raw_ji_xingdu"], "1.0281")
        self.assertEqual(l124["goryeosa_received_variant_counterfactual"]["raw_ji_xingdu"], "1.0821")
        self.assertEqual(l124["goryeosa_received_variant_counterfactual"]["derived_truncate_7dp"], "0.0757785")
        self.assertFalse(l124["goryeosa_received_variant_counterfactual"]["printed_in_kyushu_l124_ji_derived_field"])
        self.assertEqual(
            l124["classification"],
            "MECHANICALLY_LINKED_DERIVED_CONTROL_SUPPORTS_MING_1_0281_LINEAGE_NOT_DIRECT_RAW_GLYPH",
        )

    def test_epistemic_firewalls_and_fetch_script_hold(self) -> None:
        b = self.data["epistemic_boundaries"]
        self.assertEqual(b["l124_derived_control_as_direct_raw_ji_xingdu_glyph"], "FORBIDDEN")
        self.assertEqual(b["same_named_or_related_table_as_same_numeric_layer"], "FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"], "NONE")
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("SYM-LUNAR-L35-LOSSGAIN-ZERO", text)
        self.assertIn("SYM-LUNAR-L67-CHIJI-DEGREE-ZERO", text)
        self.assertIn("SYM-LUNAR-L159-LOSSGAIN", text)
        self.assertIn("STRUCTURAL_AND_FIELD_IDENTITY_ADJUDICATION_ONLY_NOT_A_DIRECT_JI_XINGDU_VALUE", text)
        self.assertIn("A_PRINTED_COLUMN_IN_A_SAME_NAMED_OR_RELATED_TABLE_MUST_NOT_BE_ASSUMED_EQUIVALENT", text)


if __name__ == "__main__":
    unittest.main()
