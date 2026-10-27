import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-13bs-native-glyphs.py"
spec=importlib.util.spec_from_file_location("g13bs",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Glyph13BS(unittest.TestCase):
 def setUp(self):self.e=m.load(m.P);self.br=m.load(m.BR);self.bq=m.load(m.BQ);self.bg=m.load(m.BG);self.l=m.load(m.L);self.s=m.load(m.S)
 def go(self,e=None,l=None,s=None):return m.check(self.e if e is None else e,self.br,self.bq,self.bg,self.l if l is None else l,self.s if s is None else s)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_original_literal(self):
  e=copy.deepcopy(self.e);e["original_rgb_rois"][3]["literal"]="十七日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_original_roi_sha(self):
  e=copy.deepcopy(self.e);e["original_rgb_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_source_artifact(self):
  e=copy.deepcopy(self.e);e["source_images"][0]["artifact_id"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_day16_cumulative(self):
  e=copy.deepcopy(self.e);e["upgraded_scope"]["WASEDA_D16_CUMULATIVE"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_naj_number_to_heading_binding(self):
  e=copy.deepcopy(self.e);e["upgraded_scope"]["NAJ_D18_D19_HEADING_TO_CUMULATIVE_FIELD"]="CLOSED"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_stemmatic_vote(self):
  e=copy.deepcopy(self.e);e["firewall"]["new_independent_stemma_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_global_index_false_promotion(self):
  e=copy.deepcopy(self.e);e["upgraded_scope"]["WHOLE_TABLE_INDEX"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s);i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  i["next_action"]="13BT CURRENT ACTION newer";i["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="FUTURE";s["historical_audit"]["current_focus"].append("13BT later")
  l["binding"]["reviewed_state_version"]="FUTURE";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BT"
  l["checkpoint_log"].append({"state_version":"FUTURE","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(l=l,s=s))
if __name__=="__main__":unittest.main()
