import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-tight-roi-13bn.py"
spec=importlib.util.spec_from_file_location("goryeosa13bn",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Waseda13BN(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.bj=m.load(m.BJ);self.bm=m.load(m.BM);self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,l=None,s=None):return m.check(self.e if e is None else e,self.bj,self.bm,self.l if l is None else l,self.s if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_new_roi_sha(self):
  e=copy.deepcopy(self.e);e["original_single_numeric_lane_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_resurrect_old_mixed_bbox(self):
  e=copy.deepcopy(self.e);e["original_single_numeric_lane_rois"][0]["bbox"]=[601,690,686,1400]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_decimal(self):
  e=copy.deepcopy(self.e);e["original_single_numeric_lane_rois"][3]["value"]="408.5508"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_global_law(self):
  e=copy.deepcopy(self.e);e["cross_holding_scope"]["whole_table_shift_proven"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_vote_inflation(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_independent_source_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_original_source_overcount(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_source_jpegs_acquired"]=2
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_old_action_resurrection(self):
  l=copy.deepcopy(self.l)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BM CURRENT ACTION stale"
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_future_append_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BO CURRENT ACTION validated future"
  issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"],"evidence_refs":[m.P]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT"
  s["historical_audit"]["current_focus"].append("13BO future scoped issue")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BO"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
