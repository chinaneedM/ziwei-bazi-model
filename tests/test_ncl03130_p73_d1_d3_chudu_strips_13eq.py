import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p73-d1-d3-chudu-strips-13eq.py"
spec=importlib.util.spec_from_file_location("v13eq",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EQ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.eo=m.read(m.EO);cls.ep=m.read(m.EP);cls.en=m.read(m.EN);cls.ei=m.read(m.EI);cls.ed=m.read(m.ED);cls.s=m.read(m.S);cls.l=m.read(m.L)
 def go(self,e=None):
  return m.check(self.e if e is None else e,self.eo,self.ep,self.en,self.ei,self.ed,self.s,self.l)
 def bad(self,f):
  q=copy.deepcopy(self.e);f(q)
  with self.assertRaises(AssertionError):self.go(q)
 def test_valid_source(self):self.assertTrue(self.go())
 def test_false_d1_glyph(self):self.bad(lambda e:e["rois"][0].update(visible_original="初度九十五一五一六"))
 def test_false_d2_original_sha(self):self.bad(lambda e:e["rois"][1].update(rgb_sha256="0"*64))
 def test_false_d3_day_label(self):self.bad(lambda e:e["day_label_rois_reused_from_13eo"][2].update(literal="四日"))
 def test_false_pdf_identity(self):self.bad(lambda e:e["source"].update(pdf_sha256="0"*64))
 def test_false_numeric_decimal(self):self.bad(lambda e:e["observations"].update(per_day_decimal_values=["0.951516",None,None]))
 def test_false_fen_unit_equivalence(self):self.bad(lambda e:e["observations"].update(interpretation_of_d1_fen_as_decimal_position="PROVEN"))
 def test_fabricated_field_mapping(self):self.bad(lambda e:e["observations"].update(technical_heading_to_daily_lane_identity="PROVEN"))
 def test_forged_independent_witness(self):self.bad(lambda e:e["source"].update(independent_physical_witnesses_added=3))
 def test_revive_13ei_error(self):self.bad(lambda e:e["observations"].update(prior_13ei_source_glyph_erratum_still_retracted=False))
 def test_shorthand_D1_D6_preserves_full_scope(self):
  q=copy.deepcopy(self.l);issue=next(x for x in q["issues"] if x["id"]=="TW-OPEN-0005")
  self.assertIn("D1-D6",issue["next_action"])
  self.assertTrue(m.check(self.e,self.eo,self.ep,self.en,self.ei,self.ed,self.s,q))
 def test_mutated_shorthand_does_not_certify_all_six(self):
  q=copy.deepcopy(self.l);issue=next(x for x in q["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]=issue["next_action"].replace("D1-D6","D1-D5").replace("D1 D2 D3 D4 D5 D6","D1 D2 D3 D4 D5")
  with self.assertRaises(AssertionError):
   m.check(self.e,self.eo,self.ep,self.en,self.ei,self.ed,self.s,q)
if __name__=="__main__":unittest.main()
