import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-correct-solar-p76-13dz.py"
s=importlib.util.spec_from_file_location("dz",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13DZ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):m.check(e,self.s,self.l)
 def test_valid(self):self.assertTrue(m.check(self.e,self.s,self.l))
 def test_false_page(self):self.bad(lambda e:e["target_field"].update(source_pdf_page=86))
 def test_fake_numeric_glyph(self):self.bad(lambda e:e["target_field"].update(original_xingdu_decimal="0.994549"))
 def test_wrong_table(self):self.bad(lambda e:e["target_field"].update(table_type="TAIYIN"))
 def test_fake_source_sha(self):self.bad(lambda e:e["original_page_register"][3].update(png_sha256="0"*64))
 def test_false_day_offset(self):self.bad(lambda e:e["cross_witness_firewall"].update(uniform_day_offset_law="PROVEN"))
 def test_false_phy_vote(self):self.bad(lambda e:e["impact"].update(new_independent_physical_copy_votes=1))
if __name__=="__main__":unittest.main()
