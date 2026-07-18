#!/usr/bin/env python3
"""Materialize and validate DEV-GROUP-002 R2 source excerpts.

This validates active S00-S19 source bytes, materializes exact parent segments
from line ranges, checks the DEV-EXAMPLE-004 Zi-hour parallel-variant receipt,
and verifies the 25-row formal-readiness matrix. It does not create local seals,
perform S03 fusion, or claim new blind accuracy.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root', type=Path, default=Path('.'))
    ap.add_argument('--artifact-dir', type=Path, default=Path('reports/dev-group-002/training-regression-r2'))
    ap.add_argument('--output', type=Path)
    args=ap.parse_args()
    root=args.repo_root.resolve(); art=(root/args.artifact_dir).resolve()
    wl=load(art/'active-whitelist-receipt.json')
    spec=load(art/'source-excerpt-spec.json')
    variant=load(art/'dev-example-004-zi-hour-variant-resolution.json')
    readiness=load(art/'formal-readiness-matrix.json')
    errors=[]; path_by_sid={}
    for row in wl['rows']:
        sid=row['library_id']
        p=root/'knowledge'/'base'/row['canonical_filename']
        if not p.exists():
            errors.append(f'{sid}: missing {p}'); continue
        b=p.read_bytes(); path_by_sid[sid]=p
        if sha(b)!=row['sha256']: errors.append(f'{sid}: sha256 mismatch')
        if len(b)!=row['bytes']: errors.append(f'{sid}: byte-size mismatch')
    materialized=[]
    for e in spec['entries']:
        p=path_by_sid.get(e['library_id'])
        if p is None: continue
        lines=p.read_text(encoding='utf-8').splitlines()
        text='\n'.join(lines[e['line_start']-1:e['line_end']])
        if sha(text.encode())!=e['excerpt_sha256']:
            errors.append(f"{e['excerpt_id']}: excerpt hash mismatch")
        materialized.append({**e,'text':text,'status':'FULL_PARENT_SEGMENT_MATERIALIZED'})
    if len(materialized)!=spec['excerpt_count']:
        errors.append('source excerpt count mismatch')
    if variant['answer_used_to_derive_variants'] is not False:
        errors.append('DEV004 variant derivation used answer')
    rules={v['day_boundary_rule'] for v in variant['variants']}
    if rules!={'ZI_CHU_DAY_CHANGE_AT_23','MIDNIGHT_DAY_CHANGE_AT_00'}:
        errors.append('DEV004 legal variant set incomplete')
    if variant['r2_classification']!='CROSS_SYSTEM_CALENDAR_CONVENTION_DIVERGENCE_VALID':
        errors.append('DEV004 classification not corrected')
    if readiness['question_count']!=25 or len(readiness['rows'])!=25:
        errors.append('formal readiness matrix must contain 25 rows')
    if readiness['summary']['s03_fused_questions']!=0:
        errors.append('S03 fusion count must remain zero')
    out={
      'schema':'DEV-GROUP-002-R2-MATERIALIZATION-VALIDATION-V1',
      'status':'PASS' if not errors else 'FAIL','error_count':len(errors),'errors':errors,
      'active_library_rows':len(path_by_sid),'source_excerpt_count':len(materialized),
      'readiness_rows':len(readiness['rows']),'dev004_variant_count':len(variant['variants']),
      'formal_local_seal_count':0,'s03_fusion_count':0,
      'score_label':'TRAINING_REGRESSION_SCORE_ONLY',
      'materialized_source_excerpts':materialized,
    }
    dest=args.output or art/'materialization-validation.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='materialized_source_excerpts'},ensure_ascii=False,sort_keys=True,indent=2))
    return 0 if not errors else 1

if __name__=='__main__': raise SystemExit(main())
