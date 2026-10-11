#!/usr/bin/env python3
"""12QV: verify bounded 141-page f9 contact preview without inventing absence."""
import copy
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
QV=RS/"MING-DATONG-YEHUOBIAN-12QV-NLC411999003250-F9-141-PAGE-CONTACT-TRIAGE-R1.json"
QL=RS/"MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
QO=RS/"MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QU=ROOT/"scripts/verify_yehuobian_nlc_f8_montage_scope_12qu.py"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def qu_module():
    spec=importlib.util.spec_from_file_location("nlc12qu_for_12qv",QU)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def verify(path=QV):
    item=load(path)
    qu=qu_module()
    previous=qu.verify()
    src=item["source"]
    v=item["manual_review"]
    nav=item["navigation"]
    past=load(QL)
    old=load(QO)
    f9=next(r for r in past["sources"] if r["fascicle"]==9)
    volumes={x["volume"]:x for x in old["original_juan_openings"]}
    if not (item["stage"]=="12QE_OPEN"
        and item["status"]=="87_UPSTREAM_F8_PLUS_141_F9_EIGHT_UP_PREVIEW_NO_NATIVE_TARGET_COLLATION"
        and src["holding"]=="NLC411999003250_ONE_HOLDING"
        and src["fascicle"]==9 and src["pages"]==141
        and src["volume_candidates"]==[16,17]
        and src["source_pdf_sha256"]==f9["source_pdf_sha256"]
        and src["pdf_binary_rehashed_this_round"] is False
        and src["artifact_id"]==f9["artifact_id"]==11674711170
        and src["workflow_run_id"]==f9["workflow_run"]==38064436808
        and src["artifact_zip_sha256"]=="6275b3521155ffcc869f2e6f8d25666650c48ef47d70a1259e17f5b0ed2bc3bd"
        and src["status_json_sha256"]=="171c92906270426228b6d395bbca80dd8ba34d6e4ca21923f0951ebea80f41c9"
        and src["page_sha_chain"]=="0b1f1df616301c576f937ffd336a513e6e87a0869d314f425890456e211828d5"
        and src["contact_sha_chain"]=="09fb9e9213ea6549c2d3af208b83738bf408071eb186f8c054a28a0232d06cdf"
        and src["source_jpeg_count"]==141 and src["contact_sheet_count"]==18
        and src["hash_mismatches"]==0 and src["ocr_used"] is False
        and src["hash_chain_encoding"].startswith("sha256(lowercase ASCII concatenation")
    ):
        raise ValueError("F9_SOURCE_IDENTITY_OR_HASH_PIN_DRIFT")
    if not (
        v["all_contact_sheets_visually_opened"]==18
        and v["page_start"]==1 and v["page_end"]==141
        and v["contact_sheet_starts"]==list(range(1,142,8))
        and v["grade"]=="EIGHT_UP_DOWNSAMPLED_PREVIEW"
        and v["native_images_opened_for_navigation_only"]==[1,84,141]
        and v["new_native_target_collations"]==0
        and v["positive_target_glyph_attestations"]==0
        and v["full_text_collated"] is False
        and v["absence_on_any_page_proven"] is False
        and v["absence_in_entire_work_proven"] is False
        and nav["f9_p1_original16_heading"]=="萬曆肆拾壹年癸丑卷十六"
        and nav["f9_p84_original17_heading"]=="萬曆肆拾貳年甲寅卷十七"
        and nav["p1_jpeg_sha256"]==volumes[16]["page_jpeg_sha256"]
        and nav["p84_jpeg_sha256"]==volumes[17]["page_jpeg_sha256"]
        and nav["p141_jpeg_sha256"]=="3eb529038b3e3d294ddb7495b6285846e1c28f21c192c9e3ea705db41917c60d"
        and nav["p84_right_leaf_original_volume"]==16
        and nav["p84_left_leaf_original_volume"]==17
        and volumes[16]["digital_fascicle"]==volumes[17]["digital_fascicle"]==9
        and volumes[16]["pdf_page"]==1 and volumes[17]["pdf_page"]==84
        and volumes[17]["right_leaf_has_previous_volume"] is True
    ):
        raise ValueError("F9_REVIEW_GRADE_OR_ORIGINAL_VOLUME_MIXED_LEAF_DRIFT")
    qt=qu.qt_module()
    oldrows=qt.build_rows()
    f9rows=[r for r in oldrows if r["fascicle"]==9]
    if len(f9rows)!=141 or [r["pdf_page"] for r in f9rows]!=list(range(1,142)):
        raise ValueError("F9_NAVIGATION_PAGE_COUNT_CHANGED")
    for r in f9rows:
        p=r["pdf_page"]
        expected=[16] if p<84 else ([16,17] if p==84 else [17])
        if not (r["original_volume_candidates"]==expected
            and r["source_pdf_sha256"]==src["source_pdf_sha256"]
            and r["body_search_eligible"] and r["requires_native_target_screen"]
            and r["target_screen_grade"]=="NOT_TARGET_SCREENED"):
            raise ValueError("F9_PAGE_SCOPE_NOT_AS_AT_PREVIEW")
    summary=copy.deepcopy(previous)
    summary["montage_only_source_pages"]+=141
    summary["not_target_screened_source_pages"]-=141
    summary["body_not_even_firstpass_screened"]-=141
    summary["per_fascicle"]["9"]["fourup_only"]+=141
    if not (
        summary["source_pages"]==1030
        and summary["body_pages"]==1027
        and summary["native_screened_source_pages"]==29
        and summary["montage_only_source_pages"]==318
        and summary["not_target_screened_source_pages"]==683
        and summary["native_body_review_backlog"]==999
        and summary["body_not_even_firstpass_screened"]==681
        and summary["body_full_text_collation_backlog"]==1027
        and summary["global_target_absence_proven"] is False
        and summary["independent_physical_copy_increment"]==0
        and summary["per_fascicle"]["9"]["fourup_only"]==141
        and summary["per_fascicle"]["9"]["native_body_backlog"]==141
        and item["queue_after"]["preview_only_pages"]==318
        and item["queue_after"]["body_not_firstpass_screened"]==681
        and item["queue_after"]["native_body_target_review_backlog"]==999
        and item["invariants"]["product"]=="CLOSED"
        and item["invariants"]["algorithm_reopens"]==0):
        raise ValueError("F9_QUEUE_OR_RUNTIME_AUTHORITY_PROMOTION")
    return summary

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
