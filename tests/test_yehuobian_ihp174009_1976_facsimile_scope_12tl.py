"""12TL independent original copy vs modern 1976 facsimile and publication claim."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/MING-DATONG-YEHUOBIAN-12TL-IHP174009-1976-FACSIMILE-PROVENANCE-R1.json"
S="docs/research/MING-DATONG-YEHUOBIAN-12TL-IHP174009-1976-SOURCE-SHARD-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
H="docs/PROJECT-CURRENT-STATE-R1.json"
def read(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
class IHPFacsimileScope12TL(unittest.TestCase):
 def test_source_scope_and_independence(self):
  e,s=read(E),read(S)
  self.assertEqual(e["original_manuscript"]["holding_barcode"],"174009")
  self.assertEqual(e["original_manuscript"]["official_digitization_label"],"已數位化")
  self.assertEqual(e["modern_facsimile"]["callmark"],"II-5-1318")
  self.assertEqual(e["modern_facsimile"]["publication_year"],1976)
  self.assertEqual(len(s["sources"]),3)
  self.assertEqual([r["source_id"] for r in s["sources"]],e["source_registry"]["source_ids"])
  self.assertTrue(all(r["physical_glyph_authority"] is False for r in s["sources"]))
  self.assertTrue(all(r["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" for r in s["sources"]))
  self.assertTrue(all(r["evidence"]==E for r in s["sources"]))
  self.assertFalse(e["original_manuscript"]["digital_image_public_access_confirmed"])
  self.assertFalse(e["original_manuscript"]["ncl02260_direct_copy_edge_proven"])
  self.assertFalse(e["modern_facsimile"]["catalog_proves_original_IHP_barcode_174009_same_exemplar"])
  self.assertFalse(e["secondary_scholarly_attribution"]["ihp_barcode174009_same_1976_exemplar_proven"])
  self.assertEqual(e["adjudication"]["new_target_article_glyph_votes"],0)
  self.assertEqual(e["adjudication"]["new_verified_independent_1827_print_votes"],0)
  self.assertEqual(e["adjudication"]["new_verified_independent_1869_repair_votes"],0)
  self.assertEqual(e["transmission_impact"]["edges_supported"],[])
  self.assertFalse(e["adjudication"]["algorithm_reopen"])
 def test_forward_source_manifest(self):
  m,h,e=read(M),read(H),read(E)
  a=h["historical_audit"]
  specs=[i for i in m["shards"] if i["path"]==S]
  self.assertEqual(len(specs),1)
  self.assertEqual(specs[0]["source_count"],3)
  self.assertGreaterEqual(m["extension_source_count"],21)
  self.assertEqual(m["extension_source_count"],sum(x["source_count"] for x in m["shards"]))
  self.assertEqual(m["combined_source_count"],m["root_source_count"]+m["extension_source_count"])
  self.assertEqual(a["external_source_registry_extension_count"],m["extension_source_count"])
  self.assertEqual(a["external_source_registry_total_unique_count"],m["combined_source_count"])
  self.assertGreaterEqual(len(a["completed_batches"]),487)
  self.assertEqual(a["row_count"],222)
  self.assertEqual(a["repaired_provenance_metadata_defect_count"],45)
  self.assertTrue(any(x.startswith("12TL IHP") for x in a["current_focus"]))
  self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertEqual(e["invariants"]["total_unique_sources"],668)
if __name__=="__main__": unittest.main()
