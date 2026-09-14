#!/usr/bin/env python3
from pathlib import Path
import json

BATCH_ID = 'BATCH-12-ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-BN'
BATCH_DOC = 'docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-BN.md'
EVIDENCE_PATH = 'docs/research/ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-R1.json'
SOURCE_ID = 'EXT-ZIWEI-TONGSHU-ZHENGZONG-CADAL02094425'
PREV = 'BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM'
COMMONS_URL = 'https://commons.wikimedia.org/wiki/Special:Redirect/file/CADAL02094425%20%E6%96%B0%E5%88%8A%E7%90%86%E6%B0%A3%E8%A9%B3%E8%BE%AF%E7%BA%82%E8%A6%81%E4%B8%89%E5%8F%B0%E4%BE%BF%E8%A6%BD%E9%80%9A%E6%9B%B8%E6%AD%A3%E5%AE%97%EF%BC%88%E5%85%AB%EF%BC%89.djvu'

EVIDENCE = {
    'schema': 'ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-R1',
    'batch_id': BATCH_ID,
    'question': 'Does a directly readable homolog under the same 選時寶鏡局 heading read 上四亥 or 上四刻 in the paired upper/lower four-ke clauses?',
    'source': {
        'source_id': SOURCE_ID,
        'title': '《新刊理氣詳辯纂要三臺便覽通書正宗》卷八',
        'author_control': '[明] 林紹周輯；Shidian additionally gives [明] 林維松重編',
        'physical_scan_identifier': 'CADAL02094425',
        'provider_route': 'Wikimedia Commons public CADAL mirror',
        'commons_url': COMMONS_URL,
        'ctext_library_control': 'https://ctext.org/library.pl?if=gb&res=3478',
        'ctext_wiki_control': 'https://ctext.org/wiki.pl?if=gb&res=193730',
        'shidian_textual_control': 'https://www.shidianguji.com/zh/book/CADAL02094418/chapter/1lb22krlkx1ys',
        'physical_page_count': 116,
        'file_size_bytes': 3764355,
        'djvu_sha256': 'bd34f6347c9fc14910ba38f03e06d8185718f8d16df65bea9c702255fca74e85',
        'edition_date_claim': 'MING_WORK; EXACT_PRINT_DATE_OF_REVIEWED_COPY_NOT_ADJUDICATED',
    },
    'hosted_evidence': {
        'exact_fascicle_run_id': 34767661747,
        'exact_fascicle_artifact_id': 10320784070,
        'exact_fascicle_artifact_digest': 'sha256:868476d212dd42103295cc00e4df8d51bd7b0fa3470244faccd000c21350af16',
        'decisive_opening_page_run_id': 34806327958,
        'decisive_opening_page_artifact_id': 10333191738,
        'decisive_opening_page_artifact_digest': 'sha256:2e2a09314c815eef19180119a6e480deea09a2413e1a16e56573c0cbebdea5fd',
        'physical_target_page_1_based': 3,
        'ocr_used_for_final_glyph_reading': False,
    },
    'physical_collation': {
        'heading_secure_reading': '選時寶鏡局',
        'context_secure_reading': '日百刻配十二時之數',
        'upper_clause_secure_reading': '巳上是上四刻',
        'lower_clause_secure_reading': '巳上是下四刻',
        'upper_clause_final_glyph': '刻',
        'lower_clause_final_glyph': '刻',
        'visual_confidence': 'HIGH',
        'reading_method': 'DIRECT_VISUAL_COLLATION_OF_NATIVE_SCAN_PAGE; OCR_NOT_USED_AS_GLYPH_AUTHORITY',
    },
    'shiqie_comparison': {
        'shidian_shiqie_heading': '選時寶鏡局',
        'shidian_shiqie_upper_transcription': '巳上是上四亥。',
        'shidian_shiqie_lower_transcription': '巳上是下四刻。',
        'homolog_upper_physical': '巳上是上四刻',
        'homolog_lower_physical': '巳上是下四刻',
        'difference_isolated_to_upper_final_token': True,
        'homology_assessment': 'VERY_HIGH_TEXTUAL_AND_STRUCTURAL_HOMOLOGY',
        'anomaly_assessment': 'STRONGLY_SUPPORTS_SHIDIAN_SHIQIE 刻→亥 TRANSCRIPTION-ANOMALY DIAGNOSIS',
        'exact_shiqie_physical_target_glyph_observed': False,
    },
    'adjudication': {
        'new_hai_glyph_witness_increment': 0,
        'new_ke_homologous_physical_witness_increment': 1,
        'may_count_shiqie_upper_hai_token_as_physical_hai_witness': False,
        'hpa_zdate_006_status': 'MISSING_FROM_PRODUCT',
        'runtime_winner_selected': False,
        'candidate_collapsed': False,
        'algorithm_reopen': False,
        'scope_boundary': 'The homolog physically reads 刻 in both paired clauses; the exact 1565 Shiqie target leaf remains unobserved.',
        'next_gate': 'Acquire the exact Shiqie fascicle-three target leaf or another independently bound Shiqie facsimile; keep the Shidian 上四亥 token quarantined from Hai witness count.',
    },
}
Path(EVIDENCE_PATH).write_text(json.dumps(EVIDENCE, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

DOC = '''# Fusion Chart Historical Provenance Audit R1 — Batch 12BN

## 《筮篋理數日抄》「上四亥」異文：同題《三臺便覽通書正宗》卷八實體同源段落校勘

Status: **DIRECT PHYSICAL HOMOLOG / SAME 選時寶鏡局 HEADING / PHYSICAL P3 READS 「巳上是上四刻」 + 「巳上是下四刻」 / SHIDIAN SHIQIE HAS 「上四亥」 + 「下四刻」 / 刻→亥 TRANSCRIPTION-ANOMALY DIAGNOSIS STRONGLY STRENGTHENED / EXACT SHIQIE TARGET LEAF STILL UNOBSERVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI PHYSICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BH quarantined the Shidian transcription `巳上是上四亥。` because its paired clause reads `巳上是下四刻。`. Batch 12BI obtained a physical parallel `係上四刻，屬本日管；係下四刻，屬第二日管`.

Batch 12BN directly collates a substantially closer physical homolog under the same `選時寶鏡局` heading and the same hundred-ke/twelve-hour framework.

## 2. Physical witness

Reviewed source: 《新刊理氣詳辯纂要三臺便覽通書正宗》卷八, public scan `CADAL02094425`, 116 pages, 3,764,355 bytes, DJVU SHA-256 `bd34f6347c9fc14910ba38f03e06d8185718f8d16df65bea9c702255fca74e85`.

Public bibliographic controls identify the work as Ming and attribute compilation to 林紹周; CText reports the original source as Peking University Library and scanner as CADAL. Shidian additionally labels 林維松 as recompiler. The exact print date of this scanned copy is not asserted here.

## 3. Direct physical reading

Native scan page 3 visibly carries `選時寶鏡局`. Direct visual collation, without OCR as glyph authority, reads:

`巳上是上四刻`

`巳上是下四刻`

Both final glyphs are visibly `刻`. The printed/transcribed `巳上` is preserved rather than silently normalised.

## 4. Comparison with 《筮篋理數日抄》 transcription

Shidian Shiqie transcription:

```text
巳上是上四亥。
巳上是下四刻。
```

Direct physical homolog:

```text
巳上是上四刻
巳上是下四刻
```

The match is not merely thematic: same heading, same timekeeping frame, and the same paired clause architecture. The discrepancy is isolated to the final token of the upper clause. Combined with Batch 12BI and other observed digital `刻→亥` confusion, this strongly strengthens a transcription-layer anomaly diagnosis.

## 5. Evidentiary boundary

The exact 1565 《筮篋理數日抄》 target physical leaf remains unread. Therefore this batch does not claim that its exact physical glyph has been observed, that all Shiqie recensions read `刻`, or that HPA-ZDATE-006 may be selected/collapsed.

## 6. Effect on HPA-ZDATE-006

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- physical Hai-glyph witness increment: `0`
- homologous physical `刻` witness increment: `1`
- count Shidian `上四亥` as physical Hai witness: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

No deterministic runtime change is authorized.

## 7. Durable evidence

Machine record: `docs/research/ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-R1.json`.

Hosted evidence: run `34767661747`, artifact `10320784070`, digest `sha256:868476d212dd42103295cc00e4df8d51bd7b0fa3470244faccd000c21350af16`; decisive p3 render run `34806327958`, artifact `10333191738`, digest `sha256:2e2a09314c815eef19180119a6e480deea09a2413e1a16e56573c0cbebdea5fd`.

## 8. Next gate

Continue direct acquisition of the exact Shiqie卷三 target leaf or another independently bound Shiqie facsimile. Until then, keep the exact Shiqie physical-glyph question open and keep the Shidian `上四亥` token out of the HPA-ZDATE-006 Hai witness count.
'''
Path(BATCH_DOC).write_text(DOC, encoding='utf-8')

reg_path = Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg = json.loads(reg_path.read_text(encoding='utf-8'))
reg['access_date'] = '2026-09-14'
src = next((s for s in reg['sources'] if s.get('source_id') == SOURCE_ID), None)
if src is None:
    src = {
        'source_id': SOURCE_ID,
        'title': '《新刊理氣詳辯纂要三臺便覽通書正宗》卷八',
        'author_attribution': '[明] 林紹周輯；Shidian control additionally gives [明] 林維松重編',
        'historical_period': 'MING_WORK; EXACT_PRINT_DATE_OF_REVIEWED_COPY_NOT_ADJUDICATED',
        'edition': 'CADAL02094425 physical scan copy',
        'provider': 'Wikimedia Commons public CADAL mirror; CText bibliographic control',
        'url': COMMONS_URL,
        'source_role': 'DIRECT_PHYSICAL_HOMOLOG_FOR_SHIQIE_UPPER_LOWER_FOUR_KE_TEXTUAL_COLLATION',
        'quality_notes': 'Native-scan visual collation; p3 carries 選時寶鏡局 and reads 巳上是上四刻 / 巳上是下四刻. Close homolog, not exact Shiqie leaf.',
    }
    reg['sources'].append(src)
src['batch_12bn'] = {
    'physical_scan_identifier': 'CADAL02094425',
    'page_count': 116,
    'djvu_sha256': 'bd34f6347c9fc14910ba38f03e06d8185718f8d16df65bea9c702255fca74e85',
    'target_page_1_based': 3,
    'heading_secure_reading': '選時寶鏡局',
    'upper_clause_secure_reading': '巳上是上四刻',
    'lower_clause_secure_reading': '巳上是下四刻',
    'shiqie_transcription_anomaly_effect': 'STRONGLY_STRENGTHENED',
    'exact_shiqie_target_glyph_observed': False,
    'hai_glyph_witness_increment': 0,
    'research_artifact': EVIDENCE_PATH,
}
reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

matrix_path = Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix = json.loads(matrix_path.read_text(encoding='utf-8'))
row = next(r for r in matrix['rows'] if r.get('rule_id') == 'HPA-ZDATE-006')
assert row['audit_status'] == 'MISSING_FROM_PRODUCT'
row['batch_12bn_shiqie_tongshu_zhengzong_homologous_physical_collation'] = {
    'source_id': SOURCE_ID,
    'physical_witness': 'Wikimedia Commons/CADAL02094425, 《新刊理氣詳辯纂要三臺便覽通書正宗》卷八, scan p.3',
    'heading_secure_reading': '選時寶鏡局',
    'upper_clause_secure_reading': '巳上是上四刻',
    'lower_clause_secure_reading': '巳上是下四刻',
    'mechanical_scope': 'DIRECT_PHYSICAL_HIGH_HOMOLOGY_PARALLEL_FOR_PAIRED_UPPER_LOWER_FOUR_KE_CLAUSES; NOT_EXACT_SHIQIE_TARGET_LEAF; NOT_UPPER_ZI_TO_HAI_BRANCH_RULE',
    'shiqie_anomaly_effect': 'STRONGLY_STRENGTHENS 刻→亥 TRANSCRIPTION-ANOMALY DIAGNOSIS; EXACT SHIQIE PHYSICAL GLYPH REMAINS UNOBSERVED',
    'hai_glyph_witness_increment': 0,
    'ke_homologous_physical_witness_increment': 1,
    'candidate_status_effect': 'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
    'runtime_winner_selected': False,
    'algorithm_reopen_authorized': False,
    'research_artifact': EVIDENCE_PATH,
}
matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

state_path = Path('docs/PROJECT-CURRENT-STATE-R1.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
assert state['schema_version'] == '1.72.0', state['schema_version']
state['schema_version'] = '1.73.0'
audit = state['historical_audit']
assert audit['completed_batches'][-1] == PREV, audit['completed_batches'][-1]
audit['completed_batches'].append(BATCH_ID)
audit['latest_batch_doc'] = BATCH_DOC
audit.setdefault('current_focus', []).extend([
    'Batch 12BN directly collates CADAL02094425 physical p3 under 選時寶鏡局: 巳上是上四刻 / 巳上是下四刻.',
    'This strongly strengthens the 刻→亥 transcription-anomaly diagnosis for Shidian Shiqie 上四亥; exact Shiqie target leaf remains unobserved, HPA-ZDATE-006 stays MISSING_FROM_PRODUCT, Hai physical vote +0, no winner/collapse/reopen.',
])
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

verifier_path = Path('scripts/verify-project-continuity-state-r1.py')
s = verifier_path.read_text(encoding='utf-8')
old = '''    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n    "BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL",\n    "BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM.md"'''
new = '''    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n    "BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL",\n    "BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM",\n    "BATCH-12-ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-BN",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-TONGSHU-ZHENGZONG-HOMOLOGOUS-PHYSICAL-COLLATION-BN.md"'''
assert old in s
verifier_path.write_text(s.replace(old, new, 1), encoding='utf-8')

print(json.dumps({
    'batch_id': BATCH_ID,
    'state_schema_version': state['schema_version'],
    'physical_source': SOURCE_ID,
    'target_page_1_based': 3,
    'upper_clause': '巳上是上四刻',
    'lower_clause': '巳上是下四刻',
    'exact_shiqie_target_glyph_observed': False,
    'hai_glyph_witness_increment': 0,
    'hpa_zdate_006_status': row['audit_status'],
    'runtime_winner_selected': False,
    'candidate_collapsed': False,
    'algorithm_reopen': False,
}, ensure_ascii=False, indent=2))
