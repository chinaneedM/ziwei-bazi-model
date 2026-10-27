#!/usr/bin/env python3
"""13AY: bounded 32-canvas original-source IIIF image acquisition; no OCR or glyph inference."""
import hashlib, json, os, re, urllib.error, urllib.parse, urllib.request
from pathlib import Path
PART=int(os.environ.get("NAJ_13AY_PART","1"))
OUT=Path(os.environ.get("NAJ_13AY_OUT",f"najda-goryeosa-13ay-part{PART}"))
MANIFEST="https://www.digital.archives.go.jp/api/iiif/4898854/manifest.json"
MAX_MANIFEST=1000000
MAX_IMAGE=12000000
MAX_PART_BYTES=64000000
EXPECTED_CANVASES=32
def parse_manifest(raw):
    d=json.loads(raw)
    seq=d.get("sequences",[])
    if len(seq)!=1 or len(seq[0].get("canvases",[]))!=EXPECTED_CANVASES: raise ValueError("unexpected manifest canvas identity/count")
    urls=[]
    for canvas in seq[0]["canvases"]:
        im=canvas.get("images",[])
        if len(im)!=1: raise ValueError("unexpected images per canvas")
        u=im[0].get("resource",{}).get("@id","")
        p=urllib.parse.urlsplit(u)
        if (p.scheme!="https" or p.netloc!="www.digital.archives.go.jp" or p.query or p.fragment or not re.fullmatch(r"/api/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2/full/max/0/native[.]jpg",p.path)): raise ValueError("non firstparty source-emitted full JPEG URL")
        urls.append(u)
    if len(set(urls))!=32: raise ValueError("duplicate image resources")
    return urls
def part_indices(part):
    if part not in (1,2,3,4): raise ValueError("part must be 1..4")
    return list(range((part-1)*8,part*8))
def bounded_fetch(url,limit):
    req=urllib.request.Request(url,headers={"User-Agent":"Tianwen-historical-folio-13AY (public IIIF provider-listed images)","Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=50) as response:
        if response.status!=200: raise ValueError("unexpected HTTP")
        h=response.headers.get("Content-Length")
        if h and int(h)>limit: raise ValueError("content length exceeds cap")
        b=response.read(limit+1)
    if len(b)>limit: raise ValueError("byte cap exceeded")
    return b
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results=[]; manifest_sha=None; fatal=None
    try:
        raw=bounded_fetch(MANIFEST,MAX_MANIFEST)
        manifest_sha=hashlib.sha256(raw).hexdigest()
        (OUT/"manifest.json").write_bytes(raw)
        urls=parse_manifest(raw)
        total=0
        for i in part_indices(PART):
            u=urls[i]; row={"ordinal":i+1,"source_url":u}
            try:
                b=bounded_fetch(u,MAX_IMAGE)
                if not b.startswith(bytes.fromhex("ffd8ff")): raise ValueError("not JPEG magic")
                total+=len(b)
                if total>MAX_PART_BYTES: raise ValueError("total payload cap")
                name=f"source-full-leaf-{i+1:02d}.jpg"
                (OUT/name).write_bytes(b)
                row.update({"status":"JPEG_VERIFIED","bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"file":name})
            except Exception as e:row.update({"status":"FAILED","error":type(e).__name__+":"+str(e)[:160]})
            results.append(row)
    except Exception as e:fatal=type(e).__name__+":"+str(e)[:160]
    record={"schema":"TIANWEN-13AY-NAJDA-ORIGINAL-32-CANVAS-PART-BY-PART-ACQUISITION-R1","part":PART,"provider_item":"https://www.digital.archives.go.jp/img/en/4898854","manifest":MANIFEST,"manifest_sha256":manifest_sha,"expected_total_canvases":32,"original_source_only":True,"original_scans_are_jpeg_renditions_not_jp2_master":True,"no_ocr":True,"no_negative_glyph_claim":True,"no_numeric_votes":True,"results":results,"fatal":fatal}
    (OUT/"result.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"part":PART,"manifest_sha256":manifest_sha,"captured":sum(x.get("status")=="JPEG_VERIFIED" for x in results),"total":len(results),"fatal":fatal}))
    if fatal or len(results)!=8 or any(x["status"]!="JPEG_VERIFIED" for x in results):raise SystemExit(1)
if __name__=="__main__":main()
