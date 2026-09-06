#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
LIST=f"{BASE}/book/list.do?book_cate=COB02&mid=GDS"
HINT_BOOK_CD="GK26787_00"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def li_block(text,needle):
    i=text.find(needle)
    if i<0:return ""
    s=text.rfind("<li",0,i); e=text.find("</li>",i)
    return text[s:e+5] if s>=0 and e>=0 else text[max(0,i-3500):i+3500]

def plain(html):
    x=re.sub(r"<script.*?</script>"," ",html,flags=re.I|re.S)
    x=re.sub(r"<style.*?</style>"," ",x,flags=re.I|re.S)
    x=re.sub(r"<[^>]+>"," ",x)
    x=re.sub(r"&nbsp;"," ",x)
    return re.sub(r"\s+"," ",x).strip()

def target_items(text,book_cd):
    out=[]
    for pat in (
        rf"/thumb/([A-Za-z0-9_-]+)/{re.escape(book_cd)}",
        rf"ThumbServlet\.do\?item_cd=([A-Za-z0-9_-]+)&book_cd={re.escape(book_cd)}",
        rf"fn_originalImg\(['\"]([A-Za-z0-9_-]+)['\"]\s*,\s*['\"]{re.escape(book_cd)}['\"]",
    ):
        for m in re.finditer(pat,text,re.I):
            if m.group(1) not in out: out.append(m.group(1))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1912-catalog-hint")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1912-CATALOG-HINT-RESOLVER-R1","locator_hint":HINT_BOOK_CD,"locator_hint_authority":False,"read_only":True,"ocr_used":False,"target_effect":"NONE"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    try:
        r=s.get(LIST,timeout=25)
        result["list_transport"]=meta(r)
        (out/"official-list.html").write_text(r.text,encoding="utf-8")
        block=li_block(r.text,HINT_BOOK_CD)
        (out/"target-list-item.html").write_text(block,encoding="utf-8")
        result["list_observation"]={
            "hint_present":HINT_BOOK_CD in block,
            "plain_text":plain(block),
            "target_bound_item_cds":target_items(block,HINT_BOOK_CD)
        }
    except Exception as exc:
        result["list_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
        block=""
    if HINT_BOOK_CD in block:
        detail=f"{BASE}/book/view.do?book_cd={HINT_BOOK_CD}&mid=GDS&target=master"
        try:
            d=s.get(detail,timeout=25)
            result["detail_transport"]=meta(d)
            (out/"detail.html").write_text(d.text,encoding="utf-8")
            p=plain(d.text)
            years=sorted(set(re.findall(r"(?<!\d)(18\d{2}|19\d{2}|20\d{2})(?!\d)",p)))
            result["detail_observation"]={
                "plain_prefix":p[:16000],
                "years_visible":years,
                "target_bound_item_cds":target_items(d.text,HINT_BOOK_CD)
            }
        except Exception as exc:
            result["detail_transport"]={"status":0,"error":f"{type(exc).__name__}: {exc}"}
    result["conclusion"]={
        "live_provider_reconfirmed_hint":bool(result.get("list_observation",{}).get("hint_present")),
        "object_identity_status":"PENDING_MANUAL_DETAIL_REVIEW" if result.get("list_observation",{}).get("hint_present") else "UNRESOLVED",
        "target_effect":"NONE"
    }
    (out/"resolver.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
