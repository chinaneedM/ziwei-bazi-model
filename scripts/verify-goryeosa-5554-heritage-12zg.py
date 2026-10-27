#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZG-GORYEOSA-5554-HERITAGE-1482-DATE-BOUNDARY-R1.json"
PREV="docs/research/TIANWEN-12ZF-GORYEOSA-5554-1972-CROSSWALK-R1.json"
def load():
 return tuple(json.loads((R/x).read_text(encoding="utf-8")) for x in (P,PREV,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def verify(d,prev,state,ledger):
 need(d["schema"]=="TIANWEN-12ZG-GORYEOSA-5554-HERITAGE-CATALOG-DATE-FIREWALL-R1" and d["prior"]==PREV,"schema")
 need(prev["official"]["k5554_year"]=="UNVERIFIED","forward original preserved")
 a=d["heritage"];b=d["kyudb"];s=d["secondary"];q=d["constraints"]
 need(a["count_work_volumes"]==98 and a["count_physical_books"]==32 and a["era_label"]=="1482년(성종13)" and a["record_number"]=="2114-2" and a["classification"]=="금속활자본","heritage")
 need(a["source_kind"]=="OFFICIAL_MODERN_CULTURAL_HERITAGE_OBJECT_CLASSIFICATION_NOT_DATED_PRINT_COLOPHON" and not a["direct_original_printing_evidence"],"no original dating")
 need(b["book_cd"]=="GK05554_00" and b["shelfmark"]=="奎貴5554" and b["treasure_no"]=="2114-2" and b["count_physical_books"]==32,"same object scope")
 need(b["impression_year_literal"]=="[刊年未詳]" and b["correlated_heritage_object_by_designation_and_holding"] and not b["heritage_year_supersedes_print_year"],"no illicit time promotion")
 need(s["claimed_original_work_volumes_count"]==105 and s["heritage_98_vs_secondary_105_not_reconciled"] and s["physical_book_no_for_volume52"]=="UNRESOLVED","separate counts")
 need(s["alternative_held_book6_to_book10_work40_52"].startswith("SECONDARY_"),"secondary localization")
 need(q["older_prior_document_immutable"] and q["work_date_1451_not_impression"] and q["modern_heritage_1482_not_original_paper_date"] and q["modern_98_volume_total_not_direct_folio_count"],"date firewall")
 need(q["confirmed_original_5554_d16"] is None and q["confirmed_original_5554_d18"] is None and q["physical_target_original_image"] is None,"no target original")
 need(q["g893_original"]=="5/6" and q["g893_cross_original"]=="0/6" and q["total_open_issues"]==11 and q["product"]=="CLOSED","prior boundaries")
 need(q["algorithm_reopened"]==q["new_historical_source_original_votes"]==q["transmission_new_edges"]==0,"no unproved graph")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"issue evidence")
 f=state["historical_audit"]["current_focus"]
 need(any(x.startswith("12ZG ") for x in f) and ledger["binding"]["source_focus_count"]==len(f) and ledger["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0],"future focus")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"sync")
 need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"])==11,"all issues")
 return {"status":"PASS","era_attribution":"1482_MODERN_HERITAGE","original_impression_date":"UNRESOLVED","original_pages_new":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
