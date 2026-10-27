#!/usr/bin/env python3
"""12YP source-typed v3/v4 arithmetic; reject pseudo-original or G893 lane promotion."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YP-MEI-V3-V4-RECEIVED-MECHANICS-AND-PRINT-SOURCE-FIREWALL-R1.json"
def read():
 return tuple(json.loads((ROOT/f).read_text(encoding="utf-8")) for f in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def check(b,msg):
 if not b: raise ValueError(msg)
def verify(doc,ledger,state):
 check(doc["grade"]=="NEW_RECEIVED_TEXT_CROSS_JUAN_FIELD_DISAMBIGUATION_NOT_DIRECT_SCANNED_ORIGINAL" and doc["prior_12yo_original_glyphs"]==0,"wrong evidence grade")
 idx={r["source"]:r for r in doc["source_presentations"]}
 check(idx["MEI_V3_WENLINSHE"]["grade"]=="ONLINE_RECEIVED_TEXT" and idx["MEI_V4_WIKISOURCE"]["grade"]=="ONLINE_RECEIVED_TEXT","web text cannot become original")
 check(idx["MEI_1971_CINII_REPRINT"]["bibliographic_id"]=="BA60875595" and idx["MEI_1971_CINII_REPRINT"]["original_17TH_18TH_print"] is False and idx["MEI_1971_CINII_REPRINT"]["scan_available"] is False,"1971 reprint cannot be authorial original")
 val={c["id"]:Decimal(c["decimal"]) for c in doc["controls"]}
 check(len(val)==6 and val["V3_LICHA"]==Decimal("0.0031") and val["V3_MUL6"]==val["V4_MUL6_CROSSCHECK"]==val["V4_DAILY_DIFF"]==Decimal("0.0186") and val["V3_PINGLI"]==Decimal("4.9386") and val["V3_PINGCHA"]==Decimal("2.4600"),"received field wrong")
 check(val["V3_LICHA"]*6==val["V3_MUL6"] and 2*val["V3_PINGCHA"]+val["V3_MUL6"]==val["V3_PINGLI"] and (Decimal("6.5568")-val["V3_PINGLI"])/87==val["V4_DAILY_DIFF"],"v3/v4 arithmetic must stay scoped")
 check(len(doc["rule_relationships"])==4 and all(q["historical_shared_physical_copy_proven"] is False for q in doc["rule_relationships"]),"no copying or original equation vote")
 p=doc["original_print_impact"]
 check(all(p[x]==0 for x in ("mei_original_page_readings","new_source_registry_records","new_physical_witness_votes","new_stemmatic_roots","new_genealogy_nodes","new_genealogy_edges","new_algorithm_reopens")),"printed-original firewall")
 flags=doc["invariants"]
 check(flags["open_research_issues"]==11 and flags["g893_original_principal_fields"]=="5/6" and flags["g893_cross_witness_final"]=="0/6" and flags["product"]=="CLOSED","never close G893 or reopen product")
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"] and issue["mei_12yp_v3_v4_received_mechanism_reviews"][0]["original_mei_print_loci_verified"]==0,"unresolved original locus not crossbound")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,630,0),"state sync")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"]),"ledger not reviewed")
 check(any(f.startswith("12YP ") for f in state["historical_audit"]["current_focus"]) and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"research scope gate")
 return {"status":"PASS","received_numerical_roles":6,"original_Mei_printed_target_readings":0,"G893_original_fields":"5/6","research_omissions":len(ledger["issues"])}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
