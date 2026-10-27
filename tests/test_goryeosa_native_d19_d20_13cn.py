import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-native-d19-d20-13cn.py"
spec=importlib.util.spec_from_file_location("goryeosa13cn",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestNative13CN(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
  cls.old={k:m.load(v["path"]) for k,v in cls.e["frozen_previous_git_blobs"].items()}
 def check(self,e=None,s=None,l=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.old)
 def test_positive(self):self.assertTrue(self.check())
 def test_bad_day(self):
  e=copy.deepcopy(self.e);e["direct_original_rois"][0]["printed_day"]=18
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_fake_rgb_sha(self):
  e=copy.deepcopy(self.e);e["direct_original_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_original_d16_emendation_forbidden(self):
  e=copy.deepcopy(self.e);e["same_field_local_arithmetic"]["original_d16_emendation_authorized"]=True
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_third_physical_vote_forbidden(self):
  e=copy.deepcopy(self.e);e["scope"]["new_independent_votes"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_false_source_cumulative_mapping(self):
  e=copy.deepcopy(self.e);e["limitations"]["W_D16_same_day_cumulative"]="PROVEN"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_both_original_photo_ids(self):
  self.assertEqual(set(self.e["original_sources"]),{"W23","N18"})
  self.assertEqual(len(self.e["direct_original_rois"]),8)
 def test_future_state_append_only(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="1.751.0"
  s["historical_audit"]["current_focus"].append("13CO future")
  l["binding"]["reviewed_state_version"]="1.751.0"
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
