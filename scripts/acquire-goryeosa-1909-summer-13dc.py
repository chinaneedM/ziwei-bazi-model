#!/usr/bin/env python3
"""13DC: source-native 1909 Goryeosa summer table folio navigation, NOT glyph adjudication."""
import base64, hashlib, io, json, os
from pathlib import Path
import fitz, requests
from PIL import Image,ImageDraw

U=("https://commons.wikimedia.org/wiki/Special:Redirect/file/"
   "NLC416-13jh005095-74760_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf")
SHA="b4bd5c557c7ba44bac1fc881e6c2e8784c9d56a8d2629f17b5255a1ec6bd9e97"
START,END=143,200
OUT=Path(os.environ.get("TIANWEN_13DC_OUT","goryeosa-13dc-summer-original"))
def digest(b):return hashlib.sha256(b).hexdigest()
def emit(tag, name, body):
 print(f"13DC_{tag}_BEGIN {name} {len(body)}")
 print(base64.b64encode(body).decode("ascii"))
 print(f"13DC_{tag}_END {name}",flush=True)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 with requests.get(U,stream=True,timeout=(35,210),allow_redirects=True,
                   headers={"User-Agent":"TianwenResearch/1.0 (source-native public domain study)"}) as res:
  res.raise_for_status()
  host=requests.utils.urlparse(res.url).hostname
  if host not in ("commons.wikimedia.org","upload.wikimedia.org"):raise RuntimeError("unexpected redirect host")
  size=0;sha=hashlib.sha256();chunks=[]
  for chunk in res.iter_content(1024*1024):
   if not chunk:continue
   size+=len(chunk)
   if size>55_000_000:raise RuntimeError("unexpected oversized file")
   sha.update(chunk);chunks.append(chunk)
 raw=b"".join(chunks)
 if sha.hexdigest()!=SHA or len(raw)!=38410680 or raw[:5]!=b"%PDF-":raise RuntimeError("source hash/size/magic mismatch")
 doc=fitz.open(stream=raw,filetype="pdf")
 if len(doc)!=755:raise RuntimeError("page count mismatch")
 manifest={"schema":"TIANWEN-13DC-NLC416-SUMMER-ORIGINAL-NAVIGATION-R1",
  "source_url":U,"sha256_original_pdf":SHA,"source_bytes":size,"pdf_page_count":len(doc),
  "page_range":[START,END],"evidence_grade":"SOURCE_NATIVE_PAGE_NAVIGATION_UNREAD_NO_OCR",
  "identifies_target_original_day28":False,"page_originals":[],"contact_sheets":[]}
 (OUT/"source.pdf").write_bytes(raw)
 imgs=[]
 for p in range(START,END+1):
  page=doc[p-1];il=page.get_images(full=True)
  entry={"page":p,"native_image_count":len(il),"text_layer_chars":len(page.get_text("text"))}
  if len(il)==1:
   raw_img=doc.extract_image(il[0][0])["image"]
   im=Image.open(io.BytesIO(raw_img)).convert("RGB")
   entry.update({"dimensions":list(im.size),"native_rgb_sha256":digest(im.tobytes())})
   bio=io.BytesIO();im.save(bio,format="JPEG",quality=89,optimize=True)
   data=bio.getvalue();name=f"native-original-p{p:03}.jpg"
   (OUT/name).write_bytes(data)
   entry.update({"jpeg_file":name,"jpeg_sha256":digest(data)})
  else:
   pix=page.get_pixmap(matrix=fitz.Matrix(1.0,1.0),alpha=False)
   im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
   entry.update({"embedded_scan_not_unique":True})
  cell=im.copy();cell.thumbnail((220,292))
  imgs.append((p,cell))
  manifest["page_originals"].append(entry)
 for offset in range(0,len(imgs),16):
  chosen=imgs[offset:offset+16]
  sheet=Image.new("RGB",(4*238,4*323),"white")
  draw=ImageDraw.Draw(sheet)
  for i,(n,img) in enumerate(chosen):
   x=(i%4)*238;y=(i//4)*323
   sheet.paste(img,(x+7,y+23));draw.text((x+9,y+4),f"PDF {n}",fill="black")
  bio=io.BytesIO();sheet.save(bio,format="JPEG",quality=82,optimize=True)
  dat=bio.getvalue();name=f"summer-navigation-{chosen[0][0]:03}-{chosen[-1][0]:03}.jpg"
  (OUT/name).write_bytes(dat);manifest["contact_sheets"].append({"file":name,"sha256":digest(dat),"pages":[chosen[0][0],chosen[-1][0]]})
  emit("ATLAS_B64",name,dat)
 (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("13DC_SOURCE_OK",SHA,"PAGES",len(doc),"SCOPED",START,END,flush=True)
if __name__=="__main__":main()
