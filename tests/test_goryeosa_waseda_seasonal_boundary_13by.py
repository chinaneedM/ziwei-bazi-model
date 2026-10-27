import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-seasonal-boundary-13by.py"
spec=importlib.util.spec_from_file_location("source13by",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Source13BY(unittest.TestCase):
 def setUp(self):self.e=m.load(m.P);self.s=m.load(m.S);self.l=m.load(m.L);self.prev={k:m.load(getattr(m,k)) for k in ("BX","BV")}
 def go(self,e=None,s=None,l=None,p=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.prev if p is None else p)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_terminal(self):
  e=copy.deepcopy(self.e);e["findings"]["last_winter_printed_day"]="八十九日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_summer_title(self):
  e=copy.deepcopy(self.e);e["findings"]["next_title_original_literal"]="大陽冬至"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_unjustified_title_normalization(self):
  e=copy.deepcopy(self.e);e["findings"]["historical_original_title_normalization_winner"]="太"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_source_day0_must_reset(self):
  e=copy.deepcopy(self.e);e["findings"]["summer_initial_days"]=["八十九日","九十日"]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_no_d16_cumulative_guess(self):
  e=copy.deepcopy(self.e);e["findings"]["Waseda_D16_independent_cumulative"]="7135.8375"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_reject_physical_copy_vote(self):
  e=copy.deepcopy(self.e);e["scope"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_original_source_sha(self):
  e=copy.deepcopy(self.e);e["source"]["source_images"][1]["sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_source_roi_sha(self):
  e=copy.deepcopy(self.e);e["original_rgb_lanes"][3]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_future_append_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]});issue["next_action"]="13BZ CURRENT ACTION future"
  s["schema_version"]="FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE";s["historical_audit"]["current_focus"].append("13BZ future")
  l["binding"]["reviewed_state_version"]="FUTURE";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BZ"
  l["checkpoint_log"].append({"state_version":"FUTURE","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
