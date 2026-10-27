#!/usr/bin/env python3
"""12QW: source-hash-bound f6/f10 previews; source image screening != text absence."""
import copy
import importlib.util
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE-R1.json"
QL=RS/"MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
QO=RS/"MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QV=ROOT/"scripts/verify_yehuobian_nlc_f9_montage_scope_12qv.py"

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def qv_module():
    spec=importlib.util.spec_from_file_location("tianwen_nlc_12qv_for_12qw",QV)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PINS={
6:{"pdf":"9949f3c736d75f1772c306455f6bead7e744675b66283a415e7c50f4dc4f1c62",
"artifact":11674845912,"run":38064436808,
"zip":"934d5c16493275c8fb0742abe8764d424bc4a2b2c5f02e99c5bcaab249a7d023",
"meta":"895597abefeac14f6f9c6c3b5a0bb41a8c1114d4250a17773e3e0e52bfc0d9e3",
"pages":"4998d749bb522d60cd7df499f5aefded8afb4e952111b4b3f2dff85d04573828",
"contacts":"835f7a36c3829c443836a084a077a227d89d92610308a9f359b05e1a944ffcfc",
"p1":"2e0c827b26682645ba9ace144b938638801a169ef1e012ea3deb03a89a20e190",
"p116":"896dd1b6fd7ab33736dc617dd8cacae40ad6561ceae5c02eb09479e5019c272d"},
10:{"pdf":"8e746faaadcd961c7983981d419862d97fdc2a1f3ec33ecb02046e9e79a6376c",
"artifact":11666856770,"run":38044584678,
"zip":"d5b3b054460cd4e5dc433bbe9ed75a3dd7baa3c5657bc0686a61a7b97423c2f8",
"meta":"e69b3f9488e317685faec3a5fc61bafc0975cfd5a836310292bde683ee727632",
"pages":"73d9ee7c925b8a0fedaf02ead8236f1a5b0db78f5be6bb66ebdc518165995955",
"contacts":"ca104b7282cbacc79b0264a0c82958934c67fa2f7843693faa7684f7402db738",
"p1":"eb185b6f31c1f285f5690627d4b199f2d2b73679ae4ed0a3648595059239e40b",
"p81":"222f6f312dee3447bf6e4446a869e6f1aad765ce45f8670cec7b54aaea1345e4",
"p137":"18881b8c7a57aaf612026b38a387c73d664e481a42063ba221517908e29ad130",
"p145":"b26468c9399352a5c947e8dac74e810761fff28bff54dc71ad555a264b00977c"}}

def verify(record_path=RECORD):
    r=load(record_path)
    qv=qv_module()
    before=qv.verify()
    qt=qv.qu_module().qt_module()
    base=qt.build_rows()
    ql=load(QL)
    qo=load(QO)
    atlas={s["fascicle"]:s for s in ql["sources"]}
    openings={(x["digital_fascicle"],x["pdf_page"]):x for x in qo["original_juan_openings"]}
    if not (r["stage"]=="12QE_OPEN"
       and r["status"]=="SOURCE_SHA_BOUND_MONTAGE_PREVIEW_NO_NEW_NATIVE_TARGET_PROOF"
       and r["physical_holding"]["id"]=="NLC411999003250_ONE_HOLDING"
       and r["physical_holding"]["copy_increment"]==0
       and r["physical_holding"]["old20_target_folio"]=="UNLOCATED"):
        raise ValueError("UNVERIFIED_PHYSICAL_COPY_OR_TARGET_LEAF")
    archives=r["source_archives"]
    if [s["fascicle"] for s in archives]!=[6,10]:
        raise ValueError("SOURCE_FASCICLE_SET_CHANGED")
    for s in archives:
        f=s["fascicle"]
        pin=PINS[f]
        q=atlas[f]
        if not (s["source_pdf_sha256"]==q["source_pdf_sha256"]==pin["pdf"]
            and s["source_pdf_rehashed_this_batch"] is False
            and s["artifact_id"]==q["artifact_id"]==pin["artifact"]
            and s["workflow_run"]==q["workflow_run"]==pin["run"]
            and s["artifact_zip_sha256"]==pin["zip"]
            and s["artifact_metadata_sha256"]==pin["meta"]
            and s["page_sha_chain"]==pin["pages"]
            and s["contact_sha_chain"]==pin["contacts"]
            and s["pdf_pages"]==q["source_pdf_pages"]==(116 if f==6 else 145)
            and s["page_jpeg_count_sha_verified"]==q["source_page_images"]==s["pdf_pages"]
            and s["contact_count_sha_verified"]==q["contact_sheets"]==(15 if f==6 else 19)
            and s["image_hash_mismatches"]==0
            and s["contact_sheet_starts"]==list(range(1,s["pdf_pages"]+1,8))
            and s["native_navigation_pages"]==([1,116] if f==6 else [1,81,137])
            and s["new_preview_only_pages"]==(116 if f==6 else 136)
            and s["prior_native_target_screened_pages"]==(0 if f==6 else 9)
            and s["original_juan"]==([11] if f==6 else [18,19,20])
            and all(re.fullmatch("[0-9a-f]{64}",s[k]) for k in
                ("source_pdf_sha256","artifact_zip_sha256","artifact_metadata_sha256","page_sha_chain","contact_sha_chain"))):
            raise ValueError("SOURCE_HASH_IDENTITY_OR_EVIDENCE_SCOPE_CHANGED")
        if f==6:
            o=openings[6,1]
            if not (s["original_volume_opening_page"]==o["pdf_page"]==1
                and o["volume"]==11 and o["right_leaf_has_previous_volume"] is False
                and s["original_volume_opening_jpeg_sha"]==o["page_jpeg_sha256"]==pin["p1"]
                and s["ending_jpeg_sha"]==pin["p116"]):
                raise ValueError("F6_OPENING_OR_TERMINAL_IMAGE_MISMATCH")
        else:
            expected=[(18,1,False),(19,81,True),(20,137,True)]
            for row,(vol,p,right) in zip(s["original_juan_openings"],expected):
                o=openings[10,p]
                if not (row["volume"]==o["volume"]==vol and row["pdf_page"]==p
                    and row["previous_volume_right_leaf"] is right
                    and o["right_leaf_has_previous_volume"] is right
                    and row["sha256"]==o["page_jpeg_sha256"]==pin[f"p{p}"]):
                    raise ValueError("F10_CROSS_ORIGINAL_VOLUME_FOLIO_MISMATCH")
            if not (s["last_colophon_page"]==145
                and s["last_colophon_jpeg_sha"]==pin["p145"]):
                raise ValueError("F10_FINAL_COLOPHON_SHA_CHANGED")
    m=r["methods"]
    if not (m["review_grade"]=="EIGHT_UP_DOWNSAMPLED_MANUAL_VISUAL_PREVIEW_ONLY"
       and m["contact_images_manually_opened"]==34
       and m["source_pages_represented_in_contacts"]==261
       and m["source_page_jpegs_rehashed"]==261
       and m["source_contact_jpegs_rehashed"]==34
       and m["digest_mismatches"]==0
       and m["original_image_direct_read_for_navigation_only"] is True
       and m["ocr_used"] is False and m["positive_target_glyph_attestation_count"]==0
       and m["new_native_target_text_reviews"]==0
       and m["target_absence_on_any_source_page_proven"] is False
       and m["whole_work_target_absence_proven"] is False
       and m["full_text_transcribed_pages"]==0):
        raise ValueError("PREVIEW_PROMOTED_TO_UNEARNED_NATIVE_OR_NEGATIVE_PROOF")
    g=r["grade_rules"]
    if not (g["f6_preview_pages"]=="1..116" and g["f10_preview_pages"]=="1..136"
       and g["f10_native_bounded_pages"]=="137..145"
       and g["f10_colophon_non_body_page"]==145
       and g["do_not_downgrade_nine_prior_native_screens"] is True
       and g["do_not_promote_native_navigation_to_target_review"] is True):
        raise ValueError("F10_EXISTING_NATIVE_SCREENS_OVERWRITTEN")
    f6=[x for x in base if x["fascicle"]==6]
    f10=[x for x in base if x["fascicle"]==10]
    if not (len(f6)==116 and len(f10)==145):
        raise ValueError("BASE_PAGE_UNIVERSE_CHANGED")
    for x in f6:
        if not (x["target_screen_grade"]=="NOT_TARGET_SCREENED"
            and x["original_volume_candidates"]==[11]
            and x["body_search_eligible"] and x["requires_native_target_screen"]):
            raise ValueError("F6_PREVIEW_PAGE_WAS_ALREADY_TARGET_SCREENED")
    for x in f10:
        p=x["pdf_page"]
        expected=[18] if p<81 else ([18,19] if p==81 else ([19] if p<137 else ([19,20] if p==137 else [20])))
        if x["original_volume_candidates"]!=expected:
            raise ValueError("F10_MIXED_FOLIO_OWNERSHIP_LOST")
        if p<=136:
            if not (x["target_screen_grade"]=="NOT_TARGET_SCREENED" and x["requires_native_target_screen"]
                and x["body_search_eligible"]):
                raise ValueError("F10_PREVIEW_ALREADY_REVIEWED")
        else:
            if not (x["target_screen_grade"]=="NATIVE_BOUNDED_HEADING_PASSAGE_SCREEN"
                and x["requires_native_target_screen"] is False):
                raise ValueError("F10_NINE_PRIOR_NATIVE_SCREENS_DOWNGRADED")
            if (p==145)==x["body_search_eligible"]:
                raise ValueError("F10_COLOPHON_BODY_FLAG_DRIFT")
    new=copy.deepcopy(before)
    new["montage_only_source_pages"]+=252
    new["not_target_screened_source_pages"]-=252
    new["body_not_even_firstpass_screened"]-=252
    new["per_fascicle"]["6"]["fourup_only"]+=116
    new["per_fascicle"]["10"]["fourup_only"]+=136
    expected=r["queue_reconciliation"]["expected_after"]
    for k,v in expected.items():
        if new[k]!=v:
            raise ValueError("QUEUE_SUMMARY_DRIFT_"+k)
    if not (new["native_body_review_backlog"]==999 and
        new["body_full_text_collation_backlog"]==1027 and
        new["montage_only_source_pages"]==570 and new["body_not_even_firstpass_screened"]==429 and
        new["not_target_screened_source_pages"]==431 and
        new["per_fascicle"]["10"]["native_screens"]==9 and
        new["per_fascicle"]["10"]["native_body_backlog"]==136 and
        new["per_fascicle"]["6"]["native_body_backlog"]==116 and
        r["invariants"]["product_r1"]=="CLOSED" and
        r["invariants"]["algorithm_reopens"]==0):
        raise ValueError("FALSE_NATIVE_CLOSURE_OR_RUNTIME_CHANGE")
    return new

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
