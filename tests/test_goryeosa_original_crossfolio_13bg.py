import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-original-crossfolio-13bg.py"
spec=importlib.util.spec_from_file_location("research13bg",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CrossFolio13BG(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.PC);self.be=m.load(m.PBE);self.bf=m.load(m.PBF);self.yz=m.load(m.PYZ)
  self.l=m.load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json");self.s=m.load("docs/PROJECT-CURRENT-STATE-R1.json")
 def go(self,e=None,ledger=None,state=None):
  return m.check(self.e if e is None else e,self.be,self.bf,self.yz,self.l if ledger is None else ledger,self.s if state is None else state)
 def test_positive(self):self.assertTrue(self.go())
 def test_wrong_original_canvas18_sha(self):
  e=copy.deepcopy(self.e);e["source_canvases"][2]["source_jpeg_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_original_roi(self):
  e=copy.deepcopy(self.e);e["source_canvases"][2]["new_day_slots"][1]["original_rgb_pixel_sha256"]="0"*64
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_fake_digit(self):
  e=copy.deepcopy(self.e);e["source_canvases"][2]["new_day_slots"][0]["literal"]="八千〇〇〇二六九六"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_folio_gap(self):
  e=copy.deepcopy(self.e);e["source_canvases"][2]["canvas_1based"]=20
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_wrong_predecessor_long(self):
  e=copy.deepcopy(self.e);e["crossfolio_original_decimal_relations"][0]["matches_original_long_day"]=17
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_ancestry_or_global_law(self):
  e=copy.deepcopy(self.e);e["historical_earliest_D16_one_vs_two"]="TWO"
  with self.assertRaises(AssertionError):self.go(e=e)
  e=copy.deepcopy(self.e);e["full_day_index_convention"]="PROVEN"
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_false_stemmatic_votes(self):
  e=copy.deepcopy(self.e);e["scope_counters"]["independent_stemmatic_votes_added"]=2
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_future_append_safe(self):
  l=copy.deepcopy(self.l);s=copy.deepcopy(self.s)
  z=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
  z["source_refs"].extend(["docs/research/FUTURE_TEST.md","docs/research/FUTURE_TEST.json"])
  s["schema_version"]="TEST_FUTURE_APPEND";s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="TEST_FUTURE_APPEND"
  s["historical_audit"]["current_focus"].append("13BH FUTURE_ONLY_TEST")
  l["binding"]["reviewed_state_version"]="TEST_FUTURE_APPEND";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["binding"]["latest_research_focus_prefix"]="13BH"
  l["checkpoint_log"].append({"state_version":"TEST_FUTURE_APPEND","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(self.go(ledger=l,state=s))
if __name__=="__main__":unittest.main()
