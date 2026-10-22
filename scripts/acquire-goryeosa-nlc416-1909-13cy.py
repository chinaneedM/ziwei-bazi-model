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
        probe_pages=[134,140,141,142,143,144,145,146,147,148,149,150,178,179]
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
        # Source-native, non-OCR crops for the newly located volume 52.
        # These are image artifacts, never automatic textual adjudications.
        target_crops=[
            (142,"table-heading-and-first-days",(0.10,0.075,0.92,0.82)),
            (143,"day12-to-day17-lower-panel",(0.10,0.44,0.91,0.85)),
            (143,"day16-adjacent-columns",(0.20,0.47,0.55,0.80)),
        ]
        r["target_source_native_crops"]=[]
        for page_number,tag,fractional_bbox in target_crops:
            pix=doc[page_number-1].get_pixmap(matrix=fitz.Matrix(4,4),alpha=False)
            img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            x0,y0,x1,y1=fractional_bbox
            bbox=(round(img.width*x0),round(img.height*y0),
                  round(img.width*x1),round(img.height*y1))
            crop=img.crop(bbox)
            bio=io.BytesIO()
            crop.save(bio,format="JPEG",quality=93,optimize=True)
            data=bio.getvalue()
            name=f"source-native-p{page_number:03}-{tag}-4x.jpg"
            (OUT/name).write_bytes(data)
            r["target_source_native_crops"].append({
                "pdf_page":page_number,"file":name,
                "raster_matrix":4,"fractional_bbox":list(fractional_bbox),
                "pixel_bbox":list(bbox),"pixels":list(crop.size),
                "bytes":len(data),"sha256":digest(data),
                "status":"SOURCE_NATIVE_IMAGE_NOT_AUTOMATIC_GLYPH_TRANSCRIPTION"})
            if args.emit_preview_base64:
                print(f"13CY_TARGET_BASE64_BEGIN {name} {len(data)}")
                print(base64.b64encode(data).decode("ascii"))
                print(f"13CY_TARGET_BASE64_END {name}")
        # Source-embedded RGB column probes; unlike raster thumbnails these
        # crop the original scan pixels and can be replayed against 13CZ hashes.
        embedded_page=doc[142].get_images(full=True)
        if len(embedded_page)!=1:
            raise RuntimeError("PDF p143 embedded image count changed")
        embedded_bytes=doc.extract_image(embedded_page[0][0])["image"]
        source_rgb=Image.open(io.BytesIO(embedded_bytes)).convert("RGB")
        if source_rgb.size!=(1486,2162):
            raise RuntimeError("PDF p143 native scan dimensions changed")
        r["native_p143_rgb_sha256"]=digest(source_rgb.tobytes())
        if r["native_p143_rgb_sha256"]!="30fd1c9c1601d871d1739a8691e90183960ca19ce3e2f225fd1573ddb8e110b4":
            raise RuntimeError("PDF p143 source RGB no longer matches 13CZ")
        raw_lanes=[
            (15,"short_long_context",(611,1080,750,1715)),
            (16,"short_long_context",(429,1080,569,1715)),
            (17,"short_long_context",(246,1080,387,1715)),
            (15,"candidate_long",(618,1080,663,1715)),
            (16,"candidate_long",(435,1080,480,1715)),
            (17,"candidate_long",(252,1080,297,1715)),
        ]
        r["native_p143_column_probes"]=[]
        for day,lane,bbox in raw_lanes:
            cut=source_rgb.crop(bbox)
            rgb_hash=digest(cut.tobytes())
            io_buffer=io.BytesIO()
            cut.save(io_buffer,format="PNG",optimize=True)
            png_bytes=io_buffer.getvalue()
            file_name=f"native-p143-day{day:02}-{lane}.png"
            (OUT/file_name).write_bytes(png_bytes)
            r["native_p143_column_probes"].append({
                "pdf_page":143,"day":day,"lane":lane,
                "bbox":list(bbox),"native_rgb_sha256":rgb_hash,
                "file":file_name,"status":"CANDIDATE_VISUAL_COLUMN_REGION_UNREVIEWED"})
            print("13CY_NATIVE_COLUMN_SHA",day,lane,rgb_hash,file_name)
            if args.emit_preview_base64:
                print(f"13CY_COLUMN_BASE64_BEGIN {file_name} {len(png_bytes)}")
                print(base64.b64encode(png_bytes).decode("ascii"))
                print(f"13CY_COLUMN_BASE64_END {file_name}")
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
