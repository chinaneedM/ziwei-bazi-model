import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-utokyo-union-13aa.py"
spec=importlib.util.spec_from_file_location("utokyo13aa",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class UTokyoNIIUnionBoundary(unittest.TestCase):
 def test_catalog_locator_and_state(self):self.assertTrue(m.verify())
 def test_not_a_direct_original_witness(self):
  x=copy.deepcopy(m.load(m.S));x["sources"][0]["physical_glyph_authority"]=True
  self.assertNotEqual(x["sources"][0]["physical_glyph_authority"],m.load(m.S)["sources"][0]["physical_glyph_authority"])
 def test_utokyo_item_not_waseda_object(self):
  e=m.load(m.E)
  self.assertEqual(e["bibliographic_source"]["item_holding_identifier"],"0008542011")
  self.assertNotEqual(e["bibliographic_source"]["call_number"],e["independent_catalog_comparator"]["shelfmark"])
 def test_future_source_registration_does_not_invalidate_13aa(self):
  from unittest.mock import patch
  orig=m.load
  st=copy.deepcopy(orig("docs/PROJECT-CURRENT-STATE-R1.json"))
  le=copy.deepcopy(orig("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
  man=copy.deepcopy(orig(m.M))
  st["schema_version"]="1.687.0"
  st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.687.0"
  st["historical_audit"]["current_focus"].append("13AB SIMULATED FUTURE SHARD")
  st["historical_audit"]["external_source_registry_extension_count"]=89
  st["historical_audit"]["external_source_registry_total_unique_count"]=736
  le["binding"]["reviewed_state_version"]="1.687.0"
  le["binding"]["latest_research_focus_prefix"]="13AB"
  le["binding"]["source_focus_count"]=len(st["historical_audit"]["current_focus"])
  le["checkpoint_log"].append({"id":"SIMULATED_FUTURE_REVIEW","state_version":"1.687.0"})
  man["extension_source_count"]=89;man["combined_source_count"]=736
  man["shards"].append({"path":"docs/research/simulated-future-shard.json","schema":"TEST","source_count":1})
  def get(path):
   if path=="docs/PROJECT-CURRENT-STATE-R1.json":return st
   if path=="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json":return le
   if path==m.M:return man
   return orig(path)
  with patch.object(m,"load",side_effect=get):self.assertTrue(m.verify())
if __name__=="__main__":unittest.main()
