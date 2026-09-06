#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, time
from pathlib import Path
from urllib.parse import urljoin
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK00893_00"
URL=f"{BASE}/book/view.do?book_cd={BOOK_CD}&mid=GDS&target=master"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/g893-detail-metadata")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    result={"schema":"KYUJANGGAK-G893-DETAIL-METADATA-DISCOVERY-R1","book_cd":BOOK_CD,"read_only":True,"ocr_used":False,"guessed_endpoint_authorized":False}
    try:
        r=s.get(URL,timeout=30)
        result["transport"]=meta(r)
        html=r.text
        (out/"detail.html").write_text(html,encoding="utf-8")
        result["identity_checks"]={
            "title_present":"授時曆立成" in html,
            "call_number_present":"奎貴893" in html,
            "book_cd_present":BOOK_CD in html,
            "microfilm_present":"M/F73-102-37-A" in html,
        }
        urls=[]
        for raw in re.findall(r'''(?:href|src|action)\s*=\s*["']([^"']+)["']''',html,re.I):
            u=urljoin(BASE,raw.replace("&amp;","&"))
            if u not in urls: urls.append(u)
        result["observed_urls"]=[u for u in urls if any(k in u.lower() for k in ("download","down","marc","book","bib","excel","xml","json","print"))][:300]
        funcs=[]
        for m in re.finditer(r'''(?:function\s+([A-Za-z0-9_]+)|([A-Za-z0-9_]+)\s*\([^)]*\))''',html):
            token=(m.group(1) or m.group(2) or "").strip()
            if any(k in token.lower() for k in ("download","down","marc","book","bib","print","original","pdf")) and token not in funcs:
                funcs.append(token)
        result["observed_function_tokens"]=funcs[:300]
        hidden=[]
        for tag in re.findall(r'<input\b[^>]*>',html,re.I):
            name=re.search(r'name=["\']([^"\']+)["\']',tag,re.I)
            value=re.search(r'value=["\']([^"\']*)["\']',tag,re.I)
            if name:
                hidden.append({"name":name.group(1),"value":value.group(1) if value else ""})
        result["input_fields"]=hidden[:500]
        keywords=["奎貴893","授時曆立成","M/F73-102-37-A","舊","旧","原番","番號","番号","登錄","등록","請求","청구","貴重","item_cd","book_cd","marc","download","서지다운로드"]
        contexts={}
        for k in keywords:
            hits=[]
            start=0
            while True:
                i=html.find(k,start)
                if i<0: break
                x=re.sub(r"\s+"," ",html[max(0,i-450):i+700])
                hits.append(x)
                start=i+len(k)
                if len(hits)>=12: break
            if hits: contexts[k]=hits
        result["contexts"]=contexts
        result["conclusion"]={
            "detail_identity_bound":all(result["identity_checks"][k] for k in ("title_present","call_number_present","book_cd_present")),
            "metadata_discovery_status":"DIRECT_DETAIL_HTML_CAPTURED",
            "old_identifier_effect":"PENDING_MANUAL_CONTEXT_REVIEW",
            "target_effect":"NONE"
        }
    except Exception as exc:
        result["transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
        result["conclusion"]={"detail_identity_bound":False,"metadata_discovery_status":"TRANSPORT_FAILED","target_effect":"NONE"}
    (out/"metadata.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
