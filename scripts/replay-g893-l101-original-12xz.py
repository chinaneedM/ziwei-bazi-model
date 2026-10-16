#!/usr/bin/env python3
"""Replay authenticated G893 original L101 image regions. No OCR or numeric adjudication."""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/research/TIANWEN-12XZ-G893-L101-DIRECT-FULL-GLYPH-R1.json"
def need(ok,msg):
    if not ok: raise ValueError(msg)
def hash256(b):
    return hashlib.sha256(b).hexdigest()
def replay(archive,evidence=DOC):
    d=json.loads(Path(evidence).read_text(encoding="utf-8"))
    need(d["schema"]=="TIANWEN-12XZ-G893-L101-SOURCE-ORIGINAL-FULL-LITERAL-FIELD-R1","wrong G893 original evidence")
    need(d["catalog_book_code"]=="GK00893_00","wrong physical source")
    archive=Path(archive)
    need(archive.is_file() and archive.stat().st_size<100_000_000,"source ZIP missing or overlarge")
    payload=archive.read_bytes()
    need(len(payload)==d["archive"]["bytes"] and hash256(payload)==d["archive"]["sha256"],"source ZIP SHA")
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        need(z.testzip() is None,"source ZIP CRC")
        report=json.loads(z.read("report.json"))
        need(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"wrong original source report")
        originals={}
        for row in report["physical_pages"]:
            pid=row["page"]
            need(pid not in originals and row["download_ok"] is True,"duplicate original page")
            raw=z.read("physical/"+pid+".jpg")
            need(len(raw)==row["bytes"] and hash256(raw)==row["sha256"],"original JPEG SHA: "+pid)
            originals[pid]=raw
        need(len(originals)==d["archive"]["original_jpg_sha256_verified"]==204,"source JPG count")
        expected={"032b":d["source_page"]["source_original_sha256"],"018b":d["structural_header"]["source_original_sha256"],"032a":d["neighbor"]["previous_original_jpeg_sha256"]}
        for pid,dig in expected.items():
            need(hash256(originals[pid])==dig,"specific source folio mismatched: "+pid)
        rois=d["original_rgb_pixel_regions"]["regions"]
        need(len(rois)==5 and len({(r["page_id"],r["role"]) for r in rois})==5,"missing full target/neighbor region")
        for region in rois:
            pid=region["page_id"]
            need(pid in expected,"region outside original folios")
            with Image.open(io.BytesIO(originals[pid])) as im:
                im.verify()
            with Image.open(io.BytesIO(originals[pid])) as im:
                image=im.convert("RGB")
            need(image.size==(1150,2000),"native image dimensions")
            rect=region["rect_px"]
            need(len(rect)==4 and all(type(x) is int for x in rect),"ROI geometry")
            l,t,r,b=rect
            need(0<=l<r<=1150 and 0<=t<b<=2000,"ROI bounds")
            need(hash256(image.crop((l,t,r,b)).tobytes())==region["rgb_pixel_sha256"],"native original pixel hash: "+str(region["role"]))
    return {"status":"PASS","physical_holding_count":1,"original_jpg_sha_matches":204,"native_rgb_roi_replays":5,"human_glyph_reading_auto_authorized":0,"cross_witness_mechanical_decisions":0}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(replay(args.archive),ensure_ascii=False))
