import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-numeric-evidence-grades-13bq.py"
spec=importlib.util.spec_from_file_location("g13bq",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class NumericGrade13BQ(unittest.TestCase):
 def setUp(self):self.e=m.load(m.P);self.src={k:m.load(path) for k,path in m.FILES.items()};self.l=m.load(m.L);self.s=m.load(m.S)
 def go(self,e=None,src=None,l=None,s=None):return m.check(self.e if e is None else e,self.src if src is None else src,self.l if l is None else l,self.s if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_fake_individual_naj_heading(self):
  e=copy.deepcopy(self.e);e["local_original_numeric_parallels"][0]["naj"]["grade"]="DIRECT_ORIGINAL_NUMERIC_AND_DAY_HEADING"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_change_legacy_day_without_supersession(self):
  e=copy.deepcopy(self.e);e["legacy_13bj_cumulative_rebindings"][0]["rebound_waseda_original_day"]=18
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_source_value(self):
  src=copy.deepcopy(self.src);src["NBG"]["source_canvases"][2]["new_day_slots"][0]["decimal"]="8000.2698"
  with self.assertRaises(AssertionError):self.go(src=src)
 def test_old_mixed_crop_for_today(self):
  e=copy.deepcopy(self.e);e["older_13be_adjoining_numerals"]["status"]="DIRECT_SAME_DAY_CUMULATIVE"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_promote_day16_ancestry(self):
  e=copy.deepcopy(self.e);e["older_13be_adjoining_numerals"]["day16_short_ancestral_winner"]="5.2362"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_source_blob_mutation(self):
  e=copy.deepcopy(self.e);e["source_files"][0]["blob_sha"]="0"*40
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_independent_witness(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_global_dayshift_false_claim(self):
  e=copy.deepcopy(self.e);e["subfinding"]["whole_table_day_offset_proven"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_extension(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);i=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  i["next_action"]="13BR CURRENT ACTION follow original";i["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT";s["historical_audit"]["current_focus"].append("13BR newer")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BR"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
