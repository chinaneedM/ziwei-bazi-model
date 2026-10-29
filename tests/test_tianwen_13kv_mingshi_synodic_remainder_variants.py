import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13kv-mingshi-synodic-remainder-variants.py"
s=importlib.util.spec_from_file_location("tw13kv",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ThirteenMoonVariants(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(m.read()))
 def fails(self):
  with self.assertRaises(ValueError):m.verify(*self.a)
 def test_valid(self):self.assertEqual(m.verify(*self.a)["leap_13_remainder"],"23897709/100")
 def test_changed_moon_length(self):self.a[0]["exact_arithmetic"]["source_succeeding_moon_base_units"]="29530594/100";self.fails()
 def test_wrong_13_remainder(self):self.a[0]["exact_arithmetic"]["leap_year_remainder"]="28897709/100";self.fails()
 def test_wrong_siku_quote(self):self.a[0]["sources"]["siku_received"]["phrase_month_13"]="有閏加二十三萬八九七七○九";self.fails()
 def test_wrong_common_quote(self):self.a[0]["sources"]["common_received"]["phrase_month_13"]="有閏加二十八萬八九七七○九";self.fails()
 def test_wrong_12_remainder(self):self.a[0]["exact_arithmetic"]["ordinary_year_remainder"]="54367115/100";self.fails()
 def test_false_daily_base(self):self.a[0]["exact_arithmetic"]["daily_base_units"]="9999";self.fails()
 def test_false_original_claim(self):self.a[0]["original_constant_control"]["original_harvard_v11_page_with_13_month_remainder_directly_verified_this_batch"]=True;self.fails()
 def test_fake_siku_witness(self):self.a[0]["sources"]["siku_received"]["separate_physical_original_authenticated"]=True;self.fails()
 def test_fake_text_winner(self):self.a[0]["adjudication"]["modern_transcription_typo_proven"]=True;self.fails()
 def test_fake_philology(self):self.a[0]["philological_controls"]["independent_source_native_image_original_glyph_p7_to_p12_verified"]=True;self.fails()
 def test_fake_index_winner(self):self.a[0]["adjudication"]["historic_zero_one_index_for_83_84_proven"]=True;self.fails()
 def test_fake_algorithm(self):self.a[0]["adjudication"]["algorithm_reopens"]=1;self.fails()
if __name__=="__main__":unittest.main()
