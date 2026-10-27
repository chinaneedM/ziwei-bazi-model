import copy,importlib.util,unittest
from pathlib import Path
loc=Path(__file__).resolve().parents[1]/'scripts'/'verify-tianwen-13ey-nikh-image-link-lifecycle.py'
s=importlib.util.spec_from_file_location('v13ey',loc);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13EY(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.get(v.P);cls.sh=v.get(v.SH);cls.m=v.get(v.M);cls.st=v.get(v.C);cls.l=v.get(v.L)
 def good(self,e=None):return v.check(self.e if e is None else e,self.sh,self.m,self.st,self.l)
 def bad(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.good(x)
 def test_valid(self):self.assertTrue(self.good())
 def test_fake_notice_body(self):self.bad(lambda x:x['notice_2023'].update(body_text_read=True))
 def test_imputed_notice_destination(self):self.bad(lambda x:x['notice_2023'].update(new_link_destination='GK03539_00'))
 def test_conflate_jeolyo(self):self.bad(lambda x:x['notice_2026'].update(same_work_as_target=True))
 def test_fake_exact_goryeosa_image(self):self.bad(lambda x:x['notice_2026'].update(exact_goryeosa_volume52_image_covered=True))
 def test_treat_snippet_as_target_proof(self):self.bad(lambda x:x['indexed_alternative_source_labels'].update(verified_on_target_article=True))
 def test_fake_original_image(self):self.bad(lambda x:x['target_article'].update(image_sha256='0'*64))
 def test_false_ancient_glyph(self):self.bad(lambda x:x['target_article'].update(glyph_winner='五'))
 def test_false_stemma_edge(self):self.bad(lambda x:x['impact'].update(new_genealogy_edges=1))
 def test_reopen_algorithm(self):self.bad(lambda x:x['impact'].update(algorithms_reopened=1))
if __name__=='__main__':unittest.main()
