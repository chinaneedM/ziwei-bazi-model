#!/usr/bin/env python3
"""Read an authorized G893 original ZIP and replay 204 image SHA plus 12YC native RGB crops; NO OCR."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def h(b): return hashlib.sha256(b).hexdigest()
def replay(archive,evidence=ROOT/"docs/research/TIANWEN-12YC-G893-L8-L159-L35-L132-ORIGINAL-PAIR-GLYPH-COLLATION-R1.json"):
    d=json.loads(Path(evidence).read_text(encoding="utf-8"))
    raw=Path(archive).read_bytes(); zmeta=d["archive"]
    if len(raw)!=zmeta["byte_count"] or h(raw)!=zmeta["zip_sha256"]:raise ValueError("ZIP size or sha mismatch")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip() is not None:raise ValueError("ZIP CRC mismatch")
        report=json.loads(z.read("report.json"))
        if report["book_cd"]!="GK00893_00" or len(report["physical_pages"])!=204:raise ValueError("wrong original copy/pages")
        saved={}
        for row in report["physical_pages"]:
            page=row["page"]
            orig=z.read("physical/"+page+".jpg")
            if not row["download_ok"] or len(orig)!=row["bytes"] or h(orig)!=row["sha256"]:raise ValueError("original page sha "+page)
            saved[page]=orig
        for p in d["original_page_evidence"]:
            if h(saved[p["page_id"]])!=p["jpeg_sha256"]:raise ValueError("target original jpeg "+p["page_id"])
        for row in d["original_rgb_roi"]["regions"]:
            with Image.open(io.BytesIO(saved[row["page_id"]])) as image:
                rgb=image.convert("RGB")
                if list(rgb.size)!=zmeta["original_jpeg_dimensions"]:raise ValueError("unexpected original image geometry")
                l,t,r,b=row["rect_px"]
                if not (0<=l<r<=rgb.width and 0<=t<b<=rgb.height):raise ValueError("ROI out of page")
                if h(rgb.crop((l,t,r,b)).tobytes())!=row["sha256"]:raise ValueError("native crop mismatch "+row["role"])
    return {"result":"PASS","original_jpegs_sha_verified":204,"original_page_sources":len(d["original_page_evidence"]),"original_native_rois_sha_verified":len(d["original_rgb_roi"]["regions"]),"automatic_glyph_readings":0,"general_numeric_symmetry_rule_awards":0}
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(replay(args.archive),ensure_ascii=False))
