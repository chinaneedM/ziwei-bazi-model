import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-first20-two-holding-headings-13ch.py"
spec=importlib.util.spec_from_file_location("dayatlas13ch",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SourceOriginalFirst20(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def ok(self,e=None,s=None,l=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.ok())
 def test_forged_day_glyph(self):
  e=copy.deepcopy(self.e);e["photos"]["W22"]["day_header_rois"][0]["literal"]="四日"
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_forged_hash(self):
  e=copy.deepcopy(self.e);e["photos"]["N18"]["day_header_rois"][2]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_missing_day(self):
  e=copy.deepcopy(self.e);e["photos"]["W23"]["day_header_rois"].pop()
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_forged_center(self):
  e=copy.deepcopy(self.e);e["photos"]["N17"]["day_header_rois"][6]["bbox"][0]+=10
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_crossfolio_day_shift_fabricated(self):
  e=copy.deepcopy(self.e);e["interpretation_boundary"]["global_day_shift_between_copies"]="PROVEN"
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_false_ancestry_from_matching_days(self):
  e=copy.deepcopy(self.e);e["interpretation_boundary"]["NAJ_WASEDA_independent_textual_stemma"]="PROVEN"
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_forged_waseda_d16_C(self):
  e=copy.deepcopy(self.e);e["interpretation_boundary"]["WASEDA_D16_original_same_day_yingsuoji"]="7570.6624"
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_forged_new_historical_witness(self):
  e=copy.deepcopy(self.e);e["source_grade_firewall"]["new_physical_historical_witnesses"]=1
  with self.assertRaises(AssertionError):self.ok(e=e)
 def test_forward_only_future_stage(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.888.0";s["historical_audit"]["current_focus"].append("13CI next batch")
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.888.0"
  l["binding"]["reviewed_state_version"]="1.888.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13CI"
  self.assertTrue(self.ok(s=s,l=l))
if __name__=="__main__":unittest.main()
