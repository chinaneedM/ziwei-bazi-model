import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p74-d4-d6-right-column-13em.py"
spec=importlib.util.spec_from_file_location("v13em",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.el=m.read(m.EL);cls.ek=m.read(m.EK);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):return m.check(self.e if e is None else e,self.el,self.ek,self.ei,self.ed,self.s,self.l)
 def reject(self,change):
  e=copy.deepcopy(self.e);change(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_source_scope_and_handoff(self):self.assertTrue(self.go())
 def test_fake_original_glyph(self):self.reject(lambda x:x["rois"][2].update(visible_literal="一千三百七十九七一二六"))
 def test_fake_image_pixel_sha(self):self.reject(lambda x:x["rois"][0].update(rgb_sha256="0"*64))
 def test_fake_original_png_sha(self):self.reject(lambda x:x["source"].update(png_sha256="0"*64))
 def test_fictitious_witness(self):self.reject(lambda x:x["source"].update(independent_witnesses_added=1))
 def test_derived_decimal_not_original(self):self.reject(lambda x:x["findings"].update(right_neighbor_exact_numeric_d4="1441.2271"))
 def test_no_unscoped_header_equivalence(self):self.reject(lambda x:x["findings"].update(p73_technical_header_to_right_neighbor_field="PROVEN"))
 def test_no_d30_missing_digit_claim(self):self.reject(lambda x:x["findings"].update(day30_missing_digit_inference="PROVEN"))
 def test_no_merging_adjacent_lanes(self):self.reject(lambda x:x["findings"].update(same_page_right_neighbor_and_chudu_concatenation=True))
if __name__=="__main__":unittest.main()
