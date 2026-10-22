#!/usr/bin/env python3
"""13CY bounded original-file acquisition; no OCR, no claim of direct target D16 read."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path

import fitz
import requests
from PIL import Image, ImageDraw

SOURCE = ("https://commons.wikimedia.org/wiki/Special:Redirect/file/"
          "NLC416-13jh005095-74760_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf")
MAX_BYTES = 55_000_000
EXPECTED_PAGES = 755
EXPECTED_SHA256 = "b4bd5c557c7ba44bac1fc881e6c2e8784c9d56a8d2629f17b5255a1ec6bd9e97"
FIRST = 1
LAST = EXPECTED_PAGES
PER_SHEET = 40
OUT = Path(os.environ.get("TIANWEN_13CY_OUTPUT", "goryeosa-13cy-original"))
def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--emit-preview-base64", action="store_true")
    args=parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    r={"schema":"TIANWEN-13CY-NLC416-1909-PHYSICAL-PAGE-SOURCE-INSTRUMENT-R1",
       "source":SOURCE,"expected_pages":EXPECTED_PAGES,
       "status":"NOT_ACQUIRED","sha256_original_pdf":"UNBOUND",
       "source_class":"COMMONS_MIRROR_OF_DESCRIBED_NLC_1909_PRINT_NOT_FIRSTPARTY_ITEM",
       "no_ocr":True,"searched_original_glyph":False,
       "target_d16_quoted_from_1909":False,"third_ancient_witnesses":0,
       "contact_sheets":[],"reviewed_target_pages":[]}
    try:
        with requests.get(SOURCE,stream=True,timeout=(35,210),allow_redirects=True,
                          headers={"User-Agent":"TianwenResearch/1.0 (public historical source collation)"}) as response:
            response.raise_for_status()
            host=requests.utils.urlparse(response.url).hostname
            if host not in ("upload.wikimedia.org","commons.wikimedia.org"):
                raise RuntimeError("redirect left expected Wikimedia source hosts")
            chunks=[];total=0;sha=hashlib.sha256()
            for chunk in response.iter_content(1024*1024):
                if not chunk:continue
                total+=len(chunk)
                if total>MAX_BYTES:raise RuntimeError("source exceeds 55MB hard limit")
                sha.update(chunk);chunks.append(chunk)
            raw=b"".join(chunks)
            if raw[:5]!=b"%PDF-": raise RuntimeError("unexpected source magic")
            r.update({"download_url":response.url,"source_bytes":total,
                      "sha256_original_pdf":sha.hexdigest()})
            if r["sha256_original_pdf"] != EXPECTED_SHA256:
                raise RuntimeError("source file SHA-256 changed since verified 13CY acquisition")
            r["expected_sha256_original_pdf"] = EXPECTED_SHA256
            pdfpath=OUT/"NLC416-1909-source.pdf"
            pdfpath.write_bytes(raw)
        doc=fitz.open(stream=raw,filetype="pdf")
        r["observed_pdf_pages"]=len(doc)
        if len(doc)!=EXPECTED_PAGES:raise RuntimeError(f"observed {len(doc)} pages, expected 755")
        if doc.is_encrypted: raise RuntimeError("encrypted input")
        r["embedded_text_page_samples"]=[]
        for p in [0,1,39,79,119,159,199,219,754]:
            content=doc[p].get_text("text")
            r["embedded_text_page_samples"].append({
                "pdf_page":p+1,"text_chars":len(content),
                "nonempty_text_layer":bool(content.strip())})
        r["atlas_scope"]={"start":FIRST,"end":LAST,"status":"ALL_PAGES_THUMBNAILS_UNREVIEWED_NOT_GLYPH_COLLATION"}
        for start in range(FIRST,LAST+1,PER_SHEET):
            hi=min(start+PER_SHEET-1,LAST)
            sheet=Image.new("RGB",(8*150,5*225),"white")
            draw=ImageDraw.Draw(sheet)
            for page in range(start,hi+1):
                page_obj=doc[page-1]
                pix=page_obj.get_pixmap(matrix=fitz.Matrix(0.24,0.24),alpha=False)
                img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
                img.thumbnail((138,198))
                idx=page-start;x=(idx%8)*150;y=(idx//8)*225
                sheet.paste(img,(x+5,y+20))
                draw.text((x+5,y+3),f"PDF p{page:03}",fill="black")
            bio=io.BytesIO();sheet.save(bio,format="JPEG",quality=77,optimize=True)
            data=bio.getvalue();name=f"contact-p{start:03}-{hi:03}.jpg"
            (OUT/name).write_bytes(data)
            r["contact_sheets"].append({"file":name,"start":start,"end":hi,"bytes":len(data),"sha256":digest(data)})
            if args.emit_preview_base64:
                print(f"13CY_ATLAS_BASE64_BEGIN {name} {len(data)}")
                print(base64.b64encode(data).decode("ascii"))
                print(f"13CY_ATLAS_BASE64_END {name}")
        # Coarse structural navigation only. These source-rendered pages are not
        # transcribed text and must never be counted as target-glyph collation.
        probe_pages=[2,71,175,222,335,446,533,610,658,675,688,707,726,727,728,739,754]
        r["native_page_probes"]=[]
        for page_number in probe_pages:
            pix=doc[page_number-1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
            img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            bio=io.BytesIO()
            img.save(bio,format="JPEG",quality=87,optimize=True)
            data=bio.getvalue()
            name=f"original-navigation-p{page_number:03}.jpg"
            (OUT/name).write_bytes(data)
            r["native_page_probes"].append({
                "pdf_page":page_number,"file":name,"bytes":len(data),
                "sha256":digest(data),"interpretation":"UNREVIEWED_NO_GLYPH_PROMOTION"})
            if args.emit_preview_base64:
                print(f"13CY_NAV_BASE64_BEGIN {name} {len(data)}")
                print(base64.b64encode(data).decode("ascii"))
                print(f"13CY_NAV_BASE64_END {name}")
        r["status"]="ACQUIRED_SHA256_PINNED_ALL_PAGES_THUMBNAILS_UNREVIEWED"
        print("13CY_SOURCE_PDF",r["sha256_original_pdf"],"BYTES",r["source_bytes"],"PAGES",len(doc))
    except Exception as exc:
        r["status"]="SOURCE_ACCESS_OR_FORMAT_BOUNDARY"
        r["error_type"]=type(exc).__name__
        r["error_message"]=str(exc)[:800]
        print("13CY_SOURCE_ACCESS_BOUNDARY",type(exc).__name__,str(exc)[:150])
        raise
    finally:
        (OUT/"manifest.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":main()
