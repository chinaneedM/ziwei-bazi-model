import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wk",ROOT/"scripts/verify-yehuobian-four-era-paratext-12wk.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class FourEraImageControlled(unittest.TestCase):
 def setUp(self):
  self.o=[v.load(p) for p in (v.REC,v.WJ,v.SHARD,v.VZ,v.STATE,v.REGISTRY)]
 def reject(self,pattern):
  with self.assertRaisesRegex(ValueError,pattern):v.validate(*self.o)
 def test_live_files(self):
  self.assertEqual(v.verify()["newly_read_image_loci"],2)
 def test_source_not_a_new_source_vote(self):
  self.o[0]["counters"]["new_registered_external_sources"]=1
  self.reject("zero manufactured")
 def test_1606_is_not_1596(self):
  self.o[0]["dated_layers"][0]["year"]=1596
  self.reject("date glyph/page")
 def test_1606_sexagenary_mismatch(self):
  self.o[0]["dated_layers"][0]["year_cycle"]="丙申"
  self.reject("date glyph/page")
 def test_1827_and_1869_must_share_page5(self):
  self.o[0]["dated_layers"][2]["page"]=6
  self.reject("date glyph/page")
 def test_page7_sha_immutable(self):
  self.o[0]["dated_layers"][0]["page_sha256"]="f"*64
  self.reject("source jpeg SHA")
 def test_no_collapsing_physical_copy_across_fascicles(self):
  self.o[0]["cross_fascicle"]["independently_authenticated_same_physical_paper_copy"]=True
  self.reject("physical print cross-fascicle")
 def test_1827_first_impression_not_claimed(self):
  self.o[0]["cross_fascicle"]["original_1827_unrepaired_juan20_leaf_obtained"]=True
  self.reject("no original target folio")
 def test_no_claim_j20_target_found_in_fasc1(self):
  self.o[0]["cross_fascicle"]["printed_target_folio_read_from_this_first_fascicle"]=True
  self.reject("no original target folio")
 def test_1869_print_vote_not_from_1869_paratext(self):
  self.o[0]["counters"]["historical_print_independence_votes"]=1
  self.reject("zero manufactured")
 def test_preexisting_source_crosswitness(self):
  self.o[0]["source"]["original_djvu_sha256"]="0"*64
  self.reject("same original SHA")
 def test_reject_unsupported_ancestry(self):
  self.o[0]["transmission_impact"]["edges_supported"]=["CADAL first scanned from sixteenth"]
  self.reject("no unsupported lineage")
if __name__=="__main__":unittest.main()
