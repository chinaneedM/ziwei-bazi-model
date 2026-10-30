"""13LQ acquired first-party IIIF manifest/preview scope guard."""
import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lq-bsb-iiif-acquisition.py"
spec=importlib.util.spec_from_file_location("verify_13lq",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13LQ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.load()
 def test_original(self):self.assertEqual(m.check(*self.data)["status"],"PASS")
 def test_claim_original_juan35(self):
  e,s,l=copy.deepcopy(self.data);e["scope_review"]["target_juan35_title_leaf"]="POSITIVE"
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_fake_1739(self):
  e,s,l=copy.deepcopy(self.data);e["adjudication"]["physical_print_year_verified"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_false_second_number(self):
  e,s,l=copy.deepcopy(self.data);e["adjudication"]["new_numeric_winners"]=1
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_wrong_archive_hash(self):
  e,s,l=copy.deepcopy(self.data);e["acquisition"]["artifact_zip_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_wrong_manifest_count(self):
  e,s,l=copy.deepcopy(self.data);e["acquisition"]["canvas_count"]=1886
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_missing_ledger_review(self):
  e,s,l=copy.deepcopy(self.data);l["binding"]["reviewed_state_version"]="1.960.0"
  with self.assertRaises(AssertionError):m.check(e,s,l)
if __name__=="__main__":unittest.main()
