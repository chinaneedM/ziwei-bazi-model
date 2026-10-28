import copy,importlib.util,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13iy-official-2114-1-manuscript-conflict.py"
sp=importlib.util.spec_from_file_location("v13iy",P);M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
class SourceScope(unittest.TestCase):
 def setUp(self):self.d=M.get(M.D)
 def reject(self):
  with self.assertRaises(AssertionError):M.check(self.d)
 def test_original(self):self.assertTrue(M.check(self.d))
 def test_wrong_2114_1_sha(self):self.d["firstparty_2114_1"]["raw_sha256"]="0"*64;self.reject()
 def test_wrong_title_source_url(self):self.d["firstparty_2114_1"]["api_url"]="https://example.invalid";self.reject()
 def test_wrong_2114_1_page(self):self.d["firstparty_2114_1"]["source_discovered_official_page"]="https://example.invalid";self.reject()
 def test_wrong_2114_1_description(self):self.d["firstparty_2114_1"]["description_sha256"]="0"*64;self.reject()
 def test_wrong_official_book_list(self):self.d["firstparty_2114_1"]["manuscript_replacement_book_ordinals"]=[8,26,29];self.reject()
 def test_missing_original_12_juan_pair(self):self.d["firstparty_2114_1"]["manuscript_juan_ranges"]=[[19,21],[31,34],[73,74]];self.reject()
 def test_no_catalog_winner_without_physical(self):self.d["adjudication"]["preferred_book_sequence"]=[8,12,26];self.reject()
 def test_no_false_book29_positive(self):self.d["snu_firstparty_metadata"]["physical_book29_juan81_83"]="CONFIRMED";self.reject()
 def test_no_false_all46_missing(self):self.d["adjudication"]["gk5553_all_46_missing_81_82_unproved"]=False;self.reject()
 def test_no_ancient_page_promotion(self):self.d["firstparty_2114_1"]["ancient_physical_target_folio"]="juan82";self.reject()
 def test_no_g893_numbers_import(self):self.d["original_ancient_targets"]["g893_original_six"]=[1,2,3,4,5,6];self.reject()
 def test_no_gk5554_specific_book_promotion(self):self.d["adjudication"]["gk5554_individual_17_or_18_to_81_82"]={"81":17};self.reject()
 def test_no_ancient_genealogy_vote(self):self.d["transmission_impact"]["edges_supported"].append("FALSE");self.reject()
if __name__=="__main__":unittest.main()
