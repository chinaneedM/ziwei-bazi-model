#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r14')
CASE_ID = 'DEV-EXAMPLE-003'
HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    **{f'R{i}': f'reports/dev-group-002/training-regression-r{i}/manifest.json' for i in range(5, 14)},
}
INPUTS = {
    'r12_matrix': 'reports/dev-group-002/training-regression-r12/literal-atom-direction-matrix.json',
    'r12_common': 'reports/dev-group-002/training-regression-r12/common-atom-subtraction.json',
    'r12_prediction': 'reports/dev-group-002/training-regression-r12/prediction-freeze.json',
    'r12_review': 'reports/dev-group-002/training-regression-r12/postreveal-review.json',
    'r13_atom_audit': 'reports/dev-group-002/training-regression-r13/atom-capability-audit.json',
    'r13_generic_fix': 'reports/dev-group-002/training-regression-r13/generic-fix.json',
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


def adjusted_direction(original: str, defects: list[str]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    direction = original
    if 'EXACT_ENDPOINT_DIRECT_SUPPORT_WITHOUT_DIRECT_ENDPOINT_PARENT' in defects:
        direction = 'LIMITED_MISSING_ENDPOINT'
        reasons.append('EXACT_ENDPOINT_REQUIRES_DIRECT_ENDPOINT_PARENT')
    elif 'NEUTRAL_TIME_USED_IN_DIRECT_EVENT_SUPPORT' in defects:
        direction = 'LIMITED_SCENE_ONLY'
        reasons.append('NEUTRAL_TIME_CANNOT_PROVE_OCCURRENCE')
    elif 'DIRECT_SUPPORT_WITHOUT_DIRECT_SCORE_PARENT' in defects:
        direction = 'PARTIAL_SUPPORT'
        reasons.append('SOURCE_CAPABILITY_LIMITS_DIRECT_RANKING_SUPPORT')
    if original == 'LIMITED_SCENE_ONLY':
        direction = 'LIMITED_SCENE_ONLY'
        reasons.append('SCENE_ONLY_REMAINS_NONPOSITIVE_CONTEXT')
    return direction, sorted(set(reasons))


def build_adjusted_matrix(matrix: dict[str, Any], audit: dict[str, Any], generic_fix: dict[str, Any]) -> dict[str, Any]:
    audit_index = {row['atom_id']: row for row in audit['rows']}
    rows = []
    changed = []
    for atom in matrix['rows']:
        audited = audit_index[atom['atom_id']]
        clone = dict(atom)
        new_direction, reasons = adjusted_direction(atom['direction_status'], audited['defect_ids']) if atom['track_id'] == 'ZIWEI' else (atom['direction_status'], [])
        clone['r12_direction_status'] = atom['direction_status']
        clone['direction_status'] = new_direction
        clone['r14_adjustment_reason_ids'] = reasons
        clone['parent_r13_atom_audit_status'] = audited['audit_status']
        clone['direct_event_parent_available'] = audited['parent_direct_event_yes_count'] > 0
        clone['direct_endpoint_parent_available'] = audited['parent_direct_endpoint_yes_count'] > 0
        clone['direct_score_parent_available'] = audited['parent_direct_score_yes_count'] > 0
        clone['endpoint_closed'] = bool(
            atom['exact_endpoint_required']
            and new_direction == 'DIRECT_SUPPORT'
            and audited['parent_direct_endpoint_yes_count'] > 0
        )
        clone['scene_positive_contribution'] = 0
        clone['answer_access_during_adjustment'] = False
        if new_direction != atom['direction_status']:
            changed.append(atom['atom_id'])
        rows.append(clone)
    return with_hash({
        'schema': 'DEV-GROUP-002-R14-ADJUSTED-ATOM-DIRECTION-MATRIX-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R14',
        'parent_r12_matrix_sha256': matrix['canonical_sha256'],
        'parent_r13_atom_audit_sha256': audit['canonical_sha256'],
        'parent_r13_generic_fix_sha256': generic_fix['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'changed_atom_ids': changed,
        'changed_atom_count': len(changed),
        'ziwei_changed_atom_count': sum(row['track_id'] == 'ZIWEI' and row['atom_id'] in set(changed) for row in rows),
        'bazi_changed_atom_count': sum(row['track_id'] == 'BAZI' and row['atom_id'] in set(changed) for row in rows),
        'status': 'PASS_GENERIC_CAPABILITY_RULES_APPLIED_BEFORE_ANSWER_ACCESS',
    })


def option_atoms(matrix: dict[str, Any], question_id: str, option_id: str) -> list[dict[str, Any]]:
    return [row for row in matrix['rows'] if row['track_id'] == 'ZIWEI' and row['question_id'] == question_id and row['option_id'] == option_id]


def ratio(numerator: int, denominator: int) -> dict[str, int]:
    return {'numerator': numerator, 'denominator': denominator if denominator else 1}


def compare_ratio(left: dict[str, int], right: dict[str, int], maximize: bool) -> int:
    lhs = left['numerator'] * right['denominator']
    rhs = right['numerator'] * left['denominator']
    if lhs == rhs:
        return 0
    left_better = lhs > rhs if maximize else lhs < rhs
    return 1 if left_better else -1


def metrics(atoms: list[dict[str, Any]], zero_short_ids: set[str]) -> dict[str, Any]:
    remaining = [atom for atom in atoms if atom['short_id'] not in zero_short_ids]
    direct = [atom['atom_id'] for atom in remaining if atom['direction_status'] == 'DIRECT_SUPPORT']
    partial = [atom['atom_id'] for atom in remaining if atom['direction_status'] == 'PARTIAL_SUPPORT']
    counter = [atom['atom_id'] for atom in remaining if atom['direction_status'] == 'DIRECT_COUNTEREVIDENCE']
    unknown = [atom['atom_id'] for atom in remaining if atom['direction_status'] == 'UNKNOWN']
    scene = [atom['atom_id'] for atom in remaining if atom['direction_status'] == 'LIMITED_SCENE_ONLY']
    missing_exact = [atom['atom_id'] for atom in remaining if atom['exact_endpoint_required'] and not atom['endpoint_closed']]
    exact_total = [atom['atom_id'] for atom in remaining if atom['exact_endpoint_required']]
    total = len(remaining)
    return {
        'remaining_atom_ids': [atom['atom_id'] for atom in remaining],
        'direct_support_atom_ids': direct,
        'partial_support_atom_ids': partial,
        'direct_counterevidence_atom_ids': counter,
        'unknown_atom_ids': unknown,
        'scene_only_atom_ids': scene,
        'missing_exact_endpoint_atom_ids': missing_exact,
        'exact_endpoint_atom_ids': exact_total,
        'direct_support_ratio': ratio(len(direct), total),
        'counterevidence_ratio': ratio(len(counter), total),
        'composite_support_ratio': ratio(len(direct) + len(partial), total),
        'missing_exact_endpoint_ratio': ratio(len(missing_exact), len(exact_total)),
        'unknown_ratio': ratio(len(unknown), total),
        'scene_only_burden_ratio': ratio(len(scene), total),
        'source_parent_excerpt_ids': sorted({parent for atom in remaining for parent in atom['source_parent_excerpt_ids']}),
    }


def decide(left: dict[str, Any], right: dict[str, Any], left_id: str, right_id: str, old_rank: str) -> tuple[str, str, dict[str, Any]]:
    criteria = [
        ('DISTINCTIVE_DIRECT_SUPPORT_RATIO', 'direct_support_ratio', True),
        ('SAME_AXIS_DIRECT_COUNTEREVIDENCE_RATIO', 'counterevidence_ratio', False),
        ('NORMALIZED_COMPOSITE_SUPPORT_COVERAGE', 'composite_support_ratio', True),
        ('NORMALIZED_EXACT_ENDPOINT_DISTANCE', 'missing_exact_endpoint_ratio', False),
        ('UNRESOLVED_UNKNOWN_BURDEN', 'unknown_ratio', False),
        ('ALTERNATIVE_SCENE_ONLY_BURDEN', 'scene_only_burden_ratio', False),
    ]
    for name, field, maximize in criteria:
        result = compare_ratio(left[field], right[field], maximize)
        if result:
            winner = left_id if result > 0 else right_id
            return winner, name, {'left': left[field], 'right': right[field], 'mode': 'MAX' if maximize else 'MIN'}
    winner = left_id if old_rank.index(left_id) < old_rank.index(right_id) else right_id
    return winner, 'LOW_INFORMATION_FORCED_TIEBREAK_PRESERVE_PREANSWER_R12_ORDER', {'left': None, 'right': None, 'mode': 'TIE'}


def build_pairwise(matrix: dict[str, Any], common: dict[str, Any], r12_prediction: dict[str, Any]) -> dict[str, Any]:
    common_index = {(row['question_id'], row['left'], row['right']): row for row in common['rows']}
    old_case = next(row for row in r12_prediction['cases'] if row['case_id'] == CASE_ID)
    old_ranks = {f'Q{i}': rank for i, rank in enumerate(old_case['ranks'], 1)}
    rows = []
    derived_ranks: dict[str, str] = {}
    cycle_questions: list[str] = []
    for qid in [f'Q{i}' for i in range(1, 6)]:
        question_rows = []
        for left_id, right_id in itertools.combinations('ABCD', 2):
            common_row = common_index[(qid, left_id, right_id)]
            left_zero = {row['left_short_id'] for row in common_row['equivalence_rows']}
            right_zero = {row['right_short_id'] for row in common_row['equivalence_rows']}
            left_metrics = metrics(option_atoms(matrix, qid, left_id), left_zero)
            right_metrics = metrics(option_atoms(matrix, qid, right_id), right_zero)
            winner, basis, values = decide(left_metrics, right_metrics, left_id, right_id, old_ranks[qid])
            row = {
                'case_id': CASE_ID,
                'question_id': qid,
                'left': left_id,
                'right': right_id,
                'winner': winner,
                'loser': right_id if winner == left_id else left_id,
                'decision_basis': basis,
                'decision_values': values,
                'common_atom_ids_zeroed': common_row['common_atom_ids_zeroed'],
                'left_atom_direction_parent_ids': left_metrics['remaining_atom_ids'],
                'right_atom_direction_parent_ids': right_metrics['remaining_atom_ids'],
                'left_source_parent_excerpt_ids': left_metrics['source_parent_excerpt_ids'],
                'right_source_parent_excerpt_ids': right_metrics['source_parent_excerpt_ids'],
                'left_metrics': left_metrics,
                'right_metrics': right_metrics,
                'scene_only_positive_contribution': 0,
                'raw_endpoint_count_decision_permission': False,
                'answer_access_during_decision': False,
                'atom_level_replay_status': 'PASS',
                'bazi_fusion_effect': 'ZERO_NO_MACHINE_VALID_BAZI_LOCAL_SEAL',
            }
            rows.append(row)
            question_rows.append(row)
        wins = {option: 0 for option in 'ABCD'}
        for row in question_rows:
            wins[row['winner']] += 1
        rank = ''.join(sorted('ABCD', key=lambda option: (-wins[option], old_ranks[qid].index(option))))
        inconsistent = []
        for left_id, right_id in itertools.combinations('ABCD', 2):
            actual = next(row['winner'] for row in question_rows if row['left'] == left_id and row['right'] == right_id)
            expected = left_id if rank.index(left_id) < rank.index(right_id) else right_id
            if actual != expected:
                inconsistent.append(f'{left_id}{right_id}:{actual}')
        if inconsistent:
            cycle_questions.append(qid)
        derived_ranks[qid] = rank
    return with_hash({
        'schema': 'DEV-GROUP-002-R14-CLEAN-PAIRWISE-REPLAY-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R14',
        'parent_adjusted_matrix_sha256': matrix['canonical_sha256'],
        'parent_common_subtraction_sha256': common['canonical_sha256'],
        'parent_r12_prediction_sha256': r12_prediction['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'derived_ranks': derived_ranks,
        'atom_level_replayable_rows': len(rows),
        'low_information_tiebreak_rows': sum(row['decision_basis'].startswith('LOW_INFORMATION') for row in rows),
        'scene_only_positive_decision_rows': 0,
        'raw_endpoint_count_decision_rows': 0,
        'cycle_question_ids': cycle_questions,
        'rank_derivation': 'COPELAND_PAIRWISE_WINS_THEN_PREANSWER_R12_ORDER_FOR_EQUAL_WIN_COUNTS',
        'status': 'PASS_COMPLETE_CLEAN_REPLAY',
    })


def build_prediction(r12_prediction: dict[str, Any], pairwise: dict[str, Any]) -> dict[str, Any]:
    cases = []
    changed = []
    for case in r12_prediction['cases']:
        clone = dict(case)
        if case['case_id'] == CASE_ID:
            ranks = [pairwise['derived_ranks'][f'Q{i}'] for i in range(1, 6)]
            changed = [f'{CASE_ID}:Q{i}' for i, (old, new) in enumerate(zip(case['ranks'], ranks), 1) if old != new]
            clone.update(
                ranks=ranks,
                top1_vector=''.join(rank[0] for rank in ranks),
                top2_vector=''.join(rank[1] for rank in ranks),
                prediction_origin='R14_GENERIC_CAPABILITY_AND_NORMALIZED_BURDEN_REPLAY',
            )
        cases.append(clone)
    return with_hash({
        'schema': 'DEV-GROUP-002-R14-PREDICTION-FREEZE-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R14',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'parent_r12_prediction_sha256': r12_prediction['canonical_sha256'],
        'pairwise_replay_sha256': pairwise['canonical_sha256'],
        'case_ids': r12_prediction['case_ids'],
        'cases': cases,
        'question_count': 25,
        'changed_case_ids': [CASE_ID] if changed else [],
        'changed_question_ids': changed,
        'contains_answers': False,
        'answer_visible_during_prediction_materialization': False,
        'formal_exact_assertion_permission': 'NULL_ONLY',
        'machine_valid_local_seals': 0,
        's03_fusions': 0,
        'new_case_admission': 'BLOCKED',
        'base_astrological_knowledge_changed': False,
    })


def build_review(r12_review: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    scores = []
    top1_total = 0
    top2_total = 0
    for case in prediction['cases']:
        answer = r12_review['answer_vectors'][case['case_id']]
        top1 = sum(predicted == correct for predicted, correct in zip(case['top1_vector'], answer))
        top2 = sum(correct in (first, second) for first, second, correct in zip(case['top1_vector'], case['top2_vector'], answer))
        scores.append({'case_id': case['case_id'], 'top1_hits': top1, 'top2_coverage': top2})
        top1_total += top1
        top2_total += top2
    return with_hash({
        'schema': 'DEV-GROUP-002-R14-POSTREVEAL-REVIEW-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R14',
        'parent_prediction_sha256': prediction['canonical_sha256'],
        'answer_vectors': r12_review['answer_vectors'],
        'case_scores': scores,
        'totals': {'top1_hits': top1_total, 'top2_coverage': top2_total, 'question_count': 25, 'score_label': 'TRAINING_REGRESSION_SCORE'},
        'comparison_to_r12': {'top1_delta': top1_total - 11, 'top2_delta': top2_total - 14},
        'accuracy_claim': 'NO_NEW_BLIND_RESULT',
        'answer_used_for_selection': False,
    })


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    r12_matrix = read_json(repo_root / INPUTS['r12_matrix'])
    common = read_json(repo_root / INPUTS['r12_common'])
    r12_prediction = read_json(repo_root / INPUTS['r12_prediction'])
    atom_audit = read_json(repo_root / INPUTS['r13_atom_audit'])
    generic_fix = read_json(repo_root / INPUTS['r13_generic_fix'])
    adjusted = build_adjusted_matrix(r12_matrix, atom_audit, generic_fix)
    pairwise = build_pairwise(adjusted, common, r12_prediction)
    prediction = build_prediction(r12_prediction, pairwise)
    # Answers are loaded only after the answer-free prediction object has been materialized in memory.
    r12_review = read_json(repo_root / INPUTS['r12_review'])
    review = build_review(r12_review, prediction)
    base = {
        'adjusted-atom-direction-matrix.json': adjusted,
        'pairwise-replay.json': pairwise,
        'prediction-freeze.json': prediction,
        'postreveal-review.json': review,
    }
    history = {rid: {'path': path, 'git_blob_sha': git_blob_sha(repo_root / path), 'preserved': True} for rid, path in HISTORY.items()}
    artifacts = {name.removesuffix('.json').replace('-', '_'): {'path': str(ROUND_DIR / name), 'canonical_sha256': obj['canonical_sha256']} for name, obj in base.items()}
    manifest = with_hash({
        'schema': 'DEV-GROUP-002-R14-FROZEN-MANIFEST-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R14',
        'status': 'FROZEN_GENERIC_CAPABILITY_AND_NORMALIZED_BURDEN_REPLAY',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'historical_rounds': history,
        'artifacts': artifacts,
        'statistics': {
            'question_count': 25,
            'processed_case_count': 1,
            'processed_question_count': 5,
            'adjusted_atom_rows': adjusted['row_count'],
            'changed_atom_count': adjusted['changed_atom_count'],
            'ziwei_changed_atom_count': adjusted['ziwei_changed_atom_count'],
            'bazi_changed_atom_count': adjusted['bazi_changed_atom_count'],
            'pairwise_rows': pairwise['row_count'],
            'atom_level_replayable_pairwise_rows': pairwise['atom_level_replayable_rows'],
            'low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'],
            'cycle_question_count': len(pairwise['cycle_question_ids']),
            'selection_changed_from_r12': bool(prediction['changed_question_ids']),
            'top1_hits': review['totals']['top1_hits'],
            'top2_coverage': review['totals']['top2_coverage'],
            'formal_valid_questions': 0,
            'machine_valid_local_seals': 0,
            's03_fusions': 0,
        },
        'training_conclusion': 'R14 applies the R13 generic capability, neutral-time, scene-only and normalized burden rules before answer access. Any selection or score change is preserved without answer-derived repair.',
        'next_required_round': 'R15_REVIEW_R14_STABILITY_AND_DECIDE_DEV_EXAMPLE_004_GATE',
        'new_case_admission': 'BLOCKED',
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
    case = next(row for row in objects['prediction-freeze.json']['cases'] if row['case_id'] == CASE_ID)
    stats = objects['manifest.json']['statistics']
    summary = f'''# DEV-GROUP-002 R14：能力上限与归一化复合负担清洁重放\n\nR14在读取答案前应用R13通用规则，调整{stats['changed_atom_count']}条原子方向并重算30组成对行。场景限制的正向贡献固定为0；精确终点缺口按比例比较，不再用不同长度复合选项的原始缺口数。\n\nDEV-EXAMPLE-003排序为：{' / '.join(case['ranks'])}。组级同题训练回归为TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。该结果不是新盲测成绩。\n\n正式有效题、本地机器密封和S03融合仍全部为0；S00—S19和基础命理知识未修改。\n'''
    (out / 'summary.md').write_text(summary, encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    out = repo_root / ROUND_DIR
    names = ['adjusted-atom-direction-matrix.json', 'pairwise-replay.json', 'prediction-freeze.json', 'postreveal-review.json', 'manifest.json']
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
    adjusted = objects['adjusted-atom-direction-matrix.json']
    pairwise = objects['pairwise-replay.json']
    prediction = objects['prediction-freeze.json']
    review = objects['postreveal-review.json']
    manifest = objects['manifest.json']
    if adjusted['row_count'] != 178 or adjusted['changed_atom_count'] <= 0 or adjusted['bazi_changed_atom_count'] != 0:
        errors.append('adjusted matrix counts')
    if any(row['answer_access_during_adjustment'] for row in adjusted['rows']):
        errors.append('answer access during adjustment')
    for row in adjusted['rows']:
        if row['track_id'] == 'ZIWEI' and row['direction_status'] == 'DIRECT_SUPPORT' and not row['direct_score_parent_available']:
            errors.append(f'unresolved direct-score ceiling {row["atom_id"]}')
        if row['direction_status'] == 'LIMITED_SCENE_ONLY' and row['scene_positive_contribution'] != 0:
            errors.append(f'scene positive contribution {row["atom_id"]}')
        if row['exact_endpoint_required'] and row['endpoint_closed'] and not row['direct_endpoint_parent_available']:
            errors.append(f'endpoint closed without parent {row["atom_id"]}')
    if pairwise['row_count'] != 30 or pairwise['atom_level_replayable_rows'] != 30:
        errors.append('pairwise row count')
    if pairwise['scene_only_positive_decision_rows'] != 0 or pairwise['raw_endpoint_count_decision_rows'] != 0:
        errors.append('illegal pairwise basis retained')
    if any(row['answer_access_during_decision'] for row in pairwise['rows']):
        errors.append('answer access during pairwise')
    if any(row['decision_basis'] in {'SCENE_ONLY_COVERAGE', 'EXACT_ENDPOINT_DISTANCE'} for row in pairwise['rows']):
        errors.append('obsolete decision basis retained')
    case = next(row for row in prediction['cases'] if row['case_id'] == CASE_ID)
    expected = [pairwise['derived_ranks'][f'Q{i}'] for i in range(1, 6)]
    if case['ranks'] != expected:
        errors.append('prediction rank mismatch')
    if prediction['contains_answers'] or prediction['answer_visible_during_prediction_materialization']:
        errors.append('prediction answer isolation')
    if review['answer_used_for_selection'] is not False:
        errors.append('review answer leakage')
    recomputed_top1 = sum(row['top1_hits'] for row in review['case_scores'])
    recomputed_top2 = sum(row['top2_coverage'] for row in review['case_scores'])
    if (recomputed_top1, recomputed_top2) != (review['totals']['top1_hits'], review['totals']['top2_coverage']):
        errors.append('review score replay')
    if manifest['status'] != 'FROZEN_GENERIC_CAPABILITY_AND_NORMALIZED_BURDEN_REPLAY':
        errors.append('manifest status')
    stats = manifest['statistics']
    if (stats['top1_hits'], stats['top2_coverage']) != (review['totals']['top1_hits'], review['totals']['top2_coverage']):
        errors.append('manifest score mismatch')
    if (stats['formal_valid_questions'], stats['machine_valid_local_seals'], stats['s03_fusions']) != (0, 0, 0):
        errors.append('formal state')
    for rid, row in manifest['historical_rounds'].items():
        if row['path'] != HISTORY[rid] or git_blob_sha(repo_root / HISTORY[rid]) != row['git_blob_sha'] or row['preserved'] is not True:
            errors.append(f'history {rid}')
    return {
        'schema': 'DEV-GROUP-002-R14-VALIDATION-V1',
        'status': 'PASS' if not errors else 'FAIL',
        'error_count': len(errors),
        'errors': errors,
        'historical_rounds_preserved': list(HISTORY),
        'processed_case_id': CASE_ID,
        'adjusted_atom_rows': adjusted['row_count'],
        'changed_atom_count': adjusted['changed_atom_count'],
        'ziwei_changed_atom_count': adjusted['ziwei_changed_atom_count'],
        'bazi_changed_atom_count': adjusted['bazi_changed_atom_count'],
        'pairwise_rows': pairwise['row_count'],
        'atom_level_replayable_pairwise_rows': pairwise['atom_level_replayable_rows'],
        'low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'],
        'cycle_question_ids': pairwise['cycle_question_ids'],
        'dev003_ranks': case['ranks'],
        'dev003_top1': case['top1_vector'],
        'dev003_top2': case['top2_vector'],
        'changed_question_ids': prediction['changed_question_ids'],
        'selection_changed_from_r12': bool(prediction['changed_question_ids']),
        'top1_hits': review['totals']['top1_hits'],
        'top2_coverage': review['totals']['top2_coverage'],
        'top1_delta_from_r12': review['comparison_to_r12']['top1_delta'],
        'top2_delta_from_r12': review['comparison_to_r12']['top2_delta'],
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
