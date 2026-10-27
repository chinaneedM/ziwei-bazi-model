import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def j(p):return json.loads((R/p).read_text(encoding="utf-8"))
class SourceScope12TP(unittest.TestCase):
 def test_not_a_glyph_or_print_proof(self):
  e=j("docs/research/MING-DATONG-YEHUOBIAN-12TP-PANG1959-NDL-CHRONOLOGY-R1.json");s=j("docs/research/MING-DATONG-YEHUOBIAN-12TP-JOURNAL-NDL-SOURCE-SHARD-R1.json")
  self.assertTrue(e["pang"]["abstract_truncated"])
  self.assertFalse(e["pang"]["full_paper_read"])
  self.assertTrue(e["adjudication"]["ming_edition_existence_unresolved"])
  self.assertEqual([x["id"] for x in e["ndl"]["records"]],["a0000004112","a0000004113","a0000004114"])
  self.assertEqual(e["ndl"]["catalog_year_month"],"1959.2")
  self.assertEqual(e["adjudication"]["new_glyph_votes"],0)
  self.assertEqual(e["adjudication"]["algorithm_reopens"],0)
  self.assertEqual(e["transmission_impact"]["edges_supported"],[])
  self.assertEqual([x["source_id"] for x in s["sources"]],e["source_ids"])
  self.assertTrue(all(not x["physical_glyph_authority"] for x in s["sources"]))
 def test_live_state(self):
  m=j("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
  h=j("docs/PROJECT-CURRENT-STATE-R1.json")
  self.assertEqual(m["combined_source_count"],m["root_source_count"]+m["extension_source_count"])
  self.assertEqual(m["extension_source_count"],sum(x["source_count"] for x in m["shards"]))
  self.assertGreaterEqual(m["combined_source_count"],678)
  self.assertEqual(h["historical_audit"]["external_source_registry_total_unique_count"],m["combined_source_count"])
  self.assertEqual(h["historical_audit"]["external_source_registry_extension_count"],m["extension_source_count"])
  self.assertTrue(any(x.startswith("12TP PANG") for x in h["historical_audit"]["current_focus"]))
  self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
if __name__=="__main__":unittest.main()
