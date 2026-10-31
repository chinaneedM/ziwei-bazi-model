"""13MQ regressions: actual original string mismatch is not same-field mechanics."""
import copy,importlib.util,json,unittest,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"scripts/verify-tianwen-13mq-g893-zhou-d15-second-lane.py"
sp=importlib.util.spec_from_file_location("gate13mq",P)
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class OriginalD15Nonidentity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.items=[json.loads(p.read_text(encoding="utf-8")) for p in (v.E,v.S,v.L,v.Y,v.M)]
 def gate(self,items):
  return v.check(*items)
 def test_scope_positive_metadata_only(self):
  result=self.gate(self.items)
  self.assertEqual(result["status"],"PASS")
  self.assertEqual(result["original_pixel_replay"],"NOT_EXECUTED_WITHOUT_ARCHIVE")
 def test_fake_original_d15_number_rejected(self):
  items=copy.deepcopy(self.items)
  items[0]["reading_adjudication"]["zhou_other_column_print"]="四百三十四分八二四九"
  with self.assertRaises(AssertionError):self.gate(items)
 def test_fake_same_second_field_rejected(self):
  items=copy.deepcopy(self.items)
  items[0]["reading_adjudication"]["cross_source_D15_second_column_printed_strings_equal"]=True
  with self.assertRaises(AssertionError):self.gate(items)
 def test_fake_same_unit_rejected(self):
  items=copy.deepcopy(self.items)
  items[0]["reading_adjudication"]["mechanical_same_field_or_equivalent_epoch"]="PROVEN"
  with self.assertRaises(AssertionError):self.gate(items)
 def test_original_roi_hash_change_rejected(self):
  items=copy.deepcopy(self.items)
  items[0]["original_roi_controls"][1]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.gate(items)
 def test_formal_historical_winner_rejected(self):
  items=copy.deepcopy(self.items)
  items[0]["scope_guard"]["G893_six_cross_original_historical_winners"]=1
  with self.assertRaises(AssertionError):self.gate(items)
 def test_successor_focus_forward_only(self):
  items=copy.deepcopy(self.items)
  e,s,l,y,m=items
  s["schema_version"]="1.980.0"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.980.0"
  s["historical_audit"]["current_focus"].append("13MR successor")
  l["binding"]["reviewed_state_version"]="1.980.0"
  l["binding"]["latest_research_focus_prefix"]="13MR"
  l["binding"]["source_focus_count"]+=1
  self.assertEqual(self.gate(items)["status"],"PASS")
 def test_source_pixel_replay_only_when_archive_supplied(self):
  archive=os.environ.get("TIANWEN_13MQ_SOURCE_ARCHIVE")
  if not archive:self.skipTest("No archived original ZIP supplied; never assert pixel replay success")
  self.assertEqual(v.replay(self.items[0],archive)["original_pixel_replay"],"PASS")
if __name__=="__main__":unittest.main()
