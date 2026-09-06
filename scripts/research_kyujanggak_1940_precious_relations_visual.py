#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, io, json, re, time
from pathlib import Path
from urllib.parse import urlencode

from curl_cffi import requests
from PIL import Image, ImageDraw

BASE="https://kyudb.snu.ac.kr"
BOOK_CD="GK26786_00"
ITEM_CD="BBG"
VOL_NO="0001"
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

def make_sheet(items,path,cols=3):
    if not items: return
    tw=420; lh=34
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
        sheet.paste(im,(x,y))
        d.text((x+5,y+im.height+5),label,fill="black")
    sheet.save(path,quality=92)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start",type=int,required=True)
    ap.add_argument("--end",type=int,required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--sheet-size",type=int,default=12)
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(impersonate="chrome"); s.headers.update({"User-Agent":UA})
    result={"schema":"KYUJANGGAK-1940-PRECIOUS-RELATIONS-VISUAL-SAMPLER-R1","book_cd":BOOK_CD,"item_cd":ITEM_CD,"vol_no":VOL_NO,"ocr_used":False,"range":[args.start,args.end],"pages":[],"contact_sheets":[]}
    sheet=[]
    sheet_no=1
    for n in range(args.start,args.end+1):
        p=f"{n:04d}"
        rr,rm=req(s,"POST",RENDERER,data={"item_cd":ITEM_CD,"book_cd":BOOK_CD,"vol_no":VOL_NO,"page_no":p,"tool":"1"})
        rec={"page_no":p,"renderer":rm}
        if rr is None or rr.status_code!=200:
            result["pages"].append(rec); continue
        path=img_path(rr.text); rec["img_path"]=path
        if not path:
            result["pages"].append(rec); continue
        base=path.rsplit("/",1)[-1]
        url=BASE+"/ImageServlet.do?"+urlencode({"imgFileNm":base,"path":path})
        ir,im=req(s,"GET",url,headers={"Referer":RENDERER,"Accept":"image/jpeg,image/*,*/*;q=0.8"})
        rec["image_transport"]=im
        if ir is not None and ir.status_code==200:
            try:
                image=Image.open(io.BytesIO(ir.content)).convert("RGB")
                rec["valid_image"]=True
                rec["image_size"]=[image.width,image.height]
                rec["image_sha256"]=hashlib.sha256(ir.content).hexdigest()
                image.thumbnail((1400,1900))
                sheet.append((p,image.copy()))
                if len(sheet)>=args.sheet_size:
                    fn=f"contact-{args.start:04d}-{args.end:04d}-{sheet_no:02d}.jpg"
                    make_sheet(sheet,out/fn)
                    result["contact_sheets"].append(fn)
                    sheet=[]; sheet_no+=1
            except Exception as exc:
                rec["valid_image"]=False; rec["image_error"]=f"{type(exc).__name__}: {exc}"
        result["pages"].append(rec)
    if sheet:
        fn=f"contact-{args.start:04d}-{args.end:04d}-{sheet_no:02d}.jpg"
        make_sheet(sheet,out/fn); result["contact_sheets"].append(fn)
    result["conclusion"]={"valid_images":sum(1 for x in result["pages"] if x.get("valid_image")),"ocr_used":False,"visual_review_required":True,"g893_identity_effect":"NONE_UNTIL_DIRECT_RECORD","target_effect":"NONE"}
    (out/"sampler.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["conclusion"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
