"""13LO preserve direct-page identification while blocking woodblock and date claims."""
import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lo-naaj-harvard-crosswalk.py"
spec=importlib.util.spec_from_file_location("verify_13lo",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13LO(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=m.load()
 def test_original(self):self.assertEqual(m.check(*self.data)["status"],"PASS")
 def test_wrong_harvard_page(self):
  e,s,l=copy.deepcopy(self.data);e["harvard"]["same_text_page"]["pdf_page_1_based"]=7
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_fake_unique_damage(self):
  e,s,l=copy.deepcopy(self.data);e["same_passage_three_locus_controls"][0]["unique_accidental_woodblock_damage_confirmed"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_false_diff_plate(self):
  e,s,l=copy.deepcopy(self.data);e["exploratory_geometric_page_identification"]["same_plate_refuted"]=True
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_false_new_winner(self):
  e,s,l=copy.deepcopy(self.data);e["adjudication"]["new_historical_g893_numeric_winners"]=1
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_wrong_original_pdf_hash(self):
  e,s,l=copy.deepcopy(self.data);e["harvard"]["original_pdf_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(e,s,l)
 def test_missed_ledger_review(self):
  e,s,l=copy.deepcopy(self.data);l["binding"]["reviewed_state_version"]="1.958.0"
  with self.assertRaises(AssertionError):m.check(e,s,l)
if __name__=="__main__":unittest.main()
