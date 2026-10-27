"""Hash-scoped image evidence keeps note date and print date separate."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/MING-DATONG-YEHUOBIAN-12TR-NLC511-1958-1959-DIRECT-COLLATION-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class Imprint12TR(unittest.TestCase):
 def test_direct_pages_and_ancient_firewall(self):
  e=read(E)
  self.assertEqual(e["source_pdf_sha256"],"90a94278928fcafd5020e09bf0edbce6e85a2b8fb90a398026f7b23876b41623")
  self.assertEqual([x["pdf_page"] for x in e["manually_collated"]],[3,4])
  self.assertEqual(e["manually_collated"][0]["reading"],["1959年2月第1版","1959年2月上海第1次印刷"])
  self.assertEqual(e["manually_collated"][1]["reading"],["出版者說明","一九五八年十一月"])
  self.assertEqual(e["manually_collated"][0]["jpeg_sha256"],"3e337dcfa8b0ae154bbf2487fbcb439c330e189e2e78ecc8ebea3b257f75d8f6")
  self.assertEqual(e["manually_collated"][1]["jpeg_sha256"],"a8bd71a8cb78eea01c10cec50b7378f760aefbe1efc7936a188c36f97e1be97d")
  self.assertTrue(e["separate_1958_physical_print_unproven"])
  self.assertFalse(e["original_1827_or_1869_target_leaf_examined"])
  self.assertEqual(e["original_glyph_votes_added"],0)
  self.assertEqual(e["new_sources"],0)
  self.assertEqual(e["graph_edges_added"],0)
  self.assertEqual(e["algorithm_reopens"],0)
  self.assertEqual(e["transmission_impact"]["edges_supported"],[])
 def test_research_state(self):
  h=read("docs/PROJECT-CURRENT-STATE-R1.json")
  self.assertGreaterEqual(h["historical_audit"]["external_source_registry_total_unique_count"],678)
  self.assertTrue(any(x.startswith("12TR NLC511") for x in h["historical_audit"]["current_focus"]))
  self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
if __name__=="__main__":unittest.main()
