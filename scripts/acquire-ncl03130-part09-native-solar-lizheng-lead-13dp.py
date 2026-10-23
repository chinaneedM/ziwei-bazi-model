#!/usr/bin/env python3
"""13DP: original earlier-book numeric table and possible winter source-original glyph review; SHA-bound, no OCR.

A photographed cover ordinal != textual juan identifier. The source is a
Wikimedia mirror, not a verified Taiwan NCL first-party item binding.
"""
import base64,hashlib,io,json
from pathlib import Path
from urllib.parse import urlsplit
import fitz,requests
from PIL import Image
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
PDF_SHA="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
PDF_SIZE=50735589
PAGES=(65,66,67,68,69,70,71,72,103,104,105,106)
OUT=Path("ncl03130-13dp-source-native-solar-lizheng-lead")
def hash_bytes(v):return hashlib.sha256(v).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 m={"schema":"TIANWEN-13DP-NCL03130-PART09-BOOK-BOUNDARY-NATIVE-R1",
    "source":SOURCE,"source_sha256":PDF_SHA,"source_class":"COMMONS_MIRROR_NOT_FIRSTPARTY_NCL",
    "item_identity":"UNBOUND","textual_juan52":"UNRESOLVED","winter_d16_exact_source_page":"REQUIRES_GLYPH_REVIEW",
    "pages":[],"no_ocr":True,"status":"STARTED"}
 try:
  chunks=[];n=0;h=hashlib.sha256()
  with requests.get(SOURCE,stream=True,allow_redirects=True,timeout=(30,180),
       headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as resp:
   resp.raise_for_status()
   p=urlsplit(resp.url)
   if p.scheme!="https" or p.hostname not in ("commons.wikimedia.org","upload.wikimedia.org"):
    raise RuntimeError("unsafe download redirect")
   for chunk in resp.iter_content(1024*1024):
    if not chunk:continue
    n+=len(chunk)
    if n>60000000:raise RuntimeError("source cap")
    h.update(chunk);chunks.append(chunk)
  raw=b"".join(chunks)
  if n!=PDF_SIZE or h.hexdigest()!=PDF_SHA or not raw.startswith(b"%PDF-"):
   raise RuntimeError("source digest or size drift")
  d=fitz.open(stream=raw,filetype="pdf")
  if d.is_encrypted or len(d)!=189:raise RuntimeError("source page-count boundary")
  for i in PAGES:
   pix=d[i-1].get_pixmap(matrix=fitz.Matrix(2.6,2.6),alpha=False)
   png=pix.tobytes("png")
   (OUT/f"native-p{i:03d}.png").write_bytes(png)
   im=Image.open(io.BytesIO(png)).convert("RGB")
   im.thumbnail((2100,1600))
   j=io.BytesIO();im.save(j,format="JPEG",quality=88,optimize=True)
   jpg=j.getvalue()
   (OUT/f"preview-p{i:03d}.jpg").write_bytes(jpg)
   m["pages"].append({"pdf_page":i,"png_sha256":hash_bytes(png),"preview_sha256":hash_bytes(jpg),
                       "raw_rgb_sha256":hash_bytes(pix.samples),"native_dimensions":[pix.width,pix.height],
                       "glyph_read":"PENDING_MANUAL_READ"})
   print("13DP_PAGE_BEGIN",i,len(jpg),flush=True)
   print(base64.b64encode(jpg).decode(),flush=True)
   print("13DP_PAGE_END",i,flush=True)
  m["status"]="NATIVE_GLYPH_IMAGES_READY_UNINTERPRETED"
  print("13DP_SOURCE_PASS",PDF_SHA,n,len(d),flush=True)
 except Exception as e:
  m.update(status="SOURCE_OR_RENDER_BOUNDARY",error_type=type(e).__name__,error=str(e)[:240])
  raise
 finally:
  (OUT/"manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
