#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re
from pathlib import Path
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
LIST=f"{BASE}/book/list.do?book_cate=COB02&mid=GDS"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def extract_li_blocks(text):
    return re.findall(r"<li\b.*?</li>", text, flags=re.I|re.S)

def ids(block):
    books=[]
    items=[]
    for m in re.finditer(r"(?:book_cd=|value=[\"'])(GK[0-9A-Za-z_-]+|GR[0-9A-Za-z_-]+)",block,re.I):
        v=m.group(1)
        if v not in books: books.append(v)
    for m in re.finditer(r"/thumb/([A-Za-z0-9_-]+)/((?:GK|GR)[0-9A-Za-z_-]+)",block,re.I):
        if m.group(1) not in items: items.append(m.group(1))
        if m.group(2) not in books: books.append(m.group(2))
    return {"book_cds":books,"item_cds":items}

def plain(block):
    text=re.sub(r"<script.*?</script>"," ",block,flags=re.I|re.S)
    text=re.sub(r"<style.*?</style>"," ",text,flags=re.I|re.S)
    text=re.sub(r"<[^>]+>"," ",text)
    text=re.sub(r"&nbsp;"," ",text)
    text=re.sub(r"\s+"," ",text).strip()
    return text

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1912-catalog-candidates")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1912-CATALOG-CANDIDATE-DISCOVERY-R1","read_only":True,"ocr_used":False,"target_effect":"NONE","candidate_authority":"NONE_UNTIL_DIRECT_OBJECT_BINDING"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    try:
        r=s.get(LIST,timeout=25)
        result["list_transport"]=meta(r)
        (out/"official-list.html").write_text(r.text,encoding="utf-8")
        blocks=extract_li_blocks(r.text)
        candidates=[]
        for index,block in enumerate(blocks):
            p=plain(block)
            # Directly discover records whose visible metadata contains 1912,
            # 明治45/四十五, or a catalog title and 1912-ish date string.
            if not (re.search(r"1912",p) or "明治45" in p or "明治四十五" in p):
                continue
            rec={"index":index,"plain_text":p,"ids":ids(block)}
            (out/f"candidate-{index:04d}.html").write_text(block,encoding="utf-8")
            candidates.append(rec)
        result["candidates"]=candidates
        result["candidate_count"]=len(candidates)
    except Exception as exc:
        result["list_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
        result["candidates"]=[]
        result["candidate_count"]=0
    result["conclusion"]={"candidate_count":result["candidate_count"],"direct_1912_catalog_object":"PENDING_MANUAL_CANDIDATE_REVIEW","target_effect":"NONE"}
    (out/"candidates.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
