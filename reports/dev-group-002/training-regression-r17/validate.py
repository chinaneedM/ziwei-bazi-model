#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
R=ROOT/'reports/dev-group-002/training-regression-r17'
INTERFACE='TR-R14-CAPABILITY-NEUTRAL-TIME-SCENE-NORMALIZED-BURDEN-V1'

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def canonical(obj):
    clone=dict(obj); clone.pop('canonical_sha256',None)
    return hashlib.sha256((json.dumps(clone,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()

def main():
    errors=[]
    review=load(R/'cross-case-stability-review.json')
    gate=load(R/'dev-example-005-gate.json')
    preservation=load(R/'prediction-preservation.json')
    manifest=load(R/'manifest.json')
    receipt=load(R/'validation.json')
    r14=load(ROOT/'reports/dev-group-002/training-regression-r14/validation.json')
    r15=load(ROOT/'reports/dev-group-002/training-regression-r15/cross-case-gate.json')
    r16v=load(ROOT/'reports/dev-group-002/training-regression-r16/validation.json')
    r16m=load(ROOT/'reports/dev-group-002/training-regression-r16/manifest.json')
    r16p=load(ROOT/'reports/dev-group-002/training-regression-r16/prediction-freeze.json')
    for name,obj in [('review',review),('gate',gate),('preservation',preservation),('manifest',manifest)]:
        if canonical(obj)!=obj.get('canonical_sha256'): errors.append(f'{name}: canonical hash mismatch')
    if r14.get('status')!='PASS' or r16v.get('status')!='PASS': errors.append('parent validation not PASS')
    if r15.get('canonical_sha256')!='1af82e715454b6220600bbc00dbdab5a0777c2d6c87494cc854d235bc331b8eb': errors.append('R15 gate hash mismatch')
    if r16m.get('canonical_sha256')!='f3d6bfd0641b9172158f31d7f78f7e40bd9c63dd77d423ed1da51699eedd0748': errors.append('R16 manifest hash mismatch')
    if r16p.get('canonical_sha256')!=preservation.get('parent_prediction_sha256'): errors.append('R16 prediction parent mismatch')
    if review.get('interface_id')!=INTERFACE or gate.get('interface_id')!=INTERFACE or manifest.get('interface_id')!=INTERFACE: errors.append('interface mismatch')
    if review.get('status')!='PASS' or review.get('decision')!='PASS_TECHNICALLY_STABLE_FOR_FINAL_FIXED_CASE_SHADOW_REBUILD': errors.append('review decision')
    inv=review.get('technical_invariants',{})
    expected_inv={'answer_access_during_prediction':False,'pairwise_cycles_total':0,'scene_only_positive_decision_rows':0,'raw_endpoint_count_decision_rows':0,'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0,'s00_s19_modified':False,'base_astrological_knowledge_changed':False,'case_specific_direction_rule_added':False}
    for key,value in expected_inv.items():
        if inv.get(key)!=value: errors.append(f'invariant {key}')
    if review.get('score_observation',{}).get('score_based_interface_rollback_permission')!='NO': errors.append('score rollback permission')
    if gate.get('allowed_case_ids')!=['DEV-EXAMPLE-005'] or gate.get('dev_example_005_shadow_rebuild_permission')!='YES': errors.append('DEV005 gate')
    if gate.get('new_external_case_admission')!='BLOCKED' or gate.get('formal_release_permission')!='NO' or gate.get('answer_visible_score_tuning_permission')!='NO': errors.append('release gate')
    if preservation.get('selection_changed') is not False or preservation.get('changed_case_ids') or preservation.get('changed_question_ids'): errors.append('prediction changed')
    if preservation.get('contains_answers') or preservation.get('answer_used_for_selection'): errors.append('answer leakage')
    score=preservation.get('current_training_regression_score',{})
    if (score.get('top1_hits'),score.get('top2_coverage'),score.get('question_count'))!=(9,13,25): errors.append('score preservation')
    if manifest.get('historical_rounds_preserved')!=[f'R{i}' for i in range(1,17)]: errors.append('history preservation')
    if manifest.get('next_required_round')!='R18_APPLY_FROZEN_INTERFACE_TO_DEV_EXAMPLE_005_FROM_CANONICAL_INPUTS': errors.append('next round')
    expected={'status':'PASS','error_count':0,'frozen_interface_id':INTERFACE,'reviewed_case_ids':['DEV-EXAMPLE-003','DEV-EXAMPLE-004'],'reviewed_pairwise_rows':60,'pairwise_cycle_count':0,'score_based_interface_rollback_permission':'NO','selection_changed':False,'top1_hits':9,'top2_coverage':13,'dev_example_005_shadow_rebuild_permission':'YES','allowed_case_ids':['DEV-EXAMPLE-005'],'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0,'formal_release_permission':'NO','new_external_case_admission':'BLOCKED','answer_visible_score_tuning_permission':'NO','base_astrological_knowledge_changed':False,'case_specific_direction_rule_added':False,'s00_s19_modified':False,'next_required_round':'R18_APPLY_FROZEN_INTERFACE_TO_DEV_EXAMPLE_005_FROM_CANONICAL_INPUTS'}
    for key,value in expected.items():
        if receipt.get(key)!=value: errors.append(f'receipt {key}')
    if errors:
        print(json.dumps({'status':'FAIL','errors':errors},ensure_ascii=False,indent=2)); return 1
    print(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
