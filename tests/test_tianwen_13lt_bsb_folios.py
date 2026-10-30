"""13LT source page scope and negative proof firewall."""
import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lt-bsb-36-folios.py"
spec=importlib.util.spec_from_file_location("verify_13lt",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13LT(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.load()
 def test_base(self):self.assertEqual(m.check(*self.data)["status"],"PASS")
 def test_fake_absence(self):
  e,s,l=copy.deepcopy(self.data);e["textual_scope"]["target_juan35_not_present_proven"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_fake_original_glyph(self):
  e,s,l=copy.deepcopy(self.data);e["textual_scope"]["original_238977_09_or_288977_09_new_glyph"]="238977.09"
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_false_global_reverse_order(self):
  e,s,l=copy.deepcopy(self.data);e["textual_scope"]["this_does_not_prove_global_inverse_order"]=False
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_header_juan_collapse(self):
  e,s,l=copy.deepcopy(self.data);e["acquisition"]["source_page_title_loci"][0]["manual_read"]="明史卷三十五"
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_archive_hash_wrong(self):
  e,s,l=copy.deepcopy(self.data);e["acquisition"]["artifact_zip_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_stale_ledger_review(self):
  e,s,l=copy.deepcopy(self.data);l["binding"]["reviewed_state_version"]="1.961.0"
  with self.assertRaises(AssertionError):m.check(e,s,l)
if __name__=="__main__":unittest.main()
