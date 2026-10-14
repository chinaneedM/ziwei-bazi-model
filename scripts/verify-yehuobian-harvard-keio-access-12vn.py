#!/usr/bin/env python3
"""Validate saved provider metadata without turning it into original-leaf evidence."""
import hashlib,json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STEM='docs/research/MING-DATONG-YEHUOBIAN-12VN-HARVARD-KEIO-OBJECT-ACCESS'
def verify():
 r=json.loads((ROOT/(STEM+'-R1.json')).read_text())
 p=r['probe'];raw=(ROOT/p['google_html_file']).read_bytes();text=html.unescape(raw.decode())
 if len(raw)!=p['google_html_bytes'] or hashlib.sha256(raw).hexdigest()!=p['google_html_sha256']:
  raise ValueError('provider HTML bytes differ from probe attestation')
 for token in ['Keio University','Aug 13, 2010','editions:KEIO10811246205','"is_browsable":false','"can_download_pdf":false']:
  if token not in text:raise ValueError('provider metadata/availability mismatch: '+token)
 for obj in [r['harvard'],r['keio_google']]:
  if obj['original_target_image'] is not None or obj['original_juan20_folio'] is not None:
   raise ValueError('catalog-only lead cannot attest original target leaf')
 if r['harvard']['original_impression_year_verified'] is not None:
  raise ValueError('1827 field and 1869 note do not choose a physical print date')
 if r['keio_google']['keio_opac_item_binding'] is not None or r['keio_google']['historical_juan_mapping'] is not None:
  raise ValueError('Google partner key is not OPAC or juan binding')
 if any(r['acquisition'][x]!=0 for x in ['original_target_images','historical_target_glyph_votes','new_independent_print_witnesses','algorithm_reopens']):
  raise ValueError('unattested original evidence promotion')
 s=json.loads((ROOT/(STEM+'-SOURCE-SHARD-R1.json')).read_text())
 if len(s['sources'])!=2 or any(x['physical_glyph_authority'] or x['verification_status']!='BIBLIOGRAPHIC_METADATA_ONLY' for x in s['sources']):
  raise ValueError('catalogue authority scope changed')
 m=json.loads((ROOT/'docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json').read_text())
 h=json.loads((ROOT/'docs/PROJECT-CURRENT-STATE-R1.json').read_text())['historical_audit']
 if m['combined_source_count']<r['source_delta']['union_after'] or m['combined_source_count']!=m['root_source_count']+m['extension_source_count'] or h['external_source_registry_total_unique_count']!=m['combined_source_count']:
  raise ValueError('present registry/state growth mismatch')
 return {'status':'PASS','new_catalogue_sources':2,'original_target_glyph_votes':0,'html_sha256':p['google_html_sha256']}
if __name__=='__main__':print(json.dumps(verify()))
