import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-solar-d21-d25-original-12yh.py"
s=importlib.util.spec_from_file_location("G893_12yh",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class D21D25Original(unittest.TestCase):
 def setUp(self):self.args=list(v.load())
 def invalid(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_pass(self):self.assertEqual(v.verify(*self.args)["crossleaf_source_edges"],5)
 def test_false_long_reading(self):self.args[0]["direct_glyph_readings"][2]["long_decimal"]="392.5634";self.invalid()
 def test_false_original_glyph(self):self.args[0]["direct_glyph_readings"][3]["short_glyph"]="五分三八四〇";self.invalid()
 def test_false_lane_hash(self):self.args[0]["source_rois"][0]["sha256"]="0"*64;self.invalid()
 def test_overlap(self):self.args[0]["source_rois"][1]["rect"][0]=765;self.invalid()
 def test_wrong_003b_page(self):self.args[0]["direct_glyph_readings"][4]["page"]="003a";self.invalid()
 def test_false_12yf_restore(self):self.args[0]["historical_error_precedence"]["previous_12yf_ascending_long"]="VALID";self.invalid()
 def test_wrong_recurrence(self):self.args[0]["exact_arithmetic"]["long_differences"][0]="5.3106";self.invalid()
 def test_false_pseudowitness(self):self.args[0]["archive"]["new_independent_physical_copies"]=1;self.invalid()
 def test_wrong_external_winner(self):self.args[0]["unresolved"]["cross_witness_mechanical_final"]="6/6";self.invalid()
 def test_false_unit_bridge(self):self.args[0]["unresolved"]["old_unit_second_shao"]="PROVEN";self.invalid()
 def test_issue_closed(self):next(q for q in self.args[1]["issues"] if q["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.invalid()
 def test_wrong_state(self):self.args[2]["schema_version"]="1.620.0";self.invalid()
if __name__=="__main__":unittest.main()
