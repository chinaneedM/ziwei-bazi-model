#!/usr/bin/env python3
"""12RV fifth fascicle original source p21-63 hash-chain and cross-batch no-double-count gate."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RV-NLC411999003250-F5-P21-63-NATIVE-REVIEW-DEDUP-R1.json"
RU=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RU-NLC411999003250-F5-P1-20-NATIVE-REVIEW-R1.json"
QM=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QM-NLC411999003250-FASC4-5-SCOPED-MANUAL-IMAGE-TRIAGE-R1.json"
QL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
PIN43=[
    "5f04ee050ee74fd6e144ddc64c2f814f29661c9f59af89fa41a5d7b68d4c7e16",
    "5c47affde92199e54d9b34df6c59d4df92468744311a7293bea199c2a3905e3f",
    "85ec8a887f3929b4769c4c204017f11feb0d6e994e938168bf248adbf12a9c80",
    "aa5f5db6872c1efc100f55d8edfe8888b08e93fb9620a2f065ffb79d14fab446",
    "99e8d4f47213ec6f3314603c69eca30e1bac775e189e3273d60b8c03871a0563",
    "b3c2624a677d3c36c5766bb43deb974b290248b721bdef0d02cedc21c24531af",
    "62fa35813d8780b3837f991c5d56100d05af9482e5f0a2b07b1d687dbad936b4",
    "f77daeee86fa9ecd1df0eb5e6fb93be98f52d61ae6a7e6833f8f5bc950c7ffe1",
    "fda2a530834c5bbb57e97ccc859e241dd5e47dcf93ae3e8feb0c40b02552519c",
    "8a9f789bf2335a3e4202218ec326fda956b5d09738c50bd06a96747bec1671ae",
    "79993ac415d0bd2e2442b062d4f7c33dfd23c02ae31c9a48e6227473440e3cba",
    "58a0c51260a12d518e0aae3a965d7c52eee4b02bc0cfa0a383078f39d934f712",
    "1aec2692b667580a4af2af39be1382f89d23c10bb35db00bc41a337566f12f7f",
    "e8f6f28211102780c423d1dd15c0209eb8a4b62f152b4cecf25aaafefd2a9664",
    "ece39d90d050f0ffbee38174525bf027800839709b27e834c64d72abf9236a3c",
    "63a1f1695cf04a07468e6bbc3bdbde1cc3003b034a74ff1010c04530de0d589b",
    "f80c9bbc20451717e6420ed4f31435681aef8c5855267cc80275dd3704e99cad",
    "e2641c0776a0817217782b3ea12874c1957051294588a198a2400a1f0f755371",
    "a70c967685a72368809b0814e190c4c16ed37e4a01c68d3c2247ab129959e369",
    "a3274efd6d6fe892304e98b1326dc22df03a4b5404494781ec4885fed62ae848",
    "074cf02de1d1f243ceb1b786159dabb6517bf03db4cc5a18bf9c2c0d8ea56277",
    "1f5add978195f0de76821219bc1a63f9683f25ec65cd0457f36ce9e77542e351",
    "1ec137a7b9f8a401d978d2f36a1e9dcda53824eff13a5b575ce931cef9c7e15b",
    "921bb47d977ed5f3780183d8091fc97640187aa9194cf4b3a2499ea814f9c62e",
    "ef39575689f6c0f88ebbd622888f643f457aa87c763423631da383f16da8e1fa",
    "9c6a60f532e5cadbf124bf6b7d40aff4c893d55a686a3df00d8e31e1cc90d190",
    "1799b7f32d881e29288684a819f1fd405967a603cfc58fb528c68035285de499",
    "ca5ea45eb425b1daec1289d8db5b0d0d76c02e2bbcd0b7636986253914b759c6",
    "4475d9b9af70e9b93a01930c94c49d36f4057645fd004d5e5be21d6f4b768e03",
    "cfdaa7c75f3b3f67acf7734a75c799e7eb4d54e314772dde6e4e03a9178c8a2f",
    "d6bb12c125a4081a071ab4b910296e73e5fac3e6fab8555ff86e3f2c46ed0f8c",
    "702807bf7fc240a0b7762cb8da6683b57eb2bc5a52f5273d16b06851aad062a6",
    "d20361ce2fc27fe7074837f51946e32baf6883b4f9dc77f326aef941cffbc9c4",
    "80918393ecef044c2fad3fed1a5681980ac499ded7fc06e90e2949d737e4735a",
    "981e312ba7c4b4b76842b20169017243241e23775772c337369539aaddd88935",
    "75da805a7418b399a0cfe5af0a3034096dbea33899ff0b2e5dbd0139658dd9ed",
    "4ae92c41d89d5b97ae2ae82b846113430e4bd2148cd04838c095009275756259",
    "7c77dbb74abcf3eb4b1c22c1dd71539a6858832684cdc676e5036fe6a1e93825",
    "215a9a78ba8dc4167b9bff00494db1dfc473ba9546649eb519d4ccf0807c2a0a",
    "3d2891c21abeaf0f8d47ac532f42cd758474c8ffe5a17b54596f32f1ac5c3eb5",
    "dcfd947044a77ab18b8a092ed69a0ce89bf6af4edff22653cae45c09b74c3912",
    "3f362c4a5002b59f2c90501a92d7981ae7b37d18904eaea8cff5b6010d6ce718",
    "1ba2f95a2f18183d28ba71fab701f9d8d1efd6c0c5b8d62ee96664d7eb718d4f"
]
SHA43="0b2ad0eea501b99718182a7df30b198c368a345807a8902237cba22524ce6ea7"
SHA20="a6d58dbc294970c879225acadca29c101a66dc6acf3e16afd2b4781b8b6cf48e"
SHA63="d66546a59822762c76936edd93d5fd11db907ffdf9dd247b69be50066592c950"

def read(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def chain(pins):return hashlib.sha256("".join(pins).encode("ascii")).hexdigest()

def verify(record_path=RECORD,ru_path=RU,qm_path=QM,ql_path=QL):
    d,ru,qm,ql=(read(p) for p in (record_path,ru_path,qm_path,ql_path))
    s,v,u,q=d["source"],d["review"],d["identity_dedup"],d["queue"]
    ps,pr=ru["source"],ru["review"]
    ql5=next(x for x in ql["sources"] if x["fascicle"]==5)
    qm5=next(x for x in qm["checked_artifacts"] if x["digital_fascicle"]==5)
    if not (
        d["batch"]=="12RV" and d["parent_open_batch"]=="12QE" and d["stage"]=="12QE_OPEN"
        and d["status"]=="NLC_F5_P21_63_ORIGINAL_JPEG_SOURCE_BOUNDED_VISUAL_FIRSTPASS_COMPLETE_WITH_CROSSBATCH_DEDUP_NOT_FULLTEXT"
        and s["holding"]==ps["holding"]=="NLC411999003250_ONE_HOLDING"
        and s["digital_fascicle"]==ps["fascicle"]==ql5["fascicle"]==5
        and s["commons_file_id"]==ps["commons"]=="NLC892-411999003250-383066"
        and s["catalogue_original_volume_labels"]==ps["catalogue_original_juan"]==ql5["volume_labels"]==[10]
        and s["source_pdf_pages"]==ps["source_pdf_pages"]==ql5["source_pdf_pages"]==63
        and s["source_pdf_sha256"]==ps["pdf_sha256_inherited"]==ql5["source_pdf_sha256"]
        and s["source_pdf_binary_rehashed_this_batch"] is False
        and s["artifact_id"]==ps["artifact_id"]==ql5["artifact_id"]==11674555957
        and s["archive_zip_sha256"]==ps["zip_sha256"]
        and s["status_json_sha256"]==ps["status_sha256"]
        and s["original_source_jpeg_sha256_and_byte_size_members_verified"]==63
        and s["original_source_jpeg_member_mismatches"]==0
        and s["source_full63_ordered_sha256_chain"]==ps["full63_ordered_jpeg_sha256_chain"]==SHA63
    ):raise ValueError("12RV_ARCHIVE_AND_SOURCE_IDENTITY_DRIFT")
    p20=pr["image_pins"]
    p43=v["original_jpeg_sha256_in_source_page_order"]
    if not(
        v["mode"]=="SOURCE_JPEG_NATIVE_PIXEL_2X2_CONTACT_MONTAGE_PAGE_LEVEL_BOUNDED_VISUAL_HEADING_TOPIC_SCREEN_NOT_GLYPH_EXHAUSTIVE"
        and (v["window_pdf_page_first"],v["window_pdf_page_last"])==(21,63)
        and v["original_jpeg_page_files_hash_verified"]==43
        and v["source_original_jpegs_displayed_in_page_preserving_montage"]==43
        and v["montage_count"]==11
        and len(p20)==20 and len(p43)==43 and p43==PIN43
        and chain(p20)==v["prior_first20_sha256_chain"]==SHA20
        and chain(p43)==v["window_sha256_chain"]==SHA43
        and chain(p20+p43)==v["fascicle5_full63_sha256_chain"]==SHA63
        and [o["pdf_pages"] for o in v["bounded_observations"]]==[[21,24],[25,28],[29,36],[37,44],[45,52],[53,60],[61,63]]
        and v["old_juan10_heading_repeated_from_prior_f5_p1"]==pr["first_page_juan_heading"]=="萬曆三十五年丁未卷十"
    ):raise ValueError("12RV_SOURCE_PAGE_SHA_ORDER_OR_VISUAL_SCOPE_DRIFT")
    blocked=("new_original_juan11_heading_directly_attested","old20_gaizao_louke_original_target_heading_or_glyph_attested",
        "ocr_performed","fulltext_linewise_text_collation_performed","page_target_absence_proven",
        "fascicle5_target_absence_proven","entire_old20_work_target_absence_proven",
        "later_1827_thirty_juan_equivalent_original_juan_proven")
    if any(v.get(k) is not False for k in blocked):
        raise ValueError("12RV_FALSE_POSITIVE_OR_NEGATIVE_TEXTUAL_CLAIM")
    source_map={i+1:sha for i,sha in enumerate(p20+p43)}
    old_map={x["page"]:x["jpeg_sha256"] for x in qm5["original_pages_opened"]}
    if not (
        u["identity_key"]=="NLC411999003250/fascicle5/pdf-source-page/original-jpeg-sha256"
        and u["previous_12ru_source_range"]==[1,20]
        and u["this_batch_source_range"]==[21,63]
        and sorted(old_map)==u["earlier_12qm_individual_original_page_numbers"]==[1,31,63]
        and u["previous_12ru_overlap_with_12qm"]==[1]
        and u["this_batch_overlap_with_12qm"]==[31,63]
        and all(source_map[p]==sha for p,sha in old_map.items())
        and len(source_map)==len(set(source_map))==u["source_page_union_count"]==63
        and u["source_page_union_contiguous_start"]==1
        and u["source_page_union_contiguous_end"]==63
        and u["global_1030_pdf_source_page_native_review_deduplicated_union_computed"] is False
        and u["do_not_inflate_global_native_count_due_to_repeated_page_views"] is True
        and u["independent_physical_holding_increment"]==0
    ):raise ValueError("12RV_CROSS_BATCH_OVERLAP_OR_GENEALOGY_DRIFT")
    if not(
        q["prior_batch"]==ru["batch"]=="12RU"
        and q["f5_total_pdf_source_pages"]==63
        and (q["prior_f5_bounded_screened_pages"],q["new_f5_bounded_screened_pages"])==(20,63)
        and q["f5_native_visual_firstpass_remaining_pages"]==0
        and (q["prior_whole_holding_global_native_reported_pages"],q["prior_whole_holding_global_preview_only_reported_pages"])==(339,689)
        and q["new_whole_holding_global_native_reconciled_pages"] is None
        and q["new_whole_holding_global_preview_reconciled_pages"] is None
        and (q["whole_holding_source_pdf_pages"],q["whole_holding_fulltext_body_collation_pending"])==(1030,1027)
        and d["transmission_impact"]["edges_supported"]==[]
        and d["transmission_impact"]["edges_revised"]==[]
        and d["invariants"]=={"matrix_rows":222,"matrix_audited":222,
          "repaired_provenance_metadata_defects":45,"source_registry":"647+7=654",
          "md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT",
          "deterministic_product_r1":"CLOSED","algorithm_reopen_count":0}
    ):raise ValueError("12RV_PENDING_QUEUE_OR_INVARIANTS_DRIFT")
    return {"batch":"12RV","fascicle5_native_bounded_visual_coverage":"63/63",
      "newly_screened_window":43,"prior_direct_page_overlaps":[1,31,63],
      "global_unique_native_source_count_reconciled":False,
      "fulltext_body_pages_still_pending":1027,"old20_target_presence_or_absence_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
