#!/usr/bin/env python3
"""12RO replay F3 p61-80 exact native JPEG checksums, contiguous F3 p1-84 and source-grade limitations."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RO-NLC411999003250-F3-P61-80-NATIVE-SOURCE-REVIEW-R1.json"
RM=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RM-NLC411999003250-F3-P41-60-NATIVE-SOURCE-REVIEW-R1.json"
RL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RL-NLC411999003250-F3-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
RK=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RK-NLC411999003250-F3-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
RN=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RN-NLC411999003250-F3-P81-84-ORIGINAL-JUAN7-MIXED-LEAF-R1.json"
PINS=[
    "bdb111b60e84c88b44bde9ad5709b3fea5a5a4e62059876385eff5c689b4d063",
    "e75d744c436036898ff05b888f0981c5471443605d35dbdc629a16b8f52e804d",
    "0e1678625c31e6dc81618b9bc8b5bcf7944b5907babb06a11782f1fdb8566867",
    "59706f786dba10821dfa07465db7d4738e2f524085ac49eff162f89c5c3caa40",
    "55dc76f205e9666f9b15feda1951878a21126b1ad0448907dd004b65b7fce0c3",
    "b17f9cd44d6cac9b324d97308b91ad69b21071f84aff47f591b27e95405e2059",
    "adc17d94d45f63469049704394ce90e050bf27ba1e6e6dcc9196841321b08705",
    "b0989079f5e3df9435cf1df6a4a99a59936b0c6b0fdf90b8bc1cdc3694a90da1",
    "a27c6362ff41beec3bc528714b41da30acbb2f6de7ea1ea615c2f5338ee16914",
    "30f30424208fd8a6f52d5be08a2b84dfb12e087f5c046fc1b0cc9468ad60f081",
    "1e61571f4bdb38ee3c886c5a208f776eb6f831b769d59874ca839aeec720fa98",
    "c4c3aebc8afa459c2e7b3f0e176a2ead96500d3330bb579c4d29159e68c70c72",
    "07cf930ff737ff9e76d91f8a94799834bb3d2ae173fc90e2e5534a609544aeac",
    "14141a0706bfe70b5ea9f0b01bf88b3a9cd1fc052c70fd1c0ed6fe430f930721",
    "08cef770b9aa2ff2ab2fbcc2501346412678a52ad17a13484921ce6ae5894e3c",
    "8fe71318f36cad45bf0803995e70acaddb9a15e6a5b50741eb6e2e822402830a",
    "444736719c61802a9de2173f1dbd54f516421099f6092113b1b9f9a976178e7a",
    "62d1421608b5bdad167aa1971ce319bb6e5de0bcffbecae2e6cc2cdc8707cfb3",
    "65eb70f7da5760c65012def1ccd2da25dc24f71c25e853a9cdbfceea6622978f",
    "e09d61fc0c8e4405d0da5e15368fdd8226653b7f2d761f4041d31636778e1a70"
]
CHAIN20="551b0a1e6298e49c4af2145adffd374b36b2d1c834604c5b8b60fa53de814551"
CHAIN80="636e3771e457019bf5c5359c01ef088eaade5b6892332b6343d3331e208ae96a"
CHAIN84="84fa5df27776ce02739bdd60687dff561b58f3c0cc7cd2758e73ddd458bfb1dc"

def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def chain(values): return hashlib.sha256("".join(values).encode("ascii")).hexdigest()

def verify(record_path=RECORD,rm_path=RM,rn_path=RN,rk_path=RK,rl_path=RL):
    obj, rm, rn, rk, rl=(read(p) for p in (record_path,rm_path,rn_path,rk_path,rl_path))
    s,v,q=obj["source"],obj["review"],obj["queue"]
    prev=rn["source"]
    if not (obj["batch"]=="12RO" and obj["stage"]==obj["parent_open_batch"]=="12QE_OPEN"
            and obj["status"]=="SOURCE_NATIVE_F3_P61_80_TARGET_BOUNDED_SCREEN_CONTIGUOUS_P1_84_NOT_FULLTEXT"
            and s["physical_holding"]==prev["physical_holding"]==rm["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==prev["digital_fascicle"]==rm["source"]["digital_fascicle"]==3
            and s["commons_file_id"]==prev["commons_file_id"]==rm["source"]["commons_file_id"]
            and s["source_pdf_pages"]==prev["source_pdf_pages"]==rm["source"]["source_pdf_pages"]==121
            and s["original_juan_candidates"]==[6,7]
            and s["source_pdf_sha256"]==prev["source_pdf_sha256"]==rm["source"]["source_pdf_sha256"]
            and s["source_pdf_binary_rehashed_in_12ro"] is False
            and s["archive_artifact_id"]==prev["archive_artifact_id"]==rm["source"]["artifact_id"]==11673474713
            and s["archive_zip_sha256"]==prev["archive_zip_sha256"]==rm["source"]["artifact_zip_sha256"]
            and s["archive_status_json_sha256"]==prev["archive_status_json_sha256"]==rm["source"]["artifact_status_json_sha256"]
            and s["whole_archive_121_jpeg_ordered_sha_chain"]==prev["archive_121_ordered_page_hash_chain"]
            and s["archive_jpeg_members_rehashed_against_status"]==121
            and s["archive_image_sha256_and_byte_size_mismatches"]==0):
        raise ValueError("12RO_SOURCE_HOLDING_ARCHIVE_AND_BINARY_GRADE_DRIFT")
    h=v["original_jpeg_sha256_in_source_page_order"]
    first=rk["review"]["original_jpeg_sha256_in_page_order"]
    second=rl["review"]["original_jpeg_sha256_in_pdf_order"]
    third=rm["review"]["original_image_sha256_ordered"]
    four=rn["review"]["source_page_sha256_in_order"]
    first60=first+second+third
    if not (v["mode"]=="INDIVIDUAL_ORIGINAL_RESOLUTION_JPEG_BOUNDED_TARGET_HEADING_AND_PHRASE_SCREEN"
            and (v["pdf_page_first"],v["pdf_page_last"],v["each_original_native_jpeg_opened"])==(61,80,20)
            and len(first)==len(second)==len(third)==len(h)==20 and len(four)==4
            and h==PINS and chain(h)==v["window_hash_chain_sha256"]==CHAIN20
            and chain(first60)==rm["review"]["full_fascicle3_first60_ordered_image_chain_sha256"]=="236fe23566ab7868eab7542aa87e76da6b9f3664cb3fbe4c0a330487a381d8f2"
            and chain(first60+h)==v["third_fascicle_p1_80_hash_chain_sha256"]==CHAIN80
            and chain(four)==rn["review"]["sha256_concatenated_page_sha256"]=="fb01d6eeb00e53c5e6cbfeb654d1b0580a9fca16c94e197a74b0d48dccf6a3ee"
            and chain(first60+h+four)==v["third_fascicle_p1_84_hash_chain_sha256"]==CHAIN84
            and four[2]==rn["review"]["mixed_page_original_jpeg_sha256"]
            and v["first80_all_original_native_bounded_visually_reviewed"] is True
            and v["page81_84_direct_source_review_inherited_from"]==rn["batch"]=="12RN"
            and v["page83_left_leaf_direct_juan7_heading"]==rn["review"]["source_direct_juan7_heading_text"]=="萬曆三十二年甲辰卷七"
            and v["page83_right_leaf_direct_juan6_heading_attested"] is False
            and v["page83_whole_page_exclusively_juan7"] is False
            and v["page80_original_juan7_heading_directly_attested"] is False
            and v["page80_previous_juan_continuity_contextual_not_fulltext"] is False):
        raise ValueError("12RO_ORDERED_JPEG_HASH_OR_MIXED_JUAN_LEAF_DRIFT")
    forbidden=("old20_gaizao_louke_original_heading_or_glyph_attested","ocr_used",
                "complete_linewise_text_transcription","any_page_target_absence_proven",
                "fascicle3_target_absence_proven","entire_old20_manuscript_target_absence_proven",
                "modern_1827_edition_original_juan_equivalence_proven")
    if any(v.get(k) is not False for k in forbidden):
        raise ValueError("12RO_FALSE_TARGET_GLYPH_TEXT_ABSENCE_OR_STEMMATIC_CLAIM")
    if v["bounded_visual_observations"]!=[
        {"pdf_pages":[61,65],"observation":"矿监税务、官署及地方事件记载，可见奏议片段；限定视觉核读"},
        {"pdf_pages":[66,75],"observation":"妖书案、宫禁与厂卫/刑部议论，p70-75多见锦衣卫、九卿奏议；限定视觉核读"},
        {"pdf_pages":[76,80],"observation":"圣谕、太子、九卿奏议及刻字事状；p80为原卷七题目前的连续史事文字"}]:
        raise ValueError("12RO_VISUAL_SCOPE_DRIFT")
    prevq=rn["queue"]
    if not (q["upstream_batch"]==rn["batch"]=="12RN"
            and (q["prior_whole_native_bounded_pages"],q["prior_preview_only_body_pages"],q["prior_native_target_backlog"])==
                (prevq["new_native_bounded_source_pages"],prevq["new_preview_only_source_pages"],prevq["new_native_target_backlog"])==(282,746,746)
            and (q["new_whole_native_bounded_pages"],q["new_preview_only_body_pages"],q["new_native_target_backlog"])==(302,726,726)
            and q["fascicle3_source_pdf_pages"]==121
            and q["fascicle3_native_bounded_target_regions"]==[[1,84]]
            and (q["fascicle3_native_bounded_target_reviewed"],q["fascicle3_native_target_pending"])==(84,37)
            and q["fascicle3_remaining_window"]==[[85,121]]
            and (q["next_window_first"],q["next_window_last"])==(85,104)
            and (q["whole_source_pdf_pages"],q["whole_source_body_pages"],q["nonbody_prelim_pages_not_target_screened"],
                 q["whole_source_body_firstpass_unseen"],q["whole_source_body_fulltext_collation_pending"])==(1030,1027,2,0,1027)
            and 302+726+2==1030
            and all(q[k]==0 for k in ("new_independent_physical_holding_count",
                "new_stemmatic_direct_copy_edges_count","chart_algorithm_reopen_count"))
            and obj["transmission_impact"]["edges_supported"]==[]
            and obj["invariants"]=={"historical_matrix_rows":222,"historical_matrix_audited":222,
                "provenance_metadata_repaired":45,"source_registry":"647+7=654","md_g03":"OPEN",
                "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","deterministic_chart_r1":"CLOSED",
                "algorithm_reopen_count":0}):
        raise ValueError("12RO_NATIVE_SCREEN_ACCOUNTING_OR_LINEAGE_DRIFT")
    return {"batch":"12RO","f3_contiguous_native_screened":84,"f3_remaining":37,
            "whole_holding_native_bounded":302,"whole_holding_preview_only":726,
            "whole_holding_fulltext_body_untranscribed":1027,
            "old20_target_glyph_or_negative_text_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
