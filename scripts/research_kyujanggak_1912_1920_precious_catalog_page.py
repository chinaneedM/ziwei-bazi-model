#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, io, json, re, time
from pathlib import Path
from urllib.parse import urlencode
from curl_cffi import requests
from PIL import Image

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26787_00"
ITEM_CD="BBG"
VOL_NO="0001"
RENDERER=BASE+"/pf01/rendererImg.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def meta(r):
    return {"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}

def req(s,method,url,**kwargs):
    errors=[]
    for attempt in range(1,5):
        try:
            r=s.request(method,url,timeout=25,**kwargs)
            m=meta(r); m["attempt"]=attempt
            return r,m
        except Exception as exc:
            errors.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(0.8*attempt)
    return None,{"url":url,"status":0,"attempts":errors}

def img_path(text):
    ms=re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''',text)
    return ms[-1] if ms else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--page",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    page=args.page
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1912-1920-PRECIOUS-CATALOG-PAGE-R1","book_cd":BOOK_CD,"item_cd":ITEM_CD,"vol_no":VOL_NO,"page_no":page,"read_only":True,"ocr_used":False,"role":"SPARSE_VISUAL_DOCUMENT_BOUNDARY_LOCALIZATION_ONLY","target_effect":"NONE"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    rr,rm=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":VOL_NO,"page_no":page,"tool":"1"})
    result["renderer_transport"]=rm
    if rr is not None and rr.status_code==200:
        (out/"renderer.html").write_bytes(rr.content)
        path=img_path(rr.text); result["img_path"]=path
        if path:
            base=path.rsplit("/",1)[-1]
            url=BASE+"/ImageServlet.do?"+urlencode({"imgFileNm":base,"path":path})
            ir,im=req(s,"GET",url,headers={"Referer":RENDERER,"Accept":"image/jpeg,image/*,*/*;q=0.8"})
            result["image_transport"]=im
            if ir is not None and ir.status_code==200:
                try:
                    image=Image.open(io.BytesIO(ir.content)).convert("RGB")
                    result["valid_image"]=True
                    result["image_size"]=[image.width,image.height]
                    result["image_sha256"]=hashlib.sha256(ir.content).hexdigest()
                    image.thumbnail((2400,3400))
                    fn=f"page-{page}.jpg"; image.save(out/fn,quality=96)
                    result["file"]=fn
                except Exception as exc:
                    result["image_error"]=f"{type(exc).__name__}: {exc}"
    result["conclusion"]={"valid_image":bool(result.get("valid_image")),"visual_review":"PENDING_MANUAL","target_effect":"NONE"}
    (out/"page.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"page":page,**result["conclusion"]},ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
