import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-summer-terminus-13bz.py"
sp=importlib.util.spec_from_file_location("g13bz",p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Summer13BZ(unittest.TestCase):
 def setUp(self):self.e=m.load(m.P);self.s=m.load(m.STATE);self.l=m.load(m.LEDGER);self.prev={"BY":m.load(m.BY),"BX":m.load(m.BX)}
 def go(self,e=None,s=None,l=None,prev=None):return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.prev if prev is None else prev)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_day94(self):
  e=copy.deepcopy(self.e);e["original_segment_context"]["claimed_day94_original"]=True
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_missing_repeated_day93(self):
  e=copy.deepcopy(self.e);e["original_segment_context"]["summer_printed_D93_occurrences_in_p43"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_premature_printed_rule(self):
  e=copy.deepcopy(self.e);e["firstparty_prose_scope"]["complete_printed_table_next_section_mechanical_law"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_second_witness(self):
  e=copy.deepcopy(self.e);e["double_page_source_scope"]["physical_source_vote_count_for_both_images"]=2
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_corrupt_source_image_digest(self):
  e=copy.deepcopy(self.e);e["source"]["image_sources"][1]["sha"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_corrupt_roi_hash(self):
  e=copy.deepcopy(self.e);e["original_native_rgb_rois"][3]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_winter_summer_sequence(self):
  e=copy.deepcopy(self.e);e["original_segment_context"]["printed_day_restart"]="八十九日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_forward_only(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13CA CURRENT ACTION later";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="LATER";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="LATER";s["historical_audit"]["current_focus"].append("13CA next")
  l["binding"]["reviewed_state_version"]="LATER";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13CA"
  l["checkpoint_log"].append({"state_version":"LATER","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
