#!/usr/bin/env python3
"""12SE F8: verify 87-source-JPEG ordered SHA identity and honest evidence scope."""
import hashlib
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12SE-NLC411999003250-F8-ALL87-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
QU=RS/"MING-DATONG-YEHUOBIAN-12QU-NLC411999003250-F8-87-PAGE-CONTACT-TRIAGE-R1.json"
SD=RS/"MING-DATONG-YEHUOBIAN-12SD-NLC411999003250-F7-P61-110-ORIGINAL-SOURCE-CLOSE-R1.json"
SHA87="b118385f23fbfb4219ea336474ceea3e77ed1864b175d41dbbb87c9b29c1a37f"
def load(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(a):return hashlib.sha256("".join(a).encode("ascii")).hexdigest()
def fail(reason):raise ValueError("12SE_"+reason)
def verify(path=RECORD):
    d,qu,sd=(load(p) for p in (path,QU,SD))
    if (d.get("batch"),d.get("parent_open_batch"),d.get("stage"),d.get("status"))!=(
      "12SE","12QE","12QE_OPEN","F8_ALL87_ORIGINAL_JPEG_NATIVE_BOUNDED_FIRSTPASS_NOT_LINEWISE_COLLATION_NOT_PASSAGE_ABSENCE_PROOF"):
        fail("BATCH")
    s,v,g=d["source"],d["review"],d["grade_union"]
    q=qu["source"]
    if not (
       s["holding"]=="NLC411999003250_ONE_HOLDING" and s["fascicle"]==8
       and s["original_volume_navigation_candidate"]==15
       and s["source_pdf_pages"]==q["source_pdf_pages"]==87
       and s["source_pdf_sha256"]==q["source_pdf_sha256"]
       and s["source_pdf_binary_rehashed_this_batch"] is False
       and s["archived_workflow_run_id"]==q["workflow_run_id"]==38064436808
       and s["archived_artifact_id"]==q["artifact_id"]==11674711192
       and s["archive_zip_sha256"]==q["artifact_zip_sha256"]
       and s["archived_status_json_sha256"]==q["artifact_status_json_sha256"]
       and s["source_jpeg_byte_size_and_sha256_verified"]==87
       and s["source_jpeg_mismatches"]==0):
        fail("SOURCE")
    hashes=v["original_jpeg_sha256_by_pdf_page"]
    if not (len(hashes)==87 and len(set(hashes))==87
      and all(isinstance(h,str) and re.fullmatch("[0-9a-f]{64}",h) for h in hashes)
      and chain(hashes)==v["page_sha256_chain"]==s["all87_source_jpeg_sha256_chain"]
         ==q["page_sha_sequence_sha256"]==SHA87
      and chain(hashes[:40])==v["window_1_40_chain"]=="e993a91388071f48e2d3bca5ee5ee1b7e361450153ad0939daf70f9fd7e314d0"
      and chain(hashes[40:60])==v["window_41_60_chain"]=="31e61c095cb9bbadd43a4e6963333ea57528208c138bf9b8d333743f2c80663c"
      and chain(hashes[60:])==v["window_61_87_chain"]=="01de7a2dc486d7b5d8925c5728d900774fa61cc7adaf0f4bfba915257ab70d86"):
        fail("ORDERED_SHA")
    if not (
       v["mode"]=="ORIGINAL_SIZE_UNSCALED_2X2_JPEG_MONTAGE_BOUNDED_HEADING_TOPIC_VISUAL_REVIEW_ONLY"
       and v["source_pages_opened"]==87 and v["original_source_page_range"]==[1,87]
       and v["original_size_montage_windows"]==[[i,min(i+3,87)] for i in range(1,88,4)]
       and [b["pages"] for b in v["bounded_topic_notes"]]==[[1,20],[21,40],[41,60],[61,87]]):
        fail("MONTAGE_OR_REVIEW_SCOPE")
    for name in (
      "ocr_used","automated_target_glyph_detection","fulltext_character_by_character_collation_complete",
      "positive_old20_gaizao_louke_original_target_folio_attestation",
      "individual_page_target_absence_proven","whole_fascicle_target_absence_proven",
      "whole_old20_work_target_absence_proven","printed_1827_themed_juan_equivalent_to_old20_juan15"):
        if v.get(name) is not False:fail("FALSE_AUTHORITY_"+name)
    expected={"inherited_native_source_pages":664,"inherited_preview_only_body_pages":364,
      "additional_native_source_body_pages":87,"after_native_source_pages":751,
      "after_native_body_pages":750,"after_preview_only_body_pages":277,
      "remaining_f8_preview_only_pages":0,"f8_native_original_source_pages_after":87,
      "whole_holding_source_pages":1030,"whole_holding_fulltext_body_pending":1027,
      "non_target_f1_prelims":2,"original_f10_nonbody_colophon":1,
      "independent_physical_holding_increment":0,"new_transmission_edges":0,"algorithm_reopens":0}
    if g!=expected or sd["grade_union"]["whole_holding_native_source_pages_after"]!=664:
        fail("GRADE_DEDUP")
    if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]:
        fail("FALSE_GENEALOGY")
    if d["invariants"]!={"matrix":"222/222","repaired_provenance":"45/45",
      "external_sources":"647+7=654","md_g03":"OPEN",
      "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","product_r1":"CLOSED",
      "confirmed_algorithm_defects":0,"algorithm_reopens":0}:
        fail("PRODUCT_INVARIANTS")
    return {"batch":"12SE","f8_native_bounded":87,"total_source_pages":1030,
      "native_bounded_source_pages":751,"preview_only_body_pages":277,
      "untouched_prelims":2,"body_fulltext_pending":1027,"chart_algorithm_reopens":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
