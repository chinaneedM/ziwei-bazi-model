import unittest,importlib.util
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts/verify-mei-lizhi-12yo-facsimile-locator.py"
sp=importlib.util.spec_from_file_location("tianwen_12yo",f);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class TestMeiCatalogGate(unittest.TestCase):
 def setUp(self):self.d=list(v.load())
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.d)
 def test_valid(self):self.assertEqual(v.verify(*self.d)["physical_witness_votes"],0)
 def test_fake_original_pixels(self):self.d[0]["catalog_routes"][1]["retrieved_original_bytes"]=True;self.fails()
 def test_assume_printed_mei_numeral(self):self.d[0]["catalog_routes"][1]["printed_target_gloss"]="一秒八十六微";self.fails()
 def test_fake_finna_copy_identity(self):self.d[0]["catalog_routes"][3]["physical_identity_to_ctext"]="SAME";self.fails()
 def test_two_websites_are_not_two_originals(self):self.d[0]["source_independence"]["physical_impression_votes_added"]=1;self.fails()
 def test_g893_algorithms_frozen(self):self.d[0]["safeguards"]["algorithm_reopens"]=1;self.fails()
 def test_incorrect_g893_closure(self):self.d[0]["safeguards"]["g893_original_fields"]="6/6";self.fails()
 def test_resolved_issue_not_allowed(self):next(z for z in self.d[1]["issues"] if z["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.fails()
 def test_old_state(self):self.d[2]["schema_version"]="1.628.0";self.fails()
if __name__=="__main__":unittest.main()
