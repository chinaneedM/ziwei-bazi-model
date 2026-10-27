#!/usr/bin/env python3
"""12RF: bound 20 directly viewed NLC fascicle-2 pages to their original-source evidence."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RF-NLC411999003250-F2-P1-20-NATIVE-SOURCE-REVIEW-R1.json"
QY=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS-R1.json"
RE=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RE-NLC411999003250-F1-CROSSBATCH-NATIVE-RECONCILIATION-R1.json"
SOURCE_PAGE_SHA256="8fa105b74efe109a08140286c96a8215f049a62d0b1cf587e7e3e5afdb559d57"
ZIP_SHA256="14015f5e788190a9b9839450fd8be45cea318e29bf7e00848e3f9f1abbe27f18"
STATUS_SHA256="5e6cd6b54df24dbde59d4cdaffdf279173e886ea15016e2bd0dca5cf68ffa470"
CHAIN_SHA256="5d82cf5f62f025bcf2bd088255d92db81af0a5e4c369d4143b9555baa0e3731c"
PINS="cba46966ef615d3d27817272e9987d8e236d05eb0fb0fd7d7f6fd9da0d1f18ff,86b0a592028b8cbce548036305e5564ae0e8364f49e3d06e03bced2a50b2b16f,8405a108c86c2412988913b4239c67915d796d961b2cc0fd0be0937d56b89ba1,92d44423befa7ce4e579955a6414099b3eb63e55a97777a5070cccd20172d20c,69ee1a2daafc6d1ee4edef2af57d749ffea5a493c62ede9858b68a42dea096bb,041720e0418d37ce616e5e05799f97032eca03f984489b1bb870e5832c7e85df,f33694691e66daab834c3f593e8fe5403f643366f1998ac20b382bb4bfc97b58,e7f3a834b7ae8a71ec8fb6c76c67a4a54ad2e07c8cbe8215c9dac01c93a18edb,7cb32717f4f1839fa68c71d0105a7b3072ac96e3a5906e62571e8b81924d1bc4,8ddae8a25b190f2aba34f05ff9beacb90176d7d0bf6333d9fdad693eddc4f05c,a36b61aa2f33d5ed648593bc1457f8a73b4d23d89f046b79c141d2984afa779a,4146a980a11283a3bc394cbed55a55848f2fafc205bf839685e45cd2ec077909,b14b6bb8cb4bdb1ef261dc6bd113775a23c3b0c87863757e31df5abf7788b15e,27852756af6366d8048d105912adfbd27089371fd4e5aa41cc90e4f17ead1afa,ccc81ac526f207fce75725cd151fe075ec6e1d69ef5e24598f55c2c00a6eec3e,28bd10eef63409230a30d5d42fe9dd0748974201ecb2a92ed5b9b4a501402fc4,e89fad5e79ddd5a4b725bca84485f9dcbb8e5ff7777fd6ceb7dc53ccf71cbf17,273bf6f019bd7a5f8cbdb677d30abbdcc0ccd89c63fb1c3f67f7815483222701,623698199ac04b5e67b4ae28aec1478f23aed1194299361f5067ee4bd933bb33,17bba79cfadef41d261fbe46cc49359ba2d8f37b95ba3f16b856b097715259ad".split(",")

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verify(record_path=RECORD,qy_path=QY,re_path=RE):
    value,qy,re=load(record_path),load(qy_path),load(re_path)
    s,v,q=value["source"],value["review"],value["queue"]
    prior=qy["sources"][1]
    if not (value["batch"]=="12RF" and value["stage"]=="12QE_OPEN"
            and value["status"]=="SCOPED_ORIGINAL_NATIVE_PAGES_1_20_SCREENED_NO_WHOLE_TEXT_NEGATIVE"
            and s["holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==prior["fascicle"]==2
            and s["commons_file_id"]=="NLC892-411999003250-383064"
            and s["source_pdf_pages"]==prior["source_pdf_pages"]==72
            and s["source_pdf_sha256"]==prior["source_pdf_sha256"]==SOURCE_PAGE_SHA256
            and s["artifact_id"]==prior["artifact_id"]==11673909003
            and s["artifact_zip_sha256"]==prior["zip_sha256"]==ZIP_SHA256
            and s["artifact_status_json_sha256"]==prior["status_sha256"]==STATUS_SHA256
            and s["source_pdf_binary_rehashed"] is False
            and s["artifact_zip_and_status_rehashed"] is True
            and s["artifact_page_members_independently_rehashed"]==72
            and s["artifact_page_members_hash_mismatches"]==0
            and prior["verified_original_jpegs"]==72
            and prior["body_preview_pages"]==72):
        raise ValueError("12RF_SOURCE_IDENTITY_ARCHIVE_DRIFT")
    hashes=v["source_page_sha256_in_pdf_order"]
    if not (v["mode"]=="INDIVIDUAL_ORIGINAL_SOURCE_JPEG_NATIVE_SIZE_BOUNDED_TITLE_TARGET_PHRASE_VISUAL_SCREEN"
            and (v["pdf_page_first"],v["pdf_page_last"],v["source_jpegs_individually_opened"])==(1,20,20)
            and hashes==PINS and len(hashes)==20
            and hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()==v["sha256_concatenated_page_hashes"]==CHAIN_SHA256
            and hashes[0]==prior["page_sha_pins"]["1"]
            and v["page1_direct_original_juan_heading"]=="萬曆三十年壬寅卷五"
            and v["page1_chronicle_label_year"]==1602
            and v["page1_half_right_blank"] is True
            and v["original_juan_label_applies_to_current_edition_not_1827_thematic_volume"] is True
            and v["ocr_used"] is False
            and v["complete_text_transcription_performed"] is False
            and v["target_original_glyph_or_heading_positive_found"] is False
            and v["page_target_absence_proven"] is False
            and v["whole_manuscript_absence_proven"] is False):
        raise ValueError("12RF_SCOPE_HASH_GLYPH_OR_ABSENCE_PROMOTION")
    base=re["review_accounting"]
    if not (q["prior_batch"]=="12RE"
            and (q["old_native_source_pages"],q["old_montage_preview_only_source_pages"],
                 q["old_native_body_target_backlog"])==
                (base["whole_source_native_screens"],base["whole_source_montage_only_screens"],
                 base["whole_body_native_target_screen_backlog"])==(146,882,882)
            and (q["new_native_source_pages"],q["new_montage_preview_only_source_pages"],
                 q["new_native_body_target_backlog"])==(166,862,862)
            and (q["original_fascicle2_total_source_body_pages"],
                 q["original_fascicle2_native_target_screened"],
                 q["original_fascicle2_native_target_screen_pending"])==(72,20,52)
            and (q["next_fascicle2_pdf_page_first"],q["next_fascicle2_pdf_page_last"])==(21,40)
            and (q["total_source_pages"],q["total_body_pages"],
                 q["whole_source_full_text_body_collation_backlog"],
                 q["preliminary_nonbody_pages"])==(1030,1027,1027,2)
            and q["whole_source_firstpass_unscreened_body_pages"]==0
            and q["new_independent_physical_copy_count"]==0
            and q["global_negative_proven"] is False
            and 166+862+2==1030
            and value["transmission_impact"]["edges_supported"]==[]
            and value["invariants"]["matrix"]=="222/222"
            and value["invariants"]["provenance_repaired"]=="45/45"
            and value["invariants"]["external_sources"]=="647+7=654"
            and value["invariants"]["product_r1"]=="CLOSED"
            and value["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("12RF_FALSE_QUEUE_ADVANCE_OR_NEW_PHYSICAL_WITNESS")
    return {"batch":"12RF","fascicle2_native_target_screen_pages":20,
            "fascicle2_remaining_native_target_screen_pages":52,
            "source_native_bounded_pages":166,"whole_source_native_body_backlog":862,
            "whole_manuscript_full_text_body_collation_backlog":1027,
            "original_target_glyph_attested":False,"whole_text_absence_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
