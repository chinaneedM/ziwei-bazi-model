#!/usr/bin/env python3
"""12ZW first-party indexed Yonsei composite copy and print chronology firewall."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12ZW-YONSEI-CHOI-SEAL-BOOK30-MANUSCRIPT-PRINT-GRADE-R1.json"
PRIOR="docs/research/TIANWEN-12ZV-GORYEOSA-YONSEI-33BOOK-LATER-IMPRESSION-BOUNDARY-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
MANIFEST="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
SHARD="docs/research/TIANWEN-12ZV-GORYEOSA-YONSEI-HERITAGE-SOURCE-SHARD-R1.json"
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def need(ok,why):
    if not ok: raise ValueError(why)
def verify():
    doc,prior,state,ledger,manifest,shard=map(load,(DOC,PRIOR,STATE,LEDGER,MANIFEST,SHARD))
    need(doc["schema"]=="TIANWEN-12ZW-YONSEI-GORYEOSA-33BOOK-OWNER-SEAL-MIXED-COPY-GRADE-R1" and doc["prior"]==PRIOR,"identity/prior")
    need(doc["new_source_registry_entries"]==0 and doc["original_source_id"]==shard["sources"][0]["source_id"],"source no duplication")
    need(shard["sources"][0]["verification_status"]=="ACCESS_BOUNDARY_UNVERIFIED" and shard["sources"][0]["physical_glyph_authority"] is False,"old unverified source grade retained")
    b=doc["physical"]; p=prior["new_physical_copy_candidate"]
    need(b["heritage_record"]==p["heritage_record"] and b["physical_book_total"]==p["physical_books"]==33 and b["printed_work_volume_total"]==p["work_volumes"]==139,"existing copy preserved")
    need((b["plate_year"],b["official_printing_class"])==(1613,"17_TO_18C_LATER_IMPRESSION"),"printing grade")
    need(all(b[k] is None for k in ("specific_item_shelfmark","work52_physical_book_number","work52_target_original_image_sha256")),"no fabricated work52 target")
    seal=doc["later_owner_seal"]
    need(seal["catalog_quoted_seal"]=="崔漢綺藏" and seal["photo_or_stamp_sha256"] is None,"catalog-not-pixel stamp")
    need(seal["proof_of_1613_or_17c_impression_date"] is False and seal["proof_of_textual_lineage"] is False,"seal source firewall")
    comp=doc["explicit_book_level_composite"]
    need(comp["physical_book_number"]==30 and comp["work_volumes"]==[122,123],"direct named book/volumes")
    need(comp["catalog_class"]=="LATER_HANDWRITTEN_SUPPLEMENT_PAGES_IN_OTHERWISE_WOODBLOCK_RECORDED_SET","manuscript scope")
    need(all(comp[k] is None for k in ("original_book30_page_sha256","original_manuscript_folio_sha256","hand_copy_date")),"no original supplement page")
    need(all(comp[k] is False for k in ("ordinary_woodblock_numeric_vote_for_122_123","work52_same_book_30","work52_printed_status_verified","work52_d16_d18_numeric_glyphs_read")),"no false printed status")
    grade=doc["impression_scope"]
    need(grade["inference"]=="POSSIBILITY_YONSEI_IMPRESSION_APPROX_SNU_ARCHIVAL_PRINTING_TIME" and grade["competing_official_catalog_label"]==b["official_printing_class"],"retained print-year tension")
    need(grade["adjudication"]=="KEEP_CATALOG_PRINT_GRADE_AND_FRAME_TIME_SUGGESTION_SIDE_BY_SIDE_UNRESOLVED","do not choose print year from frame")
    need(all(grade[k] is True for k in ("frame_size_equal_does_not_establish_same_printing_year","same_frame_size_does_not_establish_same_physical_copy","same_frame_size_does_not_establish_independent_plate_ancestor")),"ancestry firewall")
    need(grade["dated_edition_colophon_seen"] is False and grade["woodblock_frame_comparison_reported"]["direct_original_frame_measurement_this_session"] is False,"index-not-measurement")
    t=doc["target_intake_status"]
    need(t["new_original_target_folio_images"]==t["new_original_numeric_votes"]==t["genealogy_new_edges"]==t["chart_algorithm_reopens"]==0,"zero original and reopen")
    need(t["G893_principal_direct_controls"]=="5/6" and t["G893_cross_copy_controls"]=="0/6" and t["omission_issues_open"]==11 and t["source_registry_total"]==717,"unresolved controls")
    audit=state["historical_audit"]
    need(audit["external_source_registry_total_unique_count"]==manifest["combined_source_count"]==717,"no false new source")
    need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==audit["research_omission_guard"]["reviewed_state_version"],"state consistency")
    need(any(x.startswith("12ZW ") for x in audit["current_focus"]) and ledger["binding"]["latest_research_focus_prefix"]==audit["current_focus"][-1].split(" ",1)[0] and ledger["binding"]["source_focus_count"]==len(audit["current_focus"]),"focus forward")
    issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
    need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"P0 never closed")
    need(len(ledger["issues"])==11 and all(i["status"]!="RESOLVED_WITH_EVIDENCE" for i in ledger["issues"]),"11 issue preservation")
    need(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={i["id"] for i in ledger["issues"]},"checkpoint")
    need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"deterministic product protected")
    return {"status":"PASS","catalog_composite_manuscript_work_volumes":2,"new_original_glyph_votes":0,"registry_total":717}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False))
