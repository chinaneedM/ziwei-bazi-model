#!/usr/bin/env python3
"""BSB first-party IIIF catalog route; previews are NOT original glyph adjudication.
Use: python scripts/acquire-tianwen-13lp-bsb-iiif.py --out DIR
No OCR, no guessed BSB item identifier, no unrestricted bulk image collection.
"""
import argparse, hashlib, io, json, os, urllib.parse, urllib.request
from pathlib import Path

URL="https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11166692/manifest"
ALLOWED={"api.digitale-sammlungen.de","digitale-sammlungen.de"}
SAMPLE=[1,2,3,4,6,8,12,20,30,50,75,100,150,250,400,650,900,1200,1500,1850]
def sha(b):return hashlib.sha256(b).hexdigest()
def safe(u):
 p=urllib.parse.urlsplit(u)
 if p.scheme!="https" or p.hostname not in ALLOWED or p.username or p.password:
  raise ValueError("Unapproved provider host or protocol: "+str(p.hostname))
 return u
def get(u,max_bytes,timeout=25):
 req=urllib.request.Request(safe(u),headers={"User-Agent":"TIANWEN/13LP source-scoped public IIIF research"})
 with urllib.request.urlopen(req,timeout=timeout) as resp:
  if resp.status!=200:raise ValueError("unexpected HTTP status "+str(resp.status))
  data=resp.read(max_bytes+1)
  if len(data)>max_bytes:raise ValueError("download exceeds bounded byte budget")
  return data
def canvases(m):
 if isinstance(m.get("sequences"),list) and m["sequences"]:
  return m["sequences"][0].get("canvases",[])
 if isinstance(m.get("items"),list):return m["items"]
 return []
def service(c):
 images=c.get("images",[])
 if images: obj=images[0].get("resource",{})
 else:
  items=c.get("items",[])
  obj=(items[0].get("items",[{}])[0].get("body",{}) if items else {})
 sv=obj.get("service",{})
 if isinstance(sv,list):sv=sv[0] if sv else {}
 if isinstance(sv,dict):return sv.get("@id") or sv.get("id")
 return None
def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 report={"schema":"TIANWEN-13LP-BSB-IIIF-CATALOG-PROBE-R1","url":URL,
         "evidence_grade":"PROVIDER_CATALOG_AND_BOUNDED_PREVIEW_ONLY",
         "no_ocr":True,"original_juan35_glyph_proven":False,
         "physical_impression_proven":False,"independent_historical_witness_votes":0,
         "status":"SOURCE_ACCESS_UNVERIFIED","samples":[]}
 try:
  raw=get(URL,24000000)
  manifest=json.loads(raw.decode("utf-8-sig"))
  cs=canvases(manifest)
  report.update(manifest_sha256=sha(raw),manifest_bytes=len(raw),
                manifest_type=manifest.get("@type") or manifest.get("type"),
                canvas_count=len(cs),status="MANIFEST_CAPTURED")
  if not cs:raise ValueError("no IIIF canvases")
  from PIL import Image,ImageDraw
  thumbs=[]
  for n in SAMPLE:
   if n>len(cs):continue
   c=cs[n-1];s=service(c)
   rec={"canvas_1_based":n,"canvas_id":c.get("@id") or c.get("id"),
        "label":str(c.get("label",""))[:150],"service_id":s,"status":"UNACQUIRED"}
   try:
    if not s:raise ValueError("no image service in canvas")
    u=safe(s.rstrip("/")+"/full/320,/0/default.jpg")
    image_bytes=get(u,2000000,timeout=18)
    im=Image.open(io.BytesIO(image_bytes));im.load()
    if im.width>500 or im.height>800:raise ValueError("oversized preview")
    im=im.convert("RGB")
    rec.update(status="PREVIEW_FETCHED",jpeg_sha256=sha(image_bytes),
               rgb_sha256=sha(im.tobytes()),pixels=[im.width,im.height],url=u)
    im.thumbnail((260,230))
    thumbs.append((n,im))
   except Exception as exc:rec.update(status="PREVIEW_ACCESS_BOUNDARY",reason=str(exc)[:250])
   report["samples"].append(rec)
  if thumbs:
   w=1200;col=4;cellw=300;cellh=260;rows=(len(thumbs)+col-1)//col
   contact=Image.new("RGB",(w,rows*cellh),"white");draw=ImageDraw.Draw(contact)
   for ix,(n,im) in enumerate(thumbs):
    x=(ix%col)*cellw;y=(ix//col)*cellh
    draw.text((x+6,y+5),f"provider canvas {n}",fill="black")
    contact.paste(im,(x+10,y+24))
   contact.save(out/"preview-contact.jpg",quality=88)
  report["preview_count"]=len(thumbs)
  report["status"]="BOUNDED_PREVIEWS_FETCHED" if thumbs else "MANIFEST_ONLY_PREVIEW_BLOCKED"
 except Exception as exc:
  report["access_or_validation_error"]=str(exc)[:500]
  if report["status"]=="SOURCE_ACCESS_UNVERIFIED":report["status"]="MANIFEST_ACCESS_BLOCKED"
  else:report["status"]="MANIFEST_OR_CANVAS_VALIDATION_BOUNDARY"
 (out/"manifest-probe.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 (out/"sampled-preview-index.json").write_text(json.dumps(report["samples"],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:report.get(k) for k in ["status","manifest_sha256","canvas_count","preview_count","access_or_validation_error"]},ensure_ascii=False))
 return report
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--out",required=True)
 main(ap.parse_args().out)
