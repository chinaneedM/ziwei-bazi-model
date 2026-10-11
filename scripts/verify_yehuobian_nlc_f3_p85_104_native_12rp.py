#!/usr/bin/env python3
"""12RP: original third fascicle p85–104 JPEG page checksum-chain replay; preserve no-target-absence boundary."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RP-NLC411999003250-F3-P85-104-NATIVE-SOURCE-REVIEW-R1.json"
RO=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RO-NLC411999003250-F3-P61-80-NATIVE-SOURCE-REVIEW-R1.json"
RN=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RN-NLC411999003250-F3-P81-84-ORIGINAL-JUAN7-MIXED-LEAF-R1.json"
RK=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RK-NLC411999003250-F3-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
RL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RL-NLC411999003250-F3-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
RM=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RM-NLC411999003250-F3-P41-60-NATIVE-SOURCE-REVIEW-R1.json"
PINS=[
    "0da9c90e2ab2bad7337276d358cca982a3094d53494915018b7a1772ad10b7af",
    "c147b743054ae932e747b907d653250395104560064745b7a434886a7891c049",
    "dbec3b10745edcdde4a95c28173e8323890480d12dd7bf4f31cc386274a4cc55",
    "a3a16fe9b2a3bece65372e5b109aa098eb92dc7f170ea1a116e44ba50d36124e",
    "548d16f66d96b36b51a7126d28c7beffd798655f091f3ba8a997f619d364734b",
    "92f20ad6c7ed3839a9e15757b91c3d29eb73fdd5039071e67c10c3e11ee2d673",
    "311b39e15ffd635a73965b0c427f459a69d785c07d857ce300aa74a436be1a51",
    "d8f6c00814e5e326af2aa64664d664ee351de5efb298d46efbb3e4450165f5af",
    "76e969e2f7d8c948d320badc0bb2a02f9d1eb98a35ac2b7b6d4a8c6be328c78c",
    "56f7c918b4e14e068b84ad5fad0ad654a6aeffb7392b73f29862ed977712a79e",
    "a5f3d812fc744b3c5032c13e4bb5ae4573fda6868c2a10c683963b9bf0dbd7a6",
    "c6e1d11d8ebcf369d0077dc8913b731488c8101180fbe282039ed95cc85b9abd",
    "bf4e0b7184c230e912a91d4591e51e74a68e2af9d610e95ff9c311680382ba49",
    "10c1fa40a87daf77ec4246d1d4a411e2cc4f7fa60da155b298adee8118d63dc1",
    "8dd130ea6a7efb231cc50a36310e4c72e7aa4217d11246ed6c34bcbea78c7bf0",
    "0b72c6642c5731f6961a7e434a0c79c5ba3a89a38a7b50e7f959c9b61582ad1f",
    "a12fac3cc9183da1f09656028643b93f72e415e0edee8598824e11d9ffd2d9a8",
    "74910baeac50bf12b57ae0a7a4d818c5be6830af1df0c51ef8d3da476ec99ae5",
    "69ae5540c6a62baca4e4f4e652f40aa00aef621e103aedc9ecd28f281e06bcec",
    "0adffe2b52619b06e3ffd48b73ade0864c13854107d286ae0e8933e54eae0421"
]
PIN_WINDOW="36d5a9d8487f134207d92f96359defcd7f130a8d049eff84c279823d6b7e2cb5"
PIN_FIRST104="4e6fd646637e2b41caba455015808133f443f0903336792d0fceb33bc348fb6d"

def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def chained(items): return hashlib.sha256("".join(items).encode("ascii")).hexdigest()

def verify(record_path=RECORD,prior_path=RO,rn_path=RN,rk_path=RK,rl_path=RL,rm_path=RM):
    data, prior, rn, rk, rl, rm=(read(z) for z in (record_path,prior_path,rn_path,rk_path,rl_path,rm_path))
    s,v,q=data["source"],data["review"],data["queue"]
    ps=prior["source"]
    if not (data["batch"]=="12RP" and data["stage"]=="12QE_OPEN" and data["parent_open_batch"]=="12QE"
            and data["status"]=="SOURCE_NATIVE_F3_P85_104_BOUNDED_VISUAL_TARGET_SCREEN_WITH_17_REMAINING"
            and s["physical_holding"]==ps["physical_holding"]==rn["source"]["physical_holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==ps["digital_fascicle"]==rn["source"]["digital_fascicle"]==3
            and s["commons_file_id"]==ps["commons_file_id"]=="NLC892-411999003250-383068"
            and s["source_pdf_pages"]==ps["source_pdf_pages"]==121
            and s["source_pdf_sha256"]==ps["source_pdf_sha256"]
            and s["source_pdf_binary_rehashed_in_12rp"] is False
            and s["original_juan7_heading_inherited_from_batch"]==rn["batch"]=="12RN"
            and s["archive_artifact_id"]==ps["archive_artifact_id"]==rn["source"]["archive_artifact_id"]==11673474713
            and s["archive_zip_sha256"]==ps["archive_zip_sha256"]
            and s["archive_status_sha256"]==ps["archive_status_json_sha256"]
            and s["full_121_original_jpeg_ordered_sha256_chain"]==ps["whole_archive_121_jpeg_ordered_sha_chain"]
            and s["source_archive_121_original_jpegs_hashed_against_status"]==121
            and s["source_archive_hash_or_size_mismatches"]==0):
        raise ValueError("12RP_SOURCE_ARCHIVE_IDENTITY_OR_BINARY_EVIDENCE_DRIFT")
    first104=(rk["review"]["original_jpeg_sha256_in_page_order"]
             +rl["review"]["original_jpeg_sha256_in_pdf_order"]
             +rm["review"]["original_image_sha256_ordered"]
             +prior["review"]["original_jpeg_sha256_in_source_page_order"]
             +rn["review"]["source_page_sha256_in_order"]
             +v["original_source_jpeg_sha256_in_order"])
    last20=v["original_source_jpeg_sha256_in_order"]
    if not (len(first104)==104 and len(last20)==20 and last20==PINS
            and v["mode"]=="INDIVIDUAL_ORIGINAL_RESOLUTION_JPEG_BOUNDED_TITLE_PHRASE_AND_JUAN_SCOPE"
            and (v["first_pdf_page"],v["last_pdf_page"],v["individual_original_jpegs_opened"])==(85,104,20)
            and chained(first104[:-20])==prior["review"]["third_fascicle_p1_84_hash_chain_sha256"]
              =="84fa5df27776ce02739bdd60687dff561b58f3c0cc7cd2758e73ddd458bfb1dc"
            and chained(last20)==v["window_ordered_sha256_hash_chain"]==PIN_WINDOW
            and chained(first104)==v["fascicle3_first104_original_jpeg_ordered_hash_chain"]==PIN_FIRST104
            and v["direct_original_juan7_heading_in_source_pdf_p83_left_leaf"]==rn["review"]["source_direct_juan7_heading_text"]
              =="萬曆三十二年甲辰卷七"
            and v["does_not_misattribute_p83_previous_right_leaf_to_juan7"] is True
            and v["new_original_juan8_title_directly_seen"] is False
            and v["original_juan7_assigned_to_reviewed_p85_104"]==
              "CONTEXTUAL_AFTER_DIRECT_P83_JUAN7_HEADING_NOT_EXHAUSTIVE_TEXT_COLLATION"):
        raise ValueError("12RP_104_PAGE_ORDERED_CHAIN_OR_OLD_JUAN_DRIFT")
    false_flags=("old20_gaizao_louke_original_title_or_glyph_attested","ocr_performed",
                 "complete_text_collation_performed","any_page_target_absence_proven",
                 "whole_fascicle_target_absence_proven","whole_old20_work_target_absence_proven",
                 "print1827_30juan_copy_equated")
    if any(v.get(f) is not False for f in false_flags):
        raise ValueError("12RP_FALSE_GLYPH_OR_SOURCE_TEXT_NEGATIVE_CLAIM")
    if v["bounded_original_visual_findings"]!=[
        {"pdf_page":85,"scope":"河运与河工堤坝里程数字，限定视觉观察"},
        {"pdf_page":86,"scope":"山东、天津、广东进税银入内库等原图记载，限定视觉观察"},
        {"pdf_page":92,"scope":"山西广东进银及长陵火灾记载，天灾不等于漏刻目标原文"},
        {"pdf_page":104,"scope":"矿税及内廷治理议论，限定视觉观察"}]:
        raise ValueError("12RP_VISUAL_OBSERVATION_SCOPE_DRIFT")
    pq=prior["queue"]
    if not (q["prior_batch"]==prior["batch"]=="12RO"
            and (q["prior_whole_native_bounded_target_pages"],q["prior_preview_only_source_pages"],
                 q["prior_native_target_backlog"])==
                (pq["new_whole_native_bounded_pages"],pq["new_preview_only_body_pages"],pq["new_native_target_backlog"])==
                (302,726,726)
            and (q["new_whole_native_bounded_target_pages"],q["new_preview_only_source_pages"],q["new_native_target_backlog"])==(322,706,706)
            and q["fascicle3_total_source_pdf_pages"]==121
            and q["fascicle3_native_bounded_target_review_regions"]==[[1,104]]
            and (q["fascicle3_native_bounded_target_screened_pages"],q["fascicle3_pending_native_target_screen_pages"])==(104,17)
            and q["fascicle3_remaining_window"]==[[105,121]]
            and (q["next_fascicle3_page_first"],q["next_fascicle3_page_last"])==(105,121)
            and (q["whole_holding_source_pdf_pages"],q["whole_holding_body_pages"],
                 q["whole_holding_nonbody_prelim_pages"],q["whole_holding_body_firstpass_visual_unscreened"],
                 q["whole_holding_full_text_body_collation_pending"])==(1030,1027,2,0,1027)
            and 322+706+2==1030
            and all(q[k]==0 for k in ("independent_physical_copy_increment","new_direct_stemmatic_copy_edges","algorithm_reopen_count"))
            and data["transmission_impact"]["edges_supported"]==[]
            and data["invariants"]=={"matrix_rows":222,"audited_rows":222,"provenance_repairs":45,
                                   "registered_sources":"647+7=654","md_g03":"OPEN",
                                   "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
                                   "deterministic_product_r1":"CLOSED","algorithm_reopen_count":0}):
        raise ValueError("12RP_PENDING_QUEUE_OR_LINEAGE_INFLATION")
    return {"batch":"12RP","fascicle3_contiguous_native_bounded_reviewed":104,
            "fascicle3_remaining_native_review_pages":17,
            "whole_holding_native_bounded":322,"whole_holding_preview_only":706,
            "whole_holding_fulltext_body_untranscribed":1027,
            "target_old20_gaizao_louke_glyph_or_absence_proof":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
