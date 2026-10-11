#!/usr/bin/env python3
"""12SA NLC original F6 p41-80 exact-source JPEG digest windows, grade and authority gate."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SA-NLC411999003250-F6-P41-80-ORIGINAL-SOURCE-BOUNDED-REVIEW-R1.json"
RY = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RY-NLC411999003250-F6-P1-20-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
RZ = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RZ-NLC411999003250-F6-P21-40-ORIGINAL-SOURCE-BOUNDED-REVIEW-R1.json"
QW = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE-R1.json"
PDF_SHA = "9949f3c736d75f1772c306455f6bead7e744675b66283a415e7c50f4dc4f1c62"
ZIP_SHA = "934d5c16493275c8fb0742abe8764d424bc4a2b2c5f02e99c5bcaab249a7d023"
STATUS_SHA = "895597abefeac14f6f9c6c3b5a0bb41a8c1114d4250a17773e3e0e52bfc0d9e3"
FULL116 = "4998d749bb522d60cd7df499f5aefded8afb4e952111b4b3f2dff85d04573828"
SHA41_60 = "bd3122688b330f630b774aeb05239cae67fab9da75d5f48daa1533b0cb5444e7"
SHA61_80 = "c9150f3bac22a1538431f43a57f7d1fcdc0793e8a24374081d8c829fc52898c8"
SHA1_80 = "517a2607b7e3c2bd171e6ba0966805232a3d10ed5d9df4f6ed89e0833b98d42b"

def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(xs): return hashlib.sha256("".join(xs).encode("ascii")).hexdigest()
def fail(reason): raise ValueError("12SA_" + reason)

def verify(record_path=RECORD, ry_path=RY, rz_path=RZ, qw_path=QW):
    d,ry,rz,qw = (read(p) for p in (record_path,ry_path,rz_path,qw_path))
    if (d.get("batch"), d.get("parent_open_batch"), d.get("stage"),
        d.get("status")) != ("12SA","12QE","12QE_OPEN",
        "FORTY_SOURCE_JPEG_NATIVE_ORIGINAL_PAGES_BOUNDED_MANUAL_HEADING_TOPIC_SCREEN_NO_FULLTEXT_OR_NEGATIVE_PROOF"):
        fail("BATCH_STAGE_REVIEW_SCOPE")
    s,v,a = d["source"],d["review"],d["grade_union"]
    qw6 = next((x for x in qw["source_archives"] if x["fascicle"] == 6), None)
    if qw6 is None: fail("NO_F6_ORIGINAL_ARCHIVE")
    ys,zs = ry["source"],rz["source"]
    if not (s["physical_holding"] == ys["physical_holding"] == zs["physical_holding"]
            == "NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"] == ys["digital_fascicle"] == zs["digital_fascicle"] == 6
            and s["commons_file_id"] == ys["commons_file_id"] == zs["commons_file_id"]
            == "NLC892-411999003250-383071"
            and s["source_pdf_page_count"] == ys["source_pdf_pages"] == zs["source_pdf_pages"]
            == qw6["pdf_pages"] == 116
            and s["source_pdf_sha256"] == ys["source_pdf_sha256"] == zs["source_pdf_sha256"]
            == qw6["source_pdf_sha256"] == PDF_SHA
            and s["source_pdf_binary_rehashed_this_batch"] is False
            and s["archived_artifact_id"] == ys["archived_actions_artifact_id"] == zs["artifact_id"]
            == qw6["artifact_id"] == 11674845912
            and s["archived_zip_sha256"] == ys["archive_zip_sha256"] == zs["archive_zip_sha256"]
            == qw6["artifact_zip_sha256"] == ZIP_SHA
            and s["archived_status_json_sha256"] == ys["status_json_sha256"] == zs["status_sha256"]
            == qw6["artifact_metadata_sha256"] == STATUS_SHA
            and s["archive_all116_original_jpeg_sha256_and_bytes_verified"] == 116
            and s["archive_original_jpeg_hash_or_size_mismatches"] == 0
            and s["full116_image_sha256_ordered_chain"]
            == ys["full116_original_jpeg_ordered_chain"]
            == zs["full116_source_jpeg_ordered_chain"]
            == qw6["page_sha_chain"] == FULL116):
        fail("SINGLE_ARCHIVE_SOURCE_PINS")
    w = v["original_source_page_windows"]
    if not (len(w)==2 and v["original_jpeg_pages_opened"]==40
            and v["mode"]=="FORTY_ORIGINAL_SOURCE_JPEGS_OPENED_IN_TEN_2X2_PAGE_PRESERVING_NATIVE_PIXEL_MONTAGES_FOR_BOUNDED_HEADING_TOPIC_SCREEN"):
        fail("SCOPE_WINDOW")
    all_new=[]
    for entry, (lo,hi,expected_sha) in zip(w,[(41,60,SHA41_60),(61,80,SHA61_80)]):
        hs=entry["source_original_jpeg_sha256_in_page_order"]
        if not (entry["start_pdf_page"]==lo and entry["end_pdf_page"]==hi
                and len(hs)==20 and all(isinstance(h,str) and re.fullmatch("[0-9a-f]{64}",h) for h in hs)
                and chain(hs)==entry["sha256_concatenated_source_jpeg_hashes"]==expected_sha):
            fail("WINDOW_SEQUENCE_SHA_AND_PDF_PAGE_IDS")
        all_new+=hs
    old_1_20=ry["review"]["individual_page_sha256_in_order"]
    old_21_40=rz["review"]["source_jpeg_sha256_in_page_order"]
    if not (len(old_1_20)==len(old_21_40)==20
            and chain(old_1_20)==ry["review"]["p1_20_original_jpeg_ordered_chain"]
            and chain(old_21_40)==rz["review"]["window20_ordered_source_jpeg_chain"]
            and chain(old_1_20+old_21_40)==v["inherited_p1_40_original_jpeg_ordered_sha256"]
              ==rz["review"]["first40_ordered_original_jpeg_chain"]
            and chain(old_1_20+old_21_40+all_new)==v["p1_80_original_jpeg_ordered_sha256"]==SHA1_80):
        fail("PARENT_TO_80_NATIVE_JPEG_CHAIN")
    if ([e["page_range"] for e in v["direct_original_chronicle_context_observations"]]
            != [[41,48],[49,56],[57,64],[65,72],[73,80]]
            or not all(isinstance(e.get("scope"),str) and e["scope"] for e in v["direct_original_chronicle_context_observations"])):
        fail("BOUNDED_VISUAL_WINDOW_DESCRIPTIONS")
    false_fields=["positive_original_old20_gaizao_louke_title_or_passage_attestation",
                  "ocr_used","full_text_character_by_character_collated",
                  "any_source_page_target_absence_proven","whole_original_work_absence_proven",
                  "original_juan_equivalent_to_1827_reordered_30_juan_proven",
                  "new_pdf_binary_rehash_performed"]
    if any(v.get(k) is not False for k in false_fields):
        fail("SCOPE_OR_UNPROVEN_ABSENCE")
    expected={
        "baseline_batch":"12RZ","baseline_f6_bounded_original_page_count":40,
        "new_f6_bounded_original_page_count":80,"new_f6_native_pdf_ranges":[[1,80]],
        "remaining_f6_preview_only_source_ranges":[[81,116]],
        "remaining_f6_preview_only_source_pages":36,
        "whole1030_baseline_native_source_pages":498,"whole1030_new_native_source_pages":538,
        "whole1030_baseline_native_body_pages":497,"whole1030_new_native_body_pages":537,
        "whole1030_baseline_preview_only_body_pages":530,"whole1030_new_preview_only_body_pages":490,
        "whole1030_non_target_prelims":2,"whole1030_total_source_pages":1030,
        "body_fulltext_collation_still_pending":1027,
        "same_physical_copy_not_ten_independent_witnesses":True,
        "new_independent_physical_copy_count":0,
        "source_navigation_pages_reopened_not_recounted":True}
    if a!=expected or (
            rz["dedup"]["new_f6_native_source_pages"]!=40
            or rz["dedup"]["new_whole_source_native"]!=498
            or rz["dedup"]["new_whole_source_preview"]!=530
            or rz["dedup"]["f6_remaining_preview_only_pages"]!=76):
        fail("GRADING_UNION_OR_DOUBLE_COUNT")
    if (d["transmission_impact"]["edges_supported"]
        or d["transmission_impact"]["edges_revised"]
        or d["invariants"]!={"matrix_rows":222,"provenance_repairs":45,
                             "external_sources":"647+7=654","md_g03":"OPEN",
                             "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
                             "product_r1":"CLOSED","confirmed_chart_algorithm_defects":0,
                             "algorithm_reopens":0}):
        fail("TRANSMISSION_CHART_INVARIANTS")
    return {"batch":"12SA","new_original_pages":40,"f6_native_total":80,"f6_remaining_preview":36,
            "whole_native_source":538,"whole_preview_source":490,"non_target_prelims":2,
            "fulltext_body_pending":1027,"algorithm_reopens":0}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
