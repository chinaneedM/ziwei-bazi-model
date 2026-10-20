#!/usr/bin/env python3
"""13AS bounded original source-native JP2 sampling from firstparty NAJ viewer HTML."""
import hashlib, json, os, re, urllib.parse, urllib.request, urllib.error
from pathlib import Path
OUT=Path(os.environ.get("TIANWEN_13AS_OUT","najda-goryeosa-13as-evidence"))
VIEWER="https://www.digital.archives.go.jp/img/en/4898854"
MAX_HTML=200000
MAX_MANIFEST=3000000
MAX_IMAGE=12000000
MAX_DOWNLOAD_IMAGES=3

def extracted_image_metadata(html):
    marker="var najContentList = "
    at=html.find(marker)
    if at<0:return []
    raw=html[at+len(marker):].lstrip()
    rows,_=json.JSONDecoder().raw_decode(raw)
    if not isinstance(rows,list):return []
    result=[]
    for row in rows:
        if not isinstance(row,dict):continue
        path=row.get("path")
        if not isinstance(path,str):continue
        # No index construction: only use exact firstparty source-emitted paths.
        if not re.fullmatch(r"/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2",path):continue
        result.append({"path":path,"contentName":row.get("contentName"),"width":row.get("source",{}).get("width"),"height":row.get("source",{}).get("height")})
    return result

def emitted_manifest_link(html):
    hits=re.findall(r'href="(https://www[.]digital[.]archives[.]go[.]jp/api/iiif/4898854/manifest[.]json)"',html)
    return hits[0] if hits else None

def manifest_full_jpeg_urls(raw):
    if not raw:return []
    doc=json.loads(raw)
    seq=doc.get("sequences",[])
    if len(seq)!=1:return []
    urls=[]
    for canvas in seq[0].get("canvases",[]):
        try:url=canvas["images"][0]["resource"]["@id"]
        except (IndexError,KeyError,TypeError):continue
        p=urllib.parse.urlparse(url)
        if p.scheme=="https" and p.netloc=="www.digital.archives.go.jp" and re.fullmatch(r"/api/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2/full/max/0/native[.]jpg",p.path):urls.append(url)
    return urls

def fetch_bounded(url,name,cap,content):
    result={"url":url,"http":None,"status":"UNREAD","sha256":None,"bytes":0,"format":"UNDETERMINED"}
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!="https" or parsed.netloc!="www.digital.archives.go.jp":raise ValueError("Host not allowlisted")
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Tianwen-Scholarly-Original-Page-Replay/13AS (bounded source emitted paths)","Accept":"*/*"})
        with urllib.request.urlopen(req,timeout=45) as f:
            result["http"]=f.status
            length=f.headers.get("Content-Length")
            if length and int(length)>cap:result["status"]="HEADER_SIZE_LIMIT";return result,None
            b=f.read(cap+1)
            if len(b)>cap:result["status"]="STREAM_SIZE_LIMIT";return result,None
            result["sha256"]=hashlib.sha256(b).hexdigest()
            result["bytes"]=len(b);result["status"]="BYTE_CAPTURED"
            if b.startswith(bytes.fromhex("0000000c6a5020200d0a870a")) or b.startswith(bytes.fromhex("ff4f")):result["format"]="JPEG2000_MAGIC"
            elif b.startswith(bytes.fromhex("ffd8ff")):result["format"]="JPEG_MAGIC"
            elif b.lstrip().startswith(b"{"):result["format"]="JSON"
            elif b.lstrip().startswith(b"<"):result["format"]="HTML_OR_XML"
            OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_bytes(b)
            return result,b
    except urllib.error.HTTPError as e:result["http"]=e.code;result["status"]="HTTP_ERROR"
    except Exception as e:result["status"]="TRANSPORT_ERROR";result["error"]=type(e).__name__+":"+str(e)[:120]
    return result,None

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    page,bytes_=fetch_bounded(VIEWER,"official-viewer.html",MAX_HTML,False)
    html=bytes_.decode("utf-8","replace") if bytes_ else ""
    entries=extracted_image_metadata(html) if html else []
    manifest=emitted_manifest_link(html) if html else None
    mr=None
    raw_manifest=None
    if manifest:mr,raw_manifest=fetch_bounded(manifest,"official-IIIF-manifest.json",MAX_MANIFEST,False)
    resource_urls=manifest_full_jpeg_urls(raw_manifest)
    selections=[]
    for i in sorted(set([0,1,len(resource_urls)-1]))[:MAX_DOWNLOAD_IMAGES] if resource_urls else []:
        url=resource_urls[i]
        r,_=fetch_bounded(url,"source-full-leaf-%02d.jpg"%(i+1),MAX_IMAGE,True)
        r.update({"manifest_ordinal":i+1,"exact_manifest_resource_url":url})
        selections.append(r)
    out={"schema":"TIANWEN-13AS-NAJDA-NATIVE-JP2-BOUNDED-PROBE-R1","viewer":page,"source_emitted_canvas_count":len(entries),"manifest_from_provider_html":manifest,"manifest_result":mr,"manifest_full_jpeg_count":len(resource_urls),"sampled_source_native_originals":selections,"human_glyph_collation_done":False,"work52_presence":"UNVERIFIED","D16_numeric_vote":0,"single_physical_copy_witness_max":1,"no_computed_paths":True}
    (OUT/"result.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False))
if __name__=="__main__":main()
