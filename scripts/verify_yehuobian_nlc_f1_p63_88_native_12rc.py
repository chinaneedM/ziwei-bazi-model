#!/usr/bin/env python3
"""12RC proof-scoped validation for NLC old20 original JPEG images PDF p63–88."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RC-NLC411999003250-F1-P63-88-NATIVE-SOURCE-REVIEW-R1.json"
RB=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RB-NLC411999003250-F1-P43-62-NATIVE-SOURCE-REVIEW-R1.json"
QO=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
PDF_SHA="acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939"
ZIP_SHA="18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429"
STATUS_SHA="7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070"
PINS="5284e2114609a942f054dc77f0a1be801fc26066dde7fc5336cd80c87291189b,7eefe4acffa1609fa2b76202b4751d8e7a8a36011e12954e03b785e87cf2b3eb,8c68d5eb23c2e2665fd19cdab85bb8257cf8c1377e95200bcc67a59d23d6ec8c,1e489012823c4f5c37a3d7028ea82e027b2f39b5c7a220b388c11f293d980d99,47ae576987e4c4ae90b7d33bb114cc063ceb55e297554772829df87dafcef8dd,9d2ab5662a6fe7d088ec462d198a4c2e358a718ee03a5a8e944490c6d7357a2e,e197409b264fb1483bfbe77694d643b2a63203c7c6f58b73c6190f6cf90a95ec,a49e621c80743036355c76ae6d3066523693c5aef37ed092f840d260f474dce0,928d82d9eb8d6d56df7fc76af2855d5568d92b7908e758b603af7e5dee8e1030,0a727ef15456ee70eefb747272c8b6035f0b7334f001be01330210ea9ff1e322,ecfda7f13a146d8678c1b5f0ebc6744629663ecd91ee53ed6975ec3aba1030a1,17b73f7766ea67c76aa77491e28aa9c4ae8cd4bfd6e24717d3c76a80b7612f9b,459a7f7b90112195e9432c035db570b7252906f1d3ad7871a605ccbea18f9d09,ca31ce5106a6b44ad95ae2ffc05b9b4a007db3291e3cf1b1f2ec4f626dbf3fcd,5951a5a63363d6788d1842c68f2aa378739358024ee6f26c3d823220b203cfa3,17f90b7c337c9dd6290587e1643d5c1b35302e99d7c9ca890571f25d7352e287,3de1e198d2cd1f259ed32977f77d0b9b2ef566d0f28316b70eb4d0733950abeb,8d2334b69373dddf651d5f6e2cf96ed107165ee3e83fc3ae1b92a5830be77195,e58ec8523c39c1c5626711fdb6f271c349a4fba95457d8e25e6d86a50418d701,d5bc0bb49529f66d24e70b3874344ebebc17fcca3d33e0495470a99350dcd085,2f1155a84be3854f5a839679cde0ba637e82ab54f26676ddd4d4d9c796ac136d,8c6fcb0c8e01cc23342e44f178ece9f72ba1f8677b02a061e07d242f19afd598,f88e921e24f6381ab50a39d9ecbaeab18363f2099e8dabcadf10c326fe21d705,b5a4ebe7e8a275e53547f30386b5e7590bb7ea2bfe9647fafb57110c55803bee,c60d9b5161aa6596956f6be037d43eb8e289c7f38c8939f935c633d0510fe44a,086ae37fbcd0234025d1dd9637d72c344b73315622f59df87efde8d03a0c1c7a".split(",")
CHAIN="4f20a1e8db05816b4a69a850f3cd7b0f5261a45ccde1fcd53655b0f4351f4cf8"
def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def verify(record_path=RECORD,rb_path=RB,qo_path=QO):
    r,rb,qo=read(record_path),read(rb_path),read(qo_path)
    s,v,q=r["source"],r["review"],r["queue"]
    old=rb["queue"]
    if not (r["batch"]=="12RC" and r["stage"]=="12QE_OPEN"
            and r["status"]=="TWENTY_SIX_NATIVE_ORIGINAL_SOURCE_JPEG_BOUNDED_TARGET_VISUAL_SCREENS_NONEXHAUSTIVE"
            and s["holding"]==rb["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==1 and s["source_pdf_pages"]==119
            and s["source_pdf_sha256"]==rb["source"]["source_pdf_sha256"]==PDF_SHA
            and s["artifact_id"]==rb["source"]["artifact_id"]==11674078668
            and s["artifact_zip_sha256"]==rb["source"]["artifact_zip_sha256"]==ZIP_SHA
            and s["artifact_status_json_sha256"]==rb["source"]["artifact_status_json_sha256"]==STATUS_SHA
            and s["source_pdf_binary_rehashed"] is False
            and s["individually_rehashed_native_jpeg_pages"]==26
            and s["individual_jpeg_hash_mismatches"]==0):
        raise ValueError("12RC_SOURCE_HASH_IDENTITY_OR_PDF_REHASH_CLAIM_DRIFT")
    hashes=v["original_jpeg_sha256_by_pdf_page"]
    if not (v["mode"]=="INDIVIDUAL_ORIGINAL_RESOLUTION_NATIVE_JPEG_BOUNDED_TARGET_VISUAL_SCREEN"
            and v["first_pdf_page"]==63 and v["last_pdf_page"]==88
            and v["original_jpegs_individually_opened"]==26
            and len(hashes)==26 and hashes==PINS
            and hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()==v["ordered_sha256_text_chain_digest"]==CHAIN
            and v["target_original_glyph_positive_attestations"]==0
            and v["complete_text_transcription_performed"] is False
            and v["ocr_used"] is False
            and v["no_positive_target_found_does_not_prove_page_absence"] is True
            and v["proof_target_absent_on_any_page"] is False
            and v["proof_target_absent_in_manuscript"] is False):
        raise ValueError("12RC_PAGE_HASH_VISUAL_GRADE_OR_NEGATIVE_PROOF_DRIFT")
    if v["original_juan_scope"]!=[
       {"pdf_page_first":63,"pdf_page_last":87,"original_volume_candidates":[3]},
       {"pdf_page_first":88,"pdf_page_last":88,"original_volume_candidates":[3,4]}]:
        raise ValueError("12RC_ORIGINAL_JUAN_SCOPE_DRIFT")
    mixed=v["mixed_boundary_page_88"]
    opening=next((x for x in qo["original_juan_openings"] if x["digital_fascicle"]==1 and x["volume"]==4),None)
    if not (mixed=={"page_jpeg_sha256":PINS[-1],"original_juan_started":4,
                  "visible_heading":"萬曆二十九年辛丑卷四","year_label":1601,
                  "right_leaf_continues_original_juan":3,"left_leaf_starts_original_juan":4,
                  "whole_pdf_page_is_not_exclusively_old_juan4":True}
            and opening is not None and opening["pdf_page"]==88
            and opening["page_jpeg_sha256"]==PINS[-1] and opening["year_label"]==1601
            and opening["right_leaf_has_previous_volume"] is True):
        raise ValueError("12RC_MIXED_LEAF_RIGHT_OLD3_LEFT_OLD4_COLLAPSED")
    if not (q["baseline_batch"]=="12RB"
            and (q["before_native_bounded_source_pages"],q["before_preview_only_source_pages"],
                 q["before_native_body_target_backlog"])==
                (old["new_native_pages"],old["new_preview_only_pages"],old["new_native_body_backlog"])==(89,939,939)
            and (q["after_native_bounded_source_pages"],q["after_preview_only_source_pages"],
                 q["after_native_body_target_backlog"])==(115,913,913)
            and q["full_text_body_collation_backlog"]==old["full_text_collation_body_backlog"]==1027
            and q["body_not_even_firstpass_screened"]==0
            and q["preliminary_nonbody_not_target_screened"]==2
            and (q["source_pages_total"],q["body_pages_total"])==(1030,1027)
            and (q["fascicle1_native_bounded_target_screens"],q["fascicle1_preview_only_source_pages"])==(86,31)
            and q["independent_physical_copy_increment"]==0
            and q["global_target_absence_proven"] is False
            and r["transmission_impact"]["edges_supported"]==[]
            and r["invariants"]["deterministic_chart_product_r1"]=="CLOSED"
            and r["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("12RC_UNEARNED_WITNESS_CREDIT_OR_QUEUE_COUNTER_DRIFT")
    return {"batch":"12RC","native_source_target_screens":115,
            "native_body_backlog":913,"preview_only_source_pages":913,
            "body_full_text_collation_backlog":1027,
            "page88_mixed_original_juan":[3,4],
            "global_target_absence_proven":False}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
