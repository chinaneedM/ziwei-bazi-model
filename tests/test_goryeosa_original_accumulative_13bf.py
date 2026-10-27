import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-original-accumulative-13bf.py"
spec=importlib.util.spec_from_file_location("check13bf",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13BF(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.PC);self.be=m.load(m.PBE);self.bd=m.load(m.PBD);self.yz=m.load(m.PYZ)
  self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def check(self,e=None,ledger=None,state=None):
  return m.check(self.e if e is None else e,self.be,self.bd,self.yz,self.l if ledger is None else ledger,self.s if state is None else state)
 def test_live_source_lanes(self):self.assertTrue(self.check())
 def test_forged_original_cumulative(self):
  x=copy.deepcopy(self.e);x["manuscript_originals"][0]["new_original_roi"][2]["literal"]="六千六百九十五八一三五"
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_wrong_original_source_image_hash(self):
  x=copy.deepcopy(self.e);x["manuscript_originals"][1]["source_JPEG_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_wrong_original_roi(self):
  x=copy.deepcopy(self.e);x["manuscript_originals"][1]["new_original_roi"][0]["bbox"][0]+=1
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_forged_day_shift(self):
  x=copy.deepcopy(self.e);x["bounded_original_local_numeric_equations"][0]["matches_original_long_day"]=15
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_false_historical_header_winner(self):
  x=copy.deepcopy(self.e);x["received_digital_text_index_bridge"]["can_promote_received_row_shift_to_historical_header_definition"]=True
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_new_stemmatic_vote_not_permitted(self):
  x=copy.deepcopy(self.e);x["independent_stemmatic_votes_added"]=2
  with self.assertRaises(AssertionError):self.check(e=x)
 def test_forward_only_future_append(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  item=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  item["source_refs"]+=["docs/research/13BF_FUTURE_SAMPLE.md","docs/research/13BF_FUTURE_SAMPLE.json"]
  s["schema_version"]="1.TEST.FUTURE";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.TEST.FUTURE"
  s["historical_audit"]["current_focus"].append("13BG TEST_ONLY_APPEND")
  l["binding"]["reviewed_state_version"]="1.TEST.FUTURE";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["binding"]["latest_research_focus_prefix"]="13BG"
  l["checkpoint_log"].append({"state_version":"1.TEST.FUTURE","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.check(ledger=l,state=s))
if __name__=="__main__":unittest.main()
