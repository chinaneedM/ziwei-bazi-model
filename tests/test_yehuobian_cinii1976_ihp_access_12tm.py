"""12TM: 1976 five-volume institution evidence is not the exact ancient original."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = "docs/research/MING-DATONG-YEHUOBIAN-12TM-CINII1976-IHP-IMAGE-POLICY-R1.json"
S = "docs/research/MING-DATONG-YEHUOBIAN-12TM-CINII1976-IHP-SOURCE-SHARD-R1.json"
M = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
H = "docs/PROJECT-CURRENT-STATE-R1.json"
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))

class IHP1976SourceScope12TM(unittest.TestCase):
    def test_1976_item_not_1827_physical_glyph(self):
        e,s=load(E),load(S)
        b=e["bibliographic_independent_recheck"]
        self.assertEqual(b["ncid"],"BA59231697")
        self.assertEqual(b["published_parts"],5)
        self.assertEqual(b["catalog_libraries_listed"],15)
        self.assertEqual(b["publication_date"],"1976-09")
        self.assertTrue(b["japanese_national_library_crosscheck"]["same_underlying_CiNii_bibliographic_record"])
        self.assertFalse(b["barcode174009_same_as_facsimile_base_proven"])
        self.assertFalse(b["digital_target_images_available_from_catalog"])
        self.assertEqual(len(s["sources"]),3)
        self.assertEqual([v["source_id"] for v in s["sources"]],e["source_registry"]["source_ids"])
        self.assertTrue(all(v["physical_glyph_authority"] is False for v in s["sources"]))
        self.assertEqual([v["verification_status"] for v in s["sources"]],["BIBLIOGRAPHIC_METADATA_ONLY","ACCESS_BOUNDARY_UNVERIFIED","ACCESS_BOUNDARY_UNVERIFIED"])
        self.assertTrue(all(v["evidence"]==E for v in s["sources"]))
        self.assertFalse(e["archive_access_policies"]["resource_policy"]["worldwide_individual_remote_fullimage_entitlement"])
        self.assertFalse(e["archive_access_policies"]["third_party_application_policy"]["service_eligibility_of_barcode174009_confirmed"])
        self.assertFalse(e["request_packet_unsubmitted"]["external_email_or_form_submitted"])
        self.assertEqual(e["adjudication"]["new_independent_ancient_glyph_votes"],0)
        self.assertEqual(e["adjudication"]["direct_source_copy_edges_added"],0)
        self.assertEqual(e["transmission_impact"]["edges_supported"],[])
        self.assertEqual(e["adjudication"]["algorithms_reopened"],0)

    def test_live_registry_monotone_and_product_closed(self):
        e,m,h=load(E),load(M),load(H)
        a=h["historical_audit"]
        spec=[v for v in m["shards"] if v["path"]==S]
        self.assertEqual(len(spec),1)
        self.assertEqual(spec[0]["source_count"],3)
        self.assertGreaterEqual(m["combined_source_count"],671)
        self.assertEqual(m["extension_source_count"],sum(v["source_count"] for v in m["shards"]))
        self.assertEqual(m["combined_source_count"],m["root_source_count"]+m["extension_source_count"])
        self.assertEqual(a["external_source_registry_total_unique_count"],m["combined_source_count"])
        self.assertEqual(a["external_source_registry_extension_count"],m["extension_source_count"])
        self.assertGreaterEqual(len(a["completed_batches"]),487)
        self.assertEqual(a["row_count"],222)
        self.assertEqual(a["repaired_provenance_metadata_defect_count"],45)
        self.assertTrue(any(x.startswith("12TM CINII") for x in a["current_focus"]))
        self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
        self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(h["invariants"]["candidate_collapse_count"],0)

if __name__=="__main__": unittest.main()
