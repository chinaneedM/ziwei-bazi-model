import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p73-d1-d3-fourfen-13er.py"
spec=importlib.util.spec_from_file_location("v13er",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13ER(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.eq=m.read(m.EQ);cls.en=m.read(m.EN);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):
  return m.check(self.e if e is None else e,self.eq,self.en,self.ei,self.ed,self.s,self.l)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_source_scope(self):self.assertTrue(self.go())
 def test_false_d1_glyph(self):self.bad(lambda e:e["rois"][0].update(visible_original="四分四五二五"))
 def test_false_d2_crop(self):self.bad(lambda e:e["rois"][1].update(rgb_sha256="0"*64))
 def test_false_d3_original_page(self):self.bad(lambda e:e["source"].update(png_sha256="0"*64))
 def test_fake_historical_decimal(self):self.bad(lambda e:e["findings"].update(numeric_fourfen_values=["0.4524",None,None]))
 def test_fake_complete_field(self):self.bad(lambda e:e["findings"].update(complete_original_fourfen_field_proven=[True,False,False]))
 def test_fake_cross_field_assignment(self):self.bad(lambda e:e["findings"].update(p73_field_title_to_numeric_lane="PROVEN"))
 def test_fake_independent_copies(self):self.bad(lambda e:e["source"].update(new_independent_physical_witnesses=3))
 def test_revival_13ei_false_gloss(self):self.bad(lambda e:e["findings"].update(prior_13ei_chudu_roi_misreading_retracted=False))
if __name__=="__main__":unittest.main()
