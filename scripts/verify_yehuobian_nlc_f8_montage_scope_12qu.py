#!/usr/bin/env python3
"""12QU: source-bound NLC fascicle8 eight-up visual preview, not textual absence."""
import argparse
import copy
import importlib.util
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
DOC=RS/"MING-DATONG-YEHUOBIAN-12QU-NLC411999003250-F8-87-PAGE-CONTACT-TRIAGE-R1.json"
QL=RS/"MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
QO=RS/"MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QT=ROOT/"scripts/yehuobian_nlc_graded_target_review_queue_12qt.py"
QT_SNAPSHOT=RS/"MING-DATONG-YEHUOBIAN-12QT-NLC411999003250-GRADED-TARGET-REVIEW-QUEUE-R1.json"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def is_sha(s):
    return isinstance(s,str) and re.fullmatch(r"[0-9a-f]{64}",s) is not None

def qt_module():
    spec=importlib.util.spec_from_file_location("tw_12qt_for_12qu",QT)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def verify(data_path=DOC):
    record=load(data_path)
    qt=qt_module()
    old=qt.verify_snapshot()
    qo=load(QO)
    ql=load(QL)
    source=next(x for x in ql["sources"] if x["fascicle"]==8)
    opening=next(x for x in qo["original_juan_openings"] if x["volume"]==15)
    a=record["source"]
    v=record["visual_review"]
    nav=record["original_page_navigation"]
    q=record["queue_reconciliation"]
    if not (
        record["stage"]=="12QE_OPEN" and record["status"]=="SOURCE_SHA_BOUND_EIGHT_UP_PREVIEW_NOT_NATIVE_TARGET_COLLATION"
        and a["holding_id"]=="NLC411999003250_ONE_HOLDING"
        and a["fascicle"]==8 and a["original_work_volume"]==15
        and a["source_pdf_sha256"]==source["source_pdf_sha256"]
        and a["source_pdf_pages"]==source["source_pdf_pages"]==87
        and a["artifact_id"]==source["artifact_id"]==11674711192
        and a["workflow_run_id"]==source["workflow_run"]==38064436808
        and a["source_pdf_rehashed_this_batch"] is False
        and a["ocr_used"] is False and a["image_integrity"]=={
          "original_jpegs_rehashed":87,"contact_sheets_rehashed":11,"hash_mismatches":0}
        and a["artifact_zip_sha256"]=="be1fd1bb2aeb016dea6cf721e9ee72499194a4edbc8989c8906dbd491f550c21"
        and a["artifact_status_json_sha256"]=="9ccaaaafb30829e72feed99b028f76b5f4cb6390e38a339f491c4c2ed9a61cda"
        and a["page_sha_sequence_sha256"]=="b118385f23fbfb4219ea336474ceea3e77ed1864b175d41dbbb87c9b29c1a37f"
        and a["contacts_sha_sequence_sha256"]=="3d4eeee69821e211517a79cf35d21a86a030ae45ffde30e9cb2d2a6873944f3c"
    ):
        raise ValueError("F8_ARTIFACT_SOURCE_OR_DIGEST_CHANGED")
    if not (
        v["visual_method"]=="EIGHT_UP_PREEXISTING_CONTACT_SHEETS_NOT_FULL_SIZE_GLYPH_COLLATION"
        and v["contacts_opened"]==11 and v["pages_in_preview"]==87
        and v["first_page"]==1 and v["last_page"]==87
        and v["contact_sheet_starts"]==[1,9,17,25,33,41,49,57,65,73,81]
        and v["native_pages_opened_for_navigation_only"]==[1,87]
        and v["new_native_target_passage_reviews"]==0
        and v["positive_target_attestation_count"]==0
        and v["page_by_page_full_text_transcription"] is False
        and v["does_not_prove_page_absence"] is True
        and v["does_not_prove_work_absence"] is True
        and nav["opening_label_direct_native_image"]=="萬曆四十年壬子卷十五"
        and nav["p1_source_sha256"]==opening["page_jpeg_sha256"]=="827017f05fda959c727c3bfb7e5a2639c9d66d4f19476fded57dcf0d1044e71e"
        and nav["p87_source_sha256"]=="22e1062cc969a523b14ed3ca290d41fb052088289f6a9d1fc17bc9f3ecd67919"
        and opening["digital_fascicle"]==8 and opening["pdf_page"]==1
        and opening["right_leaf_has_previous_volume"] is False
    ):
        raise ValueError("F8_PREVIEW_GRADE_OR_VOLUME_NAVIGATION_CHANGED")
    if not all(is_sha(a[k]) for k in (
        "source_pdf_sha256","artifact_zip_sha256","artifact_status_json_sha256",
        "page_sha_sequence_sha256","contacts_sha_sequence_sha256"
    )):
        raise ValueError("SOURCE_SHA_SYNTAX_INVALID")
    baseline=qt.build_rows()
    f8=[x for x in baseline if x["fascicle"]==8]
    if len(f8)!=87 or [x["pdf_page"] for x in f8]!=list(range(1,88)):
        raise ValueError("F8_NAVIGATION_COVERAGE_CHANGED")
    if not all(x["target_screen_grade"]=="NOT_TARGET_SCREENED"
               and x["body_search_eligible"]
               and x["requires_native_target_screen"]
               and x["source_pdf_sha256"]==a["source_pdf_sha256"]
               and x["original_volume_candidates"]==[15] for x in f8):
        raise ValueError("F8_PREEXISTING_TARGET_GRADE_NOT_UNSCREENED")
    for x in f8:
        x["target_screen_grade"]="EIGHT_UP_DOWNSAMPLED_TARGET_PREVIEW_ONLY"
        x["target_screen_provenance"]="12QU_F8_CONTACT_1_TO_87"
        x["preview_page_sequence_sha256"]=a["page_sha_sequence_sha256"]
        x["full_resolution_opened_for_navigation_only"]=x["pdf_page"] in (1,87)
        x["requires_native_target_screen"]=True
        x["target_absence_proven"]=False
    new=copy.deepcopy(old)
    new["montage_only_source_pages"]+=87
    new["not_target_screened_source_pages"]-=87
    new["body_not_even_firstpass_screened"]-=87
    new["per_fascicle"]["8"]["fourup_only"]+=87
    if new!=q["expected_new_summary"]:
        raise ValueError("12QU_QUEUE_SUMMARY_DRIFT")
    if not (
        new["source_pages"]==1030 and new["body_pages"]==1027
        and new["native_screened_source_pages"]==29
        and new["montage_only_source_pages"]==177
        and new["not_target_screened_source_pages"]==824
        and new["native_body_review_backlog"]==999
        and new["body_not_even_firstpass_screened"]==822
        and new["body_full_text_collation_backlog"]==1027
        and new["global_target_absence_proven"] is False
        and new["independent_physical_copy_increment"]==0
        and q["old_12qt_preview_pages"]==90
        and q["new_preview_pages"]==87
        and q["native_target_review_backlog_not_reduced"] is True
        and record["historical_adjudication"]["old20_target_folio"]=="UNLOCATED"
        and record["historical_adjudication"]["independent_1827_printing_target"]=="UNVERIFIED"
        and record["historical_adjudication"]["historical_algorithm_reopen"] is False
    ):
        raise ValueError("FALSE_NEGATIVE_OR_RUNTIME_PROMOTION")
    return new

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--summary",action="store_true")
    args=ap.parse_args()
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
