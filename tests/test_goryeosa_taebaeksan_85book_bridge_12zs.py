import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-taebaeksan-85book-bridge-12zs.py"
spec=importlib.util.spec_from_file_location("t12zs",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self):self.a=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_live(self):self.assertEqual(v.verify(*self.a)["status"],"PASS")
 def test_not_same_scholar_three_votes(self):self.a[0]["kci2017"]["independent_scholar_votes_across_three_papers"]=3;self.bad()
 def test_no_odaesan_alias(self):self.a[0]["snu"]["taebaeksan"]["catalog_id"]="GK03579_00";self.bad()
 def test_no_original_print_glyph(self):self.a[0]["unresolved"]["snu_gk03539_work52_native_sha256"]="abc";self.bad()
 def test_no_guess_from_microfilm(self):self.a[0]["snu"]["taebaeksan"]["exact_book_containing_work52"]=52;self.bad()
 def test_no_article_forged_item(self):self.a[0]["bridge"]["article_explicitly_provided_gk03539_number"]=True;self.bad()
 def test_plate_not_double_vote(self):self.a[0]["unresolved"]["new_ancestral_woodblock_votes"]=2;self.bad()
 def test_forward_manifest_growth(self):
  self.a[3]["extension_source_count"]+=1;self.a[3]["combined_source_count"]+=1
  self.a[4]["historical_audit"]["external_source_registry_extension_count"]+=1
  self.a[4]["historical_audit"]["external_source_registry_total_unique_count"]+=1
  self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
