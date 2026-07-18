#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent

def load(n): return json.loads((ROOT/n).read_text(encoding='utf-8'))
def canonical(o):
 x=dict(o); x.pop('canonical_sha256',None)
 return hashlib.sha256((json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def req(cond,msg,errors):
 if not cond: errors.append(msg)

def main():
 e=[]
 names=['prediction-freeze.json','neutral-time-facts.json','blind-models.json','source-index.json','atom-index.json','common-atom-index.json','pairwise-index.json','coverage-index.json','ziwei-case-structure.json','bazi-case-structure.json','public-relative-disclosure.json','postreveal-review.json','answer-vector-literal-replay.json']
 o={n:load(n) for n in names}
 for n,x in o.items():
  if 'canonical_sha256' in x: req(canonical(x)==x['canonical_sha256'],f'{n}:canonical',e)
 pred=o['prediction-freeze.json']; ans=o['answer-vector-literal-replay.json']; post=o['postreveal-review.json']
 src=o['source-index.json']; atom=o['atom-index.json']; common=o['common-atom-index.json']; pair=o['pairwise-index.json']; cov=o['coverage-index.json']
 req(pred['contains_answers'] is False,'prediction contains answers',e)
 req(all(c['answer_visible_during_prediction_materialization'] is False for c in pred['cases']),'case answer visibility',e)
 req(ans['prediction_freeze_canonical_sha256']==pred['canonical_sha256'],'answer parent freeze',e)
 req(ans['parsers_agree'] is True and ans['normalized_answer_string']=='DADAB','answer replay',e)
 c5=next(c for c in pred['cases'] if c['case_id']=='DEV-EXAMPLE-005')
 req(c5['ranks']==['DBAC','DCBA','DBAC','ABCD','DBAC'],'prediction ranks',e)
 req(c5['top1_vector']=='DDDAD' and c5['top2_vector']=='BCBBB','prediction vectors',e)
 req(post['selection_changed_after_answer_access'] is False,'postanswer selection change',e)
 req(post['group_score_after_replacement']=={'label':'TRAINING_REGRESSION_SCORE','question_count':25,'top1_hits':8,'top2_coverage':13},'score',e)
 req(src['row_count']==28 and len(src['rows'])==28,'source rows',e)
 source_ids={r['id'] for r in src['rows']}
 req(len(source_ids)==28,'source ids unique',e)
 req(atom['literal_atom_count']==45 and atom['track_direction_count']==90 and len(atom['rows'])==45,'atom counts',e)
 atom_ids={r['id'] for r in atom['rows']}; req(len(atom_ids)==45,'atom ids unique',e)
 aset={r['id']:set(r['parents']) for r in atom['parent_sets']}
 req(all(ps in aset for ps in (r['ps'] for r in atom['rows'])),'atom parent sets defined',e)
 req(all(par <= source_ids for par in aset.values()),'atom source parents defined',e)
 req(common['row_count']==30 and common['rows_with_material_common_atoms']==6,'common counts',e)
 common_map={(r['question_id'],r['left'],r['right']):r['common_atom_ids'] for r in common['rows']}
 req(pair['row_count']==30 and len(pair['rows'])==30 and pair['cycles']==[],'pairwise counts/cycles',e)
 pset={r['id']:set(r['parents']) for r in pair['parent_sets']}
 req(all(par <= source_ids for par in pset.values()),'pair source parents defined',e)
 for r in pair['rows']:
  req(r['lp'] in pset and r['rp'] in pset,f'pair parent set {r}',e)
  req(set(r['la']) <= atom_ids and set(r['ra']) <= atom_ids,f'pair atoms {r}',e)
  req(common_map.get((r['q'],r['l'],r['r']))==r['ca'],f'common mismatch {r["q"]}{r["l"]}{r["r"]}',e)
 for q in ['Q1','Q2','Q3','Q4','Q5']:
  req(sum(r['q']==q for r in pair['rows'])==6,f'pair count {q}',e)
 req(pair['ranks']=={'Q1':'DBAC','Q2':'DCBA','Q3':'DBAC','Q4':'ABCD','Q5':'DBAC'},'pair ranks',e)
 req(cov['row_count']==10 and len(cov['rows'])==10,'coverage rows',e)
 req(all(r['complete'] and not r['early_stop'] and r['status']=='PASS' for r in cov['rows']),'coverage legality',e)
 req(o['blind-models.json']['row_count']==10 and o['blind-models.json']['answer_access'] is False,'blind models',e)
 req(o['public-relative-disclosure.json']['row_count']==5 and o['public-relative-disclosure.json']['answer_access'] is False,'public disclosure',e)
 req(o['ziwei-case-structure.json']['answer_access'] is False and o['bazi-case-structure.json']['answer_access'] is False,'track structures',e)
 out={'schema':'DEV-GROUP-002-R18-LOCAL-SAFE-PROJECTION-VALIDATION-V1','status':'PASS' if not e else 'FAIL','errors':e,'error_count':len(e),'source_rows':28,'atom_rows':45,'track_directions':90,'common_rows':30,'material_common_rows':6,'pairwise_rows':30,'cycles':0,'coverage_rows':10,'ranks':['DBAC','DCBA','DBAC','ABCD','DBAC'],'group_score':[8,13],'ci_verified':False,'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0}
 print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)); return 1 if e else 0
if __name__=='__main__': raise SystemExit(main())
