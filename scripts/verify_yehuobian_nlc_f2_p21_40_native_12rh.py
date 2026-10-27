#!/usr/bin/env python3
"""12RH: first-party archived native JPEG p21–40 checkpoint; no text absence proof."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RH-NLC411999003250-F2-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
RF = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RF-NLC411999003250-F2-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
CHAIN20 = "77f1c4ba8700994e76f89288e481d09411737f03de107c0792c5364c512ea23b"
CHAIN40 = "ace9aa09bea791d1a00e161c6fac6a6786467ebab2fd735947ba011428a5b33f"
PINS = "9de45c98f412053db1d85e2cf2fe735285a4aa0579f16e9c35e30f26d0a43c1e,91cc987b87fb2bf7374d2f58c0212c10bead927925912fbbb07caad14a2d367d,4bcf6d70e42101bcdb85079cabe2c526d9fc307c454bfe00036991dd1dd13425,69eeface7682441957d67f36160b2a6bc9b8ef98769b565883306f31c6609698,badef93b546f325b9cffca6ae0b1c8c82d80375ecf4f7b3915c87dfc648b90af,a6dda8d1360ac04ba33d40c77bde13d8cd9acc7b0c89d59c78769cf1dacca775,a302a6ad21bbd2e5aff239d385f3ddb5711a2e45f6fd955885f31c96ccf1d851,85d399d7ddc87a1b4f00b2dc680d53bd9178254ba86a465a6c3245c9c074a152,3b44a0db76e87bd6710a02eb3eb55a350e2f2c25bed4a47e0357ff76b2a129b1,65a7a845d1c691c99e8f19afd48b1ac18ad70cd0938b4868e4207e3216294805,97d6cc5821a2b2a236012f72615f01d0ce6e1489b255b4a74ce938787b70d6a1,757f9529515c9f88144397566f90826addd8e15d8f8bcfb71a131111a756b391,aaf44448dc73be6b73879283aaa073d737bcf32c57ff4477915717ad11c8bed6,9843f9e15d658c43fb4f0f370973777504ee9650e0f0eb0a69940500d3498c2e,001975e8f9f40d772cf44311c4da6466857c8c5be5ff2ba45fa000788ca5b10b,4477a4cf4a7ca72ac162aa9751d5b3f90e4b882662c5c4a18d984e79cd0d288d,084028e696fe9d25af1119682428d439e314831526d824e8e18588a07e4bbb6a,c8c5aae14eef7d17dd0097e6857cfe85aef764142bbe163b61c3d71aa62388ed,61870535cc8264465aa8e3df9d12a4a669625d024cb3e49f45cea4044cda086a,77d97606d35203a677bd568bed0cb42fc66a3be9cced2dab557909b090723117".split(",")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify(record_path=RECORD, prior_path=RF):
    data, prev = load(record_path), load(prior_path)
    s, v, q = data["source"], data["review"], data["queue"]
    p = prev["source"]
    if not (data["batch"] == "12RH" and data["stage"] == "12QE_OPEN"
            and data["status"] == "FASCICLE2_P21_40_NATIVE_VISUAL_TARGET_BOUNDED_SCREEN_NO_NEGATIVE_TEXT_CLAIM"
            and s["holding"] == p["holding"] == "NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"] == p["digital_fascicle"] == 2
            and s["commons_file_id"] == p["commons_file_id"]
            and s["source_pdf_pages"] == p["source_pdf_pages"] == 72
            and s["source_pdf_sha256"] == p["source_pdf_sha256"]
            and s["source_pdf_binary_rehashed"] is False
            and s["original_pdf_file_downloaded_in_12rh"] is False
            and s["artifact_id"] == p["artifact_id"] == 11673909003
            and s["artifact_zip_sha256"] == p["artifact_zip_sha256"]
            and s["artifact_status_json_sha256"] == p["artifact_status_json_sha256"]
            and s["source_zip_reused_and_hashed_in_12rh"] is True
            and s["source_jpeg_sha256_members_rechecked"] == 72
            and s["source_jpeg_sha256_mismatches"] == 0):
        raise ValueError("12RH_CROSS_BATCH_SOURCE_ARCHIVE_DRIFT")
    hashes = v["original_jpeg_sha256_ordered"]
    prev_hashes = prev["review"]["source_page_sha256_in_pdf_order"]
    digest = lambda seq: hashlib.sha256("".join(seq).encode("ascii")).hexdigest()
    if not (v["mode"] == "INDIVIDUALLY_OPENED_ORIGINAL_RESOLUTION_JPEG_BOUNDED_HEADING_AND_TARGET_PHRASE_VISUAL_SCREEN"
            and (v["pdf_page_first"], v["pdf_page_last"], v["pages_individually_opened"]) == (21, 40, 20)
            and len(hashes) == 20 and hashes == PINS
            and digest(hashes) == v["ordered_hash_chain_sha256"] == CHAIN20
            and len(prev_hashes) == 20
            and prev["review"]["pdf_page_first"] == 1 and prev["review"]["pdf_page_last"] == 20
            and digest(prev_hashes) == prev["review"]["sha256_concatenated_page_hashes"]
            and digest(prev_hashes + hashes) == v["fascicle2_p1_40_combined_chain_sha256"] == CHAIN40
            and v["previous_fascicle2_native_first20_batch"] == prev["batch"] == "12RF"
            and v["fascicle2_original_chronicle_volume"] == 5
            and v["volume_five_heading_inherited_from_fascicle2_page1_not_reobserved_as_new_opening"] is True
            and v["positive_old20_gaizao_louke_heading_or_passage_verified"] is False
            and v["ocr_used"] is False
            and v["complete_text_transcription_performed"] is False
            and v["page_absence_of_target_proven"] is False
            and v["whole_volume_absence_proven"] is False
            and v["whole_manuscript_absence_proven"] is False):
        raise ValueError("12RH_SOURCE_IMAGE_HASH_OR_EVIDENCE_GRADE_DRIFT")
    prior = prev["queue"]
    if not (q["prior_batch"] == "12RF"
            and (q["old_native_source_pages"], q["old_preview_only_body_pages"], q["old_native_body_target_backlog"])
            == (prior["new_native_source_pages"], prior["new_montage_preview_only_source_pages"],
                prior["new_native_body_target_backlog"]) == (166, 862, 862)
            and (q["new_native_source_pages"], q["new_preview_only_body_pages"], q["new_native_body_target_backlog"])
            == (186, 842, 842)
            and (q["fascicle2_total_pages"], q["fascicle2_native_visual_reviewed"],
                 q["fascicle2_native_body_pending"]) == (72, 40, 32)
            and (q["next_page_window_first"], q["next_page_window_last"]) == (41, 60)
            and (q["whole_source_pdf_pages"], q["whole_source_body_pages"],
                 q["frontmatter_nonbody_pages"], q["whole_source_body_firstpass_preview_backlog"],
                 q["whole_source_full_text_body_collation_backlog"]) == (1030, 1027, 2, 0, 1027)
            and q["independent_physical_witness_increment"] == 0
            and q["algorithm_reopen_count"] == 0
            and q["global_negative_target_proof"] is False
            and 186 + 842 + 2 == 1030
            and data["invariants"]["product_r1"] == "CLOSED"
            and data["invariants"]["historical_matrix"] == "222/222"
            and data["invariants"]["repaired_metadata"] == "45/45"
            and data["invariants"]["source_registry"] == "647+7=654"
            and data["invariants"]["md_g03"] == "OPEN"
            and data["invariants"]["hpa_dayun_cal_002"] == "MISSING_FROM_PRODUCT"
            and data["invariants"]["algorithm_reopen_count"] == 0
            and data["transmission_impact"]["edges_supported"] == []):
        raise ValueError("12RH_REVIEW_QUEUE_COUNTER_OR_LINEAGE_PROMOTION")
    return {"batch": "12RH", "fascicle2_native_pages": 40,
            "fascicle2_remaining_native_target_pages": 32,
            "all_native_bounded_pages": 186, "all_preview_only_remaining": 842,
            "full_text_body_collation_remaining": 1027,
            "new_target_glyph_or_text_absence_proof": False}


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
