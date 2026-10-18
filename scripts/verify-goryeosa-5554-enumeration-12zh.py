#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZH-GORYEOSA-5554-98V105-ENUMERATION-AND-V52-BOOK-BOUNDARY-R1.json"
PREV="docs/research/TIANWEN-12ZG-GORYEOSA-5554-HERITAGE-1482-DATE-BOUNDARY-R1.json"
def load():
 return tuple(json.loads((R/x).read_text(encoding="utf-8")) for x in (P,PREV,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def expand(ranges):
 ret=set()
 for pair in ranges:
  need(isinstance(pair,list) and len(pair)==2 and all(type(x)==int for x in pair) and 1<=pair[0]<=pair[1]<=137,"invalid range")
  ret.update(range(pair[0],pair[1]+1))
 return ret
def verify(d,prev,state,ledger):
 need(d["schema"]=="TIANWEN-12ZH-GORYEOSA-5554-CATALOG-ENUMERATION-COUNT-FIREWALL-R1" and d["prior"]==PREV,"schema or prior")
 need(prev["constraints"]["physical_target_original_image"] is None and prev["constraints"]["confirmed_original_5554_d16"] is None,"preserve prior")
 p=d["physical_object"]; need(p["kyudb_book_cd"]=="GK05554_00" and p["impression_year"]=="[刊年未詳]" and p["physical_books"]==32,"physical")
 c=d["citations"]; need(c["official_heritage"]["declared_work_volume_count"]==98 and c["official_claim_republication"]["declared_work_volume_count"]==98 and c["scholarly_review"]["declared_work_volume_count"]==105,"declared counts")
 need(c["official_claim_republication"]["grade"].startswith("THIRD_PARTY_") and c["scholarly_review"]["grade"].startswith("SECONDARY_") and c["official_kyudb"]["explicit_work_52_to_physical_book"] is None,"source scopes")
 e=d["received_enumerations"]; a=e["republished_heritage"];b=e["secondary_scholarly"];sa=expand(a["numbered_work_volume_ranges"]);sb=expand(b["numbered_work_volume_ranges"])
 need(len(sa)==a["computed_distinct_numbered_work_volumes"]==95 and len(sb)==b["computed_distinct_numbered_work_volumes"]==100,"replay enumerations")
 need((sa^sb)==set((30,31,32,33,34)) and (sb-sa)==set((30,31,32,33,34)),"local range discrepancy")
 need(a["published_total"]==98 and b["published_total"]==105 and a["total_minus_enumeration"]==3 and b["total_minus_enumeration"]==5,"unexplained residuals")
 dd=e["differences"];need(dd["range_29_35_minus_separate_29_and_35"]==[30,31,32,33,34] and dd["published_totals_difference"]==7 and dd["numbered_enumerations_difference"]==5,"difference distinction")
 q=d["scope"];need(52 in sa and 52 in sb and q["v52_present_in_both_received_enumerations"] and q["work_volume_52_candidate_physical_books"]==[6,7,8,9,10] and q["exact_v52_physical_book"]=="UNRESOLVED","v52 localization")
 need(q["prefatory_material_converted_to_work_volume_count"].startswith("UNRESOLVED") and q["original_5554_v52_d16_printed_glyph"] is None and q["original_5554_v52_d18_printed_glyph"] is None and q["original_5554_v52_source_page_digest"] is None,"no phantom original")
 need(q["g893_principal_original_controls"]=="5/6" and q["g893_cross_original_decisions"]=="0/6" and q["product"]=="CLOSED" and q["open_issues"]==11,"product")
 need(all(q[k]==0 for k in ("source_registry_additions","physical_witness_votes_added","transmission_edges_added","algorithm_reopens")),"no invented witness")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"issue evidence")
 f=state["historical_audit"]["current_focus"]
 need(any(z.startswith("12ZH ") for z in f) and f[-1].startswith("12ZH ") and ledger["binding"]["latest_research_focus_prefix"]=="12ZH" and ledger["binding"]["source_focus_count"]==len(f),"state/ledger focus")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"version sync")
 need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]},"reviewed issues")
 return {"status":"PASS","enumerated_heritage":95,"enumerated_scholar":100,"new_original_images":0}
if __name__=="__main__": print(json.dumps(verify(*load()),ensure_ascii=False))
