#!/usr/bin/env python3
"""13KT scoped public Harvard/Commons v11 original acquisition; never infer target glyph from thumbnails."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import requests
import fitz
from PIL import Image,ImageDraw

NAME="Harvard drs 428231199 明史 v.11.pdf"
API="https://commons.wikimedia.org/w/api.php"
OUT=Path("13kt-evidence")
OUT.mkdir(exist_ok=True)
session=requests.Session()
session.headers["User-Agent"]="TianwenAcademicHistoricalSourceAudit/13KT (public image metadata; GitHub Actions)"
response=session.get(API,params={"action":"query","prop":"imageinfo","titles":"File:"+NAME,"iiprop":"url|sha1|size|mime","format":"json"},timeout=45)
response.raise_for_status()
pages=response.json()["query"]["pages"]
value=next(iter(pages.values()))
assert "missing" not in value and value.get("imageinfo"),"official Commons original digital item missing"
info=value["imageinfo"][0]
assert info.get("mime")=="application/pdf" and info["size"]>1000000
url=info["url"]
assert url.startswith("https://upload.wikimedia.org/"),"unexpected host"
pdf=OUT/"harvard-mingshi-v11.pdf"
sha256=hashlib.sha256()
sha1=hashlib.sha1()
size=0
with session.get(url,timeout=120,stream=True) as download:
    download.raise_for_status()
    with pdf.open("wb") as f:
        for chunk in download.iter_content(chunk_size=1024*1024):
            if chunk:
                sha256.update(chunk)
                sha1.update(chunk)
                size+=len(chunk)
                f.write(chunk)
assert size==info["size"] and sha1.hexdigest()==info["sha1"],"Commons source digest/size mismatch"
with fitz.open(pdf) as doc:
    count=len(doc)
    assert 10<count<180,"unexpected physical scan page count"
    atlases=[]
    images_per_atlas=20
    for start in range(0,count,images_per_atlas):
        images=[]
        for p in range(start,min(count,start+images_per_atlas)):
            page=doc.load_page(p)
            pix=page.get_pixmap(matrix=fitz.Matrix(.23,.23),colorspace=fitz.csRGB,alpha=False)
            image=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
            image.thumbnail((360,300))
            images.append((p+1,image))
        canvas=Image.new("RGB",(5*380,4*330),"#f2f2f2")
        d=ImageDraw.Draw(canvas)
        for i,(pg,img) in enumerate(images):
            x=(i%5)*380;y=(i//5)*330
            d.text((x+6,y+2),str(pg),fill="#111111")
            canvas.paste(img,(x+6,y+22))
        name=f"source-pages-{start+1:03d}-{min(count,start+20):03d}.webp"
        dest=OUT/name
        canvas.save(dest,format="WEBP",quality=70,method=4)
        atlases.append({"file":name,"sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),"source_pages":[start+1,min(count,start+20)]})
    meta={"source":"Wikimedia Commons mirror of Harvard drs 428231199 明史 v.11.pdf","source_url":url,"commons_record_title":value["title"],"commons_imageinfo_sha1":info["sha1"],"source_pdf_sha256":sha256.hexdigest(),"source_pdf_bytes":size,"source_pdf_pages":count,"atlases":atlases,"review_grade":"DIGITAL_SOURCE_ACQUIRED_CONTACT_ATLAS_NOT_MANUAL_TARGET_GLYPH_COLLATION","physical_impression_authenticated":False,"target_folio_attested":False}
    (OUT/"evidence.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("TW13KT_META_JSON:"+json.dumps(meta,ensure_ascii=False))
    if atlases:
        blob=base64.b64encode((OUT/atlases[0]["file"]).read_bytes()).decode("ascii")
        print("TW13KT_ATLAS_B64_START")
        for offset in range(0,len(blob),256):
            print("TW13KT_ATLAS_B64:"+blob[offset:offset+256])
        print("TW13KT_ATLAS_B64_END")

# Second-pass, source-NATIVE manual target-page review; JPGs are not independent books.
with fitz.open(pdf) as doc:
    for one_based in (4,5,6,7):
        p=doc.load_page(one_based-1)
        pix=p.get_pixmap(matrix=fitz.Matrix(1.0,1.0),colorspace=fitz.csRGB,alpha=False)
        img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
        out=io.BytesIO()
        img.save(out,format="JPEG",quality=86,optimize=True)
        content=out.getvalue()
        (OUT/f"original-page-{one_based:03d}.jpg").write_bytes(content)
        print(f"TW13KT_DETAIL_PAGE_{one_based:03d}_META:"+json.dumps({"source_page":one_based,"dimensions":[pix.width,pix.height],"jpeg_sha256":hashlib.sha256(content).hexdigest(),"rgb_sha256":hashlib.sha256(pix.samples).hexdigest(),"render":"fitz Matrix(1,1) csRGB alpha=False","native_source_page_pdf_sha256":sha256.hexdigest()}))
        print(f"TW13KT_DETAIL_PAGE_{one_based:03d}_B64_START")
        string=base64.b64encode(content).decode("ascii")
        for k in range(0,len(string),256):
            print(f"TW13KT_DETAIL_PAGE_{one_based:03d}_B64:"+string[k:k+256])
        print(f"TW13KT_DETAIL_PAGE_{one_based:03d}_B64_END")
