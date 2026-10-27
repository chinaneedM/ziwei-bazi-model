#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZF-GORYEOSA-5554-1972-CROSSWALK-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def need(b,k):
 if not b:raise ValueError(k)
def verify(d,s,l):
 need(d["schema"]=="TIANWEN-12ZF-GORYEOSA-5554-1972-REPRINT-MF-CROSSWALK-R1","schema")
 a=d["official"]; r=d["modern_reprint"]; q=d["outcome"]; w=d["scholarship"]
 need(a["k5554_surviving_books"]==32 and a["k5554_medium"]=="乙亥字" and a["k5554_year"]=="UNVERIFIED","5554")
 need(a["k5553_surviving_books"]==46 and a["k5553_manuscript_books"]==[8,26,29] and a["k5553_treasure_scope_books"]==43,"5553")
 need(a["k5554_mf_field_ids"]==["M/F74-102-17-"+str(i) for i in range(1,8)] and a["k5554_mf_field_cites_other_item"]=="奎 5553" and a["k5553_exact_same_mf_field"] and not a["k5554_film_physically_bound"],"MF other copy")
 need(a["k5554_work52_image"] is None,"source page absent")
 need(w["claimed_5554_work_volumes"]=="卷40—52" and w["source_grade"]=="SECONDARY_NOT_ORIGINAL_LEAF" and w["claimed_5553_third_manuscript_book"]==28 and w["official_5553_third_manuscript_book"]==29,"secondary tension")
 need(r["ncid"]=="BA63617326" and r["parts"]==["上","中","下"] and len(r["institutional_holdings"])==5 and r["vol52_part"] is None and r["vol52_print_origin"] is None and r["modern_copy_holdings_not_independent_historical_witnesses"],"modern facsimile boundary")
 need(all(q[k]==0 for k in ("new_original_image_count","new_independent_historical_source_votes","algorithm_reopens","genealogy_edges_added")) and q["original_d16"] is None and q["original_d18"] is None,"no source promotion")
 need(q["g893_main"]=="5/6" and q["g893_final"]=="0/6" and q["open_recovery_issues"]==11 and q["product"]=="CLOSED","source controls")
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 need(i["status"]=="OPEN" and P in i["source_refs"] and P.replace(".json",".md") in i["source_refs"],"source ledger")
 f=s["historical_audit"]["current_focus"]
 need(any(x.startswith("12ZF ") for x in f) and l["binding"]["source_focus_count"]==len(f) and l["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0],"forward-only batch")
 need(s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state version")
 need(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["checkpoint_log"][-1]["reviewed_issue_ids"])==len(l["issues"])==11,"checkpoint")
 return {"status":"PASS","new_original_pages":0,"reprint_holdings":5}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
