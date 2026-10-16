#!/usr/bin/env python3
"""Replay 12YA source ZIP/204 JPEG SHA and six original RGB region SHA; no OCR."""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/research/TIANWEN-12YA-G893-D16-SOLAR-HEADER-AND-EXTERNAL-ARITHMETIC-R1.json"
def require(ok,why):
    if not ok: raise ValueError(why)
def sha256(b):
    return hashlib.sha256(b).hexdigest()
def replay(archive,evidence_path=DOC):
    d=json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    require(d["schema"]=="TIANWEN-12YA-G893-D16-SOLAR-PRINTED-COLUMNS-AND-EXTERNAL-ARITHMETIC-CONTROL-R1","wrong G893 D16 schema")
    require(d["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","wrong source copy")
    archive=Path(archive)
    require(archive.is_file() and archive.stat().st_size<100_000_000,"original ZIP missing/oversize")
    payload=archive.read_bytes();e=d["archive"]
    require(len(payload)==e["byte_count"] and sha256(payload)==e["zip_sha256"],"source archive ZIP bytes/SHA mismatch")
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        require(z.testzip() is None,"source original ZIP CRC failure")
        report=json.loads(z.read("report.json"))
        require(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"wrong original 204-page report")
        pages={}
        for p in report["physical_pages"]:
            pid=p["page"]
            require(pid not in pages and p["download_ok"] is True,"duplicate/missing original source page")
            raw=z.read("physical/"+pid+".jpg")
            require(len(raw)==p["bytes"] and sha256(raw)==p["sha256"],"original JPG SHA mismatch "+pid)
            pages[pid]=raw
        require(len(pages)==e["source_jpegs_sha256_replayed"]==204,"incomplete physical original")
        target={x["page_id"]:x for x in d["direct_original_page_evidence"]}
        require(set(target)=={"001a","002a","002b"},"scope of three source pages altered")
        for pid,rec in target.items():
            require(sha256(pages[pid])==rec["jpeg_sha256"],"specific source JPEG changed "+pid)
        crops=d["original_rgb_roi"]["regions"]
        require(len(crops)==6,"six cropped source ROIs required")
        for row in crops:
            require(row["page_id"] in target,"source ROI outside original pages")
            with Image.open(io.BytesIO(pages[row["page_id"]])) as image:
                rgb=image.convert("RGB")
                require(rgb.size==(1150,2000),"source native image size changed")
                l,t,r,b=row["rect_px"]
                require(0<=l<r<=1150 and 0<=t<b<=2000,"bad source geometry")
                require(sha256(rgb.crop((l,t,r,b)).tobytes())==row["sha256"],"source RGB crop SHA mismatch "+row["role"])
    return {"result":"PASS","source_originals_sha_verified":204,"new_3_source_pages_checked":3,"new_native_roi_digest_checks":6,"new_complete_original_target_columns":0,"automatic_glyph_readings":0,"numeric_adjudications":0}
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(replay(args.archive),ensure_ascii=False))
