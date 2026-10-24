#!/usr/bin/env python3
"""Verify 13EY temporal and work-identity source firewalls."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13EY-GORYEOSA-IMAGE-LINK-LIFECYCLE-DISTINCT-WORK-GATE-R1.json";SH="docs/research/TIANWEN-13EY-GORYEOSA-IMAGE-LINK-LIFECYCLE-DISTINCT-WORK-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json";C="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def check(d,sh,m,s,l):
 assert d['schema']=='TIANWEN-13EY-GORYEOSA-IMAGE-LINK-LIFECYCLE-DISTINCT-WORK-GATE-R1' and d['risk_id']=='TW-OPEN-0005'
 a=d['notice_2023'];b=d['notice_2026'];old=d['prior_institutional_claim'];o=d['indexed_alternative_source_labels'];t=d['target_article']
 assert a['publication_date']=='2023-11-23' and a['notice_list_row']==50 and a['display_title']=='고려사 원문이미지 LINK 변경 안내'
 assert a['body_text_read'] is False and a['old_link_destination'] is a['new_link_destination'] is a['copy_identity_effect'] is a['specific_volume52_article_effect'] is None
 assert old['notice_date']=='2025-02-04' and old['exact_article_image_copy_unbound'] is True
 assert b['publication_date']=='2026-01-29' and b['source_url']=='https://db.history.go.kr/main/notice/noticeView.do?noticeId=84'
 assert b['named_work']=='고려사절요' and b['distinct_from_target_work']=='고려사' and b['same_work_as_target'] is False
 assert b['repairs_2025_goryeosa_link'] is None and b['exact_goryeosa_volume52_image_covered'] is False
 assert o['only_other_article_context'] and o['verified_on_target_article'] is False and o['original_image_acquired'] is False
 assert o['catalog_mapping_for_target'] is None and o['source_metadata_authority']=='UNVERIFIED_INDEX_EXCERPT_ONLY' and o['not_counted_as_separate_physical_witnesses'] is True
 assert t['url']=='https://db.history.go.kr/id/kr_052_0010_0010_0020_0020' and t['work_juan']==52
 assert t['ncl_original_d5']=='四分〇一七二' and t['krdb_digital_transcription_d5']=='四分五一七二'
 assert t['retrieved_direct_ancient_target_page'] is False and all(t[key] is None for key in ('image_sha256','provider_holding_id','physical_book','source_leaf','glyph_winner','historic_numeric_decimal'))
 assert all(d['risk_controls'][key] is True for key in ('different_works_dont_share_provenance_automatically','modern_notice_dates_not_ancient_print_dates','notice_link_change_does_not_prove_copy_switch','digital_label_choices_not_direct_original_glyph_attestation','physical_book_number_not_work_juan'))
 assert d['risk_controls']['shoushi_G893_six_original_controls']=='OPEN' and d['risk_controls']['winter_d16_original_numeric'] is d['risk_controls']['summer_d30_original_numeric'] is None and d['risk_controls']['retired_13EI']=='RETRACTED'
 q=d['impact']; assert q['new_modern_registry_records']==2 and q['product']=='CLOSED' and q['registry_total_after']==760 and q['open_or_blocked_risks']==11
 assert all(q[k]==0 for k in ('physical_original_folios_added','original_glyph_votes','historical_numeric_values_added','risks_closed','new_matrix_rows','new_genealogy_nodes','new_genealogy_edges','algorithms_reopened'))
 assert d['transmission_impact']['supported_nodes']==d['transmission_impact']['supported_edges']==[]
 assert sh['schema']=='TIANWEN-13EY-GORYEOSA-IMAGE-LINK-LIFECYCLE-DISTINCT-WORK-SOURCE-SHARD-R1' and len(sh['sources'])==2
 assert [z['url'] for z in sh['sources']]==[a['source_url'],b['source_url']]
 assert all(z['physical_glyph_authority'] is False and z['verification_status']=='BIBLIOGRAPHIC_METADATA_ONLY' and z['evidence']==P for z in sh['sources'])
 assert any(z['path']==SH and z['blob_sha']=='cd806489bdec290a887c0e454a9027c02bab9e42' and z['source_count']==2 for z in m['shards'])
 assert m['root_source_count']==647 and m['extension_source_count']>=113 and m['combined_source_count']==m['root_source_count']+m['extension_source_count']
 assert s['historical_audit']['external_source_registry_total_unique_count']==m['combined_source_count']
 assert s['schema_version']==l['binding']['reviewed_state_version']==s['historical_audit']['research_omission_guard']['reviewed_state_version']
 assert any(z.startswith('13EY ') for z in s['historical_audit']['current_focus']) and l['binding']['source_focus_count']==len(s['historical_audit']['current_focus'])
 issue=next(z for z in l['issues'] if z['id']=='TW-OPEN-0005')
 assert issue['priority']=='P0' and issue['status']=='OPEN' and {P,P.replace('.json','.md'),SH}.issubset(set(issue['source_refs']))
 assert issue['next_action'].startswith(l['binding']['latest_research_focus_prefix']+' CURRENT ACTION:')
 assert all(z in issue['next_action'] for z in ('GK03539_00','GK03579_00','GK03269_00','D1','D2','D3','D4','D5','D6','四分','初度','G893','NULL','13EI'))
 assert any(z.get('revision_id')=='TW-OPEN-0005-13EY-GORYEOSA-IMAGE-LINK-CHRONOLOGY-20261024' for z in issue['history'])
 assert l['checkpoint_log'][-1]['state_version']==s['schema_version'] and len(l['issues'])==11
 return True
if __name__=='__main__':
 assert check(get(P),get(SH),get(M),get(C),get(L))
 print('13EY_PASS_IMAGE_LINK_LIFECYCLE_SEPARATE_WORK_UNBOUND_ORIGINAL_FOLIO')
