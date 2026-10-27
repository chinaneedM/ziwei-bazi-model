#!/usr/bin/env python3
"""12ZU official designation-number crosswalk, excluding common microfilm aliases."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZU-GORYEOSA-HERITAGE-GK-ID-AND-SHARED-MICROFILM-R1.json"
PRIOR="docs/research/TIANWEN-12ZT-GORYEOSA-NATIONAL-HERITAGE-IMPRESSION-GRADE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load():
    return tuple(json.loads((ROOT/f).read_text(encoding="utf-8")) for f in (P,PRIOR,STATE,LEDGER))
def ck(test,msg):
    if not test:raise ValueError(msg)
def verify(d,prior,state,ledger):
    ck(d["schema"]=="TIANWEN-12ZU-HERITAGE-GK03539-GK03579-DIRECT-DESIGNATION-CROSSWALK-R1"
       and d["issue"]=="TW-OPEN-0005" and d["prior"]==PRIOR,"identity")
    a,b=d["items"]
    ck(len(d["items"])==2 and (a["heritage_record"],b["heritage_record"])==
       ("고려사(2021-3)","고려사(2021-4)"),"heritage objects")
    for x,gk,treasure,archive,heritage in (
       (a,"GK03539_00","2115-1","太白山史庫","1121121150100"),
       (b,"GK03579_00","2115-2","五臺山史庫","1121121150200")):
        ck(x["snu_catalog_code"]==gk and x["old_treasure_number"]==
           x["snu_old_treasure_number"]==treasure and x["heritage_code"]==heritage,
           "no swapped heritage number or firstparty SNU item code")
        ck(x["heritage_code"] in x["heritage_url"] and gk in x["snu_url"] and
           x["archive"]==archive and x["physical_books"]==85 and
           x["grade"]=="1613_FIRST_IMPRESSION","physical copy identity")
        ck(x["work52_folio_sha256"] is None,"heritage id not target image")
    old=prior["heritage_items"]
    ck([r["key"] for r in old][:2]==["KHS_2021_3","KHS_2021_4"] and
       all(x["exact_SNU_item_id"] is None for x in old[:2]),
       "do not rewrite prior 12ZT historical snapshot")
    f=d["source_issued_bibliography"]
    ck(f["gk03579_item_microfilm_page_lists_physical_book_numbers_of"]=="奎3539" and
       f["m_f74_102_5_explicit_scope"]=="奎3539/v.48-60","catalog MF actual printed id")
    ck(all(f[k] is False for k in
       ("m_f74_102_5_proven_work_juan52_target",
        "gk03579_own_independent_microfilm_source_proven",
        "gk03539_work52_original_page_retrieved",
        "gk03579_work52_original_page_retrieved")),"no fake independent original scan")
    lim=d["limits"]
    ck(all(lim[k] is True for k in (
       "KHS_2021_3_to_GK03539_source_catalog_ID_proven",
       "KHS_2021_4_to_GK03579_source_catalog_ID_proven",
       "exact_heritage_item_to_snu_item_crosswalk_is_source_number_not_native_page",
       "shared_3539_microfilm_list_must_not_count_as_3579_original_scan",
       "same_1613_first_impression_not_necessarily_distinct_block_ancestors",
       "same_treasure_number_crossref_not_numeric_glyph_proof",
       "ancient_source_original_work52_d16_d18_images_missing")),"limited identity claim")
    u=d["unresolved"]
    for k in ("gk03539_vol52_physical_book_number",
              "gk03579_vol52_physical_book_number",
              "gk03539_original_52_target_image_sha256",
              "gk03579_original_52_target_image_sha256",
              "dongA_original_52_target_image_sha256"):
        ck(u[k] is None,"no physical target")
    ck(all(u[k]==0 for k in (
       "new_native_original_pages","new_ancient_d16_d18_numeric_votes",
       "new_source_registry_entries","new_genealogy_edges","algorithm_reopens")),"no false votes")
    ck((u["open_issues"],u["g893_source_controls"],u["g893_cross_original"],
        u["product"])==(11,"5/6","0/6","CLOSED"),"P0 unresolved")
    iss=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    ck(iss["status"]=="OPEN" and P in iss["source_refs"] and P.replace(".json",".md") in
       iss["source_refs"],"open researched source")
    focus=state["historical_audit"]["current_focus"]
    ck(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==
       state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],
       "continuity")
    ck(any(x.startswith("12ZU ") for x in focus) and
       ledger["binding"]["source_focus_count"]==len(focus) and
       ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],
       "research focus")
    ck(state["historical_audit"]["external_source_registry_total_unique_count"]>=716
       and state["historical_audit"]["external_source_registry_root_count"]==647,
       "existing registry preserved")
    ck(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and
       state["invariants"]["algorithm_reopen_count"]==0 and
       len(ledger["issues"])==11 and
       set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==
       {x["id"] for x in ledger["issues"]} and
       ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],
       "open coverage")
    return {"status":"PASS","KHS_SNU_exact_item_crosswalks":2,
            "independent_target_original_images":0,"new_registry_sources":0}
if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
