#!/usr/bin/env python3
"""12UP chronological volume seams and forward-only direct-image reading correction.

Structural repository gate. Source artifact JPEGs are not committed; operator
reverification may additionally call verify_original_atlas with extracted pages.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/research/MING-DATONG-YEHUOBIAN-12UP-OLD20-JUAN-SEAMS-FORWARD-CORRECTION-R1.json"
PRIOR = "docs/research/MING-DATONG-YEHUOBIAN-12UO-NLC-OLD20-TERMINAL-FOLIO-IMAGE-ANCHORS-R1.json"
QD = "docs/research/MING-DATONG-YEHUOBIAN-12QD-SHLIB-FIRSTPARTY-AND-NLC-OLD20-ATLAS-R1.json"
EXPECTED = {"1": "萬曆肆拾叄年乙卯卷十八",
            "81": "萬曆肆拾肆年丙辰十九",
            "137": "萬曆肆拾伍丁巳卷二十",
            "145": "萬曆野獲編二十卷紀事畢"}
def reject(msg):
    raise ValueError(msg)
def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def hex64(s):
    return isinstance(s, str) and len(s)==64 and all(k in "0123456789abcdef" for k in s)
def validate(data, prior, qd):
    if data.get("schema")!="TIANWEN-12UP-NLC-OLD20-JUAN-SEAM-PHYSICAL-COLLATION-FORWARD-CORRECTION-R1":
        reject("12UP schema mismatch")
    source=data["source_identity"]; up=qd["nlc_old20_direct_raster_atlas"]
    if source["source_id"]!=up["source_id"] or source["source_pdf_sha256_from_prior_12qd"]!=up["original_pdf_sha256"] or source["upstream_artifact_id"]!=up["artifact_id"] or source["upstream_run_id"]!=up["upstream_run"]:
        reject("upstream 12QD identity changed")
    if source.get("source_pdf_original_bytes_rehashed_this_batch") is not False or source.get("images_from_same_artifact_not_new_physical_witness") is not True or source.get("page_count")!=145:
        reject("unacquired PDF or source identity falsely promoted")
    if not hex64(source.get("upstream_artifact_zip_sha256")):
        reject("artifact ZIP fingerprint must be valid SHA")
    pages={str(p["pdf_page"]):p["page_jpeg_sha256"] for p in data.get("pages",[])}
    if set(pages)!={"1","80","81","82","136","137","138","145"} or not all(hex64(x) for x in pages.values()):
        reject("missing eight hashed source pages")
    correction=data.get("forward_only_correction",{})
    if prior["direct_image_anchors"][0]["manual_visible_text"]!="萬曆野獲編卷十八":
        reject("superseded prior text not present; investigate history")
    if correction.get("superseded_claim")!="12UO p001 manual_visible_text = 萬曆野獲編卷十八" or correction.get("corrected_p001_first_column")!=EXPECTED["1"]:
        reject("prior misreading not explicitly corrected")
    pts={str(x["page"]):x for x in data.get("anchors",[])}
    if set(pts)!=set(EXPECTED):
        reject("missing page title anchors")
    for p,text in EXPECTED.items():
        if pts[p].get("visible_title")!=text or pts[p].get("page_hash")!=pages[p]:
            reject("image-bound title misread or unbound")
    if [(pts[p]["juan"],pts[p].get("normalized_ce_year")) for p in ("1","81","137")]!=[(18,1615),(19,1616),(20,1617)]:
        reject("Wanli chronology / volume mismatch")
    if "NOT CONFIRMED" not in pts["81"].get("reading_scope","").replace("_"," "):
        reject("juan19 uncertain explicit 卷 glyph must remain qualified")
    seams=data.get("seams",[])
    if [(s.get("from_juan"),s.get("to_juan"),s.get("shared_pdf_page"),s.get("preceding_juan_half"),s.get("new_juan_half")) for s in seams]!=[
        (18,19,81,"RIGHT","LEFT"),(19,20,137,"RIGHT","LEFT")]:
        reject("original chronological page seams shifted")
    if any(s.get("fascicle_folio_number")!="UNBOUND" for s in seams):
        reject("unproven original folio number")
    keep=data["chronology_scope"]
    if any(keep.get(k) is not False for k in ("old_chronological_juan20_identical_to_1827_thematic_juan20","gaizao_louke_in_old20_verified","gaizao_louke_absent_from_old20_proven","full_145_page_target_text_collation_done","first_1827_unchanged_print_impression_verified","source_physically_independent_from_12qd")):
        reject("unproven target or print state")
    ac=data.get("accounting",{})
    if ac.get("prior_philological_misreading_forward_corrected")!=1 or ac.get("old20_juan_seams_located")!=2 or any(ac.get(x)!=0 for x in ("new_original_source_images","new_independent_physical_witnesses","new_target_glyph_votes","new_external_source_records","algorithm_reopens")):
        reject("historical witness accounting or algorithm reopened")
    if (ac.get("matrix_rows"),ac.get("audited"),ac.get("total_sources"),ac.get("formal_batches"),ac.get("genealogy_nodes"),ac.get("genealogy_edges"),ac.get("product"))!=(222,222,687,487,250,237,"CLOSED"):
        reject("project accounting unexpectedly changed")
    return {"status":"PASS","scan_seams":[81,137],"corrections":1,"ancient_new_witnesses":0,"chart_algorithm_reopens":0}
def verify_original_atlas(data, atlas, pages_dir):
    """Optional stronger operator check; never claim image bytes are in git."""
    sid=data["source_identity"]
    if atlas.get("source_sha256")!=sid["source_pdf_sha256_from_prior_12qd"] or atlas.get("pdf_page_count")!=145:
        reject("upstream PDF atlas identity mismatch")
    idx={int(x["pdf_page"]):x["sha256"] for x in atlas.get("pages",[])}
    if len(idx)!=145:
        reject("full atlas must index 145 pages")
    checked=0
    for p in data["pages"]:
        num=p["pdf_page"];target=p["page_jpeg_sha256"]
        if idx.get(num)!=target:
            reject("artifact page-atlas SHA mismatch")
        file=Path(pages_dir)/f"nlc-old20-p{num:03d}.jpg"
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=target:
            reject("actual raster bytes do not match SHA")
        checked+=1
    return {"checked_hashed_jpeg_pages":checked}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--atlas",type=Path)
    parser.add_argument("--pages-dir",type=Path)
    args=parser.parse_args()
    if (args.atlas is None)!=(args.pages_dir is None):
        parser.error("--atlas and --pages-dir must be supplied together")
    obj=load(ROOT/RECORD)
    result=validate(obj,load(ROOT/PRIOR),load(ROOT/QD))
    if args.atlas:
        result["operator_original_bytes"]=verify_original_atlas(obj,load(args.atlas),args.pages_dir)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":
    main()
