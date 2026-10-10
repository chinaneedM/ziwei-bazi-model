"""Regression gates for 12PZ physical-copy identity and source scope.

These tests distinguish copies, digital files, editions, historical chronology,
and deterministic charting. They do not assert a universal old20v target reading.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research"
LEDGER = RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-PRIMARY-WITNESS-BOUNDARY-LEDGER-R1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Yehuobian12PZWitnessBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = load(LEDGER)
        cls.by_id = {v["id"]: v for v in cls.ledger["witnesses"]}
        cls.original = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-NCL02260-PART2-RECEIVED-XUBIAN12-DIRECT-HEADING-R1.json")
        cls.shanghai = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-SHANGHAI30-GAIZAO-LOUKE-P441-P442-DIRECT-COLLATION-R1.json")
        cls.official = load(RESEARCH / "ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-R1.json")
        cls.variants = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-NCL02260-02261-PHYSICAL-PREFACE-BINGWU-BINGCHEN-DIRECT-COMPARISON-R1.json")

    def test_disjoint_material_copy_keys_not_digital_segment_count(self) -> None:
        self.assertEqual(len(self.by_id), len(self.ledger["witnesses"]))
        copies = [x["copy_key"] for x in self.ledger["witnesses"]]
        self.assertEqual(len(set(copies)), 4)
        a = self.by_id["TAIWAN_NCL02260_OLD20_MANUSCRIPT"]
        self.assertEqual(len(a["digital_parts"]), 2)
        self.assertEqual([x["pdf_pages"] for x in a["digital_parts"]], [1000, 35])
        self.assertEqual(a["counts_for_shen_defu_old20v_target"], 0)
        self.assertEqual(self.by_id["TAIWAN_NCL02261_GREEN_GRID_OLD20"]["counts_for_shen_defu_old20v_target"], 0)

    def test_exact_runner_pdf2_hash_and_facing_page_indices_are_source_scoped(self) -> None:
        physical = self.by_id["TAIWAN_NCL02260_OLD20_MANUSCRIPT"]
        self.assertEqual(physical["digital_parts"][1]["pdf_sha256"], self.original["source"]["source_sha256"])
        workflow = self.original["workflow_attestation_20261010"]
        self.assertEqual(workflow["run_conclusion"], "success")
        self.assertEqual(workflow["downloaded_pdf"]["pdf_pages"], 35)
        self.assertEqual(workflow["downloaded_pdf"]["sha256"], physical["digital_parts"][1]["pdf_sha256"])
        checksums = {x["pdf_page_1based"]: x["rendered_jpeg_sha256"] for x in workflow["derived_images"]}
        self.assertEqual(set(checksums), {3, 4, 5, 6})
        self.assertEqual(len(set(checksums.values())), 4)
        self.assertEqual(self.original["followup_source_page_pair_20261010"]["observed_pdf_page_1based_4"]["reading"], "萬曆野獲續編卷第十二目")
        self.assertEqual(self.original["followup_source_page_pair_20261010"]["observed_pdf_page_1based_5"]["reading"], "萬曆野獲續編卷第十二")
        self.assertFalse(workflow["artifact_zip_sha256_independently_downloaded_and_recomputed"])

    def test_1447_memorial_is_one_preexisting_official_primary_record(self) -> None:
        official = self.by_id["CHINA_NLC_YINGZONG_SHILU_V160_1447"]
        self.assertEqual(official["source_pdf_sha256"], self.official["physical_source"]["source_pdf_sha256"])
        self.assertEqual(official["target_pdf_pages_1based"], [28])
        self.assertEqual(self.official["secure_direct_reading"]["beijing_winter"], "冬至日出辰初一刻，入申正二刻，夜刻六十二")
        self.assertEqual(self.official["secure_direct_reading"]["imperial_response"], "上令內官監改造")
        self.assertEqual(sum(x["counts_for_1447_official_record"] for x in self.ledger["witnesses"]), 1)
        self.assertIn("clock construction completion", official["does_not_prove"])

    def test_shanghai_30v_physical_glyph_is_not_1827_print_or_old20(self) -> None:
        shanghai = self.by_id["SHANGHAI_REORGANIZED_30V_MANUSCRIPT"]
        self.assertEqual(shanghai["source_pdf_sha256"], self.shanghai["witness"]["source_pdf_sha256"])
        self.assertEqual(shanghai["target_pdf_pages_1based"], [441, 442])
        self.assertEqual(self.shanghai["physical_pages"][0]["visible_heading"], "改造漏刻")
        field = {x["field"]: x["source_text"] for x in self.shanghai["field_collation"]}
        self.assertEqual(field["BEIJING_WINTER_SUNRISE"], "辰初一刻")
        self.assertEqual(field["PALACE_CLOCK_ADOPTION"], "時禁中宮漏循用新製不待言")
        self.assertEqual(self.shanghai["witness"]["source_1827_fulishanfang_equivalence"], "NOT_PROVEN")
        self.assertEqual(sum(x.get("counts_for_reorganized_30v_target", 0) for x in self.ledger["witnesses"]), 1)
        self.assertEqual(sum(x["counts_for_shen_defu_old20v_target"] for x in self.ledger["witnesses"]), 0)

    def test_two_manuscript_prefaces_are_distinct_not_a_genealogy(self) -> None:
        ids = {x["witness_id"]: x["direct_year_glyphs"] for x in self.variants["source_witnesses"]}
        self.assertEqual(ids, {"NCL-02260": "丙午", "NCL-02261": "丙辰"})
        self.assertEqual(self.variants["comparison"]["physical_witness_count"], 2)
        self.assertEqual(self.variants["comparison"]["inferred_independent_textual_lineages"], "NOT_ESTABLISHED")
        self.assertEqual(sum(x.get("counts_for_old20_preface_variant", 0) for x in self.ledger["witnesses"]), 2)

    def test_gates_and_unresolved_original_are_never_auto_promoted(self) -> None:
        missing = {x["target"] for x in self.ledger["not_yet_collated"]}
        self.assertIn("original old20 改造漏刻 heading and folio", missing)
        self.assertIn("edition/copy-identified 1827 扶荔山房 print physical target leaf", missing)
        gate = self.ledger["gates"]
        self.assertFalse(gate["batch_closed"])
        self.assertFalse(gate["chart_algorithm_changed"])
        self.assertFalse(gate["matrix_changed"])
        self.assertEqual(gate["deterministic_product_r1"], "CLOSED")
        self.assertEqual(gate["md_g03"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(gate["hpa_dayun_cal_002"], "MISSING_FROM_PRODUCT")
        self.assertTrue(self.ledger["prohibitions"]["original20v_equivalent_to_categorized30v_volume20"] is False)


if __name__ == "__main__":
    unittest.main()
