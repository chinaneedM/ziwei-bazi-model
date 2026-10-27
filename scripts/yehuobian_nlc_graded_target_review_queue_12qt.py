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
    # 12QT forward-only full-CI repair: these are the twenty SHA256 digests
    # already recorded by 12QR, NOT freshly fetched source images. Prevent
    # syntactically valid but falsified QR page image digests from passing.
    qr_image_sha_pins=["7d8a5c0f761a152f75bc0b7b5e9db0dd27fe2106cbd13bee30e78bfe2d14dfe3","233f9a5c17f41469ddef6650c906f608cabb6c3dd2f662ac46ff3a9d1ef5be9e","5d551e454e166a5cf812a0f79ae1a7f485072296c4bbc3d2d7467affda66047e","fc1ac6db27972fa13ebc6763a31bf9292a3fab6746bfd8c661fa7bbee5c3d153","fdc24763efd9128cbd80e4e16a3fd48304f7593b2f59282d078ff03025d4e719","3977935d391ca0317eef9de89c6b370bcc77edda59b38d771c6f2ab313a22b8f","f785a420eb6ca4a8a712da5d34998fbe10d35dff6f3da9af3068add35145531f","6c4fbea4c3d80a14f96fed054f8e9c1420b35b4c9293c5a2cd5f4213b89a8237","dd10411756b2d54c70d599007bd1c5da079dfe75738ceb678fa10a2194b15a7e","21013ae9f460cba1e2557df0e18758b90c5cac5b19ac6e0d60d9a97b4fee4243","7bb790b45f5657d353c8e642ca9213314f460fb34748b772042279d55e62cd36","00358c8805e39bd1cc2b47ad330e6fb09abb83bf520483ae735c420d655f8e66","45496a1feab4271d32342e8f4da45288c24b34dbf15060f018150269a947ba2e","98575c2ada4e35834f0782067b2c6c39c9676886c10200ccbc787e968c8843e1","f81a17efc392a6febf4ea40aa28b9c54c58f26fdd59b164cc44fcf120ceb7880","cf77617608ef196f49f4be67ea50c99f74294d42b81f1e54330d3d7d0c4736d3","318612d7b581e6def0a67b7f106e17ec4782e9dcbce4ead84e5f5d798d5d2c65","84a98e6d37a8a5d81b59914a47695f5b91a6266d7dcc6531cd04e164a50ef008","d9ad87c77c350ca9fe9d3865ef6eed866da45c1c9550c17ce34ba1b3db49c18e","2b9630e525fc8784610efa94382d6ed16886a5e219d7dd1c797dc4f988a5f318"]
    for x in qr_pages:
        r=index[7,x["pdf_page"]]
        h=x["source_derived_page_jpeg_sha256"]
        if not (x["fascicle"]==7 and sha(h) and h==qr_image_sha_pins[x["pdf_page"]-1]
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
