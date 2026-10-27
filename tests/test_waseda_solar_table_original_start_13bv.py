import copy,importlib.util,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/"scripts"/"verify-waseda-solar-table-original-start-13bv.py"
sp=importlib.util.spec_from_file_location("source13bv",P);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class SolarStart13BV(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.s=m.load(m.S);self.l=m.load(m.L)
  self.old={k:m.load(getattr(m,k)) for k in ("BU","BS","BN")}
 def go(self,e=None,s=None,l=None,old=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.old if old is None else old)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_source_table_title(self):
  e=copy.deepcopy(self.e);e["finding"]["solar_table_original_title"]="太陽春分"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_rename_day_zero(self):
  e=copy.deepcopy(self.e);e["source_local_table_sequence"][0]["visible_initial_days"][0]="零日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_jiri_equivalence(self):
  e=copy.deepcopy(self.e);e["finding"]["printed_JIRI_equivalent_to_cumulative_numeric_field"]="YES"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_day16_cumulative(self):
  e=copy.deepcopy(self.e);e["finding"]["Waseda_day16_exact_independent_cumulative"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_bogus_original_sha(self):
  e=copy.deepcopy(self.e);e["source_original_header_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_page_provenance(self):
  e=copy.deepcopy(self.e);e["source"]["firstparty_original_images"][0]["xref"]=65
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_independent_lineage_votes(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_only_compatible(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BW CURRENT ACTION next";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT";s["historical_audit"]["current_focus"].append("13BW later")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BW"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
