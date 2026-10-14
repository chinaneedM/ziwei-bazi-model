#!/usr/bin/env python3
"""12VL first-party Berlin catalog sample must not become a target original-glyph vote."""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/research/MING-DATONG-YEHUOBIAN-12VL-BERLIN-1827-SAMPLE-DIGITAL-OBJECT"
E = json.loads((ROOT / (BASE+"-R1.json")).read_text(encoding="utf-8"))
S = json.loads((ROOT / (BASE+"-SOURCE-SHARD-R1.json")).read_text(encoding="utf-8"))
H = json.loads((ROOT / "docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))

class BerlinCatalogGate(unittest.TestCase):
    def test_link_is_source_issued_and_sample_only(self):
        obj = E["objects"][1]
        self.assertEqual(obj["ppn"], "PPN334378186X")
        self.assertTrue(obj["link_derivation"].startswith("DDB provided"))
        self.assertIn("PPN334378186X", obj["url"])
        self.assertEqual(E["access_observations"]["ddb_public_catalog"], "VISIBLE_WITH_BEISPIELSEITEN_SAMPLE_LABEL")
        self.assertEqual(E["objects"][0]["target_volume_or_leaf_present_in_public_sample"], "UNVERIFIED")
    def test_no_promoted_image_or_glyph(self):
        self.assertEqual(E["access_observations"]["original_target_glyph_votes"], 0)
        self.assertIsNone(E["access_observations"]["juan20_original_page_sha256"])
        self.assertEqual(E["objects"][1]["juan20_target_image"], "NOT_OBTAINED")
        self.assertEqual(S["sources"][0]["physical_glyph_authority"], False)
        self.assertEqual(S["sources"][0]["verification_status"], "BIBLIOGRAPHIC_METADATA_ONLY")
        self.assertEqual(H["invariants"]["algorithm_reopen_count"], 0)
        self.assertEqual(H["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
    def test_new_catalog_not_eight_item_original_queue(self):
        self.assertEqual(E["accounting"]["original_tokyo_1827_1869_glyph_votes"], 0)
        self.assertEqual(E["transmission_impact"]["nodes_added_or_strengthened"], [])
        self.assertEqual(E["transmission_impact"]["edges_supported"], [])
        self.assertEqual(len(S["sources"]), 1)
        self.assertEqual(E["accounting"]["total_unique_sources"], 691)
        manifest = json.loads((ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json").read_text())
        self.assertGreaterEqual(manifest["combined_source_count"], 691)
        self.assertEqual(manifest["combined_source_count"], manifest["root_source_count"] + manifest["extension_source_count"])
        self.assertEqual(H["historical_audit"]["external_source_registry_total_unique_count"], manifest["combined_source_count"])

if __name__ == "__main__":
    unittest.main()
