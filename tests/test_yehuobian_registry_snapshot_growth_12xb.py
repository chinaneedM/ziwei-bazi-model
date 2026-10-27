import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,slug):
 s=importlib.util.spec_from_file_location(name,ROOT/("scripts/"+slug))
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class SourceSnapshotGrowth(unittest.TestCase):
 def setUp(self):
  self.st=load("ws","verify-yehuobian-12ws-tokyo-shanben-scope.py")
  self.wm=load("wm","verify-yehuobian-cadal-first-fascicle-dual-original-12wm.py")
  self.wo=load("wo","verify-yehuobian-keio-googlebooks-access-boundary-12wo.py")
  self.wk=load("wk","verify-yehuobian-four-era-paratext-12wk.py")
 def test_ws_preserves_historical_nohit_when_registry_grows(self):
  self.assertEqual(self.st.verify()["status"],"PASS")
 def test_wm_preserves_original_zip_and_no_print_vote(self):
  self.assertEqual(self.wm.verify()["status"],"PASS")
 def test_wo_preserves_http429_and_no_glyph_vote(self):
  self.assertEqual(self.wo.verify()["status"],"PASS")
 def test_wk_four_era_original_sources_not_reinterpreted(self):
  self.assertEqual(self.wk.verify()["status"],"PASS")
 def test_live_registry_extension_count_synced(self):
  import json
  s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text())
  m=json.loads((ROOT/"docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json").read_text())
  a=s["historical_audit"]
  self.assertEqual(a["external_source_registry_extension_count"],m["extension_source_count"])
  self.assertEqual(a["external_source_registry_total_unique_count"],m["combined_source_count"])
  self.assertEqual(m["root_source_count"],647)
  self.assertGreaterEqual(m["combined_source_count"],706)
 def test_prior_705_snapshot_is_not_overwritten(self):
  import json
  r=json.loads((ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12XB-REGISTRY-706-SOURCE-GROWTH-CI-REPAIR-R1.json").read_text())
  self.assertEqual(r["historical_snapshot"],705)
  self.assertEqual(r["current_source_count"],706)
  self.assertEqual(r["altered_historical_receipts"],0)
  self.assertEqual(r["algorithms_reopened"],0)
if __name__=="__main__":unittest.main()
