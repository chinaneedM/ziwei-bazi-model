#!/usr/bin/env python3
"""13MT: identical source PDF, pinned PyMuPDF versions, identical Pillow version.
For SOURCE RENDER PROFILE only. No OCR, physical impression, or G893 field judgement.
"""
from __future__ import annotations
import argparse,hashlib,json,os,urllib.request
from pathlib import Path
import fitz
from PIL import Image
URL="https://www.kotenmon.com/cal/arabe/vol6.pdf"
SHA="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
RECORDS={
"1.26.7":{"full":"7b35af0e1e802c9346c927a02c67d1681e01b5120c3cf891160126f2018478d5",
          "roi":"188a2d98f567bf4c5c90cbd9dcb3bb4c0cbb86b097ec3f07196bf168413b0c94"},
"1.28.2":{"full":"d617e4e0a553dd019ea89a5bc54307e4d08a50cb96e958e7b34897c203c7d75d",
          "roi":"1d85a06bd3421d38113c567fbfb393d2db633232179c5d50f932ebbd4cb59d07"},
}
BOX=(1295,70,1353,1370)
def sha(b):return hashlib.sha256(b).hexdigest()
def check(version):
 assert version in RECORDS and fitz.VersionBind==version,("unexpected renderer",fitz.VersionBind)
 assert Image.__version__=="11.3.0",("Pillow drift",Image.__version__)
 req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 Tianwen13MT/1.0","Accept":"application/pdf"})
 with urllib.request.urlopen(req,timeout=85) as r:
  assert r.status==200
  raw=r.read(15000001)
 assert raw.startswith(b"%PDF") and len(raw)==4936040 and sha(raw)==SHA
 doc=fitz.open(stream=raw,filetype="pdf")
 assert len(doc)==45
 pix=doc[14].get_pixmap(matrix=fitz.Matrix(2.5,2.5),colorspace=fitz.csRGB,alpha=False)
 page=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
 assert page.size==(2105,1489)
 out={"schema":"TIANWEN-13MT-CROSS-RENDERER-ORIGINAL-RGB-R1",
    "source_original_pdf_sha256":sha(raw),"source_original_pdf_pages":len(doc),
    "python_renderer":fitz.VersionBind,"pillow":Image.__version__,
    "source_pdf_page_1based":15,"image_pixels":list(page.size),
    "source_crop_box":list(BOX),"scale":"2.5","alpha":False,"ocr":False,
    "page_rgb_sha256":sha(page.tobytes()),
    "crop_rgb_sha256":sha(page.crop(BOX).tobytes()),
    "expected":RECORDS[version],
    "copy_and_source_print_changes":0,
    "new_source_witnesses":0,"historical_winners":0,"algorithm_reopens":0}
 assert out["page_rgb_sha256"]==RECORDS[version]["full"],"FULL ORIGINAL PAGE SHA MISMATCH"
 assert out["crop_rgb_sha256"]==RECORDS[version]["roi"],"ORIGINAL CROP SHA MISMATCH"
 d=Path(os.environ.get("TIANWEN_13MT_OUT","/tmp/tianwen-13mt"))
 d.mkdir(parents=True,exist_ok=True)
 (d/("render-profile-"+version+".json")).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
 return out
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--version",choices=list(RECORDS),required=True)
 args=p.parse_args()
 print(json.dumps(check(args.version),ensure_ascii=False))
