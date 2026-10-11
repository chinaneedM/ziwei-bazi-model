#!/usr/bin/env python3
"""12QZ native original page visual screen != exhaustive transcript or absence proof."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12QZ-NLC411999003250-F1-P3-22-NATIVE-SOURCE-REVIEW-R1.json"
QO=RS/"MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QY=ROOT/"scripts/verify_yehuobian_nlc_f1_f3_firstpass_12qy.py"
PIN=[
"48f7fefc2624dd8475040dd79fe3e22a7a8f41668c0f5dea245338f943fde7a0",
"a6e63d8902c62642ca45a37d2873423b90895240c900440bdf13ea2f722ca093",
"aee07414630208f50fffdfb88b697aa794c8593d7bee0fc7f2ccc1f6616ab6c1",
"22bacffc00d48e4d09b1e9c5ec47a7e9b69c8ff2395f918a43f279480fc4ba74",
"e2821cb5ace05d7e81f5257aa6a43cb6fcb2bf7d6cfb6083e5605a22ec8dcfe0",
"bd5b130da9c467103cadbfa31025d3cde1393bd2447fe7d55ed3eb6aeace2703",
"c34588a1533c8b2fda56765447d0838bf615f8b5306fb73904925879d059c1f0",
"6e50d3f9a75a11ae22b648ee881e051ee4ea5ede1dc5a992f833ba38905ff02a",
"cfdb1e78d3a4be8feb2f012ffa4654b02f727f62ce9611ff91fffa4c63a3cc21",
"6d70dd2489e9108f4427224a6c5ec3ef16142836a55d09000184eb9dca48c45d",
"da1a6a237eb70602a95e4c6d87961bbd0dd29bdddafcccc3e7721c63c366c220",
"8d341d88839d08ce2d06ff2ffed1518b3f84eb708919a6ac33d54558eac864f0",
"2a94853eb43881080544914701d8298d5f3a571efc998cf6d386132eb6e23d75",
"e9a340f0ec295d44d79ad1a3570fd6dd64720ed63e62aa87e24fe06a277913cb",
"1553ecbfe6b297a1d8678b27d984f88482dd1166ede67e4925b733bc8244022e",
"8d5c80d7feb4236a99a760d636c56c3738c7a77eddbcf4c8e7d74aab2a666b61",
"12b2bf50c9d8d1c5fce07c4398cd7b1efae3d4b304aadfe8c212d13f42b9d7d5",
"880d42ced39943b197463ec4b84bb238a891d63d38cc935802eae7f16a12d831",
"25caf883ffc464315d71c5911bae4f867ca22ec79c7ed98b628161988eba0633",
"808ae19f391b395a79a45363406cc8b40c37858c56ea79923d1163aba498a794"
]
SOURCE_PDF_SHA="acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939"
ZIP_SHA="18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429"
STATUS_SHA="7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070"
SEQUENCE_SHA="905741bf94a40320e807b31d1da04888c51b7f54bf6503b18be3a5dabc4c5aad"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def qy_module():
    spec=importlib.util.spec_from_file_location("tianwen_12qy_for_12qz",QY)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def verify(path=RECORD):
    data=load(path)
    prior_module=qy_module()
    before=prior_module.verify()
    source=data["source"]
    review=data["review"]
    queue=data["queue_reconciliation"]
    if not (data["stage"]=="12QE_OPEN"
            and data["status"]=="TWENTY_NATIVE_ORIGINAL_SOURCE_PAGE_TARGET_VISUAL_SCREENS_NONEXHAUSTIVE"
            and source["holding"]=="NLC411999003250_ONE_HOLDING"
            and source["original_volume"]==source["digital_fascicle"]==1
            and source["source_pdf_pages"]==119
            and source["source_pdf_sha256"]==SOURCE_PDF_SHA
            and source["source_pdf_binary_rehashed"] is False
            and source["artifact_id"]==11674078668
            and source["artifact_zip_sha256"]==ZIP_SHA
            and source["artifact_status_json_sha256"]==STATUS_SHA
            and source["source_original_jpeg_members_rechecked"]==20
            and source["image_hash_mismatches"]==0):
        raise ValueError("12QZ_SOURCE_HOLDING_OR_ARCHIVE_SHA_DRIFT")
    digest=hashlib.sha256("".join(PIN).encode("ascii")).hexdigest()
    if not (review["mode"]=="INDIVIDUAL_NATIVE_SOURCE_PAGE_VISUAL_HEADING_OR_TARGET_PHRASE_SCREEN"
            and review["pdf_page_first"]==3
            and review["pdf_page_last"]==22
            and review["original_pdf_pages_individually_viewed"]==20
            and review["target_original_glyph_positive_attestations"]==0
            and review["heading_or_passage_search_visual_only"] is True
            and review["full_text_transcribed"] is False
            and review["ocr_used"] is False
            and review["proof_target_absent_on_any_page"] is False
            and review["proof_target_absent_in_manuscript"] is False
            and review["ancient_rule_adjudicated"] is False
            and review["page_image_sha256_in_pdf_order"]==PIN
            and review["page_image_sha256_concatenation_sha256"]==digest==SEQUENCE_SHA
            and review["page_source_hashes_from"]=="EXACT_PRIOR_ARCHIVED_F1_ARTIFACT_STATUS_JSON_AND_BINARY_REHASH"
            and review["page_3_original_volume_opening_direct_image_label"]=="萬曆二十六年戊戌卷一"
            and review["page_3_year"]==1598):
        raise ValueError("12QZ_NOT_NATIVE_OR_FALSE_ABSENCE_PROOF")
    qt=prior_module.qx_module().qw_module().qv_module().qu_module().qt_module()
    baseline=[r for r in qt.build_rows() if r["fascicle"]==1 and 3<=r["pdf_page"]<=22]
    if len(baseline)!=20 or [r["pdf_page"] for r in baseline]!=list(range(3,23)):
        raise ValueError("12QZ_SOURCE_NATIVE_PAGE_RANGE_CHANGED")
    for i,row in enumerate(baseline):
        if not (row["source_pdf_sha256"]==SOURCE_PDF_SHA
            and row["original_volume_candidates"]==[1]
            and row["body_search_eligible"]
            and row["requires_native_target_screen"]
            and row["target_screen_grade"]=="NOT_TARGET_SCREENED"
            and (row["page_jpeg_sha256_if_known"] is None or row["page_jpeg_sha256_if_known"]==PIN[i])):
            raise ValueError("12QZ_SOURCE_PAGE_PREVIOUS_ORIGINAL_IDENTITY_CHANGED")
    opening=next(x for x in load(QO)["original_juan_openings"]
                 if x["digital_fascicle"]==1 and x["volume"]==1)
    if not (opening["pdf_page"]==3 and opening["page_jpeg_sha256"]==PIN[0]
            and opening["right_leaf_has_previous_volume"] is False
            and opening["year_label"]==1598):
        raise ValueError("12QZ_VOLUME1_OPENING_NOT_SAME_NATIVE_SOURCE")
    after=copy.deepcopy(before)
    after["native_screened_source_pages"]+=20
    after["montage_only_source_pages"]-=20
    after["native_body_review_backlog"]-=20
    after["per_fascicle"]["1"]["native_screens"]+=20
    after["per_fascicle"]["1"]["fourup_only"]-=20
    after["per_fascicle"]["1"]["native_body_backlog"]-=20
    if not (
        queue["old_native_source_page_screens"]==before["native_screened_source_pages"]==29
        and queue["new_native_source_page_screens"]==after["native_screened_source_pages"]==49
        and queue["old_preview_only_source_pages"]==before["montage_only_source_pages"]==999
        and queue["new_preview_only_source_pages"]==after["montage_only_source_pages"]==979
        and queue["old_native_body_target_review_backlog"]==before["native_body_review_backlog"]==999
        and queue["new_native_body_target_review_backlog"]==after["native_body_review_backlog"]==979
        and queue["body_full_text_collation_backlog"]==after["body_full_text_collation_backlog"]==1027
        and queue["body_not_even_firstpass_screened"]==after["body_not_even_firstpass_screened"]==0
        and queue["non_body_no_target_screen_pages"]==after["not_target_screened_source_pages"]==2
        and queue["source_pages"]==after["source_pages"]==1030
        and queue["body_pages"]==after["body_pages"]==1027
        and queue["whole_manuscript_negative_proven"] is False
        and queue["independent_physical_copy_increment"]==0
        and after["global_target_absence_proven"] is False
        and after["per_fascicle"]["1"]["native_screens"]==20
        and after["per_fascicle"]["1"]["fourup_only"]==97
        and after["per_fascicle"]["1"]["native_body_backlog"]==97
        and data["invariants"]["deterministic_chart_product_r1"]=="CLOSED"
        and data["invariants"]["confirmed_algorithm_reopens"]==0):
        raise ValueError("12QZ_SOURCE_COUNT_OR_NATIVE_STATUS_PROMOTION")
    return after

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
