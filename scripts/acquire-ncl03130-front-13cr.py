#!/usr/bin/env python3
"""Acquire public Commons PART 01 for manual source-image review; never infer missing-juan from text/OCR."""
import hashlib
import io
import json
import os
from pathlib import Path
import requests
import fitz
from PIL import Image, ImageDraw

OUT=Path(os.environ.get("NCL13CR_OUT","13cr-public-acquisition"))
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/NCL-03130_01_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf"
MAX_BYTES=62_914_560
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={"source_url":SOURCE,"source_role":"SECONDARY_PUBLIC_COMMONS_MIRROR_ONLY","status":"FAILED_UNTIL_PDF_AND_PAGE_HASHES_BOUND","original_ncl_provider_binding":"UNBOUND","missing_register_read":False,"juan52_missing_status":"UNRESOLVED","third_independent_witnesses":0,"pages":[]}
    try:
        with requests.get(SOURCE,timeout=(25,120),allow_redirects=True,stream=True,headers={"User-Agent":"TianwenHistoricalResearch/1.0 (public-source-study)"}) as r:
            r.raise_for_status()
            if not r.url.startswith("https://"):raise RuntimeError("non-HTTPS redirected source")
            if "wikimedia.org" not in r.url and "wikipedia.org" not in r.url:raise RuntimeError("unexpected host")
            chunks=[];n=0
            for chunk in r.iter_content(1024*1024):
                if not chunk:continue
                n+=len(chunk)
                if n>MAX_BYTES:raise RuntimeError("download exceeded 60MiB bound")
                chunks.append(chunk)
            raw=b"".join(chunks)
            if not raw.startswith(b"%PDF-"):raise RuntimeError("content is not a PDF")
            manifest.update(download_url=r.url,pdf_bytes=len(raw),pdf_sha256=sha(raw))
            if manifest["pdf_sha256"]!="24fb9612634ba085d2546ba6c1f02305aa2a02b9ddfd02f0b645ba0409b5e01e":raise RuntimeError("mirror PDF source digest differs from first captured version")
        doc=fitz.open(stream=raw,filetype="pdf")
        manifest["observed_pages"]=len(doc)
        if len(doc)!=204:raise RuntimeError("PDF page count changed relative to indexed 204; quarantine")
        thumbs=[]
        for i in range(len(doc)):
            pg=doc[i]
            pix=pg.get_pixmap(matrix=fitz.Matrix(0.32,0.32),alpha=False)
            im=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            im.thumbnail((280,210))
            thumbs.append(im.copy())
            rec={"pdf_page_1based":i+1,"preview_rgb_sha256":sha(im.tobytes()),"review_status":"UNREVIEWED_NO_OCR"}
            manifest["pages"].append(rec)
            if i<12:
                larger=pg.get_pixmap(matrix=fitz.Matrix(3.5,3.5),alpha=False)
                name=f"front-page-{i+1:03}.png"
                b=larger.tobytes("png")
                (OUT/name).write_bytes(b)
                rec["preview_file"]=name
                rec["preview_png_sha256"]=sha(b)
        for start in range(0,len(thumbs),20):
            sheet=Image.new("RGB",(5*290,4*235),"white")
            draw=ImageDraw.Draw(sheet)
            for j,im in enumerate(thumbs[start:start+20]):
                x=(j%5)*290;y=(j//5)*235
                sheet.paste(im,(x,y+18))
                draw.text((x+2,y+1),f"PDF {start+j+1:03}",fill="black")
            name=f"contact-{start//20+1:02}.jpg"
            sheet.save(OUT/name,quality=88,optimize=True)
        manifest["status"]="ACQUIRED_MIRROR_BYTES_UNREVIEWED"
        manifest["no_ocr"]=True
        print("13CR_ACQUIRED_MIRROR_BYTES_PAGE_IMAGES_NEED_MANUAL_REVIEW",manifest["pdf_sha256"],len(doc))
    except Exception as exc:
        manifest["error_type"]=type(exc).__name__
        manifest["error"]=str(exc)[:600]
        print("13CR_ACCESS_OR_IMAGE_BOUNDARY",type(exc).__name__,str(exc)[:200])
        raise
    finally:
        (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
