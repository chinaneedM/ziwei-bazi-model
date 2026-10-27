import importlib.util,copy,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("wo",ROOT/"scripts/verify-yehuobian-keio-googlebooks-access-boundary-12wo.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class GoogleBooksRateLimitEvidence(unittest.TestCase):
 def setUp(self):
  self.r=v.json.loads((ROOT/v.REC).read_text())
  self.s=v.json.loads((ROOT/v.STATE).read_text())
  self.w=(ROOT/v.WN).read_text()
  self.script=(ROOT/v.WNSCRIPT).read_text()
 def bad(self,t):
  with self.assertRaisesRegex(ValueError,t):v.validate(self.r,self.s,self.w,self.script)
 def test_live_files(self):self.assertEqual(v.verify()["ancient_original_print_votes"],0)
 def test_429_cannot_be_200(self):
  self.r["capture"]["api_response"]="HTTP_200"
  self.bad("actual HTTP rate limit")
 def test_unknown_source_sha_not_authenticated(self):
  self.r["capture"]["unmodified_provider_volume_json_sha256"]="a"*64
  self.bad("not a fetched original")
 def test_429_is_not_no_holding_proof(self):
  self.r["scope"]["source_absence_proven"]=True
  self.bad("429 cannot")
 def test_no_auto_retries_from_429(self):
  self.w=self.w.replace("    if: github.event_name == 'workflow_dispatch'\n","")
  self.bad("manual-only")
 def test_no_false_original_juan20(self):
  self.r["target"]["work_volume20_content_confirmed"]=True
  self.bad("no exact Keio")
 def test_no_new_independent_print_votes(self):
  self.r["scope"]["ancient_print_votes"]=1
  self.bad("no fabricated")
 def test_no_catalog_voting_from_429(self):
  self.r["scope"]["new_registry_sources"]=1
  self.bad("no fabricated")
 def test_no_fabricated_keio_shelfmark(self):
  self.r["target"]["independently_verified_keio_institutional_shelfmark"]="invented"
  self.bad("no exact Keio")
 def test_wrong_artifact_digest(self):
  self.r["capture"]["capture_artifact_sha256_locally_recomputed"]="1"*64
  self.bad("actual independent archive")
 def test_no_genealogy_shortcut(self):
  self.r["transmission_impact"]["edges_supported"]=["same physical copy"]
  self.bad("no new transmission")
if __name__=="__main__":unittest.main()
