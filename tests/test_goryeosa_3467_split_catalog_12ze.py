import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-3467-split-catalog-12ze.py"
s=importlib.util.spec_from_file_location("tw12ze",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Kyu3467ItemRecords(unittest.TestCase):
 def setUp(self):self.a=list(m.load())
 def bad(self):
  with self.assertRaises(ValueError):m.verify(*self.a)
 def item(self,key):return next(x for x in self.a[0]["record_groups"] if x["shelfmark"]==key)
 def test_valid(self):self.assertEqual(m.verify(*self.a)["exact_item_records_verified"],2)
 def test_no_four_independent_types(self):self.item("奎3467의3-v.12")["catalog_medium"]="乙亥字";self.bad()
 def test_exact02(self):self.item("奎3467의2")["exact_book_cd"]="GK03467_01";self.bad()
 def test_exact04(self):self.item("奎3467의4")["surviving_physical_book_count"]=5;self.bad()
 def test_nonuniform_ninth_book(self):self.item("奎3467의2")["individual_mixed_physical_book_note"]="";self.bad()
 def test_folio_false_positive(self):self.item("奎3467의2")["target_volume52_folio_proven"]=True;self.bad()
 def test_book6_02_not_proven(self):self.a[0]["scope"]["prove_book6_is_02"]=True;self.bad()
 def test_book6_04_not_proven(self):self.a[0]["scope"]["prove_book6_is_04"]=True;self.bad()
 def test_film_not_guessed(self):self.a[0]["scope"]["prove_mf_206_1_or_206_2_contains_book6"]=True;self.bad()
 def test_raw_mf_numbers(self):self.a[0]["physical_metadata"]["microfilm_catalog_literals"][1]="M/F82-16-206-2";self.bad()
 def test_edition_not_direct_vote(self):self.a[0]["scope"]["genealogy_new_independent_ancestry_edges"]=1;self.bad()
 def test_no_original_image(self):self.a[0]["physical_metadata"]["source_emitted_target_image_sha256"]="imaginary";self.bad()
 def test_unchanged_issues(self):self.a[3]["issues"][4]["status"]="RESOLVED_WITH_EVIDENCE";self.bad()
 def test_state_version(self):self.a[3]["binding"]["reviewed_state_version"]="1.642.0";self.bad()
 def test_future_research_batch_without_immutable_backrewrite(self):
  self.a[2]["historical_audit"]["current_focus"].append("12ZF future research")
  self.a[3]["binding"]["source_focus_count"]+=1
  self.a[3]["binding"]["latest_research_focus_prefix"]="12ZF"
  self.assertEqual(m.verify(*self.a)["status"],"PASS")
 def test_stale_prefix_caught(self):
  self.a[3]["binding"]["latest_research_focus_prefix"]="12ZD";self.bad()
if __name__=="__main__":unittest.main()
