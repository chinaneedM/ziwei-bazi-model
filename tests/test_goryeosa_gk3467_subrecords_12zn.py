import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-gk3467-subrecords-12zn.py"
s=importlib.util.spec_from_file_location("tw12zn",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self):self.a=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_pass(self):self.assertEqual(v.verify(*self.a)["status"],"PASS")
 def test_no_subrecord_transfer(self):self.a[0]["first_party"]["separate_list"]["direct_book6_to_suffix_map"]="GK03467_02";self.bad()
 def test_no_generic_toc_as_glyph(self):self.a[0]["first_party"]["item_3467_4"]["per_book_work52_glyph"]="1";self.bad()
 def test_keep_3467_mixed_medium(self):self.a[0]["first_party"]["separate_snu_catalog_expository_note"]["remaining_woodblock_book_count"]=22;self.bad()
 def test_no_microfilm_double_vote(self):self.a[0]["unresolved"]["duplicate_microfilm_independent_original_votes"]=2;self.bad()
 def test_no_infer_5554_copy(self):self.a[0]["unresolved"]["gk5554_book_containing_work52"]=6;self.bad()
 def test_forward_compatible_focus(self):
  self.a[2]["historical_audit"]["current_focus"].append("12ZO new")
  self.a[3]["binding"]["source_focus_count"]+=1
  self.a[3]["binding"]["latest_research_focus_prefix"]="12ZO"
  self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
