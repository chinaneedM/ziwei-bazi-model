import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("v13ix",ROOT/"scripts"/"verify-tianwen-13ix-khs-juan81-82-scope.py")
M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
class DirectGovernment(unittest.TestCase):
 def setUp(self):self.e=M.get()
 def reject(self):
  with self.assertRaises(AssertionError):M.check(self.e)
 def test_original(self):self.assertTrue(M.check(self.e))
 def test_no_modern_to_ancient_upgrade(self):self.e["interpretive_limits"]["can_claim_ancient_gk5554_book18_original_leaf_captured"]=True;self.reject()
 def test_not_all46_missing(self):self.e["interpretive_limits"]["can_claim_gk5553_all46_books_physically_lack_81_82"]=True;self.reject()
 def test_no_book29_positive_inference(self):self.e["separate_firstparty_snu_scope"]["book29_to_juan81_83"]="CONFIRMED";self.reject()
 def test_no_book29_negative_inference(self):self.e["interpretive_limits"]["can_claim_5553_book29_originally_missing_81_83"]=True;self.reject()
 def test_no_81_exact_book17(self):self.e["firstparty_khs_2114_2"]["gk5554_bounded_book_range"]["exact_book_to_individual_juan"]={"81":17};self.reject()
 def test_no_1972_or_1482_print(self):self.e["interpretive_limits"]["can_claim_1482_exact_printing_of_copy"]=True;self.reject()
 def test_g893_six_not_imported(self):self.e["pending_ancient"]["g893_six_original_numeric"]=[1]*6;self.reject()
 def test_hash_chain_not_fabricated(self):self.e["firstparty_khs_2114_2"]["body_text_sha256_utf8"]="0"*64;self.reject()
 def test_secondary_not_officially_upgraded(self):self.e["lower_authority_record"]["its_5553_manuscript_books_8_12_26_is_still_not_verified_by_THIS_2114_2_DESCRIPTION"]=False;self.reject()
 def test_43_designated_vs_46_total(self):self.e["separate_firstparty_snu_scope"]["full_catalog_books"]=43;self.reject()
 def test_same_source_not_multiple_independent_ancient(self):self.e["interpretive_limits"]["can_count_one_gov_page_as_multiple_independent_ancient_witnesses"]=True;self.reject()
if __name__=="__main__":unittest.main()
