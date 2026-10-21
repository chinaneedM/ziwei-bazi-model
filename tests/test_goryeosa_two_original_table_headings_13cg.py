import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-two-original-table-headings-13cg.py"
spec=importlib.util.spec_from_file_location("solar13cg",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Solar13CG(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def go(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.go())
 def test_fabricated_first_day_original(self):
  e=copy.deepcopy(self.e);e["observations"]["full_initial_row_pixel_complete_in_waseda"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_header_equals_numeric_field(self):
  e=copy.deepcopy(self.e);e["observations"]["source_original_EAST_ASIAN_DAY_LABEL_NOT_CUMULATIVE_FIELD"]=False
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_undocumented_source_physical_copy(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_physical_witnesses"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_original_roi_mutation(self):
  e=copy.deepcopy(self.e);e["original_rgb_rois"][3]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_overlay_metadata_fabricated(self):
  e=copy.deepcopy(self.e);e["observations"]["annotation_origin_or_date"]="MING_ERA"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_cross_copy_equivalence(self):
  e=copy.deepcopy(self.e);e["observations"]["cross_copy_column_mapping"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_future_stage_forward_only(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="1.999.0";s["historical_audit"]["current_focus"].append("13ZZ future")
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.999.0"
  l["binding"]["reviewed_state_version"]="1.999.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13ZZ"
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
