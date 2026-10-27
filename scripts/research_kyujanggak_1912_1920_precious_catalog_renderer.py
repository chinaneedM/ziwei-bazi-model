#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, time
from pathlib import Path
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26787_00"
ITEM_CD="BBG"
VOL_NO="0001"
RENDERER=BASE+"/pf01/rendererImg.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def req(s,method,url,**kwargs):
    errs=[]
    for attempt in range(1,4):
        try:
            r=s.request(method,url,timeout=25,**kwargs)
            m=meta(r); m["attempt"]=attempt
            return r,m
        except Exception as exc:
            errs.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(attempt)
    return None,{"url":url,"status":0,"attempts":errs}

def page_ids(text):
    out=[]
    for m in re.finditer(r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''',text):
        p=m.group(1)
        if p not in out: out.append(p)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1912-1920-precious-catalog-renderer")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1912-1920-PRECIOUS-CATALOG-RENDERER-R1","book_cd":BOOK_CD,"item_cd":ITEM_CD,"vol_no":VOL_NO,"read_only":True,"ocr_used":False,"target_effect":"NONE"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    r,m=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":VOL_NO,"page_no":"","tool":"1"})
    result["renderer_transport"]=m
    if r is not None and r.status_code==200:
        text=r.text
        (out/"renderer-index.html").write_text(text,encoding="utf-8")
        pages=page_ids(text)
        result["page_ids"]=pages
        result["page_count"]=len(pages)
        result["non_terminal_page_ids"]=[p for p in pages if not p.startswith("999")]
        result["non_terminal_page_count"]=len(result["non_terminal_page_ids"])
        first=re.findall(r'''first_page_no\s*=\s*["']([A-Za-z0-9]+)["']''',text)
        if first: result["first_page_no"]=first[-1]
    result["conclusion"]={
        "renderer_bound":bool(result.get("page_ids")),
        "page_count":result.get("page_count",0),
        "visual_review_status":"PENDING_SPARSE_NATIVE_IMAGE_SAMPLING",
        "target_effect":"NONE"
    }
    (out/"renderer.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
