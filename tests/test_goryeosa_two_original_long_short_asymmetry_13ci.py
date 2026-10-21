import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-two-original-long-short-asymmetry-13ci.py"
spec=importlib.util.spec_from_file_location("source13ci",path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Source13CI(unittest.TestCase):
 def setUp(self):self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L)
 def check(self,e=None,s=None,l=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l)
 def test_positive(self):self.assertTrue(self.check())
 def test_prior_blob_sha(self):self.assertEqual(len(m.prior_sha(self.e)),4)
 def test_counterfactual_d16_short_52362(self):
  e=copy.deepcopy(self.e);e["rois"][1]["decimal"]="5.2362"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_counterfactual_emendation_from_subtraction(self):
  e=copy.deepcopy(self.e);e["local_exact_arithmetic"]["cannot_emend_D16_original_from_subtraction"]=False
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_fabricated_uniform_formula(self):
  e=copy.deepcopy(self.e);e["local_exact_arithmetic"]["historical_mechanical_rule_generalization"]="PROVEN"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_fabricated_roi(self):
  e=copy.deepcopy(self.e);e["rois"][4]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_false_hist_copy_vote(self):
  e=copy.deepcopy(self.e);e["new_evidence_scope"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_unbound_not_upgraded(self):
  e=copy.deepcopy(self.e);e["source_boundaries"]["NAJ_D17_same_day_yingsuoji"]="7570.6624"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_future_research_append(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="1.990.0";s["historical_audit"]["current_focus"].append("13ZZ future")
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.990.0"
  l["binding"]["reviewed_state_version"]="1.990.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13ZZ"
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
