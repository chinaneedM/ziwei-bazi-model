#!/usr/bin/env python3
"""12YR acquire verified exact archive item 06054965.cn for Mei Wending Datong Lizhi v3-4.
Only printed native visual reading, never OCR text, may support historical glyph results.
"""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path("research-12yr-mei-original")
OUT.mkdir(exist_ok=True)
ITEM="06054965.cn";FILE=ITEM+".djvu"
URLS=[
 "https://archive.org/download/06054965.cn//06054965.cn.djvu",
 "https://archive.org/download/06054965.cn/06054965.cn.djvu",
]
srcfile=OUT/FILE
access=[]
for url in URLS:
 try:
  request=urllib.request.Request(url,headers={"User-Agent":"TianwenHistoricalPageResearch/1.0 (source attribution in report; original scan)"})
  with urllib.request.urlopen(request,timeout=85) as response,srcfile.open("wb") as output:
   n=0
   while True:
    x=response.read(1<<20)
    if not x:break
    n+=len(x)
    if n>80_000_000:raise RuntimeError("bound 80MB; refuse unrelated source")
    output.write(x)
  if srcfile.stat().st_size>500_000:
   access.append({"url":url,"status":"DOWNLOADED","bytes":srcfile.stat().st_size})
   break
 except Exception as exc:
  access.append({"url":url,"error":type(exc).__name__+": "+str(exc)[:300]})
else:
 (OUT/"access.json").write_text(json.dumps({"item":ITEM,"attempts":access,"original_glyphs_direct_verified":0,"physical_original_votes":0,"status":"SOURCE_ACCESS_BLOCKED","original_source_bytes":0},ensure_ascii=False,indent=2)+"\n")
 print("12YR SOURCE_ACCESS_BLOCKED; no original bytes or glyphs",flush=True)
 raise SystemExit(0)
raw=srcfile.read_bytes()
sha1=hashlib.sha1(raw).hexdigest();sha256=hashlib.sha256(raw).hexdigest()
assert raw[:4]==b"AT&T",("not djvu",raw[:12])
print("12YR DOWNLOAD",len(raw),sha1,sha256,flush=True)
check=subprocess.run(["djvudump",str(srcfile)],capture_output=True,text=True,check=True).stdout
pages=check.count("FORM:DJVU")
if not pages: 
 info=subprocess.run(["djvused",str(srcfile),"-e","n"],capture_output=True,text=True,check=True)
 pages=int(info.stdout.strip())
assert 10<=pages<=800,("unexpected book length",pages)
print("12YR DJVU PAGES",pages,flush=True)
(OUT/"source.json").write_text(json.dumps({
 "schema":"TIANWEN-12YR-MEI-DATONG-LIZHI-V3V4-SOURCE-ACQUISITION-R1",
 "source_catalog":"Wikisource IA Scans 清 entry 梅文鼎 大統歷志",
 "source_item_id":ITEM,"file":FILE,"source_catalog_link":"https://zh.wikisource.org/zh-hans/Wikisource:古籍資源/Internet_Archive_Scans/清",
 "origin":"archive.org mirrored Zhejiang University Library/CADAL catalog", "acquisition_routes":access,
 "bytes":len(raw),"sha1":sha1,"sha256":sha256,"djvu_pages":pages,
 "original_target_printed_glyphs_verified":0,"original_physical_printing_date_verified":False,
 "source_ancient_impression_independence_proven":False,"previous_CText_same_physical_copy": "UNPROVEN",
 "G893_original_fields":"5/6", "mechanical_final":"0/6"
},ensure_ascii=False,indent=2)+"\n")
W,H=192,272
for lo in range(1,pages+1,24):
 sheet=Image.new("RGB",(W*6,H*4),"white")
 d=ImageDraw.Draw(sheet)
 for i,page in enumerate(range(lo,min(lo+24,pages+1))):
  tmp=OUT/"_page.png"
  cmd=["ddjvu","-format=pnm",f"-page={page}","-scale=18",str(srcfile)]
  p=subprocess.run(cmd,capture_output=True,check=True)
  import io
  im=Image.open(io.BytesIO(p.stdout)).convert("RGB")
  im.thumbnail((W-10,H-28))
  x=(i%6)*W+(W-im.width)//2;y=(i//6)*H+23
  sheet.paste(im,(x,y))
  d.text((i%6*W+8,i//6*H+5),f"IMAGE {page:03d}",fill="black")
 dest=OUT/f"atlas_{lo:03d}_{min(lo+23,pages):03d}.jpg"
 sheet.save(dest,quality=81,optimize=True)
 print("12YR ATLAS",str(dest),hashlib.sha256(dest.read_bytes()).hexdigest(),flush=True)
print("12YR SOURCE ACQUIRED; ORIGINAL TARGET GLYPHS STILL UNREVIEWED",flush=True)
