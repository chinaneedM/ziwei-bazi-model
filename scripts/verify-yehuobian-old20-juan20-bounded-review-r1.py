#!/usr/bin/env python3
"""12UQ: 9-page bounded old-20 source review. No OCR or target inference."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UQ-OLD20-JUAN20-NINE-PAGE-SCOPED-REVIEW-R1.json"
PRIOR = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12UP-OLD20-JUAN-SEAMS-FORWARD-CORRECTION-R1.json"
QD = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12QD-SHLIB-FIRSTPARTY-AND-NLC-OLD20-ATLAS-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
PROHIBITED = (
    "old_chronological_juan20_equals_1827_thematic_juan20",
    "exact_gaizao_louke_chapter_heading_located",
    "target_absent_from_this_juan_proven",
    "target_absent_from_all_145_pages_proven",
    "source_impression_date_from_manuscript_year",
    "entire_9_pages_fully_transcribed",
    "original_folio_number_attested",
    "new_independent_source_witness_added",
    "clock_rule_or_algorithm_reopened",
)
def load(file: Path):
    return json.loads(file.read_text(encoding="utf-8"))
def fail(message: str):
    raise ValueError(message)
def is_sha(v):
    return isinstance(v,str) and len(v)==64 and all(c in "0123456789abcdef" for c in v)
def validate(a,up,qd,state):
    if a.get("schema") != "TIANWEN-12UQ-NLC-OLD20-JUAN20-NINE-PAGE-SCOPED-REVIEW-R1":
        fail("12UQ schema")
    s=a["source"]
    prior=qd["nlc_old20_direct_raster_atlas"]
    if (s.get("source_id"),s.get("source_pdf_sha256_from_prior"),s.get("artifact_id"),s.get("upstream_run_id")) != (
        prior["source_id"],prior["original_pdf_sha256"],prior["artifact_id"],prior["upstream_run"]):
        fail("12QD artifact/source identity")
    if (s.get("source_pdf_original_bytes_rehashed_now"),s.get("same_original_witness_as_12qd"))!=(False,True):
        fail("original PDF and same-source limits")
    if s.get("original_pdf_page_count")!=145 or s.get("atlas_index_entries")!=145 or not is_sha(s.get("zip_sha256_verified")):
        fail("source atlas counts")
    sc=a["scope"]
    pages=sc["pages"]
    if (sc.get("first_page"),sc.get("last_page"),sc.get("pages_opened_manually"),sc.get("page_jpegs_sha256_rehashed"))!=(137,145,9,9):
        fail("nine-page visible span")
    if [x["pdf_page"] for x in pages]!=list(range(137,146)):
        fail("nine-page list incomplete")
    if sc.get("first_leaf_half")!="PDF137_LEFT_IS_OLD_JUAN20;RIGHT_IS_OLD_JUAN19" or sc.get("last_leaf_half")!="PDF145_RIGHT_IS_OLD_JUAN20;LEFT_IS_BLANK":
        fail("double-leaf boundary")
    if any(sc.get(k) is not False for k in ("whole_page_text_transcribed","whole_145_page_pdf_read_for_target","ocr_used")):
        fail("false complete review")
    for x in pages:
        if not is_sha(x.get("jpg_sha256")) or x.get("visually_screened") is not True:
            fail("page hashes missing/invalid")
    index={x["pdf_page"]:x["jpg_sha256"] for x in pages}
    before={x["pdf_page"]:x["page_jpeg_sha256"] for x in up["pages"]}
    for n in (137,138,145):
        if index[n]!=before[n]:
            fail("12UP old source page SHA conflict")
    m=a["month_heading_anchors"]
    if [(x["page"],x["side"],x["visible"],x["role"]) for x in m] != [
        (137,"LEFT","萬曆肆拾伍丁巳卷二十","1617_OLD_JUAN20_START"),
        (137,"LEFT","春正月","MONTH_1"),
        (139,"LEFT","二月","MONTH_2"),
        (141,"LEFT","三月","MONTH_3"),
        (143,"LEFT","四月","MONTH_4"),
        (145,"RIGHT","六月","MONTH_6"),
        (145,"RIGHT","萬曆野獲編二十卷紀事畢","OLD_JUAN20_TERMINUS")]:
        fail("manual month/head or page scope changed")
    ctx=a["astronomical_context"]
    if ctx.get("scanned_pages")!=[138,139,140] or ctx.get("same_text_as_later_thematic_gaizao_louke")!="NOT_DEMONSTRATED" or ctx.get("four_locus_variant_values_bound") is not False or ctx.get("historical_clock_rule_preference")!="NONE_AUTHORIZED":
        fail("calendar-context thematic identification not attested")
    if any(a["inference_guards"].get(k) is not False for k in PROHIBITED):
        fail("scope/firewall overclaim")
    if a["outcome"] if "outcome" in a else False:
        fail("unexpected outcome bypass")
    x=a["accounting"];h=state["historical_audit"]
    if (x["matrix_rows"],x["audited_rows"],x["provenance_repairs"],x["total_sources"],x["formal_batches"],x["graph_nodes"],x["graph_edges"]) != (
        h["row_count"],h["audited_row_count"],h["repaired_provenance_metadata_defect_count"],h["external_source_registry_total_unique_count"],len(h["completed_batches"]),250,237):
        fail("source/accounting state divergence")
    if any(x[k]!=0 for k in ("source_images_new","independent_glyph_votes_new","ancient_witnesses_new","algorithm_reopens")):
        fail("false new independent witness or algorithm reopen")
    if state["invariants"]["deterministic_fusion_chart_product_r1"]!="CLOSED" or state["invariants"]["algorithm_reopen_count"]!=0 or x["product"]!="CLOSED":
        fail("product reopened without evidence")
    return {"result":"PASS","bounded_pages":"137-145","verified_page_hashes":9,"new_independent_witnesses":0,"algorithm_reopens":0}
def verify_zip(a,zip_path):
    want=a["source"]["zip_sha256_verified"]
    h=hashlib.sha256()
    with open(zip_path,"rb") as file:
        while True:
            chunk=file.read(1024*1024)
            if not chunk:break
            h.update(chunk)
    if h.hexdigest()!=want:
        fail("artifact ZIP SHA mismatch")
    with ZipFile(zip_path) as z:
        manifest=json.loads(z.read("page-atlas.json").decode("utf-8"))
        if manifest.get("source_sha256")!=a["source"]["source_pdf_sha256_from_prior"] or manifest.get("pdf_page_count")!=145:
            fail("artifact raw manifest identity")
        idx={p["pdf_page"]:p["sha256"] for p in manifest["pages"]}
        if len(idx)!=145:fail("incomplete original atlas")
        for p in a["scope"]["pages"]:
            n=p["pdf_page"];target=p["jpg_sha256"]
            original=z.read("pages/nlc-old20-p%03d.jpg"%n)
            if idx.get(n)!=target or hashlib.sha256(original).hexdigest()!=target:
                fail("raw JPEG / atlas SHA mismatch at page %d"%n)
    return 9
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--artifact-zip",type=Path)
    args=parser.parse_args()
    data=load(REC)
    result=validate(data,load(PRIOR),load(QD),load(STATE))
    if args.artifact_zip:
        result["replayed_jpeg_bytes"]=verify_zip(data,args.artifact_zip)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":
    main()
