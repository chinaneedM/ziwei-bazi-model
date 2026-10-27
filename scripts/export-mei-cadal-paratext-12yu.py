#!/usr/bin/env python3
"""12YU bounded Mei CADAL06054965 scan *paratext* check: source identity only.

The contact atlas suggests potentially informative cover, source details,
printed volume boundaries and terminal matter. Export exact original pixels;
human review is separate. Historical printing dates are NOT inferred by script.
"""
from __future__ import annotations
import hashlib, io, json, subprocess, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

OUT=Path("research-12yu-mei-paratext");OUT.mkdir(exist_ok=True)
NAME="CADAL06054965 大統歷志·卷三~卷四.djvu"
URL="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(NAME,safe="")
DEST=OUT/NAME
SIZE=4259929
SHA256="195c3ff35ae297b43fad6bb597d46dd046b109bee4c8eae8732fba336adab800"
req=urllib.request.Request(URL,headers={"User-Agent":"TianwenHistoricalSourceParatextResearch/1.0 (public domain Commons original; no OCR)"})
with urllib.request.urlopen(req,timeout=120) as response,DEST.open("wb") as w:
 while True:
  piece=response.read(1<<20)
  if not piece: break
  w.write(piece)
raw=DEST.read_bytes()
assert len(raw)==SIZE and hashlib.sha256(raw).hexdigest()==SHA256 and raw.startswith(b"AT&T"),"source immutable SHA mismatch"
count=int(subprocess.run(["djvused",str(DEST),"-e","n"],capture_output=True,text=True,check=True).stdout.strip())
assert count==126,count
pages=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,65,66,67,68,119,120,121,122,123,124,125,126]
manifest={"schema":"TIANWEN-12YU-MEI-CADAL06054965-NATIVE-PARATEXT-ATLAS-R1","source_name":NAME,"source_url":URL,"source_bytes":SIZE,"source_sha256":SHA256,"source_pages":count,"pages_exported":pages,"original_impression_date":"UNVERIFIED_BY_CODE","origins":"SOURCE_JPEG_DJVU_PIXEL_ATLAS_ONLY_DO_NOT_INFER_TEXT","ocr_used":False,"original_loci_read_by_script":0,"scan":[]}
for n in pages:
 run=subprocess.run(["ddjvu","-format=pnm",f"-page={n}",str(DEST)],capture_output=True,check=True)
 im=Image.open(io.BytesIO(run.stdout)).convert("RGB")
 path=OUT/f"paratext_{n:03d}.png"
 im.save(path,optimize=True)
 rec={"page":n,"image_file":path.name,"width":im.width,"height":im.height,
      "rgb_sha256":hashlib.sha256(im.tobytes()).hexdigest(),
      "png_sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
 manifest["scan"].append(rec)
 print("12YU NATIVE",n,im.width,im.height,rec["png_sha256"],flush=True)
(OUT/"paratext-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
print("12YU PASS original page images exported; no impression-year or textual verdict",flush=True)
