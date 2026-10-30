#!/usr/bin/env python3
"""13LJ first-party color recovery: route success never proves optical RAW/edition."""
import hashlib,json
from pathlib import Path
# Verify historical action text through append-only revisions, not the current instruction.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E='docs/research/TIANWEN-13LJ-NAAJ-FIRSTPARTY-COLOR-RECOVERY-R1.json'
A='docs/research/TIANWEN-13LJ-NAAJ-FIRSTPARTY-COLOR-ACQUISITION-SNAPSHOT-R1.json'
def load():
    return tuple(json.loads((ROOT/p).read_text()) for p in [E,A,'docs/PROJECT-CURRENT-STATE-R1.json','docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json'])
def check(e,a,s,l):
    assert e['schema']=='TIANWEN-13LJ-NAAJ-FIRSTPARTY-COLOR-RECOVERY-R1'
    assert e['issue_id']=='TW-OPEN-0005' and e['no_ocr'] is True
    assert e['source_acquisition_snapshot']==A
    assert e['source_acquisition_snapshot_sha256']=='63978aa46ad0f86cede3044d96deed37e3caadbbb142f325989421032f80ab06'
    assert hashlib.sha256((json.dumps(a,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()==e['source_acquisition_snapshot_sha256'],'acquisition content changed'
    assert a['no_ocr'] is True and a['ancient_impression_proven'] is False and a['optical_raw_proven'] is False
    assert len(a['sources'])==2
    for src,holding,item,dims,roi in zip(a['sources'],['281-0037','281-0038'],[4034620,3637417],[[6300,4450],[6200,4500]],[[3277,472,3566,3955],[3383,499,3738,4044]]):
        assert src['holding']==holding and src['viewer_id']==item and 'error' not in src
        assert src['viewer']['status']==src['manifest']['status']==200
        assert [p['page'] for p in src['pages']]==[2,6,7]
        for p in src['pages']:
            assert p['jp2_acquired'] is False and p['jp2_download_status']==400
            assert p['color_download']['status']==200 and p['color_download']['content_type'].startswith('image/jpeg')
            assert p['source_canvas_pixels']==dims and p['color_pixels'][0]==3000
            assert p['color_pixels']!=dims,'full/max overview must not be relabeled native full image'
            assert p['color_download']['url'].endswith('/full/max/0/native.jpg')
            assert len(p['color_download']['sha256'])==len(p['color_rgb_sha256'])==64
            assert p['human_reading']=='PENDING','immutable acquisition snapshot must retain its original review grade'
        p=src['pages'][1];assert p['roi_xyxy']==roi
        x1,y1,x2,y2=roi;cursor=y1
        assert len(p['native_region_parts'])==2
        for part in p['native_region_parts']:
            x,y,w,h=part['region_xywh'];assert [x,y,w]==[x1,cursor,x2-x1] and h==min(2000,y2-y)
            assert part['download']['status']==200
            assert part['download']['url'].endswith(f'/{x},{y},{w},{h}/{w},/0/native.jpg')
            assert len(part['download']['sha256'])==len(part['rgb_sha256'])==64
            cursor+=h
        assert cursor==y2
    assert len(e['manual_numeric_collations'])==2
    for review,src in zip(e['manual_numeric_collations'],a['sources']):
        p=src['pages'][1]
        assert review['holding']==src['holding'] and review['page']==6
        assert review['roi_rgb_sha256']==p['roi_rgb_sha256'] and review['roi_xyxy']==p['roi_xyxy']
        assert review['literal']=='有閏加二十三萬八九七七○九' and review['numeric']=='238977.09'
        assert review['source_medium']=='FIRST_PARTY_IIIF_COLOR_JPEG_REGION_NOT_PDF_JBIG2'
    firewall=e['interpretation']
    for k in ['original_jp2_downloaded','unprocessed_optical_RAW_proven','jpeg2000_lossless_proven','same_woodblock_proven','dated_1739_impression_proven','jbig2_wrong_symbol_substitution_proven']:
        assert firewall[k] is False,k
    assert firewall['source_full_max_overview_is_resized'] is True
    assert firewall['independent_historical_recensions_added']==firewall['g893_six_numeric_winners_added']==0
    assert firewall['siku_original_literal_retained']=='288977.09'
    assert not e['transmission_impact']['edges_supported'] and not e['transmission_impact']['edges_revised']
    b=l['binding'];focus=s['historical_audit']['current_focus']
    assert any(x.startswith('13LJ ') for x in focus)
    assert b['source_focus_count']==len(focus) and b['latest_research_focus_prefix']==focus[-1].split()[0]
    assert b['reviewed_state_version']==s['schema_version']==s['historical_audit']['research_omission_guard']['reviewed_state_version']==l['checkpoint_log'][-1]['state_version']
    issue=next(x for x in l['issues'] if x['id']=='TW-OPEN-0005')
    assert issue['status']=='OPEN' and issue['priority']=='P0'
    assert historical_action_view(issue).startswith(b['latest_research_focus_prefix']+' CURRENT ACTION:')
    assert '13LI CURRENT ACTION:' in historical_action_view(issue) and E in issue['source_refs'] and A in issue['source_refs']
    assert any(x.get('revision_id')=='TW-OPEN-0005-13LJ-FIRSTPARTY-COLOR-20261030' for x in issue['history'])
    assert s['invariants']['deterministic_fusion_chart_product_r1']=='CLOSED' and len(l['issues'])==11
    return {'status':'PASS','firstparty_color_pages':6,'native_numeric_regions':2,'new_historical_recensions':0,'product':'CLOSED'}
if __name__=='__main__':
    e,a,s,l=load()
    assert hashlib.sha256((ROOT/A).read_bytes()).hexdigest()==e['source_acquisition_snapshot_sha256'],'immutable acquisition snapshot changed'
    print(json.dumps(check(e,a,s,l),ensure_ascii=False))
