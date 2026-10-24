#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13EX-NIKH-2025-GORYEOSA-SNU-IMAGE-LINK-R1.json";H="docs/research/TIANWEN-13EX-NIKH-2025-GORYEOSA-SNU-IMAGE-LINK-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json";C="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(x):return json.loads((R/x).read_text(encoding='utf-8'))
def check(a,b,m,c,l):
 assert a['schema']=='TIANWEN-13EX-NIKH-2025-GORYEOSA-SNU-IMAGE-LINK-R1' and a['issue_id']=='TW-OPEN-0005'
 q=a['official'];u=a['scope'];z=a['context'];v=a['impact']
 assert q['notice_url']=='https://db.history.go.kr/main/notice/noticeView.do?noticeId=78' and q['notice_date']=='2025-02-04'
 assert q['literal']=='이미지 연계 : 규장각한국학연구원 원문 이미지' and q['work']=='고려사'
 assert u['institutional_link_positive'] is True and u['exact_article_image_acquired'] is False
 assert u['catalog_copy_id'] is u['physical_book_number'] is u['source_leaf_number'] is u['source_image_sha256'] is None
 assert u['matching_GK03539_or_GK03579_copy_proven'] is False and u['not_a_new_ancient_physical_witness'] is True
 assert z['ncl_original_d5']=='四分〇一七二' and z['krdb_edited_d5']=='四分五一七二'
 assert z['d4_d5_d6_full_original_tails'] is z['summer_d30_numeric'] is z['winter_d16_numeric'] is z['hist_numeric_normalization'] is None
 assert z['g893_six_controls']=='OPEN' and z['retired_13EI']=='RETRACTED'
 assert v['modern_metadata_sources_added']==1 and all(v[k]==0 for k in ('ancient_folios_acquired','physical_glyph_votes','new_matrix_rows','new_genealogy_nodes','new_genealogy_edges','risks_closed','algorithms_reopened'))
 assert v['product']=='CLOSED' and v['registry_sources_after']==758 and v['open_risks']==11
 assert a['genealogy']['supported_new_edges']==[] and b['schema']=='TIANWEN-13EX-NIKH-2025-GORYEOSA-SNU-IMAGE-LINK-SOURCE-SHARD-R1'
 assert len(b['sources'])==1 and b['sources'][0]['url']==q['notice_url'] and b['sources'][0]['physical_glyph_authority'] is False and b['sources'][0]['verification_status']=='BIBLIOGRAPHIC_METADATA_ONLY'
 assert any(t['path']==H and t['blob_sha']=='54ddc7a607492019ba8dd272ebacbb0078fcdf30' and t['source_count']==1 for t in m['shards'])
 assert m['combined_source_count']>=758 and m['root_source_count']==647 and m['combined_source_count']==m['root_source_count']+m['extension_source_count']
 assert c['historical_audit']['external_source_registry_total_unique_count']==m['combined_source_count']
 assert c['schema_version']==l['binding']['reviewed_state_version']==c['historical_audit']['research_omission_guard']['reviewed_state_version']
 assert any(x.startswith('13EX ') for x in c['historical_audit']['current_focus'])
 assert l['binding']['source_focus_count']==len(c['historical_audit']['current_focus'])
 i=next(x for x in l['issues'] if x['id']=='TW-OPEN-0005')
 assert i['priority']=='P0' and i['status']=='OPEN' and {P,P.replace('.json','.md'),H}.issubset(set(i['source_refs']))
 assert i['next_action'].startswith(l['binding']['latest_research_focus_prefix']+' CURRENT ACTION:')
 assert all(x in i['next_action'] for x in ('GK03539_00','GK03579_00','GK03269_00','D1','D2','D3','D4','D5','D6','四分','初度','G893','NULL','13EI'))
 assert any(x.get('revision_id')=='TW-OPEN-0005-13EX-NIKH-2025-KYUJANGGAK-BRIDGE-20261024' for x in i['history'])
 assert any(x.get('id')=='OMISSIONS-13EX-NIKH2025-KYU-IMAGE-PROVIDER-20261024' for x in l['checkpoint_log']) and len(l['issues'])==11
 return True
if __name__=='__main__':
 assert check(get(P),get(H),get(M),get(C),get(L))
 print('13EX_PASS_FIRSTPARTY_INSTITUTIONAL_PROVIDER_LINK_WITHOUT_ANCIENT_GLYPH')
