import copy, importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p74-d6-chudu-long-13el.py"
spec=importlib.util.spec_from_file_location("v13el",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EL(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.ek=m.read(m.EK);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):return m.check(self.e if e is None else e,self.ek,self.ei,self.ed,self.s,self.l)
 def reject(self,mutate):
  e=copy.deepcopy(self.e);mutate(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_source_and_handoff(self):self.assertTrue(self.go())
 def test_false_image_sha(self):self.reject(lambda e:e["source"].update(png_sha256="0"*64))
 def test_false_d6_glyph(self):self.reject(lambda e:e["rois"][1].update(visible_literal="初度九十五三七五一"))
 def test_false_d6_pixel_sha(self):self.reject(lambda e:e["rois"][1].update(rgb_sha256="0"*64))
 def test_false_other_copy(self):self.reject(lambda e:e["source"].update(independent_witnesses_added=1))
 def test_false_decimal(self):self.reject(lambda e:e["findings"].update(original_full_decimal_d6="0.953750"))
 def test_restore_bad_13eh(self):self.reject(lambda e:e["findings"].update(prior_13eh_erratum_preserved=False))
 def test_unproved_field_map(self):self.reject(lambda e:e["findings"].update(p73_heading_to_daily_lanes="PROVEN"))
 def test_fake_d30_digit(self):self.reject(lambda e:e["findings"].update(d30_preserved="初度九十六二〇三八"))
if __name__=="__main__":unittest.main()
