#!/usr/bin/env python3
"""Bounded original PDF acquisition for Harvard/Wikimedia Ming Shi vol. 10.

No OCR, no guessed page locations, and no transfer of source identity to
Tenri/CADAL/NLC holdings. Only Commons-issued file URL or exact file redirect.
"""
import hashlib
import json
import os
import urllib.parse
from pathlib import Path


TITLE="File:Harvard drs 428231183 明史 v.10.pdf"
API="https://commons.wikimedia.org/w/api.php"
SPECIAL="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(TITLE[5:],safe="")
CAP=170_000_000
OUT=Path(os.environ.get("TIANWEN_13KF_OUT","/tmp/tianwen-13kf"))

def require(x,msg):
    if not x: raise ValueError(msg)

def validate_source_url(url):
    u=urllib.parse.urlsplit(url)
    require(u.scheme=="https" and u.hostname=="upload.wikimedia.org" and u.path.startswith("/wikipedia/commons/"),"untrusted image host")
    require(u.path.lower().endswith(".pdf"),"not PDF")
    require(not u.username and not u.password and not u.fragment,"malformed media URL")

def parse_metadata(payload):
    pages=payload["query"]["pages"]
    require(len(pages)==1,"multiple file objects")
    page=next(iter(pages.values()))
    require(page.get("title")==TITLE,"wrong Commons title")
    info=page.get("imageinfo",[])
    require(len(info)==1,"source file not available")
    x=info[0]
    require(x.get("mime")=="application/pdf","wrong MIME")
    require(1_000_000 <= x["size"] <= CAP,"unexpected source size")
    validate_source_url(x["url"])
    return x

def acquire(session):
    rec={"schema":"TIANWEN-13KF-HARVARD-MINGSHI-V10-BINARY-INTAKE-R1",
         "object_kind":"SINGLE_HARVARD_DIGITAL_VOLUME_NOT_A_NEW_PROVEN_PHYSICAL_IMPRESSION",
         "title":TITLE,"target_literary_juan":[33,34],
         "commons_file_list":"https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/Harvard-Yenching/1",
         "reference_catalog":"https://www.shuge.org/view/ming_shi/",
         "separate_tenri_catalog":"https://ci.nii.ac.jp/ncid/BD00540342",
         "source":"WIKIMEDIA_COMMONS_HARVARD_DIGITAL_SURROGATE",
         "metadata_verified":False,"pdf_verified":False,"glyphs_collated":False,
         "historical_numeric_winner":False,"same_copy_vs_tenri_assumed":False,
         "original_printing_year_proven_by_scan":False,"transport_attempts":[]}
    url=None
    try:
        response=session.get(API,params={"action":"query","prop":"imageinfo","iiprop":"url|size|mime|sha1","titles":TITLE,"format":"json"},timeout=30)
        rec["metadata_http"]=response.status_code
        if response.status_code==200:
            meta=parse_metadata(response.json())
            url=meta["url"]
            rec["metadata_verified"]=True
            rec["expected_bytes"]=meta["size"]
            rec["commons_sha1"]=meta.get("sha1")
    except Exception as exc:
        rec["metadata_error"]=type(exc).__name__+": "+str(exc)[:180]
    if not url:
        # The exact public Commons redirect is source-issued, not a guessed CDN path.
        url=SPECIAL
        rec["fallback"]="EXACT_COMMONS_FILE_REDIRECT_UNVERIFIED_API_METADATA"
    rec["request_url"]=url
    for attempt in range(1,3):
        entry={"attempt":attempt}
        try:
            with session.get(url,stream=True,timeout=(20,120),allow_redirects=True) as response:
                entry["http"]=response.status_code
                entry["final_host"]=urllib.parse.urlsplit(response.url).hostname
                response.raise_for_status()
                validate_source_url(response.url)
                h=hashlib.sha256(); sha1=hashlib.sha1();total=0
                tmp=OUT/"volume10.pdf.tmp"
                with tmp.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=262144):
                        if not chunk:continue
                        total+=len(chunk)
                        require(total<=CAP,"oversize original PDF")
                        f.write(chunk);h.update(chunk);sha1.update(chunk)
                head=tmp.open("rb").read(8)
                require(head.startswith(b"%PDF-"),"source not PDF")
                if rec["metadata_verified"]:
                    require(total==rec["expected_bytes"],"provider byte length mismatch")
                    if rec.get("commons_sha1"):
                        require(sha1.hexdigest().lower()==rec["commons_sha1"].lower(),"Commons source sha1 mismatch")
                rec.update({"pdf_verified":True,"pdf_bytes":total,"sha256":h.hexdigest(),
                            "sha1":sha1.hexdigest(),"final_pdf_url":response.url})
                tmp.rename(OUT/"volume10.pdf")
                entry["status"]="EXACT_PDF_ACQUIRED"
                rec["transport_attempts"].append(entry)
                break
        except Exception as exc:
            entry["status"]="NOT_ACQUIRED";entry["error"]=type(exc).__name__+": "+str(exc)[:190]
            rec["transport_attempts"].append(entry)
    return rec

def create_atlas(rec):
    import fitz
    from PIL import Image, ImageDraw, ImageFont
    pdf=fitz.open(OUT/"volume10.pdf")
    pages=len(pdf)
    require(1<=pages<=140,"unexpected source PDF page count")
    rec["pdf_page_count"]=pages
    rec["pdf_metadata"]={k:str(v)[:300] for k,v in pdf.metadata.items() if v}
    contact_files=[]
    scale=0.23
    cell_w,cell_h=250,350
    for offset in range(0,pages,16):
        atlas=Image.new("RGB",(4*cell_w,4*cell_h),"white")
        draw=ImageDraw.Draw(atlas)
        for j in range(offset,min(offset+16,pages)):
            pg=pdf.load_page(j)
            pix=pg.get_pixmap(matrix=fitz.Matrix(scale,scale),colorspace=fitz.csRGB,alpha=False)
            thumb=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
            thumb.thumbnail((cell_w-10,cell_h-28))
            x=(j-offset)%4*cell_w;y=(j-offset)//4*cell_h
            atlas.paste(thumb,(x+(cell_w-thumb.width)//2,y+6))
            draw.text((x+5,y+cell_h-18),f"PDF p{j+1}",fill="black")
        name=f"atlas-{offset//16+1:02d}.jpg"
        atlas.save(OUT/name,quality=86)
        contact_files.append(name)
    rec["atlas_files"]=contact_files
    rec["atlas_source_pdf_sha256"]=rec["sha256"]
    rec["ocr_used"]=False
    rec["target_folio_located"]=False
    rec["full_original_glyph_collation_performed"]=False
    pdf.close()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    import requests  # optional network dependency: do not break global offline unittest import
    s=requests.Session()
    s.headers.update({"User-Agent":"Tianwen-historical-source-provenance/1.0 (public edition verification)","Accept":"application/pdf,application/json,*/*"})
    rec=acquire(s)
    if rec["pdf_verified"]:
        try:create_atlas(rec)
        except Exception as exc:rec["atlas_error"]=type(exc).__name__+": "+str(exc)[:200]
    (OUT/"intake.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"pdf_verified":rec["pdf_verified"],"pdf_page_count":rec.get("pdf_page_count"),
                      "atlas_count":len(rec.get("atlas_files",[])),"glyphs_collated":False,
                      "scope":"ONE_HARVARD_DIGITAL_OBJECT_ONLY"},ensure_ascii=False))

if __name__=="__main__":main()
