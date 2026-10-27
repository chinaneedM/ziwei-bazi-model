#!/usr/bin/env python3
"""13FD: single source-attested NIKH Save Original action; no guessed endpoints."""
import hashlib
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error

BASE='https://db.history.go.kr'
VIEWER=BASE+'/common/imageViewer.do?levelId=kr_052_0010_0010_0020_0020&begin=kr_052_1055'
CFG=BASE+'/resources/imageViewer/js/html5_viewer.config.js?ver=2.0'
JS=BASE+'/resources/imageViewer/js/html5_viewer.js?ver=2.0'
SHA_VIEWER='25ecd6a4672bdaa29d188409c6c10e1c7050cc7481b54c6f9cf3fb1417f28342'
SHA_CFG='42d967840816a0d21ad8ee9cfa9f9bde8c1ffde59fe49e8a6adf86f6ab6accc8'
SHA_JS='87e8a9dfcf57083e2641939bf6fe87f1713245fbb7e8563d3e0128083a221655'
FIRST='kr/052/kr_052_1055.jpg'
OUT=Path(os.environ.get('TIANWEN_PROBE_OUT','/tmp/tianwen-13fd-probe'))

def save_url(config,code,viewer):
    if not all(s in config for s in ('proxyFile : "/common/imageProxy.do?"','proxyParam : "filePath="','serverContext : ""','imgFileRootDir : ""')):
        return None
    if not all(s in code for s in ('saveOri : function()', "'&mode=download'", 'this.cfg.imgFileList[this.cfg.imgFileViewPage]')):
        return None
    if '"kr/052/kr_052_1055.jpg"' not in viewer or 'viewer.addFile(imgArr)' not in viewer:
        return None
    return BASE+'/common/imageProxy.do?filePath=/'+FIRST+'&mode=download'

def fetch(url,limit):
    r={'url':url,'status':'UNREAD','http':None,'bytes':0,'sha256':None,'content_type':None}
    try:
        req=urllib.request.Request(url,headers={
            'User-Agent':'Tianwen-Research-13FD-Source-Emitted-Download/1.0',
            'Accept':'image/*,application/octet-stream,text/javascript,text/html;q=0.5'})
        with urllib.request.urlopen(req,timeout=26) as res:
            r['http']=res.status
            r['content_type']=res.headers.get('Content-Type')
            r['final_url']=res.geturl()
            u=urllib.parse.urlsplit(res.geturl())
            if u.scheme!='https' or u.hostname!='db.history.go.kr':
                r['status']='REDIRECT_OUTSIDE_PUBLISHER'
                return r,None
            data=res.read(limit+1)
            r['bytes']=len(data)
            if len(data)>limit:
                r['status']='BYTE_CAP'
                return r,None
            r['sha256']=hashlib.sha256(data).hexdigest()
            r['status']='PUBLIC_BYTES_CAPTURED'
            return r,data
    except urllib.error.HTTPError as e:
        r['http']=e.code
        r['status']='HTTP_ERROR'
    except Exception as e:
        r['status']='TRANSPORT_ERROR'
        r['error_type']=type(e).__name__
    return r,None

def image_format(data):
    if data.startswith(b'\xff\xd8\xff'):return 'JPEG'
    if data.startswith(b'\x89PNG\r\n\x1a\n'):return 'PNG'
    if data.startswith((b'II*\x00',b'MM\x00*')):return 'TIFF'
    if data.startswith(b'%PDF-'):return 'PDF_NOT_IMAGE'
    return 'NON_IMAGE_OR_UNKNOWN'

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    checks=[(VIEWER,SHA_VIEWER),(CFG,SHA_CFG),(JS,SHA_JS)]
    reads=[]
    raw=[]
    for url,sha in checks:
        meta,content=fetch(url,350_000)
        meta['matches_prior_source_sha256']=bool(content and meta['sha256']==sha)
        reads.append(meta)
        raw.append(content)
    proof=all(r['matches_prior_source_sha256'] for r in reads)
    url=save_url(raw[1].decode('utf8','replace'),raw[2].decode('utf8','replace'),raw[0].decode('utf8','replace')) if proof else None
    result={
        'schema':'TIANWEN-13FD-NIKH-JUAN52-FIRST-PARTY-SAVE-ORIGINAL-ONE-IMAGE-PROBE-R1',
        'date':'2026-10-24','issue_id':'TW-OPEN-0005',
        'prior_source_actions_run':40056037073,
        'source_reads':reads,'source_code_and_viewer_identity_verified':proof,
        'download_url_derived_from_first_party_js':url,'download_attempts':0,
        'image_read':None,'verified_source_physical_copy':None,
        'verified_source_leaf':None,'historic_D5_original_glyph':None,
        'g893_six_control_values':None,'num_original_glyph_votes_added':0,
        'algorithm_reopens':0,'no_endpoint_enumeration':True,
        'no_access_control_bypass':True}
    if url:
        result['download_attempts']=1
        info,data=fetch(url,25_000_000)
        info['format']=image_format(data) if data else None
        info['not_yet_certified_original_edition_folio']=True
        result['image_read']=info
        if data and info['format'] in ('JPEG','PNG','TIFF'):
            (OUT/'one-official-save-image.bin').write_bytes(data)
    (OUT/'probe-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='source_reads'},ensure_ascii=False))
    assert result['download_attempts']<=1 and result['num_original_glyph_votes_added']==0

if __name__=='__main__':
    run()
