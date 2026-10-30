#!/usr/bin/env python3
"""Acquire public NAJ JP2 pages using observed viewer form and content IDs.

The response is a provider image surrogate, not certified RAW camera data or
proof of ancient edition/impression identity. No OCR or automated glyph claims.
"""
import hashlib, http.cookiejar, io, json, re, urllib.error, urllib.parse, urllib.request, zipfile
from pathlib import Path
from PIL import Image

BASE='https://www.digital.archives.go.jp'
OUT=Path('13lj-naaj-jp2-output')
OPENER=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
TARGETS=[('281-0037',4034620,51,[3277,472,3566,3955]),('281-0038',3637417,73,[3383,499,3738,4044])]

def fetch(url, data=None):
    assert urllib.parse.urlsplit(url).netloc=='www.digital.archives.go.jp'
    req=urllib.request.Request(url,data=data,headers={'User-Agent':'TianwenHistoricalAudit/1.0 (public source provenance research)'})
    if data is not None:
        req.add_header('X-Requested-With','XMLHttpRequest')
        req.add_header('Referer',BASE+'/img/'+url.split('/contentDownload/')[1].split('?')[0])
        req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    with OPENER.open(req,timeout=70) as r:
        b=r.read(60_000_001);assert len(b)<=60_000_000
        return b, {'url':url,'method':'POST' if data else 'GET','status':r.status,'content_type':r.headers.get('Content-Type'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
    OUT.mkdir(exist_ok=True)
    result={'no_ocr':True,'evidence_grade':'PROVIDER_JP2_DIGITAL_SURROGATE_PENDING_HUMAN_REVIEW','ancient_impression_proven':False,'optical_raw_proven':False,'sources':[]}
    for holding,item,pages,roi in TARGETS:
        row={'holding':holding,'viewer_id':item,'pages':[]};result['sources'].append(row)
        try:
            html,meta=fetch(BASE+f'/img/{item}');(OUT/(holding+'-viewer.html')).write_bytes(html);row['viewer']=meta
            manifest_url=re.search(rb'href="([^"]+/api/iiif/[^"]+/manifest.json)"',html).group(1).decode()
            manifest,manifest_meta=fetch(manifest_url);(OUT/(holding+'-manifest.json')).write_bytes(manifest);row['manifest']=manifest_meta
            arr=json.loads(re.search(rb'var najContentList = (\[.*?\]);',html).group(1));assert len(arr)==pages
            match=re.search(rb'<form[^>]+id="download-form"[^>]*',html).group(0)
            action=re.search(rb'data-download-base-path="([^"]+)"',match).group(1).decode()
            assert re.fullmatch(r'/contentDownload/\d+',action)
            for page in [2,6,7]:
                entry=arr[page-1];assert entry['format']=='image/jp2' and not entry['restricted']
                # Exact cid comes from the checked input in the rendered public download UI.
                cid=re.search(rb'id="download-item-'+str(page).encode()+rb'"[^>]+value="([^"]+)"',html).group(1).decode()
                data=urllib.parse.urlencode({'cid':cid}).encode();url=BASE+action+'?type=jpeg2000'
                info,imeta=fetch(BASE+entry['path']+'/info.json');(OUT/(holding+f'-p{page:03d}-info.json')).write_bytes(info)
                body,download=fetch(url,data)
                label=holding+f'-p{page:03d}'
                (OUT/(label+'-download.bin')).write_bytes(body)
                binaries=[]
                if body.startswith(b'PK'):
                    with zipfile.ZipFile(io.BytesIO(body)) as z:
                        for name in z.namelist():
                            if name.lower().endswith('.jp2'):binaries.append((Path(name).name,z.read(name)))
                elif body.startswith(b'\x00\x00\x00\x0cjP  \r\n\x87\n'):binaries=[(entry['contentName'],body)]
                assert len(binaries)==1,'Expected exactly one provider JP2 per selected page'
                filename,binary=binaries[0];assert filename==entry['contentName']
                path=OUT/(label+'.jp2');path.write_bytes(binary)
                im=Image.open(io.BytesIO(binary)).convert('RGB');assert list(im.size)==[entry['source']['width'],entry['source']['height']]
                info={'page':page,'source_content':entry,'download_cid':cid,'download':download,'jp2_bytes':len(binary),'jp2_sha256':hashlib.sha256(binary).hexdigest(),'rgb_pixels':list(im.size),'decoded_rgb_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'human_reading':'PENDING'}
                if page==6:
                    crop=im.crop(roi);crop.save(OUT/(label+'-numeric-roi.png'));info.update(roi_xyxy=roi,roi_rgb_sha256=hashlib.sha256(crop.tobytes()).hexdigest())
                preview=im.copy();preview.thumbnail((1600,1600));preview.save(OUT/(label+'-preview.jpg'),quality=85)
                row['pages'].append(info)
        except Exception as exc:
            row['error']=type(exc).__name__+': '+str(exc)
            if isinstance(exc,urllib.error.HTTPError):
                b=exc.read();(OUT/(holding+'-http-error.bin')).write_bytes(b);row['error_body_sha256']=hashlib.sha256(b).hexdigest();row['error_body_excerpt']=b.decode('utf-8','replace')[:2000]
        (OUT/'acquisition.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert sum(len(x['pages']) for x in result['sources'])==6,'Not all original JP2 sources acquired'
if __name__=='__main__':main()
