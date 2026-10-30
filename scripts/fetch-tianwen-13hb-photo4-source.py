#!/usr/bin/env python3
"""Fetch the immutable 13HB public photo, retrying transport failures only.

Source bytes, SHA256, decoded pixels and historical scope remain strictly
checked by the existing 13HB verifier. No alternate host or cached fallback.
"""
import argparse,hashlib,json,socket,ssl,time,urllib.error,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13HB-NIKH-JUAN52-GALLERY04-D14-DIRECT-PHOTO-GLYPHS-R1.json'
URL='https://db.history.go.kr/common/imageProxy.do?filePath=/kr/052/kr_052_1058.jpg&mode=download'
RETRY_HTTP={408,429,500,502,503,504}

def retryable(exc):
    if isinstance(exc,urllib.error.HTTPError):return exc.code in RETRY_HTTP
    reason=exc.reason if isinstance(exc,urllib.error.URLError) else exc
    if isinstance(reason,ssl.SSLCertVerificationError):return False
    return isinstance(reason,(TimeoutError,ConnectionResetError,ConnectionRefusedError,socket.gaierror))

def fetch(source,opener=urllib.request.urlopen,sleeper=time.sleep,attempts=3):
    assert source['source_emitted_download_url']==URL
    assert 1<=attempts<=3
    events=[]
    for attempt in range(1,attempts+1):
        q=urllib.request.Request(URL,headers={'User-Agent':'Tianwen-13HB-Exact-Official-Gallery-Source/1.0'})
        try:
            with opener(q,timeout=25) as response:
                end=urllib.parse.urlsplit(response.geturl())
                assert end.scheme=='https' and end.netloc=='db.history.go.kr','source redirected outside provider'
                data=response.read(source['jpeg_bytes']+1)
        except (urllib.error.URLError,TimeoutError,ConnectionResetError,ConnectionRefusedError) as exc:
            events.append({'attempt':attempt,'status':'TRANSPORT_FAILURE','error':type(exc).__name__,'retryable':retryable(exc)})
            if not retryable(exc) or attempt==attempts:raise
            sleeper(attempt)
            continue
        # Integrity errors are NOT retried or silently replaced by another image.
        assert len(data)==source['jpeg_bytes'],'original photo byte length changed'
        assert hashlib.sha256(data).hexdigest()==source['jpeg_sha256'],'original photo SHA256 changed'
        events.append({'attempt':attempt,'status':'HASH_VERIFIED','bytes':len(data),'sha256':source['jpeg_sha256']})
        return data,events
    raise AssertionError('unreachable')

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--report');args=p.parse_args()
    evidence=json.loads(E.read_text())
    import importlib.util
    spec=importlib.util.spec_from_file_location('hb',ROOT/'scripts/verify-tianwen-13hb-photo4-day14-direct-glyph.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    assert v.check(evidence)
    data,events=fetch(evidence['source'])
    path=Path(args.output);path.write_bytes(data)
    assert v.check(evidence,path)
    report={'status':'PASS','attempts':events,'source_url':URL,'original_source_unchanged':True,'historical_claims_changed':False}
    if args.report:Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
