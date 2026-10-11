#!/usr/bin/env python3
"""12RI: native NLC old20 F2 p41–60 image ledger with non-negative evidence firewalls."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RI-NLC411999003250-F2-P41-60-NATIVE-SOURCE-REVIEW-R1.json"
RH = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RH-NLC411999003250-F2-P21-40-NATIVE-SOURCE-REVIEW-R1.json"
RF = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12RF-NLC411999003250-F2-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
PINS = "2d7c6218899caa97b72bcb912780d6c70b106004a9fce3eb0df5ec8b0b8fbf16,ada78cc1c3408134f8e96afdc2f9ba87da70665b1382fc34f44f139480bc4635,32778cae0c6f436b3313e59315df64424405e94c23e3265f9e7540124738e219,eaf7e8c1e4095c018b9061cec991fd8abc46a8b8d0ec8b9415994f6142a49c42,c344059a4c12fab6e4491e78651a81a91687a36a8235c6b7f5e829dca1c3dc0d,153f6a885fe01825c0b4140fcf0ec80a28b2c606716918cfa5994db55a6096bc,7b061cca46bfd4aa61ed5f86a0fb46acba7623268aa249e0df92608f71a65a45,151e298a9cb45b79dd83d4918cb45f3677622eb0ec2cf38c92426a8fd736d911,0b77ca3732d0e482e43c8c8fbbc6d77c44fa285ffdf5355353ae478cf8a41e51,a1164c9109e10eba74ac394266b66558b6c538ccc8441ab76fbce6a6ce5c7090,7863d933bbac847480842b242d711d5da7612a259466f6bbae19ac23523bcdc4,d637450ce81c2ec8456d62d9563d10862b795615370455f8429229c3f887b021,776c4aef8e84767705a69f7a8fc5dbaa6c466e19f77e92f4782b92fae9b98d91,c88d31030ae78e60fa15afb61c0f305e5f102f13ec191834634929021cb6f3ba,d45133026fae28f375370800692cf3015cfb64e221d9474637b8e0ade59cf38c,5a13b638829feb7c1eb5d1e24986451c07c9249079b995fecf2c9ea60db0aa0e,9907157947d5f5163b047c74efcb4ebe36841c93d24849f68388cf42916fc86f,e04a900857847df270edf779dd44a72752371c28e80bdd9653aacd1214d71011,512f5050de392b0fdae05739e9e5bfce8ab0aceebe95653e5c1b3c8d2f97387c,1610958c40c1c31cab32e54e242678a1661c2491576cb914ec741b48b2fbcd1e".split(",")
CHAIN = "0cea7894ee1fffd063534fcb8b58df0512663472216bd98c6ed3d4e61ae608f4"
FIRST60 = "510e26042264f58454ab4cc38e1bf8cb3aaf3314bbe547c52ce5874aa465db8c"

def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def digest(seq):
    return hashlib.sha256("".join(seq).encode("ascii")).hexdigest()

def verify(record_path=RECORD, previous_path=RH, early_path=RF):
    obj, prev, early = read(record_path), read(previous_path), read(early_path)
    s, v, q = obj["source"], obj["review"], obj["queue"]
    prior = prev["source"]
    if not (obj["batch"]=="12RI" and obj["stage"]=="12QE_OPEN"
            and obj["status"]=="SOURCE_NATIVE_F2_P41_60_BOUNDED_SCREEN_NO_TEXT_ABSENCE_CLAIM"
            and s["holding"]==prior["holding"]==early["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==prior["digital_fascicle"]==early["source"]["digital_fascicle"]==2
            and s["commons_file_id"]==prior["commons_file_id"]==early["source"]["commons_file_id"]
            and s["source_pdf_pages"]==prior["source_pdf_pages"]==72
            and s["source_pdf_sha256"]==prior["source_pdf_sha256"]==early["source"]["source_pdf_sha256"]
            and s["source_pdf_binary_rehashed"] is False
            and s["artifact_id"]==prior["artifact_id"]==early["source"]["artifact_id"]==11673909003
            and s["artifact_zip_sha256"]==prior["artifact_zip_sha256"]
            and s["artifact_status_json_sha256"]==prior["artifact_status_json_sha256"]
            and s["source_zip_rehashed"] is True
            and s["source_original_jpeg_members_rechecked"]==72
            and s["source_image_member_mismatches"]==0):
        raise ValueError("12RI_SOURCE_IDENTITY_OR_BINARY_HASH_DRIFT")
    hashes=v["source_jpeg_sha256_in_pdf_order"]
    prior_hashes=prev["review"]["original_jpeg_sha256_ordered"]
    early_hashes=early["review"]["source_page_sha256_in_pdf_order"]
    if not (v["mode"]=="INDIVIDUAL_NATIVE_ORIGINAL_JPEG_PAGE_BOUNDED_TITLE_TARGET_PHRASE_VISUAL_REVIEW"
            and (v["first_pdf_page"],v["last_pdf_page"],v["pages_individually_opened"])==(41,60,20)
            and hashes==PINS and len(hashes)==20 and digest(hashes)==v["sha256_concatenated_page_hashes"]==CHAIN
            and (prev["review"]["pdf_page_first"],prev["review"]["pdf_page_last"])==(21,40)
            and (early["review"]["pdf_page_first"],early["review"]["pdf_page_last"])==(1,20)
            and len(prior_hashes)==len(early_hashes)==20
            and digest(early_hashes+prior_hashes)==prev["review"]["fascicle2_p1_40_combined_chain_sha256"]
            and digest(early_hashes+prior_hashes+hashes)==v["sha256_fascicle2_pages1_60_chain"]==FIRST60
            and v["fascicle2_original_juan_assigned_from_prior_first_page"]==5
            and v["new_juan_opening_on_pages41_60_claimed"] is False
            and v["positive_gaizao_louke_original_heading_or_glyph_attested"] is False
            and v["ocr_used"] is False
            and v["complete_text_transcription_performed"] is False
            and v["any_scoped_page_absence_proven"] is False
            and v["whole_fascicle_absence_proven"] is False
            and v["whole_manuscript_absence_proven"] is False):
        raise ValueError("12RI_GLYPH_GRADE_HASH_OR_FALSE_ABSENCE_CLAIM")
    upstream=prev["queue"]
    if not (q["upstream_batch"]=="12RH"
            and (q["old_native_source_bounded_screens"],q["old_preview_only_source_pages"],
                 q["old_native_body_target_backlog"])==
                (upstream["new_native_source_pages"],upstream["new_preview_only_body_pages"],
                 upstream["new_native_body_target_backlog"])==(186,842,842)
            and (q["new_native_source_bounded_screens"],q["new_preview_only_source_pages"],
                 q["new_native_body_target_backlog"])==(206,822,822)
            and (q["fascicle2_total_pages"],q["fascicle2_native_target_screens"],
                 q["fascicle2_remaining_native_target_screens"])==(72,60,12)
            and q["next_source_window"]=="f2 p61-72"
            and (q["whole_manuscript_pdf_source_pages"],q["whole_manuscript_body_pages"],
                 q["prelim_frontmatter_not_target_screened"],q["body_never_firstpass_screened"],
                 q["whole_manuscript_full_text_body_collation_backlog"])==(1030,1027,2,0,1027)
            and 206+822+2==1030 and q["new_physical_copy_count"]==0
            and q["new_transmission_edge_count"]==0 and q["global_target_absence_proven"] is False
            and q["algorithm_reopen_count"]==0 and obj["transmission_impact"]["edges_supported"]==[]
            and obj["invariants"]["matrix"]=="222/222"
            and obj["invariants"]["repaired_metadata"]=="45/45"
            and obj["invariants"]["sources"]=="647+7=654"
            and obj["invariants"]["md_g03"]=="OPEN"
            and obj["invariants"]["hpa_dayun_cal_002"]=="MISSING_FROM_PRODUCT"
            and obj["invariants"]["product_r1"]=="CLOSED"
            and obj["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("12RI_NATIVE_REVIEW_QUEUE_OR_LINEAGE_INFLATION")
    return {"batch":"12RI","fascicle2_native_screened":60,
            "fascicle2_native_remaining":12,
            "native_source_bounded_screens":206,"preview_only_remaining":822,
            "whole_body_full_text_collation_remaining":1027,
            "new_target_glyph_or_absence_proof":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
