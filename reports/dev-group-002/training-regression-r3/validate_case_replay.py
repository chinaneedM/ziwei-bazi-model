#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

DEFAULT_LIBS={
'S06':'knowledge/base/S06_六十星系与十二基础盘库.txt',
'S07':'knowledge/base/S07_全星曜与星系入十二宫库.txt',
'S16':'knowledge/base/S16_八字专题映射与紫微接口库.txt',
'S17':'knowledge/base/S17_专题闭合人物太极与动作终点链库.txt',
'S18':'knowledge/base/S18_证据归并非法归零与评分分寸库.txt',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 s=s.replace('[','').replace(']','').replace('【','').replace('】','')
 return re.sub(r'[\s，。；：、“”‘’（）()\-_/|→]+','',s)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',type=Path,default=Path('.')); ap.add_argument('--object',type=Path,required=True); ap.add_argument('--output',type=Path)
 a=ap.parse_args(); root=a.repo_root.resolve(); p=(root/a.object).resolve(); o=json.loads(p.read_text(encoding='utf-8')); e=[]
 fr=o['input_freeze']
 for k in ('case_bundle','ziwei','bazi','questions'):
  fp=root/fr[f'{k}_path']; ex=fr[f'{k}_sha256']
  if not fp.exists(): e.append(f'missing {k}'); continue
  if sha(fp)!=ex:e.append(f'{k} sha mismatch')
 z=(root/fr['ziwei_path']).read_text(encoding='utf-8'); b=json.loads((root/fr['bazi_path']).read_text(encoding='utf-8'))
 for x in o['required_chart_snippets']:
  if x not in z:e.append('missing chart snippet: '+x)
 pillars=b['transcription']['pillars']; actual=' '.join(pillars[k] for k in ('year','month','day','hour'))
 if actual!=o['expected_pillars']:e.append('pillars mismatch')
 texts={k:(root/v).read_text(encoding='utf-8') for k,v in DEFAULT_LIBS.items()}
 for c in o['source_calls']:
  t=texts[c['library']]
  if c.get('source_atom_id') and c['source_atom_id'] not in t:e.append('missing atom '+c['source_atom_id'])
  if norm(c['required_text']) not in norm(t):e.append('missing required text '+str(c.get('source_atom_id',c.get('source_line'))))
 sels=o['ziwei_physical_selectors']
 if len({x['selector_id'] for x in sels})!=len(sels):e.append('duplicate selectors')
 if any(not x['selector_status'].startswith('PASS_') for x in sels):e.append('selector status failure')
 q=o['question_track_results']
 if [x['question_id'] for x in q]!=['Q1','Q2','Q3','Q4','Q5']:e.append('question order mismatch')
 if any(x['formal_exact_assertion'] is not None for x in q):e.append('formal assertion not null')
 if any(x['local_seal_status'].startswith('SEALED') for x in q):e.append('false seal')
 up=dict(o); d=up.pop('postreveal_diagnosis'); uts=json.dumps(up,ensure_ascii=False,sort_keys=True)
 for token in (d['literal_answer_vector'],d['r1_shadow_top1_vector']):
  if token in uts:e.append('answer leak into upstream')
 if d['score_label']!='TRAINING_DIAGNOSIS_NOT_ACCURACY':e.append('diagnosis label')
 ag=o['aggregate']
 for k in ('ziwei_machine_valid_local_seals','bazi_machine_valid_local_seals','s03_fusions','formal_valid_questions'):
  if ag[k]!=0:e.append(k+' must be zero')
 if ag['new_case_admission']!='BLOCKED':e.append('new case admission')
 r={'schema':'DEV-GROUP-002-R3-CASE-VALIDATION-V1','case_id':o['case_id'],'status':'PASS' if not e else 'FAIL','error_count':len(e),'errors':e,'selector_count':len(sels),'source_call_count':len(o['source_calls']),'question_count':len(q),'source_confirmed_exact_top1_count':d['source_confirmed_exact_top1_count'],'machine_valid_local_seals':0}
 out=a.output or p.with_name('validation.json'); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8'); print(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)); return 0 if not e else 1
if __name__=='__main__':raise SystemExit(main())
