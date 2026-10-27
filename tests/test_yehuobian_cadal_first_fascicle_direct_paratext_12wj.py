import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wj",ROOT/"scripts/verify-yehuobian-cadal-first-fascicle-direct-paratext-12wj.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class ImageBoundLoci(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.REC).read_text())
  self.sh=json.loads((ROOT/v.SHARD).read_text())
  self.m=json.loads((ROOT/v.MAN).read_text())
  self.state=json.loads((ROOT/v.STATE).read_text())
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.sh,self.m,self.state)
 def test_local_live_file_digests(self):self.assertEqual(v.verify()["independent_1827_1869_original_print_votes"],0)
 def test_1869_paratext_not_proof_of_actual_impression(self):
  self.r["witness"]["edition_impression_date_bound"]=True
  self.bad("paper imprint provenance firewall")
 def test_old_1700_preface_not_1700_print(self):
  self.r["textual_scope"]["actual_source_printed_paper_impression_year"]=1700
  self.bad("not a source-bound physical copy")
 def test_no_cross_fascicle_item_identity(self):
  self.r["textual_scope"]["paper_source_copy_to_CADAL02096915_identity"]="SAME_PAPER_COPY"
  self.bad("not a source-bound physical copy")
 def test_1869_colophon_must_be_on_page_five(self):
  self.r["witness"]["manually_collated_pages"][0]["visible"]="wrong text"
  self.bad("1869 printed revision preface")
 def test_no_manufactured_independent_glyph_votes(self):
  self.r["source_scope"]["new_independent_historical_print_votes"]=1
  self.bad("no historical 1827/1869 target source vote")
 def test_no_wrong_photo_page_sha(self):
  self.r["witness"]["manually_collated_pages"][1]["sha256"]="a"*64
  self.bad("photo page identity")
 def test_no_false_archive_digest_validation(self):
  self.r["source_capture"]["artifact_zip_sha256_locally_recomputed"]="b"*64
  self.bad("independently verified artifact")
 def test_shard_append_order_independent(self):
  self.assertNotEqual(self.m["shards"][0]["path"],v.SHARD)
  self.assertEqual(v.validate(self.r,self.sh,self.m,self.state)["status"],"PASS")
 def test_source_registry_scope(self):
  self.sh["sources"][0]["physical_glyph_authority"]=False
  self.bad("new source ID")
if __name__=="__main__":unittest.main()
