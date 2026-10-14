import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("cadal12vz",ROOT/"scripts/verify-yehuobian-cadal-parallel-source-12vz.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class FacsimileScope(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.REC).read_text());self.s=json.loads((ROOT/v.SHARD).read_text())
  self.m=json.loads((ROOT/v.MAN).read_text());self.st=json.loads((ROOT/v.STATE).read_text())
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.s,self.m,self.st)
 def test_committed_source_integrity(self):self.assertEqual(v.verify()["independent_1827_1869_print_votes"],0)
 def test_two_digital_images_not_physical_prints(self):
  self.r["source_scope"]["different_print_plates_unproved"]=False;self.bad("physical stemma")
 def test_exact_target_reading_not_old_misread(self):
  self.r["source_page_crosswalk"]["original_image_page_reading"]["CLOCK_NOUN"]["reading"]="宮漏";self.bad("exact target readings")
 def test_winter_not_converted_to_one_ke(self):
  self.r["source_page_crosswalk"]["original_image_page_reading"]["BEIJING_WINTER_SUNRISE"]["reading"]="辰初一刻";self.bad("exact target readings")
 def test_print_date_unbound(self):
  self.r["source_page_crosswalk"]["revised_1869_impression_proven"]=True;self.bad("date protection")
 def test_page_offset_only_local(self):
  self.r["source_page_crosswalk"]["offset_is_not_global_page_by_page_proof"]=False;self.bad("page scope")
 def test_no_independent_print_vote(self):
  self.r["source_page_crosswalk"]["independent_historical_print_copy_votes_proven"]=1;self.bad("independent print vote")
 def test_wrong_image_sha(self):
  self.r["source_page_crosswalk"]["page_sha256"]["new_p119"]="a"*64;self.bad("page binary")
 def test_duplicate_shard_registration_rejected(self):
  self.m["shards"][-1]["source_count"]=2;self.bad("registry shard")
 def test_future_growth_allowed(self):
  self.m["extension_source_count"]+=1;self.m["combined_source_count"]+=1;self.st["historical_audit"]["external_source_registry_total_unique_count"]+=1
  self.assertEqual(v.validate(self.r,self.s,self.m,self.st)["status"],"PASS")
if __name__=="__main__":unittest.main()
