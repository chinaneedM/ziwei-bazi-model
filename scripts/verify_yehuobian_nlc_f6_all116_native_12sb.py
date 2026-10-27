#!/usr/bin/env python3
"""12SB: NLC fascicle 6 full116 source JPEG identity and evidence-grade replay."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="docs/research/MING-DATONG-YEHUOBIAN-"
RECORD=ROOT/(BASE+"12SB-NLC411999003250-F6-P81-116-ORIGINAL-SOURCE-CLOSE-R1.json")
RY=ROOT/(BASE+"12RY-NLC411999003250-F6-P1-20-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json")
RZ=ROOT/(BASE+"12RZ-NLC411999003250-F6-P21-40-ORIGINAL-SOURCE-BOUNDED-REVIEW-R1.json")
SA=ROOT/(BASE+"12SA-NLC411999003250-F6-P41-80-ORIGINAL-SOURCE-BOUNDED-REVIEW-R1.json")
QW=ROOT/(BASE+"12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE-R1.json")
SHA36="1239947daf48e79417206cdc3f44beeba7efe0937248dc2f1a849040b1805e30"
SHA80="517a2607b7e3c2bd171e6ba0966805232a3d10ed5d9df4f6ed89e0833b98d42b"
SHA116="4998d749bb522d60cd7df499f5aefded8afb4e952111b4b3f2dff85d04573828"
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(xs):return hashlib.sha256("".join(xs).encode("ascii")).hexdigest()
def reject(reason):raise ValueError("12SB_"+reason)
def verify(record_path=RECORD,ry_path=RY,rz_path=RZ,sa_path=SA,qw_path=QW):
    d,ry,rz,sa,qw=(read(p) for p in (record_path,ry_path,rz_path,sa_path,qw_path))
    if (d["batch"],d["parent_open_batch"],d["stage"],d["status"])!=(
      "12SB","12QE","12QE_OPEN",
      "F6_ALL116_ORIGINAL_SOURCE_PAGES_BOUNDED_FIRSTPASS_ONLY_NOT_FULLTEXT_NOT_TARGET_ABSENCE_PROOF"):
        reject("BATCH_STAGE")
    s,v,a=d["source"],d["review"],d["grade_and_scope"]
    q=next((x for x in qw["source_archives"] if x["fascicle"]==6),None)
    if not q:reject("NO_ARCHIVE")
    if not (s["holding"]==sa["source"]["physical_holding"]=="NLC411999003250_ONE_HOLDING"
      and s["digital_fascicle"]==6 and s["old20_juan_candidate"]==11
      and s["commons_file_id"]==sa["source"]["commons_file_id"]=="NLC892-411999003250-383071"
      and s["source_pdf_pages"]==q["pdf_pages"]==116
      and s["source_pdf_sha256"]==sa["source"]["source_pdf_sha256"]==q["source_pdf_sha256"]
      and s["source_pdf_binary_rehashed_this_batch"] is False
      and s["archived_artifact_id"]==sa["source"]["archived_artifact_id"]==q["artifact_id"]==11674845912
      and s["zip_sha256"]==sa["source"]["archived_zip_sha256"]==q["artifact_zip_sha256"]
      and s["status_json_sha256"]==sa["source"]["archived_status_json_sha256"]==q["artifact_metadata_sha256"]
      and s["original_jpeg_hash_and_file_size_verified"]==116
      and s["original_jpeg_hash_or_size_mismatches"]==0
      and s["complete_f6_116_original_jpeg_ordered_sha256"]==q["page_sha_chain"]==SHA116):
        reject("SOURCE_ARCHIVE_IDENTITY")
    old=ry["review"]["individual_page_sha256_in_order"]+rz["review"]["source_jpeg_sha256_in_page_order"]
    for w in sa["review"]["original_source_page_windows"]:
        old+=w["source_original_jpeg_sha256_in_page_order"]
    new=v["source_jpeg_sha256_in_ascending_pdf_page_order"]
    if not (v["start_pdf_page"]==81 and v["end_pdf_page"]==116 and
      v["original_source_jpegs_opened_this_batch"]==36 and len(old)==80 and len(new)==36
      and all(isinstance(h,str) and re.fullmatch("[0-9a-f]{64}",h) for h in old+new)
      and chain(old)==v["parent_12sa_p1_80_sha256_concatenated_source_jpeg_sha256"]==SHA80
      and chain(new)==v["last36_window_sha256_concatenated_source_jpeg_sha256"]==SHA36
      and chain(old+new)==s["complete_f6_116_original_jpeg_ordered_sha256"]==SHA116):
        reject("FULL116_PAGE_HASH_SEQUENCE")
    if not(v["mode"]=="ORIGINAL_JPEG_NATIVE_SOURCE_P81_116_NINE_2X2_PAGE_PRESERVING_MONTAGES_BOUNDED_HEADING_TOPIC_VISUAL_REVIEW_ONLY"
      and v["nine_native_pixel_montage_windows"]==[[i,i+3] for i in range(81,117,4)]
      and [x["page_range"] for x in v["bounded_subject_visual_observations"]]
        ==[[81,88],[89,96],[97,104],[105,112],[113,116]]):
        reject("BOUND_SCREEN_WINDOWS")
    for k in ("ocr_used","fulltext_character_by_character_collation_completed",
        "old20_original_gaizao_louke_target_folio_or_glyph_positive_attestation",
        "any_page_negative_absence_proven","whole_f6_fascicle_target_absence_proven",
        "whole_20juan_work_target_absence_proven","original_juan11_is_1827_themed_volume11_proven"):
        if v.get(k) is not False:reject("FALSE_TEXT_OR_ABSENCE_CLAIM")
    expected={"inherited_12sa_f6_native_body_pages":80,
      "f6_native_source_pages_after":116,"remaining_f6_preview_only_pages":0,
      "whole_holding_source_pdf_pages":1030,
      "whole_holding_native_original_source_pages_after":574,
      "whole_holding_original_body_pages_after":573,
      "whole_holding_preview_only_source_body_pages_after":454,
      "whole_holding_f1_non_target_preliminary_pages":2,
      "whole_body_pages_total":1027,"whole_body_fulltext_collation_pages_pending":1027,
      "physical_holding_increment":0,"new_independent_witnesses":0,"new_transmission_edges":0,
      "historic_source_images_newly_downloaded_this_batch":0,
      "no_repeated_source_page_counted_twice":True,
      "all_116_f6_source_page_images_grade_native_bounded_firstpass_only":True}
    if (a!=expected or sa["grade_union"]["new_f6_bounded_original_page_count"]!=80
      or sa["grade_union"]["whole1030_new_native_source_pages"]!=538):
        reject("WHOLE_SOURCE_PAGE_DEDUP")
    if (d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"]
      or d["invariants"]!={"matrix_rows":222,"matrix_audited":222,
        "provenance_metadata_repairs":"45/45","sources":"647+7=654",
        "md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
        "product_r1":"CLOSED","confirmed_chart_algorithm_defects":0,"algorithm_reopens":0}):
        reject("TRANSMISSION_OR_CHART")
    return {"batch":"12SB","f6_native_source_pages":116,
      "global_native_source_pages":574,"global_preview_only_pages":454,
      "global_prelims":2,"fulltext_body_pending":1027,"algorithms_reopened":0}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
