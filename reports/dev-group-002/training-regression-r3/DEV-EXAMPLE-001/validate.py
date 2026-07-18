#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

KNOWLEDGE = {
    'S06': 'knowledge/base/S06_六十星系与十二基础盘库.txt',
    'S07': 'knowledge/base/S07_全星曜与星系入十二宫库.txt',
    'S16': 'knowledge/base/S16_八字专题映射与紫微接口库.txt',
}

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(s: str) -> str:
    s = s.replace('[','').replace(']','').replace('【','').replace('】','')
    return re.sub(r'[\s，。；：、“”‘’（）()\-_/|]+', '', s)

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root', type=Path, default=Path('.'))
    ap.add_argument('--object', type=Path, default=Path('reports/dev-group-002/training-regression-r3/DEV-EXAMPLE-001/source-grounded-replay.json'))
    ap.add_argument('--output', type=Path)
    args=ap.parse_args(); root=args.repo_root.resolve(); objp=(root/args.object).resolve()
    obj=json.loads(objp.read_text(encoding='utf-8')); errors=[]

    if obj.get('run_class')!='ANSWER_FREE_UPSTREAM_REBUILD_WITH_POSTREVEAL_DIAGNOSIS_SEPARATED': errors.append('run class mismatch')
    if obj.get('case_id')!='DEV-EXAMPLE-001': errors.append('case mismatch')

    freeze=obj['input_freeze']
    for key in ('case_bundle','ziwei','bazi','questions'):
        p=root/freeze[f'{key}_path']; expected=freeze[f'{key}_sha256']
        if not p.exists(): errors.append(f'missing {key}: {p}'); continue
        actual=sha256(p)
        if actual!=expected: errors.append(f'{key} sha mismatch: {actual}')

    ziwei=(root/freeze['ziwei_path']).read_text(encoding='utf-8')
    bazi=json.loads((root/freeze['bazi_path']).read_text(encoding='utf-8'))
    required_chart = [
      '命  宫[甲午]', '迁移宫[庚子]', '天同[旺][↓忌],太阴[庙][↓科]',
      '父母宫[乙未]', '疾厄宫[辛丑]', '武曲[庙],贪狼[庙]',
      '夫妻宫[壬辰][身宫]', '天机[利][↑忌],天梁[庙][↓禄]', '地劫[陷]',
      '官禄宫[戊戌]', '财帛宫[庚寅]', '太阳[旺][生年权][↓禄],巨门[庙][生年禄]',
      '田宅宫[丁酉]', '廉贞[平],破军[陷]',
      '1980年[庚申](30虚岁)', '流年四化:太阳禄,武曲权,太阴科,天同忌',
      '1993年[癸酉](43虚岁)', '流年四化:破军禄,巨门权,太阴科,贪狼忌'
    ]
    for text in required_chart:
        if text not in ziwei: errors.append('missing chart fact: '+text)
    pillars=bazi['transcription']['pillars']
    if [pillars[k] for k in ('year','month','day','hour')] != ['辛卯','己亥','戊午','丁巳']: errors.append('bazi pillars mismatch')

    knowledge_text={sid:(root/path).read_text(encoding='utf-8') for sid,path in KNOWLEDGE.items()}
    for call in obj['source_calls']:
        sid=call['library']; text=knowledge_text.get(sid)
        if text is None: errors.append('unknown source library '+sid); continue
        atom=call.get('source_atom_id')
        if atom and atom not in text: errors.append(f'missing atom {atom}')
        if norm(call['required_text']) not in norm(text): errors.append(f"required text not found: {call.get('source_atom_id', call.get('source_line'))}")
        if call.get('applicability','').startswith('NOT_APPLICABLE') and call.get('purpose')!='父母武贪火铃条件检查': errors.append('unexpected not-applicable call')

    selectors=obj['ziwei_physical_selectors']
    if len(selectors)!=6: errors.append('expected six physical selectors')
    ids={s['selector_id'] for s in selectors}
    if len(ids)!=len(selectors): errors.append('duplicate selectors')
    for s in selectors:
        if not s['selector_status'].startswith('PASS_'): errors.append('selector not passed: '+s['selector_id'])
        if s.get('borrow_from_palace') and 'BORROW' not in s['selector_status']: errors.append('borrow selector not marked borrow: '+s['selector_id'])

    years={x['year']:x for x in obj['neutral_time_facts']}
    if sorted(years)!=[1980,1993]: errors.append('neutral year set mismatch')
    if years[1980]['direct_event_type']!='UNRESOLVED': errors.append('1980 event semantics leaked')
    if years[1993]['direct_actor_and_endpoint']!='UNRESOLVED': errors.append('1993 actor/endpoint leaked')
    for y in years.values():
        if y['ziwei']['event_semantics_permission']!='NO' or y['bazi']['event_semantics_permission']!='NO': errors.append('neutral time object contains event semantics')

    qrows=obj['question_track_results']
    if [q['question_id'] for q in qrows] != ['Q1','Q2','Q3','Q4','Q5']: errors.append('question row order mismatch')
    if any(q['formal_exact_assertion'] is not None for q in qrows): errors.append('formal assertion must remain null')
    if any(q['local_seal_status'].startswith('SEALED') for q in qrows): errors.append('local seal falsely claimed')

    upstream=dict(obj); diagnosis=upstream.pop('postreveal_diagnosis')
    upstream_text=json.dumps(upstream,ensure_ascii=False,sort_keys=True)
    if diagnosis['literal_answer_vector'] in upstream_text or diagnosis['r1_shadow_top1_vector'] in upstream_text: errors.append('answer vector leaked into upstream rebuild')
    if diagnosis['score_label']!='TRAINING_DIAGNOSIS_NOT_ACCURACY': errors.append('diagnosis score label invalid')
    if diagnosis['source_confirmed_exact_top1_count']!=0: errors.append('unsupported source-confirmed count')

    agg=obj['aggregate']
    for k in ('ziwei_machine_valid_local_seals','bazi_machine_valid_local_seals','s03_fusions','formal_valid_questions'):
        if agg[k]!=0: errors.append(k+' must remain zero')
    if agg['new_case_admission']!='BLOCKED': errors.append('new case admission must remain blocked')

    result={'schema':'DEV-EXAMPLE-001-R3-VALIDATION-V1','status':'PASS' if not errors else 'FAIL','error_count':len(errors),'errors':errors,'physical_selector_count':len(selectors),'source_call_count':len(obj['source_calls']),'neutral_time_fact_count':len(obj['neutral_time_facts']),'question_count':len(qrows),'machine_valid_local_seals':0,'s03_fusions':0,'training_conclusion':'R1_ANSWER_ALIGNMENT_NOT_SOURCE_GROUNDED'}
    out=args.output or objp.with_name('validation.json')
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
