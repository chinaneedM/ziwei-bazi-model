import importlib.util,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13js-goryeosa-takeda1972-source-scope.py"
spec=importlib.util.spec_from_file_location("tw13js",S);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Test2005EditorialCitationScope(unittest.TestCase):
 def setUp(self):self.x=list(mod.load())
 def reject(self):
  with self.assertRaises(AssertionError):mod.verify(*self.x)
 def test_ok(self):self.assertEqual(mod.verify(*self.x)["status"],"PASS")
 def test_no_fake_1972_original(self):
  self.x[0]["primary_later_publication"]["facsimile_1972_original_title_page_directly_examined"]=True;self.reject()
 def test_no_fake_gk5554_original(self):
  self.x[0]["primary_later_publication"]["original_gk5553_or_gk5554_physical_folio_directly_examined"]=True;self.reject()
 def test_no_1972_ncid_promotion(self):
  self.x[0]["adjudication"]["does_not_identify_exact_1972_cinii_ncid"]=False;self.reject()
 def test_no_g893_numeric_promotion(self):
  self.x[0]["adjudication"]["g893_original_numeric_target_decisions_this_batch"]=1;self.reject()
 def test_no_ancient_witness(self):
  self.x[0]["adjudication"]["new_ancient_physical_copy_votes"]=1;self.reject()
 def test_prior_risk_revision_preserved(self):
  issue=next(x for x in self.x[2]["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"]=[r for r in issue["history"] if "TW-OPEN-0005-13JS-" not in r.get("revision_id","")];self.reject()
 def test_future_append_only_prefix(self):
  self.x[1]["historical_audit"]["current_focus"].append("13JT later")
  self.x[2]["binding"]["source_focus_count"]+=1
  self.x[2]["binding"]["latest_research_focus_prefix"]="13JT"
  self.assertEqual(mod.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
