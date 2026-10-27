import importlib.util,copy,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-waseda-goryeosa-two-day-13z.py"
spec=importlib.util.spec_from_file_location("waseda13z",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class WasedaTwoDaySource(unittest.TestCase):
 def test_exact_decimal_and_source_scope(self): self.assertTrue(m.check(m.read()))
 def test_no_unwitnessed_correction_of_d16_original(self):
  d=copy.deepcopy(m.read());d["short_original"][0]["original_glyph"]="五分二三六二"
  with self.assertRaises(AssertionError):m.check(d)
 def test_residual_not_zeroed_out(self):
  d=copy.deepcopy(m.read());d["two_day_replays"][0]["decrement_minus_short_sum"]="0.0000"
  with self.assertRaises(AssertionError):m.check(d)
 def test_no_final_source_vote(self):
  d=copy.deepcopy(m.read());d["conclusions"]["final_independent_physical_numeric_votes_added"]=1
  with self.assertRaises(AssertionError):m.check(d)
 def test_cumulative_folio_remains_unbound(self):
  d=copy.deepcopy(m.read());d["conclusions"]["waseda_d18_yingsuoji_cumulative_original_folio"]=23
  with self.assertRaises(AssertionError):m.check(d)
 def test_next_checkpoint_does_not_break_historical_13z(self):
  from unittest.mock import patch
  e=m.read();orig=m.read
  st=copy.deepcopy(orig("docs/PROJECT-CURRENT-STATE-R1.json"))
  le=copy.deepcopy(orig("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
  st["schema_version"]="1.687.0";st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.687.0"
  st["historical_audit"]["current_focus"].append("13AB SIMULATED NEXT RESEARCH FOCUS")
  le["binding"]["reviewed_state_version"]="1.687.0"
  le["binding"]["latest_research_focus_prefix"]="13AB"
  le["binding"]["source_focus_count"]=len(st["historical_audit"]["current_focus"])
  le["checkpoint_log"].append({"id":"SIMULATED_FUTURE_REVIEW","state_version":"1.687.0"})
  def get(path=m.E):
   if path=="docs/PROJECT-CURRENT-STATE-R1.json":return st
   if path=="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json":return le
   return orig(path)
  with patch.object(m,"read",side_effect=get):self.assertTrue(m.check(e))
if __name__=="__main__":unittest.main()
