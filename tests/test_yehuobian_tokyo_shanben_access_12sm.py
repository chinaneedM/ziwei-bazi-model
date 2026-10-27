import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json"
ACCESS = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-SHANBEN-ACCESS-BOUNDARY-R1.json"
SHARD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SM-SHANBEN-SOURCE-SHARD-R1.json"
MANIFEST = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
spec=importlib.util.spec_from_file_location("leaf_queue_12sm",ROOT/"scripts/verify-yehuobian-physical-leaf-attestation-r1.py")
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class Tokyo12SMAccessScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q=json.loads(QUEUE.read_text(encoding="utf-8"))
        cls.a=json.loads(ACCESS.read_text(encoding="utf-8"))
        cls.s=json.loads(SHARD.read_text(encoding="utf-8"))
        cls.m=json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.state=json.loads(STATE.read_text(encoding="utf-8"))

    def test_2009_policy_not_a_current_item_attestation(self):
        p=self.a["first_party"]
        self.assertEqual(p["recorded_scope_2009"]["class_A_titles"]+p["recorded_scope_2009"]["class_B_titles"],4630)
        self.assertIn("2009",p["source_policy_scope"])
        self.assertIs(p["target_leaf_in_this_database_seen"],False)
        for item in self.a["physical_targets"]:
            self.assertEqual(item["class_A_or_B"],"UNVERIFIED")
            self.assertEqual(item["availability"],"NOT_ITEM_SPECIFICALLY_VERIFIED")
        self.assertTrue(all(x is False for x in self.a["prohibited_claims"].values()))

    def test_manifest_and_copy_identity_are_consistent(self):
        self.assertEqual(self.s["sources"][0]["source_id"],"EXT-TOKYO-IASA-SHANBEN-AB-ACCESS-POLICY-12SM")
        self.assertIs(self.s["sources"][0]["physical_glyph_authority"],False)
        self.assertEqual(self.s["sources"][0]["verification_status"],"ACCESS_BOUNDARY_UNVERIFIED")
        self.assertGreaterEqual(self.m["extension_source_count"],9)
        self.assertEqual(self.m["combined_source_count"],self.m["root_source_count"]+self.m["extension_source_count"])
        self.assertEqual(self.state["historical_audit"]["external_source_registry_total_unique_count"],self.m["combined_source_count"])
        self.assertTrue(any(x["path"]=="docs/research/MING-DATONG-YEHUOBIAN-12SM-SHANBEN-SOURCE-SHARD-R1.json" and x["source_count"]==1 for x in self.m["shards"]))
        self.assertEqual(self.state["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(self.state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

    def test_initial_queue_admits_no_new_glyph_votes(self):
        self.assertEqual(gate.verify(self.q),{"status":"PASS","catalog_items":2,"admitted_target_glyph_votes":0})
        self.assertEqual(self.q["independent_target_glyph_votes"],0)

    def test_cannot_smuggle_glyph_into_undigitized_catalog_copy(self):
        x=copy.deepcopy(self.q)
        x["entries"][0]["collated_loci"]["WINTER_BEIJING_SUNRISE"]="辰初二刻"
        with self.assertRaisesRegex(ValueError,"unverified target leaf"):
            gate.verify(x)

    def test_cannot_claim_imaged_without_hashes_and_human_controls(self):
        x=copy.deepcopy(self.q)
        e=x["entries"][0]
        e["digital_access"]="ITEM_ORIGINAL_LEAF_VERIFIED"
        e["copy_image_identity_bound"]=True
        e["independent_target_glyph_vote"]=1
        x["independent_target_glyph_votes"]=1
        e["original_target_leaf"]={"source_url":"https://example.org/real-document","page":121}
        e["collated_loci"]={key:"unverified" for key in gate.LOCI}
        with self.assertRaisesRegex(ValueError,"sha256"):
            gate.verify(x)

    def test_future_bad_copy_id_or_sum_is_rejected(self):
        for key, value in (("physical_item","000000"),("cataloged_year",1700)):
            x=copy.deepcopy(self.q)
            x["entries"][1][key]=value
            with self.assertRaisesRegex(ValueError,"Tokyo NCID"):
                gate.verify(x)
        x=copy.deepcopy(self.q)
        x["independent_target_glyph_votes"]=1
        with self.assertRaisesRegex(ValueError,"aggregate vote"):
            gate.verify(x)

if __name__ == "__main__":
    unittest.main()
