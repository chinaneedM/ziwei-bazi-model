#!/usr/bin/env python3
"""12RM exact native F3 source-page image sha chain replay and no-absence-proof gate."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RM-NLC411999003250-F3-P41-60-NATIVE-SOURCE-REVIEW-R1.json"
RK=ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RK-NLC411999003250-F3-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
RL=ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RL-NLC411999003250-F3-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
PINS=[
    "d4729f24f3c58d6ea5a7347d3c2ceeac7fd0d033ca31b76dbcff93d002e5e7bf",
    "f599a352cc263d570b44ae7e8d60e77a59fcaf39617297cb1bccd482d45d2815",
    "0e82150a0f36db35cd91a26510e710096752be746daac7c060aa5dd6a4033577",
    "b0ed897c2a9391a3cf74db32ed5e22bd3c49d7dca3cc519522dd58d531a74cbb",
    "62e6c0a8a2c0f4b2d481aa5cbb5d962c56d14f4b56a95a0e9343cf607f1a5738",
    "737b2d0ed07902a00572b698d367585194098b0e083224a134eee126dec89c58",
    "6ca40a3678955b3e0e59aadb147da4643fba05115cf3c2b58154f4b6d30ba6e2",
    "645677d02bae2ef29551f3c016029c2994586b21f5bb0ba6d066b2e7ce6bd6ad",
    "48bfb43e02c35fb9413e52f47477fc2d68280bf401392e1844a84f763f9d4c36",
    "4bdc9deeca18d41190e78a538b82539aa94ab769cb1e9b93ce7e7e2b88a3cafb",
    "4105a788b5887e740a65c33225176d18ca3fe5400105ba0b5c411dde32dae201",
    "f6bb28b02725de30bf86c964645bdc0dfb55a98a37e1f1cc30a3a5850ef29617",
    "dcc4b4c5aac0568e6530ca5204a192e2350de66eb1d702d8f574ee0b96bd5a5b",
    "2a139d1672f4f044fd83331ce30991d1a407b9c7ae1142cec4058ac1a2bf1571",
    "54490bdb322a57e34f8007460135e88a6763d5a58b48c6612baa7d795f18b4c8",
    "bd6911b47135693776914266eb81b4534674070c838a8b1c70ab6d682b0042f8",
    "79b26d8bcc18218571d4470a720cd2ca2a8a5eabfbb08d03ec4878a20b6dc560",
    "25a1ae4db6429b31daf102af742f583a1029d2e04d4aef2884db9a3def5acb35",
    "e2ecbeb6f9357c5dd81af1b1b5a949655bff468075e3919ff93b865dfffdcbc2",
    "7ac97cb708b8bca15de2d72b6042d0e1a06ffebd70af7efab30f8488893b23f8"
]
CHAIN20="8dde8af8eaf0f351d03eb76070f47c6b03cf1a4175992fab7d49078c455e3c67"
CHAIN60="236fe23566ab7868eab7542aa87e76da6b9f3664cb3fbe4c0a330487a381d8f2"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def chain(hashes):
    return hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()

def verify(record_path=RECORD, rl_path=RL, rk_path=RK):
    obj, rl, rk=read(record_path),read(rl_path),read(rk_path)
    s, v, q=obj["source"],obj["review"],obj["queue"]
    prior=rl["source"]
    assert_fields=("holding","digital_fascicle","commons_file_id","source_pdf_pages","source_pdf_sha256",
                   "artifact_id","artifact_zip_sha256")
    if not (obj["batch"]=="12RM" and obj["stage"]==obj["parent_open_batch"]=="12QE_OPEN"
            and obj["status"]=="THIRD_FASCICLE_FIRST60_NATIVE_BOUNDED_SCREEN_NOT_FULLTEXT_OR_NEGATIVE_WORK_PROOF"
            and all(s[k]==prior[k]==rk["source"][k] for k in assert_fields)
            and s["holding"]=="NLC411999003250_ONE_HOLDING" and s["digital_fascicle"]==3
            and s["source_pdf_pages"]==121
            and s["catalogue_original_juan_candidates"]==rl["source"]["original_juan_candidates"]==[6,7]
            and s["source_pdf_binary_rehashed"] is False
            and s["artifact_id"]==11673474713
            and s["artifact_status_json_sha256"]==prior["artifact_status_json_sha256"]==rk["source"]["artifact_status_sha256"]
            and s["artifact_native_jpeg_members_hashed"]==121
            and s["artifact_image_bytes_or_hash_mismatches"]==0
            and s["artifact_121_ordered_image_hashes_sha256"]==prior["archive_all121_jpeg_sha_chain"]
              ==rk["source"]["artifact_full121_ordered_jpeg_hash_chain_sha256"]):
        raise ValueError("12RM_SOURCE_HOLDING_OR_SOURCE_ARCHIVE_IDENTITY_DRIFT")
    images=v["original_image_sha256_ordered"]
    first=rk["review"]["original_jpeg_sha256_in_page_order"]
    second=rl["review"]["original_jpeg_sha256_in_pdf_order"]
    if not (v["mode"]=="EACH_NATIVE_ORIGINAL_JPEG_OPENED_FOR_BOUNDED_TARGET_HEADING_OR_PHRASE_VISUAL_REVIEW"
            and (v["pdf_page_first"],v["pdf_page_last"],v["each_original_source_jpeg_opened"])==(41,60,20)
            and (rl["review"]["pdf_page_first"],rl["review"]["pdf_page_last"])==(21,40)
            and (rk["review"]["first_pdf_page"],rk["review"]["last_pdf_page"])==(1,20)
            and len(first)==len(second)==len(images)==20 and images==PINS
            and chain(second)==rl["review"]["ordered_page_sha256_concatenation_chain"]
            and chain(first+second)==rl["review"]["fascicle3_p1_40_combined_source_hash_chain"]
               =="fca3d756afc09dc6bc9400abff6f562f35e46001b7dfd4efe6dbb58b140b6597"
            and chain(images)==v["window_20_page_hash_chain_sha256"]==CHAIN20
            and chain(first+second+images)==v["full_fascicle3_first60_ordered_image_chain_sha256"]==CHAIN60
            and v["bounded_original_visual_observations"]==[
                {"pdf_page":41,"observation":"tax silver and 漕运 background text; no original volume-boundary inference"},
                {"pdf_page":54,"observation":"漕運總督李三才 and 天變 passage, not proven original 改造漏刻 target"},
                {"pdf_page":59,"observation":"冬十月 line and tax silver notes, no original juan boundary inferred"}]):
        raise ValueError("12RM_JPEG_ORDERED_CHAIN_OR_VISUAL_SCOPE_DRIFT")
    forbidden=("positive_old20_gaizao_louke_original_glyph_or_leaf_attested",
        "original_juan6_7_transition_directly_verified","ocr_used","full_text_transcribed",
        "proof_target_absent_on_any_page","proof_target_absent_from_fascicle3",
        "proof_target_absent_from_old20_work","claim_same_juan_as_1827_30juan")
    if any(v.get(k) is not False for k in forbidden):
        raise ValueError("12RM_FALSE_ORIGINAL_GLYPH_NEGATIVE_PROOF_OR_VOLUME_EQUIVALENCE")
    before=rl["queue"]
    if not (q["previous_batch"]==rl["batch"]=="12RL"
            and (q["previous_whole_source_native_bounded_pages"],q["previous_preview_only_body_pages"],q["previous_native_target_backlog"])==
                (before["new_whole_source_bounded_native_pages"],before["new_preview_only_body_pages"],
                 before["new_native_target_backlog"])==(258,770,770)
            and (q["new_whole_source_native_bounded_pages"],q["new_preview_only_body_pages"],
                 q["new_native_target_backlog"])==(278,750,750)
            and (q["fascicle3_total_pdf_pages"],q["fascicle3_native_target_screened_pages"],
                 q["fascicle3_remaining_native_target_pages"])==(121,60,61)
            and (q["next_fascicle3_window_first"],q["next_fascicle3_window_last"])==(61,80)
            and (q["whole_source_pdf_page_count"],q["whole_source_body_page_count"],
                 q["nonbody_frontmatter_pages"],q["whole_source_body_firstpass_unseen"],
                 q["whole_source_fulltext_body_collation_pending"])==(1030,1027,2,0,1027)
            and 278+750+2==1030
            and all(q[k]==0 for k in ("new_independent_physical_holding","new_transmission_edges","algorithm_reopen_count"))
            and obj["transmission_impact"]["edges_supported"]==[]
            and obj["invariants"]=={"matrix":"222/222","provenance_defects":"45/45",
                "registered_external_sources":"647+7=654","md_g03":"OPEN",
                "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","deterministic_chart_r1":"CLOSED",
                "algorithm_reopen_count":0}):
        raise ValueError("12RM_REVIEW_BACKLOG_OR_LINEAGE_COUNT_DRIFT")
    return {"batch":"12RM","f3_native_bounded_reviewed":60,"f3_native_backlog":61,
            "all_native_source_pages":278,"preview_only_source_pages":750,
            "untranscribed_fulltext_body_pages":1027,
            "new_original_target_glyph_or_negative_proof":False}

if __name__=="__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
