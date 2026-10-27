#!/usr/bin/env python3
"""13HN bounded source-emitted NDL991069 IIIF preview acquisition; never auto-adjudicate ancient glyph."""
import json, hashlib, urllib.request, urllib.parse
from pathlib import Path
URL = "https://dl.ndl.go.jp/api/iiif/991069/manifest.json"
DEST = Path("artifacts/13hn-ndl991069-v52")
def label(v):
    if isinstance(v, str): return v
    if isinstance(v, list): return "/".join(label(t) for t in v)
    if isinstance(v, dict): return "/".join(label(t) for t in v.values())
    return ""
def canvases(data):
    if (data.get("@id") or data.get("id")) != URL: raise ValueError("foreign manifest")
    seq = data.get("sequences") or []
    cs = seq[0].get("canvases", []) if seq else data.get("items", [])
    ids = [c.get("@id") or c.get("id") for c in cs]
    if not 1 < len(ids) < 3000 or not all(ids) or len(ids) != len(set(ids)): raise ValueError("invalid canvases")
    return cs, ids
def toc_scope(data, ids):
    idx = {v:i+1 for i,v in enumerate(ids)}
    ranges = []
    def walk(items):
        for r in items or []:
            if not isinstance(r,dict): continue
            poss = [idx[c] for c in r.get("canvases", []) if isinstance(c,str) and c in idx]
            for t in (r.get("startCanvas"), r.get("start")):
                if isinstance(t,str) and t in idx: poss.append(idx[t])
            if poss: ranges.append((label(r.get("label", "")),min(poss)))
            walk(r.get("ranges",[]))
            walk(r.get("items",[]))
    walk(data.get("structures", []))
    target = [p for s,p in ranges if "高麗史五十二" in s or "高麗史卷五十二" in s]
    if len(target)!=1: raise ValueError("source TOC target not unique")
    start = target[0]
    later = sorted(p for _,p in ranges if p>start)
    if not later: raise ValueError("no source TOC next-volume boundary")
    end = later[0]
    if end>len(ids)+1: raise ValueError("invalid end")
    return start,end
def image_service(c):
    ims=c.get("images", [])
    obj=ims[0].get("resource", {}) if ims else {}
    if not obj:
        pages=c.get("items", [])
        if pages and pages[0].get("items"): obj=pages[0]["items"][0].get("body", {})
    serv=obj.get("service",{})
    if isinstance(serv,list):serv=serv[0] if serv else {}
    url=serv.get("@id") or serv.get("id") or ""
    split=urllib.parse.urlsplit(url)
    if split.scheme!="https" or split.netloc!="dl.ndl.go.jp" or not split.path.startswith("/api/iiif/991069/"):
        raise ValueError("source image service not bound to NDL PID")
    return url.rstrip("/")
def fetch(url,limit):
    req=urllib.request.Request(url,headers={"User-Agent":"TianwenPublicIIIFSourceProbe/1.0","Accept":"application/json,image/jpeg"})
    with urllib.request.urlopen(req,timeout=25) as r:
        b=r.read(limit+1)
        if len(b)>limit: raise ValueError("oversized")
        return b,r.status,r.headers.get("Content-Type", "")
def main():
    DEST.mkdir(parents=True,exist_ok=True)
    result={"schema":"TIANWEN-13HN-NDL991069-V52-ATLAS-PROBE-R1","url":URL,"results":[],"no_ocr":True}
    try:
        b,code,_=fetch(URL,12000000)
        data=json.loads(b)
        cs,ids=canvases(data)
        start,end=toc_scope(data,ids)
        result.update(status="SOURCE_TOC_BOUND",http_status=code,manifest_sha256=hashlib.sha256(b).hexdigest(),
                      source_canvas_count=len(ids),v52_first_canvas=start,next_volume_canvas=end,
                      source_v52_canvas_count=end-start)
        for i in range(start,min(end,start+20)):
            info={"canvas":i,"canvas_id":ids[i-1]}
            try:
                service=image_service(cs[i-1])
                url=service+"/full/1600,/0/default.jpg"
                body,http,mime=fetch(url,12000000)
                if not mime.lower().startswith("image/"): raise ValueError("non-image MIME "+mime)
                fname="canvas-%03d.jpg"%i
                (DEST/fname).write_bytes(body)
                info.update(status="PREVIEW_SAVED",url=url,http_status=http,sha256=hashlib.sha256(body).hexdigest(),
                            bytes=len(body),artifact_file=fname)
            except Exception as ex:
                info.update(status="IMAGE_ACCESS_BOUNDARY",error_type=type(ex).__name__,error=str(ex)[:180])
            result["results"].append(info)
    except Exception as ex:
        result.update(status="MANIFEST_OR_TOC_BOUNDARY",error_type=type(ex).__name__,error=str(ex)[:220])
    result["saved_count"]=sum(r["status"]=="PREVIEW_SAVED" for r in result["results"])
    output=DEST/"report.json";output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:result.get(k) for k in ("status","manifest_sha256","v52_first_canvas","next_volume_canvas","source_v52_canvas_count","saved_count","error_type")},ensure_ascii=False))
if __name__=="__main__": main()
