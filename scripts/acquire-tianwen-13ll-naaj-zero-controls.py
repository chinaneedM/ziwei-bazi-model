#!/usr/bin/env python3
"""Acquire a same-page second circular-zero control via established IIIF services.

No new endpoint discovery or historical glyph adjudication is performed here.
"""
import hashlib,io,json,urllib.request
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'docs/research/TIANWEN-13LJ-NAAJ-FIRSTPARTY-COLOR-ACQUISITION-SNAPSHOT-R1.json'
OUT=Path('13ll-naaj-zero-controls-output')
ROIS={'281-0037':[2080,2250,2430,2800],'281-0038':[2140,2350,2490,2900]}

def main():
    raw=A.read_bytes();assert hashlib.sha256(raw).hexdigest()=='63978aa46ad0f86cede3044d96deed37e3caadbbb142f325989421032f80ab06'
    acquisition=json.loads(raw);OUT.mkdir(exist_ok=True)
    out={'schema':'TIANWEN-13LL-NAAJ-ZERO-CONTROL-COLOR-ACQUISITION','no_ocr':True,'human_reading':'PENDING','same_woodblock_proven':False,'new_recensions':0,'controls':[]}
    for source in acquisition['sources']:
        holding=source['holding'];p=next(x for x in source['pages'] if x['page']==6)
        service=p['native_region_parts'][0]['download']['url'].rsplit('/',4)[0]
        assert service.startswith('https://www.digital.archives.go.jp/api/content/item/') and service.endswith('.jp2')
        x1,y1,x2,y2=ROIS[holding];w=x2-x1;h=y2-y1;url=service+f'/{x1},{y1},{w},{h}/{w},/0/native.jpg'
        req=urllib.request.Request(url,headers={'User-Agent':'TianwenHistoricalAudit/1.0 (same-page source color control)'})
        with urllib.request.urlopen(req,timeout=35) as r:
            data=r.read(2_000_001);assert len(data)<2_000_000 and r.status==200
            ctype=r.headers.get('Content-Type');assert ctype.startswith('image/jpeg')
        im=Image.open(io.BytesIO(data)).convert('RGB');assert im.size==(w,h)
        name=holding+'-p006-second-zero-color.jpg';(OUT/name).write_bytes(data)
        out['controls'].append({'holding':holding,'viewer_id':source['viewer_id'],'page':6,'source_content_id':p['source_content']['id'],'source_canvas_pixels':p['source_canvas_pixels'],'url':url,'native_region_xyxy':ROIS[holding],'pixels':[w,h],'content_type':ctype,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'rgb_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'file':name,'historical_text_review':'PENDING'})
    (OUT/'acquisition.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()
