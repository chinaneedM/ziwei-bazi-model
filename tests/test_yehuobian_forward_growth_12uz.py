#!/usr/bin/env python3
"""12UZ new-source and semantic handoff counts can move without rewriting 12UX evidence."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
R=load("docs/research/MING-DATONG-YEHUOBIAN-12UX-NPM-QING-JINXIANG-PHYSICAL-COPY-R1.json")
S=load("docs/PROJECT-CURRENT-STATE-R1.json")
M=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
G=load("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
P=load("docs/research/MING-DATONG-YEHUOBIAN-12UN-ADDITIONAL-1827-PHYSICAL-COPY-BACKLOG-R1.json")
U=load("docs/research/MING-DATONG-YEHUOBIAN-12UR-CTEXT-SCAN-PAGE-IDENTITY-PROBE-R1.json")
class Growth12UZ(unittest.TestCase):
 def test_source_manifest_consistent_and_not_regressed(self):
  self.assertEqual(M["combined_source_count"],M["root_source_count"]+M["extension_source_count"])
  self.assertGreaterEqual(M["combined_source_count"],R["accounting"]["registry_total"])
  self.assertEqual(S["historical_audit"]["external_source_registry_total_unique_count"],M["combined_source_count"])
 def test_12ux_provenance_snapshot_preserved(self):
  self.assertEqual(R["accounting"]["registry_total"],689)
  self.assertEqual(R["accounting"]["graph_nodes"],252)
  self.assertEqual(R["accounting"]["graph_edges"],238)
  self.assertEqual(R["scope_outcome"]["new_historical_target_glyph_votes"],0)
 def test_older_12un_12ur_immutable_counts(self):
  for doc in [P,U]:
   self.assertEqual(doc["accounting"]["total_sources"],687)
   self.assertEqual(doc["accounting"]["root_sources"]+doc["accounting"]["extension_sources"],687)
   self.assertLessEqual(doc["accounting"]["total_sources"],M["combined_source_count"])
 def test_current_graph_edge_continues(self):
  edge=[x for x in G["edges"] if x.get("edge_id")=="TG-E0238"]
  self.assertEqual(len(edge),1)
  self.assertEqual(edge[0]["relation"],"PHYSICAL_COPY_OF_EDITION")
  self.assertEqual(edge[0]["status"],"CONFIRMED")
 def test_reopen_invariant(self):
  self.assertEqual(S["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(S["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertTrue(any(x.startswith("12UZ ") for x in S["historical_audit"]["current_focus"]))
  self.assertGreaterEqual(tuple(map(int,S["schema_version"].split("."))),(1,556,0))
if __name__=="__main__":unittest.main()
