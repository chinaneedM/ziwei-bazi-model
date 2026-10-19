import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-crosscopy-three-day-13ab.py"
spec=importlib.util.spec_from_file_location("goryeosa13ab",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CrosscopyOriginalThreeDay(unittest.TestCase):
 def test_source_hash_and_lexical_boundaries(self):self.assertTrue(m.check(m.read()))
 def test_printed_yi_must_not_be_silently_corrected(self):
  e=copy.deepcopy(m.read());e["collation"][1]["glyph"]="五分二三六二"
  with self.assertRaises(AssertionError):m.check(e)
 def test_nlc_firstparty_unproven(self):
  e=copy.deepcopy(m.read());e["source_nlc"]["firstparty_nlc_item_crosswalk_verified"]=True
  with self.assertRaises(AssertionError):m.check(e)
 def test_not_three_numerical_votes(self):
  e=copy.deepcopy(m.read());e["adjudication"]["physical_independent_numeric_votes_added"]=3
  with self.assertRaises(AssertionError):m.check(e)
 def test_no_same_plate_inference(self):
  e=copy.deepcopy(m.read());e["adjudication"]["three_day_pattern_alone_proves_shared_printing_plate"]=True
  with self.assertRaises(AssertionError):m.check(e)
if __name__=="__main__":unittest.main()
