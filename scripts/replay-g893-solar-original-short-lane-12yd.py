#!/usr/bin/env python3
"""Replay exact authorized source ZIP/204 JPG SHA and 8 original RGB ROI digests; no OCR."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/research/TIANWEN-12YD-G893-D15-D17-DIRECT-SOLAR-PRINTED-FIVE-FEN-SEQUENCE-R1.json"
def digest(b):return hashlib.sha256(b).hexdigest()
def replay(archive,evidence=DOC):
 d=json.loads(Path(evidence).read_text(encoding="utf-8"));zrec=d["archive"]
 raw=Path(archive).read_bytes()
 if len(raw)!=zrec["size_bytes"] or digest(raw)!=zrec["sha256"]:raise ValueError("ZIP byte identity mismatch")
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  if z.testzip() is not None:raise ValueError("bad ZIP CRC")
  report=json.loads(z.read("report.json"))
  if report["book_cd"]!="GK00893_00" or len(report["physical_pages"])!=204:raise ValueError("wrong original source")
  pages={}
  for r in report["physical_pages"]:
   jpg=z.read("physical/"+r["page"]+".jpg")
   if r["download_ok"] is not True or len(jpg)!=r["bytes"] or digest(jpg)!=r["sha256"]:raise ValueError("original JPG mismatch "+r["page"])
   pages[r["page"]]=jpg
  for p in d["direct_original_pages"]:
   if digest(pages[p["page_id"]])!=p["jpeg_sha256"]:raise ValueError("source page changed "+p["page_id"])
  for roi in d["native_rgb_regions"]["regions"]:
   with Image.open(io.BytesIO(pages[roi["page_id"]])) as im:
    rgb=im.convert("RGB")
    if list(rgb.size)!=zrec["original_dimension"]:raise ValueError("source image dimensions")
    if digest(rgb.crop(tuple(roi["rect_px"])).tobytes())!=roi["sha256"]:raise ValueError("source pixel crop mismatch "+roi["role"])
 return {"status":"PASS","original_jpeg_sha_verified":204,"source_pages":2,"original_rgb_rois":8,"ocr":False,"automatic_numeric_adjudications":0}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--archive",type=Path,required=True)
 args=p.parse_args();print(json.dumps(replay(args.archive),ensure_ascii=False))
