import copy, importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-p21-field-d16-boundary-13ca.py"
spec=importlib.util.spec_from_file_location("w13ca",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceField13CA(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def test_positive(self):self.assertTrue(m.check(self.e,self.s,self.l))
 def test_false_accumulation_equivalence(self):
  x=copy.deepcopy(self.e);x["direct_reading"]["jiri_equals_yingsuoji"]=True
  with self.assertRaises(AssertionError):m.check(x,self.s,self.l)
 def test_falsified_d16_value(self):
  x=copy.deepcopy(self.e);x["direct_reading"]["printed_original_D16_C_numeric_value"]="7570.6624"
  with self.assertRaises(AssertionError):m.check(x,self.s,self.l)
 def test_falsified_unit_bridge(self):
  x=copy.deepcopy(self.e);x["direct_reading"]["G893_shao_wei_equivalent_to_Waseda_richa_unit"]="PROVEN"
  with self.assertRaises(AssertionError):m.check(x,self.s,self.l)
 def test_wrong_image_crop(self):
  x=copy.deepcopy(self.e);x["source_native_rgb_rois"][1]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(x,self.s,self.l)
 def test_false_source_independence(self):
  x=copy.deepcopy(self.e);x["scope"]["new_physical_witnesses"]=1
  with self.assertRaises(AssertionError):m.check(x,self.s,self.l)
 def test_live_registry_count_drift_rejected(self):
  s=copy.deepcopy(self.s);s["historical_audit"]["external_source_registry_total_unique_count"]+=1
  with self.assertRaises(AssertionError):m.check(self.e,s,self.l)
 def test_future_shard_count_growth_is_not_static(self):
  s=copy.deepcopy(self.s);s["historical_audit"]["external_source_registry_extension_count"]+=3
  s["historical_audit"]["external_source_registry_total_unique_count"]+=3
  self.assertTrue(m.check(self.e,s,self.l))
 def test_forward_only_future_state(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="FUTURE";s["historical_audit"]["current_focus"].append("13CB NEXT")
  l["binding"]["reviewed_state_version"]="FUTURE";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(m.check(self.e,s,l))
if __name__=="__main__":unittest.main()
