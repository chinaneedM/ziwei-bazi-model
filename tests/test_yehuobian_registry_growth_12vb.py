#!/usr/bin/env python3
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path)
 mod=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(mod)
 return mod
VA=load_module("v12va","scripts/verify-yehuobian-1959-2019-historiography-12va.py")
UX=load_module("v12ux","scripts/verify-yehuobian-npm-jinxiang-12ux.py")
class RegistryGrowth12VB(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.v=[read(p) for p in (VA.REC,VA.SHARD,VA.MAN,VA.STATE,VA.GRAPH,VA.OLD)]
  cls.u=[read(p) for p in (UX.RECORD,UX.SHARD,UX.MANIFEST,UX.GRAPH,UX.STATE)]
 def test_12va_record_and_12ux_unchanged(self):
  self.assertEqual(VA.validate(*self.v)["new_scholarly_sources"],1)
  self.assertEqual(UX.validate(*self.u)["new_target_glyph_votes"],0)
 def test_live_state_and_manifest_consistent(self):
  manifest=self.v[2];state=self.v[3]
  # 12VA's 647+43=690 is an immutable historical snapshot, not a live ceiling.
  self.assertEqual(manifest["root_source_count"],647)
  self.assertGreaterEqual(manifest["extension_source_count"],43)
  self.assertEqual(manifest["combined_source_count"],
                   manifest["root_source_count"]+manifest["extension_source_count"])
  audit=state["historical_audit"]
  self.assertEqual(audit["external_source_registry_root_count"],manifest["root_source_count"])
  self.assertEqual(audit["external_source_registry_extension_count"],manifest["extension_source_count"])
  self.assertEqual(audit["external_source_registry_total_unique_count"],manifest["combined_source_count"])
  self.assertEqual(self.v[0]["source_delta"]["extension_after"],43)
  self.assertEqual(self.v[0]["source_delta"]["unique_source_count_increment"],1)
 def test_historical_12va_floor_rejected_even_if_current_state_matches(self):
  x=copy.deepcopy(self.v)
  x[2]["extension_source_count"]=42
  x[2]["combined_source_count"]=689
  x[3]["historical_audit"]["external_source_registry_extension_count"]=42
  x[3]["historical_audit"]["external_source_registry_total_unique_count"]=689
  with self.assertRaisesRegex(ValueError,"manifest current count"):
   VA.validate(*x)
 def test_nonmatching_manifest_rejected_even_if_greater(self):
  for validator,docs in [(VA.validate,self.v),(UX.validate,self.u)]:
   x=copy.deepcopy(docs)
   i=2 if validator==VA.validate else 2
   x[i]["combined_source_count"]+=1
   with self.assertRaises(ValueError):validator(*x)
 def test_reopen_not_authorized(self):
  self.assertFalse(self.v[0]["historical_state"]["algorithm_reopen_authorized"])
  self.assertEqual(self.v[3]["invariants"]["algorithm_reopen_count"],0)
  self.assertEqual(self.v[3]["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")
 def test_forward_status_exists(self):
  self.assertGreaterEqual(tuple(map(int,self.v[3]["schema_version"].split("."))),(1,558,0))
  self.assertTrue(any(x.startswith("12VB ") for x in self.v[3]["historical_audit"]["current_focus"]))
if __name__=="__main__":unittest.main()
