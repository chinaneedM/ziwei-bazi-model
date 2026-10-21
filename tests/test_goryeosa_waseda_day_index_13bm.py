import copy,importlib.util,unittest
from pathlib import Path
f=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-day-index-13bm.py"
spec=importlib.util.spec_from_file_location("goryeosa13bm",f)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OriginalDayHeader13BM(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.bj=m.load(m.BJ);self.bk=m.load(m.BK);self.yz=m.load(m.YZ)
  self.ledger=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  self.state=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,l=None,s=None):
  return m.check(self.e if e is None else e,self.bj,self.bk,self.yz,self.ledger if l is None else l,self.state if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_old_D20_header_binding(self):
  e=copy.deepcopy(self.e);e["correction"]["source_original_corrected_printed_day"]=20
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_cumulative_reading(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_rois"][5]["decimal"]="9666.1508"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_heading_original_sha(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_rois"][4]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_cumulative_crop(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_rois"][3]["bbox"]=[0,0,1,1]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_full_day_shift_law(self):
  e=copy.deepcopy(self.e);e["cross_holding_local"]["whole_table_shift_law_proven"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_original_long_reading(self):
  e=copy.deepcopy(self.e);e["arithmetic"]["original_waseda_d20_long_native_roi"]="DIRECT_POSITIVE"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_independent_vote(self):
  e=copy.deepcopy(self.e);e["scope_counters"]["independent_numerical_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_stale_13BL_action(self):
  l=copy.deepcopy(self.ledger)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BL CURRENT ACTION"
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_future_append_only(self):
  l=copy.deepcopy(self.ledger);s=copy.deepcopy(self.state)
  i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["next_action"]="13BN CURRENT ACTION future scoped work"
  i["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"],"evidence_refs":[m.P]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT"
  s["historical_audit"]["current_focus"].append("13BN future work")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BN"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
