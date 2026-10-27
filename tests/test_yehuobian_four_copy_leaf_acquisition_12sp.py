import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))

class FourCopyLeafAcquisition12SP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=load("docs/research/MING-DATONG-YEHUOBIAN-12SP-FOUR-COPY-LEAF-ACQUISITION-PACKET-R1.json")
        cls.state=load("docs/PROJECT-CURRENT-STATE-R1.json")
        cls.shard=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
        cls.tokyo=load("docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json")

    def test_four_source_scoped_distinct_holdings_and_targets(self):
        p=self.p
        self.assertEqual(p["parent_batch"],"12QE_OPEN")
        l=[x for lib in p["libraries"] for x in lib["holdings"]]
        self.assertEqual(len(l),4)
        self.assertEqual({(x["ncid"],x["physical_item"]) for x in l},{
            ("BC0492354X","6403767830"),("BB23196128","6403148395"),
            ("BB18578034","188987L"),("BB05477307","200023037620")})
        self.assertTrue(all("20" in x["volume_binding"] for x in l))
        self.assertIsNone(l[2]["catalog_impression_year"])
        self.assertEqual(len(p["four_loci"]),4)
        self.assertIs(p["anti_leakage_controls"]["no_reading_prepopulated_for_these_four_holdings"],True)

    def test_no_outbound_activity_or_claimed_target_page(self):
        self.assertTrue(all(v==0 for v in self.p["external_actions"].values()))
        self.assertIs(self.p["invariants"]["official_request_sent"],False)
        self.assertIs(self.p["invariants"]["official_copy_permission_obtained"],False)
        self.assertEqual(self.p["invariants"]["independent_target_glyph_votes_added"],0)
        self.assertEqual(self.tokyo["independent_target_glyph_votes"],0)
        self.assertTrue(all(x["original_target_leaf"] is None and not x["copy_image_identity_bound"]
                            for x in self.tokyo["entries"]))
        self.assertFalse(self.p["requested_minimal_reproduction"]["public_dissemination_authorized"])

    def test_forward_only_semantic_scope(self):
        h=self.state["historical_audit"]
        self.assertTrue(h["latest_batch_doc"].endswith("-QD.md"))
        self.assertGreaterEqual(len(h["completed_batches"]),487)
        self.assertEqual(h["external_source_registry_total_unique_count"],
                         self.shard["combined_source_count"])
        self.assertGreaterEqual(self.shard["combined_source_count"],658)
        self.assertEqual(self.p["invariants"]["source_registry_delta"],0)
        self.assertEqual(self.p["invariants"]["formal_batch_enrollment_delta"],0)
        self.assertEqual(self.p["invariants"]["graph_node_delta"],0)
        self.assertEqual(self.p["invariants"]["graph_edge_delta"],0)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)

if __name__=="__main__": unittest.main()
