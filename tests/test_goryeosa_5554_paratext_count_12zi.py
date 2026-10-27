import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-5554-paratext-count-12zi.py"
s=importlib.util.spec_from_file_location("t12zi",P);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Tests(unittest.TestCase):
 def setUp(self):self.data=list(v.load())
 def fail(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_valid(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_no_5553_5554_transfer(self):self.data[0]["constrained_model"]["same_gk5553_counting_schema_applicable_to_gk5554"]="PROVEN";self.fail()
 def test_no_5554_book52_guess(self):self.data[0]["constrained_model"]["item_5554_v52_exact_physical_book"]=10;self.fail()
 def test_no_105_fictitious_closure(self):self.data[0]["constrained_model"]["conditional_remaining_scholarly_gap_after_three_extras"]=0;self.fail()
 def test_no_original_glyph(self):self.data[0]["constrained_model"]["original_5554_v52_d16_glyph"]="五分";self.fail()
 def test_no_new_witness(self):self.data[0]["constrained_model"]["new_stemmatic_physical_witnesses"]=1;self.fail()
 def test_forward_appended_later_batches(self):
  self.data[2]["historical_audit"]["current_focus"].append("12ZJ later")
  self.data[3]["binding"]["source_focus_count"]+=1
  self.data[3]["binding"]["latest_research_focus_prefix"]="12ZJ"
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
