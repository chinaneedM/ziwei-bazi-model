from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs"/"research"/"KYUJANGGAK-G893-IMAGE-ACCESS-TOPOLOGY-R1.json"

class KyujanggakG893ImageAccessTopologyR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))

    def test_catalog_exposes_concrete_image_filename_surface_without_target_binding(self) -> None:
        self.assertEqual(self.data["source_id"],"EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893")
        self.assertEqual(self.data["book_cd"],"GK00893_00")
        self.assertEqual(self.data["item_cd"],"SIC")
        self.assertFalse(self.data["ocr_used"])
        self.assertFalse(self.data["target_glyphs_read"])
        self.assertFalse(self.data["direct_target_folio_bound"])
        files=[x["image_file"] for x in self.data["catalog_exposed_thumbnail_links"]]
        self.assertEqual(files,["GK00893_00IH_0001_000a.jpg","GK00893_00IH_0001_004b.jpg"])

    def test_access_topology_cannot_be_promoted_to_glyph_evidence(self) -> None:
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["thumbnail_filename_as_target_folio_binding"],"FORBIDDEN")
        self.assertEqual(b["sample_thumbnail_as_target_glyph_reading"],"FORBIDDEN")
        self.assertEqual(b["filename_volume_token_as_textual_volume_proof"],"FORBIDDEN")
        self.assertEqual(b["secondary_article_figure_as_target_glyph_authority"],"FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"],"NONE")

    def test_all_six_targets_remain_explicitly_pending(self) -> None:
        self.assertEqual(len(self.data["target_controls"]),6)
        self.assertIn("VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE",self.data["target_controls"])
        self.assertIn("NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING",self.data["target_controls"])

if __name__=="__main__":
    unittest.main()
