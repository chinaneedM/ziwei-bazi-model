#!/usr/bin/env python3
"""13DJ: hash pinned NCL03130 part09 suspected internal genre volume six entry p13-44.
Explicit source-images only; no OCR, original title/physical-copy human review needed.
"""
import base64,hashlib,io,json,os
from pathlib import Path
from urllib.parse import urlsplit
import fitz,requests
from PIL import Image,ImageDraw
SRC="https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
SHA="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
OUT=Path(os.environ.get("NCL13DJ_OUT","ncl03130-13dj-volume6-probe"))
TARGET=list(range(13,45))
def digest(data):return hashlib.sha256(data).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 report={"schema":"TIANWEN-13DJ-NCL03130-PART09-BOOK-BOUNDARY-SOURCE-NATIVE-R1",
    "source":SRC,"sha256_original_pdf":SHA,"pages":TARGET,
    "source_grade":"COMMONS_MIRROR_OF_DESCRIBED_NCL_COPY_NOT_FIRSTPARTY_NCL_BOUND",
    "no_ocr":True,"target_original_volume_52":"NOT_YET_MANUALLY_COLLATED",
    "physical_hand_age":"UNBOUND","manifest":[],"status":"INCOMPLETE"}
 try:
  with requests.get(SRC,stream=True,timeout=(30,180),allow_redirects=True,
     headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as r:
   r.raise_for_status()
   if urlsplit(r.url).hostname not in ("commons.wikimedia.org","upload.wikimedia.org"):
    raise RuntimeError("out of whitelist")
   h=hashlib.sha256();n=0;chunks=[]
   for chunk in r.iter_content(1048576):
    if not chunk:continue
    n+=len(chunk)
    if n>60000000:raise RuntimeError("file bound")
    chunks.append(chunk);h.update(chunk)
  raw=b"".join(chunks)
  if h.hexdigest()!=SHA or len(raw)!=50735589 or not raw.startswith(b"%PDF-"):
   raise RuntimeError("PDF original SHA or size changed")
  d=fitz.open(stream=raw,filetype="pdf")
  if len(d)!=189:raise RuntimeError("189 page contract breached")
  report["original_file_bytes"]=len(raw);report["pdf_pages"]=len(d)
  pages=[]
  for i in TARGET:
   p=d[i-1]
   img=p.get_pixmap(matrix=fitz.Matrix(2.8,2.8),alpha=False)
   payload=img.tobytes("png")
   name=f"native-p{i:03}.png";(OUT/name).write_bytes(payload)
   small=Image.open(io.BytesIO(payload)).convert("RGB")
   entry={"pdf_page":i,"file":name,"sha256_png":digest(payload),
      "dimensions":list(small.size),"grade":"SOURCE_RENDERED_NEEDS_MANUAL_GLYPH_READ"}
   report["manifest"].append(entry)
   small.thumbnail((450,320));pages.append((i,small))
  for j in range(0,len(pages),8):
   block=pages[j:j+8]
   sheet=Image.new("RGB",(4*470,2*350),"white")
   draw=ImageDraw.Draw(sheet)
   for k,(n,im) in enumerate(block):
    x=k%4*470;y=k//4*350
    sheet.paste(im,(x+7,y+22));draw.text((x+8,y+3),f"p09 PDF {n}",fill="black")
   buff=io.BytesIO();sheet.save(buff,format="JPEG",quality=87,optimize=True)
   data=buff.getvalue();name=f"navigation-{block[0][0]:03}-{block[-1][0]:03}.jpg"
   (OUT/name).write_bytes(data)
   if j<16:
    print("13DJ_ATLAS_BEGIN",name,len(data),flush=True)
    print(base64.b64encode(data).decode(),flush=True)
    print("13DJ_ATLAS_END",name,flush=True)
  report["status"]="SHA_VERIFIED_NATIVE_BOUNDARY_IMAGES_UNREAD"
  print("13DJ_SOURCE_PASS",SHA,"PAGES",len(TARGET),flush=True)
 except Exception as e:
  report.update(status="SOURCE_ACCESS_OR_FORMAT_BOUNDARY",error_type=type(e).__name__,error=str(e)[:220])
  raise
 finally:
  (OUT/"manifest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
