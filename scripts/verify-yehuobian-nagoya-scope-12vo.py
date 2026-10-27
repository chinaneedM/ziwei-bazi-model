#!/usr/bin/env python3
"""Keep acquired scholarship, selected apparatus and ancient folios separate."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD='docs/research/MING-DATONG-YEHUOBIAN-12VO-NAGOYA-FULLTEXT-AND-COLLATION-SCOPE-R1.json'
def validate(r):
 def require(c,msg):
  if not c:raise ValueError(msg)
 require([f['year'] for f in r['source_files']]==[2019,2020,2021],'source years')
 require([f['pdf_pages'] for f in r['source_files']]==[24,20,12],'file pagination')
 require(sum(len(f['manual_reviewed_pdf_pages']) for f in r['source_files'])==r['capture']['selected_scholarly_pages_visually_reviewed']==6,'selected review scope')
 a=r['apparatus_scope']
 require(a['inoue2020']['scope']=='THEMATIC_JUAN_1_TO_3_PLUS_PARATEXT' and a['inoue2021']['scope']=='THEMATIC_JUAN_4_TO_6','apparatus range')
 require(a['inoue2020']['target_juan20_covered'] is False and a['inoue2021']['target_juan20_covered'] is False,'unattested juan20 promotion')
 require(a['inoue2020']['base']=='ZHONGHUA_1959_FIRST_EDITION_1980_SECOND_IMPRESSION_USED_BY_SCHOLAR','base impression mismatch')
 require(a['selection_policy']['exhaustive_variant_apparatus'] is False and a['selection_policy']['unlisted_variant_proves_agreement'] is False,'selective apparatus cannot prove equality')
 require(r['inoue2019_selected_page_control']['full_article_negative_search_claim_allowed'] is False,'image-only nonhit forbidden')
 labels=r['scholarly_copy_labels']
 require(all(labels[k]=='UNPROVEN' for k in ['A_equals_NCL02260','B_equals_NCL02261','C_equals_IHP174009']),'copy identity shortcut')
 require(all(r['accounting'][k]==0 for k in ['new_ancient_target_images','new_target_glyph_votes','new_graph_nodes','new_graph_edges','algorithm_reopens']),'scholarship promoted to ancient vote')
 require(r['source_delta']['new_2021_scholarly_row']==1 and r['source_delta']['existing_2019_2020_rows_reused']==2,'source deduplication')
 return {'status':'PASS','acquired_scholarly_pdfs':3,'new_ancient_target_glyph_votes':0}
def verify(artifact_root=None):
 r=json.loads((ROOT/RECORD).read_text());out=validate(r)
 out['binary_rehashed_this_run']=False
 if artifact_root:
  for f in r['source_files']:
   p=artifact_root/f"inoue{f['year']}.pdf"
   with p.open('rb') as handle:sha=hashlib.file_digest(handle,'sha256').hexdigest()
   if sha!=f['sha256'] or p.stat().st_size!=f['bytes']:raise ValueError('scholarly source binary mismatch')
  out['binary_rehashed_this_run']=True
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--artifact-root',type=Path);args=p.parse_args();print(json.dumps(verify(args.artifact_root)))
