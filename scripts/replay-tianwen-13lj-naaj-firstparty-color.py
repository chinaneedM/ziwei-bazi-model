#!/usr/bin/env python3
"""Replay acquired first-party color byte/RGB and native-region integrity.

Usage: replay...py DIRECTORY of files named by the immutable acquisition JSON.
This verifies evidence integrity; it cannot perform philology or prove woodblocks.
"""
import hashlib,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT/'docs/research/TIANWEN-13LJ-NAAJ-FIRSTPARTY-COLOR-ACQUISITION-SNAPSHOT-R1.json'

def replay(directory,acquisition):
    checked=[];directory=Path(directory)
    for source in acquisition['sources']:
        for page in source['pages']:
            path=directory/page['color_file']; b=path.read_bytes()
            assert len(b)==page['color_download']['bytes'],'source length mismatch'
            assert hashlib.sha256(b).hexdigest()==page['color_download']['sha256'],'source digest mismatch'
            with Image.open(path) as im:
                rgb=im.convert('RGB')
                assert list(rgb.size)==page['color_pixels'],'color dimensions mismatch'
                assert hashlib.sha256(rgb.tobytes()).hexdigest()==page['color_rgb_sha256'],'decoded color mismatch'
            if page['page']==6:
                x1,y1,x2,y2=page['roi_xyxy'];assembled=Image.new('RGB',(x2-x1,y2-y1));cursor=y1
                for part in page['native_region_parts']:
                    x,y,w,h=part['region_xywh'];assert x==x1 and y==cursor and w==x2-x1 and 0<h<=2000
                    path=directory/part['file'];b=path.read_bytes()
                    assert hashlib.sha256(b).hexdigest()==part['download']['sha256'],'native region byte mismatch'
                    with Image.open(path) as im:
                        rgb=im.convert('RGB');assert rgb.size==(w,h),'native region resampled'
                        assert hashlib.sha256(rgb.tobytes()).hexdigest()==part['rgb_sha256'],'native region RGB mismatch'
                        assembled.paste(rgb,(0,y-y1))
                    cursor+=h
                assert cursor==y2,'native region incomplete'
                assert hashlib.sha256(assembled.tobytes()).hexdigest()==page['roi_rgb_sha256'],'assembled target mismatch'
            checked.append(page['color_file'])
    assert len(checked)==6
    return {'status':'PASS','color_pages_verified':6,'native_numeric_regions_verified':2,'no_ocr':True,'optical_RAW_certified':False}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Pass the acquired source-color directory')
    print(json.dumps(replay(sys.argv[1],json.loads(SNAPSHOT.read_text())),ensure_ascii=False,indent=2))
