#!/usr/bin/env python3
"""12RD: source-bounded original-fascicle completion is not full-text or absence proof."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RD-NLC411999003250-F1-P89-119-NATIVE-SOURCE-REVIEW-R1.json"
RC=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RC-NLC411999003250-F1-P63-88-NATIVE-SOURCE-REVIEW-R1.json"
QO=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QY=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS-R1.json"
SOURCE_PDF="acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939"
ZIP_SHA="18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429"
STATUS_SHA="7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070"
CHAIN_SHA="a53d45e4f6c03bb7a160a46243fa973d001c271bbc6ae3dbc6ce4d628cc88a6e"
PINNED_HASHES="640b366ae6b4c1cc4f998b2fe02c769ee50217b724cb39020f9da255bfe86e20,791e8526a62543dee7da0345f88caf09620de0f78f540836bd58f486264bf7af,6c42d86d7c35bbb0bd9c24a412ae72503642cb5840ff2546480cd391d63bf52e,19c665d6cacdf5a198cb06b44184a3c8878f45988a7bfce44ee047c900a13410,5afa2c01cd18d9d66a0b38af1448c821b86d89c1a342bc37a3762c2bb2c929c9,95d8dd8d171d34d14b36ce765b06afee9468bc3c1e82a23f1271cface990fad6,d7c283831b5cc3f1e465bbe772512162db140614a59d3753634c9eff0ed1d9ef,903872355b38457dde156d64134c5b40fd471cc72d8f8854ea2fe18cab43be85,e94c5e34862e7ea0cd4d3a76826915d7c69478ad9507382965b552700b604046,93b89d8166b46983b4de06390bc7ccb3100da86a89d4a1f5045cdb6c17358936,ce8c7b036685052afcfc15b2832c66092f46583dbb383dbe23ff9c714827c3d2,a5e4f5c8454bb4c5289dfefc22132b4af6812f49b11724afd9cef81da7caa979,9627cf90bbebee995661fa7fc2cc2774c61842d465070761468740138dc24b95,4854c2111b29190581231d241682a149cfc4c419a63b42aa30bce3de4518b59e,3adcc3ba51709fd9ec15655f49ad4192d09f42e4265c674e763a8d31bd773300,146e00a2ba8e7cc5906ccce7a4ea49f11503c6620924a0ec1a3957241593917e,ba15675716b786521e5908690300181bd6c561febec9a36263321c4d8e1ba0bf,51e41eeb100d7db0c8c4aef88293b37c9db6765fde31a74a336837a39bfe378f,aa9c32079bb1cd83cbed9f56fe955d4f2fab9bdf797d0a259c7727cf39c46c8d,9c08c2f706be8739060ed288ebda30c86a298d73c582c09d6788d77b202a2c05,6fc2e247184270937229d44a43194182e2a008e715cbe52cee38a2d1401dc145,d136984f7752c27cfd7b8c1100126249c85b9435047874e27290820aa8349297,08be16d3c40760b2af1bf14974d043cdbc74863783d48b407582c5205d3095b1,7580b243332ac73c3c8394c765597f08ca3b11da0b7fc96aa08f44111fc3f817,5b1bb47a171835f44ec951b9da81e4a393f3f342a6238cae32c3333a159ddb4a,4c28613e034376df2be352a1763fc62d765071bdac881b718f06a0575da94413,c61fbbc28f5d0e44725ebafb84c6ade64e069c8d3ea814d2d44c36f94a88b82c,664cda89e54f48f6d135031ec04015c19f83108b0c3e5c45da5c9e06b697a87e,14a49bbd07d98afef007d224c86a480216ef71bb96975fa95005cf177f4a7f82,eca397e3b26443c1bbfe993625aaa97c0338bd7493cfc55f0f7abb30b1605178,ee9a8f512a995b950e2dab21aba03efcd57d478bd06c0c370886b255b221e9d7".split(",")

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def verify(record_path=RECORD,prior_path=RC,qo_path=QO,qy_path=QY):
    obj,prior,qo,qy=load(record_path),load(prior_path),load(qo_path),load(qy_path)
    s,v,q=obj["source"],obj["review"],obj["queue"]
    old=prior["queue"]
    if not (obj["batch"]=="12RD" and obj["stage"]=="12QE_OPEN" and
            obj["status"]=="FASCICLE1_BODY_NATIVE_BOUNDED_TARGET_VISUAL_SCREEN_COMPLETE_NO_TEXT_ABSENCE_PROOF"
            and s["holding"]==prior["source"]["holding"]=="NLC411999003250_ONE_HOLDING"
            and s["digital_fascicle"]==1 and s["source_pdf_pages"]==119
            and s["source_pdf_sha256"]==prior["source"]["source_pdf_sha256"]==SOURCE_PDF
            and s["artifact_id"]==prior["source"]["artifact_id"]==11674078668
            and s["artifact_zip_sha256"]==prior["source"]["artifact_zip_sha256"]==ZIP_SHA
            and s["artifact_status_json_sha256"]==prior["source"]["artifact_status_json_sha256"]==STATUS_SHA
            and s["source_pdf_binary_rehashed"] is False
            and s["source_original_jpegs_independently_hashed"]==31
            and s["source_original_jpeg_hash_mismatches"]==0):
        raise ValueError("12RD_SOURCE_ARCHIVE_BINDING_DRIFT")
    hashes=v["page_jpeg_sha256_in_pdf_order"]
    if not (v["mode"]=="INDIVIDUAL_ORIGINAL_JPEG_NATIVE_SIZE_BOUNDED_HEADING_TARGET_PHRASE_VISUAL_SCREEN"
            and v["first_pdf_page"]==89 and v["last_pdf_page"]==119
            and v["pages_separately_opened_for_bounded_visual_review"]==31
            and hashes==PINNED_HASHES
            and len(hashes)==31
            and hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()
                      ==v["sha256_concatenated_page_hashes"]==CHAIN_SHA
            and v["initial_fascicle1_body_pdf_first"]==3
            and v["initial_fascicle1_body_pdf_last"]==119
            and v["frontmatter_prelim_pages_not_target_screened"]==[1,2]
            and v["original_volume_4_scope_p89_to_p119"] is True
            and v["page_119_terminal_source_image_sha256"]==hashes[-1]
            and v["page_119_one_side_blank"] is True
            and v["positive_old20_gaizao_louke_target_heading_or_glyph_verified"] is False
            and v["ocr_used"] is False
            and v["complete_text_transcription_performed"] is False
            and v["any_page_target_absence_proven"] is False
            and v["whole_manuscript_target_absence_proven"] is False
            and v["not_equating_1827_thematic30_volume4_with_old20_chronicle4"] is True
            and v["first_fascicle_body_native_target_visual_screen_complete_not_full_text_complete"] is True):
        raise ValueError("12RD_GLYPH_GRADE_OR_ABSENCE_PROMOTION")
    vol4=next((r for r in qo["original_juan_openings"]
              if r["digital_fascicle"]==1 and r["volume"]==4),None)
    if not (vol4 is not None and vol4["pdf_page"]==88
            and vol4["right_leaf_has_previous_volume"] is True
            and qy["sources"][0]["source_pdf_pages"]==119
            and qy["sources"][0]["body_preview_pages"]==117):
        raise ValueError("12RD_SOURCE_VOLUME_OR_BODY_RANGE_CHANGED")
    if not (q["upstream_batch"]=="12RC"
            and (q["old_native_source_pages"],q["old_preview_only_source_pages"],
                 q["old_native_body_target_backlog"])==
                (old["after_native_bounded_source_pages"],old["after_preview_only_source_pages"],
                 old["after_native_body_target_backlog"])==(115,913,913)
            and (q["new_native_source_pages"],q["new_preview_only_source_pages"],
                 q["new_native_body_target_backlog"])==(146,882,882)
            and (q["first_fascicle_body_pages"],q["first_fascicle_native_bounded_target_screened"],
                 q["first_fascicle_preview_only_body_pages"],q["first_fascicle_frontmatter_not_target_screened"])==(117,117,0,2)
            and (q["whole_manuscript_source_pages"],q["whole_manuscript_body_pages"],
                 q["whole_manuscript_full_text_body_collation_backlog"])==(1030,1027,1027)
            and q["whole_manuscript_body_not_even_firstpass_screened"]==0
            and q["new_independent_physical_copy_count"]==0
            and q["global_target_absence_proven"] is False
            and obj["transmission_impact"]["edges_supported"]==[]
            and obj["invariants"]["product_r1"]=="CLOSED"
            and obj["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("12RD_REVIEW_QUEUE_FALSE_NEGATIVE_OR_WITNESS_INFLATION")
    return {"batch":"12RD","fascicle1_native_body_target_screened":117,
            "fascicle1_native_target_screen_pending":0,
            "whole_source_native_bounded_screens":146,
            "whole_source_native_body_review_backlog":882,
            "whole_source_full_text_body_backlog":1027,
            "original_target_glyph_proven":False,"whole_manuscript_absence_proven":False}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
