import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fn-kyudb-book-to-juan-crosswalk.py"
sp=importlib.util.spec_from_file_location("v13fn",p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class Test13FN(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.load(v.E);cls.fm=v.load(v.FM);cls.fk=v.load(v.FK);cls.s=v.load(v.S);cls.l=v.load(v.L)
 def reject(self,f):
  e=copy.deepcopy(self.e);f(e)
  with self.assertRaises(AssertionError):v.check(e,self.fm,self.fk,self.s,self.l)
 def test_valid(self):self.assertTrue(v.check(self.e,self.fm,self.fk,self.s,self.l))
 def test_false_book28(self):self.reject(lambda e:e["gk5553"]["repaired_book_to_work_juan"][2].update(book=28))
 def test_conflate_other_copy(self):self.reject(lambda e:e["gk3467"].update(separate_physical_copy_from_GK5553=False))
 def test_fake_juan52_book_for_GK5553(self):self.reject(lambda e:e["gk5553"].update(work_juan52_to_physical_book=19))
 def test_book29_microfilm_mismatch(self):self.reject(lambda e:e["gk5553"].update(microfilm_group_for_book29="M/F74-102-17-1"))
 def test_book6_target_photo_not_captured(self):self.reject(lambda e:e["gk3467"].update(original_leaf_photo_seen=True))
 def test_original_D5_opposition(self):self.reject(lambda e:e["historical_firewall"].update(NLC_D5="四分五一七二"))
 def test_D9_missing(self):self.reject(lambda e:e["historical_firewall"].update(NLC_D9_gutter="五八二〇"))
 def test_no_claim_article_direct(self):self.reject(lambda e:e["scholarly_disagreement"].update(journal_pdf_page_image_attested=True))
 def test_source_not_an_original(self):self.reject(lambda e:e["impact"].update(independent_physical_originals_added=1))
if __name__=="__main__":unittest.main()
