#!/usr/bin/env python3
"""12RJ: source-scoped F2 final-12 JPEG hash replay, without ancient-text absence inference."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RJ-NLC411999003250-F2-P61-72-NATIVE-SOURCE-REVIEW-R1.json"
RF = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RF-NLC411999003250-F2-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
RH = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RH-NLC411999003250-F2-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
RI = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RI-NLC411999003250-F2-P41-60-NATIVE-SOURCE-REVIEW-R1.json"
PIN_HASHES = [
    "4771ee33c44ec9a0624c9af05dbad346607068756027aee40482913c593d7774",
    "8c22649e039a4dc61d3a29bd96ed438e37a208b740800759ea41714435b4286b",
    "e328b1ee343b046f3eadb01626c1b7dab4268a723673ec307229d074238d9add",
    "54a20fdd9d3dd41059f8aa9f36549499eb2245a8735759f5b33b5137149b5612",
    "48b6488f2bff2cea5d1fdc7c049556f8c0789314b986288b3efadcaa6887e45e",
    "5f2c822da4599447511972f1fd04c486e41dc83574feebbc4c3aad6aa3914d44",
    "f7c2a4231b50c5e16a0a20140debf81c0d0508f86b8070e08baf6d5a1872fcc8",
    "7e1b33014a8eb617f555ee88772f4eead13812195c51bf948dd0a5871d2ed149",
    "a2e72dd1026c978a2dc4af8d6de41bc91db4a0f09e67aed2b8b5eac5e125d10e",
    "60e4958d4d07dbd7d0dae4e0b53c3404113552bcb5822769320681a597c50e63",
    "d7500b1d44c842f37373dd61dcf02168ce5ca528fbcea744b75121500eddf045",
    "77731ecd90e28018ef93bba0ac564232daf9c1074ccc1570a6e9e7032de335a4"
]
PIN_WINDOW_SHA256 = "d3244208dd2d2ae5499e395ecb9bbe0b9d4f11b59346d432a56fd67c4ed89a69"
PIN_ALL72_SHA256 = "522bbc07c36b5f95f1d8fd427368d233cb3b336a278ad85a418021e0fce38890"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def hash_chain(values):
    return hashlib.sha256("".join(values).encode("ascii")).hexdigest()

def verify(record_path=RECORD, first_path=RF, middle_path=RH, third_path=RI):
    obj, first, middle, third = (read(p) for p in (record_path, first_path, middle_path, third_path))
    s, v, q = obj["source"], obj["review"], obj["queue"]
    sources = [first["source"], middle["source"], third["source"]]
    source_keys = ("holding", "digital_fascicle", "commons_file_id", "source_pdf_pages",
                   "source_pdf_sha256", "artifact_id", "artifact_zip_sha256",
                   "artifact_status_json_sha256")
    if not (obj["batch"] == "12RJ" and obj["stage"] == "12QE_OPEN"
            and obj["status"] == "SECOND_FASCICLE_ALL_72_NATIVE_BOUNDED_TARGET_SCREENED_NOT_FULL_TEXT_COLLATION"
            and all(s.get(k) == prev.get(k) for prev in sources for k in source_keys)
            and s["holding"] == "NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"] == 2 and s["source_pdf_pages"] == 72
            and s["artifact_id"] == 11673909003
            and s["source_pdf_binary_rehashed_in_12rj"] is False
            and s["archive_all_72_jpeg_hashes_and_lengths_rechecked"] is True
            and s["archive_jpeg_mismatch_count"] == 0
            and s["one_independent_physical_copy_increment"] == 0):
        raise ValueError("12RJ_SOURCE_ARCHIVE_IDENTITY_OR_GRADE_DRIFT")
    images = v["source_image_sha256_in_pdf_order"]
    images60 = (first["review"]["source_page_sha256_in_pdf_order"]
              + middle["review"]["original_jpeg_sha256_ordered"]
              + third["review"]["source_jpeg_sha256_in_pdf_order"])
    if not (len(images60) == 60
            and first["review"]["pdf_page_first"] == 1 and first["review"]["pdf_page_last"] == 20
            and middle["review"]["pdf_page_first"] == 21 and middle["review"]["pdf_page_last"] == 40
            and third["review"]["first_pdf_page"] == 41 and third["review"]["last_pdf_page"] == 60
            and hash_chain(images60) == third["review"]["sha256_fascicle2_pages1_60_chain"]
            and hash_chain(images60) == "510e26042264f58454ab4cc38e1bf8cb3aaf3314bbe547c52ce5874aa465db8c"
            and len(images) == 12 and images == PIN_HASHES
            and (v["pdf_page_first"], v["pdf_page_last"], v["original_jpegs_separately_opened"]) == (61, 72, 12)
            and v["mode"] == "INDIVIDUALLY_OPENED_ORIGINAL_NATIVE_JPEG_BOUNDED_TARGET_HEADING_OR_PHRASE_VISUAL_SCREEN"
            and hash_chain(images) == v["ordered_source_image_hash_chain_sha256"] == PIN_WINDOW_SHA256
            and hash_chain(images60 + images) == v["fascicle2_p1_72_ordered_source_hash_chain_sha256"] == PIN_ALL72_SHA256
            and v["page_72_original_source_image_sha256"] == images[-1]
            and v["page_72_contains_text_not_blank"] is True):
        raise ValueError("12RJ_JPEG_SOURCE_PAGE_CHAIN_OR_VISUAL_SCOPE_DRIFT")
    false_flags = ("target_old20_gaizao_louke_glyph_or_title_positively_attested",
                  "full_text_transcription_performed", "ocr_performed",
                  "any_page_target_absence_proven", "fascicle2_target_absence_proven",
                  "whole_manuscript_target_absence_proven", "old20_and_1827_30juan_equated")
    if any(v.get(k) is not False for k in false_flags):
        raise ValueError("12RJ_FALSE_GLYPH_TEXT_ABSENCE_OR_COPY_LINEAGE_CLAIM")
    if v["visual_observation_scopes"] != [
        {"pdf_pages": [61, 61], "observation": "税银/奏议文字（限定观察，不是全文翻刻）"},
        {"pdf_pages": [62, 64], "observation": "天象/长星见及官员议论段落（限定观察，尚不可证明与目标漏刻篇章关联）"},
        {"pdf_pages": [65, 72], "observation": "官署、班行与税银段落（限定观察，不能证明不存在漏刻异文）"}]:
        raise ValueError("12RJ_VISUAL_OBSERVATION_SCOPE_DRIFT")
    before = third["queue"]
    if not (q["prior_batch"] == third["batch"] == "12RI"
            and (q["old_whole_source_native_bounded_visual_screens"], q["old_preview_only_target_source_pages"],
                 q["old_native_target_screen_backlog"]) ==
                (before["new_native_source_bounded_screens"], before["new_preview_only_source_pages"],
                 before["new_native_body_target_backlog"]) == (206, 822, 822)
            and (q["new_whole_source_native_bounded_visual_screens"], q["new_preview_only_target_source_pages"],
                 q["new_native_target_screen_backlog"]) == (218, 810, 810)
            and (q["fascicle2_source_pages"], q["fascicle2_native_target_visually_screened"],
                 q["fascicle2_native_target_screen_pending"]) == (72, 72, 0)
            and q["upcoming_original_fascicle3_pdf_page_first"] == 1
            and (q["whole_source_pdf_pages"], q["whole_source_body_pages"],
                 q["frontmatter_nonbody_prelim_pages"], q["whole_body_firstpass_unreviewed_pages"],
                 q["whole_body_full_text_collation_pending"]) == (1030, 1027, 2, 0, 1027)
            and q["new_independent_physical_witnesses"] == 0
            and q["new_glyph_evidence"] == 0 and q["algorithm_reopen_count"] == 0
            and 218 + 810 + 2 == 1030
            and obj["transmission_impact"]["edges_supported"] == []
            and obj["invariants"]["matrix_rows"] == obj["invariants"]["matrix_audited_rows"] == 222
            and obj["invariants"]["provenance_metadata_defects_repaired"] == 45
            and obj["invariants"]["external_sources"] == "647+7=654"
            and obj["invariants"]["md_g03"] == "OPEN"
            and obj["invariants"]["hpa_dayun_cal_002"] == "MISSING_FROM_PRODUCT"
            and obj["invariants"]["product_r1"] == "CLOSED"
            and obj["invariants"]["algorithm_reopen_count"] == 0):
        raise ValueError("12RJ_REVIEW_QUEUE_SCOPE_INVARIANT_OR_LINEAGE_DRIFT")
    return {"batch": "12RJ", "native_fascicle2_pages": 72,
            "fascicle2_remaining_native_target_screens": 0,
            "all_native_source_bounded_screens": 218,
            "preview_only_remaining": 810,
            "whole_body_full_text_collation_remaining": 1027,
            "target_glyph_absence_or_algorithm_changes": 0}

if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
