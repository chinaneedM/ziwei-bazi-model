#!/usr/bin/env python3
"""TIANWEN 13MD: first-party BSB Ming shi 1 bounded chapter-35 title sweep; no OCR."""
import argparse, hashlib, io, json, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw
MANIFEST="https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11166691/manifest"
MANIFEST_SHA="ed4ff6358db2c462edceb9ed5c2d667645cf000ed5f031eec8342fb3a241a369"
INDEXES=[490,491,496,501,506,511,516,521,526,531,536,541,546,551,556,561,566,571,576,581,586,591,596,601,606,611,616,621,626,631,636,637]
EXPECTED_539="7c26f50ce77c3265862e8d347047a568cf424c84f5c4df4dd60b72746fdf0ca0"
def sha(b): return hashlib.sha256(b).hexdigest()
def validate(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.hostname!="api.digitale-sammlungen.de" or p.username or p.password:
        raise ValueError("outside exact BSB source API: "+str(p.hostname))
    return url
class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req,fp,code,msg,headers,validate(newurl))
OPENER=urllib.request.build_opener(SameHostRedirect)
def fetch(url,lim=3500000):
    request=urllib.request.Request(validate(url),headers={"User-Agent":"TIANWEN/13MD IIIF original source-bound research"})
    with OPENER.open(request,timeout=35) as response:
        if response.status!=200: raise ValueError("status "+str(response.status))
        raw=response.read(lim+1)
        if len(raw)>lim: raise ValueError("bounded byte limit exceeded")
        return raw
def run(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    report={"schema":"TIANWEN-13MD-BSB-V1-J35-BOUNDED-SWEEP-R1","target_issue":"TW-OPEN-0005",
      "manifest_url":MANIFEST,"manifest_sha256_expected":MANIFEST_SHA,"selected_canvas_1based":INDEXES,
      "no_ocr":True,"human_original_title_leaf_adjudicated":False,
      "original_numeric_target_adjudicated":False,"original_1739_impression_proven":False,
      "new_historical_numeric_winners":0,"same_copy_only":True,"pages":[]}
    try:
        raw=fetch(MANIFEST,2000000)
        if sha(raw)!=MANIFEST_SHA: raise ValueError("manifest hash drift; do not use old indices")
        m=json.loads(raw);pages=m.get("sequences",[{}])[0].get("canvases",[])
        if len(pages)!=1910: raise ValueError("manifest canvas count changed")
        report["verified_canvas_count"]=len(pages)
        (out/"manifest-source.json").write_bytes(raw)
        thumbs=[]
        for idx in INDEXES:
            c=pages[idx-1]
            service=c.get("images",[{}])[0].get("resource",{}).get("service",{})
            if isinstance(service,list): service=service[0] if service else {}
            sid=service.get("@id") or service.get("id")
            row={"canvas":idx,"canvas_id":c.get("@id") or c.get("id"),"service_id":sid}
            try:
                if not sid: raise ValueError("no original manifest service")
                url=validate(sid.rstrip("/")+"/full/900,/0/default.jpg")
                b=fetch(url)
                im=Image.open(io.BytesIO(b));im.load();rgb=im.convert("RGB")
                if rgb.width>1100 or rgb.height>2200: raise ValueError("unexpected dimensions")
                if idx==539 and sha(b)!=EXPECTED_539:
                    raise ValueError("control canvas539 SHA mismatch: stop numeric adjudication")
                filename=f"canvas-{idx:04d}.jpg";(out/filename).write_bytes(b)
                row.update(status="SOURCE_DERIVATIVE_CAPTURED",url=url,filename=filename,
                           bytes=len(b),sha256=sha(b),rgb_sha256=sha(rgb.tobytes()),
                           pixels=[rgb.width,rgb.height])
                thumb=rgb.copy();thumb.thumbnail((260,400));thumbs.append((idx,thumb))
            except Exception as e:
                row.update(status="PROVIDER_OR_DECODE_BOUNDARY",error=str(e)[:250])
            report["pages"].append(row)
        for group,start in enumerate(range(0,len(thumbs),20),1):
            section=thumbs[start:start+20]
            if not section:continue
            cols=5;w=285;h=445;sheet=Image.new("RGB",(cols*w,((len(section)+cols-1)//cols)*h),"white")
            d=ImageDraw.Draw(sheet)
            for i,(idx,im) in enumerate(section):
                x=(i%cols)*w;y=(i//cols)*h
                d.text((x+8,y+7),f"BSB c{idx} · TITLE CANDIDATE / NO OCR",fill="black")
                sheet.paste(im,(x+8,y+30))
            sheet.save(out/f"contact-{group:02d}.jpg",quality=92)
        report["captured_count"]=len(thumbs)
        report["status"]="SOURCE_IMAGES_CAPTURED_UNCOLLATED" if len(thumbs)==len(INDEXES) else "PARTIAL_ACCESS_BOUNDARY"
    except Exception as ex:
        report.update(status="MANIFEST_OR_INTEGRITY_BLOCKED",error=str(ex)[:350])
    (out/"source-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report.get(k) for k in ("status","verified_canvas_count","captured_count","error")},ensure_ascii=False))
    if report["status"]!="SOURCE_IMAGES_CAPTURED_UNCOLLATED": raise SystemExit(2)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    run(p.parse_args().out)
