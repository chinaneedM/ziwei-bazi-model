#!/usr/bin/env python3
"""12WF first-party metadata receipt remains distinct from target physical folio."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WF-SBB1827-ACTUAL-FIRSTPARTY-METADATA-AND-NLC-CENSUS-ROUTE-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def require(ok,msg):
    if not ok:raise ValueError(msg)
def validate(rec,state):
    require(rec["schema"]=="TIANWEN-12WF-SBB1827-ACTUAL-OFFICIAL-MANIFEST-METS-AND-WENZHOU-CENSUS-ROUTE-R1","schema")
    b=rec["berlin"]
    require((b["probe_workflow_run_id"],b["probe_workflow_job_id"],b["probe_capture_artifact_id"])==(38719445780,116370105907,11964437520),"source run receipt")
    require(b["probe_head_sha"]=="21be104c3e2f05c4a22ecd8699a24bf241931760" and b["probe_conclusion"]=="success","exact successful run")
    require(b["github_reported_artifact_zip_sha256"]=="f5997e162fd821621fdba6a137fc46dd6402d03fee8eeb1f52b1791499b7d1a1","zip archive SHA report")
    require(b["artifact_zip_independently_redownloaded_and_rehashed"] is False,"do not claim independent artifact fetch")
    require(b["source_issued_digital_object_ppn"]=="PPN334378186X","source-issued object identifier")
    x,y=b["actual_manifest"],b["actual_mets"]
    require(x["http_status"]==200 and x["bytes"]==69638 and x["canvas_count"]==38,"actual IIIF measurement")
    require(x["source_sha256"]=="db26dd7d790c66faddc46ce542354396a30a1bb1bba70b9be011e6d57db27b82","manifest source SHA")
    require(y["http_status"]==200 and y["bytes"]==73209 and y["source_sha256"]=="c30688453d2c9540be407805b9c41d88ffc4e716d0bcb8dd0fdea9349c2cb9d8","actual METS source")
    require(x["explicit_juan20_range_labels_found"]==0 and y["explicit_juan20_div_labels_found"]==0,"unconfirmed juan20 index")
    require(x["all_38_pages_manually_examined"] is False and x["canvas_count_is_not_page_count_of_entire_historical_set"] is True,"preview vs complete-book scope")
    require(all(b[k] is True for k in ("no_source_issued_article_heading_or_original_target_page_bound","no_1827_paper_impression_verified","no_1869_revised_paper_impression_verified","no_new_direct_historical_print_glyphs","no_ocr_used","source_issued_original_page_urls_not_guessed")),"historical authority firewall")
    w=rec["wenzhou"]
    require(w["official_national_census_database"]=="https://gjpc.nlc.cn/xlsworkbench/publish","official census route")
    require(w["database_search_for_this_specific_wenzhou_title_completed"] is False and w["absence_of_catalogue_item_not_inferred_from_timeout"] is True,"no false item search result")
    require(w["wenzhou_2017_catalogue_book_ncid"]=="BB26066854","modern catalogue book ID")
    require([z["id"] for z in w["wenzhou_2017_catalogue_modern_book_barcodes"]]==["200038400503","200038400512"],"2017 catalogue book physical catalog")
    require(w["catalogue_2017_copy_is_not_original_1827_yehuobian"] is True and w["catalogue_2017_copy_is_not_original_1869_yehuobian"] is True,"modern reference book not Qing original")
    require(w["wenzhou_specific_yehuobian_census_number"] is None and w["wenzhou_specific_yehuobian_callnumber"] is None and w["external_requests_sent"]==0,"original census title item unbound")
    s=rec["summary"]
    require(s["new_ancient_leaf_images"]==0 and s["new_independent_historical_print_votes"]==0 and s["new_registry_entries"]==0,"no added original votes")
    require(s["union_sources"]<=state["historical_audit"]["external_source_registry_total_unique_count"] and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","project stable")
    require(rec["transmission_impact"]["edges_supported"]==[],"no invented lineage edge")
    return {"status":"PASS","actual_firstparty_metadata_objects":2,"canvas_count_scoped_to_sample":38,"original_1827_1869_print_votes":0}
def verify():
    return validate(json.loads((ROOT/REC).read_text()),json.loads((ROOT/STATE).read_text()))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
