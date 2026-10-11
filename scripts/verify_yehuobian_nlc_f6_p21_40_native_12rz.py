#!/usr/bin/env python3
"""12RZ original NLC fascicle6 p21-40 SHA chain and no-overclaim gate."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RZ-NLC411999003250-F6-P21-40-ORIGINAL-SOURCE-BOUNDED-REVIEW-R1.json"
RY=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RY-NLC411999003250-F6-P1-20-ORIGINAL-NATIVE-BOUNDED-REVIEW-R1.json"
QW=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE-R1.json"
FULL="4998d749bb522d60cd7df499f5aefded8afb4e952111b4b3f2dff85d04573828"
H20="c1d2d1d7bb27d75ba7e3fd955a57dd99b51e504e57c7e4185305781968650ecb"
H40="1ecccd156858206c65dd2e1ab447178f9aaa848ad09519b21a969cdd5727a744"
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(p):return hashlib.sha256("".join(p).encode("ascii")).hexdigest()
def bad(c):raise ValueError("12RZ_"+c)
def verify(record_path=RECORD,ry_path=RY,qw_path=QW):
    x,prior,qw=(read(p) for p in [record_path,ry_path,qw_path])
    s,v,q=x["source"],x["review"],x["dedup"]
    ps,pv=prior["source"],prior["review"]
    q6=next(z for z in qw["source_archives"] if z["fascicle"]==6)
    if not(x["batch"]=="12RZ" and x["parent_open_batch"]=="12QE" and x["stage"]=="12QE_OPEN" and
       x["status"]=="F6_P21_40_ORIGINAL_SOURCE_JPEG_2X2_PAGE_LEVEL_BOUNDED_MANUAL_SCREEN_NOT_FULLTEXT"):
        bad("BATCH_OR_EVIDENCE_LEVEL")
    if not (s["physical_holding"]==ps["physical_holding"]=="NLC411999003250_ONE_HOLDING" and
         s["digital_fascicle"]==ps["digital_fascicle"]==6 and
         s["commons_file_id"]==ps["commons_file_id"]=="NLC892-411999003250-383071" and
         s["source_pdf_pages"]==ps["source_pdf_pages"]==q6["pdf_pages"]==116 and
         s["source_pdf_sha256"]==ps["source_pdf_sha256"]==q6["source_pdf_sha256"] and
         s["source_pdf_binary_rehashed"] is False and
         s["artifact_id"]==ps["archived_actions_artifact_id"]==q6["artifact_id"]==11674845912 and
         s["archive_zip_sha256"]==ps["archive_zip_sha256"]==q6["artifact_zip_sha256"] and
         s["status_sha256"]==ps["status_json_sha256"]==q6["artifact_metadata_sha256"] and
         s["original_jpeg_hash_size_members_checked"]==116 and s["original_jpeg_member_mismatches"]==0 and
         s["full116_source_jpeg_ordered_chain"]==ps["full116_original_jpeg_ordered_chain"]==q6["page_sha_chain"]==FULL):
        bad("HOLDING_ARCHIVE_SOURCE_PIN")
    pins=v["source_jpeg_sha256_in_page_order"]
    old=pv["individual_page_sha256_in_order"]
    if not (v["mode"]=="ORIGINAL_JPEG_SOURCE_PAGES_OPENED_IN_FIVE_TWO_BY_TWO_PAGE_PRESERVING_MONTAGES_BOUNDED_HEADING_TOPIC_NOT_FULLTEXT" and
         v["first_pdf_page"]==21 and v["last_pdf_page"]==40 and
         v["exact_original_jpeg_source_pages_displayed"]==20 and len(pins)==len(old)==20 and
         all(isinstance(h,str) and re.fullmatch("[0-9a-f]{64}",h) for h in pins) and
         chain(pins)==v["window20_ordered_source_jpeg_chain"]==H20 and
         chain(old)==v["previous_p1_20_ordered_jpeg_chain"]==pv["p1_20_original_jpeg_ordered_chain"] and
         chain(old+pins)==v["first40_ordered_original_jpeg_chain"]==H40 and
         [o["source_pdf_range"] for o in v["bounded_subject_observations"]]==[[21,24],[25,28],[29,32],[33,36],[37,40]]):
        bad("HASH_SEQUENCE_OR_WINDOW_GAP")
    if not(v["ocr_used"] is False and v["full_text_linewise_collation_performed"] is False and
       v["original_old20_gaizao_louke_target_heading_or_glyph_positive_attestation"] is False and
       v["negative_page_passage_absence_proven"] is False and
       v["negative_whole_fascicle_or_work_absence_proven"] is False and
       v["original_juan_equivalent_to_1827_thematic_juan_proven"] is False):
        bad("FALSE_TARGET_OR_TEXT_SCOPE")
    if q!={"prior_batch":"12RY","prior_f6_native_source_pages":20,"new_f6_native_source_pages":40,
          "f6_remaining_preview_only_pages":76,
          "prior_whole_source_native":478,"new_whole_source_native":498,
          "prior_whole_source_preview":550,"new_whole_source_preview":530,
          "new_whole_source_native_body":497,"source_prelims":2,"source_pages_total":1030,
          "fulltext_body_pages_pending":1027,"independent_physical_copy_count_increment":0,
          "new_direct_transmission_edges":0,
          "prior_f6_p1_original_juan11_heading_not_recounted":True}:
        bad("SOURCE_PAGE_UNION_OR_DUPLICATION")
    if x["transmission_impact"]["edges_supported"] or x["transmission_impact"]["edges_revised"] or x["invariants"]!={"matrix":"222/222","provenance_repairs":"45/45","sources":"647+7=654","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","product":"CLOSED","algorithm_reopen_count":0}:
        bad("GENEALOGY_ALGORITHM_INVARIANT")
    return {"batch":"12RZ","f6_native_source_pages":40,"remaining_f6_preview_pages":76,"whole_source_native":498,"whole_source_preview":530,"whole_source_prelims":2,"fulltext_body_pending":1027}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
