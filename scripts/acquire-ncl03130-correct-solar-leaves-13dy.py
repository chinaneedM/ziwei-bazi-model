#!/usr/bin/env python3
"""13DY — acquire SHA-bound NCL03130 correct solar section upstream of p81.

Keep all original images, no OCR; page or historical-field interpretation is
strictly separate and MUST NOT be inferred from positional arithmetic.
"""
import hashlib,json
from pathlib import Path
from urllib.parse import urlsplit
import fitz,requests
OUT=Path("ncl03130-13dy-correct-solar-original-pages")
URL="https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
SHA="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
BYTES=50735589
PAGES=list(range(73,81))
def digest(x):return hashlib.sha256(x).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 result={"schema":"TIANWEN-13DY-NCL03130-SOLAR-TARGET-REACQUISITION-R1","source":URL,
 "source_sha256_expected":SHA,"source_bytes_expected":BYTES,"source_physical_copy":"UNBOUND",
 "corrected_prior_p86_target":"TAIYIN_LIMIT_28_NOT_SOLAR_DAY_28","requested_pages":PAGES,
 "solar_day28_original_page":"UNREAD","solar_xingdu_day28_original":"UNREAD",
 "no_ocr":True,"status":"INITIAL","pages":[]}
 try:
  chunks=[];size=0;hasher=hashlib.sha256()
  with requests.get(URL,stream=True,allow_redirects=True,timeout=(30,180),
       headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as response:
   response.raise_for_status()
   p=urlsplit(response.url)
   if p.scheme!="https" or p.hostname not in ("commons.wikimedia.org","upload.wikimedia.org"):
    raise RuntimeError("non-whitelisted redirect")
   for chunk in response.iter_content(1024*1024):
    if not chunk:continue
    size+=len(chunk)
    if size>60000000:raise RuntimeError("source exceeded 60MB")
    hasher.update(chunk);chunks.append(chunk)
  data=b"".join(chunks)
  if size!=BYTES or hasher.hexdigest()!=SHA or not data.startswith(b"%PDF-"):
   raise RuntimeError("PDF SOURCE BYTE OR SHA CONTRACT MISMATCH")
  with fitz.open(stream=data,filetype="pdf") as pdf:
   if pdf.is_encrypted or len(pdf)!=189:raise RuntimeError("PDF FORMAT OR PAGE COUNT MISMATCH")
   for page_no in PAGES:
    pix=pdf[page_no-1].get_pixmap(matrix=fitz.Matrix(3.1,3.1),alpha=False)
    png=pix.tobytes("png")
    name=f"original-p{page_no:03d}.png"
    (OUT/name).write_bytes(png)
    result["pages"].append({"page":page_no,"png_file":name,"png_sha256":digest(png),
      "rgb_sha256":digest(pix.samples),"size":[pix.width,pix.height],
      "original_solar_table_title":"PENDING_MANUAL","printed_day28":"PENDING_MANUAL","xingdu":"PENDING_MANUAL"})
    print("13DY_PAGE",page_no,"PNG",len(png),"SHA",digest(png),flush=True)
  result["status"]="SHA_VERIFIED_P73_P80_CAPTURED_ORIGINAL_GLYPHS_UNREAD"
  print("13DY_PASS",SHA,size,len(PAGES),flush=True)
 except Exception as exc:
  result.update(status="SOURCE_ACCESS_OR_REPLAY_BLOCKED",error_type=type(exc).__name__,error=str(exc)[:230])
  raise
 finally:
  (OUT/"manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
