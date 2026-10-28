#!/usr/bin/env python3
"""Exact-decimal counterfactual; NOT a historical original numeric adjudicator."""
from pathlib import Path
from decimal import Decimal
import json
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13JY-G893-GORYEOSA-THREE-ROW-COUNTERFACTUAL-ARITHMETIC-R1.json"
Q=Decimal("0.0000001")
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def differences(case,branch):
 rows={q["limit"]:Decimal(q["value"]) for q in case["received_neighbour_rows"]}
 target=case["target"]
 assert len(rows)==4 and sorted(rows)==[target-2,target-1,target+1,target+2]
 rows[target]=Decimal(case[branch])
 vals=[rows[i] for i in range(target-2,target+3)]
 first=[vals[i+1]-vals[i] for i in range(4)]
 second=[first[i+1]-first[i] for i in range(3)]
 def signstr(d):
  v=d.quantize(Q)
  return ("+" if v>=0 else "")+format(v,".7f")
 return [signstr(x) for x in second]
def verify(e,s,l):
 assert e["schema"]=="TIANWEN-13JY-G893-GORYEOSA-THREE-ROW-COUNTERFACTUAL-ARITHMETIC-R1"
 assert e["method"].startswith("For each row splice")
 assert "MIXED-WITNESS" in e["method"]
 assert e["scope"]=="TABLE_INTERNAL_ARITHMETIC_DIAGNOSTIC_ONLY_NO_HISTORICAL_WINNER"
 assert len(e["cases"])==3
 expected={8:("VAR-NUM-LUNAR-L8-LOSSGAIN","019b","10.561775","10.5601775"),
 124:("VAR-NUM-LUNAR-L124-JI-XINGDU","035b","1.0281","1.0821"),
 132:("VAR-NUM-LUNAR-L132-LOSSGAIN","036b","7.886075","7.88675")}
 for c in e["cases"]:
  i=c["target"];cid,page,gv,rv=expected[i]
  assert (c["id"],c["g893_page"],c["g893_candidate"],c["received_candidate"])==(cid,page,gv,rv)
  assert len(c["g893_original_jpeg_sha256"])==64
  assert differences(c,"g893_candidate")==c["g893_splice_second_differences"]
  assert differences(c,"received_candidate")==c["received_second_differences"]
  assert len(c["received_text_rows"])==5
  assert c["received_text_rows"]==list(range(i-2,i+3))
  if i==132:
   assert c["received_candidate_grade"]=="HYPOTHETICAL_NAIVE_DECIMAL_GLYPH_JOIN_ONLY_NOT_ADJUDICATED_NORMALIZATION"
  else:assert c["received_candidate_grade"].startswith("PREEXISTING_CADAL_DIRECT_FACSIMILE")
 x=e["result"]
 assert all(x[q]==0 for q in ("new_original_target_jpeg_acquired","new_independent_witnesses","original_g893_six_cross_witness_variant_winners_awarded","ancient_received_copy_readings_retracted","source_registry_delta","graph_nodes_delta","graph_edges_delta","algorithm_reopens"))
 assert x["mixed_witness_splice_examples"]==3 and x["product"]=="CLOSED" and x["risk_closed"] is False
 a=s["historical_audit"];b=l["binding"];f=a["current_focus"]
 assert s["schema_version"]==b["reviewed_state_version"]==a["research_omission_guard"]["reviewed_state_version"]
 assert len(f)==b["source_focus_count"] and f[-1].split(" ",1)[0]==b["latest_research_focus_prefix"]
 assert any(q.startswith("13JX ") for q in f) and any(q.startswith("13JY ") for q in f)
 assert a["row_count"]==222 and a["audited_row_count"]==222
 assert a["external_source_registry_total_unique_count"]==763
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 issue=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"]
 assert sum(q.get("revision_id")=="TW-OPEN-0005-13JY-DIFFERENCES-20261029" for q in issue["history"])==1
 assert any(q.get("revision_id")=="TW-OPEN-0005-13JX-FUJIWARA1941-20261029" for q in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert len(l["issues"])==11
 return {"status":"PASS","three_mixed_witness_cases":3,"winners_awarded":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
