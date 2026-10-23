#!/usr/bin/env python3
"""13DK bounded source-original PDF preservation of Commons NCL 03130 mirror part09.
Provides hash-authenticated source bytes for full manual offline juan mapping; no OCR.
"""
import hashlib,json
from pathlib import Path
from urllib.parse import urlsplit
import requests,fitz
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_09_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
EXPECTED_SHA="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
EXPECTED_BYTES=50735589
OUT=Path("ncl03130-13dk-part09-source")
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 d={"schema":"TIANWEN-13DK-NCL03130-PART09-SHA-PINNED-PDF-PRESERVATION-R1",
    "source":SOURCE,"expected_sha256":EXPECTED_SHA,"bytes":None,
    "mirror_not_firstparty_ncl":True,"documented_target_juan52_in_part":False,
    "manual_image_coverage":"NOT_YET_COLLATED","status":"SOURCE_BOUNDARY"}
 try:
  h=hashlib.sha256();b=[];total=0
  with requests.get(SOURCE,stream=True,timeout=(30,180),allow_redirects=True,
    headers={"User-Agent":"TianwenHistoricalResearch/1.0"}) as r:
   r.raise_for_status()
   p=urlsplit(r.url)
   if p.scheme!="https" or p.hostname not in ("upload.wikimedia.org","commons.wikimedia.org"):
    raise RuntimeError("unsafe redirect")
   for chunk in r.iter_content(1048576):
    if not chunk:continue
    total+=len(chunk)
    if total>60000000:raise RuntimeError("60 MB input bound")
    h.update(chunk);b.append(chunk)
  raw=b"".join(b)
  if len(raw)!=EXPECTED_BYTES or h.hexdigest()!=EXPECTED_SHA or raw[:5]!=b"%PDF-":
   raise RuntimeError("source PDF source drift")
  pdf=fitz.open(stream=raw,filetype="pdf")
  if pdf.is_encrypted or len(pdf)!=189:raise RuntimeError("expected 189 unencrypted pages")
  (OUT/"NCL-03130-09-source.pdf").write_bytes(raw)
  d.update(bytes=total,observed_sha256=h.hexdigest(),pages=189,
           source_file="NCL-03130-09-source.pdf",status="SHA_VERIFIED_MIRROR_PDF_ARCHIVED")
  print("13DK_SOURCE_ARCHIVED",total,h.hexdigest(),189)
 except Exception as e:
  d.update(status="SOURCE_ACCESS_OR_FORMAT_BOUNDARY",error_type=type(e).__name__,error=str(e)[:300])
  raise
 finally:
  (OUT/"manifest.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
