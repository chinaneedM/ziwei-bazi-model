import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-d16-original-long-lane-13be.py"
spec=importlib.util.spec_from_file_location("c13be",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13BE(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.PC);self.bd=m.load(m.PBD);self.ba=m.load(m.PBA);self.ab=m.load(m.PAB);self.yz=m.load(m.PYZ)
  self.ledger=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  self.state=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def run_check(self,changed=None):
  return m.check(changed or self.e,self.bd,self.ba,self.ab,self.yz,self.ledger,self.state)
 def test_real_source_manual_review(self):self.assertTrue(self.run_check())
 def test_fake_original_digit(self):
  x=copy.deepcopy(self.e);x["source_original_image_reviews"][0]["day_rois"][0]["long_original"]="四百二十八六〇七三"
  with self.assertRaises(AssertionError):self.run_check(x)
 def test_fake_original_roi(self):
  x=copy.deepcopy(self.e);x["source_original_image_reviews"][1]["day_rois"][0]["rgb_pixel_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.run_check(x)
 def test_false_cumulative_same_day(self):
  x=copy.deepcopy(self.e);x["adjacent_cumulative_scope"]["can_use_cumulative_for_direct_same_day_arithmetic"]=True
  with self.assertRaises(AssertionError):self.run_check(x)
 def test_false_ancestral_winner(self):
  x=copy.deepcopy(self.e);x["evidence_grading"]["ancestral_winner"]="TWO"
  with self.assertRaises(AssertionError):self.run_check(x)
 def test_false_independent_votes(self):
  x=copy.deepcopy(self.e);x["evidence_grading"]["independent_stemmatic_votes_counted"]=2
  with self.assertRaises(AssertionError):self.run_check(x)
 def test_wrong_implied_short(self):
  x=copy.deepcopy(self.e);x["roman_decimal_bridge"]["long_d16_minus_d17"]="5.1362"
  with self.assertRaises(AssertionError):self.run_check(x)
 def test_future_batch_append_preserves_prior_source_gate(self):
  future_l=copy.deepcopy(self.ledger);future_s=copy.deepcopy(self.state)
  f=next(x for x in future_l["issues"] if x["id"]=="TW-OPEN-0005")
  f["source_refs"].extend(["docs/research/SYNTHETIC_TEST_FUTURE_BATCH.md","docs/research/SYNTHETIC_TEST_FUTURE_BATCH.json"])
  future_s["schema_version"]="TEST_FORWARD_ONLY"
  future_s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="TEST_FORWARD_ONLY"
  future_s["historical_audit"]["current_focus"].append("13BF TEST_ONLY_FOR_APPEND_FORWARD_COMPAT")
  future_l["binding"]["reviewed_state_version"]="TEST_FORWARD_ONLY"
  future_l["binding"]["source_focus_count"]=len(future_s["historical_audit"]["current_focus"])
  future_l["binding"]["latest_research_focus_prefix"]="13BF"
  future_l["checkpoint_log"].append({"state_version":"TEST_FORWARD_ONLY","reviewed_issue_ids":[x["id"] for x in future_l["issues"]]})
  self.assertTrue(m.check(self.e,self.bd,self.ba,self.ab,self.yz,future_l,future_s))
 def test_historical_source_pair_disappearance_rejected(self):
  future_l=copy.deepcopy(self.ledger)
  f=next(x for x in future_l["issues"] if x["id"]=="TW-OPEN-0005")
  f["source_refs"].remove(m.MD)
  with self.assertRaises(AssertionError):m.check(self.e,self.bd,self.ba,self.ab,self.yz,future_l,self.state)
if __name__=="__main__":unittest.main()
