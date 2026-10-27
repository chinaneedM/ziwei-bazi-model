#!/usr/bin/env python3
"""12ZS museum 85-book source-scoped catalog crosswalk, not native D16/D18 text."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-12ZS-GORYEOSA-TAEBAEKSAN-GK03539-COMPARATOR-BRIDGE-R1.json"
S="docs/research/TIANWEN-12ZS-KCI2017-TAEBAEKSAN-SOURCE-SHARD-R1.json"
P="docs/research/TIANWEN-12ZR-GORYEOSA-DONGA-SNU-PLATE-FAMILY-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(p):return json.loads((R/p).read_text(encoding="utf-8"))
def load():return tuple(get(p) for p in (E,S,P,MAN,STATE,LEDGER))
def check(x,msg):
 if not x:raise ValueError(msg)
def verify(d,shard,prior,manifest,state,ledger):
 check(d["schema"]=="TIANWEN-12ZS-GORYEOSA-TAEBAEKSAN-85BOOK-CATALOG-BRIDGE-R1" and d["prior"]==P,"scope")
 k=d["kci2017"]
 check((k["kci_id"],k["doi"],k["year"],k["pages"])==("ART002287557","10.17842/jsa.2017..69.53",2017,"53-85"),"article identity")
 check(k["same_author_as_2012_and_2014"] is True and k["independent_scholar_votes_across_three_papers"]==1,"scholar dependency")
 check("Taebaeksan" in k["comparison_description"] and k["article_grade"].endswith("NOT_VOL52_SOURCE_IMAGE"),"KCI Taebaek only")
 snu=d["snu"];ta=snu["taebaeksan"];oda=snu["odaesan"]
 check(snu["group_contains_two_85book_woodblock_items"] is True and ta["books"]==oda["books"]==85,"two distinct 85 sets")
 check((ta["catalog_id"],ta["call_number"],ta["medium"])==("GK03539_00","奎貴3539","木版本"),"Taebaeksan firstparty item")
 check((oda["catalog_id"],oda["call_number"],oda["archive_name"])==("GK03579_00","奎貴3579","五臺山史庫"),"Odaesan distinct item")
 check("太白山史庫上" in ta["copy_library_stamp"] and "萬曆四十一年" in ta["copy_library_stamp"],"dated named gift note")
 check(ta["microfilm_for_physical_books_48_60"]=="M/F74-102-5","physical microfilm scope")
 check(ta["exact_book_containing_work52"] is None and ta["source_target_work52_image_sha256"] is None
       and oda["source_target_work52_image_sha256"] is None,"no direct target image")
 bridge=d["bridge"]
 check(bridge["current_best_specific_catalog_candidate"]=="GK03539_00" and
       bridge["bridge_grade"]=="HIGH_CONFIDENCE_CATALOG_LEVEL_LOCATOR_NOT_DIRECT_PAPER_OBJECT_COMPARISON","catalog candidate only")
 for name in ("previous_12zr_snu85_exact_id_was_unresolved","microfilm_volume_range_not_work_juan_mapping",
              "original_1613_gift_stamp_not_numeric_table_reading","physical_set_comparison_not_confirmed_vol52_same_plate_by_us",
              "no_stemmatic_duplicate_votes","no_direct_digit_claim"):
  check(bridge[name] is True,name)
 check(bridge["article_explicitly_provided_gk03539_number"] is False,"do not forge paper item number")
 u=d["unresolved"]
 for name in ("kci2017_actual_matched_leaf_object_id","snu_gk03539_work52_physical_book_number",
              "snu_gk03539_work52_native_sha256","snu_gk03579_work52_native_sha256",
              "donga_work52_native_sha256","same_plate_52_direct_matched_fingerprint_sha256"):
  check(u[name] is None,"no ancient original "+name)
 for name in ("new_physical_original_vol52_folios","new_ancient_d16_d18_values",
              "new_ancestral_woodblock_votes","new_genealogy_edges","algorithm_reopens"):
  check(u[name]==0,"no unearned source vote "+name)
 check((u["open_issues"],u["g893_direct_source_controls"],u["g893_cross_original_decisions"],u["chart_product"])
       ==(11,"5/6","0/6","CLOSED"),"freeze historic findings")
 check(prior["scope"]["woodblock_85book_comparator_exact_SNU_ID"] is None,"12ZR snapshot frozen")
 check(len(shard["sources"])==1 and shard["sources"][0]["source_id"]=="EXT-TIANWEN-12ZS-KCI-KIM2017-TAEBAEKSAN-GORYEOSA-85BOOKS"
       and shard["sources"][0]["physical_glyph_authority"] is False and
       shard["sources"][0]["verification_status"]=="RECEIVED_TEXT_VERIFIED","shard not source glyph")
 specs=[x for x in manifest["shards"] if x["path"]==S]
 check(len(specs)==1 and specs[0]["source_count"]==1,"manifest shard exact")
 check(manifest["root_source_count"]==647 and manifest["extension_source_count"]>=66
       and manifest["combined_source_count"]==manifest["root_source_count"]+manifest["extension_source_count"],"source growth")
 h=state["historical_audit"]
 check((h["external_source_registry_root_count"],h["external_source_registry_extension_count"],h["external_source_registry_total_unique_count"])
       ==(manifest["root_source_count"],manifest["extension_source_count"],manifest["combined_source_count"]),"state manifest")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in (E,E.replace(".json",".md"),S)),"open issue linkage")
 focus=h["current_focus"]
 check(any(x.startswith("12ZS ") for x in focus) and ledger["binding"]["source_focus_count"]==len(focus)
       and ledger["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0],"focus live")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"continuity")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11,"open reviewed")
 check(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
       and state["invariants"]["algorithm_reopen_count"]==0,"no runtime")
 return {"status":"PASS","firstparty_catalog_locator":"GK03539_00","new_source_witnesses":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
