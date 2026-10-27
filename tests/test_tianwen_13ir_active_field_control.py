import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("v13ir",ROOT/"#!/usr/bin/env python3
"""13IR fail-closed active P0 source-field handoff gate."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-13IR-P0-ACTIVE-FIELD-CONTROL-RECONCILIATION-R1.json"
def load(path=DOC):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13IR-P0-ACTIVE-FIELD-CONTROL-RECONCILIATION-R1" and e["issue_id"]=="TW-OPEN-0005"
 ci=e["ci_baseline"]
 assert (ci["workflow_runs"],ci["completed_success"],ci["completed_failure"])==(226,225,1)
 assert ci["failure_line"]=="scripts/verify-ncl03130-d4-chudu-roi-erratum-13ei.py:71"
 controls={x["scope"]:x for x in e["source_controls"]}
 assert len(controls)==7
 for k in ["NLC03130_SOLAR","NLC03130_OLD_SIX_DAY_SOLAR","NLC03130_SUMMER","GK3467_WINTER","G893_SHOUSHI","GK5553_1972_EVIDENCE"]:
  assert controls[k]["value"] is None and controls[k]["status"].startswith("OPEN")
 assert controls["NLC03130_SOLAR_13EI"]["status"]=="RETRACTED" and controls["NLC03130_SOLAR_13EI"]["value"] is None
 assert all(e["file_policy"][k] is False for k in ("original_journal_pdf_bytes_obtained","catalog_claims_promoted_to_original","historical_13in_source_rewritten"))
 assert e["file_policy"]["source_images_added"]==0 and e["file_policy"]["rolling_action_restored_historical_keywords_for_living_gaps_only"] is True
 if with_state:
  s=load("docs/PROJECT-CURRENT-STATE-R1.json");ld=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
  assert tuple(map(int,s["schema_version"].split(".")))>=(1,897,0)
  assert s["schema_version"]==ld["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
  assert ld["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
  assert ld["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
  assert any(t.startswith("13IR ") for t in s["historical_audit"]["current_focus"])
  issue=next(x for x in ld["issues"] if x["id"]=="TW-OPEN-0005")
  action=issue["next_action"]
  assert action.startswith("13IR CURRENT ACTION:")
  for scope,control in controls.items():
   for token in control["labels"]:
    assert token in action,(scope,token)
  assert re.search(r"(?<![A-Za-z0-9])(?:D1-D6|D1\\s+D2\\s+D3\\s+D4\\s+D5\\s+D6)(?![A-Za-z0-9])",action)
  assert "NLC03130 solar D30" in action and "NLC03130 summer D14" in action
  assert "13EI" in action and "RETRACTED" in action and "NULL" in action
  assert issue["status"]=="OPEN" and DOC in issue["source_refs"]
  assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13IR-") for h in issue["history"])
  assert len(ld["issues"])==11 and ld["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load())
 print("TIANWEN_13IR_ACTIVE_SOURCE_FIELD_HANDOFF_PASS")
")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Evidence(unittest.TestCase):
 def test_current_active_controls(self):self.assertTrue(m.check(m.load()))
 def test_solar_d30_remains_null(self):
  d=copy.deepcopy(m.load());d["source_controls"][0]["value"]=13
  with self.assertRaises(AssertionError):m.check(d,False)
 def test_preserve_13ei_retraction(self):
  d=copy.deepcopy(m.load());d["source_controls"][2]["status"]="RESOLVED"
  with self.assertRaises(AssertionError):m.check(d,False)
 def test_no_new_historic_source(self):
  d=copy.deepcopy(m.load());d["file_policy"]["source_images_added"]=1
  with self.assertRaises(AssertionError):m.check(d,False)
if __name__=="__main__":unittest.main()
