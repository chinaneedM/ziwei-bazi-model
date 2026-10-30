#!/usr/bin/env python3
"""13LM exact-source overview/physical-plate boundary and live handoff gate."""
import json
from pathlib import Path
# Historical source text is validated through immutable issue revisions.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
NAME='docs/research/TIANWEN-13LM-NAAJ-P7-COLOR-OVERVIEW-DISCRIMINATOR-TRIAGE-R1.json'
def load():
    return tuple(json.loads((ROOT/p).read_text(encoding='utf-8')) for p in [NAME,'docs/PROJECT-CURRENT-STATE-R1.json','docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json'])
def check(e,s,l):
    assert e['schema']=='TIANWEN-13LM-NAAJ-P7-COLOR-OVERVIEW-DISCRIMINATOR-TRIAGE-R1' and e['no_ocr'] is True
    a=e['source_archive']
    assert a['sha256']=='4dfdafa918d89b8a8c137da295ff3a121d4f59e186289ce716732cf49176814e' and a['bytes']==7779645
    ss=e['sources'];assert [x['holding'] for x in ss]==['281-0037','281-0038']
    assert [x['source_content_id'] for x in ss]==['C100857577900','C100858348000']
    assert [x['acquired_overview_pixels'] for x in ss]==[[3000,2119],[3000,2177]]
    assert [x['source_canvas_pixels'] for x in ss]==[[6300,4450],[6200,4500]]
    assert all(x['overview_is_resized'] is True and x['original_jp2_acquired'] is False for x in ss)
    assert e['overview_alignment']['candidate_matches']==748 and e['overview_alignment']['ransac_inliers']==266
    assert e['overview_alignment']['comparison_level']=='RESIZED_JPEG_OVERVIEW_NOT_NATIVE'
    assert e['overview_alignment']['same_woodblock_adjudicated'] is False
    ts=e['targets'];assert [t['target_id'] for t in ts]==['LEFT_NONCIRCLE_COLUMNS','GUTTER_NONCIRCLE_COLUMNS','RIGHT_NONCIRCLE_COLUMNS']
    for t in ts:
        assert t['native_color_acquisition']=='PENDING' and len(t['positions'])==2
        assert [p['holding'] for p in t['positions']]==['281-0037','281-0038']
        for p in t['positions']:
            src=next(x for x in ss if x['holding']==p['holding'])
            x1,y1,x2,y2=p['overview_xyxy'];X1,Y1,X2,Y2=p['planned_native_canvas_xyxy']
            assert 0<=x1<x2<=src['acquired_overview_pixels'][0] and 0<=y1<y2<=src['acquired_overview_pixels'][1]
            assert 0<=X1<X2<=src['source_canvas_pixels'][0] and 0<=Y1<Y2<=src['source_canvas_pixels'][1]
            assert len(p['overview_crop_rgb_sha256'])==64 and p['native_bounds_derived_by_floor_ceil_scale'] is True
    g=e['adjudication']
    for k in ['unique_accidental_engraving_damage_identified','plate_identity_or_impression_date_proven','source_native_jpeg_fragments_acquired_in_this_batch','ancient_source_negative_proof']:assert g[k] is False,k
    assert g['firstparty_native_acquisition_is_pending'] is True and g['three_source_page_loci_registered']==3
    assert g['new_historical_recensions']==g['independent_physical_copies_added']==g['g893_six_winners']==0
    assert g['original_23897709_retained']=='238977.09' and g['siku_28897709_retained']=='288977.09'
    assert not e['transmission_impact']['edges_supported'] and not e['transmission_impact']['edges_revised']
    assert e['counts']==dict(source_registry=765,matrix_rows=222,matrix_audited=222,graph_nodes=252,graph_edges=238,open_issues=11,algorithm_reopens=0,product='CLOSED')
    assert tuple(map(int,s['schema_version'].split('.')))>=(1,957,0)
    assert any(f.startswith('13LM ') for f in s['historical_audit']['current_focus'])
    assert len(s['historical_audit']['current_focus'])==l['binding']['source_focus_count']
    assert s['historical_audit']['current_focus'][-1].startswith(l['binding']['latest_research_focus_prefix']+' ')
    assert l['binding']['reviewed_state_version']==l['checkpoint_log'][-1]['state_version']==s['schema_version']
    assert all(x['status']!='RESOLVED_WITH_EVIDENCE' for x in l['issues'])
    issue=next(x for x in l['issues'] if x['id']=='TW-OPEN-0005')
    assert issue['status']=='OPEN' and '13LM CURRENT ACTION:' in historical_action_view(issue)
    assert '13LL CURRENT ACTION:' in historical_action_view(issue)
    assert NAME in issue['source_refs']
    assert any(x.get('revision_id')=='TW-OPEN-0005-13LM-P7-OVERVIEW-20261030' for x in issue['history'])
    assert s['invariants']['deterministic_fusion_chart_product_r1']=='CLOSED'
    return {'status':'PASS','p7_candidate_regions':3,'physical_historical_winners':0,'native_original_glyphs_newly_reviewed':0,'algorithm_reopens':0}
if __name__=='__main__':print(json.dumps(check(*load()),ensure_ascii=False))
