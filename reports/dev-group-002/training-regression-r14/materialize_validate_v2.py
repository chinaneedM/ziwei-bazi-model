#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import materialize_validate as r14


def fixed_build_adjusted_matrix(matrix: dict[str, Any], audit: dict[str, Any], generic_fix: dict[str, Any]) -> dict[str, Any]:
    audit_index = {(row['track_id'], row['atom_id']): row for row in audit['rows']}
    if len(audit_index) != len(audit['rows']):
        raise ValueError('track-aware atom audit key is not unique')
    rows = []
    changed = []
    for atom in matrix['rows']:
        audited = audit_index[(atom['track_id'], atom['atom_id'])]
        clone = dict(atom)
        if atom['track_id'] == 'ZIWEI':
            new_direction, reasons = r14.adjusted_direction(atom['direction_status'], audited['defect_ids'])
        else:
            new_direction, reasons = atom['direction_status'], []
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
        clone['audit_binding_key'] = [atom['track_id'], atom['atom_id']]
        if new_direction != atom['direction_status']:
            changed.append(atom['atom_id'])
        rows.append(clone)
    return r14.with_hash({
        'schema': 'DEV-GROUP-002-R14-ADJUSTED-ATOM-DIRECTION-MATRIX-V2',
        'group_id': 'DEV-GROUP-002',
        'case_id': r14.CASE_ID,
        'round_id': 'R14',
        'parent_r12_matrix_sha256': matrix['canonical_sha256'],
        'parent_r13_atom_audit_sha256': audit['canonical_sha256'],
        'parent_r13_generic_fix_sha256': generic_fix['canonical_sha256'],
        'audit_binding_key_mode': 'TRACK_ID_PLUS_ATOM_ID',
        'r14_v1_atom_id_only_collision_corrected': True,
        'rows': rows,
        'row_count': len(rows),
        'changed_atom_ids': changed,
        'changed_atom_count': len(changed),
        'ziwei_changed_atom_count': sum(row['track_id'] == 'ZIWEI' and row['atom_id'] in set(changed) for row in rows),
        'bazi_changed_atom_count': sum(row['track_id'] == 'BAZI' and row['atom_id'] in set(changed) for row in rows),
        'status': 'PASS_GENERIC_CAPABILITY_RULES_APPLIED_BEFORE_ANSWER_ACCESS',
    })


r14.build_adjusted_matrix = fixed_build_adjusted_matrix


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
        r14.materialize(root)
    if args.validate:
        result = r14.validate(root)
        result['schema'] = 'DEV-GROUP-002-R14-VALIDATION-V2'
        result['track_aware_audit_binding_fix'] = {
            'status': 'PASS' if result['status'] == 'PASS' else 'FAIL',
            'key_mode': 'TRACK_ID_PLUS_ATOM_ID',
            'selection_or_direction_rule_changed': False,
        }
        out = root / r14.ROUND_DIR
        out.mkdir(parents=True, exist_ok=True)
        r14.write_json(out / 'validation.json', result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result['status'] == 'PASS' else 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
