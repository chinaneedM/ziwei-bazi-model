#!/usr/bin/env python3
"""12SF F9 p1-80: validate source-page SHA sequences and evidence-grade firewall."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12SF-NLC411999003250-F9-P1-80-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
QV=RS/"MING-DATONG-YEHUOBIAN-12QV-NLC411999003250-F9-141-PAGE-CONTACT-TRIAGE-R1.json"
SE=RS/"MING-DATONG-YEHUOBIAN-12SE-NLC411999003250-F8-ALL87-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
SHA80="75b80312ee881ff6fb5e93998cb23761b3230cbde051c038da9c9b0717ea4df5"
SHA141="0b1f1df616301c576f937ffd336a513e6e87a0869d314f425890456e211828d5"
GROUP=["92d1572dafa50d4c5e6ebf2a8e65d4bad6e7102daa3a572cda4dc32fed84ec1c","6221e3e28a4a29a5ae3408db34ae83f925800fea63ef301ff4899824081d5e00","7f309b29fad18c8b818c4a2ff7bcc022e8860ed909deccef7a769663187f5ff1","b5ff3c092a9b65b87ad23d42617cf199b1bc792fee087e27bf9b59b6d4cb0175"]
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(xs):return hashlib.sha256("".join(xs).encode("ascii")).hexdigest()
def reject(x):raise ValueError("12SF_"+x)
def verify(path=RECORD):
    d,qv,se=read(path),read(QV),read(SE)
    s,v,g=d["source"],d["review"],d["grade_union"]
    if (d.get("batch"),d.get("parent_open_batch"),d.get("stage"),d.get("status"))!=("12SF","12QE","12QE_OPEN","F9_P1_80_ORIGINAL_JPEG_PAGE_NATIVE_BOUNDED_FIRSTPASS_NOT_FULLTEXT_NOT_PASSAGE_ABSENCE_PROOF"):reject("BATCH_STAGE")
    qs=qv["source"]
    if not(s["physical_holding"]==qs["holding"]=="NLC411999003250_ONE_HOLDING"
      and s["digital_fascicle"]==qs["fascicle"]==9
      and s["commons_file_id"]=="NLC892-411999003250-383063"
      and s["source_pdf_pages"]==qs["pages"]==141
      and s["original_chronological_volume_candidates"]==qs["volume_candidates"]==[16,17]
      and s["source_pdf_sha256"]==qs["source_pdf_sha256"]
      and s["source_pdf_binary_rehashed_this_batch"] is False
      and s["original_workflow_run_id"]==qs["workflow_run_id"]==38064436808
      and s["archived_artifact_id"]==qs["artifact_id"]==11674711170
      and s["artifact_zip_sha256"]==qs["artifact_zip_sha256"]
      and s["artifact_status_json_sha256"]==qs["status_json_sha256"]
      and s["source_jpeg_size_sha256_rechecked_all141"]==141
      and s["source_jpeg_size_sha256_mismatches"]==qs["hash_mismatches"]==0
      and s["source_all141_original_jpeg_ordered_chain"]==qs["page_sha_chain"]==SHA141):reject("ARCHIVED_SOURCE")
    hashes=v["individual_source_page_sha256_in_pdf_order"]
    if not(len(hashes)==80 and len(set(hashes))==80
      and all(isinstance(x,str) and re.fullmatch("[0-9a-f]{64}",x) for x in hashes)
      and chain(hashes)==v["p1_80_ordered_source_page_sha256_chain"]==SHA80
      and chain(hashes[:40])==v["p1_40_ordered_source_page_sha256_chain"]=="0eb68d90e8a116dde0ceec55e727e673ef6ce18ca5401a4f4330268501fb43c6"
      and [chain(hashes[i:i+20]) for i in range(0,80,20)]==v["twenty_page_windows_sha256"]==GROUP
      and hashes[0]==qv["navigation"]["p1_jpeg_sha256"]
      and v["source_all141_original_jpeg_ordered_chain"]==SHA141):reject("SOURCE_PAGE_HASH_ORDER")
    if not(v["mode"]=="ORIGINAL_JPEG_PIXEL_PRESERVING_2X2_PAGE_IDENTITY_MONTAGE_BOUNDED_HEADING_TOPIC_SCREEN"
      and (v["start_pdf_page"],v["end_pdf_page"],v["native_original_jpeg_pages_opened"])==(1,80,80)
      and v["montage_windows"]==[[x,x+3] for x in range(1,81,4)]
      and v["source_first_page_original_heading"]==qv["navigation"]["f9_p1_original16_heading"]
      and v["f9_original_volume17_boundary_native_reviewed_this_batch"] is False
      and [n["pages"] for n in v["topic_windows"]]==[[1,20],[21,40],[41,60],[61,80]]):reject("BOUNDED_REVIEW_SCOPE")
    for k in ("ocr_used","fulltext_character_by_character_collation_complete",
      "old20_gaizao_louke_original_heading_or_glyph_positive_attested",
      "page_target_absence_proven","whole_f9_target_absence_proven",
      "whole_old20_work_target_absence_proven","independent_print_1827_target_image_collated",
      "old20_chronological_volume_equivalent_to_1827_thematic_volume"):
        if v.get(k) is not False:reject("UNSUPPORTED_TEXT_OR_LINEAGE_"+k)
    expected={"prior_native_source_pages":751,"prior_preview_only_body_pages":277,
      "new_f9_native_body_source_pages":80,"after_native_source_pages":831,
      "after_native_body_pages":830,"after_preview_only_body_pages":197,
      "f9_native_bounded_after":80,"f9_pending_native_source_pages":61,
      "whole_holding_source_pages":1030,"f1_non_target_prelims":2,"nonbody_f10_colophon_native":1,
      "whole_body_fulltext_pages_pending":1027,"new_physical_copy_count":0,
      "new_independent_witness_count":0,"transmission_edges_supported":0,"algorithm_reopens":0}
    if g!=expected or se["grade_union"]["after_native_source_pages"]!=751 or se["grade_union"]["after_preview_only_body_pages"]!=277:reject("GRADED_PAGE_DEDUP")
    if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]:reject("FALSE_LINEAGE")
    if d["invariants"]!={"matrix":"222/222","repaired_provenance":"45/45","external_sources":"647+7=654",
      "md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
      "product_r1":"CLOSED","confirmed_algorithm_defects":0,"algorithm_reopens":0}:reject("PRODUCT")
    return {"batch":"12SF","f9_native_bounded_pages":80,"f9_pending":61,"global_native_source_pages":831,"global_preview_only_body_pages":197,"fulltext_body_pending":1027,"algorithms_reopened":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
