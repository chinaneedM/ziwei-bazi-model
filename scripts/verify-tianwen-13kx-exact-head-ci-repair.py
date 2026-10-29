#!/usr/bin/env python3
"""13KX: exact-HEAD CI regression fixes without altering historical source data."""
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KX-EXACT-HEAD-CI-REPAIR-ROLLING-ISSUE-PREFIX-AND-UNIT-TYPE-R1.json"
V="docs/research/TIANWEN-13KV-MINGSHI-V35-THIRTEEN-SYNODIC-REM-RUBRIC-RECEIVED-VARIANTS-R1.json"
W="docs/research/TIANWEN-13KW-MINGSHI-V35-13KU-SOURCE-ATTRIBUTION-FORWARD-ERRATUM-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def ck(p,msg):
 if not p:raise ValueError(msg)
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,V,W,S,L))
def verify(e,v,w,state,ledger):
 ck(e["schema"]=="TIANWEN-13KX-EXACT-HEAD-CI-REPAIR-ROLLING-ISSUE-PREFIX-AND-UNIT-TYPE-R1" and e["issue_id"]=="TW-OPEN-0005","identity")
 ck(e["failed_exact_head"]=="b4e43d12cc013301b86dac95852762e707704b1c","failed HEAD")
 a=v["exact_arithmetic"]; m=F(a["source_succeeding_moon_base_units"]);c=F(a["period_divisor_units"]);days=F(a["daily_base_units"])
 ck(m==F(29530593,100) and c==600000 and days==10000,"source units")
 r13=13*m-(13*m//c)*c
 difference=F(a["siku_received_leap_remainder"])-r13
 ck(r13==F("238977.09") and difference==50000 and difference/days==5,"fraction result")
 d=e["defects"]
 ck(len(d)==2 and d[0]["kind"]=="SOURCE_TYPED_SCALAR_COMPARISON_IN_VERIFIER" and d[1]["kind"]=="ISSUE_LATEST_ACTION_PREFIX_CONTRACT","defect identity")
 ck(d[0]["value_in_13kv_json"]==a["daily_base_units"]=="10000" and d[0]["actual_type"]=="str" and d[0]["fix"]=="F(a['daily_base_units'])==10000","not weakened unit type gate")
 ck(d[0]["negative_test"]=="9999 must still reject" and d[1]["new_prefix"]=="13KX CURRENT ACTION:","must retain strict gates")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 ck(issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(binding["latest_research_focus_prefix"]+" CURRENT ACTION:"),"rolling issue")
 ck(w["transition"]=="FORWARD_ONLY_SOURCE_ATTRIBUTION_ERRATUM_NO_PREVIOUS_EVIDENCE_REWRITE","preserve 13KW erratum")
 b=e["preserved_boundaries"]
 for k in ("no_change_to_13kv_original_source_json","no_change_to_13kw_erratum_evidence","no_change_to_historic_numeric_variant_readings","prior_error_reproduced_in_exact_head_ci"):
  ck(b[k] is True,"historical evidence not rewritten "+k)
 for k in ("independent_physical_witnesses_added","historical_g893_six_numeric_winners","algorithm_reopens"):
  ck(b[k]==0,"historic vote and chart invariant "+k)
 ck(b["source_13_lunation_remainder"]==str(r13) and F(b["siku_received_lunation_variant"])==F(a["siku_received_leap_remainder"]) and F(b["unit_delta"])==difference and F(b["unit_delta_in_days"])==5,"rational summary")
 ck(b["chart"]=="CLOSED" and b["open_issues"]==11 and e["counts"]==dict(root=647,extension=118,total=765,matrix=222,graph_nodes=252,graph_edges=238),"scope")
 h=state["historical_audit"];binding=ledger["binding"];i=state["invariants"]
 ck(state["schema_version"]==h["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"],"version sync")
 ck(any(z.startswith("13KX ") for z in h["current_focus"]) and binding["latest_research_focus_prefix"]==h["current_focus"][-1].split(" ")[0] and binding["source_focus_count"]==len(h["current_focus"]),"current focus")
 ck(i["deterministic_fusion_chart_product_r1"]=="CLOSED" and i["algorithm_reopen_count"]==0 and h["row_count"]==222 and h["external_source_registry_total_unique_count"]==765,"unchanged counters")
 ck(E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"] and any(x.get("revision_id")=="TW-OPEN-0005-13KX-CI-GATE-REPAIR-20261030" and E in x.get("evidence_refs",[]) for x in issue["history"]),"append only issue event")
 ck(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"checkpoint")
 return {"status":"PASS","original_13kv_value_type":"str","verified_exact_daily_unit":str(days),"month13_remainder":str(r13),"delta":str(difference),"reopens":0}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
