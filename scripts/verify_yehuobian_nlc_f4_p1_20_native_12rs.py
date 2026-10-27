#!/usr/bin/env python3
"""12RS: NLC original fascicle4 source-image pins, scope and no-double-count gate."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RS-NLC411999003250-F4-P1-20-NATIVE-IMAGE-SCREEN-R1.json"
QL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
PINS=[
    "86bb06ae975b10e5495b8f161631f6f9b4aa857fb785048908c868479fdb5161",
    "4d12e8e1b09c03d4260873476dc9789a41a45ad995e4f8e76899d0a6a3604981",
    "2d2abc7a4efde5bfcee335b0b4683c702e9bbbfe9bbbb008bdc1e74459052a47",
    "8453eb4a76009b74f69e6e9126ce276b9dadec53f6e6f5a704a448bd1f901279",
    "81523819ff3e442cc54f8cb3721b4992ab127dad498ab2190adb89b2f43bc0b3",
    "694a5c3280365a0705e38dc13b486bddf738e45b9344f3a85b975fcc207d94ac",
    "280858e62261f409f1b72c6871bd2aaf2f026996682d8578bcc75b674ea38ff2",
    "5eb5e9a34c0e429e9d776480178361005e9c0172f584dab175aaf2f2028ed5d5",
    "0e791b51dc42f78772b34e5f4e83444805c86d684f8a39cefe99791e2a0ab042",
    "24dfdc98e866757db730daaccb3e6d77bf7ced5cf98467431d14de404e2b5aac",
    "a1159bc990c1a37a4c2e430fce93deb650cf9b39c510d4b67d3a110924640059",
    "d90730cac8297e51e1d322ab28df56a168c29d520230484777b9193ba3f523f3",
    "7f8dfd1111f65be5203156f5a54999fdcf035b0d9dc43dd93c93c558507598d3",
    "3669b113db6726d6c4aa6c050a17df19a1d86f0f332f66999c13895b3fafca27",
    "b20c6b8d6ec5cf5675ce1e1606a680ac6e83cc503d58d689d637dcd4eadc2c7e",
    "0afe907b3e34f946b8b3b7a45ef47d7177d9a5828ecfac09e7ffa203afc4f378",
    "09e687008da2d1593f9398ec17872b57b3402ec3c24dd71562484ad82e7b1cb3",
    "41b9f367d5fce40363a3f5c6400f8599a191e477fffd363859df4279533fa806",
    "21436edb7afe71ec4235b8a1bd23d90f6b8aa689781df277171d3b5d2d78f14d",
    "dfd39a3b0590bb239111b1138eed762538d9c9bf506ca02033269371294d7781"
]
FIRST20="8a443e749f36b5f5f187ec2ad027df4fd9ccc3e3649b0390f02e10e99e83e2a9"
FULL56="b1866e1fe3cf4c3b73f87d88699d1dae31e6e1ea65aa7c545072d15c0006c8e1"
ARCHIVE="9a56d1f98fdb4a727ad1cd1f8c4131c94334d35864ed66279b118a26deb2f4f7"
MANIFEST="44a12a988cfdaa867a1f2471383669c3f7f3f3fcc8c99d620535c4d5c577e3b1"

def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def verify(record_path=DATA, prior_path=QL):
    d=read(record_path)
    ql=read(prior_path)
    src=d["source"];rev=d["review"];q=d["queue"]
    row=next(x for x in ql["sources"] if x["fascicle"]==4)
    if not (d["batch"]=="12RS" and d["parent_open_batch"]=="12QE" and d["stage"]=="12QE_OPEN"
        and d["status"]=="SOURCE_F4_P1_20_ORIGINAL_JPEG_BOUNDED_VISUAL_REVIEW_WITH_GLOBAL_UNIQUE_PAGE_COUNT_PENDING_DEDUP"
        and src["physical_holding"]=="NLC411999003250_ONE_HOLDING"
        and src["fascicle"]==row["fascicle"]==4
        and src["catalogue_original_volume_labels"]==row["volume_labels"]==[8,9]
        and src["source_pdf_pages"]==row["source_pdf_pages"]==56
        and src["source_pdf_sha256_from_12ql"]==row["source_pdf_sha256"]
        and src["source_pdf_binary_rehashed_in_12rs"] is False
        and src["archive_artifact_id"]==row["artifact_id"]==11674246374
        and src["archive_zip_sha256"]==ARCHIVE
        and src["archive_status_json_sha256"]==MANIFEST
        and src["archive_original_jpeg_members_hashed_and_size_checked"]==56
        and src["archive_sha256_or_size_mismatch_count"]==0
        and src["whole_56_source_jpeg_sha256_concatenation_chain"]==FULL56
        and src["commons_file_id"]=="NLC892-411999003250-383062"):
        raise ValueError("12RS_SOURCE_HOLDING_OR_ARCHIVE_DRIFT")
    sha=rev["source_jpeg_sha256_in_pdf_order"]
    if not (sha==PINS and len(sha)==20
        and hashlib.sha256("".join(sha).encode("ascii")).hexdigest()==rev["first20_original_jpeg_sha256_concatenation_chain"]==FIRST20
        and (rev["pdf_page_first"],rev["pdf_page_last"],rev["original_resolution_source_jpegs_individually_opened"])==(1,20,20)
        and rev["mode"]=="INDIVIDUAL_OPENING_OF_SOURCE_NATIVE_JPEG_P1_20_BOUNDED_HEADING_AND_CONTEXTUAL_VISUAL_SCREEN_NOT_LINEWISE_FULL_TEXT"
        and rev["source_p1_direct_volume_heading"]=="萬曆三十三年乙巳卷八"
        and rev["source_p1_heading_previously_directly_attested_in"]=="12QL"
        and [x["pdf_page"] for x in rev["bounded_observations"]]==[1,6,7,19,20]):
        raise ValueError("12RS_ORIGINAL_PAGE_HASH_OR_TITLE_DRIFT")
    forbidden=("any_original_old20_gaizao_louke_heading_or_glyph_attested","ocr_used",
        "full_text_linewise_collation_completed","any_page_target_absence_proven",
        "fascicle_target_absence_proven","whole_old20_work_target_absence_proven",
        "same_as_1827_fulishanfang_original_juan_or_direct_copy_proven")
    if any(rev.get(k) is not False for k in forbidden) or rev["independent_copy_increment"]!=0:
        raise ValueError("12RS_UNSUPPORTED_TARGET_GLYPH_ABSENCE_OR_LINEAGE")
    if not (q["previous_batch"]=="12RQ"
        and q["fascicle4_total_pages"]==56
        and q["fascicle4_consecutive_original_jpeg_bounded_screened_first_pages"]==20
        and q["fascicle4_remaining_contiguous_screening_window"]==[[21,56]]
        and q["fascicle4_remaining_contiguous_screening_pages"]==36
        and (q["prior_whole_holding_native_bounded_pages"],q["prior_whole_holding_preview_only_pages"],q["prior_whole_holding_fulltext_body_pending"])==(339,689,1027)
        and q["unique_global_native_screen_count_recomputed_in_batch"] is False
        and q["new_whole_holding_native_bounded_pages_reported"] is None
        and q["new_whole_holding_preview_only_pages_reported"] is None
        and d["transmission_impact"]["edges_supported"]==[]
        and d["transmission_impact"]["edges_revised"]==[]
        and d["invariants"]=={"matrix_rows":222,"audited_rows":222,"provenance_repairs":45,
            "source_registry_root":647,"source_registry_extensions":7,"md_g03":"OPEN",
            "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","product_r1":"CLOSED","algorithm_reopen_count":0}):
        raise ValueError("12RS_GLOBAL_DEDUP_OR_INVARIANT_DRIFT")
    return {"batch":"12RS","original_individual_pages_reviewed":20,
        "archive_jpeg_sha_and_size_56_checked":True,"whole_book_global_unique_page_recounted":False,
        "full_text_body_pages_still_pending":1027,"new_old20_target_presence_or_absence_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
