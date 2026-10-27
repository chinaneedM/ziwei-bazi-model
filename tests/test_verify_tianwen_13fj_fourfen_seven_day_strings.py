import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fj-fourfen-seven-day-strings.py"
spec=importlib.util.spec_from_file_location("v13fj",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13FJ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.x=v.read(v.P);cls.fi=v.read(v.FI);cls.s=v.read(v.S);cls.l=v.read(v.L)
 def test_valid_seven_days(self):self.assertTrue(v.check(self.x,self.fi,self.s,self.l))
 def reject(self,fn):
  q=copy.deepcopy(self.x);fn(q)
  with self.assertRaises(AssertionError):v.check(q,self.fi,self.s,self.l)
 def test_wrong_d7_photo_glyph(self):self.reject(lambda q:q["new_source_pixel_direct_collations"][0].update(glyphs="五四九五"))
 def test_wrong_d10_sha(self):self.reject(lambda q:q["new_source_pixel_direct_collations"][3].update(native_RGB_SHA256="0"*64))
 def test_fake_day_heading(self):self.reject(lambda q:q["new_source_pixel_direct_collations"][2].update(header="十日"))
 def test_wrong_local_step(self):self.reject(lambda q:q["literal_string_replay"]["successive_literal_string_differences"].__setitem__(4,163))
 def test_false_glyph_numeric_rewrite(self):self.reject(lambda q:q["literal_string_replay"]["temporary_character_digit_map"].update({"〇":"5"}))
 def test_fake_ancient_winner(self):self.reject(lambda q:q["literal_string_replay"].update(cross_copy_historical_winner="NIKH_FIVE"))
 def test_fake_historical_D5_unit(self):self.reject(lambda q:q["literal_string_replay"].update(historic_decimal_unit_or_arithmetic_not_inferred=False))
 def test_ncl_photo_erased(self):self.reject(lambda q:q["literal_string_replay"].update(NLC_prior_source_GLYPH_O_erased=True))
 def test_forged_physical_edition(self):self.reject(lambda q:q["source_gallery_scope"].update(original_juan52_to_physical_book_mapping_authenticated=True))
 def test_ancient_witness_multiplication(self):self.reject(lambda q:q["changes"].update(new_independent_physical_copies=4))
 def test_algo_reopen(self):self.reject(lambda q:q["changes"].update(algorithm_reopen_count=1))
if __name__=="__main__":unittest.main()
