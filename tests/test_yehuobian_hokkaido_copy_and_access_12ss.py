import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/research/MING-DATONG-YEHUOBIAN-12SS-HOKKAIDO-COPY-PROVENANCE-AND-SERVICE-GATES-R1.json"
SHARD = "docs/research/MING-DATONG-YEHUOBIAN-12SS-HOKKAIDO-ACCESS-SOURCE-SHARD-R1.json"
MANIFEST = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = "docs/PROJECT-CURRENT-STATE-R1.json"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class HokkaidoCopyAndAccess12SS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(RECORD)
        cls.s=load(SHARD)
        cls.m=load(MANIFEST)
        cls.st=load(STATE)

    def test_catalog_seal_is_bibliographic_not_provenance_chain_or_same_copy(self):
        c=self.r["copy"]
        self.assertEqual((c["ncid"],c["item"],c["fascicle"]),("BB10385966","0181427762","卷19-20"))
        self.assertEqual(c["source_catalog_notes"]["former_institutional_seal_exact"],"東方文化學院東京研究所の蔵書印あり")
        self.assertEqual(c["source_catalog_notes"]["seal_evidence_class"],"CATALOG_DESCRIBES_PHYSICAL_SEAL_NOT_DIRECT_SEAL_PHOTOGRAPHY")
        self.assertEqual(c["source_catalog_notes"]["transfer_chain"],"UNRESOLVED")
        self.assertEqual(c["online_target_image"],"NOT_OBSERVED")
        self.assertEqual(len(c["four_locus_readings"]),4)
        self.assertTrue(all(value is None for value in c["four_locus_readings"].values()))
        self.assertTrue(all(self.r["chronology_firewall"].values()))

    def test_actual_item_access_not_inferred_from_general_ill(self):
        access=self.r["official_access"]
        self.assertTrue(access["rare_book_interlibrary_loan_excluded"])
        self.assertTrue(access["main_rare_materials_room_ordinary_copy_excluded"])
        self.assertFalse(access["item_is_confirmed_in_main_rare_materials_room"])
        self.assertEqual(access["item_specific_copy_permitted"],"UNDETERMINED")
        self.assertEqual(access["item_specific_photography_permitted"],"UNDETERMINED")
        self.assertEqual(access["actual_item_copy_fee"],"UNDETERMINED")
        self.assertEqual(access["publication_rights"],"NOT_GRANTED")
        self.assertEqual(set(access["public_form_scope"]),{"ITEM_HOLDING","ITEM_BIBLIOGRAPHY","LIBRARY_USAGE_RULES"})
        self.assertTrue(all(n == 0 for n in self.r["external_actions"].values()))

    def test_source_shard_registered_and_forward_only(self):
        sources=self.s["sources"]
        self.assertEqual(len(sources),1)
        self.assertEqual(sources[0]["source_id"],"EXT-HOKKAIDO-UNIVERSITY-LIBRARY-ILL-EXCLUSIONS-12SS")
        self.assertFalse(sources[0]["physical_glyph_authority"])
        self.assertEqual(sources[0]["verification_status"],"ACCESS_BOUNDARY_UNVERIFIED")
        items=self.m["shards"]
        self.assertEqual(sum(x["path"]==SHARD for x in items),1)
        self.assertEqual(len(items),len({x["path"] for x in items}))
        self.assertGreaterEqual(self.m["extension_source_count"],12)
        self.assertEqual(self.m["extension_source_count"],sum(x["source_count"] for x in items))
        self.assertEqual(self.m["combined_source_count"],self.m["root_source_count"]+self.m["extension_source_count"])
        audit=self.st["historical_audit"]
        self.assertEqual(audit["external_source_registry_total_unique_count"],self.m["combined_source_count"])
        self.assertEqual(audit["external_source_registry_extension_count"],self.m["extension_source_count"])
        self.assertGreaterEqual(len(audit["completed_batches"]),487)
        self.assertGreaterEqual(audit["row_count"],222)
        self.assertEqual(audit["row_count"],audit["audited_row_count"])
        self.assertEqual(self.r["parent_batch"],"12QE_OPEN")
        self.assertEqual(self.r["invariant_snapshot"]["independent_target_glyph_votes_added"],0)
        self.assertEqual(self.r["invariant_snapshot"]["formal_batch_delta"],0)
        self.assertEqual(self.st["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.st["invariants"]["algorithm_reopen_count"],0)
        self.assertTrue(any(x.startswith("12SS HOKKAIDO") for x in audit["current_focus"]))

if __name__=="__main__":
    unittest.main()
