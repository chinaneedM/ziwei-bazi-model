import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-d18-d20-13bj.py"
spec=importlib.util.spec_from_file_location("research13bj",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Waseda13BJ(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.P);self.be=m.load(m.PBE);self.bg=m.load(m.PBG)
  self.bh=m.load(m.PBH);self.yz=m.load(m.PYZ)
  self.ledger=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  self.state=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,ledger=None,state=None):
  return m.check(self.e if e is None else e,self.be,self.bg,self.bh,self.yz,self.ledger if ledger is None else ledger,self.state if state is None else state)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_image_sha(self):
  e=copy.deepcopy(self.e);e["source"]["original_jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_heading(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_regions"][1]["original_literal"]="十八日"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_crop(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_regions"][5]["original_rgb_roi_bbox"]=[0,0,1,1]
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_roi_hash(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_regions"][6]["original_rgb_pixel_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fabricated_D20_digit(self):
  e=copy.deepcopy(self.e);e["source_native_rgb_regions"][5]["decimal_value"]="8843.7572"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_long_relation(self):
  e=copy.deepcopy(self.e);e["arithmetic_relations"][1]["original_long_value"]="419.0163"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_source_vote_inflation(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["independent_stemmatic_votes_added"]=1
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_unproved_global_law(self):
  e=copy.deepcopy(self.e);e["scope_firewall"]["whole_table_day_index_law"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_old_action_reintroduced(self):
  l=copy.deepcopy(self.ledger)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BI CURRENT EVIDENCE-BOUND NEXT ACTION"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_unregistered_future_action_rejected(self):
  l=copy.deepcopy(self.ledger)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BL UNREGISTERED ACTION"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_false_stale_action_after_newer_revision(self):
  l=copy.deepcopy(self.ledger)
  next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13BI CURRENT EVIDENCE-BOUND NEXT ACTION (STALE)"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_new_focus_does_not_rewrite_prior_action(self):
  l=copy.deepcopy(self.ledger);s=copy.deepcopy(self.state)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  assert issue["next_action"].startswith("13DA CURRENT ACTION")
  assert l["binding"]["latest_research_focus_prefix"]=="13DB"
  self.assertTrue(self.go(ledger=l,state=s))
 def test_latest_focus_without_action_event_cannot_spoof(self):
  l=copy.deepcopy(self.ledger)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]="13DB CURRENT ACTION spoofed without material scope revision"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_last_action_event_must_authorize_prefix(self):
  l=copy.deepcopy(self.ledger)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]="13DC CURRENT ACTION unregistered"
  with self.assertRaises(AssertionError):self.go(ledger=l)
 def test_future_forward_only(self):
  l=copy.deepcopy(self.ledger);s=copy.deepcopy(self.state)
  issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  issue["next_action"]="13BK CURRENT ACTION future test"
  issue["history"].append({"event":"ISSUE_REVISION","date":"2026-10-21","changed_fields":["next_action"],"reason":"future test","evidence_refs":[m.P]})
  s["schema_version"]="NEXT_VERSION";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT_VERSION"
  s["historical_audit"]["current_focus"].append("13BK NEXT TEST")
  l["binding"]["reviewed_state_version"]="NEXT_VERSION";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13BK"
  l["checkpoint_log"].append({"state_version":"NEXT_VERSION","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(ledger=l,state=s))
if __name__=="__main__":unittest.main()
