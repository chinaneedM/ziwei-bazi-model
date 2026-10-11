import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SN-TOKYO-IOC-REPRODUCTION-SERVICE-R1.json"
SHARD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SN-IOC-REPRODUCTION-SERVICE-SOURCE-SHARD-R1.json"
MANIFEST = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
QUEUE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json"

class Tokyo12SNReproductionServiceScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.s = json.loads(SHARD.read_text(encoding="utf-8"))
        cls.m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.state = json.loads(STATE.read_text(encoding="utf-8"))
        cls.q = json.loads(QUEUE.read_text(encoding="utf-8"))

    def test_first_party_service_not_copy_access_attestation(self):
        self.assertEqual(self.r["parent_batch"], "12QE_OPEN")
        self.assertEqual(len(self.r["first_party_pages"]), 4)
        self.assertTrue(all(x["url"].startswith("https://www.ioc.u-tokyo.ac.jp/") for x in self.r["first_party_pages"]))
        g = self.r["acquisition_gate"]
        for k in ("official_inquiry_submitted", "rare_copy_application_submitted",
                  "reading_reservation_submitted", "permission_granted", "fees_confirmed",
                  "individual_postal_copy_supported"):
            self.assertIs(g[k], False)
        self.assertIn("SERVICE_POLICY", self.r["evidence_grade"])

    def test_two_distinct_copy_objects_and_no_glyph_vote(self):
        expected = {("BC0492354X", "6403767830", 1827), ("BB23196128", "6403148395", 1869)}
        self.assertEqual({(x["ncid"], x["physical_item"], x["cataloged_year"]) for x in self.r["physical_targets"]}, expected)
        self.assertTrue(all(x["physical_target_image_attested"] is False and
                            x["specific_folio"] == "UNLOCATED" and
                            x["copy_or_microfilm_eligibility"] == "UNVERIFIED_PER_ITEM"
                            for x in self.r["physical_targets"]))
        self.assertEqual(self.q["independent_target_glyph_votes"], 0)
        self.assertEqual(self.r["counts"]["source_glyph_votes_delta"], 0)
        self.assertEqual(self.r["transmission_impact"]["edges_supported"], [])

    def test_shard_and_manifest_forward_only(self):
        self.assertEqual(self.s["sources"][0]["source_id"], "EXT-TOKYO-IOC-RARE-BOOK-REPRODUCTION-AND-APPLICATION-12SN")
        self.assertIs(self.s["sources"][0]["physical_glyph_authority"], False)
        self.assertEqual(self.s["sources"][0]["verification_status"], "ACCESS_BOUNDARY_UNVERIFIED")
        self.assertEqual(self.m["extension_source_count"], 10)
        self.assertEqual(self.m["combined_source_count"], 657)
        self.assertEqual(self.state["historical_audit"]["external_source_registry_total_unique_count"], 657)
        self.assertEqual(self.state["historical_audit"]["external_source_registry_extension_count"], 10)
        self.assertTrue(any(x["path"] == "docs/research/MING-DATONG-YEHUOBIAN-12SN-IOC-REPRODUCTION-SERVICE-SOURCE-SHARD-R1.json" and x["source_count"] == 1 for x in self.m["shards"]))

    def test_parent_and_product_invariants_not_reopened(self):
        h = self.state["historical_audit"]
        self.assertTrue(h["latest_batch_doc"].endswith("-QD.md"))
        self.assertEqual(len(h["completed_batches"]), 487)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"], "CLOSED")
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"], 0)
        self.assertEqual(self.r["invariants"]["algorithm_reopens"], 0)

if __name__ == "__main__":
    unittest.main()
