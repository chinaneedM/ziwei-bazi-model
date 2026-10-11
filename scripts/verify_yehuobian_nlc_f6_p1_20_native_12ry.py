#!/usr/bin/env python3
"""12RY: verify archived native original F6 source SHA ledger, dedup and philological scope."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RY-NLC411999003250-F6-P1-20-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
RX=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RX-NLC411999003250-ALL1030-SOURCE-PAGE-GRADE-UNION-R1.json"
QW=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE-R1.json"
QL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
ZIP="934d5c16493275c8fb0742abe8764d424bc4a2b2c5f02e99c5bcaab249a7d023"
STATUS="895597abefeac14f6f9c6c3b5a0bb41a8c1114d4250a17773e3e0e52bfc0d9e3"
SHA20="b176e7a32a5f1910b4a16dd086b78037450da01a4d5e88abe9fcab9ef82f0118"
SHA116="4998d749bb522d60cd7df499f5aefded8afb4e952111b4b3f2dff85d04573828"
FIRST="2e0c827b26682645ba9ace144b938638801a169ef1e012ea3deb03a89a20e190"
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def bad(t): raise ValueError("12RY_"+t)
def verify(record_path=RECORD,rx_path=RX,qw_path=QW,ql_path=QL):
    x,rx,qw,ql=map(read,(record_path,rx_path,qw_path,ql_path))
    s,v,d=x["source"],x["review"],x["dedup"]
    if (x.get("batch"),x.get("parent_open_batch"),x.get("stage"))!=("12RY","12QE","12QE_OPEN"):
        bad("BATCH_STAGE")
    if x.get("status")!="F6_P1_20_ORIGINAL_JPEG_HASH_VERIFIED_NATIVE_SOURCE_BOUNDED_MANUAL_FIRSTPASS_NO_FULLTEXT":
        bad("REVIEW_STATUS")
    ql6=next(y for y in ql["sources"] if y["fascicle"]==6)
    qw6=next(y for y in qw["source_archives"] if y["fascicle"]==6)
    if not(
       s["physical_holding"]=="NLC411999003250_ONE_HOLDING" and
       s["digital_fascicle"]==6 and s["original_juan_labels"]==[11] and
       s["commons_file_id"]=="NLC892-411999003250-383071" and
       s["source_pdf_pages"]==ql6["source_pdf_pages"]==qw6["pdf_pages"]==116 and
       s["source_pdf_sha256"]==ql6["source_pdf_sha256"]==qw6["source_pdf_sha256"] and
       s["source_pdf_binary_rehashed_this_batch"] is False and
       s["archived_actions_artifact_id"]==ql6["artifact_id"]==qw6["artifact_id"]==11674845912 and
       s["archive_zip_sha256"]==qw6["artifact_zip_sha256"]==ZIP and
       s["status_json_sha256"]==qw6["artifact_metadata_sha256"]==STATUS and
       s["full116_original_jpeg_ordered_chain"]==qw6["page_sha_chain"]==SHA116 and
       s["original_jpeg_members_sha256_size_checked"]==116 and s["source_jpeg_mismatch_count"]==0
    ):bad("ARCHIVE_SOURCE_SHA")
    hashes=v["individual_page_sha256_in_order"]
    if not (v["pdf_page_first"]==1 and v["pdf_page_last"]==20 and
         v["source_jpegs_opened_in_native_pixel_contact_montages"]==20 and
         len(hashes)==20 and all(isinstance(h,str) and re.fullmatch("[a-f0-9]{64}",h) for h in hashes)
         and hashes[0]==qw6["original_volume_opening_jpeg_sha"]==FIRST and
         hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()==v["p1_20_original_jpeg_ordered_chain"]==SHA20 and
         v["p1_heading_original_glyph"]=="萬曆三十六年戊申卷十一" and
         v["heading_previously_seen_at_archive_navigation"]=="12QW"):
        bad("WINDOW_PAGE_IMAGE_HASH_OR_HEADING")
    false_flags=("new_target_old20_gaizao_louke_original_glyph_confirmed",
                 "any_page_or_whole_work_target_absence_proven","fulltext_transcribed",
                 "original_juan_equivalence_to_1827_thematic_volume_proven",
                 "original_source_pdf_binary_rehashed")
    if any(v.get(k) is not False for k in false_flags) or v.get("no_ocr") is not True:
        bad("FALSE_PHILOLOGICAL_CLAIM")
    if not (rx["accounting"]["source_pages_with_prior_bounded_native_target_screen"]==458 and
         rx["accounting"]["body_pages_with_prior_bounded_native_target_screen"]==457 and
         rx["accounting"]["preview_only_pages"]==570 and
         rx["fascicles"][5]["preview_only_ranges"]==[[1,116]] and
         rx["fascicles"][5]["native_target_bounded_ranges"]==[] and
         d=={"scope":"SINGLE_NLC_HOLDING_F6_SOURCE_PDF_PAGE_SHA",
            "previous_12rx_f6_native_source_pages":0,
            "previous_12rx_f6_preview_only_pages":116,
            "previous_12qw_p1_source_navigation_reopen_same_original_page":True,
            "one_physical_holding_increment":0,
            "new_f6_unique_native_source_pages":20,
            "f6_remaining_preview_only_pages":96,
            "global_native_source_pages_after":478,"global_native_body_pages_after":477,
            "global_preview_only_body_pages_after":550,
            "global_non_target_prelims_after":2,"whole_holding_source_pages":1030,
            "body_fulltext_collation_pending":1027,
            "explicit_no_double_count_same_p1_source_identity":True}):
        bad("CROSSBATCH_DEDUP_GRADE")
    if x["transmission_impact"]["edges_supported"] or x["transmission_impact"]["edges_revised"] or x["invariants"]!={
        "matrix_rows":222,"matrix_audited":222,"provenance_repairs":45,
        "source_registry":"647+7=654","md_g03":"OPEN",
        "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","product_r1":"CLOSED","algorithm_reopens":0}:
        bad("LINEAGE_PRODUCT_INVARIANT")
    return {"batch":"12RY","new_f6_original_source_visual_pages":20,"next_f6_source_page":21,
            "full_source_native":478,"full_source_preview":550,
            "full_source_prelims":2,"body_fulltext_backlog":1027,"new_independent_witnesses":0}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
