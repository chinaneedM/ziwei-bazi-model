"""13MN source-native original numeric lane and anti-promotion regressions."""
import copy,importlib.util,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gate13mn",R/"scripts/verify-tianwen-13mn-g893-original-three-day-lane.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class OriginalLane(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(v.E.read_text(encoding="utf-8"))
  cls.s=json.loads(v.S.read_text(encoding="utf-8"))
  cls.l=json.loads(v.L.read_text(encoding="utf-8"))
 def test_source_original_positive(self):
  self.assertEqual(v.check(self.e,self.s,self.l)["status"],"PASS")
 def test_wrong_direct_g893_d16_rejected(self):
  e=copy.deepcopy(self.e);e["g893_direct_original"]["observations"][1]["normalized"]="5.1362"
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_original_crop_hash_tamper_rejected(self):
  e=copy.deepcopy(self.e);e["g893_direct_original"]["observations"][1]["native_rgb_crop_sha256"]="0"*64
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_d16_printed_glyph_tamper_rejected(self):
  e=copy.deepcopy(self.e);e["g893_direct_original"]["observations"][1]["original_print"]="五分一三六二"
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_field_bridge_rejected(self):
  e=copy.deepcopy(self.e);e["independent_1569_print"]["same_field_unit_radix_calendar_epoch_confirmed"]=True
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_false_historical_winner_rejected(self):
  e=copy.deepcopy(self.e);e["scope_guard"]["historical_G893_six_cross_original_winners"]=1
  with self.assertRaises(AssertionError):v.check(e,self.s,self.l)
 def test_future_focus_allowed(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"].append("13MO successor research")
  l["binding"]["source_focus_count"]+=1
  l["binding"]["latest_research_focus_prefix"]="13MO"
  self.assertEqual(v.check(self.e,s,l)["status"],"PASS")
 def test_missing_checkpoint_rejected(self):
  l=copy.deepcopy(self.l);l["checkpoint_log"]=[x for x in l["checkpoint_log"] if x.get("id")!="OMISSIONS-13MN-G893-DIRECT-ORIGINAL-D15-D17-20261031"]
  with self.assertRaises(AssertionError):v.check(self.e,self.s,l)
if __name__=="__main__":unittest.main()
