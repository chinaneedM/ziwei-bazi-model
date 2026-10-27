import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-d16-seam-triad-13cb.py"
spec=importlib.util.spec_from_file_location("w13cb",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Folio13CB(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def go(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_original_roi_digest(self):
  e=copy.deepcopy(self.e);e["new_original_rgb_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_source_numeral(self):
  e=copy.deepcopy(self.e);e["new_original_rgb_rois"][0]["decimal"]="7570.6623"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_arithmetic(self):
  e=copy.deepcopy(self.e);e["local_numeric_identity"]["int_units_1e4"]["result"]+=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_global_formula(self):
  e=copy.deepcopy(self.e);e["local_numeric_identity"]["globally_proven_day_index_or_unit_formula"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_same_day_original_winner(self):
  e=copy.deepcopy(self.e);e["field_day_binding_boundary"]["signed_historical_D16_C_field_value"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_copy_multiplication(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_independent_stemma_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_only_after_later_batch(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="1.999.0"
  s["historical_audit"]["current_focus"].append("13CC next source")
  l["binding"]["reviewed_state_version"]="1.999.0";l["binding"]["latest_research_focus_prefix"]="13CC"
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
