#!/usr/bin/env python3
"""Bounded public historical original-page reproduction, no OCR."""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"cadal-vol20-source-12qe"
OUT.mkdir(parents=True,exist_ok=True)
URL="https://upload.wikimedia.org/wikipedia/commons/0/0f/CADAL02096915_%E9%87%8E%E7%8D%B2%E7%B7%A8%EF%BC%88%E5%8D%81%E5%85%AD%EF%BC%89.djvu"
SHA1="69d9b157cc060b5cd760c953fedcd5eae282d8e9"
BYTES=3495009
PAGES=135
def digest(x):
    return hashlib.sha256(x).hexdigest()
def main():
    result={"schema":"YEHUOBIAN-CADAL02096915-BOUND-VOL19-20-ATLAS-12QE-R1",
     "source_url":URL,"physical_fascicle_number":16,"first_source_volume_heading_from_public_thumb":"卷十九目錄","next_fascicle_first_volume":"卷二十一目錄",
     "expected_sha1":SHA1,"expected_bytes":BYTES,"expected_pages":PAGES,
     "ocr_used":False,"edition_impression_date_bound":False,
     "manually_verified_target_glyph":False,"status":"STARTED","images":[],"contacts":[]}
    try:
        request=urllib.request.Request(URL,headers={"User-Agent":"TianwenHistoricalResearch/1.0 (public edition collation; GitHub Actions)"})
        with urllib.request.urlopen(request,timeout=50) as h:
            data=h.read(5_000_000)
        result["observed_sha1"]=hashlib.sha1(data).hexdigest()
        result["observed_sha256"]=digest(data)
        result["observed_bytes"]=len(data)
        if result["observed_sha1"]!=SHA1 or len(data)!=BYTES:
            raise RuntimeError("SOURCE_IDENTITY_MISMATCH")
        file=OUT/"source.djvu"
        file.write_bytes(data)
        pages=int(subprocess.check_output(["djvused",str(file),"-e","n"],text=True,timeout=30).strip())
        result["observed_pages"]=pages
        if pages!=PAGES:
            raise RuntimeError("SOURCE_PAGE_COUNT_MISMATCH")
        d=OUT/"pages";d.mkdir(exist_ok=True)
        for p in range(1,pages+1):
            tmp=OUT/"tmp.ppm"
            subprocess.run(["ddjvu","-format=ppm",f"-page={p}","-size=950x1400",str(file),str(tmp)],check=True,timeout=45)
            with Image.open(tmp) as im:
                jpg=d/f"p{p:03d}.jpg"
                im.convert("RGB").save(jpg,"JPEG",quality=88,optimize=True)
            tmp.unlink(missing_ok=True)
            result["images"].append({"page":p,"sha256":digest(jpg.read_bytes()),"bytes":jpg.stat().st_size})
        d2=OUT/"contacts";d2.mkdir(exist_ok=True)
        for start in range(1,pages+1,8):
            canvas=Image.new("RGB",(2400,1500),"white")
            draw=ImageDraw.Draw(canvas)
            for i,p in enumerate(range(start,min(start+8,pages+1))):
                with Image.open(d/f"p{p:03d}.jpg") as im: pic=im.copy()
                pic.thumbnail((550,650))
                x=(i%4)*600+(600-pic.width)//2;y=(i//4)*750+35
                canvas.paste(pic,(x,y))
                draw.text(((i%4)*600+14,(i//4)*750+8),f"p{p:03d}",fill="black")
            jpg=d2/f"sheet-{start:03d}.jpg";canvas.save(jpg,"JPEG",quality=89)
            result["contacts"].append({"start":start,"sha256":digest(jpg.read_bytes())})
        result["status"]="CAPTURED_NOT_MANUALLY_COLLATED"
    except Exception as err:
        result["status"]="ACCESS_OR_EXTRACT_BOUNDARY"
        result["error"]=type(err).__name__+": "+str(err)[:500]
        if "MISMATCH" in str(err):result["status"]="SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED"
    finally:
        (OUT/"status.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"pages":len(result["images"]),"error":result.get("error")}))
    if result["status"]=="SOURCE_IDENTITY_MISMATCH_FAIL_CLOSED":raise SystemExit(1)
if __name__=="__main__":main()
