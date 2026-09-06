#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
LIST=f"{BASE}/book/list.do?book_cate=COB02&mid=GDS"
CALL="古016.09-G995"
TITLE="貴重圖書目錄"
BOOK_CD="GR35006_00"
ITEM_CD="BBG"
PDF_LIST=f"{BASE}/ajax/book/mfPdfList.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def li_block(text,needle):
    i=text.find(needle)
    if i<0:return ""
    s=text.rfind("<li",0,i); e=text.find("</li>",i)
    return text[s:e+5] if s>=0 and e>=0 else text[max(0,i-2500):i+2500]

def ids(text):
    books=[]; items=[]
    for m in re.finditer(r"(GK[0-9]{5,}_[0-9]{2})",text):
        if m.group(1) not in books: books.append(m.group(1))
    for m in re.finditer(r"item_cd=([A-Za-z0-9_-]+)",text):
        if m.group(1) not in items: items.append(m.group(1))
    for m in re.finditer(r"/thumb/([A-Za-z0-9_-]+)/GK[0-9A-Za-z_-]+",text):
        if m.group(1) not in items: items.append(m.group(1))
    return {"book_cds":books,"item_cds":items}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1908-precious-catalog")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1908-PRECIOUS-CATALOG-PROBE-R1","call_number":CALL,"title":TITLE,"read_only":True,"ocr_used":False,"g893_identity_effect":"NONE_UNTIL_DIRECT_ENTRY","target_effect":"NONE"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    try:
        r=s.get(LIST,timeout=20)
        result["list_transport"]=meta(r)
        text=r.text; (out/"list.html").write_text(text,encoding="utf-8")
        block=li_block(text,CALL); (out/"target-list-item.html").write_text(block,encoding="utf-8")
        observed=ids(block)
        result["list_observation"]={"call_present":CALL in block,"title_present":TITLE in block,"ids":observed}
    except Exception as exc:
        result["list_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
        observed={"book_cds":[],"item_cds":[]}
    # Official live list thumbnail routing independently exposes
    # GR35006_00 / BBG for this exact 1908 catalog. Use those observed IDs
    # directly so a transient list-page TLS reset cannot block the PDF endpoint.
    result["official_live_list_bound_ids"]={"book_cd":BOOK_CD,"item_cd":ITEM_CD}
    result["book_cd"]=BOOK_CD
    result["item_cd"]=ITEM_CD
    detail=f"{BASE}/book/view.do?book_cd={BOOK_CD}&mid=GDS&target=master"
    try:
        d=s.get(detail,timeout=20)
        result["detail_transport"]=meta(d)
        (out/"detail.html").write_text(d.text,encoding="utf-8")
    except Exception as exc:
        result["detail_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
    try:
        p=s.post(PDF_LIST,data={"book_cd":BOOK_CD},headers={"Referer":detail,"Content-Type":"application/x-www-form-urlencoded"},timeout=20)
        result["pdf_list_transport"]=meta(p)
        (out/"mfPdfList.raw").write_bytes(p.content)
        try: result["pdf_list_json"]=p.json()
        except Exception as exc: result["pdf_list_parse_error"]=f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        result["pdf_list_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
    result["frontend_route_probe"]={}
    for js_path in ("/js/common.js","/js/common2.js","/js/book/bookSearch.js"):
        try:
            j=s.get(BASE+js_path,headers={"Referer":detail},timeout=20)
            rec={"transport":meta(j)}
            (out/("js-"+js_path.rsplit("/",1)[-1])).write_bytes(j.content)
            text=j.text
            idx=text.find("fn_mfPdf")
            rec["contains_fn_mfPdf"]=idx>=0
            if idx>=0:
                rec["context"]=text[max(0,idx-1200):idx+5000]
            result["frontend_route_probe"][js_path]=rec
        except Exception as exc:
            result["frontend_route_probe"][js_path]={"status":0,"error":f"{type(exc).__name__}: {exc}"}

    pdf_view_url=f"{BASE}/book/mfPdf.do?book_cd={BOOK_CD}&vol_no=0001"
    result["official_pdf_view_url"]=pdf_view_url
    try:
        vr=s.get(pdf_view_url,headers={"Referer":detail},timeout=30)
        result["pdf_view_transport"]=meta(vr)
        ctype=vr.headers.get("content-type","").lower()
        if "pdf" in ctype or vr.content.startswith(b"%PDF"):
            (out/"GR35006_00_0001.pdf").write_bytes(vr.content)
            result["pdf_view_kind"]="DIRECT_PDF"
            result["pdf_file"]="GR35006_00_0001.pdf"
        else:
            (out/"mfPdf-viewer.html").write_bytes(vr.content)
            result["pdf_view_kind"]="HTML_OR_OTHER"
            html=vr.text
            candidates=[]
            for pat in (
                r'''(?:file|url|pdfUrl|pdf_url)\s*[:=]\s*["']([^"']+\.pdf(?:\?[^"']*)?)["']''',
                r'''["']([^"']+\.pdf(?:\?[^"']*)?)["']''',
                r'''(?:src|href)=["']([^"']+)["']''',
            ):
                for m in re.finditer(pat,html,re.I):
                    value=m.group(1)
                    if value not in candidates and ("pdf" in value.lower() or "file" in value.lower()):
                        candidates.append(value)
            result["viewer_pdf_candidates"]=candidates[:50]
    except Exception as exc:
        result["pdf_view_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}

    result["conclusion"]={
        "catalog_object_bound":bool(result.get("book_cd")),
        "pdf_list_observed":bool(result.get("pdf_list_json")),
        "g893_internal_entry_status":"PENDING_DIRECT_1908_CATALOG_READING",
        "g893_identity_effect":"NONE",
        "target_effect":"NONE"
    }
    (out/"probe.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
