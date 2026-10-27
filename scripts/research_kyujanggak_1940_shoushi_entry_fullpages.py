#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, io, json, re, time
from pathlib import Path
from urllib.parse import urlencode
from curl_cffi import requests
from PIL import Image

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26786_00"
ITEM_CD="BBG"
VOL_NO="0001"
PAGES=("0124","0125","0126","0127")
RENDERER=BASE+"/pf01/rendererImg.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def req(s,method,url,**kwargs):
    errs=[]
    for attempt in range(1,4):
        try:
            r=s.request(method,url,timeout=30,**kwargs)
            return r,{"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest(),"attempt":attempt}
        except Exception as exc:
            errs.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(attempt)
    return None,{"url":url,"status":0,"attempts":errs}

def img_path(text):
    ms=re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''',text)
    return ms[-1] if ms else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1940-shoushi-entry-fullpages")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    result={
      "schema":"KYUJANGGAK-1940-PRECIOUS-TABLE-HEADER-FULLPAGES-R1",
      "book_cd":BOOK_CD,"item_cd":ITEM_CD,"vol_no":VOL_NO,
      "pages":list(PAGES),"ocr_used":False,
      "role":"DIRECT_FULL_PAGE_BINDING_FOR_PRECIOUS_TABLE_HEADER_AND_NUMBER_FIELD_SEMANTICS",
      "g893_identity_authorized":False,
      "target_numeric_values_authorized":False,
      "records":[]
    }
    for p in PAGES:
        rr,rm=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":VOL_NO,"page_no":p,"tool":"1"})
        rec={"page_no":p,"renderer":rm}
        if rr is None or rr.status_code!=200:
            result["records"].append(rec); continue
        path=img_path(rr.text); rec["direct_renderer_img_path"]=path
        if not path:
            result["records"].append(rec); continue
        base=path.rsplit("/",1)[-1]
        url=BASE+"/ImageServlet.do?"+urlencode({"imgFileNm":base,"path":path})
        ir,imeta=req(s,"GET",url,headers={"Referer":RENDERER,"Accept":"image/jpeg,image/*,*/*;q=0.8"})
        rec["image_transport"]=imeta
        if ir is not None and ir.status_code==200:
            try:
                im=Image.open(io.BytesIO(ir.content)).convert("RGB")
                rec["valid_image"]=True
                rec["image_size"]=[im.width,im.height]
                rec["image_sha256"]=hashlib.sha256(ir.content).hexdigest()
                fn=f"full-{p}.jpg"
                im.save(out/fn,quality=98)
                rec["file"]=fn
            except Exception as exc:
                rec["valid_image"]=False; rec["image_error"]=f"{type(exc).__name__}: {exc}"
        result["records"].append(rec)
    result["conclusion"]={
      "valid_images":sum(1 for r in result["records"] if r.get("valid_image")),
      "ocr_used":False,
      "direct_visual_review_required":True,
      "target_effect":"NONE_UNTIL_FULL_PAGE_FIELDS_ARE_DIRECTLY_READ"
    }
    (out/"fullpages.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
