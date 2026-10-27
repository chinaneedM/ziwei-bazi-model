import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'verify-tianwen-13ex-nikh-image-provider.py'
s=importlib.util.spec_from_file_location('v13ex',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13EX(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.a=v.get(v.P);cls.b=v.get(v.H);cls.m=v.get(v.M);cls.c=v.get(v.C);cls.l=v.get(v.L)
 def test_valid(self):self.assertTrue(v.check(self.a,self.b,self.m,self.c,self.l))
 def deny(self,fn):
  a=copy.deepcopy(self.a);fn(a)
  with self.assertRaises(AssertionError):v.check(a,self.b,self.m,self.c,self.l)
 def test_fake_1613_copy_assignment(self):self.deny(lambda x:x['scope'].update(catalog_copy_id='GK03539_00'))
 def test_fake_original_image(self):self.deny(lambda x:x['scope'].update(exact_article_image_acquired=True))
 def test_fake_ancient_witness(self):self.deny(lambda x:x['impact'].update(physical_glyph_votes=2))
 def test_false_historical_digit(self):self.deny(lambda x:x['context'].update(ncl_original_d5='四分五一七二'))
 def test_false_numeric(self):self.deny(lambda x:x['context'].update(summer_d30_numeric='95.0'))
 def test_reopen(self):self.deny(lambda x:x['impact'].update(algorithms_reopened=1))
if __name__=='__main__':unittest.main()
