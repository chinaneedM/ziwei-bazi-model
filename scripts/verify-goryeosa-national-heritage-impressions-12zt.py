#!/usr/bin/env python3
"""12ZT: official object-level first/later printing classification ≠ ancient folio glyph."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EV="docs/research/TIANWEN-12ZT-GORYEOSA-NATIONAL-HERITAGE-IMPRESSION-GRADE-R1.json"
SH="docs/research/TIANWEN-12ZT-KOREA-HERITAGE-GORYEOSA-SOURCE-SHARD-R1.json"
ST="docs/PROJECT-CURRENT-STATE-R1.json"
LE="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MA="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
PR="docs/research/TIANWEN-12ZS-GORYEOSA-TAEBAEKSAN-GK03539-COMPARATOR-BRIDGE-R1.json"

def load():
    return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in
                 (EV,SH,ST,LE,MA,PR))

def ck(value, reason):
    if not value:
        raise ValueError(reason)

def verify(d, shard, state, ledger, manifest, prior):
    ck(d["schema"]=="TIANWEN-12ZT-GORYEOSA-NATIONAL-HERITAGE-IMPRESSIONS-VS-PLATE-DATE-R1"
       and d["issue_id"]=="TW-OPEN-0005" and d["prior"]==PR, "evidence identity")
    ck(d["source_type"]=="KOREA_HERITAGE_SERVICE_FIRST_PARTY_GOVERNMENT_OBJECT_METADATA_NOT_17C_NATIVE_PAGE",
       "metadata not source image")
    items={x["key"]:x for x in d["heritage_items"]}
    ck(len(items)==3 and len(d["heritage_items"])==3 and set(items)==
       {"KHS_2021_3","KHS_2021_4","KHS_2021_6"}, "three official government heritage records")
    for key in ("KHS_2021_3","KHS_2021_4"):
        x=items[key]
        ck(x["holder"]=="Seoul National University Kyujanggak"
           and x["designation_date"]=="2021-02-17"
           and (x["work_juan_count"],x["physical_book_count"],x["plate_cut_year"])==(139,85,1613)
           and x["material"]=="WOODBLOCK"
           and x["impression_grade"]=="FIRST_IMPRESSION_1613", "SNU official first-impression category")
        ck(x["exact_SNU_item_id"] is None and x["target_52_source_image_sha256"] is None,
           "SNU heritage to item or folio unbound")
    x=items["KHS_2021_6"]
    ck(x["holder"]=="Dong-A University Seokdang Museum"
       and x["designation_date"]=="2021-02-17"
       and (x["work_juan_count"],x["physical_book_count"],x["plate_cut_year"])==(139,75,1613)
       and x["material"]=="WOODBLOCK"
       and x["impression_grade"]=="LATER_IMPRESSION_CENTURY_17_TO_18",
       "Dong-A official 17-18th c later impression")
    ck(x["exact_DongA_item_shelfmark"] is None
       and x["target_52_source_image_sha256"] is None, "Dong-A source folio unbound")
    guard=d["hypotheses_to_preserve"]
    for key in ("same_1613_woodblock_family_possible",
                "different_impression_dates_proven_at_official_catalog_classification_level",
                "printed_again_after_1613_possible",
                "dating_DongA_first_print_1613_from_plate_year_is_incorrect"):
        ck(guard[key] is True, "copy-date evidence kept: "+key)
    for key in ("individual_woodblock_plates_comparison_directly_proven",
                "different_target_D16_D18_digits_due_to_late_wear_proven",
                "first_impression_more_correct_numeric_without_collation_proven",
                "assign_KHS_2021_3_to_GK03539_and_2021_4_to_GK03579_proven"):
        ck(guard[key] is False,"invented target glyph or item mapping: "+key)
    checks=d["cross_checks"]
    ck(checks["snu_catalog_gk03539_1613_taebaeksan"] is True
       and checks["snu_catalog_gk03579_1613_odaesan"] is True
       and checks["heritage_2021_3_vs_2021_4_individual_GK03539_GK03579_mapping_proven"] is False,
       "separate Kyujanggak archive gift from heritage item code")
    ck(prior["bridge"]["current_best_specific_catalog_candidate"]=="GK03539_00"
       and prior["unresolved"]["snu_gk03539_work52_native_sha256"] is None,
       "prior 12ZS catalog scope changed")
    missing=d["unresolved"]
    for field in ("khs2021_3_exact_snu_catalog_item_id","khs2021_4_exact_snu_catalog_item_id",
                  "dongA_physical_item_callnumber","snu_3539_work52_physical_book_number",
                  "snu_3579_work52_physical_book_number","dongA_work52_physical_book_number",
                  "snu_3539_original_work52_page_image_sha256","snu_3579_original_work52_page_image_sha256",
                  "dongA_original_work52_page_image_sha256","each_D16_D18_original_glyph_decision"):
        ck(missing[field] is None, "original target unobserved: "+field)
    for field in ("new_ancient_physical_folio_images","new_original_target_numeric_votes",
                  "new_independent_plate_ancestry_votes","new_genealogy_nodes",
                  "new_genealogy_edges","algorithm_reopens"):
        ck(missing[field]==0,"cannot manufacture physical witness: "+field)
    ck((missing["open_issues"],missing["g893_direct_controls"],
        missing["g893_cross_independent_original"],missing["product"])==
       (11,"5/6","0/6","CLOSED"),"G893 source target stays unresolved")
    ck(shard["schema"]=="TIANWEN-12ZT-GORYEOSA-KHS-FIRST-LATER-IMPRESSION-SOURCE-SHARD-R1"
       and len(shard["sources"])==3
       and all(x["physical_glyph_authority"] is False
               and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY"
               and x["evidence"]==EV for x in shard["sources"]), "official metadata only")
    ck(len(set(x["source_id"] for x in shard["sources"]))==3,"source ids distinct")
    record=[x for x in manifest["shards"] if x["path"]==SH]
    ck(len(record)==1 and record[0]["schema"]==shard["schema"]
       and record[0]["source_count"]==3,"registry shard")
    ck(manifest["root_source_count"]==647
       and manifest["extension_source_count"]>=69
       and manifest["combined_source_count"]==
       manifest["root_source_count"]+manifest["extension_source_count"], "growing source registry")
    audit=state["historical_audit"]
    ck((audit["external_source_registry_root_count"],
        audit["external_source_registry_extension_count"],
        audit["external_source_registry_total_unique_count"])==
       (manifest["root_source_count"],manifest["extension_source_count"],
        manifest["combined_source_count"]), "source manifest and state consistent")
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    ck(issue["status"]=="OPEN"
       and all(p in issue["source_refs"] for p in (EV,EV.replace(".json",".md"),SH)),
       "P0 issue remains open and recorded")
    focus=audit["current_focus"]
    ck(any(x.startswith("12ZT ") for x in focus)
       and ledger["binding"]["source_focus_count"]==len(focus)
       and ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],
       "focus bookkeeping")
    ck(state["schema_version"]==ledger["binding"]["reviewed_state_version"]
       ==audit["research_omission_guard"]["reviewed_state_version"], "state synchrony")
    ck(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
       and {x["id"] for x in ledger["issues"]}==
           set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"]), "all 11 issues re-reviewed")
    ck(audit["row_count"]==audit["audited_row_count"]==222
       and state["invariants"]["algorithm_reopen_count"]==0
       and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED",
       "algorithm does not change")
    return {"status":"PASS","new_official_heritage_metadata_records":3,
            "target_ancient_folio_images":0,"independent_original_glyph_votes":0,
            "open_issues":11}

if __name__=="__main__":
    print(json.dumps(verify(*load()),ensure_ascii=False))
