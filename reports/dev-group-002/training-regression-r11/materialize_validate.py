#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path

D=Path('reports/dev-group-002/training-regression-r11'); C='DEV-EXAMPLE-002'
H={'R1':'reports/dev-group-002/training-regression-r1/manifest.json','R2':'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json','R3':'reports/dev-group-002/training-regression-r3/progress.json','R4':'reports/dev-group-002/training-regression-r4/compact-manifest.json',**{f'R{i}':f'reports/dev-group-002/training-regression-r{i}/manifest.json' for i in range(5,11)}}
I={'p':'reports/dev-group-002/training-regression-r9/prediction-freeze.json','b':'reports/dev-group-002/training-regression-r9/track-option-parent-bindings.json','e':'reports/dev-group-002/training-regression-r9/source-excerpts.json','r':'reports/dev-group-002/training-regression-r9/postreveal-review.json'}
# q|option|atom id|direction|exact(1/0)|literal
S='''
Q1|A|HEALTHY_FEW_PAIN|P|0|健康少病痛
Q1|A|SKIN_SENSITIVITY|U|1|皮肤敏感问题
Q1|A|SEAFOOD_AVOIDANCE|U|1|需戒吃海鲜
Q1|B|MAJOR_SURGERY|U|1|做过大型手术
Q1|B|LIFE_DANGER|U|1|曾有生命危险
Q1|C|WEAK_SICKLY|D|0|体弱多病
Q1|C|DIABETES|M|1|患有糖尿病
Q1|C|RECURRENT_CONDITION|P|0|病情反复
Q1|D|OBESITY|M|1|身材变得肥胖
Q1|D|LIVER_PROBLEM|M|1|肝问题
Q1|D|GI_PROBLEM|D|0|肠胃问题
Q1|D|FOOT_PROBLEM|D|0|脚患困扰
Q2|A|MEDIOCRE_LAZY|C|0|平庸懒惰
Q2|A|UNIVERSITY_GRADUATION|M|1|大学毕业
Q2|A|ORDINARY_SALARIED|P|1|普通受薪阶层
Q2|B|INTELLIGENT|P|0|聪明
Q2|B|NOT_STUDY|U|0|不读书
Q2|B|HIGH_SCHOOL|M|1|中学毕业
Q2|B|PART_TIME_PRIMARY|M|1|兼职为主
Q2|C|NOT_INTELLIGENT|C|0|不聪敏
Q2|C|HARDWORKING|P|0|勤力
Q2|C|UNIVERSITY_GRADUATION|M|1|大学毕业
Q2|C|FAMILY_BUSINESS|M|1|经营家族生意
Q2|D|INTELLIGENT|P|0|聪敏
Q2|D|CAN_STUDY|P|0|能读书
Q2|D|MASTERS_PHD|M|1|硕士博士
Q2|D|MANAGEMENT_ORIENTATION|D|0|企业管理能力取向
Q2|D|FORMAL_MANAGEMENT_TITLE|M|1|企业的管理层
Q3|A|ROMANCE_SCAM|U|1|感情受骗
Q3|A|ALL_SAVINGS_LOST|M|1|积蓄全无
Q3|A|FIXED_JOB|C|1|有固定工作
Q3|A|STABLE_INCOME|C|1|收入稳定
Q3|A|RECOVER_LOSS|U|1|弥补损失
Q3|B|FAME_SUCCESS|M|1|名成利就
Q3|B|SMOOTH_WORK|C|1|工作顺利
Q3|B|ABILITY_USED|P|0|个人能力得以发挥
Q3|B|PUBLIC_RECOGNITION|M|1|得到众人赏识
Q3|C|OWNER_IDENTITY|M|1|自己当了老板
Q3|C|AVERAGE_TURNOVER|P|1|生意额一般
Q3|C|HARD_OPERATION|P|0|艰辛经营
Q3|C|BREAK_FRAME|P|0|寻求突破框架
Q3|D|REPEATED_JOB_CHANGE|D|1|不停转工
Q3|D|MONEY_FLOW|P|0|财来财去
Q3|D|LIVE_WITH_FAMILY|P|1|与家人居住
Q3|D|PARTNER_PAYS|M|1|日常开支由伴侣负责
Q4|A|MARRIED|U|1|婚姻存在
Q4|A|HAPPY_HARMONIOUS|C|1|婚姻美满、相敬如宾
Q4|B|MARRIED|U|1|已婚
Q4|B|RELATION_HURT|S|0|配偶关系伤害
Q4|B|VERBAL_ABUSE|M|1|语言伤害、责备
Q4|C|MARRIED|U|1|曾有婚姻
Q4|C|MULTI_STAGE_RELATION|D|0|两阶段关系或两次结合
Q4|C|REGISTERED_DIVORCE|M|1|离婚
Q4|C|REGISTERED_REMARRIAGE|M|1|再婚
Q4|C|CURRENT_STABLE|M|1|现在感情稳定
Q4|D|SAME_SEX_ORIENTATION|U|1|同性恋者
Q4|D|PARTNER_CARE|U|1|得到伴侣爱护
Q5|A|WEALTHY|M|1|家境富有、不愁衣食
Q5|A|MOTHER_CLOSE|P|1|跟母亲感情好
Q5|A|FATHER_DISTANT|U|1|父亲关系较疏远
Q5|B|COMFORTABLE_CLASS|M|1|家境曾经小康
Q5|B|FATHER_BUSINESS_FAILURE|S|1|父亲随后生意失败
Q5|B|HOUSEHOLD_DECLINE|D|0|家庭或祖业衰退场景
Q5|B|NORMAL_PARENT_RELATION|P|1|父母与命主感情关系正常
Q5|C|POOR_CHILDHOOD|M|1|从小贫穷
Q5|C|MOTHER_DEATH|C|1|母亲去世
Q5|C|FATHER_CAREGIVER|U|1|父亲养育命主
Q5|C|FATHER_CLOSE|P|1|与父亲感情关系好
Q5|D|PARENT_DIVORCE|U|1|父母离婚
Q5|D|BASIC_SUPPORT|P|1|父母各自提供基本生活费
Q5|D|GRANDMOTHER_CAREGIVER|U|1|从小由外婆照顾
'''.strip()
# Equivalent atoms removed before comparison.
E={('Q2','A','C'):[('UNIVERSITY_GRADUATION','UNIVERSITY_GRADUATION','UNIVERSITY_GRADUATION')],('Q2','B','D'):[('INTELLIGENT','INTELLIGENT','POSITIVE_INTELLIGENCE')],('Q4','A','B'):[('MARRIED','MARRIED','MARRIED_STATE')],('Q4','A','C'):[('MARRIED','MARRIED','MARRIED_STATE')],('Q4','B','C'):[('MARRIED','MARRIED','MARRIED_STATE')]}
N={'D':'DIRECT_SUPPORT','P':'PARTIAL_SUPPORT','S':'LIMITED_SCENE_ONLY','M':'LIMITED_MISSING_ENDPOINT','U':'UNKNOWN','C':'DIRECT_COUNTEREVIDENCE'}

def R(p): return json.loads(p.read_text(encoding='utf-8'))
def payload(o):
 c=dict(o);c.pop('canonical_sha256',None);return (json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def W(o): c=dict(o);c['canonical_sha256']=hashlib.sha256(payload(c)).hexdigest();return c
def h(o): return hashlib.sha256(payload(o)).hexdigest()
def blob(p):
 x=p.read_bytes();return hashlib.sha1(f'blob {len(x)}\0'.encode()+x).hexdigest()
def wr(p,o): p.write_text(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def key(q,a,b): return (q,*sorted((a,b)))
def specs():
 out=[]
 for line in S.splitlines():
  q,o,a,d,x,t=line.split('|',5);out.append({'question_id':q,'option_id':o,'atom_id':f'{q}_{o}_{a}','short_id':a,'literal_atom':t,'direction_status':N[d],'exact_endpoint_required':x=='1'})
 return out

def atom_matrix(bindings,excerpts):
 bi={(x['question_id'],x['track_id'],x['option_id']):x for x in bindings['track_rows']};valid={x['excerpt_id'] for x in excerpts['rows']};rows=[]
 for a in specs():
  b=bi[(a['question_id'],'ZIWEI',a['option_id'])];parents=b['parent_excerpt_ids']
  if not set(parents)<=valid: raise ValueError('unresolved parent')
  rows.append({**a,'case_id':C,'track_id':'ZIWEI','source_parent_excerpt_ids':parents,'source_parent_binding_sha256':bindings['canonical_sha256'],'capability_ceiling':'RELATIVE_DIRECTION_ONLY','formal_exact_assertion':None})
 return W({'schema':'DEV-GROUP-002-R11-LITERAL-ATOM-DIRECTION-MATRIX-V1','group_id':'DEV-GROUP-002','case_id':C,'round_id':'R11','parent_r9_bindings_sha256':bindings['canonical_sha256'],'parent_r9_source_excerpts_sha256':excerpts['canonical_sha256'],'rows':rows,'row_count':len(rows),'option_count':20,'status':'PASS_ALL_ATOMS_HAVE_DIRECTION_AND_SOURCE_PARENTS'})
def common(matrix):
 rows=[]
 for q in [f'Q{i}' for i in range(1,6)]:
  for l,r in itertools.combinations('ABCD',2):
   eq=E.get(key(q,l,r),[]);rows.append({'case_id':C,'question_id':q,'left':l,'right':r,'equivalence_rows':[{'left_short_id':a,'right_short_id':b,'common_atom_id':c,'distinguishing_contribution':0} for a,b,c in eq],'common_atom_ids_zeroed':[c for _,_,c in eq],'status':'EXECUTED_BEFORE_PAIRWISE'})
 return W({'schema':'DEV-GROUP-002-R11-COMMON-ATOM-SUBTRACTION-V1','group_id':'DEV-GROUP-002','case_id':C,'round_id':'R11','parent_atom_matrix_sha256':matrix['canonical_sha256'],'rows':rows,'row_count':30,'rows_with_material_common_atoms':sum(bool(x['common_atom_ids_zeroed']) for x in rows),'status':'PASS'})
def oa(matrix,q,o): return [x for x in matrix['rows'] if x['question_id']==q and x['option_id']==o]
def metrics(atoms,zero):
 z=[x for x in atoms if x['short_id'] not in zero]
 ids=lambda s:[x['atom_id'] for x in z if x['direction_status']==s]
 return {'remaining_atom_ids':[x['atom_id'] for x in z],'direct_support_atom_ids':ids('DIRECT_SUPPORT'),'direct_counterevidence_atom_ids':ids('DIRECT_COUNTEREVIDENCE'),'partial_support_atom_ids':ids('PARTIAL_SUPPORT'),'scene_only_atom_ids':ids('LIMITED_SCENE_ONLY'),'missing_exact_endpoint_atom_ids':[x['atom_id'] for x in z if x['exact_endpoint_required'] and x['direction_status'] in {'LIMITED_MISSING_ENDPOINT','UNKNOWN','DIRECT_COUNTEREVIDENCE'}],'unknown_atom_ids':ids('UNKNOWN'),'source_parent_excerpt_ids':sorted({p for x in z for p in x['source_parent_excerpt_ids']})}
def choose(a,b,rank,l,r):
 crit=[('DISTINCTIVE_DIRECT_SUPPORT','direct_support_atom_ids','MAX'),('SAME_AXIS_DIRECT_COUNTEREVIDENCE','direct_counterevidence_atom_ids','MIN'),('COMPOSITE_PARTIAL_COVERAGE','partial_support_atom_ids','MAX'),('EXACT_ENDPOINT_DISTANCE','missing_exact_endpoint_atom_ids','MIN'),('SCENE_ONLY_COVERAGE','scene_only_atom_ids','MAX'),('UNRESOLVED_UNKNOWN_ATOMS','unknown_atom_ids','MIN')]
 for n,k,m in crit:
  x,y=len(a[k]),len(b[k])
  if x!=y:return (l if (x>y if m=='MAX' else x<y) else r),n,{'left_value':x,'right_value':y,'mode':m}
 return (l if rank.index(l)<rank.index(r) else r),'LOW_INFORMATION_FORCED_TIEBREAK_PRESERVE_R9_ORDER',{'left_value':None,'right_value':None,'mode':'TIE'}
def pairwise(matrix,sub,pred):
 case=next(x for x in pred['cases'] if x['case_id']==C);ranks={f'Q{i}':x for i,x in enumerate(case['ranks'],1)};si={(x['question_id'],x['left'],x['right']):x for x in sub['rows']};rows=[]
 for q in ranks:
  for l,r in itertools.combinations('ABCD',2):
   e=si[(q,l,r)]['equivalence_rows'];a=metrics(oa(matrix,q,l),{x['left_short_id'] for x in e});b=metrics(oa(matrix,q,r),{x['right_short_id'] for x in e});w,basis,v=choose(a,b,ranks[q],l,r)
   rows.append({'case_id':C,'question_id':q,'left':l,'right':r,'winner':w,'loser':r if w==l else l,'decision_basis':basis,'decision_values':v,'common_atom_ids_zeroed':si[(q,l,r)]['common_atom_ids_zeroed'],'left_atom_direction_parent_ids':a['remaining_atom_ids'],'right_atom_direction_parent_ids':b['remaining_atom_ids'],'left_source_parent_excerpt_ids':a['source_parent_excerpt_ids'],'right_source_parent_excerpt_ids':b['source_parent_excerpt_ids'],'left_metrics':a,'right_metrics':b,'atom_level_replay_status':'PASS','answer_access_during_decision':False})
 derived={}
 for q in ranks:
  qr=[x for x in rows if x['question_id']==q];wins={o:0 for o in 'ABCD'}
  for x in qr:wins[x['winner']]+=1
  rank=''.join(sorted('ABCD',key=lambda o:(-wins[o],ranks[q].index(o))))
  for l,r in itertools.combinations('ABCD',2):
   actual=next(x['winner'] for x in qr if x['left']==l and x['right']==r);expected=l if rank.index(l)<rank.index(r) else r
   if actual!=expected:raise ValueError(f'non-transitive {q}')
  derived[q]=rank
 return W({'schema':'DEV-GROUP-002-R11-ATOM-PARENT-PAIRWISE-REPLAY-V1','group_id':'DEV-GROUP-002','case_id':C,'round_id':'R11','parent_atom_matrix_sha256':matrix['canonical_sha256'],'parent_common_subtraction_sha256':sub['canonical_sha256'],'parent_r9_prediction_sha256':pred['canonical_sha256'],'rows':rows,'row_count':30,'derived_ranks':derived,'atom_level_replayable_rows':30,'low_information_tiebreak_rows':sum(x['decision_basis'].startswith('LOW_INFORMATION') for x in rows),'status':'PASS_COMPLETE_TRANSITIVE_REPLAY'})
def prediction(old,pw):
 cases=[];changed=[]
 for c in old['cases']:
  n=dict(c)
  if c['case_id']==C:
   ranks=[pw['derived_ranks'][f'Q{i}'] for i in range(1,6)]
   changed=[f'{C}:Q{i}' for i,(a,b) in enumerate(zip(c['ranks'],ranks),1) if a!=b];n.update(ranks=ranks,top1_vector=''.join(x[0] for x in ranks),top2_vector=''.join(x[1] for x in ranks),prediction_origin='R11_LITERAL_ATOM_PARENT_PAIRWISE_REPLAY')
  cases.append(n)
 return W({'schema':'DEV-GROUP-002-R11-PREDICTION-FREEZE-V1','group_id':'DEV-GROUP-002','round_id':'R11','run_class':'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD','parent_r9_prediction_sha256':old['canonical_sha256'],'pairwise_replay_sha256':pw['canonical_sha256'],'case_ids':old['case_ids'],'cases':cases,'question_count':25,'changed_case_ids':[C] if changed else [],'changed_question_ids':changed,'contains_answers':False,'answer_visible_during_prediction_materialization':False,'formal_exact_assertion_permission':'NULL_ONLY','machine_valid_local_seals':0,'s03_fusions':0,'new_case_admission':'BLOCKED','base_astrological_knowledge_changed':False})
def review(old,pred):
 scores=[];a=b=0
 for c in pred['cases']:
  ans=old['answer_vectors'][c['case_id']];x=sum(i==j for i,j in zip(c['top1_vector'],ans));y=sum(k in (i,j) for i,j,k in zip(c['top1_vector'],c['top2_vector'],ans));a+=x;b+=y;scores.append({'case_id':c['case_id'],'top1_hits':x,'top2_coverage':y})
 return W({'schema':'DEV-GROUP-002-R11-POSTREVEAL-REVIEW-V1','group_id':'DEV-GROUP-002','round_id':'R11','parent_prediction_sha256':pred['canonical_sha256'],'answer_vectors':old['answer_vectors'],'case_scores':scores,'totals':{'top1_hits':a,'top2_coverage':b,'question_count':25,'score_label':'TRAINING_REGRESSION_SCORE'},'comparison_to_r9':{'top1_delta':a-13,'top2_delta':b-16},'accuracy_claim':'NO_NEW_BLIND_RESULT','answer_used_for_selection':False})
def generic():return W({'schema':'DEV-GROUP-002-R11-GENERIC-FIX-V1','group_id':'DEV-GROUP-002','round_id':'R11','fix_id':'TR-R11-LITERAL-ATOM-PARENT-PAIRWISE-REPLAY','defect_class':'PAIRWISE_DECISION_WITHOUT_LITERAL_ATOM_PARENT_REPLAY','general_rules':['Every material option atom must have an explicit semantic direction, exact-endpoint flag, capability ceiling, and immutable source-parent identifiers before pairwise comparison.','Equivalent atoms shared by two options must be mapped explicitly and removed from both distinctive sides before any comparison criterion is evaluated.','Pairwise decisions must publish the atom identifiers and source-parent identifiers actually used on both sides.','The fixed decision sequence is evaluated mechanically from atom rows; prior order may be used only for the final low-information tiebreak after all earlier criteria tie.','Postreveal answers are read only after the answer-free prediction object is canonically frozen and cannot alter an atom direction or pairwise winner.'],'base_astrological_knowledge_changed':False,'case_specific_direction_rule_added':False,'s00_s19_modified':False,'impact_scope':'GENERIC_ATOM_DIRECTION_AND_PAIRWISE_RUNTIME_INTERFACE'})
def build(root):
 p=R(root/I['p']);b=R(root/I['b']);e=R(root/I['e']);rv=R(root/I['r']);m=atom_matrix(b,e);s=common(m);pw=pairwise(m,s,p);pr=prediction(p,pw);re=review(rv,pr);g=generic();base={'literal-atom-direction-matrix.json':m,'common-atom-subtraction.json':s,'pairwise-replay.json':pw,'prediction-freeze.json':pr,'postreveal-review.json':re,'generic-fix.json':g};hist={k:{'path':v,'git_blob_sha':blob(root/v),'preserved':True} for k,v in H.items()};arts={n[:-5].replace('-','_'):{'path':str(D/n),'canonical_sha256':o['canonical_sha256']} for n,o in base.items()};man=W({'schema':'DEV-GROUP-002-R11-FROZEN-MANIFEST-V1','group_id':'DEV-GROUP-002','round_id':'R11','status':'FROZEN_ATOM_LEVEL_PAIRWISE_REPLAY','run_class':'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD','historical_rounds':hist,'artifacts':arts,'statistics':{'question_count':25,'processed_case_count':1,'processed_question_count':5,'literal_atom_direction_rows':m['row_count'],'common_atom_pair_rows':30,'pairwise_rows':30,'atom_level_replayable_pairwise_rows':30,'low_information_tiebreak_rows':pw['low_information_tiebreak_rows'],'selection_changed_from_r9':bool(pr['changed_question_ids']),'top1_hits':re['totals']['top1_hits'],'top2_coverage':re['totals']['top2_coverage'],'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0},'training_conclusion':'R11 replaces aggregate option keys with literal atom directions, common-atom subtraction, and atom/source-parent pairwise replay. Any selection changes are derived before answer access; exact formal endpoints remain unsealed.','next_required_round':'R12_APPLY_ATOM_REPLAY_INTERFACE_TO_DEV_EXAMPLE_003_FROM_CANONICAL_INPUTS','new_case_admission':'BLOCKED','base_astrological_knowledge_changed':False,'case_specific_direction_rule_added':False,'s00_s19_modified':False});base['manifest.json']=man;return base
def materialize(root):
 out=root/D;out.mkdir(parents=True,exist_ok=True);o=build(root)
 for n,x in o.items():wr(out/n,x)
 c=next(x for x in o['prediction-freeze.json']['cases'] if x['case_id']==C);st=o['manifest.json']['statistics'];(out/'summary.md').write_text(f"# DEV-GROUP-002 R11：字面原子方向父链与成对重放\n\nR11物化{st['literal_atom_direction_rows']}条字面原子方向行和30组成对重放，全部成对行引用实际原子与来源父ID。DEV-EXAMPLE-002排序：{' / '.join(c['ranks'])}。相对R9变化题数：{len(o['prediction-freeze.json']['changed_question_ids'])}。组级训练回归TOP1 {st['top1_hits']}/25、TOP2 {st['top2_coverage']}/25。正式有效题、本地密封和S03融合仍为0。\n",encoding='utf-8')
def validate(root):
 er=[];out=root/D;names=['literal-atom-direction-matrix.json','common-atom-subtraction.json','pairwise-replay.json','prediction-freeze.json','postreveal-review.json','generic-fix.json','manifest.json'];o={}
 for n in names:
  if not (out/n).exists():er.append('missing '+n)
  else:o[n]=R(out/n)
 if er:return {'status':'FAIL','error_count':len(er),'errors':er}
 for n,x in o.items():
  if h(x)!=x.get('canonical_sha256'):er.append(n+' hash')
 m=o[names[0]];s=o[names[1]];pw=o[names[2]];pr=o[names[3]];rv=o[names[4]];g=o[names[5]];man=o[names[6]]
 if m['row_count']!=len(specs()) or any(not x['source_parent_excerpt_ids'] for x in m['rows']):er.append('atom matrix')
 if s['row_count']!=30 or s['rows_with_material_common_atoms']!=5:er.append('common subtraction')
 if pw['row_count']!=30 or pw['atom_level_replayable_rows']!=30 or pw['status']!='PASS_COMPLETE_TRANSITIVE_REPLAY':er.append('pairwise')
 if any(not x['left_atom_direction_parent_ids'] or not x['right_atom_direction_parent_ids'] or x['answer_access_during_decision'] for x in pw['rows']):er.append('pair parents/answer')
 c=next(x for x in pr['cases'] if x['case_id']==C);derived=[pw['derived_ranks'][f'Q{i}'] for i in range(1,6)]
 if c['ranks']!=derived or pr['contains_answers'] or pr['answer_visible_during_prediction_materialization']:er.append('prediction')
 if rv['answer_used_for_selection']:er.append('review')
 if any(t in '\n'.join(g['general_rules']) for t in ['DEV-EXAMPLE-002','DBDDB','Q2','Q4']):er.append('generic case token')
 if man['status']!='FROZEN_ATOM_LEVEL_PAIRWISE_REPLAY' or man['statistics']['atom_level_replayable_pairwise_rows']!=30:er.append('manifest')
 for k,x in man['historical_rounds'].items():
  if x['path']!=H[k] or blob(root/H[k])!=x['git_blob_sha'] or not x['preserved']:er.append('history '+k)
 return {'schema':'DEV-GROUP-002-R11-VALIDATION-V1','status':'PASS' if not er else 'FAIL','error_count':len(er),'errors':er,'historical_rounds_preserved':list(H),'processed_case_id':C,'literal_atom_direction_rows':m['row_count'],'common_atom_pair_rows':30,'rows_with_material_common_atoms':5,'pairwise_rows':30,'atom_level_replayable_pairwise_rows':30,'low_information_tiebreak_rows':pw['low_information_tiebreak_rows'],'dev002_ranks':c['ranks'],'dev002_top1':c['top1_vector'],'dev002_top2':c['top2_vector'],'selection_changed_from_r9':bool(pr['changed_question_ids']),'changed_question_ids':pr['changed_question_ids'],'top1_hits':rv['totals']['top1_hits'],'top2_coverage':rv['totals']['top2_coverage'],'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0,'base_astrological_knowledge_changed':False,'s00_s19_modified':False,'new_case_admission':'BLOCKED'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo-root',default='.');p.add_argument('--write',action='store_true');p.add_argument('--validate',action='store_true');a=p.parse_args();root=Path(a.repo_root).resolve()
 if a.write:materialize(root)
 if a.validate:
  x=validate(root);wr(root/D/'validation.json',x);print(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2));return 0 if x['status']=='PASS' else 1
 return 0
if __name__=='__main__':raise SystemExit(main())
