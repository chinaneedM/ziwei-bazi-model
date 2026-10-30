"""Source-route gate must reject invented original glyph, misleading edition dates, or count upgrades."""
import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lp-bsb-source-route.py"
spec=importlib.util.spec_from_file_location("verify_13lp",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13LP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.load()
 def test_positive_catalog(self):self.assertEqual(m.check(*self.data)["status"],"PASS")
 def test_original_glyph_faked(self):
  e,s,l=copy.deepcopy(self.data);e["adjudication"]["new_juan35_original_glyph_positive"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_exact_1739_impression_faked(self):
  e,s,l=copy.deepcopy(self.data);e["first_party_catalog"]["exact_holding_and_specific_1739_impression_binding"]="PROVEN"
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_juan35_faked(self):
  e,s,l=copy.deepcopy(self.data);e["first_party_catalog"]["actual_chapter_juan35_in_this_object"]="PROVEN"
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_unreviewed_ledger(self):
  e,s,l=copy.deepcopy(self.data);l["binding"]["reviewed_state_version"]="1.959.0"
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_registry_count_inflated(self):
  e,s,l=copy.deepcopy(self.data);e["counts"]["sources"]=766
  with self.assertRaises(AssertionError):m.check(e,s,l)
if __name__=="__main__":unittest.main()
