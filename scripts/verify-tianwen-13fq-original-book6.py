#!/usr/bin/env python3
"""Verify archived provider payloads and source pixel geometry, without source-count voting."""
import gzip
import hashlib
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
E='docs/research/TIANWEN-13FQ-GK3467-ORIGINAL-BOOK6-JUAN52-ACQUISITION-R1.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(e):
    assert e['schema']=='TIANWEN-13FQ-GK3467-ORIGINAL-BOOK6-JUAN52-ACQUISITION-R1'
    payloads={}
    for x in e['snapshots']:
        p=ROOT/x['path'];assert p.is_relative_to(ROOT/'docs/research/evidence/13fq')
        raw=gzip.decompress(p.read_bytes());assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
        payloads[p.name]=raw
    records=e['acquisition']['records']
    assert len(records)==6 and sum(x['pdf_pages'] for x in records)==e['acquisition']['pdf_pages']==302
    assert sum(x['bytes'] for x in records)==80444834
    for bc,vols in [('GK03467_02',['0001','0002','0003','0004','0005']),('GK03467_04',['0001'])]:
        listing=json.loads(payloads[bc+'-mf.json.gz'])
        assert listing['RESULT']=='SUCCESS'
        assert [x['VOL_NO'] for x in listing['volList']]==vols
        assert all(x['BOOK_CD']==bc and x['IS_PDF']=='Y' for x in listing['volList'])
        assert [x['vol_no'] for x in records if x['book_cd']==bc]==vols
    target=next(x for x in records if x['book_cd']=='GK03467_04')
    assert target['sha256']=='b75009805dae9ccc22797c005bd5f32c7870a192945b503f6b3af3fbf14e1386'
    assert target['pdf_pages']==53 and target['bytes']==12898627
    assert target['url']=='https://kyudb.snu.ac.kr/book/mfPdf.do?book_cd=GK03467_04&vol_no=0001'
    binding=e['original_binding']
    assert (binding['catalog'],binding['digital_volume'],binding['cover_label_book_number'],binding['work_juan'])==('GK03467_04','0001',6,52)
    assert binding['work_title_literal']=='高麗史五十二' and binding['cover_label_total_books']==30
    assert binding['physical_impression_year'] is binding['ancient_folio_number'] is binding['same_physical_copy_as_NIKH_GK5553'] is None
    pages={}
    for p in e['native_pages']:
        raw=(ROOT/p['path']).read_bytes();im=Image.open(ROOT/p['path']).convert('RGB')
        assert sha(raw)==p['embedded_jp2_sha256'] and sha(im.tobytes())==p['rgb_sha256']
        assert im.size==(p['width'],p['height']);pages[p['pdf_page_one_based']]=im
    assert set(pages)=={1,2,14}
    for roi in e['glyph_rois']:
        im=Image.open(ROOT/roi['path']).convert('RGB')
        assert sha((ROOT/roi['path']).read_bytes())==roi['png_sha256']
        assert sha(im.tobytes())==roi['rgb_sha256']==sha(pages[14].crop(roi['box_xyxy']).tobytes())
    assert e['glyph_rois'][1]['literal']=='四分五一七二'
    b=e['bounded_glyph_reading'];assert b['literal']=='五一七二' and b['NLC_D5']=='四分〇一七二'
    assert b['D5_historical_winner'] is b['NLC_D9'] is None
    f=e['boundaries'];assert f['G893_six_controls']=='OPEN' and f['fourfen_to_chudu_historical_units']=='UNPROVEN'
    assert f['D1_D2_D3_D4_D5_D6_D30_historical_units'] is None
    assert not f['full_volume_linewise_collated'] and not f['six_downloads_are_six_independent_editions']
    assert not e['transmission_impact']['edges_supported']
    assert e['impact']['product']=='CLOSED' and e['impact']['algorithm_reopens']==e['impact']['candidate_collapses']==0
    return True
if __name__=='__main__':
    assert check(json.loads((ROOT/E).read_text()))
    print('13FQ_PASS_SOURCE_PAYLOAD_AND_NATIVE_PIXEL_BINDING_BOOK6_WORK52_NO_HISTORIC_WINNER')
