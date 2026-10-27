import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-third-witness-access-13co.py"
spec=importlib.util.spec_from_file_location("goryeosa13co",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13CO(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def check(self,e=None,s=None,l=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.check())
 def test_cannot_make_1909_1451_original(self):
  e=copy.deepcopy(self.e);e["evidence_limits"]["can_identify_NDL_1909_as_1451_edition"]=True
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_fabricated_third_glyph(self):
  e=copy.deepcopy(self.e);e["evidence_limits"]["third_qualified_direct_original_D16_witnesses_added"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_mirror_identity_silent_repair(self):
  e=copy.deepcopy(self.e);e["new_candidate_routes"][1]["surrogate_conflict"]["record_grading"]="ORIGINAL_BOUND"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_conflation_upload_name(self):
  e=copy.deepcopy(self.e);e["new_candidate_routes"][1]["surrogate_conflict"]["source_03117_not_conclusively_proved_wrong_copy"]=False
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_unsigned_early_original_glyph(self):
  e=copy.deepcopy(self.e);e["new_candidate_routes"][0]["access"]["original_printed_D16_glyph_read"]="5.2362"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_future_state_append_only(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="1.752.0"
  s["historical_audit"]["current_focus"].append("13CP future")
  l["binding"]["reviewed_state_version"]="1.752.0"
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
