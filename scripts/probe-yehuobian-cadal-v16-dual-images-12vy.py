#!/usr/bin/env python3
"""12VY: bounded public Commons DJVU acquisition, no OCR or historical glyph voting."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,tempfile,urllib.request
from pathlib import Path
from PIL import Image

SOURCES=[{"id":"CADAL02096915","url":"https://upload.wikimedia.org/wikipedia/commons/0/0f/CADAL02096915_%E9%87%8E%E7%8D%B2%E7%B7%A8%EF%BC%88%E5%8D%81%E5%85%AD%EF%BC%89.djvu","bytes":3495009,"sha1":"69d9b157cc060b5cd760c953fedcd5eae282d8e9","pages":[65,66,120,121,122],"expected_pages":135,"existing_sha256":"262edac806b90c984d5f0c4fce1bc150a974ebd574d847738a08a00cad39640d"},{"id":"CADAL02112262","url":"https://upload.wikimedia.org/wikipedia/commons/d/d9/CADAL02112262_%E9%87%8E%E7%8D%B2%E7%B7%A8%EF%BC%88%E5%8D%81%E5%85%AD%EF%BC%89.djvu","bytes":3413348,"sha1":"837c8df07b562d4a94950efc1a5b96b8a11b7447","pages":[64,65,66,115,116,117,118,119,120,121,122,123],"expected_pages":133,"existing_sha256":null}]
LIMIT=8_000_000
def checksum(path,algo):
    h=hashlib.new(algo)
    with Path(path).open("rb") as f:
        for part in iter(lambda:f.read(1024*1024),b""):h.update(part)
    return h.hexdigest()
def download(item,path):
    if not item["url"].startswith("https://upload.wikimedia.org/wikipedia/commons/"):
        raise ValueError("Unexpected untrusted source host")
    request=urllib.request.Request(item["url"],headers={"User-Agent":"TIANWEN-HISTORICAL-PROVENANCE-12VY/1.0 (public facsimile comparison)"})
    size=0
    with urllib.request.urlopen(request,timeout=55) as response,open(path,"wb") as f:
        for chunk in iter(lambda:response.read(1024*1024),b""):
            size+=len(chunk)
            if size>LIMIT:raise ValueError("source exceeds per-file download cap")
            f.write(chunk)
    if size!=item["bytes"] or checksum(path,"sha1")!=item["sha1"]:
        raise ValueError("source file bytes differ from Commons published checksum")
    if item["existing_sha256"] and checksum(path,"sha256")!=item["existing_sha256"]:
        raise ValueError("source SHA256 disagrees with prior 12QE original")
    return size
def pages_count(source):
    p=subprocess.run(["djvused",str(source),"-e","n"],capture_output=True,text=True,check=True)
    return int(p.stdout.strip())
def capture(outdir):
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    results=[]
    for item in SOURCES:
        p=outdir/f'{item["id"]}.djvu'
        download(item,p)
        count=pages_count(p)
        if count!=item["expected_pages"]:raise ValueError("DJVU page count differs from published Commons file")
        observed={"id":item["id"],"source_url":item["url"],"source_bytes":p.stat().st_size,
                  "source_sha1":checksum(p,"sha1"),"source_sha256":checksum(p,"sha256"),
                  "djvu_pages":count,"physical_copy_identity":"UNBOUND","impression_year":"UNBOUND",
                  "target_glyphs_human_verified":False,"independent_historical_witness":False,"images":[]}
        for n in item["pages"]:
            if n<1 or n>count:raise ValueError("page out of range")
            jpg=outdir/f'{item["id"]}-p{n:03}.jpg'
            with tempfile.TemporaryDirectory() as tmp:
                ppm=Path(tmp)/"page.ppm"
                subprocess.run(["ddjvu","-format=ppm",f"-page={n}",str(p),str(ppm)],check=True)
                with Image.open(ppm) as image:
                    image.convert("RGB").save(jpg,format="JPEG",quality=88,optimize=True)
            observed["images"].append({"source_page_number":n,"image_file":jpg.name,
                                       "sha256":checksum(jpg,"sha256"),"bytes":jpg.stat().st_size})
        results.append(observed)
    report={"schema":"TIANWEN-12VY-CADAL-DUAL-SOURCE-PAGE-ATLAS-R1",
      "status":"SOURCE_BYTES_AND_SELECTED_PAGE_JPEGS_CAPTURED_NO_MANUAL_GLYPH_ADJUDICATION",
      "data_sources":results,"new_ancient_target_glyph_votes":0,"printing_state_proven":False,
      "source_paper_copy_independence_proven":False,"ocr_used":False}
    (outdir/"atlas.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    return report
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output-dir",default="cadal-v16-evidence")
    args=parser.parse_args()
    report=capture(args.output_dir)
    print(json.dumps({"status":report["status"],"sources":[{"id":x["id"],"sha256":x["source_sha256"],"pages":x["djvu_pages"],"captured":len(x["images"])} for x in report["data_sources"]],"new_ancient_target_glyph_votes":0}))
if __name__=="__main__":main()
