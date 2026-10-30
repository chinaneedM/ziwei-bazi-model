#!/usr/bin/env python3
"""Source-bound bounded BSB Ming shi .2 printed-leaf sweep, no OCR or guessed item URLs.
Only source-listed IIIF canvases; 36 explicit samples from 1880 actual manifest canvases.
Outputs raw provider JPEGs, exact hashes, and a visual contact atlas for manual review.
"""
import argparse, hashlib, io, json, urllib.request, urllib.parse
from pathlib import Path
from PIL import Image, ImageDraw
MANIFEST="https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11166692/manifest"
MANIFEST_SHA256="fb28be88c767636c6394926620c112e994f1b0b5d58cf896d4a5edc2919f047c"
INDICES=(1,6,8,30,80,130,190,250,310,370,430,490,550,610,670,730,790,850,910,970,1030,1090,1150,1210,1270,1330,1390,1450,1510,1570,1630,1690,1750,1810,1870,1880)
def h(b):return hashlib.sha256(b).hexdigest()
def get(url,limit,timeout=30):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.hostname!="api.digitale-sammlungen.de" or p.username or p.password:
  raise ValueError("unapproved original source host "+str(p.hostname))
 r=urllib.request.Request(url,headers={"User-Agent":"TIANWEN/13LS documentary first-party IIIF research"})
 with urllib.request.urlopen(r,timeout=timeout) as resp:
  if resp.status!=200:raise ValueError("HTTP "+str(resp.status))
  b=resp.read(limit+1)
  if len(b)>limit:raise ValueError("Exceeded bounded download size")
  return b
def run(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 meta={"schema":"TIANWEN-13LS-BSB-JUAN35-FOLIO-SWEEP-SOURCE-BOUND-R1","manifest":MANIFEST,
 "manifest_sha256_expected":MANIFEST_SHA256,"page_samples":list(INDICES),
 "no_ocr":True,"target_juan35_verified":False,"numeric_glyph_verified":False,
 "physical_1739_impression_verified":False,"historical_recension_vote":0,
 "images":[]}
 try:
  b=get(MANIFEST,25000000)
  if h(b)!=MANIFEST_SHA256:raise ValueError("EXACT_MANIFEST_HASH_MISMATCH")
  m=json.loads(b);canvases=m.get("sequences",[{}])[0].get("canvases",[])
  if len(canvases)!=1880:raise ValueError("unexpected source canvas count")
  meta["manifest_rechecked"]=True;meta["canvas_count"]=len(canvases)
  thumb_list=[]
  for index in INDICES:
   canvas=canvases[index-1]
   resources=canvas.get("images",[])
   service=(resources[0].get("resource",{}).get("service",{}) if resources else {})
   if isinstance(service,list):service=service[0]
   service_id=(service.get("@id") or service.get("id")) if isinstance(service,dict) else None
   entry={"index_1_based":index,"canvas_id":canvas.get("@id") or canvas.get("id"),"service_id":service_id}
   try:
    if not service_id:raise ValueError("source-listed image service missing")
    image_url=service_id.rstrip("/")+"/full/900,/0/default.jpg"
    data=get(image_url,6000000,timeout=26)
    image=Image.open(io.BytesIO(data));image.load()
    if image.width>1000 or image.height>2300:raise ValueError("large/unbounded image")
    rgb=image.convert("RGB")
    fn=f"canvas-{index:04d}.jpg";(out/fn).write_bytes(data)
    entry.update(status="FETCHED",file=fn,url=image_url,bytes=len(data),
                 sha256=h(data),rgb_sha256=h(rgb.tobytes()),pixels=list(rgb.size))
    preview=rgb.copy();preview.thumbnail((225,335))
    thumb_list.append((index,preview))
   except Exception as exc:entry.update(status="ACCESS_BOUNDARY",reason=str(exc)[:220])
   meta["images"].append(entry)
  if thumb_list:
   width=5*250;rows=(len(thumb_list)+4)//5;sheet=Image.new("RGB",(width,rows*375),"white")
   draw=ImageDraw.Draw(sheet)
   for i,(index,im) in enumerate(thumb_list):
    x=(i%5)*250;y=(i//5)*375
    draw.text((x+5,y+3),f"BSB canvas {index}",fill="black")
    sheet.paste(im,(x+8,y+25))
   sheet.save(out/"folio-sweep-contact.jpg",quality=90)
  meta["captured_count"]=len(thumb_list)
  meta["status"]="CAPTURED" if len(thumb_list)==len(INDICES) else "PARTIAL"
 except Exception as exc:
  meta["status"]="SOURCE_VALIDATION_OR_TRANSPORT_BLOCKED"
  meta["blocker"]=str(exc)
 (out/"folio-sweep.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print(json.dumps({k:meta.get(k) for k in ("status","canvas_count","captured_count","blocker")},ensure_ascii=False))
 if meta["status"]!="CAPTURED":raise SystemExit("Manifest/images failed source integrity or availability; stored bounded record")
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--out",required=True)
 run(a.parse_args().out)
