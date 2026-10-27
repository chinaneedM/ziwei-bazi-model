import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mei-ia-12ys-404-boundary.py"
sp=importlib.util.spec_from_file_location("mei_12ys",p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class TestMeiIAExactLocator(unittest.TestCase):
 def setUp(self):self.a=list(v.load())
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_valid(self):self.assertEqual(v.verify(*self.a)["Mei_original_glyphs"],0)
 def test_invented_original_sha(self):self.a[0]["target"]["source_file_sha256"]="fake";self.fails()
 def test_404_not_200(self):self.a[0]["acquisition_attempt"]["attempts"][0]["result"]="SUCCESS";self.fails()
 def test_mislabeled_cat_id(self):self.a[0]["target"]["file_identifier"]="06056955.cn";self.fails()
 def test_fake_ctext_same_copy(self):self.a[0]["catalog_provenance"]["cadal_same_physical_copy_as_12yo_ctext"]="SAME";self.fails()
 def test_paid_without_authorization(self):self.a[0]["alternate_routes"][2]["payment_made"]=True;self.fails()
 def test_fake_witness(self):self.a[0]["evidence_grade"]["new_independent_physical_print_voting"]=1;self.fails()
 def test_issue_must_remain_open(self):next(x for x in self.a[1]["issues"] if x["id"]=="TW-OPEN-0005")["status"]="RESOLVED";self.fails()
 def test_old_state(self):self.a[2]["schema_version"]="1.630.0";self.fails()
 def test_future_focus_does_not_erase(self):self.a[2]["historical_audit"]["current_focus"].append("12YT FUTURE");self.assertEqual(v.verify(*self.a)["status"],"PASS")
 def test_missing_scope_rejected(self):self.a[2]["historical_audit"]["current_focus"]=[x for x in self.a[2]["historical_audit"]["current_focus"] if not x.startswith("12YS ")];self.fails()
if __name__=="__main__":unittest.main()
