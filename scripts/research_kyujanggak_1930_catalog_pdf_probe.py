#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26775_00"
DETAIL=f"{BASE}/book/view.do?book_cd={BOOK_CD}&mid=GDS&target=master"
PDF_LIST=f"{BASE}/ajax/book/mfPdfList.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1930-catalog-pdf-probe")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1930-CATALOG-PDF-PROBE-R1","book_cd":BOOK_CD,"read_only":True,"ocr_used":False,"target_effect":"NONE"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    try:
        d=s.get(DETAIL,timeout=20)
        result["detail"]=meta(d)
        (out/"detail.html").write_text(d.text,encoding="utf-8")
    except Exception as exc:
        result["detail"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
    try:
        r=s.post(PDF_LIST,data={"book_cd":BOOK_CD},headers={"Referer":DETAIL,"Content-Type":"application/x-www-form-urlencoded"},timeout=20)
        result["pdf_list_transport"]=meta(r)
        (out/"mfPdfList.raw").write_bytes(r.content)
        try:
            result["pdf_list_json"]=r.json()
        except Exception as exc:
            result["pdf_list_parse_error"]=f"{type(exc).__name__}: {exc}"
            result["pdf_list_body_prefix"]=r.text[:4000]
    except Exception as exc:
        result["pdf_list_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
    result["conclusion"]={
        "official_pdf_list_observed":bool(result.get("pdf_list_json")),
        "g893_internal_entry_status":"PENDING_DIRECT_CATALOG_PAGE_READING",
        "g893_identity_effect":"NONE",
        "target_effect":"NONE"
    }
    (out/"pdf-probe.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
