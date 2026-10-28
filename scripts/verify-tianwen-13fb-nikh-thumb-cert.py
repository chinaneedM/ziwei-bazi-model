#!/usr/bin/env python3
"""13FB source-emitted 23-image viewer + bounded two-thumbnail positive control."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13FB-NIKH-JUAN52-SOURCE-EMITTED-VIEWER-THUMBNAIL-ATTESTATION-R1.json";C="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def get(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def check(x,s,l,m):
 assert x['schema']=='TIANWEN-13FB-NIKH-JUAN52-SOURCE-EMITTED-VIEWER-THUMBNAIL-ATTESTATION-R1' and x['issue_id']=='TW-OPEN-0005'
 z=x['source_provenance'];v=x['native_viewer'];a=x['bounded_thumbnail_requests'];f=x['numerical_and_philological_firewall'];i=x['impact']
 assert z['probe_run']==40055193124 and z['probe_job']==120756532311 and z['probe_conclusion']=='success' and z['probe_artifact_id']==12545157143
 assert z['article_html_sha256']=='e2a5a7b1136202c5828e67a187b8572519490444d57d77c8a4cc78cf323ee753'
 assert z['verified_js_sha256']=='79c748e9ee7755175dc42e945f87cff617130b60443f945beed9a800aeaa5066'
 assert z['this_run_viewer_proof_kind']=='THIS_RUN_SCRIPT_DIRECT' and z['viewer_http']==200 and z['viewer_html_bytes']==22767
 assert z['viewer_html_sha256']=='25ecd6a4672bdaa29d188409c6c10e1c7050cc7481b54c6f9cf3fb1417f28342'
 assert z['script_derived_viewer_url']=='https://db.history.go.kr/common/imageViewer.do?levelId=kr_052_0010_0010_0020_0020&begin=kr_052_1055'
 assert v['source_emitted_image_count']==v['source_emitted_thumbnails_count']==23
 assert v['source_emitted_first_file']=='kr/052/kr_052_1055.jpg' and v['source_emitted_last_file']=='kr/052/kr_052_1077.jpg'
 assert v['linked_snu_catalog']=='GK05553_00' and v['work_juan']==52 and v['physical_book_number'] is v['source_original_leaf_number'] is None
 assert v['full_resolution_original_image_acquired'] is False and v['thumbnail_not_sufficient_for_original_glyph_adjudication']
 assert v['image_names_are_modern_viewer_sequential_numbers_not_original_leaf_ids'] and v['physical_copy_exact_image_edition_confirmed'] is False
 assert [r['sequence'] for r in a]==[1,2,3] and [r['image_name'] for r in a]==['kr_052_1055.jpg','kr_052_1056.jpg','kr_052_1057.jpg']
 assert [r['status'] for r in a]==['PUBLIC_THUMBNAIL_CAPTURED','TRANSPORT_ERROR','PUBLIC_THUMBNAIL_CAPTURED']
 assert [r['http'] for r in a]==[200,None,200] and [r['bytes'] for r in a]==[2134,0,2217]
 assert [r['sha256'] for r in a]==['712067426574f5496d39de24a619a6f930bb059fb58c91e40941f5984d1d51d3',None,'1351f2cf029bd01ba2915c77d2b16a10eb47415df987e8fc0c9671f09f9be26a']
 assert [r['jpeg_magic_verified'] for r in a]==[True,False,True] and all(r['original_full_resolution_glyph_grade'] is False for r in a)
 assert a[1]['error_type']=='RemoteDisconnected' and all(r['official_data_src'].endswith('/kr/052/'+r['image_name']) for r in a)
 assert f['ncl_direct_original_p74_day5_visual']=='四分〇一七二' and f['krdb_modern_han_text_day5']=='四分五一七二'
 assert f['second_edition_original_reading_added'] is False and f['precise_historic_numeric_D5'] is f['original_solar_D30_numeric'] is f['original_winter_D16_numeric'] is f['missing_D4_D5_D6_original_complete_numeric_tails'] is None
 assert f['original_six_G893_numeric_targets']=='OPEN' and f['old_13EI_false_source_claim']=='RETRACTED'
 assert all(v is True for v in x['limitations'].values())
 assert i['source_registry_records_added']==0 and i['source_registry_current']==761 and i['proven_modern_viewer_html_pages_added']==1 and i['successfully_captured_jpeg_thumbnail_files']==2 and i['failed_thumbnail_requests']==1
 assert all(i[k]==0 for k in ('source_original_high_resolution_folio_images_added','original_historic_glyph_votes_added','historical_matrix_rows_changed','genealogy_nodes_added','genealogy_edges_added','algorithm_reopens','research_risk_closures'))
 assert i['open_or_blocked_issues']==11 and i['product']=='CLOSED' and x['transmission_impact']['new_supported_edges']==[]
 # Historical 13FB source_count is an immutable snapshot, not the live manifest total.
 assert i['source_registry_current']==761
 assert m['root_source_count']==647 and m['extension_source_count']>=114
 assert m['combined_source_count']==m['root_source_count']+m['extension_source_count']
 assert m['combined_source_count']>=i['source_registry_current']
 assert s['historical_audit']['external_source_registry_total_unique_count']==m['combined_source_count'] and s['schema_version']==l['binding']['reviewed_state_version']==s['historical_audit']['research_omission_guard']['reviewed_state_version']
 assert any(z.startswith('13FB ') for z in s['historical_audit']['current_focus']) and l['binding']['source_focus_count']==len(s['historical_audit']['current_focus'])
 risk=next(z for z in l['issues'] if z['id']=='TW-OPEN-0005')
 assert risk['priority']=='P0' and risk['status']=='OPEN' and {P,P.replace('.json','.md')}.issubset(set(risk['source_refs']))
 assert risk['next_action'].startswith(l['binding']['latest_research_focus_prefix']+' CURRENT ACTION:')
 assert any(z in risk['next_action'] for z in ('GK05553_00','GK5553'))
 assert all(z in risk['next_action'] for z in ('GK03539_00','GK03579_00','GK03269_00','D1','D2','D3','D4','D5','D6','四分','初度','G893','NULL','13EI'))
 assert any(z.get('revision_id')=='TW-OPEN-0005-13FB-JUAN52-23FRAMES-TWO-THUMBS-20261024' for z in risk['history'])
 assert l['checkpoint_log'][-1]['state_version']==s['schema_version'] and len(l['issues'])==11
 return True
if __name__=='__main__':
 assert check(get(P),get(C),get(L),get(M))
 print('13FB_PASS_OFFICIAL_23_VIEWER_FRAMES_TWO_DERIVATIVE_JPEG_THUMBS_ZERO_ANCIENT_GLYPH_VOTES')
