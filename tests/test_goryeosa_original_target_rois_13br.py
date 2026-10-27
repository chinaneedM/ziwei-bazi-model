import copy,importlib.util,unittest,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
a=R/"scripts"/"acquire-goryeosa-original-target-rois-13br.py"
spec=importlib.util.spec_from_file_location("acq13br",a)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
vpath=R/"scripts"/"verify-goryeosa-original-target-rois-13br.py"
spec2=importlib.util.spec_from_file_location("verify13br",vpath)
v=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(v)
class Acquire13BR(unittest.TestCase):
 def setUp(self):self.e=v.load(v.P);self.st=v.load(v.S);self.ld=v.load(v.L)
 def test_positive_source_and_state(self):self.assertTrue(v.check(self.e,self.st,self.ld))
 def test_unapproved_host(self):self.assertFalse(m.allowed_url("https://fake.example/path","archive.wul.waseda.ac.jp"))
 def test_remote_redirect_is_not_authorized(self):self.assertFalse(m.allowed_url("https://www.digital.archives.go.jp/path?token=1","www.digital.archives.go.jp"))
 def test_manifest_sha_protection(self):
  with self.assertRaises((ValueError,KeyError)):m.naj_original_url(b'{"sequences":[{"canvases":[]}]}')
 def test_day16_glyph_cannot_be_predeclared(self):
  e=copy.deepcopy(self.e);e["d16_original_numeric_claim"]="7135.8375"
  with self.assertRaises(AssertionError):m.validate_spec(e)
 def test_naj_day_heading_cannot_be_predeclared(self):
  e=copy.deepcopy(self.e);e["naj_d18_d19_heading_claim"]="VERIFIED"
  with self.assertRaises(AssertionError):m.validate_spec(e)
 def test_out_of_bounds_crop(self):
  e=copy.deepcopy(self.e);e["sources"][0]["roi_plan"][0]["bbox"][2]=3000
  with self.assertRaises(AssertionError):m.validate_spec(e)
 def test_wrong_source_digest(self):
  e=copy.deepcopy(self.e);e["sources"][1]["image_sha256"]="0"*64
  with self.assertRaises(AssertionError):m.validate_spec(e)
 def test_false_source_votes(self):
  e=copy.deepcopy(self.e);e["source_scope"]["source_witnesses"]=1
  with self.assertRaises(AssertionError):m.validate_spec(e)
 def test_state_bind_and_forward_only(self):
  l=copy.deepcopy(self.ld);s=copy.deepcopy(self.st)
  issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BS CURRENT ACTION future work";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE"
  s["historical_audit"]["current_focus"].append("13BS future evidence")
  l["binding"]["reviewed_state_version"]="FUTURE";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["binding"]["latest_research_focus_prefix"]="13BS"
  l["checkpoint_log"].append({"state_version":"FUTURE","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(v.check(self.e,s,l))
if __name__=="__main__":unittest.main()
