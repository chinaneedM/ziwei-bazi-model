#!/usr/bin/env python3
"""12YT probe one exact Commons CADAL06054965 Mei v3-v4 original.

Do not assume a catalog list link means the file exists. No OCR, no evidence
promotion until original bytes plus exact source glyph regions are certified.
"""
from __future__ import annotations
import hashlib, json, subprocess, urllib.error, urllib.parse, urllib.request, io
from pathlib import Path
from PIL import Image, ImageDraw

OUT=Path("research-12yt-mei-commons");OUT.mkdir(exist_ok=True)
NAME="CADAL06054965 大統歷志·卷三~卷四.djvu"
TITLE="File:"+NAME
CATALOG="https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/CADAL/13"
WEB="https://commons.wikimedia.org/w/api.php"
URLS=[
 WEB+"?"+urllib.parse.urlencode({"action":"query","format":"json","formatversion":2,"titles":TITLE,"prop":"imageinfo","iiprop":"url|size|sha1|mime|timestamp"}),
 "https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(NAME,safe=""),
 "https://commons.wikimedia.org/wiki/Special:FilePath/"+urllib.parse.quote(NAME,safe=""),
]
results=[]
def response(url,limit=50_000_000):
 req=urllib.request.Request(url,headers={"User-Agent":"TianwenHistoricallyScopedPublicDomainImageCollation/1.0 (metadata-only unless exact catalog PDF/DjVu)"})
 with urllib.request.urlopen(req,timeout=120) as r:
  actual=r.geturl()
  typ=r.headers.get("Content-Type","")
  dat=r.read(limit+1)
  if len(dat)>limit:raise RuntimeError("LIMIT_EXCEEDED")
  return actual,typ,dat
meta=None
try:
 actual,typ,data=response(URLS[0],1_000_000)
 meta=json.loads(data)
 results.append({"route":"commons-mediawiki-api","state":"AVAILABLE","url":actual,"content_type":typ})
except Exception as exc:
 results.append({"route":"commons-mediawiki-api","state":"UNAVAILABLE","error":type(exc).__name__+": "+str(exc)[:240]})
imageinfo=None
if meta:
 pages=meta.get("query",{}).get("pages",[])
 for p in pages:
  if "imageinfo" in p:imageinfo=p["imageinfo"][0]
 results.append({"route":"commons-catalog-item","exists":bool(imageinfo),"page_entries":[{"title":p.get("title"),"missing":"missing" in p} for p in pages[:2]],"imageinfo":imageinfo})
if imageinfo and imageinfo.get("url"):URLS.insert(1,imageinfo["url"])
target=OUT/NAME
downloaded=False
for url in URLS[1:]:
 try:
  actual,typ,dat=response(url,80_000_000)
  if dat[:4]!=b"AT&T":
   results.append({"route":"source-byte","state":"NOT_DJVU","requested":url,"actual":actual,"type":typ,"length":len(dat),"first_bytes_hex":dat[:14].hex()})
   continue
  target.write_bytes(dat)
  results.append({"route":"source-byte","state":"DJVU_VERIFIED","requested":url,"actual":actual,"type":typ,"length":len(dat)})
  downloaded=True;break
 except Exception as exc:
  results.append({"route":"source-byte","state":"UNAVAILABLE","requested":url,"error":type(exc).__name__+": "+str(exc)[:240]})
report={"schema":"TIANWEN-12YT-CADAL06054965-EXACT-COMMONS-ORIGINAL-PROBE-R1",
"source_title":NAME,"wiki_catalog_index":CATALOG,"wiki_catalog_exact_filename_listed":True,
"mediawiki_imageinfo_verified":bool(imageinfo),
"acquisition_attempts":results,
"original_source_image_bytes_acquired":downloaded,
"source_file_sha256":None,"source_file_sha1":None,"source_image_count":None,
"original_target_glyphs_approved":0,"independent_ancient_impression_vote":0,
"source_physical_print_date":"UNVERIFIED","relation_to_ctext_original":"UNVERIFIED",
"relation_to_ia_06054965_cn":"CATALOG_NUMERIC_ID_MATCH_NOT_PROVEN_BYTE_IDENTITY"}
if not downloaded:
 report["status"]="FILE_NOT_YET_RETRIEVED_NOT_PROOF_HISTORICAL_NONEXISTENCE"
 (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
 print("12YT COMMONS_CATALOG_ONLY no original bytes, zero printed-glyph votes",flush=True);raise SystemExit(0)
raw=target.read_bytes();report["source_file_sha256"]=hashlib.sha256(raw).hexdigest();report["source_file_sha1"]=hashlib.sha1(raw).hexdigest()
if imageinfo and imageinfo.get("size"):assert imageinfo["size"]==len(raw),("Commons catalog byte-size mismatch",len(raw),imageinfo["size"])
if imageinfo and imageinfo.get("sha1"):assert imageinfo["sha1"].lower()==report["source_file_sha1"].lower(),("Commons catalog SHA1 mismatch")
pages_result=subprocess.run(["djvused",str(target),"-e","n"],capture_output=True,text=True,check=True)
pages=int(pages_result.stdout.strip())
assert 10<=pages<=800,pages
report["source_image_count"]=pages;report["status"]="SOURCE_ORIGINAL_DIGITAL_FILE_ACQUIRED_GLYPHS_PENDING"
print("12YT ORIGINAL_DIGITAL_BYTES",len(raw),pages,report["source_file_sha256"],flush=True)
W,H=195,265
for start in range(1,pages+1,24):
 sheet=Image.new("RGB",(W*6,H*4),"white");draw=ImageDraw.Draw(sheet)
 for i,p in enumerate(range(start,min(start+24,pages+1))):
  q=subprocess.run(["ddjvu","-format=pnm",f"-page={p}","-scale=20",str(target)],capture_output=True,check=True)
  im=Image.open(io.BytesIO(q.stdout)).convert("RGB");im.thumbnail((W-12,H-32))
  left=(i%6)*W+(W-im.width)//2;top=(i//6)*H+25;sheet.paste(im,(left,top))
  draw.text(((i%6)*W+8,(i//6)*H+5),f"IMAGE {p:03d}",fill="black")
 name=OUT/f"contact_{start:03d}_{min(start+23,pages):03d}.jpg"
 sheet.save(name,quality=85,optimize=True)
 print("12YT ATLAS",name,hashlib.sha256(name.read_bytes()).hexdigest(),flush=True)
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
# Export all candidate Juan-3 to Juan-4 boundary pages without OCR at native
# lossless resolution, so a human can locate both printed numeric targets.
native_manifest=[]
for page in range(25,min(pages+1,78)):
 rendered=subprocess.run(["ddjvu","-format=pnm",f"-page={page}",str(target)],capture_output=True,check=True)
 image=Image.open(io.BytesIO(rendered.stdout)).convert("RGB")
 pth=OUT/f"native_{page:03d}.png"
 image.save(pth,optimize=True)
 rec={"page_one_based":page,"width":image.width,"height":image.height,
      "rgb_sha256":hashlib.sha256(image.tobytes()).hexdigest(),
      "png_sha256":hashlib.sha256(pth.read_bytes()).hexdigest()}
 native_manifest.append(rec)
 if page%10==0: print("12YT NATIVE_PRINT",page,image.width,image.height,rec["png_sha256"],flush=True)
(OUT/"native-manifest.json").write_text(json.dumps(native_manifest,ensure_ascii=False,indent=2)+"\n")
print("12YT native candidate folios",len(native_manifest),"original glyph verdict pending manual collation",flush=True)
print("12YT source acquired, direct printed numeral review STILL ZERO",flush=True)
