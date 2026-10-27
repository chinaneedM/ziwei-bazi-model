import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fi-fourfen-local-strings.py"
sp=importlib.util.spec_from_file_location("v13fi",p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class Test13FI(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.get(v.P);cls.s=v.get(v.S);cls.l=v.get(v.L)
 def test_pass(self):self.assertTrue(v.check(self.e,self.s,self.l))
 def deny(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):v.check(x,self.s,self.l)
 def test_false_adjacent_digit(self):self.deny(lambda x:x["source_photo_literal_rows"][2].update(direct_photo_glyphs="五三〇四"))
 def test_forged_rgb_sha(self):self.deny(lambda x:x["source_photo_literal_rows"][0].update(sha256_native_RGB_crop="0"*64))
 def test_false_increment(self):self.deny(lambda x:x["literal_digit_replay"].update(D5_to_D6_step=163))
 def test_false_historical_numeric_winner(self):self.deny(lambda x:x["literal_digit_replay"].update(establishes_historic_D5_numeric_value=True))
 def test_ncl_original_erased(self):self.deny(lambda x:x["opposing_NLC_day5_scope"].update(NLC_original_glyph_revision_authorized=True))
 def test_false_edition_winner(self):self.deny(lambda x:x["opposing_NLC_day5_scope"].update(winner="FIVE"))
 def test_fake_unit_bridge(self):self.deny(lambda x:x["literal_digit_replay"].update(unit_time_calendar_mapping="APPROVED"))
 def test_fake_algorithm_reopen(self):self.deny(lambda x:x["impact"].update(algorithm_reopen_count=1))
if __name__=="__main__":unittest.main()
