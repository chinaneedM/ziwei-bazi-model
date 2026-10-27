#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, io, json, re, time
from pathlib import Path
from urllib.parse import urlencode
from curl_cffi import requests
from PIL import Image, ImageDraw

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26775_00"
ITEM_CD="BBG"
VOLUMES=("0001","0002","0003","0004","0005","0006","0007")
RENDERER=BASE+"/pf01/rendererImg.do"
UA="Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"

def req(s,method,url,**kwargs):
    errs=[]
    for attempt in range(1,4):
        try:
            r=s.request(method,url,timeout=20,**kwargs)
            return r,{"url":r.url,"status":r.status_code,"content_type":r.headers.get("content-type",""),"bytes":len(r.content),"sha256":hashlib.sha256(r.content).hexdigest(),"attempt":attempt}
        except Exception as exc:
            errs.append({"attempt":attempt,"type":type(exc).__name__,"error":str(exc)})
            time.sleep(0.5*attempt)
    return None,{"url":url,"status":0,"attempts":errs}

def pages(text):
    out=[]
    for m in re.finditer(r'''fn_goPageJumpWithMokIdxClear\(["']([A-Za-z0-9]+)["']\)''',text):
        p=m.group(1)
        if p.startswith("999"): continue
        if p not in out: out.append(p)
    return out

def img_path(text):
    ms=re.findall(r'''var\s+imgFileNm\s*=\s*["']([^"']+)["']''',text)
    return ms[-1] if ms else None

def make_sheet(items,path):
    if not items: return
    tw=600; lh=36; cols=2
    thumbs=[]
    for label,im in items:
        ratio=tw/im.width
        h=max(1,int(im.height*ratio))
        thumbs.append((label,im.resize((tw,h))))
    ch=max(im.height for _,im in thumbs)+lh
    rows=(len(thumbs)+cols-1)//cols
    sheet=Image.new("RGB",(cols*tw,rows*ch),"white")
    d=ImageDraw.Draw(sheet)
    for i,(label,im) in enumerate(thumbs):
        x=(i%cols)*tw; y=(i//cols)*ch
        sheet.paste(im,(x,y)); d.text((x+5,y+im.height+5),label,fill="black")
    sheet.save(path,quality=92)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="artifacts/kyujanggak-1930-catalog-boundary")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    result={"schema":"KYUJANGGAK-1930-CATALOG-BOUNDARY-SAMPLER-R1","book_cd":BOOK_CD,"item_cd":ITEM_CD,"ocr_used":False,"role":"VOLUME_RANGE_LOCALIZATION_ONLY","target_effect":"NONE","volumes":[]}
    for vol in VOLUMES:
        r0,m0=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":vol,"page_no":"","tool":"1"})
        rec={"vol_no":vol,"renderer":m0,"samples":[]}
        if r0 is None or r0.status_code!=200:
            result["volumes"].append(rec); continue
        ps=pages(r0.text); rec["page_count"]=len(ps)
        picks=[]
        for idx in (0,1,len(ps)//2,max(0,len(ps)-2),len(ps)-1):
            if 0<=idx<len(ps) and ps[idx] not in picks: picks.append(ps[idx])
        rec["sample_page_ids"]=picks
        sheet=[]
        for p in picks:
            rr,rm=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":vol,"page_no":p,"tool":"1"})
            item={"page_no":p,"renderer":rm}
            if rr is None or rr.status_code!=200:
                rec["samples"].append(item); continue
            path=img_path(rr.text); item["img_path"]=path
            if not path:
                rec["samples"].append(item); continue
            base=path.rsplit("/",1)[-1]
            url=BASE+"/ImageServlet.do?"+urlencode({"imgFileNm":base,"path":path})
            ir,im=req(s,"GET",url,headers={"Referer":RENDERER,"Accept":"image/jpeg,image/*,*/*;q=0.8"})
            item["image_transport"]=im
            if ir is not None and ir.status_code==200:
                try:
                    image=Image.open(io.BytesIO(ir.content)).convert("RGB")
                    item["valid_image"]=True
                    item["image_size"]=[image.width,image.height]
                    item["image_sha256"]=hashlib.sha256(ir.content).hexdigest()
                    image.thumbnail((1800,2400))
                    fn=f"{vol}-{p}.jpg"; image.save(out/fn,quality=94)
                    item["file"]=fn; sheet.append((f"{vol}:{p}",image.copy()))
                except Exception as exc:
                    item["valid_image"]=False; item["image_error"]=f"{type(exc).__name__}: {exc}"
            rec["samples"].append(item)
        make_sheet(sheet,out/f"contact-{vol}.jpg")
        result["volumes"].append(rec)
    result["conclusion"]={"valid_images":sum(sum(1 for x in v.get("samples",[]) if x.get("valid_image")) for v in result["volumes"]),"g893_entry_status":"NOT_READ_VISUAL_REVIEW_REQUIRED","target_effect":"NONE"}
    (out/"boundary-sampler.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
