import copy,importlib.util,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/"scripts"/"verify-goryeosa-waseda-folio-seam-13bu.py"
spec=importlib.util.spec_from_file_location("g13bu",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Folio13BU(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.s=m.load(m.S);self.l=m.load(m.L)
  self.p={k:m.load(getattr(m,k)) for k in ("BS","BT","BQ")}
 def go(self,e=None,s=None,l=None,p=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.p if p is None else p)
 def test_positive(self):self.assertTrue(self.go())
 def test_no_promoted_day16(self):
  e=copy.deepcopy(self.e);e["local_original_observation"]["d16_same_heading_isolated_cumulative"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_no_speculative_left_folio_value(self):
  e=copy.deepcopy(self.e);e["local_original_observation"]["d17_side_outer_numeric_candidate_value"]="7570.6624"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_page_count_boundary(self):
  e=copy.deepcopy(self.e);e["bounded_neighbor_pdf_pages_1based"]=[19,20,21,22]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_sha_guard(self):
  e=copy.deepcopy(self.e);e["prior_p23_original_rgb_guard_rois"][0]["rgb_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_no_alteration_to_existing_holding(self):
  e=copy.deepcopy(self.e);e["source"]["known_embedded_jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_no_stemmatic_votes(self):
  e=copy.deepcopy(self.e);e["scope"]["independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_future_append_only(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BV CURRENT ACTION future";issue["history"].append({"event":"ISSUE_REVISION","changed_fields":["next_action"]})
  s["schema_version"]="NEXT";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT";s["historical_audit"]["current_focus"].append("13BV newer")
  l["binding"]["reviewed_state_version"]="NEXT";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BV"
  l["checkpoint_log"].append({"state_version":"NEXT","reviewed_issue_ids":[z["id"] for z in l["issues"]]})
  self.assertTrue(self.go(s=s,l=l))
if __name__=="__main__":unittest.main()
