#!/usr/bin/env python3
"""Replay SHA-bound G893 12XX source pixels; cannot recognize ancient glyphs automatically."""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"docs/research/TIANWEN-12XX-G893-L124-DIRECT-ORIGINAL-JI-XINGDU-GLYPH-R1.json"

def require(t,msg):
    if not t: raise ValueError(msg)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def replay(archive,evidence=EVIDENCE):
    d=json.loads(Path(evidence).read_text(encoding="utf-8"))
    require(d["schema"]=="TIANWEN-12XX-G893-L124-DIRECT-ORIGINAL-JI-XINGDU-GLYPH-R1","unexpected source evidence")
    require(d["physical_source"]["catalog_book_code"]=="GK00893_00","wrong source identity")
    archive=Path(archive)
    require(archive.is_file() and archive.stat().st_size<100_000_000,"missing/oversized archive")
    raw=archive.read_bytes()
    src=d["archived_original"]
    require(len(raw)==src["archive_bytes"] and digest(raw)==src["archive_sha256"],"original archive content/sha mismatched")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(z.testzip() is None,"archive member CRC mismatch")
        report=json.loads(z.read("report.json"))
        require(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"wrong 204-page original report")
        require(src["verified_source_jpegs"]==src["reported_source_jpegs"]==204,"G893 original source total changed")
        originals={}
        for row in report["physical_pages"]:
            pid=row["page"]
            require(pid not in originals,"duplicated physical original")
            jpg=z.read(f"physical/{pid}.jpg")
            require(row["download_ok"] is True and len(jpg)==row["bytes"] and digest(jpg)==row["sha256"],"G893 source original mismatch "+pid)
            originals[pid]=jpg
        require(len(originals)==204,"original JPG count incorrect")
        pages={"035b":d["source_page"],"018b":d["structural_header"]}
        for pid,record in pages.items():
            require(digest(originals[pid])==record["source_original_sha256"],"target JPG hash mismatched "+pid)
        for region in d["original_rgb_pixel_regions"]["regions"]:
            pid=region["page_id"]; image=Image.open(io.BytesIO(originals[pid])).convert("RGB")
            require(image.size==(1150,2000),"native original dimensions changed "+pid)
            rect=region["rect_px"];l,t,r,b=rect
            require(0<=l<r<=1150 and 0<=t<b<=2000,"invalid region bounds")
            require(digest(image.crop((l,t,r,b)).tobytes())==region["rgb_pixel_sha256"],"original RGB ROI hash mismatched "+region["role"])
    return {"status":"PASS","original_jpgs_sha256_checked":204,"original_rgb_rois_checked":3,"human_glyph_readings_auto_authorized":0,"mechanical_numeric_adjudications":0}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive",type=Path,required=True)
    args=ap.parse_args()
    print(json.dumps(replay(args.archive),ensure_ascii=False))

if __name__=="__main__":main()
