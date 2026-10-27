#!/usr/bin/env python3
"""12RK original NLC old20 F3 first20 native image checksum and research scope gate."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RK-NLC411999003250-F3-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
PREVIOUS=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RJ-NLC411999003250-F2-P61-72-NATIVE-SOURCE-REVIEW-R1.json"
ORIGIN=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS-R1.json"
PIN_HASHES=[
    "2f0597703f7cb5c29a65e47ac28c17a933e2c28da68416573d4afd0fcebe5a42",
    "0784febab1f61f3c7e864889e3e315cfbda988c5e818a5a1a7e2e32087cff79a",
    "8c22a5eb8c716a4c6755079f79da302fe60a7b2afd3d226355fd439dd956bbc8",
    "e454b9aadff94b723a89fb88ba65a8e4533e8d426ac8a8e420c24b1a19b6a61f",
    "226d93dc65be378153bf5d8c3883a16c4113c4f11f15f2a7793e6047fc5ce460",
    "7cd0b9dfa87c1e8a5e378f66b164998ee162893fb258865e32fc7e568f82d2bd",
    "1bf0cd9a2e955bd51bf552c4b7c1a4252ef46a94138265deffdc181577a8dc72",
    "12e3ee791648e14ac145abb22d675f11553e242eca0396630444cb2ae6a21469",
    "3209713ceb22bd46475481242db176705b3e9f6579d16db75e1982187192c1a5",
    "92f0a03fa1768d64ee53237448878323a70425a3f44d313582a6da2be488781a",
    "e5adc9b7321e85afa570fbc83faea789948fb18aa3f1522d196fd4c1a010020a",
    "c598f7d17832b4c83bfafe77a2582e799e3d608d04b1e4f5ad51750f0ed0be9a",
    "0f153a8b7db962377a4a974847872a08f3c2fe7f3419b9dcb214a878e76b2de3",
    "f32d2fde448dbc884527eb4014582902e8d4521d2c63ae62ecd461188a404c72",
    "385670b3637fd716f720d4c801af03f5f4845e365af96f631ba65cabbfc12098",
    "52f82c39368eee1541c77094996eafb74fe945bc4973b1312852752b33a2d1d9",
    "0dad0ca9742b79895352337670b1a3341cc500a3c70d326960f8da72bf60ed40",
    "bb8e37809da771bee2e6822f60c8d21bd2488d448e38dfee9c6b42fbb7faf183",
    "6fe4fde4be31389662b3b43f7b383a0208647a54abfcdd2474c15e263493856a",
    "3798cff1033a6bc5fc97c8d6f118db187b502a8626c58c001c4766dbf13df06a"
]
PIN_CHAIN="c9639302d880faba8f26ee4eb07257999b2fafcf390fdd6cd91fce456acdd680"
PIN_ALL121="9e15a3a0707adda7cd5b319b21d24f7e1df38b64dc35c48034cb92800e1eb769"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verify(record_path=RECORD, previous_path=PREVIOUS, origin_path=ORIGIN):
    data, last, manifest=read(record_path),read(previous_path),read(origin_path)
    source, review, queue=data["source"],data["review"],data["queue"]
    upstream=manifest["sources"][2]
    if not (data["batch"]=="12RK" and data["stage"]=="12QE_OPEN"
            and data["parent_open_batch"]=="12QE"
            and data["status"]=="F3_FIRST20_SOURCE_ORIGINAL_SIZE_BOUNDED_SCREEN_NOT_TEXTUAL_COLLATION"
            and source["holding"]==last["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
            and source["digital_fascicle"]==upstream["fascicle"]==3
            and source["commons_file_id"]=="NLC892-411999003250-383068"
            and source["catalogued_original_juan_candidates"]==upstream["original_volume_candidates"]==[6,7]
            and source["source_pdf_pages"]==upstream["source_pdf_pages"]==121
            and source["source_pdf_sha256"]==upstream["source_pdf_sha256"]
            and source["source_pdf_binary_rehashed_in_12rk"] is False
            and source["actual_pdf_binary_retrieved_in_12rk"] is False
            and source["artifact_id"]==upstream["artifact_id"]==11673474713
            and source["artifact_zip_sha256"]==upstream["zip_sha256"]
            and source["artifact_status_sha256"]==upstream["status_sha256"]
            and source["artifact_full121_ordered_jpeg_hash_chain_sha256"]==upstream["page_sha_chain"]==PIN_ALL121
            and source["artifact_image_members_independently_hashed"]==121
            and source["artifact_image_member_sha_or_size_mismatches"]==0):
        raise ValueError("12RK_F3_SOURCE_ARCHIVE_OR_PHYSICAL_HOLDING_DRIFT")
    images=review["original_jpeg_sha256_in_page_order"]
    if not (review["mode"]=="INDIVIDUALLY_OPENED_NATIVE_JPEG_FOR_BOUNDED_TITLE_AND_TARGET_PHRASE_VISUAL_SEARCH"
            and (review["first_pdf_page"],review["last_pdf_page"],review["native_individual_images_opened"])==(1,20,20)
            and images==PIN_HASHES and len(images)==20
            and hashlib.sha256("".join(images).encode("ascii")).hexdigest()==review["ordered_jpeg_hash_chain_sha256"]==PIN_CHAIN
            and upstream["page_sha_pins"]["1"]==images[0]
            and review["page1_first_leaf_text_bearing_and_opposite_blank"] is True
            and review["page1_does_not_directly_attest_which_original_juan"] is True
            and review["exact_juan_6_to_7_change_boundary_directly_located_in_window"] is False
            and review["no_1827_reedited30juan_volume_identity_inferred"] is True):
        raise ValueError("12RK_NATIVE_IMAGE_SEQUENCE_OR_OLD_JUAN_SCOPE_DRIFT")
    absent_flags=("positive_old20_gaizao_louke_original_title_or_folio_glyph_attested",
                  "ocr_performed","complete_text_collation_performed","any_page_target_absence_proven",
                  "whole_fascicle_target_absence_proven","whole_work_target_absence_proven")
    if any(review.get(key) is not False for key in absent_flags):
        raise ValueError("12RK_FALSE_GLYPH_OR_NEGATIVE_TEXT_CLAIM")
    lastq=last["queue"]
    if not (queue["prior_batch"]==last["batch"]=="12RJ"
            and (queue["old_native_bounded_source_screens"],queue["old_preview_only_source_pages"],
                 queue["old_native_body_target_screen_backlog"])==
                (lastq["new_whole_source_native_bounded_visual_screens"],
                 lastq["new_preview_only_target_source_pages"],
                 lastq["new_native_target_screen_backlog"])==(218,810,810)
            and (queue["new_native_bounded_source_screens"],queue["new_preview_only_source_pages"],
                 queue["new_native_body_target_screen_backlog"])==(238,790,790)
            and (queue["fascicle3_total_source_pdf_pages"],
                 queue["fascicle3_first20_native_bounded_target_visual_screens"],
                 queue["fascicle3_remaining_native_target_screens"])==(121,20,101)
            and (queue["next_fascicle3_window_first"],queue["next_fascicle3_window_last"])==(21,40)
            and (queue["whole_holding_source_pdf_pages"],queue["whole_holding_body_pages"],
                 queue["prelim_nonbody_not_target_screened"],queue["whole_holding_body_firstpass_screen_missing"],
                 queue["whole_holding_full_text_body_collation_pending"])==(1030,1027,2,0,1027)
            and 238+790+2==1030
            and (queue["new_independent_physical_holding_count"],queue["new_glyph_attestation_count"],
                 queue["new_transmission_edges_count"],queue["algorithm_reopen_count"])==(0,0,0,0)
            and data["transmission_impact"]["edges_supported"]==[]
            and data["invariants"]["matrix_rows"]==data["invariants"]["matrix_audited"]==222
            and data["invariants"]["metadata_repairs_confirmed"]==data["invariants"]["metadata_repairs_completed"]==45
            and data["invariants"]["external_sources"]=="647+7=654"
            and data["invariants"]["md_g03"]=="OPEN"
            and data["invariants"]["hpa_dayun_cal_002"]=="MISSING_FROM_PRODUCT"
            and data["invariants"]["deterministic_product_r1"]=="CLOSED"
            and data["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("12RK_REVIEW_QUEUE_OR_STEMMATIC_INFLATION")
    return {"batch":"12RK","native_page_screened_in_f3":20,
            "fascicle3_native_screen_pending":101,
            "whole_source_native_screened":238,
            "whole_source_preview_only_pending":790,
            "whole_body_full_text_collation_pending":1027,
            "positive_target_glyph_or_wholetext_absence_proofs":0}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
