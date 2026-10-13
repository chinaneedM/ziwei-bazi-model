#!/usr/bin/env python3
"""12UY: as-of-batch evidence counts are not frozen global registry ceilings."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
STATE=load("docs/PROJECT-CURRENT-STATE-R1.json")
MAN=load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
D={
"12UM":load("docs/research/MING-DATONG-YEHUOBIAN-12UM-KYOTO-DUAL-ITEM-ACQUISITION-GATE-R1.json"),
"12UO":load("docs/research/MING-DATONG-YEHUOBIAN-12UO-NLC-OLD20-TERMINAL-FOLIO-IMAGE-ANCHORS-R1.json"),
"12UP":load("docs/research/MING-DATONG-YEHUOBIAN-12UP-OLD20-JUAN-SEAMS-FORWARD-CORRECTION-R1.json"),
"12UQ":load("docs/research/MING-DATONG-YEHUOBIAN-12UQ-OLD20-JUAN20-NINE-PAGE-SCOPED-REVIEW-R1.json")}
class SnapshotGrowth12UY(unittest.TestCase):
 def test_current_manifest_and_state_equal(self):
  self.assertEqual(STATE["historical_audit"]["external_source_registry_total_unique_count"],MAN["combined_source_count"])
  self.assertEqual(MAN["root_source_count"],647)
  self.assertGreaterEqual(MAN["extension_source_count"],42)
  self.assertEqual(MAN["combined_source_count"],MAN["root_source_count"]+MAN["extension_source_count"])
 def test_four_snapshots_remain_unchanged_at_687(self):
  for k,v in D.items():
   a=v["accounting"]
   base= {"12UM":a.get("combined_sources"),"12UO":a.get("source_registry_unique"),"12UP":a.get("total_sources"),"12UQ":a.get("total_sources")}[k]
   self.assertEqual(base,687,k)
   self.assertLessEqual(base,MAN["combined_source_count"])
 def test_asof_parts_add_up(self):
  for k,v in D.items():
   a=v["accounting"]
   root={"12UM":"root_sources","12UO":"source_registry_root","12UP":"source_root","12UQ":"root_sources"}[k]
   ext={"12UM":"extension_sources","12UO":"source_registry_extension","12UP":"source_extensions","12UQ":"extension_sources"}[k]
   self.assertEqual(a[root]+a[ext],687,k)
 def test_scope_unchanged(self):
  self.assertFalse(D["12UO"]["negative_inference_firewall"]["gaizao_louke_target_heading_located"])
  self.assertFalse(D["12UQ"]["astronomical_context"]["four_locus_variant_values_bound"])
  self.assertFalse(D["12UM"]["acquisition"]["outreach_sent"])
  self.assertFalse(D["12UP"]["chronology_scope"]["old_chronological_juan20_identical_to_1827_thematic_juan20"])
 def test_no_reopen_or_new_target(self):
  self.assertEqual(STATE["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(STATE["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
  self.assertEqual(STATE["historical_audit"]["row_count"],222)
  self.assertGreaterEqual(tuple(map(int,STATE["schema_version"].split("."))),(1,555,0))
if __name__=="__main__":unittest.main()
