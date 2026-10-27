#!/usr/bin/env python3
"""12QY verify 1027-source-body first-pass coverage without false target negatives."""
import copy
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RS=ROOT/"docs/research"
RECORD=RS/"MING-DATONG-YEHUOBIAN-12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS-R1.json"
QL=RS/"MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
QO=RS/"MING-DATONG-YEHUOBIAN-12QO-NLC411999003250-ALL20-CHRONICLE-VOLUME-OPENINGS-R1.json"
QX=ROOT/"scripts/verify_yehuobian_nlc_f4_f5_preview_12qx.py"

PINS={
1:("acd33a56d2c829fcafd8db1c15b4bb9cb3d3b21905cc8d1e9e9d5a5c45b11939","18908565bbcffda40cf2251e747ae37c3b487ce4b0c13a15e0d04cf01fc38429","7ba8967f430666612df09b8dfefd312d601b40ac60e35d7cc6f5d08e69b1c070","45453afd8b172a05fbc311aa4b3bf2ae5569c2da17fe971d72a9aa8287f96873","3ac3f33d5f031d9a8c7758f4a8d108ca2dabc1166a27e85db28987c4df893592"),
2:("8fa105b74efe109a08140286c96a8215f049a62d0b1cf587e7e3e5afdb559d57","14015f5e788190a9b9839450fd8be45cea318e29bf7e00848e3f9f1abbe27f18","5e6cd6b54df24dbde59d4cdaffdf279173e886ea15016e2bd0dca5cf68ffa470","522bbc07c36b5f95f1d8fd427368d233cb3b336a278ad85a418021e0fce38890","7b8d7946a6694b07bfaccd1fad2dba7a84d3e349d9b9cbe71f85222f3d4f486d"),
3:("94ef8982e97b05427836639d45daeb88d46b8de3918d61bab4f444536388e739","1fc995f9c8c5f7e35d15f2b994b5d3121501a1d0c9d0aa7c5d6d0e2b92a26359","776b0eecacf0aaa1c6ab0d752487e47d9085be07241f4b7002f1cd4764fd9372","9e15a3a0707adda7cd5b319b21d24f7e1df38b64dc35c48034cb92800e1eb769","cdf8015424e5ebe81a0b709cd797a12db60cdb5f28ba9291f028be1a71ce3d18")}
NATIVE_PIN={
(1,1):"4813a0e91f4fa2b8f2a1c9c57849360d8c989b9a4ea70f4f2d4c23bcb51db5ca",
(1,2):"b5e190970c92928d2aec5cc337492c3b295c1911a0418492af1c926cbeb83b15",
(1,3):"48f7fefc2624dd8475040dd79fe3e22a7a8f41668c0f5dea245338f943fde7a0",
(1,35):"92eaeeafefb06ddd60feb120082445a603a1ff153b3401cc5c87c4296f099732",
(1,62):"f2e336479c322cde066d866208127ecd9966548dbf9c20454c01342d023e42d4",
(1,88):"086ae37fbcd0234025d1dd9637d72c344b73315622f59df87efde8d03a0c1c7a",
(1,119):"ee9a8f512a995b950e2dab21aba03efcd57d478bd06c0c370886b255b221e9d7",
(2,1):"cba46966ef615d3d27817272e9987d8e236d05eb0fb0fd7d7f6fd9da0d1f18ff",
(2,72):"77731ecd90e28018ef93bba0ac564232daf9c1074ccc1570a6e9e7032de335a4",
(3,1):"2f0597703f7cb5c29a65e47ac28c17a933e2c28da68416573d4afd0fcebe5a42",
(3,83):"a5fc4b32f0fa0e2425a313cf55504833af501435b3020809cb8578ad2b4720a6",
(3,121):"06d18ec79259d48522da52e7c13f107870978846726dad16adbbb79f80bd2982"}

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def qx_module():
    spec=importlib.util.spec_from_file_location("tw12qx_for_12qy",QX)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def verify(path=RECORD):
    obj=load(path)
    qx=qx_module()
    prior=qx.verify()
    qt=qx.qw_module().qv_module().qu_module().qt_module()
    base=qt.build_rows()
    captured={s["fascicle"]:s for s in load(QL)["sources"]}
    openings={(s["digital_fascicle"],s["pdf_page"]):s for s in load(QO)["original_juan_openings"]}
    if not (obj["stage"]=="12QE_OPEN"
        and obj["status"]=="ALL_1027_BODY_SOURCE_PAGES_HAVE_FIRSTPASS_VISUAL_SCREEN_NOT_FULL_TEXT_OR_TARGET_ABSENCE"
        and obj["physical_holding"]=="NLC411999003250_ONE_HOLDING"
        and [s["fascicle"] for s in obj["sources"]]==[1,2,3]):
        raise ValueError("12QY_SOURCE_OR_AUTHORITY_SCOPE_DRIFT")
    for s in obj["sources"]:
        f=s["fascicle"]
        pin=PINS[f]
        source=captured[f]
        pages=[r for r in base if r["fascicle"]==f]
        expected_count={1:119,2:72,3:121}[f]
        contacts={1:15,2:9,3:16}[f]
        navigation={1:[3,35,62,88,119],2:[1,72],3:[1,83,121]}[f]
        if not (s["source_pdf_sha256"]==source["source_pdf_sha256"]==pin[0]
            and s["original_pdf_rehashed"] is False
            and s["artifact_id"]==source["artifact_id"]=={1:11674078668,2:11673909003,3:11673474713}[f]
            and (s["zip_sha256"],s["status_sha256"],s["page_sha_chain"],s["contact_sha_chain"])==pin[1:]
            and s["source_pdf_pages"]==len(pages)==source["source_pdf_pages"]==expected_count
            and s["verified_original_jpegs"]==expected_count
            and s["verified_contacts"]==contacts==source["contact_sheets"]
            and s["contact_starts"]==list(range(1,expected_count+1,8))
            and s["hash_mismatches"]==0
            and s["body_preview_pages"]==expected_count-(2 if f==1 else 0)
            and s["non_body_prelim_pages"]==([1,2] if f==1 else [])
            and s["native_pages_opened_for_navigation_only"]==navigation
            and s["original_volume_candidates"]=={1:[1,2,3,4],2:[5],3:[6,7]}[f]
            and s["page_sha_pins"]=={str(p):h for (sf,p),h in NATIVE_PIN.items() if sf==f}):
            raise ValueError("12QY_ARCHIVE_MEMBER_HASHES_OR_PREVIEW_SCOPE_DRIFT")
        for r in pages:
            p=r["pdf_page"]
            nonbody=f==1 and p in (1,2)
            if not (r["source_pdf_sha256"]==pin[0]
                and r["target_screen_grade"]=="NOT_TARGET_SCREENED"
                and r["body_search_eligible"] is (not nonbody)
                and r["requires_native_target_screen"] is (not nonbody)):
                raise ValueError("PREEXISTING_IMAGE_GRADE_NOT_UNSCREENED")
            if not nonbody:
                expected=[1] if f==1 and p<35 else (
                    [1,2] if f==1 and p==35 else (
                    [2] if f==1 and p<62 else (
                    [3] if f==1 and p<88 else (
                    [3,4] if f==1 and p==88 else (
                    [4] if f==1 else (
                    [5] if f==2 else ([6] if p<83 else ([6,7] if p==83 else [7]))))))))
                if r["original_volume_candidates"]!=expected:
                    raise ValueError("OLD_JUAN_PAGE_NAVIGATION_CHANGED")
        for (sf,p),digest in NATIVE_PIN.items():
            if sf==f and any(o for o in openings.values() if o["digital_fascicle"]==f and o["pdf_page"]==p):
                if openings[f,p]["page_jpeg_sha256"]!=digest:
                    raise ValueError("DIRECT_ORIGINAL_LEAF_SHA_DIFFERS_FROM_12QO")
    r=obj["review_scope"]
    if not (r["member_hashes_rechecked_total"]==352
        and r["member_source_pages_rechecked"]==312
        and r["member_contact_sheets_rechecked"]==40
        and r["hash_mismatches"]==0
        and r["all_40_contacts_individually_visually_viewed"] is True
        and r["source_images_in_contacts"]==312
        and r["firstpass_body_pages_added"]==310
        and r["frontmatter_nonbody_pages_visual_previewed_but_not_target_screened"]==2
        and r["target_native_reviews_added"]==0
        and r["full_text_transcriptions_added"]==0
        and r["source_original_PDF_binary_rehashed"] is False
        and r["ocr_used"] is False
        and r["positive_target_glyph_attestations"]==0
        and r["negative_per_page_proofs"]==0
        and r["negative_entire_work_proven"] is False
        and r["contact_grade"]=="EIGHT_UP_DOWNSAMPLED_VISUAL_SCREEN_ONLY"
        and r["native_page_anchors_only_navigation"] is True):
        raise ValueError("12QY_UNEARNED_NEGATIVE_OR_NATIVE_GLYPH_PROMOTION")
    n=obj["original_volume_navigation"]
    if not (n["f1_old1_start"]==3
        and n["f1_old2_mixed_right_old1_left_old2"]==35
        and n["f1_old3_start"]==62
        and n["f1_old3_start_blank_right_previous_volume"] is False
        and n["f1_old4_mixed_right_old3_left_old4"]==88
        and n["f2_old5_start"]==1 and n["f3_old6_start"]==1
        and n["f3_old6_first_line_clipped"] is True
        and n["f3_old7_mixed_right_old6_left_old7"]==83
        and n["unreadable_year_from_f3_p1_not_treated_as_physical_glyph"] is True
        and openings[1,35]["right_leaf_has_previous_volume"] is True
        and openings[1,62]["right_leaf_has_previous_volume"] is False
        and openings[1,88]["right_leaf_has_previous_volume"] is True
        and openings[3,83]["right_leaf_has_previous_volume"] is True):
        raise ValueError("12QY_MIXED_LEAF_OR_TRUNCATED_YEAR_CAVEAT_LOST")
    after=copy.deepcopy(prior)
    after["montage_only_source_pages"]+=310
    after["not_target_screened_source_pages"]-=310
    after["body_not_even_firstpass_screened"]-=310
    for f,new_pages in [(1,117),(2,72),(3,121)]:
        after["per_fascicle"][str(f)]["fourup_only"]+=new_pages
    q=obj["queue_reconciliation"]
    if not (q["prior_preview_only_pages"]==prior["montage_only_source_pages"]==689
        and q["new_preview_only_pages"]==after["montage_only_source_pages"]==999
        and q["prior_body_never_firstpass"]==prior["body_not_even_firstpass_screened"]==310
        and q["new_body_never_firstpass"]==after["body_not_even_firstpass_screened"]==0
        and q["prior_source_not_target_screened"]==prior["not_target_screened_source_pages"]==312
        and q["new_source_not_target_screened"]==after["not_target_screened_source_pages"]==2
        and q["source_pages"]==after["source_pages"]==1030
        and q["body_pages"]==after["body_pages"]==1027
        and q["native_screened_source_pages"]==after["native_screened_source_pages"]==29
        and q["native_body_target_review_backlog"]==after["native_body_review_backlog"]==999
        and q["full_text_body_collation_backlog"]==after["body_full_text_collation_backlog"]==1027
        and q["original_target_folio"]==after["manuscript_target_folio"]=="UNLOCATED"
        and q["independent_physical_copy_increment"]==0
        and after["global_target_absence_proven"] is False
        and 29+999+2==1030
        and obj["invariants"]["product_r1"]=="CLOSED"
        and obj["invariants"]["algorithm_reopen_count"]==0):
        raise ValueError("12QY_TARGET_ABSENCE_OR_QUEUE_COUNT_PROMOTION")
    return after

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
