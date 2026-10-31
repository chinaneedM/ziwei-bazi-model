#!/usr/bin/env python3
"""13MS original Zhou 1569 source-pixel acquisition; NO OCR or field adjudication.
Exact PDF hash, 45-page count, 2.5x RGB pages and source-coordinate ROIs.
Does not assert physical impression identity, G893 equivalence or historical winner.
"""
from __future__ import annotations
import hashlib, io, json, os, urllib.parse, urllib.request
from pathlib import Path

URL="https://www.kotenmon.com/cal/arabe/vol6.pdf"
EXPECTED="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
PAGES=(14,15,16)
ROIS=[
 ("p14-operator-right",14,(1010,75,1930,1400)),
 ("p14-table-first-days-left",14,(165,75,1090,1400)),
 ("p15-d15-short-and-other-lanes",15,(1190,65,1480,1390)),
 ("p15-d15-vertical-column",15,(1295,70,1353,1370)),
 ("p15-entire-table",15,(150,70,1980,1400)),
 ("p16-next-day-continuation",16,(150,70,1980,1400)),
]
ALLOWED_REDIRECTS={"kotenmon.com","www.kotenmon.com"}
def sha(b):return hashlib.sha256(b).hexdigest()
class RestrictedRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,url):
  parsed=urllib.parse.urlsplit(url)
  if parsed.scheme!="https" or parsed.hostname not in ALLOWED_REDIRECTS:
   raise ValueError("source redirect outside allowlist")
  return super().redirect_request(req,fp,code,msg,headers,url)
def fetch_pdf():
 req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0 Tianwen-13MS/1.0","Accept":"application/pdf"})
 with urllib.request.build_opener(RestrictedRedirect).open(req,timeout=90) as r:
  assert r.status==200
  b=r.read(15_000_001)
  assert b.startswith(b"%PDF") and len(b)<=15_000_000
  assert sha(b)==EXPECTED, "Source PDF unexpected bytes: fail-closed, no substitute"
  return b
def gate(report):
 assert report["schema"]=="TIANWEN-13MS-ZHOU1569-ORIGINAL-PAGE-ATLAS-R1"
 assert report["source"]["sha256"]==EXPECTED
 assert report["source"]["pdf_pages"]==45
 assert report["source"]["new_historical_source_count"]==0
 assert report["source"]["new_physical_witness_count"]==0
 assert report["source"]["ocr"] is False
 assert report["limits"]["cross_source_same_field_verified"] is False
 assert report["limits"]["column_unit_radix_epoch_complete"] is False
 assert report["limits"]["historical_six_winners"]==0
 assert report["limits"]["algorithm_reopens"]==0
 assert report["limits"]["physical_impression_identified"] is False
 assert len(report["roi_records"])==len(ROIS)
 assert [(r["name"],r["page"],tuple(r["box"])) for r in report["roi_records"]]==ROIS
 return True
def main():
 from PIL import Image,ImageDraw
 import fitz
 out=Path(os.environ.get("TIANWEN_13MS_OUT","/tmp/tianwen-13ms"))
 out.mkdir(parents=True,exist_ok=True)
 report={"schema":"TIANWEN-13MS-ZHOU1569-ORIGINAL-PAGE-ATLAS-R1",
    "stage":"ACQUISITION_RUNNING_FAIL_CLOSED",
    "source":{"url":URL,"expected_sha256":EXPECTED,"ocr":False,"new_historical_source_count":0,
              "new_physical_witness_count":0},
    "roi_records":[],
    "limits":{"cross_source_same_field_verified":False,"column_unit_radix_epoch_complete":False,
             "historical_six_winners":0,"algorithm_reopens":0,
             "physical_impression_identified":False,
             "interpretation":"SOURCE_IMAGE_ATLAS_ONLY_NO_GLYPH_ADJUDICATION"}}
 try:
  raw=fetch_pdf()
  doc=fitz.open(stream=raw,filetype="pdf")
  assert len(doc)==45, "wrong source pages"
  report["source"].update(sha256=sha(raw),pdf_pages=len(doc),file_bytes=len(raw))
  (out/"zhouxiang-1569-vol6-original.pdf").write_bytes(raw)
  renders={}
  for n in PAGES:
   pix=doc[n-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),colorspace=fitz.csRGB,alpha=False)
   im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
   assert im.size==(2105,1489),f"source image shape changed at p{n}"
   renders[n]=im
   name=f"zhouxiang-original-p{n:02d}-2p5x.png"
   im.save(out/name)
   report.setdefault("full_pages",[]).append({"pdf_page_1based":n,"file":name,
      "image_sha256":sha((out/name).read_bytes()),"rgb_sha256":sha(im.tobytes()),
      "pixels":[im.width,im.height]})
  for name,p,box in ROIS:
   im=renders[p]
   x0,y0,x1,y1=box
   assert min(box)>=0 and x1<=im.width and y1<=im.height and x1>x0 and y1>y0
   crop=im.crop(box)
   fname=name+".png"
   crop.save(out/fname)
   report["roi_records"].append({"name":name,"page":p,"box":list(box),
      "pixels":[crop.width,crop.height],"file":fname,
      "rgb_sha256":sha(crop.tobytes()),"png_sha256":sha((out/fname).read_bytes())})
  # Context mosaic is explicitly a derivative, not another original witness.
  atlas=Image.new("RGB",(1260,3*680),"white")
  draw=ImageDraw.Draw(atlas)
  for i,(name,p,box) in enumerate(ROIS[:3]):
   thumb=renders[p].crop(box)
   thumb.thumbnail((1190,570))
   atlas.paste(thumb,(22,i*680+48))
   draw.text((22,i*680+12),name+" | ORIGINAL PDF p"+str(p),fill="black")
  atlas.save(out/"annotated-3-region-contact.jpg",quality=94)
  report["stage"]="SOURCE_PDF_AND_RGB_ROIS_HASH_VERIFIED_UNCOLLATED"
  gate(report)
 except Exception as e:
  report["stage"]="SOURCE_ACCESS_OR_HASH_BOUNDARY_NO_VERIFIED_IMAGE"
  report["error"]=type(e).__name__+": "+str(e)[:400]
  (out/"source-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
  print(json.dumps({"stage":report["stage"],"error":report["error"]},ensure_ascii=False))
  raise
 (out/"source-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({"stage":report["stage"],"source_sha256":report["source"]["sha256"],
     "source_bytes":report["source"]["file_bytes"],"pages":report["source"]["pdf_pages"],
     "original_crops":report["roi_records"],"historical_winners":0},ensure_ascii=False))
if __name__=="__main__":main()
