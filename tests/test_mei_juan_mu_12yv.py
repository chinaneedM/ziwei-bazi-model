import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mei-juan-mu-12yv.py"
spec=importlib.util.spec_from_file_location("verify_mei_12yv",p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class JuanMuEvidenceScope(unittest.TestCase):
 def setUp(self):self.data=v.load()
 def fail_scope(self):
  with self.assertRaises(ValueError):v.check(*self.data)
 def test_live(self):self.assertEqual(v.check(*self.data)["result"],"PASS")
 def test_future_12yw_is_allowed(self):
  self.assertTrue(any(x.startswith("12YW ") for x in self.data[2]["historical_audit"]["current_focus"]))
  self.data[2]["historical_audit"]["current_focus"].append("12ZZ synthetic later research focus")
  self.data[1]["binding"]["source_focus_count"]+=1
  self.data[1]["binding"]["latest_research_focus_prefix"]="12ZZ"
  self.assertEqual(v.check(*self.data)["result"],"PASS")
 def test_mu_to_juan_leap(self):self.data[0]["philology"]["mu_total_is_not_automatically_historical_juan_count"]=False;self.fail_scope()
 def test_fabricated_independent_original(self):self.data[0]["evidence_impact"]["new_distinct_historical_physical_witnesses"]=1;self.fail_scope()
 def test_false_historical_edition(self):self.data[0]["comparison_result"]["seventeen_juan_historical_edition_or_repagination"]="PROVED";self.fail_scope()
 def test_false_catalog_visitor(self):self.data[1]["issues"][4]["mei_12yv_bibliographic_juan_mu_conflict_reviews"][0]["original_catalog_leaf_verified"]=True;self.fail_scope()
 def test_false_g893_mechanical_closure(self):self.data[0]["evidence_impact"]["g893_cross_witness_final"]="6/6";self.fail_scope()
if __name__=="__main__":unittest.main()
