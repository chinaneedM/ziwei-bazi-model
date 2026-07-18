#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = Path(__file__).resolve().parent / 'materialize_validate.py'
OUTPUT = Path(__file__).resolve().parent / 'preflight.json'


def main() -> int:
    spec = importlib.util.spec_from_file_location('r9_materializer', MODULE_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit('cannot load R9 materializer')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result: dict[str, object] = {'schema': 'DEV-GROUP-002-R9-PREFLIGHT-DIAGNOSTIC-V1'}
    try:
        whitelist = module.build_whitelist(ROOT)
        result['whitelist_status'] = whitelist.get('status')
        result['whitelist_failures'] = [row for row in whitelist.get('rows', []) if row.get('status') != 'PASS']
    except Exception as exc:
        result['whitelist_exception'] = repr(exc)
    try:
        input_freeze, _, _, _ = module.build_input_freeze(ROOT)
        result['input_freeze_status'] = input_freeze.get('status')
        result['input_file_failures'] = [row for row in input_freeze.get('files', []) if row.get('status') != 'PASS']
        result['ziwei_missing_tokens'] = input_freeze.get('ziwei_missing_tokens')
        result['answer_isolation'] = input_freeze.get('answer_isolation')
    except Exception as exc:
        result['input_freeze_exception'] = repr(exc)
    try:
        excerpts = module.build_source_excerpts(ROOT)
        result['source_excerpt_status'] = excerpts.get('status')
        result['source_excerpt_failures'] = [
            {
                'excerpt_id': row.get('excerpt_id'),
                'path': row.get('path'),
                'line_start': row.get('line_start'),
                'line_end': row.get('line_end'),
                'missing_required_phrases': row.get('missing_required_phrases'),
                'status': row.get('status'),
            }
            for row in excerpts.get('rows', [])
            if row.get('status') != 'PASS_FULL_PARENT_SEGMENT'
        ]
    except Exception as exc:
        result['source_excerpt_exception'] = repr(exc)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(OUTPUT.read_text(encoding='utf-8'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
