import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

class Tokyo12SOPhysicalFormatAndHistoricalImagePolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load("docs/research/MING-DATONG-YEHUOBIAN-12SO-TOKYO-PRINT-IDENTITY-AND-HISTORIC-DIGITIZATION-R1.json")
        cls.s=load("docs/research/MING-DATONG-YEHUOBIAN-12SO-TOKYO-2005-DIGITIZATION-SOURCE-SHARD-R1.json")
        cls.m=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
        cls.state=load("docs/PROJECT-CURRENT-STATE-R1.json")
        cls.q=load("docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json")

    def test_2005_historical_scope_not_current_access(self):
        p=self.r["historic_official_handout"]
        self.assertEqual(p["internal_date"],"2005-12-15")
        self.assertEqual(p["web_2005_titles"],537)
        self.assertIn("FIRST_TEN",p["historical_access_policy"]["class_B"])
        self.assertEqual(p["historical_access_policy"]["class_indicator_in_list"],"NOT_SHOWN_AS_OF_2005_HANDOUT")
        self.assertEqual(p["source_surrogate_sequence"][-1],"historical web 120dpi JPEG")
        self.assertNotEqual(p["source_surrogate_sequence"][2],p["source_surrogate_sequence"][3])
        self.assertTrue(all(x["verification_status"]=="ACCESS_BOUNDARY_UNVERIFIED" and not x["physical_glyph_authority"] for x in self.s["sources"]))

    def test_two_print_records_distinct_and_target_leaf_unbound(self):
        items=self.r["direct_catalog_recheck"]["items"]
        self.assertEqual({(x["ncid"],x["physical_item"],x["fascicles"]) for x in items},{
            ("BC0492354X","6403767830",34),("BB23196128","6403148395",20)})
        self.assertEqual({tuple(x["inner_frame_cm"]) for x in items},{(18.4,13.2),(18.2,13.1)})
        self.assertTrue(all(x["public_target_leaf_seen"] is False and x["public_target_page_number"] is None and x["independent_glyph_vote"]==0 for x in items))
        self.assertIn("補遺卷4",items[0]["copy_notes_scope"])
        self.assertIn("卷30",items[1]["copy_notes_scope"])
        self.assertEqual(self.r["claims"]["independent_target_glyph_votes_added"],0)
        self.assertEqual(self.q["independent_target_glyph_votes"],0)
        self.assertEqual(self.r["claims"]["lineage_edges_added"],0)

    def test_opac_403_does_not_claim_nonholding(self):
        o=self.r["direct_catalog_recheck"]["precise_opac_openurl_probe"]
        self.assertEqual(o["results_observed"],"WEB_FETCH_HTTP_403_FOR_BOTH_AT_2026_10_12")
        self.assertIn("not proof",o["scope"])
        self.assertTrue(o["items_visited_by_source_emitted_catalog_links_only"])

    def test_source_manifest_forward_only_and_formal_batch_unchanged(self):
        sh=self.s["sources"][0]
        self.assertEqual(sh["source_id"],"EXT-TOKYO-IOC-2005-HANJI-DIGITIZATION-PRACTICE-12SO")
        self.assertEqual(self.m["extension_source_count"],11)
        self.assertEqual(self.m["combined_source_count"],658)
        self.assertEqual(self.state["historical_audit"]["external_source_registry_total_unique_count"],658)
        self.assertTrue(any(x["path"]=="docs/research/MING-DATONG-YEHUOBIAN-12SO-TOKYO-2005-DIGITIZATION-SOURCE-SHARD-R1.json" and x["source_count"]==1 for x in self.m["shards"]))
        self.assertEqual(len(self.state["historical_audit"]["completed_batches"]),487)
        self.assertTrue(self.state["historical_audit"]["latest_batch_doc"].endswith("-QD.md"))
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)

if __name__=="__main__":
    unittest.main()
