from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs" / "research" / "KYUJANGGAK-G893-PROVENANCE-AND-PUBLIC-FIGURE-CONTROL-R1.json"
TOPOLOGY = ROOT / "docs" / "research" / "KYUJANGGAK-G893-IMAGE-ACCESS-TOPOLOGY-R1.json"
REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"


class KyujanggakG893ProvenancePublicFigureR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.control = json.loads(CONTROL.read_text(encoding="utf-8"))
        cls.topology = json.loads(TOPOLOGY.read_text(encoding="utf-8"))
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.by_source = {x["source_id"]: x for x in cls.registry["sources"]}

    def test_provider_range_is_kept_separate_from_exact_year(self) -> None:
        c = self.control
        self.assertEqual(c["source_id"], "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893")
        self.assertEqual(c["provider_catalog"]["date"], "15世紀前半（世宗年間 1418-1450）")
        self.assertFalse(c["provider_catalog"]["exact_print_year_stated"])
        adj = c["exact_print_year_adjudication"]
        self.assertEqual(adj["project_copy_level_value"], "UNRESOLVED_WITHIN_1418_1450_PROVIDER_RANGE")
        claims = {x["source_id"]: x["claim"] for x in adj["evidence"]}
        self.assertIn("1434", claims["EXT-KOSTMA-GAPJA-SHOUSHI-LICHENG-1434"])
        self.assertIn("1434", claims["EXT-LI-LIANG-LICHENG-TABLES-2018"])
        self.assertIn("1444", claims["EXT-LI-LIANG-SUNRISE-TABLES-2022"])
        self.assertIn("PRESERVE_1434_AND_1444", adj["disposition"])

    def test_source_registry_preserves_conflicting_secondary_dates(self) -> None:
        g = self.by_source["EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893"]
        self.assertEqual(
            g["exact_print_year_status"],
            "UNRESOLVED_WITHIN_SEJONG_1418_1450_PROVIDER_RANGE_CONFLICTING_1434_AND_1444_SECONDARY_REPORTS",
        )
        self.assertIn("EXT-LI-LIANG-SUNRISE-TABLES-2022", g["bibliographic_witnesses"])
        li22 = self.by_source["EXT-LI-LIANG-SUNRISE-TABLES-2022"]
        self.assertEqual(li22["doi"], "10.1484/M.PALS-EB.5.127700")
        self.assertIn("1444", li22["quality_notes"])
        self.assertIn("1434", self.by_source["EXT-LI-LIANG-LICHENG-TABLES-2018"]["quality_notes"])

    def test_public_figure_is_object_level_but_not_target_value_evidence(self) -> None:
        fig = self.control["public_object_figure"]
        self.assertEqual(fig["article_figure_number"], 1)
        self.assertIn("figure_001.jpg", fig["image_url"])
        visible = "\n".join(fig["directly_visible"])
        self.assertIn("授時曆立成卷上", visible)
        self.assertIn("嘉儀大夫太史令臣王恂奉敕撰", visible)
        self.assertIn("太陽冬至前後二象盈初縮末限", visible)
        self.assertIn("初日", visible)
        self.assertIn("八日", visible)
        self.assertFalse(fig["direct_target_control_visible"])
        self.assertFalse(fig["target_value_authorized"])

    def test_six_targets_remain_fail_closed(self) -> None:
        targets = self.control["six_target_status"]
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
        self.assertTrue(all(x["status"].startswith("PENDING_DIRECT_TARGET_PAGE") for x in targets))

    def test_thumbnail_tokens_are_not_mapped_to_public_figure(self) -> None:
        thumb = self.control["catalog_thumbnail_control"]
        self.assertEqual(thumb["item_cd"], "SIC")
        files = [x["image_file"] for x in thumb["directly_observed_links"]]
        self.assertEqual(files, [
            "GK00893_00IH_0001_000a.jpg",
            "GK00893_00IH_0001_004b.jpg",
        ])
        self.assertIn("NOT_ASSUMED", thumb["relation_to_public_figure"])
        self.assertEqual(thumb["target_folio_effect"], "NONE")

    def test_topology_and_runtime_firewalls_hold(self) -> None:
        self.assertEqual(self.topology["copy_date_boundary"]["status"], "EXACT_SURVIVING_COPY_PRINT_YEAR_UNRESOLVED")
        fig = self.topology["public_scholarly_object_figure"]
        self.assertFalse(fig["direct_target_control_visible"])
        self.assertFalse(fig["direct_target_folio_bound"])
        b = self.control["epistemic_boundaries"]
        self.assertEqual(b["public_opening_figure_as_d16_value"], "FORBIDDEN")
        self.assertEqual(b["goryeosa_or_ming_value_as_g893_prepopulation"], "FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"], "NONE")


if __name__ == "__main__":
    unittest.main()
