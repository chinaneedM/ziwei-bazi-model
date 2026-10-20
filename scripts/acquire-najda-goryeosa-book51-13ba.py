#!/usr/bin/env python3
"""13BA source-native full 36-image public original atlas for neighboring NAJ Goryeosa physical book51."""
import hashlib,json,os,re,urllib.parse,urllib.request
from pathlib import Path
MANIFEST="https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json"
EXPECTED_SHA="3f38f52860bd06ca7f4b89cec65a32b8529fcb547ac098548120e8071fe370a1"
PART=int(os.environ.get("NAJ_13BA_PART","1"))
OUT=Path(f"najda-goryeosa-13ba-part{PART}")
MAX_MANIFEST=1000000;MAX_IMAGE=12000000;MAX_TOTAL=80000000
def part_indices(part):
    if part not in (1,2,3,4):raise ValueError("out-of-scope part")
    return list(range((part-1)*9,part*9))
def provider_urls(raw):
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:raise ValueError("manifest original SHA drift")
    j=json.loads(raw); seq=j.get("sequences",[])
    if len(seq)!=1 or len(seq[0].get("canvases",[]))!=36:raise ValueError("unexpected original canvas count")
    urls=[]
    for c in seq[0]["canvases"]:
        im=c.get("images",[])
        if len(im)!=1:raise ValueError("unexpected annotations")
        u=im[0].get("resource",{}).get("@id","")
        p=urllib.parse.urlsplit(u)
        if p.scheme!="https" or p.netloc!="www.digital.archives.go.jp" or p.query or p.fragment or not re.fullmatch(r"/api/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2/full/max/0/native[.]jpg",p.path):raise ValueError("untrusted page URL")
        urls.append(u)
    if len(set(urls))!=36:raise ValueError("not 36 distinct provider originals")
    return urls
def get(url,limit):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="www.digital.archives.go.jp":raise ValueError("unsupported host")
    req=urllib.request.Request(url,headers={"User-Agent":"Tianwen-NAJ-original-leaf-source-replay-13BA","Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=55) as r:
        if r.status!=200:raise ValueError("unexpected HTTP")
        cl=r.headers.get("Content-Length")
        if cl and int(cl)>limit:raise ValueError("content-length cap")
        raw=r.read(limit+1)
    if len(raw)>limit:raise ValueError("response cap")
    return raw
def main():
    OUT.mkdir(exist_ok=True);result={"schema":"TIANWEN-13BA-GORYEOSA-51-ALL36-PROVIDER-RENDERING-BYTE-HASH-R1","source_manifest":MANIFEST,"part":PART,"rows":[],"error":None,"no_OCR":True,"same_physical_copy":True,"solar_D16_unread":True}
    try:
        raw=get(MANIFEST,MAX_MANIFEST);urls=provider_urls(raw);(OUT/"official-book51-manifest.json").write_bytes(raw);result["manifest_sha256"]=hashlib.sha256(raw).hexdigest()
        total=0
        for i in part_indices(PART):
            d={"ordinal":i+1,"exact_source_url":urls[i]}
            try:
                b=get(urls[i],MAX_IMAGE);total+=len(b)
                if total>MAX_TOTAL:raise ValueError("part total cap")
                if not b.startswith(bytes.fromhex("ffd8ff")):raise ValueError("not image/jpeg")
                name=f"book51-full-leaf-{i+1:03}.jpg";(OUT/name).write_bytes(b)
                d.update({"status":"SHA_VERIFIED_JPEG","sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"file":name})
            except Exception as e:d.update({"status":"FAILED","error":type(e).__name__+":"+str(e)[:150]})
            result["rows"].append(d)
    except Exception as e:result["error"]=type(e).__name__+":"+str(e)[:150]
    (OUT/"result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"part":PART,"count":len(result["rows"]),"ok":sum(x.get("status")=="SHA_VERIFIED_JPEG" for x in result["rows"]),"error":result["error"]}))
    if result["error"] or len(result["rows"])!=9 or any(x["status"]!="SHA_VERIFIED_JPEG" for x in result["rows"]):raise SystemExit(1)
if __name__=="__main__":main()
