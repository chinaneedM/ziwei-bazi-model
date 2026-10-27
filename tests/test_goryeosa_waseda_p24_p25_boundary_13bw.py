import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-p24-p25-boundary-13bw.py"
spec=importlib.util.spec_from_file_location("a13bw",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13BW(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.s=m.load(m.S);self.l=m.load(m.L);self.p={k:m.load(getattr(m,k)) for k in ("BV","BN","BM")}
 def check(self,e=None,s=None,l=None,p=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.p if p is None else p)
 def test_positive(self):self.assertTrue(self.check())
 def test_change_d30_heading(self):
  e=copy.deepcopy(self.e);e["original_native_day_header_rois"][2]["literal"]="三十一日"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_change_source_p25_sha(self):
  e=copy.deepcopy(self.e);e["source"]["source_images"][1]["jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_change_one_original_roi(self):
  e=copy.deepcopy(self.e);e["original_native_day_header_rois"][3]["original_native_rgb_sha256"]="f"*64
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_false_table_end(self):
  e=copy.deepcopy(self.e);e["findings"]["printed_table_end"]="D38"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_day16_cumulative_guess(self):
  e=copy.deepcopy(self.e);e["findings"]["Waseda_D16_isolated_cumulative"]="7135.8375"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_no_extra_source_votes(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_different_requested_next_pages(self):
  e=copy.deepcopy(self.e);e["acquisition_next"]["source_pages_requested"]=[25,26]
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_forward_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]});issue["next_action"]="13BX CURRENT ACTION new"
  s["schema_version"]="AFTER";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="AFTER"
  s["historical_audit"]["current_focus"].append("13BX new")
  l["binding"]["reviewed_state_version"]="AFTER";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["binding"]["latest_research_focus_prefix"]="13BX"
  l["checkpoint_log"].append({"state_version":"AFTER","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
