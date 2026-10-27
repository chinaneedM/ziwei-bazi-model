#!/usr/bin/env python3
"""12RB validates page-source review metadata without false proof of target absence."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RB-NLC411999003250-F1-P43-62-NATIVE-SOURCE-REVIEW-R1.json"
RA=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RA-NLC411999003250-F1-P23-42-NATIVE-SOURCE-REVIEW-R1.json"
QO=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
SOURCE_PDF="acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939"
ZIP_SHA="18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429"
STATUS_SHA="7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070"
CHAIN="bd3c8b8474eb1874243df0a53c3477a01f306c76db0c187432003cf47f322f01"
PAGE62="f2e336479c322cde066d866208127ecd9966548dbf9c20454c01342d023e42d4"
def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))
def verify(record_path=RECORD,ra_path=RA,qo_path=QO):
    r,ra,qo=read(record_path),read(ra_path),read(qo_path)
    s,v,q=r["source"],r["review"],r["queue"]
    prv=ra["queue_reconciliation"]
    if not (r["batch"]=="12RB" and r["stage"]=="12QE_OPEN"
        and r["status"]=="TWENTY_NATIVE_ORIGINAL_JPEG_TARGET_SCREENS_NOT_FULL_TEXT"
        and s["holding"]==ra["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
        and s["digital_fascicle"]==1 and s["source_pdf_pages"]==119
        and s["source_pdf_sha256"]==ra["source"]["source_pdf_sha256"]==SOURCE_PDF
        and s["artifact_id"]==ra["source"]["artifact_id"]==11674078668
        and s["artifact_zip_sha256"]==ra["source"]["artifact_zip_sha256"]==ZIP_SHA
        and s["artifact_status_json_sha256"]==ra["source"]["artifact_status_json_sha256"]==STATUS_SHA
        and s["original_image_jpegs_hash_matched"]==20 and s["image_hash_mismatches"]==0
        and s["source_pdf_binary_rehashed"] is False):
        raise ValueError("12RB_BAD_SOURCE_OR_HASH_EVIDENCE")
    pins=v["source_image_sha256_by_pdf_page"]
    if not (v["pdf_page_first"]==43 and v["pdf_page_last"]==62
        and v["original_jpegs_individually_opened"]==20
        and v["mode"]=="INDIVIDUAL_NATIVE_SOURCE_IMAGE_BOUNDED_VISUAL_HEADING_TARGET_SCREEN"
        and len(pins)==20 and all(len(h)==64 and all(c in "0123456789abcdef" for c in h) for h in pins)
        and hashlib.sha256("".join(pins).encode("ascii")).hexdigest()==v["hash_sequence_sha256"]==CHAIN
        and pins[-1]==PAGE62
        and v["pages_43_to_61_original_juan"]==2
        and v["ocr_used"] is False and v["full_text_transcribed"] is False
        and v["positive_target_original_glyph_attested"] is False
        and v["negative_page_text_proven"] is False
        and v["negative_manuscript_text_proven"] is False):
        raise ValueError("12RB_INCORRECT_TARGET_REVIEW_OR_TEXT_PROOF")
    leaf=v["year_1600_original_juan3_start"]
    opening=next((o for o in qo["original_juan_openings"] if o["digital_fascicle"]==1 and o["volume"]==3),None)
    if not (leaf=={"pdf_page":62,"sha256":PAGE62,"heading":"萬曆二十八年庚子卷三",
                       "right_leaf_previous_volume":False,"right_half_blank":True,"left_half_volume":3}
        and opening is not None and opening["pdf_page"]==62 and opening["page_jpeg_sha256"]==PAGE62
        and opening["year_label"]==1600 and opening["right_leaf_has_previous_volume"] is False):
        raise ValueError("12RB_ORIGINAL_JUAN3_LEAF_IDENTITY_DRIFT")
    if not (q["previous_batch"]=="12RA"
        and (q["previous_native_pages"],q["previous_preview_only_pages"],q["previous_native_body_backlog"])
             ==(prv["new_native_source_page_screens"],prv["new_preview_only_source_pages"],prv["new_native_body_target_review_backlog"])
             ==(69,959,959)
        and (q["new_native_pages"],q["new_preview_only_pages"],q["new_native_body_backlog"])==(89,939,939)
        and (q["source_pages"],q["body_pages"],q["full_text_collation_body_backlog"])==(1030,1027,1027)
        and q["body_not_firstpass_screened"]==0 and q["unreviewed_prelim_nonbody"]==2
        and q["new_physical_copy_count"]==0 and q["global_negative_proven"] is False
        and r["transmission_impact"]["edges_supported"]==[]
        and r["invariants"]["deterministic_product"]=="CLOSED" and r["invariants"]["algorithm_reopens"]==0):
        raise ValueError("12RB_QUEUE_OR_INVARIANT_DRIFT")
    return {"batch":"12RB","native_screened_source_pages":89,"native_body_backlog":939,
            "fulltext_body_backlog":1027,"original_juan3_opening_page":62,
            "target_absence_proven":False}
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False,indent=2))
