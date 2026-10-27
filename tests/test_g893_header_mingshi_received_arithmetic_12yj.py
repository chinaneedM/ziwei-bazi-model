import unittest,importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-g893-header-mingshi-received-arithmetic-12yj.py"
spec=importlib.util.spec_from_file_location("G893_12YJ",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class G893HeaderReceivedArithmetic(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def rejects(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_valid(self):self.assertEqual(v.verify(*self.x)["internal_mingshi_discrepancy"],"-0.0100")
 def test_false_received_math(self):self.x[0]["textual_calc"]["correct_sum"]="4.9286";self.rejects()
 def test_altered_received_value(self):self.x[0]["received_witnesses"][0]["received_total"]="4.9386";self.rejects()
 def test_fake_source_glyph_unit(self):self.x[0]["source_original"]["last_graphic_少_vs_微"]="SAME";self.rejects()
 def test_orig_pixel_digest(self):self.x[0]["source_original"]["original_rgb_roi"]["sha256"]="0"*64;self.rejects()
 def test_fake_unit_bridge(self):self.x[0]["source_local_check"]["identical_historical_units"]="PROVEN";self.rejects()
 def test_fake_ming_field(self):self.x[0]["source_local_check"]["cross_edition_D16_final"]="PROVEN";self.rejects()
 def test_fake_independent_historical_vote(self):self.x[0]["evidence_weight"]["new_historical_independent_physical_copies"]=1;self.rejects()
 def test_wrong_inferred_period(self):self.x[0]["source_original"]["second_as_modern_time_second"]="YES";self.rejects()
 def test_no_ledger_source(self):self.x[1]["issues"][-7]["source_refs"]=[];self.rejects()
 def test_closed_risk(self):next(q for q in self.x[1]["issues"] if q["id"]=="TW-OPEN-0005")["status"]="RESOLVED_WITH_EVIDENCE";self.rejects()
 def test_stale_state(self):self.x[2]["schema_version"]="1.623.0";self.rejects()
if __name__=="__main__":unittest.main()
