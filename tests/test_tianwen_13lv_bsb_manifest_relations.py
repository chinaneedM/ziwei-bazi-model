"""13LV title/catalog-only strict epistemic guard."""
import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lv-bsb-manifest-relations.py"
spec=importlib.util.spec_from_file_location("test_13lv",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13LV(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.load()
 def test_base(self):self.assertEqual(m.check(*self.data)["status"],"PASS")
 def test_fake_sibling(self):
  e,s,l=copy.deepcopy(self.data);e["adjudication"]["sibling_first_volume_verified"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_fake_juan35(self):
  e,s,l=copy.deepcopy(self.data);e["adjudication"]["new_target_original_juan35_glyph"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_fake_physical_date(self):
  e,s,l=copy.deepcopy(self.data);e["source_identifiers"]["exact_1739_physical_print_date_proven"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_wrong_opac(self):
  e,s,l=copy.deepcopy(self.data);e["direct_first_party_links"]["opac"]="https://example.net/guess"
  with self.assertRaises(AssertionError):m.check(e,s,l)
if __name__=="__main__":unittest.main()
