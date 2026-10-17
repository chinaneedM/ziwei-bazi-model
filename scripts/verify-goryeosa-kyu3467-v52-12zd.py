#!/usr/bin/env python3
"""12ZD first-party bibliographic book6 vol52 locator; no phantomed original page."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZD-GORYEOSA-KYU3467-V52-EULHAE-TARGET-AND-5553-SUPPLEMENT-EXCLUSION-R1.json"
PRIOR="docs/research/TIANWEN-12ZC-GORYEOSA-KYU-COPY-REPLACEMENT-AND-TARGET-FOLIO-PRIORITY-R1.json"
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (DOC,PRIOR,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def need(cond,msg):
 if not cond: raise ValueError(msg)
def verify(d,prior,state,ledger):
 need(d["schema"]=="TIANWEN-12ZD-GORYEOSA-KYU3467-V52-MIXED-COPY-SCOPE-R1","schema")
 need(d["previous_batch"]==PRIOR and prior["named_target"]["volume_number"]==52,"prior target")
 need(d["source"]["role"]=="KYUJANGGAK_FIRST_PARTY_HISTORICAL_BIBLIOGRAPHIC_OVERVIEW_NOT_DIRECT_HISTORICAL_GLYPH" and not d["source"]["original_d16_d18_folio_in_source"],"bibliography not folio")
 a,b,c=d["new_leads"]
 need(a["shelfmark"]=="奎3467" and a["work_volume"]==52 and a["reported_fascicle_number"]==6 and a["reported_fascicle_medium"]=="乙亥字_MOVABLE_TYPE","exact mixed-copy lead")
 need(a["print_year"]=="UNVERIFIED" and a["exact_present_day_item_id"] is None and not a["original_target_folio_bound"],"no invented copy-date/item/image")
 need(b["shelfmark"]=="奎貴5553" and b["target_volume"]==52 and [(x["fascicle"],x["work_volumes"]) for x in b["known_manuscript_replacements"]]==[(8,[19,20,21]),(26,[73,74]),(29,[81,82,83])],"all three first-party supplement ranges")
 need(not b["known_whole_fascicle_replacements_intersect_target"] and b["unknown_local_repair_possible"] and b["physical_target_fascicle_unknown"] and not b["printed_target_glyph_bound"],"no original-glyph promotion")
 need(c["shelfmark"]=="奎貴3539" and c["microfilm_catalog_groups"]==[{"mf":"M/F74-102-5","physical_fascicles":"v.48-60"}] and c["target_work_volume"]==52 and c["target_microfilm_group_identified"] is False,"folio!=fascicle; MF only physical")
 need(d["digital_catalog_scope"]["exact_match_of_fascicle_6_to_split_catalog_item"]=="UNRESOLVED" and d["digital_catalog_scope"]["first_party_records_not_counted_as_four_printing_branches"],"do not forge digital split identity")
 q=d["risk_controls"]
 need(all(q[k] for k in ("work_completion_1451_is_not_print_year","type_name_乙亥字_does_not_date_specific_copy","bibliographic_fascicle_binding_is_not_page_glyph","manuscript_replacement_exclusion_does_not_exclude_local_touchups","catalog_record_split_is_not_independent_edition","all_11_omission_issues_open")),"fences")
 need(q["source_witness_count_new"]==q["named_original_d16_d18_page_new"]==q["algorithm_reopen_count"]==q["genealogy_new_edges"]==0,"no phantom original or reopen")
 need(q["G893_principal_original_controls"]=="5/6" and q["G893_cross_original_decisions"]=="0/6" and q["deterministic_product"]=="CLOSED","prior invariants")
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"durable issue crosswalk")
 need(issue["g893_12zd_kyu3467_targeted_original_folio_lead"][-1]["new_original_images"]==0,"issue no page")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state ledger version")
 focus=state["historical_audit"]["current_focus"]
 need(any(x.startswith("12ZD ") for x in focus),"12ZD committed batch retained")
 need(ledger["binding"]["source_focus_count"]==len(focus) and ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],"latest review scope")
 need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"])==11,"checkpoint all issues")
 need(prior["closure"]["new_physical_page_images_acquired"] is False,"no backward overwrite")
 return {"status":"PASS","new_targeted_mixed_copy_leads":1,"new_original_folios":0,"known_5553_supplement_fascicles":3,"open_recovery_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
