import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("columbia12vx",ROOT/"scripts/verify-yehuobian-columbia-shard111-observation-12vx.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class Shard111Scope(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.RECORD).read_text())
  self.p=json.loads((ROOT/v.PARENT).read_text())
  self.s=json.loads((ROOT/v.STATE).read_text())
  self.m=json.loads((ROOT/v.MANIFEST).read_text())
 def bad(self,needle):
  with self.assertRaisesRegex(ValueError,needle):v.validate(self.r,self.p,self.s,self.m)
 def test_current_log_snapshot(self):
  self.assertEqual(v.verify()["parsed_records"],21553)
 def test_wrong_exact_head(self):
  self.r["exact_git_workflow"]["head_sha"]="0"*40;self.bad("exact head")
 def test_faked_independent_hash(self):
  self.r["exact_git_workflow"]["source_gzip_redownloaded_in_this_batch"]=True;self.bad("independent rehash")
 def test_wrong_gzip_digest(self):
  self.r["observed_probe"]["source_sha256"]="a"*64;self.bad("source binding")
 def test_wrong_parsed_count(self):
  self.r["observed_probe"]["record_count"]=21554;self.bad("runner log")
 def test_single_shard_cannot_count_as_full_catalog(self):
  self.r["observed_probe"]["whole_catalog_searched"]=True;self.bad("global catalog")
 def test_nonhit_does_not_refute_columbia_holdings(self):
  self.r["claim_firewall"]["no_columbia_1827_copy_negated"]=True;self.bad("unsafe negative")
 def test_no_ancient_glyph_vote(self):
  self.r["observed_probe"]["ancient_glyph_votes"]=1;self.bad("global catalog")
 def test_source_not_reregistered(self):
  self.r["accounting"]["new_registered_external_sources"]=1;self.bad("false source")
 def test_forward_growth_count(self):
  self.m["combined_source_count"]+=1;self.m["extension_source_count"]+=1;self.s["historical_audit"]["external_source_registry_total_unique_count"]+=1
  self.assertEqual(v.validate(self.r,self.p,self.s,self.m)["status"],"PASS")
if __name__=="__main__":unittest.main()
