#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D='docs/research/MING-DATONG-YEHUOBIAN-12VI-NCL-YUJIDENG-TWO-COPIES-R1.json'
S='docs/PROJECT-CURRENT-STATE-R1.json'
def validate(d,s):
 if d.get('schema')!='TIANWEN-12VI-NCL-YUJIDENG-MING-COPY-ACCESS-GATE-R1' or d.get('status')!='CATALOGUE_CONFIRMED_GLYPHS_PENDING':raise ValueError('scope')
 a=d['catalog_records']
 if [(x['catalog_id'],x['archive_id'],x['fascicles'],x['frame_cm']) for x in a]!=[('02253','544585',18,'21.2 x 14.8'),('02254','544586',16,'21 x 14.8')]:raise ValueError('item identity')
 if [x['url'] for x in a]!=['https://catalog.digitalarchives.tw/item/00/08/4f/49.html','https://catalog.digitalarchives.tw/item/00/08/4f/4a.html']:raise ValueError('item links')
 for x in a:
  if x['juan11_original_leaf'] is not None or x['target_numeral_winter'] is not None or x['target_numeral_summer'] is not None or x['independent_glyph_votes']!=0:raise ValueError('unearned leaf')
  if x['edition_label']!='明萬曆間(1573-1620)新城王象乾校刊本':raise ValueError('edition')
 p=d['provider_link']
 if p['kind']!='GENERIC_CURRENT_NCL_SEARCH_NO_ITEM_LEAF_LINK' or p['item_issued_url'] is not None:raise ValueError('generic landing page')
 im=d['surrogate_locator']
 if im['downloads_verified'] or im['source_image_sha256'] is not None or im['page_sha256'] is not None or im['imprint_image_verified'] or im['scan_to_copy_crosswalk_verified']:raise ValueError('false image evidence')
 if im['nominal_pages']!=[645,660] or len(im['files'])!=4:raise ValueError('surrogate index')
 if len(d['no_promotion'])!=7 or any(x is not True for x in d['no_promotion'].values()):raise ValueError('firewalls')
 c=d['accounting']; expected={'matrix_rows':222,'audited_rows':222,'repaired_provenance':45,'formal_batches':487,'latest_formal':'12QD','root_sources':647,'extension_sources':43,'total_sources':690,'graph_nodes':252,'graph_edges':238,'product':'CLOSED'}
 for k,v in expected.items():
  if c.get(k)!=v:raise ValueError('snapshot '+k)
 for k in ('new_source_rows','new_graph_nodes','new_graph_edges','new_original_target_pages','new_glyph_votes','algorithm_reopens'):
  if c.get(k)!=0:raise ValueError('false promotion '+k)
 if any(d['transmission_impact'].get(k) for k in ('nodes_added','edges_supported','edges_revised')):raise ValueError('genealogy claim')
 h=s['historical_audit']
 if tuple(map(int,s['schema_version'].split('.')))<(1,565,0) or not any(x.startswith('12VI ') for x in h['current_focus']):raise ValueError('handoff missing')
 if h['row_count']!=222 or h['audited_row_count']!=222 or h['external_source_registry_total_unique_count']<690 or s['invariants']['algorithm_reopen_count']!=0:raise ValueError('state regression')
 return {'status':'PASS','catalogued_copies':2,'source_bound_target_glyph_votes':0}
if __name__=='__main__':
 print(json.dumps(validate(json.loads((R/D).read_text(encoding='utf-8')),json.loads((R/S).read_text(encoding='utf-8'))),ensure_ascii=False))
