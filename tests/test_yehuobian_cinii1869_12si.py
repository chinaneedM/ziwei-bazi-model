import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
EVIDENCE = BASE / "docs/research/MING-DATONG-YEHUOBIAN-12SI-TOKYO-1869-PRINT-CATALOG-BOUNDARY-R1.json"
SHARD = BASE / "docs/research/MING-DATONG-YEHUOBIAN-12SI-CINII1869-SOURCE-SHARD-R1.json"
MANIFEST = BASE / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = BASE / "docs/PROJECT-CURRENT-STATE-R1.json"

class TestYehuobian1869CatalogGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.shard = json.loads(SHARD.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))

    def test_exact_cinii_holding(self):
        c = self.e["catalog_object"]
        self.assertEqual(c["ncid"], "BB23196128")
        self.assertEqual(c["volume"], "卷19-20")
        self.assertEqual(c["call_number"], "倉石文庫:20128:11")
        self.assertEqual(c["item_number"], "6403148395")
        self.assertIn("1869", c["catalog_imprint"])

    def test_bibliographic_not_glyph_or_runtime(self):
        c = self.e["catalog_object"]
        self.assertIs(c["holding_target_page_digitized_and_read"], False)
        self.assertIs(c["physical_copy_date_independently_attested"], False)
        for name, value in self.e["claims_fail_closed"].items():
            self.assertIs(value, False, name)
        self.assertEqual(self.e["transmission_impact"]["edges_supported"], [])
        self.assertEqual(self.shard["sources"][0]["verification_status"], "BIBLIOGRAPHIC_METADATA_ONLY")
        self.assertIs(self.shard["sources"][0]["physical_glyph_authority"], False)

    def test_counts_and_formal_batch_invariant(self):
        source = self.shard["sources"][0]
        self.assertEqual(source["evidence"], "docs/research/MING-DATONG-YEHUOBIAN-12SI-TOKYO-1869-PRINT-CATALOG-BOUNDARY-R1.json")
        self.assertEqual(self.e["parent_research_batch"], "12QE_OPEN")
        # At 12SI the union was 647+8=655; subsequent append-only shards are valid.
        self.assertEqual(self.manifest["root_source_count"], 647)
        self.assertGreaterEqual(self.manifest["extension_source_count"], 8)
        self.assertEqual(self.manifest["combined_source_count"],
                         self.manifest["root_source_count"] + self.manifest["extension_source_count"])
        self.assertTrue(any(s["path"] == "docs/research/MING-DATONG-YEHUOBIAN-12SI-CINII1869-SOURCE-SHARD-R1.json" and s["source_count"] == 1 for s in self.manifest["shards"]))
        audit = self.state["historical_audit"]
        self.assertEqual((audit["external_source_registry_root_count"], audit["external_source_registry_extension_count"], audit["external_source_registry_total_unique_count"]),
                         (self.manifest["root_source_count"], self.manifest["extension_source_count"], self.manifest["combined_source_count"]))
        self.assertEqual((audit["row_count"], audit["audited_row_count"]), (222, 222))
        self.assertTrue(audit["latest_batch_doc"].endswith("-QD.md"))
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"], 0)

if __name__ == "__main__":
    unittest.main()
