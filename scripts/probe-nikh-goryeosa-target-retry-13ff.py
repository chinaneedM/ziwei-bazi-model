#!/usr/bin/env python3
"""13FF source-index 3+4 exact-first-party retries after 13FE transport resets."""
import importlib.util
import json
import os
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("atlas13fe",ROOT/"scripts/probe-nikh-goryeosa-source-atlas-13fe.py")
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
OUT=Path(os.environ.get("TIANWEN_PROBE_OUT","/tmp/tianwen-13ff-retry"))

def retry_plan(urls):
    if len(urls)!=23 or not all(x.startswith(m.BASE+"/common/imageProxy.do?filePath=/kr/052/kr_052_") for x in urls):
        return []
    if not urls[2].endswith("/kr/052/kr_052_1057.jpg&mode=download") or not urls[3].endswith("/kr/052/kr_052_1058.jpg&mode=download"):
        return []
    return [(3,urls[2]),(4,urls[3])]

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    sources={};raw={}
    for url,sha in m.EXPECTED.items():
        row,data=m.read(url,750_000)
        row["sha256_matches_13fe"]=bool(data and row["sha256"]==sha)
        sources[url]=row
        raw[url]=data
    verified=all(z["sha256_matches_13fe"] for z in sources.values())
    urls=m.permitted_download_urls(*(raw[u].decode("utf8","replace") for u in (m.VIEWER,m.CFG,m.JS))) if verified else []
    plan=retry_plan(urls)
    results=[]
    for position,url in plan:
        obj={"position":position,"source_emitted_url":url,"bounded_attempts":[],"success":False,"saved_sha256":None,"physical_original_leaf_number":None,"D5_glyph_reading":None}
        for attempt in range(1,4):
            if attempt>1:time.sleep(1.3*attempt)
            z,data=m.read(url)
            z["attempt"]=attempt
            z["image_header_verified"]=bool(data and data.startswith(b"\xff\xd8\xff"))
            obj["bounded_attempts"].append(z)
            if data and z["image_header_verified"]:
                p=OUT/f"target-source-viewer-{position:02d}.jpg"
                p.write_bytes(data)
                obj["success"]=True
                obj["saved_sha256"]=z["sha256"]
                obj["saved_bytes"]=z["bytes"]
                break
        results.append(obj)
    output={
      "schema":"TIANWEN-13FF-GORYEOSA-JUAN52-SOURCE-INDEX3-4-BOUNDED-RETRY-R1",
      "issue_id":"TW-OPEN-0005","date":"2026-10-24",
      "source_sha_all_verified":verified,
      "public_publisher_declared_pages":len(urls),
      "targeted_source_indexes":[3,4],
      "source_only_retry_plan":len(plan)==2,
      "total_requests_attempted":sum(len(x["bounded_attempts"]) for x in results),
      "results":results,
      "no_guessed_ancient_folio_or_endpoint":True,
      "source_original_D5_glyph_adjudicated":False,
      "num_original_source_glyph_votes_added":0,
      "source_copy_distinctness_assumed":False,
      "remaining_transport_errors_are_not_missing_historical_pages":True,
    }
    (OUT/"retry-manifest.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"source_verified":verified,"planned":len(plan),"attempts":output["total_requests_attempted"],"results":[(z["position"],z["success"],z["saved_sha256"]) for z in results],"glyph_votes":0}))
    assert output["total_requests_attempted"]<=6
if __name__=="__main__":run()
