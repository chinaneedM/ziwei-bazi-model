#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13E-GORYEOSA-NOH2015-CRITICAL-EDITION-PROVENANCE-R1.json"
S="docs/research/TIANWEN-13E-GORYEOSA-NOH2015-SNU2014-SOURCE-SHARD-R1.json"
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def verify():
 d=read(E); sh=read(S); st=read("docs/PROJECT-CURRENT-STATE-R1.json"); l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"); m=read("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
 assert d['conference']['author']=='노명호 / Noh Myeong-ho'
 assert d['conference']['pdf_pages_zero_based']==[103,104] and d['conference']['printed_pages']==[94,95]
 assert d['conference']['ancient_work52_D16_D18_original_glyphs_read'] is False
 assert d['institution']['project_id']=='KIKS-2014-452-23205' and d['institution']['full_final_report_read'] is False
 b=d['boundaries']
 assert b['conference_and_project_not_independent_scholar_vote'] is True and b['work52_exact_book'] is None and b['direct_original_woodblock_page_sha256'] is None
 assert b['new_original_glyph_votes']==b['new_independent_physical_witnesses']==b['new_transmission_edges']==b['algorithm_reopens']==0
 assert sh['schema']=='TIANWEN-13E-GORYEOSA-NOH2015-KYUJANGGAK2014-SOURCE-SHARD-R1' and len(sh['sources'])==2
 assert all(not x['physical_glyph_authority'] and x['verification_status']=='BIBLIOGRAPHIC_METADATA_ONLY' for x in sh['sources'])
 assert any(x['path']==S and x['source_count']==2 for x in m['shards'])
 assert m['combined_source_count']==st['historical_audit']['external_source_registry_total_unique_count']>=726 and m['extension_source_count']>=79
 assert st['schema_version']==l['binding']['reviewed_state_version']==st['historical_audit']['research_omission_guard']['reviewed_state_version']
 assert l['binding']['latest_research_focus_prefix']==st['historical_audit']['current_focus'][-1].split(' ',1)[0]
 assert l['binding']['source_focus_count']==len(st['historical_audit']['current_focus'])
 assert any(x.startswith('13E ') for x in st['historical_audit']['current_focus'])
 i=next(i for i in l['issues'] if i['id']=='TW-OPEN-0005')
 assert i['status']=='OPEN' and all(x in i['source_refs'] for x in (E,E.replace('.json','.md'),S))
 assert len(l['issues'])==11 and all(i['status']!='RESOLVED_WITH_EVIDENCE' for i in l['issues'])
 assert l['checkpoint_log'][-1]['state_version']==st['schema_version']
 assert set(l['checkpoint_log'][-1]['reviewed_issue_ids'])=={i['id'] for i in l['issues']}
 assert st['invariants']['deterministic_fusion_chart_product_r1']=='CLOSED' and st['invariants']['algorithm_reopen_count']==0
 return {'status':'PASS','sources':m['combined_source_count'],'target_originals':0}
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False))
