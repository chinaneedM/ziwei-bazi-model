import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p73-headings-p74-day-sequence-13eo.py"
spec=importlib.util.spec_from_file_location("v13eo",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EO(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.en=m.read(m.EN);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):return m.check(self.e if e is None else e,self.en,self.ei,self.ed,self.s,self.l)
 def reject(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_p73_p74_source_handoff(self):self.assertTrue(self.go())
 def test_reject_false_header_glyph(self):self.reject(lambda e:e["rois"][1].update(visible_literal="盈縮程"))
 def test_reject_false_pixel_hash(self):self.reject(lambda e:e["rois"][3].update(rgb_sha256="0"*64))
 def test_reject_false_p73_source_sha(self):self.reject(lambda e:e["source"]["original_page_73"].update(png_sha256="0"*64))
 def test_reject_imputed_lane_mapping(self):self.reject(lambda e:e["findings"].update(p73_header_to_p74_d4_d5_d6_fourfen="PROVEN"))
 def test_reject_imputed_day30_decimal(self):self.reject(lambda e:e["findings"].update(d30_decimal="0.96203"))
 def test_reject_forged_independent_witness(self):self.reject(lambda e:e["source"].update(independent_witnesses_added=1))
 def test_reject_13en_promoted_to_full_digits(self):self.reject(lambda e:e["findings"].update(source_original_d4_d5_d6_fourfen_complete_lanes=[True,True,True]))
if __name__=="__main__":unittest.main()
