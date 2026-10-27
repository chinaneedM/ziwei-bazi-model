#!/usr/bin/env python3
"""12WI: physical-paratext acquisition candidate: original Commons CADAL fascicle1.

Acquire original publisher-hosted scan, SHA-grade it, generate page atlas/contact
sheets for human image review. Zero OCR, print-year or copy-identity inference.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess,tempfile,urllib.parse,urllib.request
from pathlib import Path

TITLE="File:CADAL02096900 野獲編（一）.djvu"
CADAL_ID="02096900"
COMMS_API="https://commons.wikimedia.org/w/api.php"
EXPECTED_INVENTORY_BYTES=2833699
MAX_SOURCE=8_000_000
UA="TIANWEN-historical-12WI-paratext-source/1.0 (Commons official file, no OCR)"
def hash_file(path,alg="sha256"):
    h=hashlib.new(alg)
    with Path(path).open("rb") as f:
        for part in iter(lambda:f.read(1024*1024),b""):h.update(part)
    return h.hexdigest()
def check_host(url):
    u=urllib.parse.urlparse(url)
    if u.scheme!="https" or u.hostname!="upload.wikimedia.org" or not u.path.startswith("/wikipedia/commons/"):
        raise ValueError("non-commons original image host")
def resolve():
    q=urllib.parse.urlencode({"action":"query","prop":"imageinfo","iiprop":"url|size|sha1","format":"json","formatversion":"2","titles":TITLE})
    with urllib.request.urlopen(urllib.request.Request(COMMS_API+"?"+q,headers={"User-Agent":UA}),timeout=40) as r:
        obj=json.load(r)
    pages=obj.get("query",{}).get("pages",[])
    if len(pages)!=1 or not pages[0].get("imageinfo"):raise ValueError("no source-emitted Commons file identity")
    info=pages[0]["imageinfo"][0]
    check_host(info["url"])
    if info["size"]!=EXPECTED_INVENTORY_BYTES:raise ValueError("source file-size drift from published Commons listing")
    if not isinstance(info["sha1"],str) or len(info["sha1"])!=40:raise ValueError("source sha1 missing")
    return info
def download(info,path):
    request=urllib.request.Request(info["url"],headers={"User-Agent":UA})
    seen=0
    with urllib.request.urlopen(request,timeout=60) as r,Path(path).open("wb") as out:
        check_host(r.geturl())
        for chunk in iter(lambda:r.read(1024*1024),b""):
            seen+=len(chunk)
            if seen>MAX_SOURCE:raise ValueError("over 8MB source download boundary")
            out.write(chunk)
    if seen!=info["size"] or hash_file(path,"sha1")!=info["sha1"]:raise ValueError("original Commons source bytes/SHA1 mismatch")
    with Path(path).open("rb") as f:
        if f.read(8)!=b"AT&TFORM":raise ValueError("not genuine DJVU")
    return {"bytes":seen,"sha1":hash_file(path,"sha1"),"sha256":hash_file(path)}
def count_pages(src):
    x=subprocess.run(["djvused",str(src),"-e","n"],capture_output=True,text=True,check=True)
    count=int(x.stdout.strip())
    if not 30<=count<=500:raise ValueError("implausible first fascicle page count")
    return count
def render(src,num,outfile):
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        ppm=Path(tmp)/"page.ppm"
        subprocess.run(["ddjvu","-format=ppm",f"-page={num}",str(src),str(ppm)],check=True,timeout=60,stdout=subprocess.DEVNULL)
        with Image.open(ppm) as image:
            rgb=image.convert("RGB")
            original=list(rgb.size)
            rgb.thumbnail((1250,1800),Image.Resampling.LANCZOS)
            rgb.save(outfile,"JPEG",quality=84,optimize=True)
            return {"page":num,"original_dimensions":original,"display_dimensions":list(rgb.size),
                "jpeg_bytes":Path(outfile).stat().st_size,"jpeg_sha256":hash_file(outfile)}
def sheets(out,pages):
    from PIL import Image,ImageDraw
    contacts=[]
    for offset in range(0,len(pages),12):
        block=pages[offset:offset+12]
        canvas=Image.new("RGB",(4*360,3*600),(245,245,245))
        draw=ImageDraw.Draw(canvas)
        for j,e in enumerate(block):
            with Image.open(out/f"p{e['page']:03}.jpg") as img:
                thumb=img.convert("RGB")
                thumb.thumbnail((340,550),Image.Resampling.BILINEAR)
                x=(j%4)*360+(360-thumb.width)//2
                y=(j//4)*600+28
                canvas.paste(thumb,(x,y))
                draw.text(((j%4)*360+10,(j//4)*600+4),f"Source page {e['page']}",fill=(10,10,10))
        name=f"contact-{offset//12+1:02}.jpg"
        canvas.save(out/name,quality=83,optimize=True)
        contacts.append({"file":name,"jpeg_sha256":hash_file(out/name),"pages":[e["page"] for e in block]})
    return contacts
def capture(folder):
    out=Path(folder);out.mkdir(parents=True,exist_ok=True)
    info=resolve()
    file=out/(CADAL_ID+".djvu")
    d=download(info,file)
    n=count_pages(file)
    selected=sorted(set(range(1,min(44,n)+1)).union(range(max(1,n-3),n+1)))
    pics=[render(file,x,out/f"p{x:03}.jpg") for x in selected]
    contacts=sheets(out,pics)
    result={"schema":"TIANWEN-12WI-CADAL02096900-ORIGINAL-PARATEXT-PAGE-ATLAS-R1",
        "status":"SOURCE_FILE_AND_EARLY_LATE_PAGES_CAPTURED_NOT_HUMAN_GLYPH_COLLATED",
        "title":TITLE,"source_url":info["url"],"cadal_id":CADAL_ID,
        "source":d,"source_pages":n,"selected_pages":pics,"contacts":contacts,
        "source_to_CADAL02096915_same_paper_copy_proven":False,
        "original_1827_first_impression_proven":False,"original_1869_revision_impression_proven":False,
        "new_ancient_print_votes":0,"manual_glyph_collation":False,"ocr_used":False}
    (out/"atlas.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"source_sha256":d["sha256"],"djvu_pages":n,
        "pages_selected":selected,"contact_sheets":[x["file"] for x in contacts],
        "source_paper_copy_impression":"UNBOUND","new_print_votes":0},ensure_ascii=False))
    return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",default="cadal-12wi-first-fascicle")
    x=p.parse_args()
    try:capture(x.output_dir)
    except Exception as e:
        out=Path(x.output_dir);out.mkdir(parents=True,exist_ok=True)
        (out/"capture-error.json").write_text(json.dumps({"status":"SOURCE_CAPTURE_FAILED_NO_HISTORICAL_VOTE",
            "error":type(e).__name__+":"+str(e)[:400],"historical_votes":0},ensure_ascii=False))
        raise
if __name__=="__main__":main()
