#!/usr/bin/env python3
"""Bounded public-source DJVU image inventory; never OCR or assume edition."""
from __future__ import annotations
import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"yehuobian-cadal-12qe"
OUT.mkdir(parents=True,exist_ok=True)
SOURCE="https://upload.wikimedia.org/wikipedia/commons/8/84/CADAL02096919_%E9%87%8E%E7%8D%B2%E7%B7%A8%EF%BC%88%E4%BA%8C%E5%8D%81%EF%BC%89.djvu"
EXPECTED_SHA1="da6bd71dc31801b70572eb4aff16792f93234096"
EXPECTED_BYTES=1936886
EXPECTED_PAGES=77

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    receipt={
       "schema":"YEHUOBIAN-CADAL02096919-BOUNDED-IMAGE-ATLAS-12QE-R1",
       "source_url":SOURCE, "source_identity":"Commons CADAL02096919 野獲編（二十）",
       "expected_sha1":EXPECTED_SHA1, "expected_bytes":EXPECTED_BYTES,
       "expected_pages":EXPECTED_PAGES,
       "ocr_performed":False,"target_passage_transcribed":False,
       "physical_edition_date_bound":False,
       "status":"STARTED","rendered_pages":[],"contact_sheets":[]}
    try:
        request=urllib.request.Request(SOURCE,headers={"User-Agent":"TianwenHistoricalResearch/1.0 (public edition collation)"})
        with urllib.request.urlopen(request,timeout=45) as stream:
            data=stream.read(4_000_000)
        receipt["observed_bytes"]=len(data)
        receipt["observed_sha1"]=hashlib.sha1(data).hexdigest()
        receipt["observed_sha256"]=sha256(data)
        if len(data)!=EXPECTED_BYTES or receipt["observed_sha1"]!=EXPECTED_SHA1:
            raise RuntimeError("SOURCE_CONTENT_IDENTITY_MISMATCH")
        input_file=OUT/"source.djvu"
        input_file.write_bytes(data)
        n=int(subprocess.check_output(["djvused",str(input_file),"-e","n"],text=True,timeout=30).strip())
        receipt["observed_pages"]=n
        if n!=EXPECTED_PAGES:
            raise RuntimeError("SOURCE_PAGE_COUNT_MISMATCH")
        folder=OUT/"pages"
        folder.mkdir(exist_ok=True)
        for p in range(1,n+1):
            tmp=OUT/"tmp.ppm"
            subprocess.run(["ddjvu","-format=ppm",f"-page={p}","-size=850x1200",str(input_file),str(tmp)],check=True,timeout=35)
            with Image.open(tmp) as im:
                jpg=folder/f"cadal02096919-p{p:03d}.jpg"
                im.convert("RGB").save(jpg,"JPEG",quality=86,optimize=True)
            tmp.unlink(missing_ok=True)
            receipt["rendered_pages"].append({"djvu_page":p,"path":str(jpg.relative_to(OUT)),"sha256":sha256(jpg.read_bytes()),"bytes":jpg.stat().st_size})
        contacts=OUT/"contacts"
        contacts.mkdir(exist_ok=True)
        for start in range(1,n+1,8):
            canvas=Image.new("RGB",(2400,1500),"white")
            draw=ImageDraw.Draw(canvas)
            for idx,p in enumerate(range(start,min(start+8,n+1))):
                with Image.open(folder/f"cadal02096919-p{p:03d}.jpg") as original:
                    img=original.copy()
                img.thumbnail((550,650))
                x=(idx%4)*600+(600-img.width)//2
                y=(idx//4)*750+38
                canvas.paste(img,(x,y))
                draw.text(((idx%4)*600+20,(idx//4)*750+10),f"DJVU p{p:03d}",fill="black")
            dst=contacts/f"contact-{start:03d}.jpg"
            canvas.save(dst,"JPEG",quality=88)
            receipt["contact_sheets"].append({"path":str(dst.relative_to(OUT)),"sha256":sha256(dst.read_bytes())})
        receipt["status"]="CAPTURED_NOT_MANUALLY_COLLATED"
    except Exception as err:
        receipt["status"]="ACCESS_OR_EXTRACTION_BOUNDARY"
        receipt["error"]=type(err).__name__+": "+str(err)[:500]
        if "MISMATCH" in str(err):
            receipt["status"]="SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED"
    finally:
        (OUT/"probe-status.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":receipt["status"],"rendered_pages":len(receipt["rendered_pages"]),"expected_pages":EXPECTED_PAGES,"error":receipt.get("error")},ensure_ascii=False))
    if receipt["status"]=="SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED":
        raise SystemExit(1)

if __name__=="__main__":
    main()
