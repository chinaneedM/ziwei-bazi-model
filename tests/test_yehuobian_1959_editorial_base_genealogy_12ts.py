"""12TS direct modern publisher-note assertion must not imply physical-copy genealogy."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(x):return json.loads((ROOT/x).read_text(encoding="utf-8"))
class PublisherSourceGraph12TS(unittest.TestCase):
 def test_direct_page_and_typed_edges(self):
  e=load("docs/research/MING-DATONG-YEHUOBIAN-12TS-ZHONGHUA1959-PUBLISHER-YAO1827-BASE-CITATION-R1.json")
  g=load("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
  self.assertEqual(e["pdf_page_1based"],4)
  self.assertEqual(e["page_jpeg_sha256"],"a8bd71a8cb78eea01c10cec50b7378f760aefbe1efc7936a188c36f97e1be97d")
  self.assertTrue(e["human_read_no_ocr"])
  self.assertFalse(e["editorial_self_report"]["original_1827_physical_copy_identifier_given"])
  self.assertFalse(e["editorial_self_report"]["other_qing_manuscripts_identified"])
  self.assertEqual(e["invariants"]["ancient_target_glyph_votes"],0)
  self.assertGreaterEqual(len(g["nodes"]),250)
  self.assertGreaterEqual(len(g["edges"]),237)
  nodes={x["node_id"]:x for x in g["nodes"]}
  edges={x["edge_id"]:x for x in g["edges"]}
  self.assertIn("EDITION-YEHUOBIAN-ZHONGHUA1959-FIRSTPRINT-3V",nodes)
  self.assertIn("PASSAGE-YEHUOBIAN-ZHONGHUA1958-PUBLISHER-NOTE-1827BASE",nodes)
  a=edges["TG-E0236"];b=edges["TG-E0237"]
  self.assertEqual(a["relation"],"EXPLICITLY_CITES")
  self.assertEqual(a["to"],"EDITION-YEHUOBIAN-1827-FULISHANFANG-30V")
  self.assertEqual(a["status"],"CONFIRMED")
  self.assertIn("does not identify a specific 1827 physical copy",a["scope_note"])
  self.assertEqual(b["relation"],"ATTESTS")
 def test_monotone_handoff(self):
  h=load("docs/PROJECT-CURRENT-STATE-R1.json")
  self.assertTrue(any(x.startswith("12TS NLC511") for x in h["historical_audit"]["current_focus"]))
  self.assertEqual(h["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertEqual(h["invariants"]["algorithm_reopen_count"],0)
  self.assertGreaterEqual(h["historical_audit"]["external_source_registry_total_unique_count"],678)
if __name__=="__main__":unittest.main()
