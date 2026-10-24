import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p73-summer-richa-13ep.py"
spec=importlib.util.spec_from_file_location("v13ep",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.P);cls.eo=m.read(m.EO);cls.en=m.read(m.EN);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):return m.check(self.e if e is None else e,self.eo,self.en,self.ei,self.ed,self.s,self.l)
 def reject(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_baseline(self):self.assertTrue(self.go())
 def test_reject_false_original_glyph(self):self.reject(lambda e:e["rois"][0].update(visible_literal="日差加一秒八十六少"))
 def test_reject_false_source_crop(self):self.reject(lambda e:e["rois"][0].update(rgb_sha256="0"*64))
 def test_reject_false_source_page(self):self.reject(lambda e:e["source"].update(png_sha256="0"*64))
 def test_reject_imputed_decimal(self):self.reject(lambda e:e["findings"].update(historical_decimal="0.0162"))
 def test_reject_wrong_day_value(self):self.reject(lambda e:e["findings"].update(technical_subheader_does_not_equal_day_specific_printed_row=False))
 def test_reject_witness_inflation(self):self.reject(lambda e:e["source"].update(new_independent_physical_witnesses=1))
 def test_reject_imputed_p74_mapping(self):self.reject(lambda e:e["findings"].update(p73_to_p74_day4_6_field_assignment="PROVEN"))
if __name__=="__main__":unittest.main()
