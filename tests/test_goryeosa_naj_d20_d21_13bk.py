import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-naj-d20-d21-13bk.py"
sp=importlib.util.spec_from_file_location("research13bk",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class NAJ13BK(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.bg=m.load(m.PBG);self.bj=m.load(m.PBJ)
  self.yz=m.load(m.PYZ);self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,ledger=None,state=None):
  return m.check(self.e if e is None else e,self.bg,self.bj,self.yz,self.l if ledger is None else ledger,self.s if state is None else state)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_source_image_sha(self):
  e=copy.deepcopy(self.e);e["source"]["source_jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_roi_sha(self):
  e=copy.deepcopy(self.e);e["original_native_rois"][2]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_roi_coords(self):
  e=copy.deepcopy(self.e);e["original_native_rois"][1]["bbox"]=[0,0,100,100]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_original_D21(self):
  e=copy.deepcopy(self.e);e["original_native_rois"][2]["literal"]="九千二百五十七六〇〇一"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_delta(self):
  e=copy.deepcopy(self.e);e["source_local_equations"][0]["cumulative_difference"]="413.8428"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_voting(self):
  e=copy.deepcopy(self.e);e["scope_counters"]["independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_global_header_upgrade(self):
  e=copy.deepcopy(self.e);e["local_original_span_update"]["universal_day_header_law"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_Waseda_D21(self):
  e=copy.deepcopy(self.e);e["negative_controls"]["no_assumed_Waseda_D21_original"]=False
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_old_action_cannot_regress(self):
  l=copy.deepcopy(self.l);next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BJ CURRENT ACTION superseded"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_unregistered_future_action_rejected(self):
  l=copy.deepcopy(self.l)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BL UNREGISTERED ACTION"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_false_old_action_with_append_only_history(self):
  l=copy.deepcopy(self.l)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BJ CURRENT ACTION (STALE)"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_later_research_focus_does_not_rewrite_last_evidence_scoped_issue_action(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  # The 13DG issue action may remain the active next source request while a
  # later image/physical-cover batch advances the general handoff focus.
  prior_action=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]
  self.assertTrue(prior_action.startswith("13DZ CURRENT ACTION"))
  s["schema_version"]="NEXT_FOCUS_ONLY"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT_FOCUS_ONLY"
  s["historical_audit"]["current_focus"].append("13DN SOURCE-ORIGINAL BOUNDARY")
  l["binding"].update(reviewed_state_version="NEXT_FOCUS_ONLY",
    source_focus_count=len(s["historical_audit"]["current_focus"]),
    latest_research_focus_prefix="13DN")
  l["checkpoint_log"].append({"state_version":"NEXT_FOCUS_ONLY",
     "reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(ledger=l,state=s))
 def test_unrelated_future_focus_cannot_activate_an_unrecorded_issue_action(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13DN CURRENT ACTION invented"
  s["historical_audit"]["current_focus"].append("13DN FOCUS")
  s["schema_version"]="NEXT_FOCUS_ONLY"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT_FOCUS_ONLY"
  l["binding"].update(reviewed_state_version="NEXT_FOCUS_ONLY",
     source_focus_count=len(s["historical_audit"]["current_focus"]),
     latest_research_focus_prefix="13DN")
  l["checkpoint_log"].append({"state_version":"NEXT_FOCUS_ONLY",
     "reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  with self.assertRaises(AssertionError):self.go(ledger=l,state=s)
 def test_future_append_safe(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["next_action"]="13BL CURRENT ACTION test newer scoped work"
  i["history"].append({"event":"ISSUE_REVISION","date":"2026-10-21","changed_fields":["next_action"],"reason":"test forward","evidence_refs":[m.P]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT"
  s["historical_audit"]["current_focus"].append("13BL FUTURE")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BL"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(ledger=l,state=s))
if __name__=="__main__":unittest.main()
