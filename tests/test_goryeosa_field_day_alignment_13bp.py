import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-field-day-alignment-13bp.py"
spec=importlib.util.spec_from_file_location("goryeosa13bp",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Alignment13BP(unittest.TestCase):
 def setUp(self):self.e=m.load(m.P);self.w=m.load(m.W);self.n=m.load(m.N);self.l=m.load(m.L);self.s=m.load(m.S)
 def go(self,e=None,w=None,n=None,l=None,s=None):return m.check(self.e if e is None else e,self.w if w is None else w,self.n if n is None else n,self.l if l is None else l,self.s if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_all_field_day_shift(self):
  e=copy.deepcopy(self.e);e["observed_local_matches"][2]["naj_day"]=20
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_naj_original_day(self):
  n=copy.deepcopy(self.n);next(z for z in n["original_native_rois"] if z["key"]=="D21_CUM")["layout_day"]=20
  with self.assertRaises(AssertionError):self.go(n=n)
 def test_wrong_waseda_original_numeral(self):
  w=copy.deepcopy(self.w);next(z for z in w["original_single_numeric_lane_rois"] if z["key"]=="P23_D19_C")["value"]="8843.7572"
  with self.assertRaises(AssertionError):self.go(w=w)
 def test_wrong_source_git_hash(self):
  e=copy.deepcopy(self.e);e["source_files"][0]["git_blob_sha"]="0"*40
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_inflate_votes(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["independent_lineage_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_algorithm_reopen(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["algorithm_reopens"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_omit_issue_crosswalk(self):
  l=copy.deepcopy(self.l);next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")["source_refs"].remove(m.P)
  with self.assertRaises(AssertionError):self.go(l=l)
 def test_future_forward_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BQ CURRENT ACTION follow-up";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE";s["historical_audit"]["current_focus"].append("13BQ next check")
  l["binding"]["reviewed_state_version"]="FUTURE";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BQ"
  l["checkpoint_log"].append({"state_version":"FUTURE","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
