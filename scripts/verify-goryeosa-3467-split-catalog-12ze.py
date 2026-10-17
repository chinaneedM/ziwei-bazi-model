#!/usr/bin/env python3
"""12ZE exact Kyujanggak child-item catalog vs original-page boundary."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZE-GORYEOSA-KYU3467-SPLIT-CATALOG-AND-MF-EXACT-RECORD-CROSSWALK-R1.json"
PREV="docs/research/TIANWEN-12ZD-GORYEOSA-KYU3467-V52-EULHAE-TARGET-AND-5553-SUPPLEMENT-EXCLUSION-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,PREV,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def req(v,msg):
 if not v:raise ValueError(msg)
def verify(d,previous,state,ledger):
 req(d["schema"]=="TIANWEN-12ZE-GORYEOSA-KYU3467-SPLIT-CATALOG-AND-MICROFILM-LOCATOR-R1","schema")
 req(d["prior_batch"]==PREV and previous["new_leads"][0]["reported_fascicle_number"]==6 and previous["new_leads"][0]["work_volume"]==52,"prior v52")
 req(d["sources"]["scholarly_overview_book6"].startswith("奎3467 第6冊=高麗史 卷52"),"exact target")
 types={"奎3467의1":"木版本","奎3467의2":"乙亥字","奎3467의3-v.12":"筆寫本","奎3467의4":"乙亥字"}
 by={x["shelfmark"]:x for x in d["record_groups"]}
 req(len(by)==len(d["record_groups"])==4 and {k:v["catalog_medium"] for k,v in by.items()}==types,"four split types")
 a,b=by["奎3467의2"],by["奎3467의4"]
 req(a["exact_book_cd"]=="GK03467_02" and b["exact_book_cd"]=="GK03467_04","exact verified item IDs")
 req(a["surviving_physical_book_count"]==5 and b["surviving_physical_book_count"]==1 and a["individual_mixed_physical_book_note"]=="第9冊(1冊)木板本","partial and mixed print")
 req(a["physical_fascicle_book6_link"]==b["physical_fascicle_book6_link"]=="UNRESOLVED","book6 mapping not proven")
 req(all(x["target_volume52_folio_proven"] is False for x in by.values()),"no invented target folio")
 req(all(by[k]["exact_book_cd"]=="NOT_VERIFIED" for k in ("奎3467의1","奎3467의3-v.12")),"unverified exact item ids")
 src=d["sources"]
 req(src["verified_detail_urls"]==["https://kyudb.snu.ac.kr/book/view.do?book_cd=GK03467_02","https://kyudb.snu.ac.kr/book/view.do?book_cd=GK03467_04"],"source detail matches")
 req(d["same_edition_menu"]["source_emitted_similar_edition_shelfmarks"]==["奎3467의4","奎貴5553-v.1-46","奎貴5554","奎5874의2"],"same edition menu literal")
 m=d["physical_metadata"]
 req(m["microfilm_catalog_literals"]==["M/F82-16-206-1","M/F82-166-206-2"] and m["microfilm_digit_inconsistency_retained_raw"] and m["microfilm_locator_same_on_02_and_04"],"retain as printed MF")
 req(m["individual_microfilm_to_fascicle6_mapping"]=="UNRESOLVED" and m["source_emitted_target_image_url"] is None and m["source_emitted_target_image_sha256"] is None and all(z is None for z in m["directly_collated_target_glyphs"].values()),"no direct image")
 req(m["physical_year_authenticated"] is None and m["common_catalog_print_year"]=="[刊年未詳]","year firewall")
 k=d["scope"]
 req(k["candidate_child_records"]==["GK03467_02","GK03467_04"] and k["candidate_set_status"].startswith("PROVISIONAL"),"candidate not proof")
 req(all(k[z] is False for z in ("prove_book6_is_02","prove_book6_is_04","prove_book6_is_1613","prove_mf_206_1_or_206_2_contains_book6")),"binding firewall")
 req(k["existing_CADAL_original_independent_of_3467"]=="UNKNOWN_COPY_IDENTITY" and k["no_categorical_original_scan_absence_claim"],"surrogate firewall")
 req(k["source_registry_new_physical_witnesses"]==k["genealogy_new_independent_ancestry_edges"]==k["algorithm_reopens"]==0 and k["research_issues_open"]==11,"no invented source/algorithm")
 req(k["g893_source_original_control"]=="5/6" and k["g893_cross_original_decisions"]=="0/6" and k["chart_product_status"]=="CLOSED","R1 remains closed")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 req(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue cross-reference")
 req(issue["g893_12ze_exact_child_item_and_mf_scope"][-1]["new_original_images"]==0,"checkpoint no original")
 req(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state version")
 req(ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]) and ledger["binding"]["latest_research_focus_prefix"]=="12ZE","latest focus review")
 req(state["historical_audit"]["current_focus"][-1].startswith("12ZE "),"new source focus")
 req(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(ledger["issues"])==11,"review all 11")
 req(previous["risk_controls"]["named_original_d16_d18_page_new"]==0,"prior invariant")
 return {"status":"PASS","exact_item_records_verified":2,"split_catalog_groups":4,"original_glyph_pages":0,"unresolved_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
