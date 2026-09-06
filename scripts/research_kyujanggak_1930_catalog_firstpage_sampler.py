#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, io, json, re
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
    try:
        r=s.request(method,url,timeout=8,**kwargs)
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
    ap.add_argument("--output",default="artifacts/kyujanggak-1930-catalog-firstpages")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    result={"schema":"KYUJANGGAK-1930-CATALOG-FIRSTPAGE-SAMPLER-R1","book_cd":BOOK_CD,"item_cd":ITEM_CD,"ocr_used":False,"role":"VOLUME_START_RANGE_LOCALIZATION_ONLY","target_effect":"NONE","volumes":[]}
    sheet=[]
    for vol in VOLUMES:
        rec={"vol_no":vol}
        r0,m0=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":vol,"page_no":"","tool":"1"})
        rec["index"]=m0
        if r0 is None or r0.status_code!=200:
            result["volumes"].append(rec); continue
        ps=parse_pages(r0.text)
        rec["page_count"]=len(ps)
        # Prefer the first recto after the cover; fall back to first provider page.
        target="001a" if "001a" in ps else (ps[0] if ps else None)
        rec["sample_page_id"]=target
        if not target:
            result["volumes"].append(rec); continue
        rr,rm=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":vol,"page_no":target,"tool":"1"})
        rec["page_renderer"]=rm
        if rr is None or rr.status_code!=200:
            result["volumes"].append(rec); continue
        path=parse_img_path(rr.text); rec["img_path"]=path
        if not path:
            result["volumes"].append(rec); continue
        base=path.rsplit("/",1)[-1]
        url=BASE+"/ImageServlet.do?"+urlencode({"imgFileNm":base,"path":path})
        ir,im=req(s,"GET",url,headers={"Referer":RENDERER,"Accept":"image/jpeg,image/*,*/*;q=0.8"})
        rec["image"]=im
        if ir is not None and ir.status_code==200:
            try:
                image=Image.open(io.BytesIO(ir.content)).convert("RGB")
                rec["valid_image"]=True
                rec["image_size"]=[image.width,image.height]
                rec["image_sha256"]=hashlib.sha256(ir.content).hexdigest()
                image.thumbnail((1800,2500))
                fn=f"{vol}-{target}.jpg"; image.save(out/fn,quality=95)
                rec["file"]=fn; sheet.append((f"{vol}:{target}",image.copy()))
            except Exception as exc:
                rec["valid_image"]=False; rec["image_error"]=f"{type(exc).__name__}: {exc}"
        result["volumes"].append(rec)
    if sheet:
        tw=650; lh=40; cols=2
        thumbs=[]
        for label,im in sheet:
            ratio=tw/im.width; h=max(1,int(im.height*ratio))
            thumbs.append((label,im.resize((tw,h))))
        ch=max(im.height for _,im in thumbs)+lh
        rows=(len(thumbs)+cols-1)//cols
        canvas=Image.new("RGB",(cols*tw,rows*ch),"white"); d=ImageDraw.Draw(canvas)
        for i,(label,im) in enumerate(thumbs):
            x=(i%cols)*tw; y=(i//cols)*ch
            canvas.paste(im,(x,y)); d.text((x+5,y+im.height+5),label,fill="black")
        canvas.save(out/"contact-firstpages.jpg",quality=94)
    result["conclusion"]={"valid_images":sum(1 for v in result["volumes"] if v.get("valid_image")),"g893_entry_status":"NOT_READ_VISUAL_REVIEW_REQUIRED","target_effect":"NONE"}
    (out/"firstpage-sampler.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
