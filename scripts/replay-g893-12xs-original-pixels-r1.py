#!/usr/bin/env python3
"""Offline replay of G893 12XS native JPEG pixels. Never authorizes numeric collation."""
import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"docs/research/TIANWEN-12XS-G893-THREE-TARGET-PIXEL-ROI-GATES-R1.json"

def require(condition,message):
 if not condition:raise ValueError(message)
def sha256(data):
 return hashlib.sha256(data).hexdigest()
def rgb_crop_digest(image,box):
 require(isinstance(box,list) and len(box)==4 and all(type(x) is int for x in box),"invalid ROI geometry")
 l,t,r,b=box
 require(0<=l<r<=image.width and 0<=t<b<=image.height,"ROI beyond original image")
 return sha256(image.crop((l,t,r,b)).tobytes())

def replay(archive_path,evidence_path=EVIDENCE):
 archive_path=Path(archive_path)
 evidence=json.loads(Path(evidence_path).read_text(encoding="utf-8"))
 require(evidence["schema"]=="TIANWEN-12XS-G893-TARGET-SOURCE-ROI-BOUND-NO-FIELD-OR-NUMERIC-DECISION-R1","unexpected research evidence")
 require(evidence["book_cd"]=="GK00893_00" and evidence["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893","wrong original source")
 require(archive_path.is_file() and archive_path.stat().st_size<100_000_000,"archive missing or too large")
 require(sha256(archive_path.read_bytes())==evidence["archive"]["archive_zip_sha256"],"archive original ZIP SHA-256 mismatch")
 with zipfile.ZipFile(archive_path) as z:
  require(z.testzip() is None,"original archive ZIP CRC failed")
  report=json.loads(z.read("report.json"))
  allpages=report["physical_pages"]
  require(len(allpages)==evidence["archive"]["source_original_jpgs_total"]==204,"source original 204 page count mismatch")
  index={a["page"]:a for a in allpages}
  require(len(index)==204 and all(re.fullmatch(r"[0-9]{3}[ab]",k) for k in index),"original source page IDs not unique")
  raws={}
  for pid,item in index.items():
   info=z.getinfo("physical/"+pid+".jpg")
   require(info.file_size<=2_000_000,"unbounded source JPEG")
   raw=z.read(info.filename)
   require(sha256(raw)==item["sha256"],"original source JPG SHA-256 mismatch: "+pid)
   raws[pid]=raw
  require(evidence["archive"]["source_jpg_digest_matches"]==204,"unverified manifest assertion")
  observed=0
  for item in evidence["reviews"]:
   require(item["field_identity_positive"] is False and item["field_literal"] is None and item["numeric_value"] is None and item["negative_absence_proven"] is False,"region promoted to historical number or absence")
   for region_key,pid_key,hash_key in (
    ("day_heading_region","target_page_id","target_original_jpeg_sha256"),
    ("table_candidate_region","target_page_id","target_original_jpeg_sha256"),
    ("source_header_region","header_page_id","header_original_jpeg_sha256"),
   ):
    pid=item[pid_key]
    require(pid in index and item[hash_key]==index[pid]["sha256"],"ROI page original identity mismatch")
    binary=raws[pid]
    img=Image.open(io.BytesIO(binary))
    img.verify()
    img=Image.open(io.BytesIO(binary)).convert("RGB")
    require(img.size==(1150,2000),"source original dimensions mismatch")
    real=rgb_crop_digest(img,item[region_key]["rect_px"])
    require(real==item[region_key]["rgb_pixel_sha256"],"original pixel digest mismatch: "+pid+"/"+region_key)
    observed+=1
 require(len(evidence["reviews"])==3 and observed==9,"original target 3x3 ROI count mismatch")
 return {"status":"PASS","original_source_jpgs_sha256_matched":204,"native_rgb_rois_sha256_matched":9,"source_scoped_numeric_decisions_authorized":0}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--archive",type=Path,required=True,help="separately held original image ZIP, not stored in public repository")
 parser.add_argument("--evidence",type=Path,default=EVIDENCE)
 args=parser.parse_args()
 print(json.dumps(replay(args.archive,args.evidence),ensure_ascii=False))
if __name__=="__main__":
 main()
