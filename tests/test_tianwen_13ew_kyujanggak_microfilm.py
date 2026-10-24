import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13ew-kyujanggak-microfilm.py"
spec=importlib.util.spec_from_file_location("v13ew",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13EW(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.x=v.load(v.P);cls.s=v.load(v.S);cls.l=v.load(v.L)
 def test_valid(self): self.assertTrue(v.check(self.x,self.s,self.l))
 def bad(self,fn):
  x=copy.deepcopy(self.x);fn(x)
  with self.assertRaises(AssertionError):v.check(x,self.s,self.l)
 def test_fake_3579_owner(self): self.bad(lambda x:x["microfilm_groups"][0].update(source_catalog_shelfmark="奎 3579"))
 def test_false_work_juan52_map(self): self.bad(lambda x:x["microfilm_groups"][4].update(work_juan_52_bound=True))
 def test_false_original_image(self): self.bad(lambda x:x["microfilm_groups"][4].update(original_target_folio_sha256="fabricated"))
 def test_false_cross_copy(self): self.bad(lambda x:x["microfilm_groups"][3].update(cross_bind_to_GK03579=True))
 def test_false_votes(self): self.bad(lambda x:x["impact"].update(new_original_glyph_votes=2))
 def test_false_numeric_winner(self): self.bad(lambda x:x.update(winter_D16_original_numerics="5.2362"))
if __name__=="__main__":unittest.main()
