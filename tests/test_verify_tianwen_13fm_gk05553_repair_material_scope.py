import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fm-gk05553-repair-material-scope.py"
spec=importlib.util.spec_from_file_location("v13fm",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13FM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.read(v.E);cls.fl=v.read(v.FL);cls.fk=v.read(v.FK);cls.s=v.read(v.S);cls.l=v.read(v.L)
 def test_good(self):self.assertTrue(v.check(self.e,self.fl,self.fk,self.s,self.l))
 def reject(self,f):
  e=copy.deepcopy(self.e);f(e)
  with self.assertRaises(AssertionError):v.check(e,self.fl,self.fk,self.s,self.l)
 def test_handcopy_not_woodblock(self):self.reject(lambda e:e["first_party_same_holding_two_descriptions"]["source_2"].update(interpreted_media="WOODBLOCK_SUPPLEMENT"))
 def test_official_book29_not_erased(self):self.reject(lambda e:e["first_party_same_holding_two_descriptions"]["source_1"].update(reported_ordinals=[8,26,28]))
 def test_reprint_28_not_erased(self):self.reject(lambda e:e["secondary_article_republication"].update(ordinals=[8,26,29]))
 def test_blog_not_promoted_to_government_primary(self):self.reject(lambda e:e["third_republication_heritage_description_lead"].update(heritage_official_original_exact_page_directly_checked=True))
 def test_article_pdf_uncertified(self):self.reject(lambda e:e["secondary_article_republication"].update(direct_original_journal_pdf_target_page_image_verified=True))
 def test_two_same_holding_descriptions_not_two_originals(self):self.reject(lambda e:e["differentiation"].update(independent_physical_originals_authenticated_here=2))
 def test_preserve_nlc_d5(self):self.reject(lambda e:e["chart_and_original_witness_firewall"].update(NLC_13FK_D5="四分五一七二"))
 def test_preserve_nlc_d9(self):self.reject(lambda e:e["chart_and_original_witness_firewall"].update(NLC_13FK_D9_gutter="四分五八二〇"))
 def test_no_new_genealogy_or_runtime(self):self.reject(lambda e:e["impact"].update(algorithm_reopens=1))
if __name__=="__main__":unittest.main()
