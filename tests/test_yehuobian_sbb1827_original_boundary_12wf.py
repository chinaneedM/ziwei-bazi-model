import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("wf",ROOT/"scripts/verify-yehuobian-sbb1827-original-boundary-12wf.py")
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class ProvenanceFirewall(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/v.REC).read_text());self.state=json.loads((ROOT/v.STATE).read_text())
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.state)
 def test_exact_source_metadata(self):self.assertEqual(v.verify()["original_1827_1869_print_votes"],0)
 def test_38_samples_not_complete_volume(self):
  self.r["berlin"]["actual_manifest"]["canvas_count_is_not_page_count_of_entire_historical_set"]=False;self.bad("preview vs complete-book")
 def test_zero_article_labels_not_absence_proof(self):
  self.r["berlin"]["actual_manifest"]["all_38_pages_manually_examined"]=True;self.bad("preview vs complete-book")
 def test_source_digest_must_match(self):
  self.r["berlin"]["actual_mets"]["source_sha256"]="a"*64;self.bad("actual METS source")
 def test_census_title_not_pretend_searched(self):
  self.r["wenzhou"]["database_search_for_this_specific_wenzhou_title_completed"]=True;self.bad("no false item search result")
 def test_modern_catalogue_not_ancient_book(self):
  self.r["wenzhou"]["catalogue_2017_copy_is_not_original_1827_yehuobian"]=False;self.bad("modern reference book")
 def test_no_invented_census_id(self):
  self.r["wenzhou"]["wenzhou_specific_yehuobian_census_number"]="330000-1704-1";self.bad("original census title item unbound")
 def test_no_ancient_copy_vote(self):
  self.r["summary"]["new_independent_historical_print_votes"]=1;self.bad("no added original votes")
if __name__=="__main__":unittest.main()
