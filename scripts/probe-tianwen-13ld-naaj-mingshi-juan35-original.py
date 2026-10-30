#!/usr/bin/env python3
"""13LD public NAJDA original PDF acquisition; only hashes/pages, never automated historical text inference."""
import hashlib, io, json, os, sys, urllib.request, urllib.parse, time
from pathlib import Path
from urllib.parse import urlparse
import fitz
from PIL import Image, ImageOps, ImageDraw
FILE="NAJDA-281-0038 明史 志第11-13.pdf"
API="https://commons.wikimedia.org/w/api.php"
ROOT=Path("13ld-naaj-original-output")
ROOT.mkdir(parents=True, exist_ok=True)
def req(url):
 q=urllib.request.Request(url,headers={"User-Agent":"TianwenSourceAudit/1.0 (public source image provenance; Wikimedia Commons)"})
 return urllib.request.urlopen(q,timeout=70)
def get_meta():
 args=urllib.parse.urlencode({"action":"query","format":"json","prop":"imageinfo","iiprop":"url|sha1|size","titles":"File:"+FILE})
 with req(API+"?"+args) as r:data=json.load(r)
 pages=list(data["query"]["pages"].values())
 assert len(pages)==1 and "missing" not in pages[0], "public backup file not found"
 info=pages[0]["imageinfo"][0]
 assert urlparse(info["url"]).netloc=="upload.wikimedia.org", "non-Wikimedia download URL"
 assert len(info["sha1"])==40 and int(info["size"])>10000, "missing file evidence"
 return info
def download(meta):
 path=ROOT/"naaj-281-0038-shi11-13-original.pdf"
 h1=hashlib.sha1();h2=hashlib.sha256();n=0
 with req(meta["url"]) as r, path.open("wb") as output:
  while True:
   chunk=r.read(1024*1024)
   if not chunk:break
   n+=len(chunk)
   assert n<=300_000_000,"PDF beyond resource ceiling"
   output.write(chunk);h1.update(chunk);h2.update(chunk)
 assert n==int(meta["size"]) and h1.hexdigest()==meta["sha1"], "Commons original byte hash mismatch"
 return path,n,h1.hexdigest(),h2.hexdigest()
def acquire():
 result={"source":"NAJDA 281-0038 / item book order 0011 / 明史 志第11-13","source_catalog":"https://www.digital.archives.go.jp/file/en/3610285","file_name":FILE,"no_ocr":True,"original_glyph_evidence_awarded":False,"new_numeric_original_votes":0,"direct_13month_reading":None,"source_original_page_review":"PENDING_HUMAN_REVIEW"}
 try:
  meta=get_meta()
  path,n,sha1,sha256=download(meta)
  doc=fitz.open(str(path))
  assert 1<=doc.page_count<=300,"unexpected volume range"
  result.update({"status":"SOURCE_FILE_HASH_VERIFIED_NOT_GLYPH_READ","bytes":n,"sha1":sha1,"sha256":sha256,"pages":doc.page_count,"commons_imageinfo_url":meta["url"],"catalogued_sha1":meta["sha1"],"catalogued_bytes":meta["size"]})
  entries=[];thumbs=[]
  for i in range(doc.page_count):
   pg=doc[i]
   mini=pg.get_pixmap(matrix=fitz.Matrix(0.23,0.23),alpha=False)
   im=Image.open(io.BytesIO(mini.tobytes("png"))).convert("RGB")
   im.thumbnail((250,330))
   thumbs.append((i+1,im.copy()))
   if i<24:
    pm=pg.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    full=Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")
    jpeg=ROOT/f"candidate-p{i+1:03d}.jpg"
    full.save(jpeg,format="JPEG",quality=84)
    entries.append({"pdf_page":i+1,"image_pixels":[full.width,full.height],"native_render_rgb_sha256":hashlib.sha256(full.tobytes()).hexdigest(),"jpeg_sha256":hashlib.sha256(jpeg.read_bytes()).hexdigest(),"human_glyph_review":False})
  page_w,page_h=280,360
  sheets=[]
  for block in range(0,len(thumbs),20):
   canvas=Image.new("RGB",(5*page_w,4*page_h),"white")
   dr=ImageDraw.Draw(canvas)
   for k,(p,img) in enumerate(thumbs[block:block+20]):
    x=(k%5)*page_w;y=(k//5)*page_h
    canvas.paste(img,(x+12,y+22))
    dr.text((x+10,y+6),f"PDF p{p}",fill="black")
   dst=ROOT/f"contact-{1+block//20:02d}.jpg"
   canvas.save(dst,format="JPEG",quality=77)
   sheets.append({"file":dst.name,"sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),"pdf_page_range":[block+1,min(block+20,len(thumbs))]})
  result["candidate_pages"]=entries
  result["contact_sheets"]=sheets
  doc.close()
  path.unlink()
 except Exception as exc:
  result["status"]="SOURCE_ACQUISITION_BLOCKED_OR_INVALID_NOT_HISTORICAL_ABSENCE"
  result["error"]=str(type(exc).__name__)+": "+str(exc)[:500]
  (ROOT/"acquisition.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps(result,ensure_ascii=False))
  raise
 (ROOT/"acquisition.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:v for k,v in result.items() if k not in ("candidate_pages","contact_sheets")},ensure_ascii=False))
if __name__=="__main__":acquire()
