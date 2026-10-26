#!/usr/bin/env python3
"""13HM NDL first-party IIIF manifest scope probe. No OCR, no page guesses, no images fetched."""
import argparse, hashlib, json, urllib.request
from pathlib import Path
URL="https://dl.ndl.go.jp/api/iiif/991069/manifest.json"
def lab(x):
    if isinstance(x,str): return x
    if isinstance(x,list): return " / ".join(lab(v) for v in x)
    if isinstance(x,dict): return " / ".join(lab(v) for v in x.values())
    return ""
def analyze(payload):
    if not isinstance(payload,dict): raise ValueError("manifest must be object")
    ident=payload.get("id") or payload.get("@id") or ""
    if "991069" not in ident or "manifest" not in ident: raise ValueError("manifest identity not NDL991069")
    seq=payload.get("sequences",[])
    canvases=seq[0].get("canvases",[]) if seq else payload.get("items",[])
    if not isinstance(canvases,list) or not 1<=len(canvases)<=3000: raise ValueError("no bounded IIIF canvases")
    ids=[x.get("id") or x.get("@id") for x in canvases]
    if not all(isinstance(i,str) and i for i in ids) or len(set(ids))!=len(ids): raise ValueError("missing or duplicated canvas ids")
    positions={identifier:i+1 for i,identifier in enumerate(ids)}
    targets=[]
    def walk(nodes,path=()):
        if not isinstance(nodes,list):return
        for n in nodes:
            if not isinstance(n,dict):continue
            title=lab(n.get("label",""))
            refs=n.get("canvases",[])
            if not isinstance(refs,list): refs=[]
            starts=[n.get("startCanvas"),n.get("start")]
            idx=[positions[t] for t in list(refs)+starts if isinstance(t,str) and t in positions]
            if any(q in title for q in ("高麗史五十二","高麗史卷五十二","第六　高麗史五十二","卷52")):
                targets.append({"label":title[:220],"range_path":list(path),"bound_canvas_positions":idx[:24],"index_scope":"LABEL_ONLY_NOT_ORIGINAL_PAGE_ATTESTATION"})
            walk(n.get("ranges",[]),path+(title[:90],))
            walk(n.get("items",[]),path+(title[:90],))
    walk(payload.get("structures",[]))
    walk(payload.get("items",[]) if seq else [],("iiif3",))
    return {"source_pid":"991069","manifest_id":ident,"canvas_count":len(canvases),
            "first_canvas_id":ids[0],"last_canvas_id":ids[-1],
            "title":lab(payload.get("label",""))[:250],
            "toc_range_hints":targets[:40],
            "target_d14_glyph_obtained":False,"target_d16_glyph_obtained":False,
            "physical_copy_independence_adjudicated":False}
def execute(url=URL):
    out={"schema":"TIANWEN-13HM-NDL991069-IIIF-PROBE-RESULT-R1","url":url,"source_type":"PUBLISHED_FIRST_PARTY_NDL_IIIF_MANIFEST"}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"TianwenHistoricalSourceScopeProbe/1.0 (noncommercial bibliographic research)","Accept":"application/json"})
        with urllib.request.urlopen(req,timeout=25) as response:
            content=response.read(12_000_001)
            if len(content)>12_000_000: raise ValueError("manifest exceeds safe 12 MB bound")
            out["http_status"]=response.status
            out["manifest_sha256"]=hashlib.sha256(content).hexdigest()
            out["analysis"]=analyze(json.loads(content))
        out["status"]="MANIFEST_READABLE_UNCOLLATED"
    except Exception as exc:
        out["status"]="ACCESS_OR_FORMAT_BOUNDARY"
        out["error_type"]=type(exc).__name__
        out["error_summary"]=str(exc)[:220]
        out["target_image_acquired"]=False
    return out
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",default="artifacts/13hm-ndl991069-manifest.json")
    args=p.parse_args();v=execute()
    dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":v["status"],"canvas_count":v.get("analysis",{}).get("canvas_count"),"toc_range_hints":len(v.get("analysis",{}).get("toc_range_hints",[])),"manifest_sha256":v.get("manifest_sha256"),"error_type":v.get("error_type")},ensure_ascii=False))
