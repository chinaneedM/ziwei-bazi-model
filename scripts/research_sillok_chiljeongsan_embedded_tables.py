#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import urllib.error
import urllib.request
from pathlib import Path
from PIL import Image

BASE="https://sillok.history.go.kr"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
TARGETS={
 "wda_50016011":[
   "/images/slkimg/wda_50016011_01_v.jpg",
   "/images/slkimg/wda_50016011_01_h.jpg",
 ],
 "wda_50016016":[
   "/images/slkimg/wda_50016016_01_v.jpg",
   "/images/slkimg/wda_50016016_01_h.jpg",
   "/images/slkimg/wda_50016016_02_v.jpg",
   "/images/slkimg/wda_50016016_02_h.jpg",
 ],
}

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Referer":BASE+"/","Accept":"image/jpeg,image/*,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return int(getattr(r,"status",200)),r.headers.get("Content-Type",""),r.read()
    except urllib.error.HTTPError as e:
        return e.code,e.headers.get("Content-Type",""),e.read()
    except Exception as e:
        return 0,type(e).__name__,str(e).encode("utf-8","replace")

def main():
    out=Path("artifacts/sillok-chiljeongsan-embedded-tables")
    out.mkdir(parents=True,exist_ok=True)
    result={
      "schema":"SILLOK-CHILJEONGSAN-EMBEDDED-TABLE-IMAGES-R1",
      "source_layer":"NIKH_OFFICIAL_ARTICLE_EMBEDDED_TABLE_IMAGE",
      "ocr_used":False,
      "target_values_authorized_by_fetch":False,
      "physical_scan_equivalence":"NOT_ASSUMED",
      "articles":[],
    }
    any_error=False
    for article,paths in TARGETS.items():
        rec={"article_id":article,"images":[]}
        for p in paths:
            url=BASE+p
            status,ctype,body=fetch(url)
            item={"path":p,"url":url,"status":status,"content_type":ctype,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()}
            try:
                im=Image.open(io.BytesIO(body))
                item["valid_image"]=True
                item["format"]=im.format
                item["size"]=[im.width,im.height]
                fn=Path(p).name
                (out/fn).write_bytes(body)
                item["file"]=fn
            except Exception as exc:
                item["valid_image"]=False
                item["image_error"]=f"{type(exc).__name__}: {exc}"
                any_error=True
            rec["images"].append(item)
        result["articles"].append(rec)
    (out/"embedded-table-map.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 2 if any_error else 0

if __name__=="__main__":
    raise SystemExit(main())
