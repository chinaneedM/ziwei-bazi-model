#!/usr/bin/env python3
"""13DF: source-emitted NAJ book51 original canvas 19-36, no OCR, no automatic glyph adjudication."""
import base64,hashlib,io,json,os
from pathlib import Path
from urllib.parse import urlparse
import requests
from PIL import Image,ImageDraw
M="https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json"
EXPECTED_MANIFEST_SHA="3f38f52860bd06ca7f4b89cec65a32b8529fcb547ac098548120e8071fe370a1"
OUT=Path(os.environ.get("TIANWEN_13DF_OUTPUT","goryeosa-13df-naj-summer-source"))
FIRST,LAST=19,36
def digest(x):return hashlib.sha256(x).hexdigest()
def fetch(url,maxbytes=3500000):
 p=urlparse(url)
 if p.scheme!="https" or p.netloc!="www.digital.archives.go.jp":
  raise RuntimeError("source URL not institutional https")
 with requests.get(url,timeout=(25,100),stream=True,
   headers={"User-Agent":"TianwenHistoricalSourceAudit/1.0"}) as response:
  response.raise_for_status()
  final=urlparse(response.url)
  if final.scheme!="https" or final.netloc!="www.digital.archives.go.jp":
   raise RuntimeError("untrusted redirect")
  b=bytearray()
  for chunk in response.iter_content(1024*1024):
   if chunk:b.extend(chunk)
   if len(b)>maxbytes:raise RuntimeError("source too large")
 return bytes(b)
def emit(data,name):
 print("13DF_ATLAS_B64_BEGIN",name,len(data),flush=True)
 print(base64.b64encode(data).decode(),flush=True)
 print("13DF_ATLAS_B64_END",name,flush=True)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 raw=fetch(M,maxbytes=200000)
 if digest(raw)!=EXPECTED_MANIFEST_SHA:raise RuntimeError("first-party manifest changed from hash-bound earlier original")
 (OUT/"official-manifest.json").write_bytes(raw)
 manifest=json.loads(raw)
 assert manifest["label"]=="高麗史５１"
 assert manifest["metadata"][2]["value"]==["２８２－０００６-0051"]
 canvases=manifest["sequences"][0]["canvases"]
 if len(canvases)!=36:raise RuntimeError("unexpected canvas count")
 result={"schema":"TIANWEN-13DF-NAJ-BOOK51-ORIGINAL-SUMMER-NAVIGATION-R1",
  "source":M,"manifest_sha256":EXPECTED_MANIFEST_SHA,"total_canvases":len(canvases),
  "bounded_photos":[FIRST,LAST],"same_physical_book_as_previous_13BA":True,
  "no_ocr":True,"manual_original_glyph_collation_complete":False,
  "third_stemmatically_independent_vote_added":0,"rows":[],"atlas":[]}
 previews=[]
 for i in range(FIRST,LAST+1):
  canvas=canvases[i-1];url=canvas["images"][0]["resource"]["@id"]
  if f"_{i:04}.jp2/" not in url:raise RuntimeError("canvas source mismatch")
  jpg=fetch(url)
  if not jpg.startswith(b"\xff\xd8"):raise RuntimeError("not jpeg source")
  im=Image.open(io.BytesIO(jpg)).convert("RGB")
  if im.width<2000 or im.height<1500:raise RuntimeError("unexpected low resolution")
  fname=f"naj-book51-source-{i:02}.jpg"
  (OUT/fname).write_bytes(jpg)
  rec={"photo":i,"canvas_id":canvas["@id"],"provider_jpeg":url,
    "jpg_sha256":digest(jpg),"jpg_size":len(jpg),"rgb_sha256":digest(im.tobytes()),
    "dimensions":list(im.size),"file":fname,"original_field_glyph":"NOT_REVIEWED"}
  result["rows"].append(rec)
  thumb=im.copy();thumb.thumbnail((430,325))
  previews.append((i,thumb))
 for start in range(0,len(previews),9):
  part=previews[start:start+9]
  sheet=Image.new("RGB",(3*460,3*360),"white")
  draw=ImageDraw.Draw(sheet)
  for j,(n,im) in enumerate(part):
   x=j%3*460;y=j//3*360
   sheet.paste(im,(x+8,y+25))
   draw.text((x+8,y+6),f"NAJ book51 photo {n:02}",fill="black")
  bio=io.BytesIO();sheet.save(bio,format="JPEG",quality=86,optimize=True)
  data=bio.getvalue()
  name=f"naj-summer-atlas-{part[0][0]:02}-{part[-1][0]:02}.jpg"
  (OUT/name).write_bytes(data)
  result["atlas"].append({"filename":name,"sha256":digest(data),"from":part[0][0],"to":part[-1][0]})
  emit(data,name)
 (OUT/"result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("13DF_ACQUIRED",len(result["rows"]),"MANIFEST_SHA",digest(raw),flush=True)
if __name__=="__main__":main()
