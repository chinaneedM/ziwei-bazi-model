#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r13')
CASE_ID = 'DEV-EXAMPLE-003'
HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    **{f'R{i}': f'reports/dev-group-002/training-regression-r{i}/manifest.json' for i in range(5, 13)},
}
INPUTS = {
    'r11_prediction': 'reports/dev-group-002/training-regression-r11/prediction-freeze.json',
    'r12_matrix': 'reports/dev-group-002/training-regression-r12/literal-atom-direction-matrix.json',
    'r12_pairwise': 'reports/dev-group-002/training-regression-r12/pairwise-replay.json',
    'r12_prediction': 'reports/dev-group-002/training-regression-r12/prediction-freeze.json',
    'r12_review': 'reports/dev-group-002/training-regression-r12/postreveal-review.json',
    'r12_excerpts': 'reports/dev-group-002/training-regression-r12/source-excerpts.json',
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def canonical_payload(obj: dict[str, Any]) -> bytes:
    clone = dict(obj)
    clone.pop('canonical_sha256', None)
    return (json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def with_hash(obj: dict[str, Any]) -> dict[str, Any]:
    clone = dict(obj)
    clone['canonical_sha256'] = hashlib.sha256(canonical_payload(clone)).hexdigest()
    return clone


def canonical_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload(obj)).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')


def parent_capabilities(excerpts: dict[str, Any]) -> dict[str, dict[str, bool]]:
    result: dict[str, dict[str, bool]] = {}
    for row in excerpts['rows']:
        text = row['text']
        result[row['excerpt_id']] = {
            'direct_event_yes': '"direct_event":"YES"' in text or 'DIRECT_EVENT=YES' in text,
            'direct_endpoint_yes': '"direct_endpoint":"YES"' in text or 'DIRECT_REALITY_ENDPOINT=YES' in text,
            'direct_score_yes': '"direct_score":"YES"' in text or 'DIRECT_OPTION_RANKING_AUTHORITY=YES' in text,
            'contains_direct_event_no': '"direct_event":"NO"' in text or 'DIRECT_EVENT=NO' in text,
            'contains_direct_endpoint_no': '"direct_endpoint":"NO"' in text or 'DIRECT_REALITY_ENDPOINT=NO' in text,
            'contains_direct_score_no': '"direct_score":"NO"' in text or 'DIRECT_OPTION_RANKING_AUTHORITY=NO' in text,
            'neutral_time': row['excerpt_id'] in {'S10_NEUTRAL_TIME', 'S15_NEUTRAL_TIME'},
        }
    return result


def build_atom_capability_audit(matrix: dict[str, Any], excerpts: dict[str, Any]) -> dict[str, Any]:
    caps = parent_capabilities(excerpts)
    rows = []
    for atom in matrix['rows']:
        parent_ids = atom['source_parent_excerpt_ids']
        parent_caps = [caps[parent] for parent in parent_ids]
        defects: list[str] = []
        if atom['track_id'] == 'ZIWEI':
            if atom['exact_endpoint_required'] and atom['direction_status'] == 'DIRECT_SUPPORT' and not any(c['direct_endpoint_yes'] for c in parent_caps):
                defects.append('EXACT_ENDPOINT_DIRECT_SUPPORT_WITHOUT_DIRECT_ENDPOINT_PARENT')
            if atom['direction_status'] == 'DIRECT_SUPPORT' and any(c['neutral_time'] for c in parent_caps) and not any(c['direct_event_yes'] for c in parent_caps):
                defects.append('NEUTRAL_TIME_USED_IN_DIRECT_EVENT_SUPPORT')
            if atom['direction_status'] == 'DIRECT_SUPPORT' and not any(c['direct_score_yes'] for c in parent_caps):
                defects.append('DIRECT_SUPPORT_WITHOUT_DIRECT_SCORE_PARENT')
            if atom['direction_status'] == 'LIMITED_SCENE_ONLY':
                defects.append('SCENE_ONLY_MUST_NOT_COUNT_AS_POSITIVE_COVERAGE')
        rows.append({
            'case_id': CASE_ID,
            'question_id': atom['question_id'],
            'track_id': atom['track_id'],
            'option_id': atom['option_id'],
            'atom_id': atom['atom_id'],
            'literal_atom': atom['literal_atom'],
            'direction_status': atom['direction_status'],
            'exact_endpoint_required': atom['exact_endpoint_required'],
            'source_parent_excerpt_ids': parent_ids,
            'parent_direct_event_yes_count': sum(c['direct_event_yes'] for c in parent_caps),
            'parent_direct_endpoint_yes_count': sum(c['direct_endpoint_yes'] for c in parent_caps),
            'parent_direct_score_yes_count': sum(c['direct_score_yes'] for c in parent_caps),
            'defect_ids': defects,
            'audit_status': 'FAIL_CLOSED' if defects else 'PASS_OR_NOT_APPLICABLE',
            'selection_change_permission': 'NO_R13_DIAGNOSTIC_ONLY',
        })
    ziwei_rows = [row for row in rows if row['track_id'] == 'ZIWEI']
    return with_hash({
        'schema': 'DEV-GROUP-002-R13-ATOM-CAPABILITY-AUDIT-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R13',
        'parent_matrix_sha256': matrix['canonical_sha256'],
        'parent_source_excerpts_sha256': excerpts['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'summary': {
            'ziwei_atom_rows': len(ziwei_rows),
            'bazi_atom_rows': len(rows) - len(ziwei_rows),
            'exact_endpoint_direct_support_without_parent': sum('EXACT_ENDPOINT_DIRECT_SUPPORT_WITHOUT_DIRECT_ENDPOINT_PARENT' in row['defect_ids'] for row in ziwei_rows),
            'neutral_time_direct_support_rows': sum('NEUTRAL_TIME_USED_IN_DIRECT_EVENT_SUPPORT' in row['defect_ids'] for row in ziwei_rows),
            'direct_support_without_direct_score_parent': sum('DIRECT_SUPPORT_WITHOUT_DIRECT_SCORE_PARENT' in row['defect_ids'] for row in ziwei_rows),
            'scene_only_rows': sum('SCENE_ONLY_MUST_NOT_COUNT_AS_POSITIVE_COVERAGE' in row['defect_ids'] for row in ziwei_rows),
            'fail_closed_ziwei_rows': sum(bool(row['defect_ids']) for row in ziwei_rows),
        },
        'status': 'FAIL_CLOSED_FOR_R12_DIRECTION_REUSE',
    })


def build_pairwise_legality_audit(pairwise: dict[str, Any], atom_audit: dict[str, Any]) -> dict[str, Any]:
    atom_index = {row['atom_id']: row for row in atom_audit['rows']}
    rows = []
    for pair in pairwise['rows']:
        left_ids = pair['left_atom_direction_parent_ids']
        right_ids = pair['right_atom_direction_parent_ids']
        winner_ids = left_ids if pair['winner'] == pair['left'] else right_ids
        loser_ids = right_ids if pair['winner'] == pair['left'] else left_ids
        winner_defects = sorted({defect for atom_id in winner_ids for defect in atom_index[atom_id]['defect_ids']})
        loser_defects = sorted({defect for atom_id in loser_ids for defect in atom_index[atom_id]['defect_ids']})
        pair_defects: list[str] = []
        if pair['decision_basis'] == 'SCENE_ONLY_COVERAGE':
            pair_defects.append('SCENE_ONLY_USED_AS_POSITIVE_DECISION_BASIS')
        if pair['decision_basis'] == 'DISTINCTIVE_DIRECT_SUPPORT' and winner_defects:
            pair_defects.append('WINNER_DIRECT_SUPPORT_CONTAINS_CAPABILITY_VIOLATION')
        left_remaining = len(pair['left_metrics']['remaining_atom_ids'])
        right_remaining = len(pair['right_metrics']['remaining_atom_ids'])
        if pair['decision_basis'] == 'EXACT_ENDPOINT_DISTANCE' and left_remaining != right_remaining:
            pair_defects.append('RAW_MISSING_ENDPOINT_COUNT_COMPARES_UNEQUAL_COMPOUND_LENGTHS')
        rows.append({
            'case_id': CASE_ID,
            'question_id': pair['question_id'],
            'left': pair['left'],
            'right': pair['right'],
            'r12_winner': pair['winner'],
            'r12_decision_basis': pair['decision_basis'],
            'winner_atom_ids': winner_ids,
            'loser_atom_ids': loser_ids,
            'winner_atom_defect_ids': winner_defects,
            'loser_atom_defect_ids': loser_defects,
            'left_remaining_atom_count': left_remaining,
            'right_remaining_atom_count': right_remaining,
            'pair_defect_ids': pair_defects,
            'legal_replay_status': 'FAIL_CLOSED' if pair_defects else 'PASS_UNDER_R13_AUDIT',
            'winner_change_permission': 'NO_R13_DIAGNOSTIC_ONLY',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R13-PAIRWISE-LEGALITY-AUDIT-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R13',
        'parent_r12_pairwise_sha256': pairwise['canonical_sha256'],
        'parent_atom_audit_sha256': atom_audit['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'summary': {
            'scene_only_decision_rows': sum('SCENE_ONLY_USED_AS_POSITIVE_DECISION_BASIS' in row['pair_defect_ids'] for row in rows),
            'winner_direct_support_capability_violation_rows': sum('WINNER_DIRECT_SUPPORT_CONTAINS_CAPABILITY_VIOLATION' in row['pair_defect_ids'] for row in rows),
            'unequal_compound_raw_endpoint_count_rows': sum('RAW_MISSING_ENDPOINT_COUNT_COMPARES_UNEQUAL_COMPOUND_LENGTHS' in row['pair_defect_ids'] for row in rows),
            'fail_closed_pairwise_rows': sum(bool(row['pair_defect_ids']) for row in rows),
            'legally_replayable_rows': sum(not row['pair_defect_ids'] for row in rows),
        },
        'status': 'FAIL_CLOSED_FOR_SELECTION_CHANGE',
    })


def build_regression_diagnosis(r11_prediction: dict[str, Any], r12_prediction: dict[str, Any], review: dict[str, Any], pair_audit: dict[str, Any]) -> dict[str, Any]:
    old_case = next(row for row in r11_prediction['cases'] if row['case_id'] == CASE_ID)
    new_case = next(row for row in r12_prediction['cases'] if row['case_id'] == CASE_ID)
    answer = review['answer_vectors'][CASE_ID]
    pair_rows = pair_audit['rows']
    rows = []
    for index, (old_rank, new_rank, correct) in enumerate(zip(old_case['ranks'], new_case['ranks'], answer), 1):
        qid = f'Q{index}'
        q_failures = [row for row in pair_rows if row['question_id'] == qid and row['pair_defect_ids']]
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'r11_rank': old_rank,
            'r12_rank': new_rank,
            'literal_answer': correct,
            'r11_top1_correct': old_rank[0] == correct,
            'r12_top1_correct': new_rank[0] == correct,
            'r11_top2_covered': correct in old_rank[:2],
            'r12_top2_covered': correct in new_rank[:2],
            'rank_changed': old_rank != new_rank,
            'fail_closed_pairwise_count': len(q_failures),
            'pairwise_defect_ids': sorted({defect for row in q_failures for defect in row['pair_defect_ids']}),
            'learning_classification': 'SOURCE_CONFIRMED_EXECUTION_DEFECT' if q_failures else 'OPEN_RESEARCH_QUESTION',
            'direction_change_authorized': False,
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R13-REGRESSION-DIAGNOSIS-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R13',
        'parent_r11_prediction_sha256': r11_prediction['canonical_sha256'],
        'parent_r12_prediction_sha256': r12_prediction['canonical_sha256'],
        'parent_r12_review_sha256': review['canonical_sha256'],
        'parent_pairwise_audit_sha256': pair_audit['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'score_change': review['comparison_to_r11'],
        'knowledge_defect_proven': False,
        'reproducible_interface_defect_proven': True,
        'conclusion': 'The R12 score regression is preserved. Source and pairwise audits prove generic capability-propagation and burden-comparison defects, but the revealed answer cannot authorize any option promotion or astrological direction change.',
    })


def build_generic_fix() -> dict[str, Any]:
    return with_hash({
        'schema': 'DEV-GROUP-002-R13-GENERIC-FIX-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R13',
        'fix_id': 'TR-R13-CAPABILITY-CEILING-SCENE-NEUTRALITY-COMPOUND-BURDEN',
        'defect_class': 'SOURCE_CAPABILITY_AND_COMPOUND_COMPARISON_PROPAGATION',
        'general_rules': [
            'An exact diagnosis, disability, occupation, ownership, legal status, death, dated event, procedure or asset action cannot be marked DIRECT_SUPPORT unless at least one correctly selected source parent has direct endpoint authority for that same atom.',
            'A neutral-time parent can permit or activate a stage but cannot create DIRECT_SUPPORT for actual occurrence.',
            'LIMITED_SCENE_ONLY is an alternative explanation or mechanism context. It contributes zero to distinctive direct support, partial support and positive coverage.',
            'Exact-endpoint distance cannot be compared as an unnormalized raw count when the two compound options contain different numbers of remaining material atoms.',
            'A pairwise winner is fail-closed when its decisive direct-support atoms violate the source capability ceiling.',
            'Postreveal answers may classify the defect and measure its outcome effect, but cannot change an atom direction, winner, rank or source rule.',
        ],
        'required_next_replay': 'R14_RECOMPUTE_DEV_EXAMPLE_003_WITH_GENERIC_RULES_BEFORE_ANSWER_ACCESS',
        'base_astrological_knowledge_changed': False,
        'case_specific_direction_rule_added': False,
        's00_s19_modified': False,
        'impact_scope': 'GENERIC_RUNTIME_DIRECTION_PROPAGATION_AND_PAIRWISE_ADJUDICATION_ONLY',
    })


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    r11_prediction = read_json(repo_root / INPUTS['r11_prediction'])
    matrix = read_json(repo_root / INPUTS['r12_matrix'])
    pairwise = read_json(repo_root / INPUTS['r12_pairwise'])
    r12_prediction = read_json(repo_root / INPUTS['r12_prediction'])
    review = read_json(repo_root / INPUTS['r12_review'])
    excerpts = read_json(repo_root / INPUTS['r12_excerpts'])
    atom_audit = build_atom_capability_audit(matrix, excerpts)
    pair_audit = build_pairwise_legality_audit(pairwise, atom_audit)
    diagnosis = build_regression_diagnosis(r11_prediction, r12_prediction, review, pair_audit)
    generic_fix = build_generic_fix()
    preservation = with_hash({
        'schema': 'DEV-GROUP-002-R13-PREDICTION-PRESERVATION-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R13',
        'parent_r12_prediction_sha256': r12_prediction['canonical_sha256'],
        'cases': r12_prediction['cases'],
        'question_count': 25,
        'selection_changed': False,
        'top1_hits': review['totals']['top1_hits'],
        'top2_coverage': review['totals']['top2_coverage'],
        'formal_exact_assertion_permission': 'NULL_ONLY',
        'new_case_admission': 'BLOCKED',
    })
    base = {
        'atom-capability-audit.json': atom_audit,
        'pairwise-legality-audit.json': pair_audit,
        'regression-diagnosis.json': diagnosis,
        'generic-fix.json': generic_fix,
        'prediction-preservation.json': preservation,
    }
    history = {rid: {'path': path, 'git_blob_sha': git_blob_sha(repo_root / path), 'preserved': True} for rid, path in HISTORY.items()}
    artifacts = {name.removesuffix('.json').replace('-', '_'): {'path': str(ROUND_DIR / name), 'canonical_sha256': obj['canonical_sha256']} for name, obj in base.items()}
    manifest = with_hash({
        'schema': 'DEV-GROUP-002-R13-FROZEN-MANIFEST-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R13',
        'status': 'FROZEN_R12_LEGALITY_DIAGNOSIS_NO_SELECTION_CHANGE',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD_DIAGNOSIS',
        'historical_rounds': history,
        'artifacts': artifacts,
        'statistics': {
            'question_count': 25,
            'diagnosed_case_count': 1,
            'diagnosed_question_count': 5,
            **atom_audit['summary'],
            **pair_audit['summary'],
            'top1_hits': review['totals']['top1_hits'],
            'top2_coverage': review['totals']['top2_coverage'],
            'formal_valid_questions': 0,
            'machine_valid_local_seals': 0,
            's03_fusions': 0,
        },
        'training_conclusion': 'R13 preserves every R12 selection and score. It proves generic capability-ceiling, neutral-time, scene-only and unequal-compound burden defects; it does not infer the correct option from the answer.',
        'next_required_round': 'R14_RECOMPUTE_DEV_EXAMPLE_003_WITH_GENERIC_RULES_BEFORE_ANSWER_ACCESS',
        'new_case_admission': 'BLOCKED',
        'selection_change_permission': 'NO_UNTIL_R14_CLEAN_REPLAY',
        'base_astrological_knowledge_changed': False,
        'case_specific_direction_rule_added': False,
        's00_s19_modified': False,
    })
    base['manifest.json'] = manifest
    return base


def materialize(repo_root: Path) -> None:
    out = repo_root / ROUND_DIR
    out.mkdir(parents=True, exist_ok=True)
    objects = build_objects(repo_root)
    for name, obj in objects.items():
        write_json(out / name, obj)
    stats = objects['manifest.json']['statistics']
    summary = f'''# DEV-GROUP-002 R13：R12能力上限与成对合法性诊断\n\nR13不改变R12的任何选择，组级同题训练回归继续为TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。\n\n本轮逐条审计R12的178条双轨原子方向及30组成对行。审计检查精确终点是否具有直接终点父权威、中立时间是否被升级为实际发生、场景限制是否被当作正向覆盖，以及不同长度复合选项是否用原始缺口数比较。\n\n已证明的是通用执行接口缺陷，不是命理知识缺陷。R14必须在看答案前应用统一修复并重新计算第3案；正确答案不得决定降级对象、成对赢家或排序。\n'''
    (out / 'summary.md').write_text(summary, encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    out = repo_root / ROUND_DIR
    names = ['atom-capability-audit.json', 'pairwise-legality-audit.json', 'regression-diagnosis.json', 'generic-fix.json', 'prediction-preservation.json', 'manifest.json']
    objects: dict[str, dict[str, Any]] = {}
    for name in names:
        if not (out / name).exists():
            errors.append(f'missing {name}')
        else:
            objects[name] = read_json(out / name)
    if errors:
        return {'status': 'FAIL', 'error_count': len(errors), 'errors': errors}
    for name, obj in objects.items():
        if canonical_hash(obj) != obj.get('canonical_sha256'):
            errors.append(f'{name}: canonical hash mismatch')
    atom = objects['atom-capability-audit.json']
    pair = objects['pairwise-legality-audit.json']
    diagnosis = objects['regression-diagnosis.json']
    generic = objects['generic-fix.json']
    preservation = objects['prediction-preservation.json']
    manifest = objects['manifest.json']
    if atom['row_count'] != 178 or atom['summary']['ziwei_atom_rows'] != 89 or atom['summary']['bazi_atom_rows'] != 89:
        errors.append('atom audit row count')
    for field in ('exact_endpoint_direct_support_without_parent', 'direct_support_without_direct_score_parent', 'scene_only_rows', 'fail_closed_ziwei_rows'):
        if atom['summary'][field] <= 0:
            errors.append(f'atom audit failed to detect {field}')
    if pair['row_count'] != 30:
        errors.append('pair audit row count')
    for field in ('scene_only_decision_rows', 'winner_direct_support_capability_violation_rows', 'unequal_compound_raw_endpoint_count_rows', 'fail_closed_pairwise_rows'):
        if pair['summary'][field] <= 0:
            errors.append(f'pair audit failed to detect {field}')
    if diagnosis['knowledge_defect_proven'] is not False or diagnosis['reproducible_interface_defect_proven'] is not True:
        errors.append('diagnosis classification')
    if any(row['direction_change_authorized'] for row in diagnosis['rows']):
        errors.append('answer-derived direction change')
    if preservation['selection_changed'] is not False or (preservation['top1_hits'], preservation['top2_coverage']) != (11, 14):
        errors.append('prediction preservation')
    rule_text = '\n'.join(generic['general_rules'])
    if any(token in rule_text for token in ('DEV-EXAMPLE-003', 'BBDCA', 'Q1', 'Q2', 'Q5')):
        errors.append('case token leaked into generic rules')
    if generic['base_astrological_knowledge_changed'] is not False or generic['case_specific_direction_rule_added'] is not False:
        errors.append('unauthorized generic fix')
    if manifest['status'] != 'FROZEN_R12_LEGALITY_DIAGNOSIS_NO_SELECTION_CHANGE':
        errors.append('manifest status')
    if manifest['selection_change_permission'] != 'NO_UNTIL_R14_CLEAN_REPLAY':
        errors.append('selection gate')
    stats = manifest['statistics']
    if (stats['top1_hits'], stats['top2_coverage'], stats['formal_valid_questions'], stats['machine_valid_local_seals'], stats['s03_fusions']) != (11, 14, 0, 0, 0):
        errors.append('manifest formal statistics')
    for rid, row in manifest['historical_rounds'].items():
        if row['path'] != HISTORY[rid] or git_blob_sha(repo_root / HISTORY[rid]) != row['git_blob_sha'] or row['preserved'] is not True:
            errors.append(f'history {rid}')
    return {
        'schema': 'DEV-GROUP-002-R13-VALIDATION-V1',
        'status': 'PASS' if not errors else 'FAIL',
        'error_count': len(errors),
        'errors': errors,
        'historical_rounds_preserved': list(HISTORY),
        'diagnosed_case_id': CASE_ID,
        **atom['summary'],
        **pair['summary'],
        'selection_changed': False,
        'top1_hits': 11,
        'top2_coverage': 14,
        'formal_valid_questions': 0,
        'machine_valid_local_seals': 0,
        's03_fusions': 0,
        'base_astrological_knowledge_changed': False,
        's00_s19_modified': False,
        'new_case_admission': 'BLOCKED',
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if not args.write and not args.validate:
        parser.error('select --write and/or --validate')
    if args.write:
        materialize(root)
    if args.validate:
        result = validate(root)
        out = root / ROUND_DIR
        out.mkdir(parents=True, exist_ok=True)
        write_json(out / 'validation.json', result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result['status'] == 'PASS' else 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
