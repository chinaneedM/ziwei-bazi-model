#!/usr/bin/env python3
"""13FA NIKH exact-article native GK5553 menu: source label != original glyph."""
import json
from pathlib import Path
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13FA-GORYEOSA-JUAN52-GK05553-POPUP-CATALOG-R1.json";SH="docs/research/TIANWEN-13FA-GORYEOSA-JUAN52-GK05553-POPUP-CATALOG-SOURCE-SHARD-R1.json";M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json";ST="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def get(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def check(d,src,manifest,state,ledger):
 assert d['schema']=='TIANWEN-13FA-GORYEOSA-JUAN52-GK05553-POPUP-CATALOG-R1' and d['issue_id']=='TW-OPEN-0005'
 a=d['source_probe'];n=d['target_native_menu'];c=d['kyujanggak_catalog'];k=d['contrast'];q=d['impact']
 assert a['workflow_run']==40054281719 and a['run_conclusion']=='success' and a['article_http']==200 and a['article_size_bytes']==277246
 assert a['article_html_sha256']=='e2a5a7b1136202c5828e67a187b8572519490444d57d77c8a4cc78cf323ee753'
 assert n['article_id']=='kr_052_0010_0010_0020_0020' and n['matching_entries']==1
 assert n['exact_label']=='규장각한국학연구원 소장본(규귀5553[을해자])'
 assert n['exact_source_emitted_call']=="fnImageViewerPopup('kr_052_0010_0010_0020_0020', 'kr_052_1055')"
 assert n['viewer_item_id']=='kr_052_1055' and n['first_party_label_at_exact_target_article'] is True
 assert n['existing_13EY_other_article_index_only_restriction_now_superseded_for_5553_target_menu'] is True
 assert n['any_KO21634_menu_entry_proven_at_target'] is False and n['onclick_executed'] is False and n['original_image_loaded'] is False
 assert n['viewer_destination_url'] is n['original_image_bytes_sha256'] is n['exact_folio'] is n['original_glyph_reading'] is None
 assert n['actual_printed_historic_copy_verified'] is False and n['work_juan']==52
 assert c['url']=='https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00' and c['book_cd']=='GK05553_00'
 assert c['shelfmark']=='奎貴5553-v.1-46' and c['format']=='乙亥字' and c['physical_books_count']==46 and c['work_juan_count']==139
 assert c['catalog_print_year'] is None and c['notable_replacement_physical_books']==[8,26,29]
 assert c['juan52_to_physical_book'] is c['juan52_to_source_leaf'] is None and c['independent_catalog_glyph_authority'] is False
 assert k['ncl_direct_p74_d5']=='四分〇一七二' and k['krdb_editorial_table_d5']=='四分五一七二'
 assert k['ancient_variant_established'] is False and k['independent_original_glyph_votes']==0
 assert k['ncl_original_d4_d5_d6_complete_tails'] is k['summer_d30_original_historic_numeric'] is k['winter_d16_original_historic_numeric'] is None
 assert k['g893_six_historic_controls']=='OPEN' and k['retired_13EI']=='RETRACTED'
 assert all(z is True for z in d['controls'].values())
 assert d['transmission_impact']['supported_nodes']==d['transmission_impact']['supported_edges']==[]
 assert q['new_firstparty_catalog_sources']==1 and q['registry_total_after']==761 and q['product']=='CLOSED' and q['open_or_blocked_risks']==11
 assert all(q[z]==0 for z in ('new_historic_original_page_images','new_historic_glyph_votes','historical_matrix_rows_added','genealogy_nodes_added','genealogy_edges_added','risk_closures','algorithm_reopens'))
 assert src['schema']=='TIANWEN-13FA-GORYEOSA-JUAN52-GK05553-POPUP-CATALOG-SOURCE-SHARD-R1' and len(src['sources'])==1
 assert src['sources'][0]['url']==c['url'] and src['sources'][0]['physical_glyph_authority'] is False and src['sources'][0]['verification_status']=='BIBLIOGRAPHIC_METADATA_ONLY'
 assert src['sources'][0]['evidence']==E
 assert any(z['path']==SH and z['blob_sha']=='2e6c87ca5b034471bc459531ebaca116b3f90613' and z['source_count']==1 for z in manifest['shards'])
 assert manifest['root_source_count']==647 and manifest['extension_source_count']>=114 and manifest['combined_source_count']==manifest['root_source_count']+manifest['extension_source_count']
 assert state['historical_audit']['external_source_registry_total_unique_count']==manifest['combined_source_count']
 assert state['schema_version']==ledger['binding']['reviewed_state_version']==state['historical_audit']['research_omission_guard']['reviewed_state_version']
 assert any(z.startswith('13FA ') for z in state['historical_audit']['current_focus']) and ledger['binding']['source_focus_count']==len(state['historical_audit']['current_focus'])
 risk=next(z for z in ledger['issues'] if z['id']=='TW-OPEN-0005')
 assert risk['priority']=='P0' and risk['status']=='OPEN' and {E,E.replace('.json','.md'),SH}.issubset(set(risk['source_refs']))
 assert historical_action_view(risk).startswith(ledger['binding']['latest_research_focus_prefix']+' CURRENT ACTION:')
 assert any(z in historical_action_view(risk) for z in ('GK05553_00','GK5553'))
 assert all(z in historical_action_view(risk) for z in ('GK03539_00','GK03579_00','GK03269_00','D1','D2','D3','D4','D5','D6','四分','初度','G893','NULL','13EI'))
 assert any(z.get('revision_id')=='TW-OPEN-0005-13FA-NIKH-EXACT-JUAN52-GK5553-20261024' for z in risk['history'])
 assert ledger['checkpoint_log'][-1]['state_version']==state['schema_version'] and len(ledger['issues'])==11
 return True
if __name__=='__main__':
 assert check(get(E),get(SH),get(M),get(ST),get(L))
 print('13FA_PASS_GK05553_TARGET_MENU_DIRECTLY_PROVEN_WITHOUT_TARGET_IMAGE_GLYPH')
