from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "docs" / "research" / "JOSEON-1444-CHILJEONGSAN-EARLY-TABLE-WITNESS-ROUTES-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
LEDGER = ROOT / "docs" / "research" / "MING-DATONG-1569-CROSS-EDITION-VARIANT-LEDGER-R1.json"


class Joseon1444ChiljeongsanWitnessRoutesR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.routes = json.loads(ROUTES.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.by_source = {x["source_id"]: x for x in cls.registry["sources"]}

    def test_g894_is_provider_dated_1444_but_separate_from_g893(self) -> None:
        g = self.routes["witnesses"]["kyujanggak_g894"]
        self.assertEqual(g["catalog_identifier"], "奎貴894-v.1-3")
        self.assertEqual(g["edition"], "甲寅字")
        self.assertEqual(g["publication_year"], 1444)
        self.assertEqual(g["observed_catalog_image_surface_book_cd"], "GK00894_00")
        self.assertTrue(g["original_images_advertised"])
        self.assertTrue(g["original_text_advertised"])
        self.assertIn("SEPARATE_WORK_AND_SEPARATE_CATALOG_OBJECT", g["relationship_to_g893"])
        self.assertEqual(g["target_glyph_authority"], "PENDING_EXACT_PAGE_BINDING")

    def test_sillok_official_table_family_and_leaf_locations_are_bound(self) -> None:
        s = self.routes["witnesses"]["sejong_sillok_v156"]
        self.assertEqual(s["solar"]["article_id"], "wda_50016011")
        self.assertEqual(s["solar"]["title"], "太陽冬至前後二象盈初縮末限")
        self.assertEqual(s["solar"]["taebaeksan_location"], "60冊 156卷 6張 A面")
        self.assertEqual(s["lunar"]["article_id"], "wda_50016016")
        self.assertEqual(s["lunar"]["title"], "太陰限數遲疾度")
        self.assertEqual(s["lunar"]["taebaeksan_location"], "60冊 156卷 13張 A面")
        self.assertEqual(s["original_image_infrastructure"]["current_project_exact_target_image_ids"], "NOT_YET_EXTRACTED")

    def test_six_targets_are_not_prepopulated(self) -> None:
        targets = self.routes["target_controls"]
        self.assertEqual(len(targets), 6)
        ids = {x["control_id"] for x in targets}
        self.assertEqual(ids, {
            "VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE",
            "VAR-NUM-LUNAR-L8-LOSSGAIN",
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING",
            "VAR-NUM-LUNAR-L114-DAYRATE",
            "VAR-NUM-LUNAR-L124-JI-XINGDU",
            "VAR-NUM-LUNAR-L132-LOSSGAIN",
        })
        self.assertTrue(all("PENDING" in x["g894_status"] for x in targets))
        self.assertTrue(all("PENDING" in x["sillok_status"] for x in targets))
        self.assertTrue(all(x["g893_effect"] == "NONE" for x in targets))

    def test_registry_keeps_three_joseon_sources_distinct(self) -> None:
        for source_id in (
            "EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444",
            "EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES",
            "EXT-NIKH-CHILJEONGSAN-HISTORY-1444",
        ):
            self.assertIn(source_id, self.by_source)
        g894 = self.by_source["EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444"]
        self.assertEqual(g894["publication_year"], 1444)
        self.assertIn("NOT_THE_G893_TEXT", g894["source_role"])
        sillok = self.by_source["EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES"]
        self.assertEqual(sillok["solar_table"]["article_id"], "wda_50016011")
        self.assertEqual(sillok["lunar_table"]["article_id"], "wda_50016016")

    def test_cross_edition_ledger_adds_routes_without_closing_g893(self) -> None:
        witnesses = {x["source_id"]: x for x in self.ledger["comparison_witnesses"]}
        self.assertIn("EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444", witnesses)
        self.assertIn("EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES", witnesses)
        route = self.ledger["joseon_1444_chiljeongsan_witness_routes"]
        self.assertEqual(route["g894_provider_publication_year"], 1444)
        self.assertEqual(route["sillok_solar_binding"]["article_id"], "wda_50016011")
        self.assertEqual(route["sillok_lunar_binding"]["article_id"], "wda_50016016")
        self.assertEqual(route["relationship_to_g893"], "INDEPENDENT_SAME_PERIOD_COMPARISON_ROUTES_NOT_SUBSTITUTES")
        self.assertEqual(route["source_count_adjudication"], "FORBIDDEN")
        self.assertEqual(route["runtime_effect"], "NONE")
        g893 = self.ledger["independent_physical_image_adjudication"]
        self.assertTrue(all(x["target_reading_status"] == "PENDING_DIRECT_IMAGE" for x in g893["targets"]))

    def test_epistemic_firewalls_hold(self) -> None:
        b = self.routes["epistemic_boundaries"]
        self.assertEqual(b["g894_as_g893"], "FORBIDDEN")
        self.assertEqual(b["adjacent_call_number_as_shared_copy_genealogy"], "FORBIDDEN")
        self.assertEqual(b["sejong_sillok_table_as_1444_g894_same_glyph_surface"], "FORBIDDEN")
        self.assertEqual(b["article_embedded_image_as_read_numeric_value"], "FORBIDDEN")
        self.assertEqual(b["viewer_url_pattern_as_target_image_binding"], "FORBIDDEN")
        self.assertEqual(b["composition_year_as_surviving_sillok_copy_date"], "FORBIDDEN")
        self.assertEqual(b["value_prepopulation_from_ming_goryeosa_ogawa"], "FORBIDDEN")
        self.assertEqual(b["source_count_as_variant_adjudication"], "FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"], "NONE")


if __name__ == "__main__":
    unittest.main()
