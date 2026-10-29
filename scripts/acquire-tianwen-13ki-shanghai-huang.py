#!/usr/bin/env python3
"""13KI: bounded source-issued Shanghai Huang Shoushi Ligu PDF intake.

Transport/image atlas only. No OCR, antique impression attribution, target glyph
award, numeric adjudication or physical-copy merging.
"""
import hashlib
import json
import os
import urllib.parse
from pathlib import Path

TITLE="File:Shanghai 授時歷故四卷.pdf"
API="https://commons.wikimedia.org/w/api.php"
REDIRECT="https://commons.wikimedia.org/wiki/Special:Redirect/file/"+urllib.parse.quote(TITLE[5:],safe="")
OUT=Path(os.environ.get("TIANWEN_13KI_OUT","/tmp/tianwen-13ki"))
MAX_BYTES=30_000_000
EXPECTED_SHA1="73c2017bb9eb109edf069f9563c397e7fcb2cba4"
EXPECTED_BYTES=14376480
EXPECTED_PAGES=97
UPSTREAM_UPLOAD_NAME="dGJ2300966.pdf"

def demand(ok,label):
    if not ok: raise ValueError(label)

def valid_original_url(url):
    u=urllib.parse.urlsplit(url)
    demand(u.scheme=="https" and u.hostname=="upload.wikimedia.org" and
           u.path.startswith("/wikipedia/commons/") and
           u.path.lower().endswith(".pdf") and not u.username and not u.password,
           "not Commons original PDF")

def read_metadata(data):
    pages=data["query"]["pages"]
    demand(len(pages)==1,"source object cardinality")
    page=next(iter(pages.values()))
    demand(page.get("title")==TITLE,"source title")
    ii=page.get("imageinfo",[])
    demand(len(ii)==1,"source imageinfo cardinality")
    info=ii[0]
    demand(info.get("mime")=="application/pdf","source MIME")
    demand(info.get("size")==EXPECTED_BYTES,"source byte count")
    demand(info.get("sha1","").lower()==EXPECTED_SHA1,"source sha1")
    valid_original_url(info["url"])
    return info

def download(session):
    meta={"schema":"TIANWEN-13KI-SHANGHAI-HUANG-SHOUSHI-PDF-INTAKE-R1",
          "file_title":TITLE,
          "source_inventory":"https://commons.wikimedia.org/wiki/File:Shanghai_%E6%8E%88%E6%99%82%E6%AD%B7%E6%95%85%E5%9B%9B%E5%8D%B7.pdf",
          "commons_upload_name":UPSTREAM_UPLOAD_NAME,
          "provider": "Commons-listed Shanghai Library digital object, physical copy not identified",
          "expected_sha1":EXPECTED_SHA1,"expected_bytes":EXPECTED_BYTES,
          "source_version":"SINGLE_DIGITAL_OBJECT_NOT_PROVEN_1923_JIAYETANG_PRINT",
          "metadata_verified":False,"pdf_verified":False,"glyph_collation":False,
          "printed_impression_identified":False,"six_numeric_winners_awarded":0,
          "transmission_direct_edges_awarded":0,"algorithm_reopens":0,
          "attempts":[]}
    try:
        r=session.get(API,params={"action":"query","prop":"imageinfo",
                 "iiprop":"url|size|mime|sha1","titles":TITLE,"format":"json"},timeout=30)
        meta["metadata_http"]=r.status_code
        if r.status_code==200:
            info=read_metadata(r.json())
            meta["metadata_verified"]=True
            url=info["url"]
        else:url=REDIRECT
    except Exception as err:
        meta["metadata_error"]=type(err).__name__+":"+str(err)[:170]
        url=REDIRECT
    if url==REDIRECT:meta["metadata_fallback"]="EXACT_FILE_REDIRECT_NOT_INDEPENDENT_SOURCE_METADATA"
    for i in range(2):
        try:
            with session.get(url,stream=True,timeout=(20,100),allow_redirects=True) as r:
                r.raise_for_status();valid_original_url(r.url)
                h=hashlib.sha1();h256=hashlib.sha256();size=0
                tmp=OUT/"original.pdf.tmp"
                with tmp.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=262144):
                        if not chunk:continue
                        size+=len(chunk);demand(size<=MAX_BYTES,"source size cap")
                        h.update(chunk);h256.update(chunk);f.write(chunk)
                demand(size==EXPECTED_BYTES and h.hexdigest()==EXPECTED_SHA1,"source identity mismatch")
                with tmp.open("rb") as f:demand(f.read(5)==b"%PDF-","not PDF bytes")
                tmp.rename(OUT/"original.pdf")
                meta.update({"pdf_verified":True,"sha256":h256.hexdigest(),"sha1":h.hexdigest(),
                             "bytes":size,"pdf_url":r.url})
                meta["attempts"].append({"attempt":i+1,"status":"EXACT_SOURCE_BYTES_VERIFIED"})
                break
        except Exception as e:
            meta["attempts"].append({"attempt":i+1,"status":"NOT_ACQUIRED",
                                     "error":type(e).__name__+":"+str(e)[:200]})
    return meta

def atlas(meta):
    import fitz
    from PIL import Image, ImageDraw
    doc=fitz.open(OUT/"original.pdf")
    demand(len(doc)==EXPECTED_PAGES,"PDF page count changed")
    meta["pages"]=len(doc)
    meta["source_pdf_metadata"]={k:str(v)[:250] for k,v in doc.metadata.items() if v}
    files=[]
    cw,ch=246,320
    for st in range(0,len(doc),16):
        img=Image.new("RGB",(cw*4,ch*4),"white");draw=ImageDraw.Draw(img)
        for p in range(st,min(st+16,len(doc))):
            pix=doc[p].get_pixmap(matrix=fitz.Matrix(.19,.19),colorspace=fitz.csRGB,alpha=False)
            thumb=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
            thumb.thumbnail((cw-12,ch-25))
            x=(p-st)%4*cw;y=(p-st)//4*ch
            img.paste(thumb,(x+(cw-thumb.width)//2,y+5))
            draw.text((x+6,y+ch-16),f"PDF p{p+1}",fill="black")
        filename=f"atlas-{st//16+1:02d}.jpg"
        img.save(OUT/filename,quality=87)
        files.append(filename)
    # First-page physical ownership clue + last-volume inspection candidates.
    for p in (1,2,3,60,70,80,90,96,97):
        pix=doc[p-1].get_pixmap(matrix=fitz.Matrix(.65,.65),colorspace=fitz.csRGB,alpha=False)
        pix.save(str(OUT/f"sample-p{p:03d}.png"))
    meta["atlas_files"]=files
    meta["sampled_pdf_pages"]=[1,2,3,60,70,80,90,96,97]
    meta["target_locus_identified"]=False
    meta["full_line_by_line_corpus_collated"]=False
    meta["ocr_used"]=False
    doc.close()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    import requests
    s=requests.Session()
    s.headers.update({"User-Agent":"Tianwen-source-identity/1.0 (non-commercial historical research)"})
    report=download(s)
    if report["pdf_verified"]:
        try:atlas(report)
        except Exception as e:report["atlas_error"]=type(e).__name__+":"+str(e)[:160]
    (OUT/"intake.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"pdf_verified":report["pdf_verified"],"pages":report.get("pages"),
          "sha256":report.get("sha256"),"atlases":len(report.get("atlas_files",[])),
          "ancient_printed_original_winner":False,"target_glyphs_collated":False},ensure_ascii=False))
    if not report["pdf_verified"] or report.get("pages")!=EXPECTED_PAGES:raise SystemExit(2)

if __name__=="__main__":main()
