#!/usr/bin/env python3
"""13LY first-party volume1 IIIF page atlas: no OCR, no guessed provider IDs."""
import argparse,hashlib,io,json,urllib.parse,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw
URL="https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11166691/manifest"
ALLOW={"api.digitale-sammlungen.de"}
def safe(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.hostname not in ALLOW or p.username or p.password:
  raise ValueError("not an exact BSB image API host")
 return url
class Redirects(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,new):
  safe(new)
  return super().redirect_request(req,fp,code,msg,headers,new)
def fetch(url,limit=24000000):
 with urllib.request.build_opener(Redirects).open(urllib.request.Request(safe(url),headers={"User-Agent":"TIANWEN/13LY source-bounded Ming Shi IIIF research"}),timeout=25) as f:
  data=f.read(limit+1)
  if len(data)>limit:raise ValueError("excessive response")
  return data
def pages(m):
 if isinstance(m.get("sequences"),list) and m["sequences"]:return m["sequences"][0].get("canvases",[])
 return m.get("items",[])
def service(can):
 images=can.get("images",[])
 if images:
  resource=images[0].get("resource",{})
 else:
  layer=can.get("items",[])
  resource=layer[0].get("items",[{}])[0].get("body",{}) if layer else {}
 svc=resource.get("service",{})
 if isinstance(svc,list):svc=svc[0] if svc else {}
 if isinstance(svc,dict):return svc.get("@id") or svc.get("id")
 return None
def indices(n,count=40):
 if n<=0:return []
 return sorted(set(round(1+(n-1)*i/(min(count,n)-1)) for i in range(min(count,n)))) if n>1 else [1]
def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 result={"schema":"TIANWEN-13LY-BSB-VOLUME1-IIIF-ACQUISITION-PROBE-R1","exact_official_index_volume_id":"bsb11166691",
 "manifest_url":URL,"status":"SOURCE_UNVERIFIED","ocr":False,"target_juan35_title_leaf_proven":False,
 "original_numeral_verified":False,"independent_1739_impression_verified":False,"historical_numeric_winners":0,"samples":[]}
 try:
  raw=fetch(URL)
  (out/"volume1-original-manifest.json").write_bytes(raw)
  manifest=json.loads(raw)
  cs=pages(manifest)
  result.update(manifest_sha256=hashlib.sha256(raw).hexdigest(),manifest_bytes=len(raw),
                canvas_count=len(cs),manifest_type=manifest.get("@type") or manifest.get("type"),
                top_label=manifest.get("label"),status="MANIFEST_CAPTURED")
  thumbs=[]
  for n in indices(len(cs)):
   canvas=cs[n-1];svc=service(canvas)
   row={"canvas_1based":n,"canvas_id":canvas.get("@id") or canvas.get("id"),"service_id":svc,"status":"UNAVAILABLE"}
   try:
    if not svc:raise ValueError("no declared image service")
    u=safe(svc.rstrip("/")+"/full/900,/0/default.jpg")
    rawimage=fetch(u,3500000)
    im=Image.open(io.BytesIO(rawimage));im.load()
    if im.width>1200 or im.height>2000:raise ValueError("unexpected image dimensions")
    rgb=im.convert("RGB")
    filename=f"canvas-{n:04d}.jpg";(out/filename).write_bytes(rawimage)
    row.update(status="ORIGINAL_PROVIDER_DERIVATIVE_CAPTURED",image_url=u,file=filename,
               jpeg_bytes=len(rawimage),jpeg_sha256=hashlib.sha256(rawimage).hexdigest(),
               rgb_sha256=hashlib.sha256(rgb.tobytes()).hexdigest(),
               dimensions=[rgb.width,rgb.height])
    rgb.thumbnail((240,320));thumbs.append((n,rgb))
   except Exception as ex:row.update(status="PROVIDER_ACCESS_OR_DECODE_BOUNDARY",error=str(ex)[:180])
   result["samples"].append(row)
  if thumbs:
   columns=5;cellw=270;cellh=360
   atlas=Image.new("RGB",(columns*cellw,((len(thumbs)+columns-1)//columns)*cellh),"white")
   draw=ImageDraw.Draw(atlas)
   for i,(n,im) in enumerate(thumbs):
    x=(i%columns)*cellw;y=(i//columns)*cellh
    draw.text((x+5,y+5),f"BSB1 canvas {n}",fill="black")
    atlas.paste(im,(x+5,y+24))
   atlas.save(out/"volume1-firstpass-atlas.jpg",quality=88)
  result["successfully_sampled"]=len(thumbs)
  result["status"]="SAMPLED_PROVIDER_IMAGES" if thumbs else "MANIFEST_ONLY_IMAGE_BOUNDARY"
 except Exception as e:
  result.update(status="SOURCE_OR_MANIFEST_ACCESS_BOUNDARY",error=str(e)[:400])
 (out/"volume1-probe.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print(json.dumps({k:result.get(k) for k in ["status","manifest_sha256","canvas_count","successfully_sampled","error"]},ensure_ascii=False))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--out",required=True);main(p.parse_args().out)
