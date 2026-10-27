import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fo-kyudb-3467-book6-reels.py"
spec=importlib.util.spec_from_file_location("v13fo",P);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test13FO(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.read(v.E);cls.fn=v.read(v.FN);cls.s=v.read(v.S);cls.l=v.read(v.L)
 def reject(self,mut):
  e=copy.deepcopy(self.e);mut(e)
  with self.assertRaises(AssertionError):v.check(e,self.fn,self.s,self.l)
 def test_base(self):self.assertTrue(v.check(self.e,self.fn,self.s,self.l))
 def test_book6_not_woodblock(self):self.reject(lambda e:e["firstparty_holding_3467"][0].update(book6_in_eulhae_segment=False))
 def test_six_book_original_detail(self):self.reject(lambda e:e["firstparty_holding_3467"][1].update(original_six_eulhae_books=[26,27,28,29,30]))
 def test_reel_exact_verbatim(self):self.reject(lambda e:e["candidate_sublibrary_records"][0].update(microfilm_identifiers_verbatim=["M/F82-166-206-1","M/F82-166-206-2"]))
 def test_subgroup_cannot_be_book6_without_scan(self):self.reject(lambda e:e["candidate_sublibrary_records"][0].update(specific_book6_in_this_subrecord=6))
 def test_two_subgroups_not_ancient_independent_photos(self):self.reject(lambda e:e["impact"].update(new_authenticated_physical_originals=2))
 def test_no_source_original_without_page(self):self.reject(lambda e:e["firstparty_holding_3467"][0].update(source_original_leaf=10))
 def test_paper_pdf_index_not_direct_page(self):self.reject(lambda e:e["identity_firewall"].update(original_2020_Wei_Chen_PDF_direct_target_page_obtained=True))
 def test_NLC_D5_unresolved(self):self.reject(lambda e:e["historical_control_firewall"].update(D5_winner="四分五一七二"))
 def test_NLC_D9_unresolved(self):self.reject(lambda e:e["historical_control_firewall"].update(NLC_13FK_D9="五八二〇"))
 def test_G893_stays_open(self):self.reject(lambda e:e["historical_control_firewall"].update(g893_six_original_controls="CLOSED"))
if __name__=="__main__":unittest.main()
