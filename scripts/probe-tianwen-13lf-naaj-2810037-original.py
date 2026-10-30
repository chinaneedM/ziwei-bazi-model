#!/usr/bin/env python3
"""13LF public NAJDA 281-0037 original PDF source route. NEVER OCR or infer historical glyphs."""
import hashlib, io, json, os, urllib.parse, urllib.request
from pathlib import Path
from urllib.parse import urlparse
import fitz
from PIL import Image, ImageDraw

API="https://commons.wikimedia.org/w/api.php"
OUTPUT=Path("13lf-naaj-2810037-output")
OUTPUT.mkdir(parents=True,exist_ok=True)
BOOKS=(10,11,12,13,14)
def req(url):
    request=urllib.request.Request(url,headers={"User-Agent":"TianwenHistorySourceAudit/1.0 (Wikimedia Commons source integrity review)"})
    return urllib.request.urlopen(request,timeout=75)
def metadata(book):
    name=f"NAJDA-281-0037 明史{book}.pdf"
    args=urllib.parse.urlencode({"action":"query","format":"json","prop":"imageinfo","iiprop":"url|sha1|size","titles":"File:"+name})
    with req(API+"?"+args) as response:
        data=json.load(response)
    pages=list(data["query"]["pages"].values())
    assert len(pages)==1 and "missing" not in pages[0] and "imageinfo" in pages[0],"Commons source not found"
    info=pages[0]["imageinfo"][0]
    assert urlparse(info["url"]).netloc=="upload.wikimedia.org" and len(info["sha1"])==40 and 10000<int(info["size"])<100_000_000,"untrusted image metadata"
    return name,info
def download(book,meta):
    path=OUTPUT/f"original-2810037-book{book:03d}.pdf"
    sha1=hashlib.sha1();sha256=hashlib.sha256();size=0
    with req(meta["url"]) as response, path.open("wb") as out:
        while True:
            chunk=response.read(1024*1024)
            if not chunk:break
            size+=len(chunk)
            assert size<=100_000_000,"original file exceeds safety ceiling"
            out.write(chunk);sha1.update(chunk);sha256.update(chunk)
    assert size==int(meta["size"]) and sha1.hexdigest()==meta["sha1"],"source original hash mismatch"
    return path,{"sha1":sha1.hexdigest(),"sha256":sha256.hexdigest(),"bytes":size}
def atlas(book,path,entry):
    pdf=fitz.open(str(path))
    assert 1<=len(pdf)<=400,"unexpected original volume pages"
    entry["pdf_pages"]=len(pdf)
    entry["page_samples"]=[]
    thumbnails=[]
    for i in range(len(pdf)):
        page=pdf[i]
        low=page.get_pixmap(matrix=fitz.Matrix(0.18,0.18),alpha=False)
        thumb=Image.open(io.BytesIO(low.tobytes("png"))).convert("RGB")
        thumb.thumbnail((240,290))
        thumbnails.append((i+1,thumb.copy()))
        if i<6:
            pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
            img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            out=OUTPUT/f"book{book:03d}-native-first-p{i+1:03d}.png"
            img.save(out)
            entry["page_samples"].append({"pdf_page":i+1,"rgb_sha256":hashlib.sha256(img.tobytes()).hexdigest(),"pixels":[img.width,img.height],"original_heading_manual_review":"PENDING"})
    entry["sheets"]=[]
    for start in range(0,len(thumbnails),20):
        canvas=Image.new("RGB",(5*260,4*325),"white");draw=ImageDraw.Draw(canvas)
        for slot,(page_num,im) in enumerate(thumbnails[start:start+20]):
            x=(slot%5)*260;y=(slot//5)*325
            canvas.paste(im,(x+7,y+24));draw.text((x+6,y+4),f"Book {book} PDF p{page_num}",fill="black")
        dst=OUTPUT/f"book{book:03d}-atlas-{start//20+1:02d}.jpg"
        canvas.save(dst,quality=78)
        entry["sheets"].append({"name":dst.name,"sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),"page_range":[start+1,min(start+20,len(thumbnails))]})
    pdf.close()
def main():
    result={"status":"SOURCE_ACQUISITION_ATTEMPTED_NO_HISTORICAL_GLYPH_AWARDED","official_holding":"https://www.digital.archives.go.jp/file/3602570","reference_code":"281-0037","source_volumes":120,"candidate_books_not_confirmed_historical_chapter":list(BOOKS),"historical_target_chapter":"明史卷三十五","target_book_original_verified":False,"numerical_glyph_original_verified":False,"independent_textual_recension_votes":0,"new_historical_numeric_winners":0,"no_ocr":True,"books":[]}
    found=0
    for book in BOOKS:
        entry={"book_number":book,"contains_historical_juan35":"UNKNOWN","glyph_reading":None}
        try:
            filename,meta=metadata(book)
            path,digests=download(book,meta)
            entry.update({"status":"FILE_SHA1_AND_SIZE_VERIFIED_NOT_CHAPTER_BOUND","filename":filename,"source_url":meta["url"],"metadata_sha1":meta["sha1"],**digests})
            atlas(book,path,entry)
            entry["full_original_retained_in_artifact"]=True
            found+=1
        except Exception as exc:
            entry["status"]="ACCESS_OR_HASH_ERROR_NO_HISTORICAL_ABSENCE"
            entry["error"]=type(exc).__name__+": "+str(exc)[:300]
        result["books"].append(entry)
        (OUTPUT/"acquisition.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result["downloaded_and_hash_checked_books"]=found
    (OUTPUT/"acquisition.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"downloaded_and_hash_checked_books":found,"book_statuses":[[x["book_number"],x["status"]] for x in result["books"]],"original_target_chapter_confirmed":False},ensure_ascii=False))
    if not found:raise RuntimeError("No original book acquired; blocked source route, not negative historical proof")
if __name__=="__main__":main()
