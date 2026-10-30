#!/usr/bin/env python3
"""Rebuild p7 RESIZED overview target crops from the immutable 13LJ first-party ZIP.
No OCR, source-native glyph review, woodblock adjudication or historic votes.
"""
import hashlib,io,json,sys,zipfile
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13LM-NAAJ-P7-COLOR-OVERVIEW-DISCRIMINATOR-TRIAGE-R1.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def replay(zip_path,out_dir):
    e=json.loads(E.read_text(encoding='utf-8'))
    raw=Path(zip_path).read_bytes()
    assert sha(raw)==e['source_archive']['sha256'] and len(raw)==e['source_archive']['bytes'],'wrong source archive'
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    images={}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for src in e['sources']:
            hold=src['holding'];b=z.read(hold+'-p007-iiif.jpg')
            assert sha(b)==src['overview_jpeg_sha256'],'wrong p7 JPEG'
            im=Image.open(io.BytesIO(b)).convert('RGB')
            assert list(im.size)==src['acquired_overview_pixels'],'wrong overview size'
            assert sha(im.tobytes())==src['overview_rgb_sha256'],'wrong decoded source RGB'
            images[hold]=im
    board=Image.new('RGB',(1380,1260),'#f5f4f0');d=ImageDraw.Draw(board);records=[]
    for col,target in enumerate(e['targets']):
        row={'target_id':target['target_id'],'historical_damage_proven':False,'controls':[]}
        for j,loc in enumerate(target['positions']):
            hold=loc['holding'];xyxy=loc['overview_xyxy'];im=images[hold]
            x1,y1,x2,y2=xyxy
            assert 0<=x1<x2<=im.width and 0<=y1<y2<=im.height
            crop=im.crop((x1,y1,x2,y2));assert sha(crop.tobytes())==loc['overview_crop_rgb_sha256'],'source ROI drift'
            assert crop.width<=440 and crop.height<=555
            file=hold+'-'+target['target_id'].lower()+'.png'
            crop.save(out/file)
            x=col*460+10;y=j*630+55;board.paste(crop,(x,y))
            d.text((x,y-24),hold+' '+target['target_id'],fill='black')
            row['controls'].append({'holding':hold,'overview_xyxy':xyxy,'rgb_sha256':loc['overview_crop_rgb_sha256'],'file':file})
        records.append(row)
    board.save(out/'p7-paired-overview-controls.png')
    data={'schema':'TIANWEN-13LM-OVERVIEW-REPLAY','no_ocr':True,'native_source_glyph_review':False,'same_woodblock_proven':False,'historical_winners_added':0,'targets':records}
    (out/'replay.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: replay FILE_13LJ_ZIP OUTPUT_DIR')
    print(json.dumps(replay(sys.argv[1],sys.argv[2]),ensure_ascii=False))
