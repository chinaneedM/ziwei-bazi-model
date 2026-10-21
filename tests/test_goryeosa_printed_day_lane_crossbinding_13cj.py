import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-printed-day-lane-crossbinding-13cj.py"
spec=importlib.util.spec_from_file_location("goryeosa13cj",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PrintedDay13CJ(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L);self.prior=m.frozen(self.e)
 def verify(self,e=None,s=None,l=None,prior=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.prior if prior is None else prior)
 def test_positive(self):self.assertTrue(self.verify())
 def test_frozen_git_blob_shas(self):self.assertEqual(len(self.prior),4)
 def test_swapped_day_heading(self):
  e=copy.deepcopy(self.e);e["atlas_to_numerical_original_bindings"][0]["printed_day"]=17
  with self.assertRaises(AssertionError):self.verify(e=e)
 def test_horizontal_column_outside_day(self):
  e=copy.deepcopy(self.e);e["atlas_to_numerical_original_bindings"][0]["numeric_bbox"][0]=750
  with self.assertRaises(AssertionError):self.verify(e=e)
 def test_incorrect_heading_hash(self):
  e=copy.deepcopy(self.e);e["atlas_to_numerical_original_bindings"][2]["day_heading_rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.verify(e=e)
 def test_hidden_pixel_review_inflation(self):
  e=copy.deepcopy(self.e);e["new_evidence_scope"]["new_original_pixel_crops"]=1
  with self.assertRaises(AssertionError):self.verify(e=e)
 def test_false_C_field_upgrade(self):
  e=copy.deepcopy(self.e);e["source_boundaries"]["W_D16_same_day_yingsuoji"]="7570.6624"
  with self.assertRaises(AssertionError):self.verify(e=e)
 def test_false_formula_upgrade(self):
  e=copy.deepcopy(self.e);e["geometry_conclusion"]["does_not_prove"].remove("WHOLE_TABLE_GLOBAL_RECURRENCE")
  with self.assertRaises(AssertionError):self.verify(e=e)
 def test_old_source_roi_regression(self):
  p=copy.deepcopy(self.prior);p["13BS"]["original_rgb_rois"][1]["bbox"][0]+=1
  with self.assertRaises(AssertionError):self.verify(prior=p)
 def test_risk_issue_must_remain_open(self):
  l=copy.deepcopy(self.l);next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED"
  with self.assertRaises(AssertionError):self.verify(l=l)
 def test_future_append(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.999.0";s["historical_audit"]["current_focus"].append("13ZZ future")
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.999.0"
  l["binding"]["reviewed_state_version"]="1.999.0"
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["binding"]["latest_research_focus_prefix"]="13ZZ"
  self.assertTrue(self.verify(s=s,l=l))
if __name__=="__main__":unittest.main()
