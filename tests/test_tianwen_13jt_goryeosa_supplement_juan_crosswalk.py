import importlib.util
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("tw13jt",ROOT/"scripts/verify-tianwen-13jt-goryeosa-supplement-juan-crosswalk.py")
mod=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)
class TestGoryeosa1972SupplementCrosswalk(unittest.TestCase):
 def setUp(self):self.x=list(mod.load())
 def fails(self):
  with self.assertRaises(AssertionError):mod.verify(*self.x)
 def test_pass(self):self.assertEqual(mod.verify(*self.x)["status"],"PASS")
 def test_internal_versus_global_offset_wrong(self):
  self.x[0]["normalization"]["ji_relative_offset"]=47;self.fails()
 def test_aks_78_false_insertion(self):
  self.x[0]["normalization"]["aks"]["ji_internal_juan"].append(32);self.fails()
 def test_dropped_scholar_82_conflict(self):
  self.x[0]["normalization"]["comparison"]["only_wei_chen_global_juan"]=[78];self.fails()
 def test_immutable_prior_review_mismatch(self):
  self.x[1]["source_evidence"]["academic"]["replaced_work_volumes"].remove(82);self.fails()
 def test_work52_not_inferred_from_absence(self):
  self.x[0]["normalization"]["comparison"]["no_list_proves_1972_work_juan_52_printing_copy"]=False;self.fails()
 def test_no_forged_original(self):
  self.x[0]["conclusion"]["juan_82_original_leaf_read"]=True;self.fails()
 def test_no_fake_g893_numeric_win(self):
  self.x[0]["conclusion"]["new_g893_six_numeric_decisions"]=1;self.fails()
 def test_no_new_copy_vote(self):
  self.x[0]["conclusion"]["independent_ancient_physical_copy_votes"]=1;self.fails()
 def test_future_forward_only_append(self):
  self.x[2]["historical_audit"]["current_focus"].append("13JU later")
  self.x[3]["binding"]["source_focus_count"]+=1
  self.x[3]["binding"]["latest_research_focus_prefix"]="13JU"
  self.assertEqual(mod.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
