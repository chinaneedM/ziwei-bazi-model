import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-p26-p27-original-13bx.py"
sp=importlib.util.spec_from_file_location("g13bx",p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Test13BX(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.s=m.load(m.S);self.l=m.load(m.L);self.p={k:m.load(getattr(m,k)) for k in ("BW","BV")}
 def go(self,e=None,s=None,l=None,p=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.p if p is None else p)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_day_header(self):
  e=copy.deepcopy(self.e);e["original_day_header_rois"][-1]["literal"]="五十七日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_source_jpeg(self):
  e=copy.deepcopy(self.e);e["source"]["images"][0]["jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_pixel_sha(self):
  e=copy.deepcopy(self.e);e["original_day_header_rois"][0]["pixel_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fake_table_end(self):
  e=copy.deepcopy(self.e);e["extension_summary"]["historical_full_table_end"]="D56"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fake_d16_cumulative(self):
  e=copy.deepcopy(self.e);e["extension_summary"]["Waseda_D16_independent_cumulative"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_scope_vote_gate(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_atlas_page_bounds(self):
  e=copy.deepcopy(self.e);e["requested_atlas"]["pages_last"]=55
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_only_append(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BY CURRENT ACTION next";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT";s["historical_audit"]["current_focus"].append("13BY future")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BY"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
