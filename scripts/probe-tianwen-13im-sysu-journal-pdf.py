#!/usr/bin/env python3
"""Read-only public university PDF probe. Metadata only, no copyrighted file committed."""
import hashlib, json, urllib.request, urllib.error
from pathlib import Path
URL="https://sir.sysu.edu.cn/sites/default/files/2026-07/%E9%AB%98%E4%B8%BD%E5%8F%B2_%E7%89%88%E6%9C%AC%E6%BA%90%E6%B5%81%E4%B8%8E%E7%BC%96%E7%BA%82%E4%BD%93%E4%BE%8B%E8%80%83_%E9%AD%8F%E5%BF%97%E6%B1%9F.pdf"
OUT=Path("docs/research/artifacts/13im-official-journal-probe.json")
MAX=25*1024*1024
def probe(url=URL):
    out={"url":url,"request_method":"GET","pdf_bytes_obtained":False,"pdf_sha256":None,"pdf_pages":None,"source_original_text_glyph_adjudicated":False}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"TianwenAcademicSourceVerification/1.0"})
        with urllib.request.urlopen(req, timeout=25) as response:
            out["status"]=getattr(response,"status",None)
            out["content_type"]=response.headers.get("Content-Type")
            raw=response.read(MAX+1)
            out["bytes_received"]=len(raw)
            if len(raw)>MAX:
                out["result"]="SIZE_LIMIT_EXCEEDED_NO_ARCHIVE"
            elif raw.startswith(b"%PDF-"):
                out["pdf_bytes_obtained"]=True
                out["pdf_sha256"]=hashlib.sha256(raw).hexdigest()
                try:
                    import fitz
                    doc=fitz.open(stream=raw,filetype="pdf")
                    out["pdf_pages"]=len(doc)
                    out["printed_100_text_layer_contains_5553_and_5554"]=len(doc)>7 and all(s in doc[7].get_text() for s in ("5553","5554"))
                    out["result"]="ORIGINAL_BYTES_VERIFIED_NOT_ARCHIVED"
                except Exception as e:
                    out["page_parse_error"]=type(e).__name__
                    out["result"]="PDF_MAGIC_SHA_VERIFIED_PAGE_PARSE_UNAVAILABLE"
            else:
                out["result"]="NOT_PDF_MAGIC"
    except Exception as e:
        out["result"]="ACCESS_BOUNDARY_NO_PDF_BYTES"
        out["error_type"]=type(e).__name__
        out["error_excerpt"]=str(e)[:200]
    return out
if __name__=="__main__":
    OUT.parent.mkdir(parents=True,exist_ok=True)
    result=probe()
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
