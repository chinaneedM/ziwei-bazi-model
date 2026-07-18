#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r15')
HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    **{f'R{i}': f'reports/dev-group-002/training-regression-r{i}/manifest.json' for i in range(5, 15)},
}
INPUTS = {
    'r11_manifest': 'reports/dev-group-002/training-regression-r11/manifest.json',
    'r12_manifest': 'reports/dev-group-002/training-regression-r12/manifest.json',
    'r12_prediction': 'reports/dev-group-002/training-regression-r12/prediction-freeze.json',
    'r13_manifest': 'reports/dev-group-002/training-regression-r13/manifest.json',
    'r13_generic_fix': 'reports/dev-group-002/training-regression-r13/generic-fix.json',
    'r14_manifest': 'reports/dev-group-002/training-regression-r14/manifest.json',
    'r14_validation': 'reports/dev-group-002/training-regression-r14/validation.json',
    'r14_adjusted': 'reports/dev-group-002/training-regression-r14/adjusted-atom-direction-matrix.json',
    'r14_pairwise': 'reports/dev-group-002/training-regression-r14/pairwise-replay.json',
    'r14_prediction': 'reports/dev-group-002/training-regression-r14/prediction-freeze.json',
    'r14_review': 'reports/dev-group-002/training-regression-r14/postreveal-review.json',
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


def build_score_trend(r11: dict[str, Any], r12: dict[str, Any], r14: dict[str, Any]) -> dict[str, Any]:
    rows = [
        {'round_id': 'R11', 'top1_hits': r11['statistics']['top1_hits'], 'top2_coverage': r11['statistics']['top2_coverage'], 'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD'},
        {'round_id': 'R12', 'top1_hits': r12['statistics']['top1_hits'], 'top2_coverage': r12['statistics']['top2_coverage'], 'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD'},
        {'round_id': 'R14', 'top1_hits': r14['statistics']['top1_hits'], 'top2_coverage': r14['statistics']['top2_coverage'], 'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD'},
    ]
    return with_hash({
        'schema': 'DEV-GROUP-002-R15-SCORE-TREND-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R15',
        'original_blind_baseline': {'top1_hits': 11, 'top2_coverage': 16, 'question_count': 25, 'immutable': True},
        'rows': rows,
        'training_score_delta_r11_to_r14': {
            'top1': rows[-1]['top1_hits'] - rows[0]['top1_hits'],
            'top2': rows[-1]['top2_coverage'] - rows[0]['top2_coverage'],
        },
        'interpretation': 'The same-case answer-visible score worsened while execution legality improved. This is not a blind generalization estimate and cannot authorize answer-directed rule reversal.',
        'status': 'FROZEN_DIAGNOSTIC_ONLY',
    })


def build_interface_freeze(generic: dict[str, Any], adjusted: dict[str, Any], pairwise: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    changed_rows = [row for row in adjusted['rows'] if row['r14_adjustment_reason_ids']]
    invalid_changed_rows = [row['atom_id'] for row in changed_rows if row['track_id'] != 'ZIWEI' or not row['r14_adjustment_reason_ids']]
    return with_hash({
        'schema': 'DEV-GROUP-002-R15-INTERFACE-FREEZE-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R15',
        'interface_id': 'TR-R14-CAPABILITY-NEUTRAL-TIME-SCENE-NORMALIZED-BURDEN-V1',
        'parent_r13_generic_fix_sha256': generic['canonical_sha256'],
        'parent_r14_adjusted_matrix_sha256': adjusted['canonical_sha256'],
        'parent_r14_pairwise_sha256': pairwise['canonical_sha256'],
        'parent_r14_validation_git_blob_sha': validation.get('canonical_sha256'),
        'rules': generic['general_rules'],
        'track_aware_atom_key': 'TRACK_ID_PLUS_ATOM_ID',
        'changed_atom_count': adjusted['changed_atom_count'],
        'ziwei_changed_atom_count': adjusted['ziwei_changed_atom_count'],
        'bazi_changed_atom_count': adjusted['bazi_changed_atom_count'],
        'invalid_changed_atom_ids': invalid_changed_rows,
        'pairwise_rows': pairwise['row_count'],
        'atom_level_replayable_pairwise_rows': pairwise['atom_level_replayable_rows'],
        'cycle_question_ids': pairwise['cycle_question_ids'],
        'low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'],
        'scene_only_positive_decision_rows': pairwise['scene_only_positive_decision_rows'],
        'raw_endpoint_count_decision_rows': pairwise['raw_endpoint_count_decision_rows'],
        'answer_access_during_adjustment': any(row['answer_access_during_adjustment'] for row in adjusted['rows']),
        'answer_access_during_decision': any(row['answer_access_during_decision'] for row in pairwise['rows']),
        'selection_rule_change_permission_inside_fixed_group': 'NO_UNTIL_CROSS_CASE_REPLAY_EVIDENCE',
        'base_astrological_knowledge_changed': False,
        'case_specific_direction_rule_added': False,
        's00_s19_modified': False,
        'status': 'PASS_TECHNICALLY_FROZEN_FOR_CROSS_CASE_REPLAY' if not invalid_changed_rows else 'FAIL',
    })


def build_gate(interface: dict[str, Any], score_trend: dict[str, Any], r14_prediction: dict[str, Any], r14_review: dict[str, Any]) -> dict[str, Any]:
    case = next(row for row in r14_prediction['cases'] if row['case_id'] == 'DEV-EXAMPLE-003')
    return with_hash({
        'schema': 'DEV-GROUP-002-R15-CROSS-CASE-GATE-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R15',
        'interface_freeze_sha256': interface['canonical_sha256'],
        'score_trend_sha256': score_trend['canonical_sha256'],
        'dev003_r14_ranks': case['ranks'],
        'dev003_r14_top1': case['top1_vector'],
        'dev003_r14_top2': case['top2_vector'],
        'current_training_regression_score': r14_review['totals'],
        'dev_example_004_shadow_rebuild_permission': 'YES',
        'permission_basis': [
            'DEV-EXAMPLE-004_ALREADY_BELONGS_TO_FIXED_DEV_GROUP_002',
            'R14_INTERFACE_TECHNICALLY_VALIDATED',
            'CROSS_CASE_REPLAY_REQUIRED_TO_TEST_INTERFACE_STABILITY',
            'NO_NEW_ASTROLOGICAL_RULE_OR_CASE_SPECIFIC_PATCH_ALLOWED',
        ],
        'formal_release_permission': 'NO',
        'new_external_case_admission': 'BLOCKED',
        'answer_visible_score_tuning_permission': 'NO',
        'next_required_round': 'R16_APPLY_FROZEN_R14_INTERFACE_TO_DEV_EXAMPLE_004_CANONICAL_INPUTS',
        'status': 'DEV004_SHADOW_REBUILD_ALLOWED_FORMAL_RELEASE_BLOCKED',
    })


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    r11_manifest = read_json(repo_root / INPUTS['r11_manifest'])
    r12_manifest = read_json(repo_root / INPUTS['r12_manifest'])
    generic = read_json(repo_root / INPUTS['r13_generic_fix'])
    r14_manifest = read_json(repo_root / INPUTS['r14_manifest'])
    validation = read_json(repo_root / INPUTS['r14_validation'])
    adjusted = read_json(repo_root / INPUTS['r14_adjusted'])
    pairwise = read_json(repo_root / INPUTS['r14_pairwise'])
    prediction = read_json(repo_root / INPUTS['r14_prediction'])
    review = read_json(repo_root / INPUTS['r14_review'])
    score_trend = build_score_trend(r11_manifest, r12_manifest, r14_manifest)
    interface = build_interface_freeze(generic, adjusted, pairwise, validation)
    gate = build_gate(interface, score_trend, prediction, review)
    preservation = with_hash({
        'schema': 'DEV-GROUP-002-R15-PREDICTION-PRESERVATION-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R15',
        'parent_r14_prediction_sha256': prediction['canonical_sha256'],
        'cases': prediction['cases'],
        'question_count': 25,
        'selection_changed': False,
        'top1_hits': review['totals']['top1_hits'],
        'top2_coverage': review['totals']['top2_coverage'],
        'formal_exact_assertion_permission': 'NULL_ONLY',
        'new_external_case_admission': 'BLOCKED',
    })
    base = {
        'score-trend.json': score_trend,
        'interface-freeze.json': interface,
        'cross-case-gate.json': gate,
        'prediction-preservation.json': preservation,
    }
    history = {rid: {'path': path, 'git_blob_sha': git_blob_sha(repo_root / path), 'preserved': True} for rid, path in HISTORY.items()}
    artifacts = {name.removesuffix('.json').replace('-', '_'): {'path': str(ROUND_DIR / name), 'canonical_sha256': obj['canonical_sha256']} for name, obj in base.items()}
    manifest = with_hash({
        'schema': 'DEV-GROUP-002-R15-FROZEN-MANIFEST-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R15',
        'status': 'FROZEN_R14_INTERFACE_AND_DEV004_CROSS_CASE_GATE',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD_STABILITY_GATE',
        'historical_rounds': history,
        'artifacts': artifacts,
        'statistics': {
            'question_count': 25,
            'top1_hits': review['totals']['top1_hits'],
            'top2_coverage': review['totals']['top2_coverage'],
            'r14_changed_atom_count': adjusted['changed_atom_count'],
            'r14_pairwise_rows': pairwise['row_count'],
            'r14_cycle_question_count': len(pairwise['cycle_question_ids']),
            'r14_low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'],
            'formal_valid_questions': 0,
            'machine_valid_local_seals': 0,
            's03_fusions': 0,
        },
        'training_conclusion': 'The R14 interface is technically valid but its same-case answer-visible score is lower. The score cannot justify reverting generic legality rules. The frozen interface must be tested on DEV-EXAMPLE-004 before any further generic rule change.',
        'next_required_round': gate['next_required_round'],
        'new_external_case_admission': 'BLOCKED',
        'dev_example_004_shadow_rebuild_permission': 'YES',
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
    manifest = objects['manifest.json']
    summary = f'''# DEV-GROUP-002 R15：R14接口冻结与跨案例准入\n\nR15不改变任何选择。当前同题训练回归维持TOP1 {manifest['statistics']['top1_hits']}/25、TOP2 {manifest['statistics']['top2_coverage']}/25。\n\nR14接口在技术上通过：轨道感知原子键、能力上限传播、场景零正贡献、归一化复合负担、30组成对重放、无循环。分数下降不能作为回滚合法性规则的依据。\n\n下一步只允许在固定组内对DEV-EXAMPLE-004执行规范无答案影子重建，用跨案例结果检验接口稳定性；禁止新增规则、答案调参、正式释放或组外案例准入。\n'''
    (out / 'summary.md').write_text(summary, encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    out = repo_root / ROUND_DIR
    names = ['score-trend.json', 'interface-freeze.json', 'cross-case-gate.json', 'prediction-preservation.json', 'manifest.json']
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
    score = objects['score-trend.json']
    interface = objects['interface-freeze.json']
    gate = objects['cross-case-gate.json']
    preservation = objects['prediction-preservation.json']
    manifest = objects['manifest.json']
    if score['original_blind_baseline'] != {'top1_hits': 11, 'top2_coverage': 16, 'question_count': 25, 'immutable': True}:
        errors.append('blind baseline mutation')
    if score['training_score_delta_r11_to_r14'] != {'top1': -3, 'top2': -3}:
        errors.append('score trend replay')
    if interface['status'] != 'PASS_TECHNICALLY_FROZEN_FOR_CROSS_CASE_REPLAY':
        errors.append('interface status')
    if interface['invalid_changed_atom_ids'] or interface['bazi_changed_atom_count'] != 0:
        errors.append('invalid interface change scope')
    if interface['answer_access_during_adjustment'] or interface['answer_access_during_decision']:
        errors.append('answer access')
    if interface['scene_only_positive_decision_rows'] != 0 or interface['raw_endpoint_count_decision_rows'] != 0:
        errors.append('obsolete pairwise basis')
    if gate['dev_example_004_shadow_rebuild_permission'] != 'YES' or gate['formal_release_permission'] != 'NO':
        errors.append('gate permission')
    if gate['new_external_case_admission'] != 'BLOCKED' or gate['answer_visible_score_tuning_permission'] != 'NO':
        errors.append('gate boundary')
    if preservation['selection_changed'] is not False or (preservation['top1_hits'], preservation['top2_coverage']) != (10, 13):
        errors.append('prediction preservation')
    if manifest['status'] != 'FROZEN_R14_INTERFACE_AND_DEV004_CROSS_CASE_GATE':
        errors.append('manifest status')
    if manifest['dev_example_004_shadow_rebuild_permission'] != 'YES':
        errors.append('manifest gate')
    if (manifest['statistics']['formal_valid_questions'], manifest['statistics']['machine_valid_local_seals'], manifest['statistics']['s03_fusions']) != (0, 0, 0):
        errors.append('formal state')
    for rid, row in manifest['historical_rounds'].items():
        if row['path'] != HISTORY[rid] or git_blob_sha(repo_root / HISTORY[rid]) != row['git_blob_sha'] or row['preserved'] is not True:
            errors.append(f'history {rid}')
    return {
        'schema': 'DEV-GROUP-002-R15-VALIDATION-V1',
        'status': 'PASS' if not errors else 'FAIL',
        'error_count': len(errors),
        'errors': errors,
        'historical_rounds_preserved': list(HISTORY),
        'interface_id': interface['interface_id'],
        'r14_changed_atom_count': interface['changed_atom_count'],
        'r14_pairwise_rows': interface['pairwise_rows'],
        'r14_cycle_question_ids': interface['cycle_question_ids'],
        'r14_low_information_tiebreak_rows': interface['low_information_tiebreak_rows'],
        'selection_changed': False,
        'top1_hits': 10,
        'top2_coverage': 13,
        'dev_example_004_shadow_rebuild_permission': gate['dev_example_004_shadow_rebuild_permission'],
        'formal_release_permission': gate['formal_release_permission'],
        'answer_visible_score_tuning_permission': gate['answer_visible_score_tuning_permission'],
        'new_external_case_admission': gate['new_external_case_admission'],
        'formal_valid_questions': 0,
        'machine_valid_local_seals': 0,
        's03_fusions': 0,
        'base_astrological_knowledge_changed': False,
        's00_s19_modified': False,
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
