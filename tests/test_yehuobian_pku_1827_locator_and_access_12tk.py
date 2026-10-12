"""12TK first-party PKU access controls must not masquerade as ancient glyph witnesses."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = "docs/research/MING-DATONG-YEHUOBIAN-12TK-PKU-ACCESS-AND-1827-LOCATOR-R1.json"
SHARD = "docs/research/MING-DATONG-YEHUOBIAN-12TK-PKU-ACCESS-AND-1827-SOURCE-SHARD-R1.json"
MANIFEST = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE = "docs/PROJECT-CURRENT-STATE-R1.json"
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class Pku1827Locator12TK(unittest.TestCase):
    def test_access_not_physical_source(self):
        rec, shard = load(RESEARCH), load(SHARD)
        self.assertEqual(len(shard["sources"]), 3)
        self.assertEqual([x["source_id"] for x in shard["sources"]], rec["source_registry"]["new_source_ids"])
        self.assertEqual([x["verification_status"] for x in shard["sources"]], [
            "BIBLIOGRAPHIC_METADATA_ONLY", "ACCESS_BOUNDARY_UNVERIFIED", "UNVERIFIED_TARGET_LOCATOR_QUARANTINED"])
        self.assertTrue(all(x["physical_glyph_authority"] is False for x in shard["sources"]))
        self.assertTrue(all(x["evidence"] == RESEARCH for x in shard["sources"]))
        self.assertFalse(rec["secondary_candidate"]["first_party_pku_holding_record_seen"])
        self.assertIsNone(rec["secondary_candidate"]["pku_accession_id"])
        self.assertFalse(rec["secondary_candidate"]["identical_to_xuxiu1174_base_copy"])
        self.assertFalse(rec["primary_institutional_pages"][1]["item_specific_1827_permission"])
        self.assertFalse(rec["primary_institutional_pages"][1]["claim_that_vol20_direct_photo_will_be_approved"])
        self.assertTrue(rec["primary_institutional_pages"][1]["no_contact_submitted"])
        self.assertEqual(rec["decision"]["permission_requests_submitted"],0)
        self.assertEqual(rec["decision"]["new_direct_1827_source_folios"],0)
        self.assertEqual(rec["decision"]["new_direct_1869_source_folios"],0)
        self.assertEqual(rec["decision"]["independent_original_target_glyph_votes"],0)
        self.assertFalse(rec["decision"]["algorithm_reopen"])
        self.assertEqual(rec["transmission_impact"]["edges_supported"],[])

    def test_registry_state_forward_only(self):
        rec, m, state = load(RESEARCH), load(MANIFEST), load(STATE)
        audit = state["historical_audit"]
        specs = [x for x in m["shards"] if x["path"] == SHARD]
        self.assertEqual(len(specs),1)
        self.assertEqual(specs[0]["source_count"],3)
        self.assertGreaterEqual(m["extension_source_count"],18)
        self.assertEqual(m["extension_source_count"],sum(x["source_count"] for x in m["shards"]))
        self.assertEqual(m["combined_source_count"],m["root_source_count"]+m["extension_source_count"])
        self.assertEqual(audit["external_source_registry_root_count"],m["root_source_count"])
        self.assertEqual(audit["external_source_registry_extension_count"],m["extension_source_count"])
        self.assertEqual(audit["external_source_registry_total_unique_count"],m["combined_source_count"])
        self.assertGreaterEqual(len(audit["completed_batches"]),487)
        self.assertEqual(audit["row_count"],222)
        self.assertEqual(audit["repaired_provenance_metadata_defect_count"],45)
        self.assertTrue(any(x.startswith("12TK PKU FIRST-PARTY") for x in audit["current_focus"]))
        self.assertEqual(state["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(state["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(state["invariants"]["candidate_collapse_count"],0)
        self.assertEqual(rec["source_registry"]["new_shard"],SHARD)

if __name__=="__main__":
    unittest.main()
