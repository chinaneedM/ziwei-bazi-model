#!/usr/bin/env python3
"""12YN NLC 1892 lithographic MingShi v33 independent-catalog scanned-source probe.

Acquires only a specifically catalogued public-domain Commons object. Screens
are locator-only until a human directly reads exact native target pixels.
"""
import hashlib, json, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

FILENAME="NLC892-312002017339-363680_二十四史_第178冊.pdf"
ORIGINAL="https://upload.wikimedia.org/wikipedia/commons/9/96/"+urllib.parse.quote(FILENAME,safe="~")
OUT=Path("research-12yn-nlc1892"); OUT.mkdir(exist_ok=True)
SRC=OUT/FILENAME
EXPECTED_CATALOG_BYTES=78635564
EXPECTED_CATALOG_PAGES=108
req=urllib.request.Request(ORIGINAL,headers={"User-Agent":"TianwenResearchOriginalWitnessCollation/1.0 (public domain; cite Commons)"})
try:
    with urllib.request.urlopen(req,timeout=150) as src,SRC.open("wb") as dest:
        while True:
            b=src.read(2*1024*1024)
            if not b:break
            dest.write(b)
except Exception as exc:
    print("SOURCE_ACCESS_BLOCKED",str(exc),flush=True)
    raise
data=SRC.read_bytes()
assert len(data)==EXPECTED_CATALOG_BYTES,(len(data),EXPECTED_CATALOG_BYTES)
assert data[:5]==b"%PDF-","Not original PDF"
sha1=hashlib.sha1(data).hexdigest()
sha256=hashlib.sha256(data).hexdigest()
try:
    info=subprocess.run(["pdfinfo",str(SRC)],text=True,capture_output=True,check=True).stdout
    pages=int(next(x.split(":",1)[1].strip() for x in info.splitlines() if x.startswith("Pages:")))
except Exception as exc:raise RuntimeError("PDF_METADATA_UNAVAILABLE "+str(exc))
assert pages==EXPECTED_CATALOG_PAGES,pages
print("12YN ORIGINAL_FILE_VERIFIED",len(data),pages,sha1,sha256,flush=True)
report={"schema":"TIANWEN-12YN-1892-MINGSHI-V33-CANDIDATE-SOURCE-PROBE-R1",
        "catalog_title":"二十四史 第178冊（明史卷25至39）",
        "catalog_claimed_edition":"武林竹簡齋 清光緒十八年[1892]石印",
        "catalog_book_item":"NLC892-312002017339-363680",
        "physical_copy_vs_cadal":"DISTINCT_REPORTED_PROVENANCE_NOT_YET_PAGE_LEVEL_ADJUDICATED",
        "original_url":ORIGINAL,"bytes":len(data),"sha1":sha1,"sha256":sha256,
        "pdf_pages":pages,"original_loci_verified":0,
        "original_catalog_printing_date_verified_by_original_colophon":False,
        "independent_original_evidence_votes":0,
        "comments":"Contact atlas for volume33 page location only. No OCR performed; target glyphs not adjudicated by index."}
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
W,H=245,330
for first in range(1,pages+1,20):
    sheet=Image.new("RGB",(W*5,H*4),"white")
    draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(range(first,min(pages+1,first+20))):
        prefix=OUT/f"_tmp_{p:03d}"
        subprocess.run(["pdftoppm","-f",str(p),"-l",str(p),"-scale-to","280","-singlefile","-png",str(SRC),str(prefix)],capture_output=True,check=True)
        tmp=prefix.with_suffix(".png")
        with Image.open(tmp) as im:
            im.thumbnail((W-8,H-30));x=(i%5)*W+(W-im.width)//2;y=(i//5)*H+23;sheet.paste(im,(x,y))
        tmp.unlink()
        draw.text((i%5*W+8,i//5*H+4),f"NLC1892 PDF p {p:03d}",fill="black")
    dest=OUT/f"contact_{first:03d}_{min(pages,first+19):03d}.jpg"
    sheet.save(dest,quality=83,optimize=True)
    print("12YN ATLAS",dest.name,hashlib.sha256(dest.read_bytes()).hexdigest(),flush=True)
print("12YN COMPLETE; ORIGINAL_2_LOCI_NOT_YET_ADJUDICATED",flush=True)
