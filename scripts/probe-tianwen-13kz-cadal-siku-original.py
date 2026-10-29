#!/usr/bin/env python3
"""13KZ: public CADAL06056956 126-page DjVu retrieval and no-OCR contact atlas."""
import hashlib,io,json,subprocess,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw
URL="https://upload.wikimedia.org/wikipedia/commons/3/36/CADAL06056956_%E6%98%8E%E5%8F%B2%C2%B7%E5%8D%B7%E4%B8%89%E5%8D%81%E4%BA%94~%E5%8D%B7%E4%B8%89%E5%8D%81%E5%85%AD.djvu"
EXPECTED_BYTES=4528817
EXPECTED_SHA1="45fc977d134b07689391907d6671eac3c0b7eedb"
OUT=Path("13kz-output")
def require(ok,msg):
 if not ok:raise ValueError(msg)
def acquire():
 req=urllib.request.Request(URL,headers={"User-Agent":"TianwenHistoricalAudit/1.0 (research; +https://github.com/chinaneedM/ziwei-bazi-model)","Accept":"*/*"})
 with urllib.request.urlopen(req,timeout=120) as f:
  data=f.read()
 require(len(data)==EXPECTED_BYTES,"source file size")
 require(hashlib.sha1(data).hexdigest()==EXPECTED_SHA1,"source original SHA1")
 OUT.mkdir(exist_ok=True)
 (OUT/"original-source.djvu").write_bytes(data)
 return data
def contact(source,count):
 pages=list(range(1,count+1));sheet_height=6*560;sheet_width=6*402
 for first in range(0,count,36):
  im=Image.new("RGB",(sheet_width,sheet_height),"white");draw=ImageDraw.Draw(im)
  for n in pages[first:first+36]:
   run=subprocess.run(["ddjvu","-format=ppm",f"-page={n}","-size=360x515",str(source),"-"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
   page=Image.open(io.BytesIO(run.stdout)).convert("RGB")
   col=(n-1-first)%6;row=(n-1-first)//6
   im.paste(page,(col*402,row*560+22))
   draw.text((col*402+8,row*560+2),f"DJVU PAGE {n:03d}",fill="black")
  final=min(first+36,count);im.save(OUT/f"contact-p{first+1:03d}-{final:03d}.jpg",quality=89)
def main():
 data=acquire();doc=OUT/"original-source.djvu"
 proc=subprocess.run(["djvused",str(doc),"-e","n"],capture_output=True,text=True,check=True)
 page_count=int(proc.stdout.strip());require(page_count==126,"page count")
 contact(doc,page_count)
 evidence={"document_url":URL,"sha1":hashlib.sha1(data).hexdigest(),"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"pages":page_count,
  "source_scope":"DIGITAL_ORIGINAL_ACQUIRED_NOT_PHYSICAL_IMPRESSION_NOT_TARGET_GLYPH_COLLATED","ocr_used":False,
  "commons_sha1_verified":True,"new_independent_physical_witnesses":0}
 (OUT/"source-receipt.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(evidence,ensure_ascii=False))
if __name__=="__main__":main()
