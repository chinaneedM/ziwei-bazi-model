#!/usr/bin/env python3
"""12QT graded NLC old20 review queue: images screened != text absent."""
import argparse
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
QR=RS/"MING-DATONG-YEHUOBIAN-12QR-NLC411999003250-F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS-R1.json"
QS=RS/"MING-DATONG-YEHUOBIAN-12QS-NLC411999003250-F7-REMAINING90-MONTAGE-TRIAGE-R1.json"
SNAP=RS/"MING-DATONG-YEHUOBIAN-12QT-NLC411999003250-GRADED-TARGET-REVIEW-QUEUE-R1.json"

def module(path, name):
    spec=importlib.util.spec_from_file_location(name, ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def sha(value):
    return isinstance(value,str) and re.fullmatch("[0-9a-f]{64}",value) is not None

def build_rows(qr_path=QR,qs_path=QS):
    qq=module("scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py","tw_12qq_for_12qt")
    qsv=module("scripts/verify_yehuobian_nlc_f7_montage_scope_12qs.py","tw_12qs_for_12qt")
    qsv.verify_scope(qs_path)
    qr,qs=load(qr_path),load(qs_path)
    base=qq.build_rows()
    if len(base)!=1030 or qq.summary(base)["remaining_target_body_review_queue"]!=1019:
        raise ValueError("UPSTREAM_SOURCE_UNIVERSE_DRIFT")
    index={(r["fascicle"],r["pdf_page"]):dict(r) for r in base}
    if len(index)!=1030:
        raise ValueError("DUPLICATE_SOURCE_PAGE")
    source=qr["source"]
    if not (source["holding_id"]=="NLC411999003250_ONE_HOLDING"
        and source["digital_fascicle"]==7 and source["source_page_count"]==110
        and source["source_pdf_sha256"]==index[7,1]["source_pdf_sha256"]==qs["source"]["source_pdf_sha256"]
        and source["artifact_id"]==qs["source"]["original_artifact_id"]
        and source["artifact_zip_sha256"]==qs["source"]["artifact_zip_sha256"]
        and source["artifact_status_sha256"]==qs["source"]["artifact_status_json_sha256"]
        and source["artifact_members_verified"]=={"page_jpegs":110,"contact_sheets":14,"hash_mismatches":0}
        and qr["review"]["mode"]=="DIRECT_MANUAL_FULL_SOURCE_PAGE_VISUAL_SCREEN_NO_OCR_NO_FULL_TEXT_TRANSCRIPTION"
        and qr["review"]["first_pdf_page"]==1 and qr["review"]["last_pdf_page"]==20
        and qr["queue_reconciliation"]["remaining_unscreened_body_candidate_pages"]==999):
        raise ValueError("12QR_SOURCE_SCOPE_DRIFT")
    for row in index.values():
        old=row["target_review_status"]=="PRIOR_NINE_PAGE_BOUNDED_CHECK"
        row.update(target_screen_grade=("NATIVE_BOUNDED_HEADING_PASSAGE_SCREEN" if old else "NOT_TARGET_SCREENED"),
                   target_screen_provenance=("12QE_BOUNDED_REVIEW" if old else None),
                   target_image_sha256=(row["page_jpeg_sha256_if_known"] if old else None),
                   preview_sequence_sha256=None,
                   full_resolution_opened_for_navigation_only=False,
                   target_absence_proven=False,
                   fully_transcribed=False)
    qr_pages=qr["review"]["screened_pdf_pages"]
    if len(qr_pages)!=20 or [x["pdf_page"] for x in qr_pages]!=list(range(1,21)):
        raise ValueError("12QR_EXPECTED_TWENTY_NATIVE_PAGES")
    for x in qr_pages:
        r=index[7,x["pdf_page"]]
        h=x["source_derived_page_jpeg_sha256"]
        if not (x["fascicle"]==7 and sha(h)
                and x["original_volume_candidates"]==r["original_volume_candidates"]
                and x["review_mode"]=="DIRECT_MANUAL_FULL_PAGE_SCREEN"
                and x["target_status"]=="NO_POSITIVE_TARGET_ATTESTATION_IN_THIS_SCREEN"
                and x["proof_target_absent_on_page"] is False
                and r["target_screen_grade"]=="NOT_TARGET_SCREENED"
                and (r["page_jpeg_sha256_if_known"] is None or r["page_jpeg_sha256_if_known"]==h)):
            raise ValueError("12QR_SOURCE_PAGE_DRIFT")
        r["target_screen_grade"]="NATIVE_FULL_PAGE_VISUAL_TARGET_SCREEN"
        r["target_screen_provenance"]="12QR_F7_P1_TO_20"
        r["target_image_sha256"]=h
    chain=qs["review_scope"]["page_sequence_hash_sha256"]
    anchors=qs["review_scope"]["original_full_image_anchor_sha256"]
    if not sha(chain) or set(anchors)!={"48","68","110"}:
        raise ValueError("12QS_SOURCE_CHAIN_OR_ANCHORS_CHANGED")
    for p in range(21,111):
        r=index[7,p]
        if r["target_screen_grade"]!="NOT_TARGET_SCREENED":
            raise ValueError("OVERLAPPING_PREVIEW_AND_NATIVE_TARGET_REVIEW")
        r["target_screen_grade"]="FOURUP_DOWNSAMPLED_TARGET_PREVIEW_ONLY"
        r["target_screen_provenance"]="12QS_F7_P21_TO_110"
        r["preview_sequence_sha256"]=chain
        if str(p) in anchors:
            h=anchors[str(p)]
            if not sha(h) or (r["page_jpeg_sha256_if_known"] is not None and r["page_jpeg_sha256_if_known"]!=h):
                raise ValueError("12QS_NAVIGATION_GLYPH_ANCHOR_DRIFT")
            r["full_resolution_opened_for_navigation_only"]=True
            r["target_image_sha256"]=h
    rows=[index[r["fascicle"],r["pdf_page"]] for r in base]
    for r in rows:
        native=r["target_screen_grade"].startswith("NATIVE_")
        r["requires_native_target_screen"]=r["body_search_eligible"] and not native
        r["requires_full_text_collation"]=r["body_search_eligible"]
        if r["target_absence_proven"] or r["fully_transcribed"]:
            raise ValueError("UNAUTHORIZED_TEXTUAL_PROOF_PROMOTION")
    out=summary(rows)
    required=(1030,1027,29,90,911,999,909,1027)
    actual=tuple(out[x] for x in (
        "source_pages","body_pages","native_screened_source_pages","montage_only_source_pages",
        "not_target_screened_source_pages","native_body_review_backlog",
        "body_not_even_firstpass_screened","body_full_text_collation_backlog"))
    if actual!=required:
        raise ValueError("GRADED_QUEUE_COUNT_DRIFT")
    return rows

def summary(rows):
    c=Counter(r["target_screen_grade"] for r in rows)
    count=lambda fn:sum(1 for r in rows if fn(r))
    per={}
    for f in range(1,11):
        subset=[r for r in rows if r["fascicle"]==f]
        per[str(f)]={
            "pages":len(subset),
            "native_screens":sum(r["target_screen_grade"].startswith("NATIVE_") for r in subset),
            "fourup_only":sum(r["target_screen_grade"]=="FOURUP_DOWNSAMPLED_TARGET_PREVIEW_ONLY" for r in subset),
            "native_body_backlog":sum(r["requires_native_target_screen"] for r in subset)}
    return {
        "source_pages":len(rows),
        "body_pages":count(lambda r:r["body_search_eligible"]),
        "native_screened_source_pages":c["NATIVE_BOUNDED_HEADING_PASSAGE_SCREEN"]+c["NATIVE_FULL_PAGE_VISUAL_TARGET_SCREEN"],
        "montage_only_source_pages":c["FOURUP_DOWNSAMPLED_TARGET_PREVIEW_ONLY"],
        "not_target_screened_source_pages":c["NOT_TARGET_SCREENED"],
        "native_body_review_backlog":count(lambda r:r["requires_native_target_screen"]),
        "body_not_even_firstpass_screened":count(lambda r:r["body_search_eligible"] and r["target_screen_grade"]=="NOT_TARGET_SCREENED"),
        "body_full_text_collation_backlog":count(lambda r:r["requires_full_text_collation"]),
        "manuscript_target_folio":"UNLOCATED",
        "global_target_absence_proven":False,
        "independent_physical_copy_increment":0,
        "per_fascicle":per}

def verify_snapshot():
    data=load(SNAP)
    result=summary(build_rows())
    if data["summary"]!=result or data["policy"]!="MONTAGE_PREVIEW_IS_NOT_NATIVE_TEXT_ATTESTATION":
        raise ValueError("12QT_SNAPSHOT_OR_GRADE_POLICY_DRIFT")
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary",action="store_true")
    parser.add_argument("--fascicle",type=int)
    parser.add_argument("--page",type=int)
    parser.add_argument("--native-queue",action="store_true")
    parser.add_argument("--limit",type=int,default=25)
    args=parser.parse_args()
    if args.fascicle is not None and not 1<=args.fascicle<=10:parser.error("UNKNOWN_FASCICLE")
    if args.page is not None and args.fascicle is None:parser.error("PAGE_REQUIRES_FASCICLE")
    if not 1<=args.limit<=1030:parser.error("INVALID_LIMIT")
    rows=build_rows()
    if args.summary or (args.fascicle is None and not args.native_queue):
        output=summary(rows)
    else:
        pages=[r for r in rows if (args.fascicle is None or r["fascicle"]==args.fascicle)
               and (args.page is None or r["pdf_page"]==args.page)
               and (not args.native_queue or r["requires_native_target_screen"])]
        output={"authority":"REVIEW_NAVIGATION_NOT_TEXTUAL_NEGATIVE","pages":pages[:args.limit]}
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
