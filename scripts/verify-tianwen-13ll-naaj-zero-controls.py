#!/usr/bin/env python3
"""13LL exact two-locus evidence and digital/physical interpretation firewall."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D='docs/research/'
E=D+'TIANWEN-13LL-NAAJ-SAME-PAGE-ZERO-COLOR-MASK-COLLATION-R1.json'
A=D+'TIANWEN-13LL-NAAJ-SECOND-ZERO-COLOR-ACQUISITION-SNAPSHOT-R1.json'
R=D+'TIANWEN-13LL-SAME-PAGE-ZERO-COLOR-MASK-REPLAY-SNAPSHOT-R1.json'
K=D+'TIANWEN-13LK-EXACT-HEAD-SOURCE-PHOTO-TRANSPORT-RECOVERY-R1.json'
def digest(d):return hashlib.sha256((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
def load():return tuple(json.loads((ROOT/p).read_text()) for p in [E,A,R,'docs/PROJECT-CURRENT-STATE-R1.json','docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json',K])
def check(e,a,r,s,l,k):
    assert e['schema']=='TIANWEN-13LL-NAAJ-SAME-PAGE-ZERO-COLOR-MASK-COLLATION-R1' and e['issue_id']=='TW-OPEN-0005' and e['no_ocr'] is True
    assert e['acquisition_snapshot']==A and e['replay_snapshot']==R
    assert e['acquisition_snapshot_sha256']==digest(a)=='a26c855128c0ad562803eb9902d3f1c5bfa82b2d8fa940668353c0891c86f8cd'
    assert e['replay_snapshot_sha256']==digest(r)=='97a68e4bf7954f1803252eef41a46487ab975d5f5aad06d7f37b9656d55fb361'
    assert e['prior_numeric_parent_snapshot_sha256']=='63978aa46ad0f86cede3044d96deed37e3caadbbb142f325989421032f80ab06'
    assert a['human_reading']=='PENDING' and a['same_woodblock_proven'] is False and a['new_recensions']==0
    assert [c['holding'] for c in a['controls']]==['281-0037','281-0038']
    assert r['no_ocr'] is True and r['resized'] is False and r['physical_damage_inference'] is False and r['connectivity']==8 and r['component_min_area']==8
    assert len(e['direct_visual_reviews'])==len(r['glyphs'])==4
    for review,g in zip(e['direct_visual_reviews'],r['glyphs']):
        for key in ['holding','page','tag','glyph_xyxy','color_glyph_rgb_sha256','mask_glyph_gray_sha256']:assert review[key]==g[key],key
        assert review['visible_glyph']=='○' and review['historical_cause_of_gap']=='UNRESOLVED' and review['new_physical_witness_increment']==0
        assert review['grade']=='DIRECT_NATIVE_COORDINATE_COLOR_AND_MASK_VISUAL_COMPARISON_NO_OCR'
    x=e['interpretation']
    for key in ['numeric_contexts_are_different_registered_source_loci','thin_ring_238977_context_and_thicker_same_page_ring_distinct','corresponding_loci_between_holdings_visually_compatible','compatibility_is_not_unique_accidental_damage_proof','component_count_is_not_historical_break_count']:assert x[key] is True,key
    for key in ['cause_of_each_gap_adjudicated','wrong_jbig2_symbol_substitution_proven','same_woodblock_proven','exact_impression_year_proven','unprocessed_optical_RAW_acquired','second_control_decimal_value_inferred']:assert x[key] is False,key
    assert x['same_page_control_mask_component_counts']==[len(r['glyphs'][i]['mask_component_areas_ge8']) for i in [1,3]]==[3,2]
    assert x['new_independent_recensions']==x['new_historical_g893_six_winners']==0
    assert x['prior_original_numeric_literal_retained']=='238977.09' and x['siku_original_numeric_literal_retained']=='288977.09'
    assert x['13LH_shared_plate_candidate']=='POSSIBLE_RETAINED_NOT_CONFIRMED'
    assert not e['transmission_impact']['edges_supported'] and not e['transmission_impact']['edges_revised']
    assert e['method']['native_coordinates_only'] is True and e['method']['resized'] is False
    assert k['failed_run_id']==41043922884 and k['recovery_run_id']==41044890867 and k['recovery_status']=='success'
    assert k['observed_bytes']==247816 and k['observed_sha256']=='63a45c4dc223e360267659acd2a6900767aaf10d82db1bf43724463edb8ddc0a'
    assert k['retry_policy']['maximum_attempts']==3 and k['retry_policy']['source_hash_gate_unchanged'] is True and k['historical_claims_changed'] is False
    b=l['binding'];f=s['historical_audit']['current_focus'];assert any(t.startswith('13LK ') for t in f) and any(t.startswith('13LL ') for t in f)
    assert len(f)==b['source_focus_count'] and f[-1].split()[0]==b['latest_research_focus_prefix']
    assert s['schema_version']==b['reviewed_state_version']==s['historical_audit']['research_omission_guard']['reviewed_state_version']==l['checkpoint_log'][-1]['state_version']
    i=next(x for x in l['issues'] if x['id']=='TW-OPEN-0005')
    assert i['status']=='OPEN' and i['next_action'].startswith(b['latest_research_focus_prefix']+' CURRENT ACTION:') and '13LJ CURRENT ACTION:' in i['next_action']
    assert all(p in i['source_refs'] for p in [E,A,R,K])
    assert any(x.get('revision_id')=='TW-OPEN-0005-13LL-ZERO-COLOR-MASK-20261030' for x in i['history'])
    assert s['invariants']['deterministic_fusion_chart_product_r1']=='CLOSED'
    return {'status':'PASS','paired_glyphs':4,'new_native_color_controls':2,'new_historical_recensions':0,'same_woodblock_proven':False,'transport_recovered':True}
if __name__=='__main__':print(json.dumps(check(*load()),ensure_ascii=False))
