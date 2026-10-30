#!/usr/bin/env python3
"""Acquire six first-party IIIF p7 JPEG windows registered by 13LM.
Acquisition is not a human glyph collation or woodblock identification.
"""
import hashlib,io,json,time,urllib.error,urllib.request
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13LM-NAAJ-P7-COLOR-OVERVIEW-DISCRIMINATOR-TRIAGE-R1.json'
OUT=Path('13lm-naaj-p7-native-output')
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(url):
    assert url.startswith('https://www.digital.archives.go.jp/api/content/item/da12/')
    last_error=None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'TianwenHistoricalAudit/1.0 (p7 noncircle source provenance)'})
            with urllib.request.urlopen(req,timeout=40) as r:
                assert r.status==200 and r.headers.get('Content-Type','').lower().startswith('image/jpeg')
                b=r.read(3000001);assert len(b)<=3000000
                return b
        except (TimeoutError,ConnectionError,urllib.error.URLError) as ex:
            last_error=ex
            if isinstance(ex,urllib.error.HTTPError):raise
            if attempt<2:time.sleep(attempt+1)
    raise last_error
def main():
    doc=json.loads(E.read_text(encoding='utf-8'));OUT.mkdir(parents=True,exist_ok=True)
    byholding={x['holding']:x for x in doc['sources']}
    assert list(byholding)==['281-0037','281-0038']
    result={'schema':'TIANWEN-13LM-P7-NATIVE-COLOR-ACQUISITION','original_research_batch':doc['schema'],'human_reading':'PENDING','no_ocr':True,'optical_raw_or_original_jp2_acquired':False,'woodblock_and_impression_adjudicated':False,'historical_votes_awarded':0,'controls':[]}
    for target in doc['targets']:
        for p in target['positions']:
            src=byholding[p['holding']]
            x1,y1,x2,y2=p['planned_native_canvas_xyxy']
            w=x2-x1;h=y2-y1
            assert 0<=x1<x2<=src['source_canvas_pixels'][0] and 0<=y1<y2<=src['source_canvas_pixels'][1]
            assert 0<w<=1000 and 0<h<=1250
            url=src['firstparty_service']+f'/{x1},{y1},{w},{h}/{w},/0/native.jpg'
            b=fetch(url);im=Image.open(io.BytesIO(b)).convert('RGB')
            assert im.size==(w,h),f'native-region response resampled {p["holding"]}/{target["target_id"]}'
            name=p['holding']+'-'+target['target_id'].lower()+'-native.jpg'
            (OUT/name).write_bytes(b)
            result['controls'].append({'holding':p['holding'],'target_id':target['target_id'],'page':7,'source_content_id':src['source_content_id'],'url':url,'native_region_xyxy':[x1,y1,x2,y2],'jpeg_sha256':sha(b),'rgb_sha256':sha(im.tobytes()),'pixels':[w,h],'bytes':len(b),'file':name,'human_reading':'PENDING','same_woodblock_proven':False})
            (OUT/'acquisition.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert len(result['controls'])==6
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
