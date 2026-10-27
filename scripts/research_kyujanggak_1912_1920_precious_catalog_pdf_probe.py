#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json
from pathlib import Path
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26787_00"
ITEM_CD="BBG"
DETAIL=f"{BASE}/book/view.do?book_cd={BOOK_CD}&mid=GDS&target=master"
PDF_LIST=f"{BASE}/ajax/book/mfPdfList.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1912-1920-precious-catalog-pdf")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={
        "schema":"KYUJANGGAK-1912-1920-PRECIOUS-CATALOG-PDF-PROBE-R1",
        "book_cd":BOOK_CD,
        "item_cd":ITEM_CD,
        "title":"貴重圖書目錄",
        "catalog_identifier":"奎26787",
        "provider_date":"[1912-1920]",
        "provider_extent":"1冊(72張)",
        "provider_description":"奎章閣 도서 가운데 貴重圖書·特別取扱圖書 및 唐板子部目錄에 관한 8종의 문서를 合綴한 것",
        "read_only":True,
        "ocr_used":False,
        "target_effect":"NONE"
    }
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    try:
        d=s.get(DETAIL,timeout=25)
        result["detail_transport"]=meta(d)
        (out/"detail.html").write_bytes(d.content)
    except Exception as exc:
        result["detail_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
    try:
        r=s.post(PDF_LIST,data={"book_cd":BOOK_CD},headers={"Referer":DETAIL,"Content-Type":"application/x-www-form-urlencoded"},timeout=25)
        result["pdf_list_transport"]=meta(r)
        (out/"mfPdfList.raw").write_bytes(r.content)
        try:
            rows=r.json()
            result["pdf_list_json"]=rows
        except Exception as exc:
            rows=[]
            result["pdf_list_parse_error"]=f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        rows=[]
        result["pdf_list_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}

    downloaded=[]
    for row in rows if isinstance(rows,list) else []:
        vol=str(row.get("VOL_NO") or "").strip()
        is_pdf=str(row.get("IS_PDF") or "").strip().upper()
        if not vol or is_pdf!="Y":
            continue
        url=f"{BASE}/book/mfPdf.do?book_cd={BOOK_CD}&vol_no={vol}"
        rec={"vol_no":vol,"url":url,"provider_row":row}
        try:
            p=s.get(url,headers={"Referer":DETAIL},timeout=40)
            rec["transport"]=meta(p)
            if "pdf" in p.headers.get("content-type","").lower() or p.content.startswith(b"%PDF"):
                fn=f"{BOOK_CD}_{vol}.pdf"
                (out/fn).write_bytes(p.content)
                rec["file"]=fn
                rec["direct_pdf"]=True
            else:
                rec["direct_pdf"]=False
                (out/f"mfPdf-{vol}.html").write_bytes(p.content)
        except Exception as exc:
            rec["transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
        downloaded.append(rec)
    result["pdf_downloads"]=downloaded
    result["conclusion"]={
        "pdf_list_observed":bool(rows),
        "direct_pdf_count":sum(1 for x in downloaded if x.get("direct_pdf")),
        "catalog_review_status":"PENDING_RENDER_FIRST_NO_OCR_VISUAL_REVIEW",
        "g893_identity_effect":"NONE",
        "target_effect":"NONE"
    }
    (out/"probe.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
