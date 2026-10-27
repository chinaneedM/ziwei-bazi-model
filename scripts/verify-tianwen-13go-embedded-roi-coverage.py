#!/usr/bin/env python3
"""13GO: ratio-only coverage audit; never mistake a proposal for a source glyph."""
import json
from pathlib import Path
from math import floor,ceil
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13GO-NCL03130-EMBEDDED-ROI-COVERAGE-AUDIT-R1.json'
def inside(outer,inner):
 return outer[0]<=inner[0] and outer[1]<=inner[1] and outer[2]>=inner[2] and outer[3]>=inner[3]
def projected(rect,old_size,new_size):
 return [floor(rect[0]*new_size[0]/old_size[0]),floor(rect[1]*new_size[1]/old_size[1]),ceil(rect[2]*new_size[0]/old_size[0]),ceil(rect[3]*new_size[1]/old_size[1])]
def check(e):
 assert e['grade']=='REPRODUCIBLE_DIMENSION_RATIO_CROP_COVERAGE_CHECK_NOT_DIRECT_GLYPH_COLLATION'
 assert e['pixel_registration_verified'] is False
 assert e['source']['new_physical_witnesses']==e['source']['new_original_glyphs']==0
 gn=json.loads((ROOT/e['inputs']['prior_gn']).read_text(encoding='utf8'))
 gd=json.loads((ROOT/e['inputs']['prior_gd']).read_text(encoding='utf8'))
 fv=json.loads((ROOT/e['inputs']['prior_fv']).read_text(encoding='utf8'))
 assert e['source']['pdf_sha256']==gn['source']['sha256']==fv['source']['source_pdf_sha256']
 assert e['source']['source_pdf_is_same_as_13gn'] is True
 assert [x['target'] for x in e['cases']]==['D9','D14','D30']
 for row in e['cases']:
  page=row['page'];target=row['target'];scan=next(p for p in gn['pages'] if p['page']==page)
  old=scan['previous_render']['size'];new=scan['embedded']['size']
  saved=next(q['xyxy'] for q in scan['review_rois'] if q['target']==target)
  assert row['saved_embedded_review_xyxy']==saved
  if target in ('D9','D14'):
   original=next(x for x in gd['non_adjudicated_original_scopes'] if x['day']==int(target[1:]))
   assert row['prior_render_union_xyxy']==original['candidate_roi_xyxy']
   assert page==74
  else:
   strips=[x['rect'] for x in fv['regions'] if x['label'] in ('SEAM_ADJACENT_CANDIDATE_STRIP','NEXT_CANDIDATE_STRIP')]
   assert len(strips)==2 and page==76
   union=[min(x[0] for x in strips),min(x[1] for x in strips),max(x[2] for x in strips),max(x[3] for x in strips)]
   assert row['prior_render_union_xyxy']==union
  calc=projected(row['prior_render_union_xyxy'],old,new)
  assert row['ratio_projected_xyxy']==calc
  assert row['saved_roi_contains_projected'] is inside(saved,calc)
  probe=row['proposed_followup_embedded_probe_xyxy']
  if probe is not None:
   assert inside(probe,calc) and 0<=probe[0]<probe[2]<=new[0] and 0<=probe[1]<probe[3]<=new[1]
 assert [x['saved_roi_contains_projected'] for x in e['cases']]==[True,False,False]
 assert e['cases'][0]['proposed_followup_embedded_probe_xyxy'] is None
 assert all(v is None for v in e['unresolved'].values())
 assert e['guardrails']=={'D5_opposition':'〇/五_UNRESOLVED','G893_six':'OPEN','prior_13EI':'RETRACTED','algorithm_reopens':0,'candidate_collapses':0,'source_registry_added':0,'genealogy_nodes_added':0,'genealogy_edges_added':0}
 assert e['transmission_impact']['edges_supported']==e['transmission_impact']['edges_revised']==[]
 assert e['counts']=={'matrix':[222,222],'external_sources':761,'graph':[252,238],'open_or_blocked':11,'product':'CLOSED'}
 return True
if __name__=='__main__':
 check(json.loads(E.read_text(encoding='utf8')))
 print('13GO_PASS_RATIO_ONLY_GEOMETRIC_COVERAGE_NO_GLYPH_UPGRADE')
