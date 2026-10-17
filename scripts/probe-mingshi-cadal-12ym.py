#!/usr/bin/env python3
"""12YM public-domain CADAL DjVu acquisition/byte-bound page atlas; no OCR claims."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAME = "CADAL06056955_明史·卷三十二~卷三十四.djvu"
URL = "https://upload.wikimedia.org/wikipedia/commons/7/76/" + urllib.parse.quote(NAME, safe="~")
EXPECTED_SIZE = 6001348
EXPECTED_SHA1 = "903ac33c6409ff95a5eff64c19b6eacd90f41a5e"
DEST = Path("source-mingshi-cadal-12ym")
DEST.mkdir(exist_ok=True)
source = DEST / NAME
for attempt in range(3):
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "TianwenHistoricalAudit/1.0 (public domain source verification)"})
        with urllib.request.urlopen(req, timeout=85) as resp, source.open("wb") as f:
            while True:
                chunk = resp.read(1024 * 512)
                if not chunk: break
                f.write(chunk)
        break
    except Exception as e:
        print("12YM public source fetch error, attempt", attempt + 1, str(e), flush=True)
        if attempt == 2: raise
        time.sleep(5)
data = source.read_bytes()
h1 = hashlib.sha1(data).hexdigest()
h256 = hashlib.sha256(data).hexdigest()
if len(data) != EXPECTED_SIZE or h1 != EXPECTED_SHA1:
    raise RuntimeError(f"SOURCE_DIGEST_MISMATCH length={len(data)} sha1={h1}")
print("12YM SOURCE_BYTES_VERIFIED", len(data), h1, h256, flush=True)
dump = subprocess.run(["djvudump", str(source)], capture_output=True, text=True, check=True).stdout
if not dump.strip(): raise RuntimeError("DJVU_DUMP_EMPTY")
pages = subprocess.run(["djvused", str(source), "-e", "n"], capture_output=True, text=True, check=True).stdout.strip()
if pages != "168": raise RuntimeError(f"UNEXPECTED_PAGE_COUNT {pages}")
print("12YM ORIGINAL_PAGE_COUNT_VERIFIED", pages, flush=True)
report = {"schema":"TIANWEN-12YM-CADAL-ORIGINAL-IMAGE-ACQUISITION-R1",
          "source_url":URL, "catalog_id":"CADAL06056955", "byte_size":len(data), "sha1":h1, "sha256":h256, "pages":168,
          "original_target_glyphs_adjudicated":0, "independent_physical_witnesses_added":0,
          "caption":"Contact atlases are locator-only; do not use thumbnails to decide small original glyphs."}
(DEST/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
cell_w,cell_h=220,337
for start in range(1,169,20):
    atlas=Image.new("RGB",(cell_w*5,cell_h*4),"white")
    draw=ImageDraw.Draw(atlas)
    for idx,page in enumerate(range(start,min(168,start+19)+1)):
        ppm=DEST/f"page_{page:03d}.ppm"
        subprocess.run(["ddjvu","-format=ppm","-page="+str(page),"-scale=190",str(source),str(ppm)],check=True,stdout=subprocess.DEVNULL)
        with Image.open(ppm) as image:
            image.thumbnail((cell_w-6,cell_h-31))
            x=(idx%5)*cell_w+(cell_w-image.width)//2
            y=(idx//5)*cell_h+25
            atlas.paste(image,(x,y))
        ppm.unlink()
        draw.text(((idx%5)*cell_w+8,(idx//5)*cell_h+7),f"CADAL 06056955 : DjVu page {page:03d}",fill="black")
    target=DEST/f"atlas_{start:03d}_{min(168,start+19):03d}.jpg"
    atlas.save(target,quality=78,optimize=True)
    print("12YM ATLAS",target.name,"sha256",hashlib.sha256(target.read_bytes()).hexdigest(),flush=True)
print("12YM COMPLETE original archive SHA verified; glyphs remain UNREAD until manual full-page inspection.",flush=True)
