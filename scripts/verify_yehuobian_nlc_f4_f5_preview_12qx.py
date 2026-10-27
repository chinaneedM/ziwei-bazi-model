#!/usr/bin/env python3
"""12QX f4/f5 SHA-bound NLC manuscript preview is not native target text."""
import copy
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12QX-NLC411999003250-F4-F5-CONTACT-TRIAGE-R1.json"
QL=RS/"MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
QO=RS/"MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QW=ROOT/"scripts/verify_yehuobian_nlc_f6_f10_preview_12qw.py"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def qw_module():
    spec=importlib.util.spec_from_file_location("tw12qw_for_12qx",QW)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PINS={
4:{"pdf":"11c1cfacb913404be79e386a967324048b762a166b1c08c1853fcbdcc904d67a","artifact":11674246374,
"zip":"9a56d1f98fdb4a727ad1cd1f8c4131c94334d35864ed66279b118a26deb2f4f7",
"status":"44a12a988cfdaa867a1f2471383669c3f7f3fcc8c99d620535c4d5c577e3b1",
"pages":"b1866e1fe3cf4c3b73f87d88699d1dae31e6e1ea65aa7c545072d15c0006c8e1",
"contacts":"78c6f8b765511bb90b40450d960c608d613d8cac21d93a3f0328dd8d657ca18d",
"p1":"86bb06ae975b10e5495b8f161631f6f9b4aa857fb785048908c868479fdb5161",
"p35":"320a25d6902b0e5e0a4e9931eda67b2882195f6f96abdfb862c4b1ef0afa8e76",
"last":"c0500d19b5b3033fb89f5a0b68cbbb3117f4a75cfb9814ea3ecfd28c7fe3ebad"},
5:{"pdf":"06692bd33c86c6c6cd8eb732fe89aa1d289e06da976663d33ca04352d9f45280",
"artifact":11674555957,"zip":"89d314baafc615809a2ba906bb308bedbe130bd7f100571724cdba8a27978c36",
"status":"73a464cf649f92226d6f016ad50acb71d2f1f00a32ba8bf9c7c43eb3828d77a7",
"pages":"d66546a59822762c76936edd93d5fd11db907ffdf9dd247b69be50066592c950",
"contacts":"5f9fd56c4b5f0f79ea95fcc95d31cbf55da217dfb43580207e304c5dafa2b4d1",
"p1":"7b6499149c1a0f21c7dc2e03018af90eafc390001115c9969a64a7b88c0f37e7",
"last":"1ba2f95a2f18183d28ba71fab701f9d8d1efd6c0c5b8d62ee96664d7eb718d4f"}}

def verify(path=RECORD):
    obj=load(path)
    mod=qw_module()
    prior=mod.verify()
    qt=mod.qv_module().qu_module().qt_module()
    base=qt.build_rows()
    atlas={r["fascicle"]:r for r in load(QL)["sources"]}
    original={(r["digital_fascicle"],r["pdf_page"]):r for r in load(QO)["original_juan_openings"]}
    if not (obj["stage"]=="12QE_OPEN"
        and obj["status"]=="HASH_VERIFIED_CONTACT_PREVIEW_ONLY_NO_NATIVE_TARGET_PROOF"
        and obj["physical_holding"]=="NLC411999003250_ONE_HOLDING"
        and [a["fascicle"] for a in obj["source_archives"]]==[4,5]):
        raise ValueError("SOURCE_STUDY_SCOPE_DRIFT")
    for a in obj["source_archives"]:
        f=a["fascicle"]
        p=PINS[f]
        q=atlas[f]
        body=[r for r in base if r["fascicle"]==f]
        if not (a["source_pdf_pages"]==q["source_pdf_pages"]==(56 if f==4 else 63)
            and a["source_pdf_sha256"]==q["source_pdf_sha256"]==p["pdf"]
            and a["source_pdf_binary_rehashed"] is False
            and a["artifact_id"]==q["artifact_id"]==p["artifact"]
            and a["workflow_run_id"]==q["workflow_run"]==38064436808
            and a["archive_sha256"]==p["zip"]
            and a["status_json_sha256"]==p["status"]
            and a["source_page_sha_chain"]==p["pages"]
            and a["contact_sheet_sha_chain"]==p["contacts"]
            and a["source_page_jpeg_count"]==len(body)==(56 if f==4 else 63)
            and a["contact_sheet_jpeg_count"]==(7 if f==4 else 8)
            and a["contact_sheet_starts"]==list(range(1,len(body)+1,8))
            and a["member_hash_mismatches"]==0
            and a["original_images_opened_for_navigation_only"]==([1,35,56] if f==4 else [1,63])
            and a["old_original_juan"]==([8,9] if f==4 else [10])
            and a["last_source_jpeg_sha256"]==p["last"]):
            raise ValueError("ARCHIVE_SOURCE_SHA_OR_VISUAL_SCOPE_MISMATCH")
        expected_orig=[(8,1,False,1605),(9,35,True,1606)] if f==4 else [(10,1,False,1607)]
        if len(a["volume_openings"])!=len(expected_orig):
            raise ValueError("ORIGINAL_VOLUME_OPENINGS_COUNT_CHANGED")
        for record,(vol,page,right,year) in zip(a["volume_openings"],expected_orig):
            upstream=original[f,page]
            if not (record["old_juan"]==upstream["volume"]==vol
                and record["page"]==upstream["pdf_page"]==page
                and record["year"]==upstream["year_label"]==year
                and record["sha256"]==upstream["page_jpeg_sha256"]==p[f"p{page}"]
                and record["prior_volume_on_right_leaf"] is right
                and upstream["right_leaf_has_previous_volume"] is right):
                raise ValueError("MIXED_ORIGINAL_LEAF_OR_HEADING_DRIFT")
        if not (len(body)==len(list(range(1,len(body)+1)))
            and [r["pdf_page"] for r in body]==list(range(1,len(body)+1))):
            raise ValueError("FASCICLE_PAGE_INDEX_CHANGED")
        for r in body:
            page=r["pdf_page"]
            correct=[8] if f==4 and page<35 else ([8,9] if f==4 and page==35 else ([9] if f==4 else [10]))
            if not (r["original_volume_candidates"]==correct
                and r["source_pdf_sha256"]==p["pdf"]
                and r["body_search_eligible"] is True
                and r["requires_native_target_screen"] is True
                and r["target_screen_grade"]=="NOT_TARGET_SCREENED"):
                raise ValueError("SOURCE_PAGE_GRADE_INHERITANCE_DRIFT")
    v=obj["visual_method"]
    if not (v["mode"]=="EIGHT_UP_SOURCE_CONTACT_MANUAL_PREVIEW_NOT_NATIVE_FULL_TEXT"
        and v["individual_contacts_opened"]==15
        and v["pages_represented"]==119
        and v["source_jpegs_rehashed"]==119
        and v["contact_jpegs_rehashed"]==15
        and v["hash_mismatches"]==0
        and v["ocr_used"] is False
        and v["source_pdf_rehashed"] is False
        and v["new_native_target_text_screens"]==0
        and v["verified_target_glyphs"]==0
        and v["negative_on_individual_page_proven"] is False
        and v["negative_on_entire_work_proven"] is False
        and v["full_text_transcribed"] is False
        and v["full_size_page_reopens_navigation_only"] is True):
        raise ValueError("VISUAL_PREVIEW_UNJUSTIFIABLY_PROMOTED")
    new=copy.deepcopy(prior)
    new["montage_only_source_pages"]+=119
    new["not_target_screened_source_pages"]-=119
    new["body_not_even_firstpass_screened"]-=119
    new["per_fascicle"]["4"]["fourup_only"]+=56
    new["per_fascicle"]["5"]["fourup_only"]+=63
    s=obj["queue_reconciliation"]
    if not (
        s["prior_preview_only_source_pages"]==prior["montage_only_source_pages"]==570
        and s["added_preview_only_source_pages"]==119
        and s["new_preview_only_source_pages"]==new["montage_only_source_pages"]==689
        and s["new_not_target_screened_source_pages"]==new["not_target_screened_source_pages"]==312
        and s["new_body_not_even_firstpass_screened"]==new["body_not_even_firstpass_screened"]==310
        and s["native_screened_source_pages"]==new["native_screened_source_pages"]==29
        and s["native_body_review_backlog"]==new["native_body_review_backlog"]==999
        and s["body_full_text_collation_backlog"]==new["body_full_text_collation_backlog"]==1027
        and s["source_pages"]==new["source_pages"]==1030
        and s["body_pages"]==new["body_pages"]==1027
        and s["independent_physical_copy_increment"]==0
        and s["full_work_target_absence_proven"] is False
        and new["per_fascicle"]["4"]["native_body_backlog"]==56
        and new["per_fascicle"]["5"]["native_body_backlog"]==63
        and new["per_fascicle"]["4"]["fourup_only"]==56
        and new["per_fascicle"]["5"]["fourup_only"]==63
        and obj["invariants"]["product_r1"]=="CLOSED"
        and obj["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("FALSE_NATIVE_REVIEW_OR_NEGATIVE_12QX_COUNT")
    return new

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
