#!/usr/bin/env python3
"""13AZ: source-emitted adjacent NAJ Goryeosa physical book51 image-boundary probe."""
import hashlib,json,os,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path
OUT=Path("najda-goryeosa-13az-evidence")
INDEX="https://www.digital.archives.go.jp/search?fond=1073275&lang=en&page=1"
ITEM="https://www.digital.archives.go.jp/item/en/4898853"
VIEWER="https://www.digital.archives.go.jp/img/en/4898853"
MAX_HTML=1100000; MAX_MANIFEST=1200000; MAX_IMAGE=12000000; MAX_IMAGES=9
def provider_bound_book51(html):
    if 'id="row-52-title"' not in html or 'id="row-53-title"' not in html:return False
    frag=html.split('id="row-52-title"',1)[1].split('id="row-53-title"',1)[0]
    return "高麗史５１" in frag and ('href="'+ITEM+'"') in frag and ('href="'+VIEWER+'"') in frag
def emitted_manifest(html):
    matches=re.findall(r'href="(https://www[.]digital[.]archives[.]go[.]jp/api/iiif/4898853/manifest[.]json)"',html)
    return matches[0] if matches else None
def manifest_urls(raw):
    x=json.loads(raw);seq=x.get("sequences",[])
    if len(seq)!=1:raise ValueError("expected one source sequence")
    canvases=seq[0].get("canvases",[])
    if not canvases or len(canvases)>400:raise ValueError("unexpected page count")
    urls=[]
    for canvas in canvases:
        images=canvas.get("images",[])
        if len(images)!=1:raise ValueError("non-one-image canvas")
        u=images[0].get("resource",{}).get("@id","")
        p=urllib.parse.urlsplit(u)
        if p.scheme!="https" or p.netloc!="www.digital.archives.go.jp" or p.query or p.fragment or not re.fullmatch(r"/api/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2/full/max/0/native[.]jpg",p.path):raise ValueError("untrusted resource URL")
        urls.append(u)
    if len(set(urls))!=len(urls):raise ValueError("duplicate URLs")
    return urls
def bounded_fetch(url,cap):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="www.digital.archives.go.jp":raise ValueError("invalid provider")
    request=urllib.request.Request(url,headers={"User-Agent":"Tianwen-NAJ-Goryeosa-source-13AZ (public exact object only)","Accept":"*/*"})
    with urllib.request.urlopen(request,timeout=55) as response:
        if response.status!=200:raise ValueError("unexpected HTTP")
        cl=response.headers.get("Content-Length")
        if cl and int(cl)>cap:raise ValueError("content-length cap")
        b=response.read(cap+1)
    if len(b)>cap:raise ValueError("stream cap")
    return b
def main():
    OUT.mkdir(exist_ok=True)
    rec={"schema":"TIANWEN-13AZ-NAJDA-PHYSICAL-BOOK51-PROVIDER-EMITTED-ORIGINAL-SAMPLE-R1","catalog_url":INDEX,"item_url":ITEM,"viewer_url":VIEWER,"selected":[],"no_ocr":True,"no_non_source_paths":True,"numeric_votes":0,"fatal":None}
    try:
        b=bounded_fetch(INDEX,MAX_HTML);rec["index_sha256"]=hashlib.sha256(b).hexdigest()
        if not provider_bound_book51(b.decode("utf-8","replace")):raise ValueError("no exact book51 original index paired links")
        viewer=bounded_fetch(VIEWER,MAX_HTML); rec["viewer_sha256"]=hashlib.sha256(viewer).hexdigest()
        (OUT/"official-book51-viewer.html").write_bytes(viewer)
        u=emitted_manifest(viewer.decode("utf-8","replace"))
        if not u:raise ValueError("viewer has no exact source-emitted manifest")
        raw=bounded_fetch(u,MAX_MANIFEST);rec["manifest_sha256"]=hashlib.sha256(raw).hexdigest();rec["manifest_url"]=u
        (OUT/"official-book51-manifest.json").write_bytes(raw)
        urls=manifest_urls(raw); rec["source_canvas_count"]=len(urls)
        picks=sorted(set([0]+list(range(max(0,len(urls)-8),len(urls)))))
        if len(picks)>MAX_IMAGES:raise ValueError("sample cap")
        for i in picks:
            o={"ordinal":i+1,"url":urls[i]}
            try:
                image=bounded_fetch(urls[i],MAX_IMAGE)
                if not image.startswith(bytes.fromhex("ffd8ff")):raise ValueError("non-JPEG response")
                o.update({"status":"JPEG_VERIFIED","sha256":hashlib.sha256(image).hexdigest(),"bytes":len(image)})
                (OUT/f"book51-source-leaf-{i+1:03d}.jpg").write_bytes(image)
            except Exception as e:o.update({"status":"FAILED","error":type(e).__name__+":"+str(e)[:150]})
            rec["selected"].append(o)
    except Exception as e:rec["fatal"]=type(e).__name__+":"+str(e)[:200]
    (OUT/"result.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"fatal":rec["fatal"],"canvases":rec.get("source_canvas_count"),"sample_ok":sum(x.get("status")=="JPEG_VERIFIED" for x in rec["selected"]),"selected":len(rec["selected"])}))
    if rec["fatal"] or not rec["selected"] or any(x["status"]!="JPEG_VERIFIED" for x in rec["selected"]):raise SystemExit(1)
if __name__=="__main__":main()
