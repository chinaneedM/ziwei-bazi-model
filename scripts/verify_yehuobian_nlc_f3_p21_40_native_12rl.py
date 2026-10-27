#!/usr/bin/env python3
"""12RL original fascicle3 p21-40 verification: SHA-chain and evidence-scope replay."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RL-NLC411999003250-F3-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
RK = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RK-NLC411999003250-F3-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
ORIGIN = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS-R1.json"
PINS = [
    "9f4c53652505e4b800abaa7acb0c68c04ebc6bae3c4d5edcd51a955d13992f1d",
    "676b49403ad253fa34f13529ea9749d5fa591e2469bb6028ad5a9fb541ee8633",
    "7a8c0aea38d6f63df58bd632a6218a0f784ae9b6bea1def059a2935d85bdea9f",
    "9380d99dd23146a8b2266db816fb7934b4f1f1efe7f65f59628e7330aedf859e",
    "f4c0bfda08c1d2de0633c11b011b638f6c44bc449941f9a5727b3c07bc73c251",
    "2471d9a3460d762971646de57ba417340ca564b5ba42a750b9c979abebcf8a8f",
    "49c7d102dfba1cddbfe3c4234c468e04f9c06a289de000eff89670a98fb5fbc4",
    "4a23ddf0959fd376e911df42b9bc4881b40363b3e4d2d74da5f8c5af3ffa7002",
    "01d776bb9316ad3a7fa399f3c2b285a4ecc668eba1e97b21f20052b5972eefcf",
    "20400e801e9fd9146236f4be6f7c5a50d63d5f7cbad8c2971f6c1c606be5b2b3",
    "7b9e0087968049c74ad52a7a9f957b89afb7aaca5b3ed4bc6ee62370d61e3925",
    "68db74b8f04581564aa939e618c4b3d71655adb4ec66453b0c42835d98bd949b",
    "b2fc44cda1d321feb8783ca06ab11733c057a1a0e85789b89eaab9e17de51f8b",
    "f8e7d2653f1e17a488662b9fedf07e394bf59c1a3ee39de714458eab7689f137",
    "fe7698d547126550d30d45daaddc8c76322c92d45367b6bbd56257ce9f27a7e1",
    "f0ad622764db507dd4a7dccc4d21e58534476ee5fae6194c31ff3157578dc6e1",
    "881290a44bd32f031ff70a630bd02023b614ed5278b6a518562abaf56d09ac46",
    "353097da1dd19292ab3cf219b9abfdc1c0c979c02fd8dc72299d9925e4487539",
    "f1a69ec4d3630cb3b07d08a9f192ba8ed7ab04d9b4f5562b418374b93a60641c",
    "c039866fad63a9167ddac1db4afe98b95f2fa79b9dcaed987a7a68f13eb5738f"
]
CHAIN20 = "5f417983ca7ae816403c66390ce08cb0f44735dee38e0cc221b11192efdcc8a3"
CHAIN40 = "fca3d756afc09dc6bc9400abff6f562f35e46001b7dfd4efe6dbb58b140b6597"
CHAIN121 = "9e15a3a0707adda7cd5b319b21d24f7e1df38b64dc35c48034cb92800e1eb769"

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def sha_order(hashes):
    return hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()

def verify(record_path=RECORD, prior_path=RK, origin_path=ORIGIN):
    obj, prior, atlas = read(record_path), read(prior_path), read(origin_path)
    source, review, queue = obj["source"], obj["review"], obj["queue"]
    ps, pr, pq = prior["source"], prior["review"], prior["queue"]
    atlas3 = atlas["sources"][2]
    if not (obj["batch"] == "12RL" and obj["stage"]=="12QE_OPEN" and obj["parent_open_batch"]=="12QE"
            and obj["status"] == "THIRD_DIGITAL_FASCICLE_P21_40_NATIVE_BOUNDED_HEADING_SCREEN_NO_TEXT_ABSENCE_PROOF"
            and source["holding"] == ps["holding"] == "NLC411999003250_ONE_HOLDING"
            and source["digital_fascicle"] == ps["digital_fascicle"] == atlas3["fascicle"] == 3
            and source["commons_file_id"] == ps["commons_file_id"] == "NLC892-411999003250-383068"
            and source["source_pdf_pages"] == ps["source_pdf_pages"] == atlas3["source_pdf_pages"] == 121
            and source["source_pdf_sha256"] == ps["source_pdf_sha256"] == atlas3["source_pdf_sha256"]
            and source["source_pdf_binary_rehashed_in_12rl"] is False
            and source["artifact_id"] == ps["artifact_id"] == atlas3["artifact_id"] == 11673474713
            and source["artifact_zip_sha256"] == ps["artifact_zip_sha256"] == atlas3["zip_sha256"]
            and source["artifact_status_json_sha256"] == ps["artifact_status_sha256"] == atlas3["status_sha256"]
            and source["archive_all121_jpeg_sha_chain"] == ps["artifact_full121_ordered_jpeg_hash_chain_sha256"] == CHAIN121
            and source["artifact_page_jpegs_independently_hashed"] == 121
            and source["artifact_page_sha_or_size_mismatches"] == 0
            and source["original_juan_candidates"] == ps["catalogued_original_juan_candidates"] == [6, 7]
            and source["new_physical_holding_count"] == 0):
        raise ValueError("12RL_SOURCE_ARCHIVE_OR_CATALOGUE_JUAN_DRIFT")
    images = review["original_jpeg_sha256_in_pdf_order"]
    first20 = pr["original_jpeg_sha256_in_page_order"]
    if not (review["mode"] == "NATIVE_ORIGINAL_JPEG_INDIVIDUAL_BOUNDED_HEADING_AND_PHRASE_VISUAL_SCREEN"
            and (review["pdf_page_first"], review["pdf_page_last"], review["original_jpegs_individually_opened"]) == (21, 40, 20)
            and (pr["first_pdf_page"], pr["last_pdf_page"]) == (1, 20)
            and len(first20) == len(images) == 20
            and images == PINS
            and sha_order(first20) == pr["ordered_jpeg_hash_chain_sha256"] == "c9639302d880faba8f26ee4eb07257999b2fafcf390fdd6cd91fce456acdd680"
            and sha_order(images) == review["ordered_page_sha256_concatenation_chain"] == CHAIN20
            and sha_order(first20 + images) == review["fascicle3_p1_40_combined_source_hash_chain"] == CHAIN40
            and review["bounded_original_observations"] == [
                {"pdf_page": 23, "observation": "original leaf shows 六月 marker and fiscal/Chu-domain notes; no era or original juan transition inferred"},
                {"pdf_page": 35, "observation": "original leaf shows 八月 marker and 河水 passage; not direct folio evidence for target 改造漏刻"},
                {"pdf_page": 40, "observation": "original leaf shows tax-silver notes, not an original volume-opening identity proof"}]):
        raise ValueError("12RL_NATIVE_IMAGE_ORDER_OR_VISUAL_OBSERVATION_DRIFT")
    forbidden = ("positive_original_old20_gaizao_louke_heading_glyph_or_leaf_attested",
                 "original_juan6_7_boundary_directly_identified_in_window", "ocr_performed",
                 "full_text_page_by_page_collation_performed", "any_scoped_page_target_absence_proven",
                 "whole_fascicle_target_absence_proven", "whole_work_target_absence_proven",
                 "catalogue_volume_candidates_promoted_to_leaf_assignment",
                 "restructured_1827_edition_identified_as_same_juan")
    if any(review.get(key) is not False for key in forbidden):
        raise ValueError("12RL_FALSE_GLYPH_ABSENCE_OR_EDITION_EQUIVALENCE_PROMOTION")
    if not (queue["previous_batch"] == prior["batch"] == "12RK"
            and (queue["prior_whole_source_bounded_native_pages"], queue["prior_preview_only_body_pages"],
                 queue["prior_native_target_backlog"]) ==
                (pq["new_native_bounded_source_screens"], pq["new_preview_only_source_pages"],
                 pq["new_native_body_target_screen_backlog"]) == (238, 790, 790)
            and (queue["new_whole_source_bounded_native_pages"], queue["new_preview_only_body_pages"],
                 queue["new_native_target_backlog"]) == (258, 770, 770)
            and (queue["fascicle3_source_pages"], queue["fascicle3_native_visual_target_screened"],
                 queue["fascicle3_native_visual_target_pending"]) == (121, 40, 81)
            and (queue["next_fascicle3_page_window_first"], queue["next_fascicle3_page_window_last"]) == (41, 60)
            and (queue["whole_holding_source_pages"], queue["whole_holding_body_pages"],
                 queue["whole_holding_nonbody_frontmatter_pages"], queue["whole_holding_body_firstpass_unscreened"],
                 queue["whole_holding_full_text_collation_pending"]) == (1030, 1027, 2, 0, 1027)
            and 258 + 770 + 2 == 1030
            and all(queue[k] == 0 for k in ("independent_copy_increment", "transmission_edge_increment",
                                            "glyph_authority_increment", "algorithm_reopen_count"))
            and obj["transmission_impact"]["edges_supported"] == []
            and obj["invariants"] == {"matrix": "222/222", "metadata_repairs": "45/45",
                                       "sources": "647+7=654", "md_g03": "OPEN",
                                       "hpa_dayun_cal_002": "MISSING_FROM_PRODUCT",
                                       "deterministic_product_r1": "CLOSED",
                                       "algorithm_reopen_count": 0}):
        raise ValueError("12RL_NATIVE_PAGE_QUEUE_OR_LINEAGE_INFLATION")
    return {"batch": "12RL", "f3_native_bounded_pages": 40, "f3_remaining": 81,
            "whole_native_bounded_pages": 258, "whole_preview_only_pages": 770,
            "whole_fulltext_body_pending": 1027, "new_target_glyph_attested": False,
            "target_absence_proven": False}

if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
