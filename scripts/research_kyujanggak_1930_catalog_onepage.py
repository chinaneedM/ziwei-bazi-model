#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, io, json, re
from pathlib import Path
from urllib.parse import urlencode
from curl_cffi import requests
from PIL import Image

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26775_00"
ITEM_CD="BBG"
RENDERER=BASE+"/pf01/rendererImg.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def req(s,method,url,**kwargs):
    try:
        r=s.request(method,url,timeout=7,**kwargs)
        return r,{"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest()}
    except Exception as exc:
        return None,{"url":url,"status":0,"error":f"{type(exc).__name__}: {exc}"}

def parse_pages(text):
    out=[]
    for m in re.finditer(r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''',text):
        p=m.group(1)
        if p.startswith("999"): continue
        if p not in out: out.append(p)
    return out

def parse_img_path(text):
    ms=re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''',text)
    return ms[-1] if ms else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--volume",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    vol=args.volume
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"KYUJANGGAK-1930-CATALOG-ONEPAGE-R1","book_cd":BOOK_CD,"item_cd":ITEM_CD,"vol_no":vol,"ocr_used":False,"role":"VOLUME_START_RANGE_LOCALIZATION_ONLY","target_effect":"NONE"}
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    r0,m0=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":vol,"page_no":"","tool":"1"})
    result["index"]=m0
    if r0 is not None and r0.status_code==200:
        ps=parse_pages(r0.text); result["page_count"]=len(ps)
        p="001a" if "001a" in ps else (ps[0] if ps else None)
        result["page_no"]=p
        if p:
            rr,rm=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":vol,"page_no":p,"tool":"1"})
            result["page_renderer"]=rm
            if rr is not None and rr.status_code==200:
                path=parse_img_path(rr.text); result["img_path"]=path
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
                            image.thumbnail((2200,3000))
                            fn=f"{vol}-{p}.jpg"; image.save(out/fn,quality=96)
                            result["file"]=fn
                        except Exception as exc:
                            result["valid_image"]=False
                            result["image_error"]=f"{type(exc).__name__}: {exc}"
    result["g893_entry_status"]="NOT_READ_VISUAL_REVIEW_REQUIRED"
    (out/"onepage.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"vol_no":vol,"valid_image":result.get("valid_image",False),"page_no":result.get("page_no"),"target_effect":"NONE"},ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
