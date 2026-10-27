import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-solar-d26-d30-original-12yi.py"
s=importlib.util.spec_from_file_location("G893_12yi",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class G893D26D30Original(unittest.TestCase):
 def setUp(self):self.args=list(v.load())
 def invalid(self):
  with self.assertRaises(ValueError):v.verify(*self.args)
 def test_pass(self):self.assertEqual(v.verify(*self.args)["local_new_exact_edges"],5)
 def test_false_solar_reading(self):self.args[0]["direct_glyph_readings"][1]["short_decimal"]="5.4409";self.invalid()
 def test_false_original_glyph(self):self.args[0]["direct_glyph_readings"][3]["long_glyph"]="三百六十〇分〇八六九";self.invalid()
 def test_source_hash(self):self.args[0]["source_rois"][9]["sha256"]="0"*64;self.invalid()
 def test_overlapping_columns(self):self.args[0]["source_rois"][0]["rect"][2]=890;self.invalid()
 def test_wrong_source_leaf(self):self.args[0]["direct_glyph_readings"][0]["page"]="004a";self.invalid()
 def test_fake_independent_source(self):self.args[0]["archive"]["new_independent_physical_copies"]=1;self.invalid()
 def test_false_final_conclusion(self):self.args[0]["unresolved"]["cross_witness_mechanical_final"]="6/6";self.invalid()
 def test_false_global_law(self):self.args[0]["unresolved"]["whole_table_law"]="PROVEN";self.invalid()
 def test_reinstate_retracted(self):self.args[0]["historical_error_precedence"]["previous_12yf_ascending_long"]="VALID";self.invalid()
 def test_change_arithmetic(self):self.args[0]["exact_arithmetic"]["long_differences"][0]="5.4036";self.invalid()
 def test_remove_prior_baseline(self):self.args[0]["baseline_D25"]["long_decimal"]="381.8118";self.invalid()
 def test_close_issue(self):next(i for i in self.args[1]["issues"] if i["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.invalid()
 def test_stale_state(self):self.args[2]["schema_version"]="1.621.0";self.invalid()
if __name__=="__main__":unittest.main()
