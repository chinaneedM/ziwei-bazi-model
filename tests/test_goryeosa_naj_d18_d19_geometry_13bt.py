import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-naj-d18-d19-source-geometry-13bt.py"
sp=importlib.util.spec_from_file_location("na13bt",p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class NAJ13BT(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.s=m.load(m.S);self.l=m.load(m.L);self.p={k:m.load(getattr(m,k)) for k in ("BS","BG","BQ","BR")}
 def go(self,e=None,s=None,l=None,p=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.p if p is None else p)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_day_heading(self):
  e=copy.deepcopy(self.e);e["paired_original_field_columns"][0]["heading"]="十七日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_numeric(self):
  e=copy.deepcopy(self.e);e["paired_original_field_columns"][1]["cumulative_value"]="8424.6409"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_source_sha(self):
  e=copy.deepcopy(self.e);e["firstparty_source"]["jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_original_roi_sha(self):
  e=copy.deepcopy(self.e);e["paired_original_field_columns"][0]["cumulative_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_break_geometry(self):
  e=copy.deepcopy(self.e);e["paired_original_field_columns"][0]["cumulative_bbox"]=[100,827,162,1760]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_no_uniform_day_shift(self):
  e=copy.deepcopy(self.e);e["comparison"]["uniform_all_field_day_shift_proven"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_no_new_votes(self):
  e=copy.deepcopy(self.e);e["source_scope"]["new_independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_extension(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BU CURRENT ACTION later";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="AFTER";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="AFTER";s["historical_audit"]["current_focus"].append("13BU later")
  l["binding"]["reviewed_state_version"]="AFTER";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BU"
  l["checkpoint_log"].append({"state_version":"AFTER","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
