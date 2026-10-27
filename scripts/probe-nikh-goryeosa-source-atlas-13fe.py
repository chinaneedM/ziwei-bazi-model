#!/usr/bin/env python3
"""13FE: acquire at most 23 publisher-listed NIKH juan52 original-save JPEGs.

No URL guessing, no privileged access, no image interpretation or glyph voting.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

BASE="https://db.history.go.kr"
VIEWER=BASE+"/common/imageViewer.do?levelId=kr_052_0010_0010_0020_0020&begin=kr_052_1055"
CFG=BASE+"/resources/imageViewer/js/html5_viewer.config.js?ver=2.0"
JS=BASE+"/resources/imageViewer/js/html5_viewer.js?ver=2.0"
EXPECTED={
VIEWER:"25ecd6a4672bdaa29d188409c6c10e1c7050cc7481b54c6f9cf3fb1417f28342",
CFG:"42d967840816a0d21ad8ee9cfa9f9bde8c1ffde59fe49e8a6adf86f6ab6accc8",
JS:"87e8a9dfcf57083e2641939bf6fe87f1713245fbb7e8563d3e0128083a221655",
}
CAP=6_000_000
OUT=Path(os.environ.get("TIANWEN_PROBE_OUT","/tmp/tianwen-13fe-collation"))
SOURCE_IMG=re.compile(r"kr/052/kr_052_[0-9]+[.]jpg\Z")
def source_emitted_array(markup):
    match=re.search(r"\bvar\s+imgArr\s*=\s*\[([^\]]{1,3000})\]\s*;",markup)
    if not match or "viewer.addFile(imgArr);" not in markup: return []
    literal=match.group(1)
    values=re.findall(r'"([^"]+)"',literal)
    leftover=re.sub(r'"[^"]+"',"",literal)
    if leftover.strip(" \n\r\t,") or len(values)!=23 or len(set(values))!=len(values):
        return []
    if not all(SOURCE_IMG.fullmatch(x) for x in values):return []
    first_party_thumb_paths=re.findall(r'data-src="/common/imageProxy[.]do[?]mode=thumb&filePath=/([^"]+)"',markup)
    if values!=first_party_thumb_paths:return []
    return values
def permitted_download_urls(markup,config,script):
    if not all(s in config for s in ('proxyFile : "/common/imageProxy.do?"','proxyParam : "filePath="','serverContext : ""','imgFileRootDir : ""')):return []
    if not all(s in script for s in ('saveOri : function()', "'&mode=download'", 'this.cfg.imgFileList[this.cfg.imgFileViewPage]')):return []
    names=source_emitted_array(markup)
    return [BASE+"/common/imageProxy.do?filePath=/"+x+"&mode=download" for x in names]
def read(url,cap=CAP):
    row={"url":url,"status":None,"http":None,"bytes":0,"sha256":None}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Tianwen-Research-13FE-Source-Declared-Image-Atlas/1.0","Accept":"image/jpeg,image/*;q=0.8,*/*;q=0.1"})
        with urllib.request.urlopen(req,timeout=16) as f:
            row["http"]=f.status
            if urllib.parse.urlsplit(f.geturl()).hostname!="db.history.go.kr":
                row["status"]="UNTRUSTED_REDIRECT"
                return row,None
            data=f.read(cap+1)
            row["bytes"]=len(data)
            if len(data)>cap:
                row["status"]="TOO_LARGE";return row,None
            row["sha256"]=hashlib.sha256(data).hexdigest()
            row["status"]="PUBLIC_SOURCE_BYTES" if f.status==200 else "HTTP_NON200"
            return row, data if f.status==200 else None
    except urllib.error.HTTPError as e:
        row["http"]=e.code;row["status"]="HTTP_ERROR"
    except Exception as e:
        row["status"]="TRANSPORT_ERROR";row["error_type"]=type(e).__name__
    return row,None
def run():
    OUT.mkdir(parents=True,exist_ok=True)
    sources={};source_raw={}
    for u,sha in EXPECTED.items():
        info,raw=read(u,750_000)
        info["matches_prior_sha"]=bool(raw and info["sha256"]==sha)
        sources[u]=info;source_raw[u]=raw
    trusted=all(r["matches_prior_sha"] for r in sources.values())
    urls=permitted_download_urls(*(source_raw[u].decode("utf-8","replace") for u in (VIEWER,CFG,JS))) if trusted else []
    result={
      "schema":"TIANWEN-13FE-JUAN52-EXACT-SOURCE-EMITTED-IMAGE-ATLAS-R1",
      "date":"2026-10-24","issue_id":"TW-OPEN-0005",
      "source_script_and_viewer_sha_match":trusted,
      "source_reads":sources,
      "source_emitted_image_count":len(urls),
      "image_acquisitions":[],
      "no_number_enumeration_or_guessed_endpoints":True,
      "original_physical_book_number":None,"original_leaf_numbers":None,
      "source_D5_ink_decision":None,
      "source_original_glyph_votes":0,
      "exhaustive_historical_text_collation_done":False,
      "modern_source_images_are_one_witness_not_many":True,
    }
    for i,url in enumerate(urls):
        if i:time.sleep(0.25)
        r,raw=read(url)
        r["viewer_index"]=i+1
        r["original_physical_folio_certified"]=False
        r["format"]="JPEG" if raw and raw.startswith(b"\xff\xd8\xff") else "UNKNOWN_OR_NONE"
        if raw and r["format"]=="JPEG":
            (OUT/("viewer-%02d.jpg"%(i+1))).write_bytes(raw)
            r["saved_file"]="viewer-%02d.jpg"%(i+1)
        result["image_acquisitions"].append(r)
    (OUT/"atlas-manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    succeeded=sum(x["format"]=="JPEG" for x in result["image_acquisitions"])
    print(json.dumps({"trusted":trusted,"source_declared":len(urls),"saved_jpeg":succeeded,"failures":[{"i":x["viewer_index"],"status":x["status"]} for x in result["image_acquisitions"] if x["format"]!="JPEG"],"glyph_vote":0}))
    assert len(urls)<=23 and result["source_original_glyph_votes"]==0
if __name__=="__main__":run()
