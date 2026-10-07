import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((ROOT/"docs/research/MING-DATONG-JINGTAI1-GUOQUE-PHYSICAL-COLLATION-R1.json").read_text(encoding="utf-8")); c.b=json.loads((ROOT/"docs/research/MING-DATONG-EXECUTABLE-ADAPTER-BLOCKER-DECOMPOSITION-R1.json").read_text(encoding="utf-8")); c.m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json").read_text(encoding="utf-8")); c.g=json.loads((ROOT/"docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json").read_text(encoding="utf-8")); c.s=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json").read_text(encoding="utf-8"))
 def test_target(c):
  p=c.r["physical_page_binding"]; c.assertEqual(p["target_pdf_page"],112); c.assertEqual(p["direct_target_reading"],"卯刻月食欽天監官以辰初刻被劾下法司宥之"); c.assertFalse(c.r["source_route"]["ocr_used_for_final_glyph_claims"])
 def test_fail_closed(c):
  a=c.r["adjudication"]; c.assertEqual(a["jingtai1_absolute_anchor_status"],"NOT_YET_ADMISSIBLE"); c.assertFalse(a["runtime_authorized"])
 def test_bindings(c):
  row=next(x for x in c.m["rows"] if x["rule_id"]=="HPA-DAYUN-CAL-002"); c.assertEqual(row["audit_status"],"MISSING_FROM_PRODUCT"); src=next(x for x in c.s["sources"] if x["source_id"]=="EXT-COMMONS-ZJLIB-GUOQUE-V25-P112-JINGTAI1-ECLIPSE-PHYSICAL"); c.assertTrue(src["physical_glyph_authority"]); nodes={x["node_id"] for x in c.g["nodes"]}; edges={x["edge_id"] for x in c.g["edges"]}; [c.assertIn(x,nodes) for x in c.r["transmission_impact"]["graph_nodes_added"]]; [c.assertIn(x,edges) for x in c.r["transmission_impact"]["graph_edges_added"]]
if __name__=="__main__": unittest.main()
