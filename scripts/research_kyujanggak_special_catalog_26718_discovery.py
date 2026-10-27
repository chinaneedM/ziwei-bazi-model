#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

from curl_cffi import requests

BASE="https://kyudb.snu.ac.kr"
START=BASE+"/book/list.do?book_cate=COB02&mid=GDS"
TITLE="奎章閣特別圖書目錄"
CALL_NUMBER="奎26718"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def req(s,url):
    errs=[]
    for attempt in range(1,4):
        try:
            r=s.get(url,timeout=30)
            m=meta(r); m["attempt"]=attempt
            return r,m
        except Exception as exc:
            errs.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(attempt)
    return None,{"url":url,"status":0,"attempts":errs}

def same_catalog_list(url):
    p=urlparse(url)
    return p.netloc in ("","kyudb.snu.ac.kr") and p.path.endswith("/book/list.do") and "COB02" in p.query

def pagination_links(html):
    out=[]
    for raw in re.findall(r'''href\s*=\s*["']([^"']+)["']''',html,re.I):
        u=urljoin(BASE,raw.replace("&amp;","&"))
        if same_catalog_list(u) and u not in out:
            out.append(u)
    for raw in re.findall(r'''(?:fn_)?goPage\s*\(\s*['"]?([^'")]+)''',html,re.I):
        if raw.isdigit():
            # Do not construct a page URL from this alone; record only.
            continue
    return out

def context(html,needle,radius=6000):
    i=html.find(needle)
    if i<0:return ""
    s=html.rfind("<li",0,i); e=html.find("</li>",i)
    if s>=0 and e>=0:return html[s:e+5]
    return html[max(0,i-radius):min(len(html),i+radius)]

def ids(text):
    books=[]
    for pat in (r"book_cd=([A-Za-z0-9_-]+)",r"(GK[0-9]{5,}_[0-9]{2})",r"(GR[0-9]{5,}_[0-9]{2})"):
        for m in re.finditer(pat,text,re.I):
            if m.group(1) not in books:books.append(m.group(1))
    return books

def plain(html):
    x=re.sub(r"<script.*?</script>"," ",html,flags=re.I|re.S)
    x=re.sub(r"<style.*?</style>"," ",x,flags=re.I|re.S)
    x=re.sub(r"<[^>]+>"," ",x)
    x=re.sub(r"&nbsp;"," ",x)
    return re.sub(r"\s+"," ",x).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-special-catalog-26718-discovery")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    q=deque([START]); seen=set(); records=[]; matches=[]
    while q and len(seen)<40:
        u=q.popleft()
        if u in seen:continue
        seen.add(u)
        r,m=req(s,u)
        rec={"url":u,"transport":m}
        if r is not None and r.status_code==200:
            html=r.text
            rec["title_present"]=TITLE in html
            rec["call_number_present"]=CALL_NUMBER in html
            links=pagination_links(html)
            rec["observed_pagination_links"]=links
            for v in links:
                if v not in seen and v not in q:q.append(v)
            needle=TITLE if TITLE in html else CALL_NUMBER if CALL_NUMBER in html else None
            if needle:
                block=context(html,needle)
                rec["target_context_plain"]=plain(block)[:12000]
                rec["target_context_book_cds"]=ids(block)
                fn=f"match-{len(matches)+1:02d}.html"
                (out/fn).write_text(block,encoding="utf-8")
                rec["target_context_file"]=fn
                matches.append(rec.copy())
        records.append(rec)
    result={
        "schema":"KYUJANGGAK-SPECIAL-CATALOG-26718-DISCOVERY-R1",
        "target":{"title":TITLE,"call_number":CALL_NUMBER},
        "read_only":True,
        "ocr_used":False,
        "start_url":START,
        "follow_policy":"ONLY_OFFICIAL_SAME_CATALOG_LIST_HREFS_OBSERVED_IN_RETURNED_HTML",
        "visited_count":len(records),
        "visited":records,
        "matches":matches,
        "conclusion":{
            "official_list_match_count":len(matches),
            "object_identity":"PENDING_DETAIL_BINDING" if matches else "NOT_FOUND_IN_OBSERVED_COB02_LIST_LINK_GRAPH",
            "g893_identity_effect":"NONE",
            "target_effect":"NONE"
        }
    }
    (out/"discovery.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
