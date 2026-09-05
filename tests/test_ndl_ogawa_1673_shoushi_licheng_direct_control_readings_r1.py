from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs" / "research" / "NDL-OGAWA-1673-SHOUSHI-LICHENG-DIRECT-CONTROL-READINGS-R1.json"
SCRIPT = ROOT / "scripts" / "research_ndl_ogawa_shoushi_licheng_target_pages.py"


class NdlOgawa1673ShoushiLichengDirectControlReadingsR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(PATH.read_text(encoding="utf-8"))
        cls.controls = {x["control_id"]: x for x in cls.data["controls"]}

    def test_source_and_reproduction_are_no_ocr_and_directly_bound(self) -> None:
        self.assertEqual(self.data["source_id"], "EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673")
        self.assertEqual(self.data["publication_date"], "寛文13 [1673]")
        self.assertFalse(self.data["ocr_used"])
        self.assertFalse(self.data["cross_copy_page_offset_used"])
        r = self.data["reproduction"]
        self.assertEqual(r["full_probe_workflow_run_id"], 33975487368)
        self.assertEqual(r["full_probe_artifact_id"], 9972186258)
        self.assertEqual(r["page_fetch_workflow_run_id"], 33975870344)
        self.assertEqual(r["page_fetch_artifact_id"], 9972290306)
        self.assertEqual(r["native_page_fetch_head_sha"], "f90477b4247f6c7bfc70f58f68082c0638947cf5")
        self.assertEqual(r["native_page_fetch_workflow_run_id"], 33977235461)
        self.assertEqual(r["native_page_fetch_artifact_id"], 9972676923)
        self.assertEqual(r["native_page_fetch_width_px"], 7392)
        self.assertEqual(
            r["native_page_fetch_artifact_sha256"],
            "81c99a8952dfbabf80c9d2cb9e95093b06aca734bf9a7d19e1c70d3ec567e216",
        )
        self.assertEqual(r["d16_locator_revision_head_sha"], "f5b1b362a3fcb5816da9231b2eb43824d50b8c6e")
        self.assertEqual(r["d16_locator_revision_workflow_run_id"], 33978788314)
        self.assertEqual(r["d16_locator_revision_artifact_id"], 9973124845)
        self.assertEqual(
            r["d16_locator_revision_artifact_sha256"],
            "1e259e9ba7c8c6393b8b9d9674981022e23f27bda7823868714e2320189232f8",
        )
        self.assertEqual(r["d16_locator_revision_width_px"], 7392)
        self.assertFalse(r["native_fetch_authorizes_target_values"])

    def test_independent_same_edition_holding_does_not_promote_glyph_evidence(self) -> None:
        b = self.data["bibliographic_corroboration"]
        kyushu = b["kyushu_university_independent_holding"]
        self.assertEqual(kyushu["publication_date"], "寛文13年 [1673]")
        self.assertTrue(kyushu["public_domain"])
        self.assertIn("manifest", kyushu["iiif_manifest"])
        self.assertIn("NOT_YET_TARGET_GLYPH_EVIDENCE", kyushu["role"])
        self.assertEqual(
            self.data["epistemic_boundaries"]["independent_same_edition_catalog_as_target_glyph"],
            "FORBIDDEN",
        )

    def test_d16_is_structurally_noncomparable_not_inferred(self) -> None:
        v = self.controls["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"]
        self.assertEqual(v["table_opening_canvas_index"], 3)
        self.assertEqual(v["table_opening_image_id"], "R0000003")
        self.assertEqual(v["day16_context_canvas_index"], 4)
        self.assertEqual(v["day16_context_image_id"], "R0000004")
        self.assertFalse(v["target_value_authorized"])
        self.assertIn("STRUCTURALLY_NOT_PRINTED", v["diplomatic_reading_status"])
        s = self.data["structural_scope"]
        self.assertEqual(s["solar_table_title"], "太陽盈縮立成")
        self.assertEqual(s["solar_visible_schema"], ["積日", "盈縮積度", "盈縮加分"])
        self.assertIn("NOT_DIRECTLY_COMPARABLE", s["solar_d16_difference_status"])
        self.assertEqual(
            self.data["epistemic_boundaries"]["absent_solar_difference_column_as_inferred_numeric_value"],
            "FORBIDDEN",
        )

    def test_l114_direct_reading_is_3489(self) -> None:
        v = self.controls["VAR-NUM-LUNAR-L114-DAYRATE"]
        self.assertEqual(v["canvas_index"], 19)
        self.assertEqual(v["image_id"], "R0000019")
        self.assertEqual(v["printed_limit_heading"], "一百十四限")
        self.assertEqual(v["direct_surface"], "九日三四八九")
        self.assertEqual(v["normalized_value"], "9日3489")
        self.assertTrue(v["target_value_authorized"])

    def test_l124_overbinding_is_rejected_and_not_numeric_evidence(self) -> None:
        v = self.controls["VAR-NUM-LUNAR-L124-JI-XINGDU"]
        self.assertFalse(v["target_value_authorized"])
        self.assertIn("FIELD_BINDING_REJECTED", v["diplomatic_reading_status"])
        self.assertEqual(
            self.data["structural_scope"]["l124_ji_xingdu_status"],
            "NO_SEPARATE_JI_XINGDU_TABLE_IDENTIFIED_IN_COMPLETE_PID_14488128_VOLUME2_SEQUENCE_FIELD_NOT_DIRECTLY_COMPARABLE_YET",
        )
        self.assertEqual(self.data["epistemic_boundaries"]["chiji_page_as_ji_xingdu_evidence"], "FORBIDDEN")
        self.assertEqual(self.data["epistemic_boundaries"]["absence_of_separate_column_as_numeric_zero_or_variant"], "FORBIDDEN")

    def test_pending_lunar_controls_are_not_silently_promoted(self) -> None:
        for cid in (
            "VAR-NUM-LUNAR-L8-LOSSGAIN",
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING",
            "VAR-NUM-LUNAR-L132-LOSSGAIN",
        ):
            self.assertFalse(self.controls[cid]["target_value_authorized"], cid)
            self.assertIn("7392PX", self.controls[cid]["direct_page_status"])
            self.assertIn("SPLIT_VERTICAL_TYPESETTING", self.controls[cid]["diplomatic_reading_status"])

    def test_runtime_and_authority_firewalls_hold(self) -> None:
        b = self.data["epistemic_boundaries"]
        self.assertEqual(b["page_fetch_as_target_value"], "FORBIDDEN")
        self.assertEqual(b["native_resolution_fetch_as_target_value"], "FORBIDDEN")
        self.assertEqual(b["later_1673_japanese_witness_as_early_g893_substitute"], "FORBIDDEN")
        self.assertEqual(b["later_1673_japanese_witness_as_ming_1569_edition_authority"], "FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"], "NONE")

    def test_fetch_script_localizes_d16_opening_and_does_not_map_l124(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        target_block = text.split("TARGETS = {", 1)[1].split("}\nUNRESOLVED_CONTROLS", 1)[0]
        self.assertIn('3: ["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE_LOCATOR_CANDIDATE"]', target_block)
        self.assertIn('4: ["SOLAR-D16-CONTEXT-ADD-ACCUMULATED-COLUMNS"]', target_block)
        self.assertNotIn("VAR-NUM-LUNAR-L124-JI-XINGDU", target_block)
        self.assertIn("VAR-NUM-LUNAR-L124-JI-XINGDU", text)
        self.assertIn("UNRESOLVED_CONTROLS", text)


if __name__ == "__main__":
    unittest.main()
