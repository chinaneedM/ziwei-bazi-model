import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-native-d15-d18-13cm.py"
spec=importlib.util.spec_from_file_location("goryeosa13cm",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestNative13CM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
  cls.old={k:m.load(z["path"]) for k,z in cls.e["frozen_previous_git_blobs"].items()}
 def check(self,e=None,s=None,l=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None,self.old)
 def test_positive(self):self.assertTrue(self.check())
 def test_roi_sha_mismatch(self):
  e=copy.deepcopy(self.e);e["native_original_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_wrong_printed_day(self):
  e=copy.deepcopy(self.e);e["native_original_rois"][0]["printed_day"]=16
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_false_source_image_multiplication(self):
  e=copy.deepcopy(self.e);e["limitations"]["new_physical_copy_witnesses"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_unauthorized_emendation(self):
  e=copy.deepcopy(self.e);e["original_local_arithmetic"]["original_d16_short_always_read"]="5.2362"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_false_c_claim(self):
  e=copy.deepcopy(self.e);e["limitations"]["waseda_D16_same_day_C"]="PROVEN"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_original_13ci_photo_key_names(self):
  self.assertEqual({x["source"] for x in self.old["13CI"]["rois"]},{"W23","NAJ17","NAJ18"})
  self.assertEqual({z["source"] for z in self.e["native_original_rois"]},{"W23","N17","N18"})
  self.assertTrue(self.check())
 def test_old_missing_revision_id(self):
  l=copy.deepcopy(self.l)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["history"].insert(0,{"event":"LEGACY_NO_REVISION_ID"})
  self.assertTrue(self.check(l=l))
 def test_future_append_only(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.800.0";s["historical_audit"]["current_focus"].append("13ZZ future")
  l["binding"]["reviewed_state_version"]="1.800.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13ZZ"
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
