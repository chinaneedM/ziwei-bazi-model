import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kn-moon-operator-firewall.py"
s=importlib.util.spec_from_file_location("tw13kn",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class TestOperatorLayers(unittest.TestCase):
 def setUp(self):self.data=copy.deepcopy(list(v.load()))
 def fail_verification(self):
  with self.assertRaises(ValueError):v.verify(*self.data)
 def test_positive(self):self.assertEqual(v.verify(*self.data)["status"],"PASS")
 def test_wrong_next_amount_sign(self):self.data[0]["operator_layers"][0]["effect_sign"]=-1;self.fail_verification()
 def test_conflate_mei_final_with_next_amount(self):self.data[0]["operator_layers"][2]["object"]="NEXT_LIMIT_GAIN_LOSS_AMOUNT";self.fail_verification()
 def test_false_original_huang(self):self.data[0]["adjudication"]["huang_p79_dayan_glyph_proves_received_next_day_clause"]=True;self.fail_verification()
 def test_zero_based_claim(self):self.data[0]["limits"]["original_index_base_adjudicated"]=True;self.fail_verification()
 def test_false_167_glyph(self):self.data[0]["adjudication"]["huang_original_full_167_glyph_verified"]=True;self.fail_verification()
 def test_false_second_witness(self):self.data[0]["modern_reading_locators"][0]["direct_original_target_glyph_verified"]=True;self.fail_verification()
 def test_future_focus_append_only(self):
  self.data[1]["historical_audit"]["current_focus"].append("13KO FUTURE research")
  self.data[2]["binding"]["latest_research_focus_prefix"]="13KO"
  self.data[2]["binding"]["source_focus_count"]+=1
  self.assertEqual(v.verify(*self.data)["status"],"PASS")
if __name__=="__main__":unittest.main()
