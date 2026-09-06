#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import unquote, urljoin

from curl_cffi import requests

BASE = "https://kyudb.snu.ac.kr"
LIST_URL = BASE + "/book/list.do?book_cate=COB02&mid=GDS"
TITLE = "奎章閣貴重圖書關係書類"
CALL_NUMBER = "奎26786"
COMPILER = "京城帝國大學"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {
        "url": r.url,
        "status": r.status_code,
        "content_type": r.headers.get("content-type", ""),
        "bytes": len(r.content),
        "sha256": hashlib.sha256(r.content).hexdigest(),
    }

def get(session, url, **kwargs):
    errors=[]
    for attempt in range(1,4):
        try:
            r=session.get(url,timeout=30,**kwargs)
            m=meta(r); m["attempt"]=attempt
            return r,m
        except Exception as exc:
            errors.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(attempt)
    return None,{"url":url,"status":0,"attempts":errors}

def post(session, url, **kwargs):
    errors=[]
    for attempt in range(1,4):
        try:
            r=session.post(url,timeout=30,**kwargs)
            m=meta(r); m["attempt"]=attempt
            return r,m
        except Exception as exc:
            errors.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(attempt)
    return None,{"url":url,"status":0,"attempts":errors}

def unique(values):
    out=[]
    for x in values:
        if x and x not in out: out.append(x)
    return out

def target_context(text: str, radius: int = 5000) -> str:
    idx=text.find(TITLE)
    if idx < 0:
        idx=text.find(CALL_NUMBER)
    if idx < 0:
        return ""
    return text[max(0,idx-radius):min(len(text),idx+radius)]

def extract_book_cds(text: str) -> list[str]:
    pats=[
        r"book_cd=([A-Za-z0-9_-]+)",
        r"""book_cd\s*[:=]\s*['"]([A-Za-z0-9_-]+)['"]""",
        r"""fn_[A-Za-z0-9_]+\([^)]*['"](GK[0-9A-Za-z_-]+)['"]""",
        r"(GK[0-9]{5,}_[0-9]{2})",
    ]
    vals=[]
    for pat in pats:
        vals.extend(m.group(1) for m in re.finditer(pat,text,re.I))
    return unique(vals)

def extract_item_cds(text: str, book_cd: str) -> list[str]:
    vals=[]
    pats=[
        rf"item_cd=([A-Za-z0-9_-]+)[^\n\r\"']{{0,180}}book_cd={re.escape(book_cd)}",
        rf"item_cd\s*[:=]\s*['"]([A-Za-z0-9_-]+)['"][^\n\r]{{0,300}}{re.escape(book_cd)}",
        rf"fn_originalImg\(['"]([A-Za-z0-9_-]+)['"]\s*,\s*['"]{re.escape(book_cd)}['"]",
    ]
    for pat in pats:
        vals.extend(m.group(1) for m in re.finditer(pat,text,re.I))
    return unique(vals)

def parse_renderer(text: str):
    vols=unique(m.group(1) for m in re.finditer(r'<option\s+value=["\']([A-Za-z0-9]+)["\']',text,re.I))
    pages=unique(m.group(1) for m in re.finditer(r'fn_goPageJumpWithMokIdxClear\(["\']([A-Za-z0-9]+)["\']\)',text))
    return {"volume_ids":vols,"page_ids":pages,"page_count":len(pages)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1940-precious-relations-locator")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)

    result={
        "schema":"KYUJANGGAK-1940-PRECIOUS-BOOK-RELATIONS-LOCATOR-R1",
        "target":{"title":TITLE,"call_number":CALL_NUMBER,"compiler":COMPILER,"year":1940},
        "read_only":True,
        "ocr_used":False,
        "guessed_book_cd_authorized":False,
        "guessed_item_cd_authorized":False,
        "g893_identity_effect":"NONE_UNTIL_DIRECT_INTERNAL_RECORD",
        "target_value_effect":"NONE",
        "attempts":{},
    }
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    r,m=get(s,LIST_URL,headers={"Referer":BASE+"/"})
    result["attempts"]["list"]=m
    if r is None or r.status_code!=200:
        result["conclusion"]="LIST_UNAVAILABLE"
    else:
        text=r.text
        ctx=target_context(text)
        (out/"target-context.html").write_text(ctx,encoding="utf-8")
        result["list_observation"]={
            "title_present":TITLE in ctx,
            "call_number_present":CALL_NUMBER in ctx,
            "compiler_present":COMPILER in ctx,
            "book_cds_in_target_context":extract_book_cds(ctx),
        }
        # The context may still contain adjacent cards. Bind candidates by probing
        # detail pages and requiring all three target identity fields.
        candidates=extract_book_cds(ctx)
        matches=[]
        for book_cd in candidates:
            url=f"{BASE}/book/view.do?book_cd={book_cd}&mid=GDS&target=master"
            dr,dm=get(s,url,headers={"Referer":LIST_URL})
            rec={"book_cd":book_cd,"transport":dm}
            if dr is not None and dr.status_code==200:
                dt=dr.text
                rec.update({
                    "title_present":TITLE in dt,
                    "call_number_present":CALL_NUMBER in dt,
                    "compiler_present":COMPILER in dt,
                    "item_cds":extract_item_cds(dt,book_cd),
                })
                if rec["title_present"] and rec["call_number_present"] and rec["compiler_present"]:
                    matches.append(rec)
                    (out/f"detail-{book_cd}.html").write_text(dt,encoding="utf-8")
            result.setdefault("candidate_probes",[]).append(rec)
        result["identity_matches"]=matches
        if len(matches)==1:
            book_cd=matches[0]["book_cd"]
            item_cds=matches[0].get("item_cds",[])
            result["observed_book_cd"]=book_cd
            result["observed_item_cds"]=item_cds
            if len(item_cds)==1:
                item_cd=item_cds[0]
                rr,rm=post(s,BASE+"/pf01/rendererImg.do",
                    data={"item_cd":item_cd,"book_cd":book_cd,"vol_no":"","page_no":"","tool":"1"},
                    headers={"Referer":f"{BASE}/book/view.do?book_cd={book_cd}&mid=GDS&target=master",
                             "Content-Type":"application/x-www-form-urlencoded"})
                result["attempts"]["renderer"]=rm
                if rr is not None and rr.status_code==200:
                    (out/"renderer-index.html").write_text(rr.text,encoding="utf-8")
                    result["renderer"]=parse_renderer(rr.text)
            result["conclusion"]="OFFICIAL_DETAIL_IDENTITY_BOUND"
        else:
            result["conclusion"]="TARGET_DETAIL_IDENTITY_NOT_UNIQUELY_BOUND"

    (out/"locator.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "conclusion":result.get("conclusion"),
        "observed_book_cd":result.get("observed_book_cd"),
        "observed_item_cds":result.get("observed_item_cds"),
        "renderer":result.get("renderer"),
    },ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
