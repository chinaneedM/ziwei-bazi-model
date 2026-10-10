#!/usr/bin/env python3
"""Strictly bounded, no-OCR CADAL physical-fascicle -> source-volume title crosswalk."""
import hashlib
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"cadal-fascicle-crosswalk-12qe"
OUT.mkdir(parents=True,exist_ok=True)
SPEC=[
 (13,"十四","f75e52bd732d1e27458833a98a3c4607498136ae",3516033,139),
 (14,"十五","fed798a34b70ab7d41d43d3e4f5d09c485c0ba2c",2221825,87),
 (15,"十六","69d9b157cc060b5cd760c953fedcd5eae282d8e9",3495009,135),
 (16,"十七","ca05d8f8c0e71f68c2def08c9efa6c0db008f129",3589777,141),
 (17,"十八","14d96919042adcd33b6be310c250392561f95785",3549515,139)]
def url_for(index,numeral):
    name=f"CADAL020969{index}_野獲編（{numeral}）.djvu"
    md5=hashlib.md5(name.encode("utf-8")).hexdigest()
    return f"https://upload.wikimedia.org/wikipedia/commons/{md5[0]}/{md5[:2]}/{urllib.parse.quote(name)}"
def main():
    result={"schema":"YEHUOBIAN-CADAL-FASCICLE-CROSSWALK-12QE-R1","method":"FIVE_EXACT_COMMONS_SHA1_BOUND_FASCICLES_PAGES_2_TO_4_RENDERED_NO_OCR","status":"IN_PROGRESS","ocr_performed":False,"physical_edition_date_bound":False,"units":[]}
    try:
        for index,numeral,sha1,size,pages in SPEC:
            src=url_for(index,numeral)
            entry={"cadal_id":f"020969{index}","physical_fascicle_label":numeral,"source_url":src,"expected_sha1":sha1,"expected_bytes":size,"expected_pages":pages,"status":"STARTED","sample_images":[]}
            result["units"].append(entry)
            try:
                req=urllib.request.Request(src,headers={"User-Agent":"TianwenHistoricalResearch/1.0 (public edition collation)"})
                with urllib.request.urlopen(req,timeout=45) as resp:
                    raw=resp.read(4_500_000)
                entry["actual_sha1"]=hashlib.sha1(raw).hexdigest()
                entry["actual_bytes"]=len(raw)
                if entry["actual_sha1"]!=sha1 or len(raw)!=size:
                    entry["status"]="IDENTITY_MISMATCH_FAIL_CLOSED"
                    continue
                source=OUT/f"cadal020969{index}.djvu"
                source.write_bytes(raw)
                actual=int(subprocess.check_output(["djvused",str(source),"-e","n"],text=True,timeout=30).strip())
                entry["actual_pages"]=actual
                if actual!=pages:
                    entry["status"]="PAGE_COUNT_MISMATCH_FAIL_CLOSED"
                    continue
                for p in (2,3,4):
                    ppm=OUT/"tmp.ppm"
                    subprocess.run(["ddjvu","-format=ppm",f"-page={p}","-size=1150x1700",str(source),str(ppm)],check=True,timeout=40)
                    with Image.open(ppm) as im:
                        target=OUT/f"cadal020969{index}-p{p:03d}.jpg"
                        im.convert("RGB").save(target,"JPEG",quality=90,optimize=True)
                    ppm.unlink(missing_ok=True)
                    entry["sample_images"].append({"page":p,"path":target.name,"sha256":hashlib.sha256(target.read_bytes()).hexdigest()})
                entry["status"]="SAMPLE_CAPTURED_NOT_TRANSCRIBED"
                source.unlink(missing_ok=True)
            except Exception as err:
                entry["status"]="ACCESS_OR_EXTRACTION_BOUNDARY"
                entry["error"]=type(err).__name__+": "+str(err)[:400]
        result["status"]="COMPLETED_WITH_SOURCE_SCOPED_RESULTS"
    finally:
        (OUT/"crosswalk-receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"units":[{"id":x["cadal_id"],"status":x["status"]} for x in result["units"]]}))
    if any(x["status"].endswith("FAIL_CLOSED") for x in result["units"]):
        raise SystemExit(1)
if __name__=="__main__":
    main()
