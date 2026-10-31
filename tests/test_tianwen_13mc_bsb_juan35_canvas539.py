"""13MC no-promotion source-page/body candidate tests."""
import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
script=ROOT/"scripts/verify-tianwen-13mc-bsb-juan35-canvas539.py"
sp=importlib.util.spec_from_file_location("v13mc",script)
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class CanvasBound(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(v.E.read_text(encoding="utf-8"))
  cls.s=json.loads(v.S.read_text(encoding="utf-8"))
  cls.l=json.loads(v.L.read_text(encoding="utf-8"))
 def test_original_source_bound(self):
  self.assertEqual(v.check(self.e,self.s,self.l)["status"],"PASS")
 def test_fake_title_leaf_rejected(self):
  e=copy.deepcopy(self.e);e["specific_target"]["is_chapter_title_leaf"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_physical_1739_rejected(self):
  e=copy.deepcopy(self.e);e["epistemic_limits"]["exact_1739_impression_proven"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_fake_original_numeric_rejected(self):
  e=copy.deepcopy(self.e);e["specific_target"]["original_juan35_target_numeric_reading_verified"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_original_sha_tamper_rejected(self):
  e=copy.deepcopy(self.e);e["specific_target"]["jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_only_local_order(self):
  e=copy.deepcopy(self.e);e["ordering_boundary"]["global_scan_direction_proven"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_forward_only_successor_focus_is_accepted(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"].append("13MM successor research, archive intact")
  l["binding"]["source_focus_count"]+=1
  l["binding"]["latest_research_focus_prefix"]="13MM"
  self.assertEqual(v.check(self.e,s,l)["status"],"PASS")
 def test_missing_archived_13mc_focus_rejected(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"]=[x for x in s["historical_audit"]["current_focus"] if not x.startswith("13MC ")]
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  with self.assertRaises(AssertionError):v.check(self.e,s,l)
 def test_latest_focus_prefix_mismatch_rejected(self):
  l=copy.deepcopy(self.l);l["binding"]["latest_research_focus_prefix"]="13MC"
  with self.assertRaises(AssertionError):v.check(self.e,self.s,l)
 def test_original_13mc_checkpoint_required(self):
  l=copy.deepcopy(self.l)
  l["checkpoint_log"]=[x for x in l["checkpoint_log"] if x.get("id")!="OMISSIONS-13MC-BSB-J35-C539-CROSSWALK-20261030"]
  with self.assertRaises(AssertionError):v.check(self.e,self.s,l)
if __name__=="__main__":unittest.main()
