#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r10')
CASE_ID = 'DEV-EXAMPLE-002'
HISTORY = {
    f'R{i}': f'reports/dev-group-002/training-regression-r{i}/manifest.json'
    for i in range(1, 10)
}
INPUTS = {
    'r9_prediction': 'reports/dev-group-002/training-regression-r9/prediction-freeze.json',
    'r9_pairwise': 'reports/dev-group-002/training-regression-r9/pairwise-adjudication.json',
    'r9_bindings': 'reports/dev-group-002/training-regression-r9/track-option-parent-bindings.json',
    'r9_atoms': 'reports/dev-group-002/training-regression-r9/option-atom-freeze.json',
    'r9_review': 'reports/dev-group-002/training-regression-r9/postreveal-review.json',
    'questions': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-002/questions-parsed.json',
}

COMMON_ATOMS = {
    ('Q2', 'A', 'C'): ['UNIVERSITY_COMPLETION'],
    ('Q2', 'B', 'D'): ['INTELLIGENCE_POSITIVE'],
    ('Q4', 'A', 'B'): ['MARRIED_STATE'],
    ('Q4', 'A', 'C'): ['MARRIED_STATE'],
    ('Q4', 'B', 'C'): ['MARRIED_STATE'],
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


def pair_key(qid: str, left: str, right: str) -> tuple[str, str, str]:
    a, b = sorted((left, right))
    return qid, a, b


def build_common_atom_subtraction(questions: list[dict[str, Any]], r9_pairwise: dict[str, Any]) -> dict[str, Any]:
    literals = {
        (q['question_id'], option['option_id']): option['text']
        for q in questions
        for option in q['options']
    }
    rows = []
    for row in r9_pairwise['rows']:
        qid, left, right = row['question_id'], row['left'], row['right']
        common = COMMON_ATOMS.get(pair_key(qid, left, right), [])
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'left': left,
            'right': right,
            'left_literal': literals[(qid, left)],
            'right_literal': literals[(qid, right)],
            'shared_domain_atoms_zeroed': [f'{qid}_COMMON_DOMAIN_CONTEXT'],
            'shared_material_atom_ids_zeroed': common,
            'remaining_left_distinctive_atoms_status': 'REQUIRES_ATOM_LEVEL_DIRECTION_REPLAY',
            'remaining_right_distinctive_atoms_status': 'REQUIRES_ATOM_LEVEL_DIRECTION_REPLAY',
            'subtraction_status': 'EXECUTED_LITERAL_COMMON_ATOMS_ONLY',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R10-COMMON-ATOM-SUBTRACTION-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R10',
        'parent_pairwise_sha256': r9_pairwise['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'rows_with_material_common_atoms': sum(bool(row['shared_material_atom_ids_zeroed']) for row in rows),
        'interpretation': 'Only literal common atoms are zeroed. This object does not change the frozen R9 winner.',
    })


def build_pairwise_audit(r9_pairwise: dict[str, Any], r9_bindings: dict[str, Any], subtraction: dict[str, Any]) -> dict[str, Any]:
    binding_index = {
        (row['question_id'], row['track_id'], row['option_id']): row
        for row in r9_bindings['track_rows']
    }
    subtraction_index = {
        (row['question_id'], row['left'], row['right']): row
        for row in subtraction['rows']
    }
    rows = []
    for pair in r9_pairwise['rows']:
        qid, left, right = pair['question_id'], pair['left'], pair['right']
        left_binding = binding_index[(qid, 'ZIWEI', left)]
        right_binding = binding_index[(qid, 'ZIWEI', right)]
        common = subtraction_index[(qid, left, right)]['shared_material_atom_ids_zeroed']
        defects = []
        if 'left_atom_direction_parent_ids' not in pair or 'right_atom_direction_parent_ids' not in pair:
            defects.append('PAIRWISE_ROW_LACKS_ATOM_DIRECTION_PARENT_IDS')
        if pair.get('left_key') is not None or pair.get('right_key') is not None:
            defects.append('HAND_AUTHORED_AGGREGATE_KEY_USED_AS_DECISION_PROXY')
        if common:
            defects.append('COMMON_MATERIAL_ATOM_NOT_SUBTRACTED_BEFORE_R9_DECISION')
        if not left_binding['partial_atom_ids'] and not right_binding['partial_atom_ids']:
            defects.append('NO_DIRECT_PARTIAL_ATOM_DIFFERENCE')
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'left': left,
            'right': right,
            'r9_winner': pair['winner'],
            'r9_decision_basis': pair['decision_basis'],
            'r9_left_key': pair.get('left_key'),
            'r9_right_key': pair.get('right_key'),
            'common_material_atoms': common,
            'left_binding_parent_ids': left_binding['parent_excerpt_ids'],
            'right_binding_parent_ids': right_binding['parent_excerpt_ids'],
            'left_partial_atoms': left_binding['partial_atom_ids'],
            'right_partial_atoms': right_binding['partial_atom_ids'],
            'left_missing_endpoints': left_binding['missing_exact_endpoint_ids'],
            'right_missing_endpoints': right_binding['missing_exact_endpoint_ids'],
            'defect_ids': defects,
            'atom_level_replay_status': 'NOT_REPLAYABLE_FROM_R9_PAIRWISE_ROW',
            'winner_change_permission': 'NO_R10_DIAGNOSTIC_ONLY',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R10-PAIRWISE-PROVENANCE-AUDIT-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R10',
        'parent_r9_pairwise_sha256': r9_pairwise['canonical_sha256'],
        'parent_r9_bindings_sha256': r9_bindings['canonical_sha256'],
        'parent_common_atom_subtraction_sha256': subtraction['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'summary': {
            'rows_missing_atom_direction_parent_ids': sum('PAIRWISE_ROW_LACKS_ATOM_DIRECTION_PARENT_IDS' in row['defect_ids'] for row in rows),
            'rows_using_aggregate_keys': sum('HAND_AUTHORED_AGGREGATE_KEY_USED_AS_DECISION_PROXY' in row['defect_ids'] for row in rows),
            'rows_with_unsubtracted_common_material_atoms': sum('COMMON_MATERIAL_ATOM_NOT_SUBTRACTED_BEFORE_R9_DECISION' in row['defect_ids'] for row in rows),
            'atom_level_replayable_rows': 0,
        },
        'status': 'FAIL_CLOSED_FOR_SELECTION_CHANGE',
    })


def build_regression_diagnosis(r9_prediction: dict[str, Any], r9_review: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    case = next(row for row in r9_prediction['cases'] if row['case_id'] == CASE_ID)
    answer = r9_review['answer_vectors'][CASE_ID]
    rows = []
    r8_ranks = ['DCBA', 'BADC', 'DCBA', 'BCAD', 'BADC']
    for index, (r8_rank, r9_rank, correct) in enumerate(zip(r8_ranks, case['ranks'], answer), 1):
        qid = f'Q{index}'
        top1_changed = r8_rank[0] != r9_rank[0]
        outcome_change = (r8_rank[0] == correct, r9_rank[0] == correct)
        diagnosis = 'NO_TOP1_CHANGE'
        classification = 'SOURCE_CONFIRMED'
        if qid == 'Q2':
            diagnosis = 'R9_PREFERRED_ADVANCED_DEGREE_MANAGEMENT_COMPOUND_AFTER_COUNTING_SHARED_INTELLIGENCE_AND_AGGREGATE_KEY; POSTREVEAL_OUTCOME_REGRESSED'
            classification = 'REASONED_HYPOTHESIS'
        elif qid == 'Q4':
            diagnosis = 'TOP1_CHURN_BETWEEN_TWO_UNCLOSED_RELATIONSHIP_COMPOUNDS; CORRECT_OPTION_REMAINS OUTSIDE_TOP2_AND CANNOT_BE_PROMOTED_FROM_OUTCOME'
            classification = 'OPEN_RESEARCH_QUESTION'
        elif r8_rank != r9_rank:
            diagnosis = 'LOWER_ORDER_CHANGE_ONLY_NO_SCORE_EFFECT'
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'r8_rank': r8_rank,
            'r9_rank': r9_rank,
            'literal_answer': correct,
            'r8_top1_correct': outcome_change[0],
            'r9_top1_correct': outcome_change[1],
            'top1_changed': top1_changed,
            'diagnosis': diagnosis,
            'learning_classification': classification,
            'direction_change_authorized': False,
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R10-REGRESSION-DIAGNOSIS-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R10',
        'parent_r9_prediction_sha256': r9_prediction['canonical_sha256'],
        'parent_r9_review_sha256': r9_review['canonical_sha256'],
        'parent_pairwise_audit_sha256': audit['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'score_change': {'top1': -1, 'top2': 0},
        'knowledge_defect_proven': False,
        'reproducible_interface_defects': [
            'COMMON_ATOM_SUBTRACTION_NOT_MATERIALIZED_BEFORE_R9_PAIRWISE',
            'PAIRWISE_ROWS_LACK_ATOM_LEVEL_DIRECTION_PARENT_IDS',
            'HAND_AUTHORED_AGGREGATE_KEYS_SUBSTITUTE_FOR_MECHANICAL_ATOM_REPLAY',
        ],
        'conclusion': 'The score regression is real, but the answer outcome does not identify a valid astrological direction patch. R9 selection must remain frozen until the generic atom-level adjudication interface is rebuilt.',
    })


def build_generic_fix() -> dict[str, Any]:
    return with_hash({
        'schema': 'DEV-GROUP-002-R10-GENERIC-FIX-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R10',
        'fix_id': 'TR-R10-COMMON-ATOM-AND-PAIRWISE-PARENT-REPLAY-GATE',
        'defect_class': 'AGGREGATE_OPTION_KEY_WITHOUT_COMMON_ATOM_SUBTRACTION_OR_ATOM_PARENT_REPLAY',
        'general_rules': [
            'Before pairwise comparison, material atoms shared by the two options must be explicitly identified and assigned zero distinguishing contribution.',
            'A pairwise row must reference the exact option-atom direction rows and their source-parent identifiers; an aggregate numeric or ordinal key is not a substitute.',
            'Stable personality or capability support cannot be counted again as support for an exact degree, title, registration, diagnosis, marriage status, caregiver identity, or amount endpoint.',
            'A compound option must preserve the status of every material atom. One supported tendency cannot silently complete several missing exact endpoints.',
            'Postreveal correctness or rank position may classify an execution defect, but cannot authorize an astrological direction change or a case-specific rule.',
        ],
        'base_astrological_knowledge_changed': False,
        'case_specific_direction_rule_added': False,
        's00_s19_modified': False,
        'impact_scope': 'GENERIC_PAIRWISE_RUNTIME_AND_AUDIT_INTERFACE_ONLY',
    })


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    r9_prediction = read_json(repo_root / INPUTS['r9_prediction'])
    r9_pairwise = read_json(repo_root / INPUTS['r9_pairwise'])
    r9_bindings = read_json(repo_root / INPUTS['r9_bindings'])
    r9_review = read_json(repo_root / INPUTS['r9_review'])
    questions = read_json(repo_root / INPUTS['questions'])
    subtraction = build_common_atom_subtraction(questions, r9_pairwise)
    audit = build_pairwise_audit(r9_pairwise, r9_bindings, subtraction)
    diagnosis = build_regression_diagnosis(r9_prediction, r9_review, audit)
    generic_fix = build_generic_fix()
    preservation = with_hash({
        'schema': 'DEV-GROUP-002-R10-PREDICTION-PRESERVATION-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R10',
        'parent_r9_prediction_sha256': r9_prediction['canonical_sha256'],
        'cases': r9_prediction['cases'],
        'question_count': 25,
        'selection_changed': False,
        'top1_hits': 13,
        'top2_coverage': 16,
        'formal_exact_assertion_permission': 'NULL_ONLY',
        'new_case_admission': 'BLOCKED',
    })
    base = {
        'common-atom-subtraction.json': subtraction,
        'pairwise-provenance-audit.json': audit,
        'regression-diagnosis.json': diagnosis,
        'generic-fix.json': generic_fix,
        'prediction-preservation.json': preservation,
    }
    history = {
        rid: {'path': path, 'git_blob_sha': git_blob_sha(repo_root / path), 'preserved': True}
        for rid, path in HISTORY.items()
    }
    artifacts = {
        name.removesuffix('.json').replace('-', '_'): {
            'path': str(ROUND_DIR / name),
            'canonical_sha256': obj['canonical_sha256'],
        }
        for name, obj in base.items()
    }
    manifest = with_hash({
        'schema': 'DEV-GROUP-002-R10-FROZEN-MANIFEST-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R10',
        'status': 'FROZEN_REGRESSION_DIAGNOSIS_NO_SELECTION_CHANGE',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD_DIAGNOSIS',
        'historical_rounds': history,
        'artifacts': artifacts,
        'statistics': {
            'question_count': 25,
            'diagnosed_case_count': 1,
            'diagnosed_question_count': 5,
            'common_atom_pair_rows': subtraction['row_count'],
            'rows_with_material_common_atoms': subtraction['rows_with_material_common_atoms'],
            'pairwise_audit_rows': audit['row_count'],
            'atom_level_replayable_pairwise_rows': 0,
            'top1_hits': 13,
            'top2_coverage': 16,
            'formal_valid_questions': 0,
            'machine_valid_local_seals': 0,
            's03_fusions': 0,
        },
        'training_conclusion': 'R10 preserves the R9 regression and identifies generic atom-subtraction and pairwise-parent replay defects. It does not infer an astrological knowledge correction from the answer.',
        'next_required_round': 'R11_REBUILD_PAIRWISE_FROM_LITERAL_ATOM_DIRECTION_PARENTS_WITHOUT_ANSWER_GUIDANCE',
        'new_case_admission': 'BLOCKED',
        'selection_change_permission': 'NO_UNTIL_R11_ATOM_LEVEL_REPLAY',
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
    summary = f'''# DEV-GROUP-002 R10：R9退化与成对裁决接口诊断\n\nR10完整保留R1—R9和R9全部排序，不根据正确答案修复Q2或Q4。组级同题训练回归继续为TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。\n\n本轮物化30条共同原子扣除行，并审计R9的30组成对裁决。审计发现：R9没有在成对比较前物化共同原子扣除；成对行没有引用逐原子方向父对象；手工聚合key替代了机械原子重放。Q2的B与D共享“聪明”原子，该共同原子不应构成区别贡献。\n\n揭盲结果只能证明R9的TOP1退化真实存在，不能证明应把B改为首选。Q4同样只显示两个未闭合关系复合项之间发生首选漂移，不能由正确答案倒推性取向或婚姻手续。\n\nR10修复候选仅涉及通用执行接口：共同原子归零、逐原子父链和成对理由重放。S00—S19、基础命理知识、案例方向规则和R9选择均未修改。\n'''
    (out / 'summary.md').write_text(summary, encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    out = repo_root / ROUND_DIR
    names = ['common-atom-subtraction.json','pairwise-provenance-audit.json','regression-diagnosis.json','generic-fix.json','prediction-preservation.json','manifest.json']
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
    subtraction = objects['common-atom-subtraction.json']
    if subtraction['row_count'] != 30 or len(subtraction['rows']) != 30:
        errors.append('common atom row count')
    if subtraction['rows_with_material_common_atoms'] != 5:
        errors.append('material common atom row count')
    audit = objects['pairwise-provenance-audit.json']
    if audit['row_count'] != 30 or audit['summary']['atom_level_replayable_rows'] != 0:
        errors.append('pairwise audit count or replay status')
    if audit['summary']['rows_missing_atom_direction_parent_ids'] != 30:
        errors.append('missing atom parent detection')
    diagnosis = objects['regression-diagnosis.json']
    if diagnosis['score_change'] != {'top1': -1, 'top2': 0}:
        errors.append('score change diagnosis')
    if diagnosis['knowledge_defect_proven'] is not False:
        errors.append('knowledge defect falsely proven')
    if any(row['direction_change_authorized'] for row in diagnosis['rows']):
        errors.append('answer-derived direction change')
    preservation = objects['prediction-preservation.json']
    if preservation['selection_changed'] is not False or (preservation['top1_hits'], preservation['top2_coverage']) != (13, 16):
        errors.append('prediction preservation')
    generic_fix = objects['generic-fix.json']
    if generic_fix['base_astrological_knowledge_changed'] is not False or generic_fix['case_specific_direction_rule_added'] is not False:
        errors.append('unauthorized generic fix')
    rule_text = '\n'.join(generic_fix['general_rules'])
    if any(token in rule_text for token in ['DEV-EXAMPLE-002','DBDDB','Q2','Q4']):
        errors.append('case token leaked into generic rules')
    manifest = objects['manifest.json']
    if manifest['status'] != 'FROZEN_REGRESSION_DIAGNOSIS_NO_SELECTION_CHANGE':
        errors.append('manifest status')
    if manifest['selection_change_permission'] != 'NO_UNTIL_R11_ATOM_LEVEL_REPLAY':
        errors.append('selection gate')
    stats = manifest['statistics']
    if (stats['top1_hits'], stats['top2_coverage'], stats['formal_valid_questions'], stats['machine_valid_local_seals'], stats['s03_fusions']) != (13,16,0,0,0):
        errors.append('manifest statistics')
    for rid, row in manifest['historical_rounds'].items():
        if row['path'] != HISTORY[rid] or git_blob_sha(repo_root / HISTORY[rid]) != row['git_blob_sha'] or row['preserved'] is not True:
            errors.append(f'history {rid}')
    return {
        'schema': 'DEV-GROUP-002-R10-VALIDATION-V1',
        'status': 'PASS' if not errors else 'FAIL',
        'error_count': len(errors),
        'errors': errors,
        'historical_rounds_preserved': list(HISTORY),
        'diagnosed_case_id': CASE_ID,
        'common_atom_pair_rows': subtraction['row_count'],
        'rows_with_material_common_atoms': subtraction['rows_with_material_common_atoms'],
        'pairwise_audit_rows': audit['row_count'],
        'atom_level_replayable_pairwise_rows': 0,
        'selection_changed': False,
        'top1_hits': 13,
        'top2_coverage': 16,
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
