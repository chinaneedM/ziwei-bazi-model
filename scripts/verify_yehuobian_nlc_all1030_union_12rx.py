#!/usr/bin/env python3
"""12RX: graded union of 1030 source PDF page IDs; no new original image reading."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RX-NLC411999003250-ALL1030-SOURCE-PAGE-GRADE-UNION-R1.json"
EXPECTED_TOTALS=(119,72,121,56,63,116,110,87,141,145)
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def fail(code): raise ValueError("12RX_"+code)
def count_range(pair): return pair[1]-pair[0]+1
def first_five_gate():
    p=ROOT/"scripts/verify_yehuobian_nlc_f1_f5_union_12rw.py"
    s=importlib.util.spec_from_file_location("audit12rw",p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m.verify()
def verify(record_path=RECORD, replacement_sources=None, prior_gate=True):
    d=read(record_path); replacement_sources=replacement_sources or {}
    if (d.get("batch"),d.get("parent_open_batch"),d.get("stage"),d.get("status"))!=(
        "12RX","12QE","12QE_OPEN",
        "ALL1030_SOURCE_PAGE_IDENTITIES_CLASSIFIED_BY_HISTORIC_BOUNDED_NATIVE_VS_PREVIEW_AND_PRELIMS_NO_NEW_PHYSICAL_READING"):
        fail("BATCH_SCOPE_OR_GRADE_DRIFT")
    paths=d["source"]
    wanted={
        "holding":"NLC411999003250_ONE_HOLDING",
        "capture":"12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION",
        "first_five_union":"12RW-NLC411999003250-F1-F5-NATIVE-PAGE-UNION",
        "f7_native":"12QR-NLC411999003250-F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS",
        "f7_preview":"12QS-NLC411999003250-F7-REMAINING90-MONTAGE-TRIAGE",
        "f8_preview":"12QU-NLC411999003250-F8-87-PAGE-CONTACT-TRIAGE",
        "f9_preview":"12QV-NLC411999003250-F9-141-PAGE-CONTACT-TRIAGE",
        "f6_f10_preview":"12QW-NLC411999003250-F6-F10-CONTACT-TRIAGE",
        "f10_native":"12QE-NLC-OLD20-V20-NINE-PAGE-BOUNDED-REVIEW",
        "all_body_firstpass":"12QY-NLC411999003250-F1-F3-ALL-BODY-FIRSTPASS",
        "graded_prior_baseline":"12QT-NLC411999003250-GRADED-TARGET-REVIEW-QUEUE"}
    if set(paths)!=set(wanted): fail("UPSTREAM_SCOPE_SET")
    for k,v in wanted.items():
        if k!="holding" and paths[k]!="docs/research/MING-DATONG-YEHUOBIAN-"+v+"-R1.json": fail("UPSTREAM_IDENTITY")
        if k=="holding" and paths[k]!=v: fail("HOLDING")
    up={k:read(replacement_sources.get(k,ROOT/paths[k])) for k in paths if k!="holding"}
    ql=up["capture"];rw=up["first_five_union"]; qr=up["f7_native"];qs=up["f7_preview"]
    qu=up["f8_preview"];qv=up["f9_preview"];qw=up["f6_f10_preview"]
    qe=up["f10_native"];qy=up["all_body_firstpass"];qt=up["graded_prior_baseline"]
    if prior_gate:
        result=first_five_gate()
        if result["native_source_identity_pages_f1_f5"]!=429: fail("PRIOR_UNION_REPLAY")
    if rw["accounting"]["first_five_unique_native_body_pages"]!=429 or len(rw["windows"])!=20:
        fail("PRIOR_FIVE_FASCICLE_UNION")
    if len(d["fascicles"])!=10 or len(ql["sources"])!=10:
        fail("FASCICLE_COUNT")
    native=set();preview=set();prelim=set()
    for n,(entry,total) in enumerate(zip(d["fascicles"],EXPECTED_TOTALS),1):
        src=next((x for x in ql["sources"] if x["fascicle"]==n),None)
        if not src or (entry["fascicle"],entry["source_pages"])!=(n,total) or (
                src["source_pdf_pages"],src["source_page_images"])!=(total,total):
            fail("FASCICLE_IDENTITY_OR_SIZE")
        for field,store in [("native_target_bounded_ranges",native),
                            ("preview_only_ranges",preview),("non_target_prelim_ranges",prelim)]:
            seq=entry[field]
            if not isinstance(seq,list): fail("RANGE_TYPE")
            for pair in seq:
                if not (isinstance(pair,list) and len(pair)==2 and
                        all(type(x)==int for x in pair) and 1<=pair[0]<=pair[1]<=total):
                    fail("SOURCE_PDF_RANGE")
                for p in range(pair[0],pair[1]+1):
                    key=(n,p)
                    if key in native or key in preview or key in prelim:
                        fail("REPEATED_OR_OVERLAPPING_PAGE")
                    store.add(key)
        if [p for f,p in sorted(native|preview|prelim) if f==n]!=list(range(1,total+1)):
            fail("FASCICLE_MISSING_PAGES")
        if n<=5:
            if [p for f,p in sorted(native) if f==n]!=list(range(3 if n==1 else 1,total+1)):
                fail("F1_F5_NATIVE_IDENTITY_MISMATCH")
        elif n==6 and [p for f,p in sorted(preview) if f==n]!=list(range(1,117)):
            fail("F6_PREVIEW_BOUNDARY")
        elif n==7 and ([p for f,p in sorted(native) if f==n]!=list(range(1,21))
                          or [p for f,p in sorted(preview) if f==n]!=list(range(21,111))):
            fail("F7_PREVIEW_NATIVE_GRADES")
        elif n in (8,9) and any(f==n for f,p in native):
            fail("NAVIGATION_IMAGES_NOT_NATIVE_TARGET_SCREENS")
        elif n==10 and ([p for f,p in sorted(native) if f==n]!=list(range(137,146))
                           or [p for f,p in sorted(preview) if f==n]!=list(range(1,137))):
            fail("F10_NATIVE_CONTEXT_136_BOUNDARY")
    if (len(native),len(preview),len(prelim))!=(458,570,2) or len(native|preview|prelim)!=1030:
        fail("WHOLE_HOLDING_GRADING_UNION")
    if (10,145) not in native or (10,136) not in preview or (1,1) not in prelim or (1,2) not in prelim:
        fail("NONBODY_OR_CONTEXT_GRADE")
    if not (len(qr["review"]["screened_pdf_pages"])==20
            and qr["source"]["source_page_count"]==110
            and qr["source"]["source_pdf_sha256"]==ql["sources"][6]["source_pdf_sha256"]
            and qr["source"]["artifact_id"]==ql["sources"][6]["artifact_id"]
            and qr["review"]["first_pdf_page"]==1 and qr["review"]["last_pdf_page"]==20
            and qr["review"]["source_digest_sequence_sha256"]==d["scoped_original_page_controls"]["f7_native_20_ordered_sha_chain"]
            and all(x["fascicle"]==7 and x["pdf_page"]==i
                    and isinstance(x["source_derived_page_jpeg_sha256"],str)
                    and len(x["source_derived_page_jpeg_sha256"])==64
                    and x["proof_target_absent_on_page"] is False
                    for i,x in enumerate(qr["review"]["screened_pdf_pages"],1))):
        fail("F7_NATIVE_SOURCE_HASH_AND_GRADE")
    f7pins=[x["source_derived_page_jpeg_sha256"] for x in qr["review"]["screened_pdf_pages"]]
    if hashlib.sha256("".join(f7pins).encode("ascii")).hexdigest()!=qr["review"]["source_digest_sequence_sha256"]:
        fail("F7_ORDERED_SOURCE_HASH_CHAIN")
    if not (qs["review_scope"]["start_pdf_page"]==21 and qs["review_scope"]["end_pdf_page"]==110
            and qs["review_scope"]["new_visually_screened_pages"]==90
            and qs["review_scope"]["full_text_line_by_line_collated"] is False
            and qs["source"]["source_pdf_sha256"]==ql["sources"][6]["source_pdf_sha256"]
            and qs["source"]["original_artifact_id"]==ql["sources"][6]["artifact_id"]):
        fail("F7_PREVIEW_SOURCE")
    if not (qu["visual_review"]["pages_in_preview"]==87
            and qu["visual_review"]["new_native_target_passage_reviews"]==0
            and qu["source"]["source_pdf_sha256"]==ql["sources"][7]["source_pdf_sha256"]
            and qu["source"]["artifact_id"]==ql["sources"][7]["artifact_id"]):
        fail("F8_PREVIEW_SOURCE")
    if not (qv["manual_review"]["page_start"]==1 and qv["manual_review"]["page_end"]==141
            and qv["manual_review"]["new_native_target_collations"]==0
            and qv["source"]["source_pdf_sha256"]==ql["sources"][8]["source_pdf_sha256"]
            and qv["source"]["artifact_id"]==ql["sources"][8]["artifact_id"]):
        fail("F9_PREVIEW_SOURCE")
    for n,count,prior in [(6,116,0),(10,136,9)]:
        src=next((s for s in qw["source_archives"] if s["fascicle"]==n),None)
        if (not src or src["source_pdf_sha256"]!=ql["sources"][n-1]["source_pdf_sha256"]
            or src["artifact_id"]!=ql["sources"][n-1]["artifact_id"]
            or src["new_preview_only_pages"]!=count or src["prior_native_target_screened_pages"]!=prior):
            fail("F6_F10_PREVIEW_ARCHIVE_AND_GRADE")
    old=qe["direct_page_review"]; rows=old["reviewed_pages"]
    if (qe["source"]["source_pdf_sha256"]!=ql["sources"][9]["source_pdf_sha256"]
        or qe["source"]["existing_capture_artifact_id"]!=ql["sources"][9]["artifact_id"]
        or (old["boundary_start_pdf_page"],old["boundary_end_pdf_page"])!=(137,145)
        or [p["pdf_page"] for p in rows]!=list(range(136,146))
        or old["preceding_context_pdf_page"]!=136 or old["reviewed_nine_page_unit_complete"] is not True
        or old["heading_start_exact"]!=d["scoped_original_page_controls"]["f10_p137_original_juan20_heading"]
        or old["end_exact"]!=d["scoped_original_page_controls"]["f10_p145_colophon_text"]
        or rows[1]["derived_jpeg_sha256"]!=d["scoped_original_page_controls"]["f10_p137_jpeg_sha256"]
        or rows[-1]["derived_jpeg_sha256"]!=d["scoped_original_page_controls"]["f10_p145_colophon_jpeg_sha256"]
        or old["target_not_in_any_other_old20_volume"]!="UNRESOLVED"):
        fail("F10_NATIVE_PAGE_AND_COLOPHON_BINDING")
    if qw["grade_rules"]["f10_colophon_non_body_page"]!=145 or (
        qw["grade_rules"]["f10_native_bounded_pages"]!="137..145"):
        fail("F10_NONBODY_CHRONICLE_BOUNDARY")
    if (qy["queue_reconciliation"]["source_pages"],qy["queue_reconciliation"]["body_pages"],
        qy["queue_reconciliation"]["new_body_never_firstpass"],
        qy["queue_reconciliation"]["native_screened_source_pages"])!=(1030,1027,0,29):
        fail("INHERITED_FIRSTPASS_GRADE")
    if (qt["summary"]["native_screened_source_pages"]!=29 or
        qt["summary"]["per_fascicle"]["7"]["native_screens"]!=20 or
        qt["summary"]["per_fascicle"]["10"]["native_screens"]!=9):
        fail("PRE_NATIVE_BASELINE_MISMATCH")
    a=d["accounting"]
    if a!={"source_pdf_pages":1030,"body_pages":1027,
        "source_pages_with_prior_bounded_native_target_screen":458,
        "body_pages_with_prior_bounded_native_target_screen":457,
        "preview_only_pages":570,"non_target_first_fascicle_prelims":2,
        "terminal_fascicle10_colophon_native_bounded_nonbody_pages":1,
        "all_body_pages_have_at_least_preview_firstpass":True,
        "all_body_pages_fulltext_collation_pending":1027,
        "source_pages_with_new_original_images_viewed_in_this_batch":0,
        "source_pdf_rehashed_in_this_batch":False}:
        fail("COUNTS_OR_FULLTEXT_FIREWALL")
    s=d["scoped_original_page_controls"]
    if not (s["f7_native_first"]==1 and s["f7_native_last"]==20 and
         s["f10_native_first"]==137 and s["f10_native_last"]==145 and
         all(s[k] is True for k in [
          "f10_p136_prior_original_jpeg_context_only_not_target_reviewed",
          "f7_f10_original_native_review_is_only_bounded_heading_target_screen",
          "no_direct_old20_gaizao_louke_target_attested",
          "original20_chronicle_juan_not_equivalent_to_1827_thematic30_juan"])):
        fail("PHILOLOGICAL_AND_CONTEXT_GRADE")
    if (d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"] or
         d["invariants"]!={"matrix":"222/222","repaired_provenance":"45/45",
          "external_sources":"647+7=654","md_g03":"OPEN",
          "hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","product_r1":"CLOSED",
          "chart_algorithm_defects":0,"algorithm_reopens":0}):
        fail("TRANSMISSION_OR_PRODUCT_STATE")
    return {"batch":"12RX","source_pages":1030,"bounded_native_source_pages":458,
            "bounded_native_body_pages":457,"preview_only_body_pages":570,
            "unreviewed_prelim_pages":2,"full_text_collation_body_backlog":1027,
            "source_image_reviews_added":0,
            "algorithm_changes":0}
if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
