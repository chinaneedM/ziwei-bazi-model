#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZL-GORYEOSA-1972-MIXED-FACSIMILE-AND-5553-SUPPLEMENT-CONFLICT-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (P,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def require(ok,msg):
 if not ok:raise ValueError(msg)
def verify(d,state,ledger):
 require(d["schema"]=="TIANWEN-12ZL-GORYEOSA-1972-5553-SOURCE-COMPOSITION-R1","identity")
 e=d["source_evidence"];a=d["adjudication"];o=d["open_originals"]
 require(e["snu"]["kind"].startswith("FIRST_PARTY_BIBLIOGRAPHIC") and e["snu"]["supplement_books"]==[8,26,29] and e["snu"]["heritage_exclusion"]==[8,26,29],"firstparty 5553")
 require(e["heritage_reprint"]["kind"]=="SECONDARY_REPUBLICATION_NOT_DIRECT_FIRSTPARTY" and not e["heritage_reprint"]["original_heritage_full_text_directly_verified"],"do not promote secondary")
 require(e["heritage_reprint"]["book_numbers"]==[8,12,26] and [z["volumes"] for z in e["heritage_reprint"]["volumes_by_book"]]==[[19,20,21],[31,32,33],[73,74]],"secondary book-vs-juan enumeration")
 require(e["academic"]["modern_facsimile_year"]==1972 and e["academic"]["reported_base"]=="奎5554" and e["academic"]["reported_supplements"]=="woodblock recut","mixed facsimile")
 require(e["academic"]["replaced_work_volumes"]==[19,20,21,31,73,74,77,78,79,81,82,83] and not e["academic"]["modern_1972_target_page_acquired"] and not e["academic"]["original_pdf_sha256_bound"],"scholarly-only evidence")
 require(a["snu_books"]==[8,26,29] and a["secondary_books"]==[8,12,26] and a["shared_books"]==[8,26] and a["contested_books"]==[12,29],"source disagreement preserved")
 require(a["secondary_work_volume_count"]==sum(len(z["volumes"]) for z in e["heritage_reprint"]["volumes_by_book"])==8 and a["arithmetic_full139_less_manuscript8"]==131,"conditional arithmetic")
 require(a["same_manuscript_count_not_same_folio_identification"] and a["modern_1972_is_provenance_heterogeneous_from_scholarly_account"] and a["cannot_transfer_1972_edition_to_gk5554_d16_d18"],"scope firewall")
 for k in ("modern_1972_total_work_is_single_original_5554","snu_catalog_wins_without_original_page","reprint_wins_without_original_page"):
  require(a[k] is False,"no false winner "+k)
 for k in ("gk5553_book12_image","gk5553_book29_image","gk5554_work52_book","gk5554_d16_image","gk5554_d18_image","facsimile_1972_work52_page"):
  require(o[k] is None,"no original acquired "+k)
 for k in ("independent_physical_votes","registry_additions","genealogy_additions","algorithm_reopens"):
  require(o[k]==0,"no invented new evidence "+k)
 require((o["open_issues"],o["g893_source"],o["g893_crossoriginal"],o["product"])==(11,"5/6","0/6","CLOSED") and d["transmission_impact"]=="NONE","chart historical boundary")
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 require(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"risk crosswalk")
 f=state["historical_audit"]["current_focus"]
 require(any(z.startswith("12ZL ") for z in f) and len(f)==ledger["binding"]["source_focus_count"] and ledger["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0],"focus sync")
 require(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"version sync")
 require(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]},"all research issues reviewed")
 return {"status":"PASS","open_issues":11,"independent_new_originals":0}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
