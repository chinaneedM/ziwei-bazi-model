import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("hb",ROOT/"scripts/verify-tianwen-13hb-photo4-day14-direct-glyph.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class D14PositivePhoto(unittest.TestCase):
 def setUp(self):self.e=json.loads(m.E.read_text(encoding="utf8"))
 def test_evidence_preservation(self):self.assertTrue(m.check(self.e))
 def test_no_ncl_overclaim(self):
  self.e["boundaries"]["NCL_03130_p74_D14_original_complete_literal"]="四分六六三〇"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_no_ncl_terminal_overclaim(self):
  self.e["boundaries"]["NCL_03130_p74_D14_terminal_glyph"]="〇"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_no_crosscopy_independence(self):
  self.e["boundaries"]["NLC_vs_NIKH_independent_physical_copy_certified"]=True
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_no_unknown_unit_promotion(self):
  self.e["boundaries"]["ancient_unit"]="秒"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_no_false_sha(self):
  self.e["source"]["jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_no_wrong_season(self):
  self.e["crosscheck"]["seasonal_key"]="WINTER_EARLY_YING_LATE_SUO"
  with self.assertRaises(AssertionError):m.check(self.e)
 def test_no_false_source_pixel_coordinate(self):
  self.e["direct_visual_glyph_reviews"][1]["xyxy"][1]=698
  with self.assertRaises(AssertionError):m.check(self.e)
if __name__=="__main__":unittest.main()
