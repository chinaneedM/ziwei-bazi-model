#!/usr/bin/env python3
from pathlib import Path
import json

batch_id = 'BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI'
batch_doc = 'docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI.md'
evidence_path = 'docs/research/ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-R1.json'
source_id = 'EXT-ZIWEI-LEIBIAN-LIFA-TONGSHU-CADAL02094403'
prev = 'BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH'

physical_lines = [
    '論定半夜子時隔界',
    '子初初刻、初二刻、初三刻、初四刻，係上四刻，屬本日管。',
    '子正一刻、正二刻、正三刻、正四刻，係下四刻，屬第二日管。',
]

evidence = {
    'schema': 'ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-R1',
    'batch_id': batch_id,
    'question': 'Does a directly readable independent physical calendrical witness confirm the 上四刻/下四刻 terminology that makes the Shiqie public-transcription token 上四亥 unsafe to treat as Hai-branch rule evidence?',
    'source': {
        'title': '類編曆法通書大全（一）',
        'compiler_attribution': '熊宗立編纂（received bibliographic attribution; exact scan-impression date not re-adjudicated here）',
        'provider': 'Wikimedia Commons public-domain CADAL facsimile',
        'commons_file': 'CADAL02094403 類編曆法通書大全（一）.djvu',
        'commons_url': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/CADAL02094403%20%E9%A1%9E%E7%B7%A8%E6%9B%86%E6%B3%95%E9%80%9A%E6%9B%B8%E5%A4%A7%E5%85%A8%EF%BC%88%E4%B8%80%EF%BC%89.djvu',
        'scan_sha256': '50535ad31514f733a4aebaf39824b2128e4fb1ebdc6a2fc33d9e7813d912a63e',
        'scan_page_count': 89,
        'target_scan_pages_1_based': [82, 83],
        'source_role': 'DIRECT_FACSIMILE_PARALLEL_FOR_UPPER_LOWER_FOUR_KE_TERMINOLOGY_AND_DATE_ORIENTATION',
        'exact_print_date_status': 'NOT_ESTABLISHED_IN_THIS_BATCH'
    },
    'physical_collation': {
        'method': 'DIRECT_VISUAL_COLLATION_OF_RENDERED_PUBLIC_DOMAIN_DJVU; DJVU_TEXT_LAYER_EMPTY; NO_OCR_USED_FOR_FINAL_GLYPH_JUDGMENT',
        'scan_page_82_secure_lines': physical_lines,
        'scan_page_83_scope': 'Continues the calendrical examples across the date boundary and the warning to distinguish the upper/lower four-ke division when choosing action times.',
        'upper_label_physically_read': '上四刻',
        'lower_label_physically_read': '下四刻',
        'upper_date_assignment_physically_read': '本日',
        'lower_date_assignment_physically_read': '第二日',
        'hai_glyph_in_upper_label': False
    },
    'relationship_to_shiqie_bh': {
        'shiqie_target_token_on_public_transcription': '巳上是上四亥',
        'shiqie_target_physical_leaf_observed': False,
        'shiqie_exact_target_glyph_judgment_authorized': False,
        'same_shiqie_passage_repeated_labels': ['下四刻', '上四刻屬本日管', '下四刻屬第二日管', '是上四刻作二十六日管'],
        'parallel_physical_effect': 'The independent facsimile establishes 上四刻/下四刻 as an actual printed terminology pair in the same night-Zi date-boundary discourse. This strongly corroborates the anomaly diagnosis but cannot substitute for direct collation of the Shiqie target leaf.',
        'safe_classification': 'STRONGLY_CORROBORATED_TRANSCRIPTION_ANOMALY_PENDING_EXACT_SHIQIE_PHYSICAL_LEAF',
        'forbidden_inference': 'Do not convert 上四亥 into an explicit upper-Zi-to-Hai branch vote until the Shiqie physical leaf or another direct mechanical source says so.'
    },
    'workflow_evidence': [
        {
            'run_id': 34760486843,
            'job_id': 103732346260,
            'artifact_id': 10319085691,
            'artifact_zip_digest': 'sha256:09da6df549729fbd9d33cf8333926d771c8b4d037e983be6d1507ec4c4adb409',
            'scope': 'PUBLIC_DJVU_ACQUISITION_AND_SCAN_PAGES_1_TO_35_RENDER'
        },
        {
            'run_id': 34760591933,
            'job_id': 103732623688,
            'artifact_id': 10318299257,
            'artifact_zip_digest': 'sha256:5542e0cd375bf4aab3a58c21a4f3fca93e8f9e879c9c83837e482671e33f7117',
            'scope': 'SCAN_PAGES_36_TO_89_RENDER; TARGET_P82_P83_IDENTIFIED_AND_VISUALLY_COLLATED'
        }
    ],
    'rule_adjudication': {
        'parallel_physical_upper_four_ke_confirmed': True,
        'parallel_physical_lower_four_ke_confirmed': True,
        'parallel_date_orientation_confirmed': True,
        'exact_shiqie_target_glyph_confirmed': False,
        'upper_night_zi_to_hai_branch_explicitly_attested': False,
        'hai_glyph_witness_increment': 0,
        'hpa_zdate_006_status': 'MISSING_FROM_PRODUCT',
        'runtime_winner_selected': False,
        'candidate_collapsed': False,
        'algorithm_reopen': False,
        'next_gate': 'Acquire the physical target leaf of the Jiajing-44 Shiqie copy, or another independent early source explicitly mapping upper/night Zi to Hai branch.'
    },
    'access_policy': 'PUBLIC_DOMAIN_WIKIMEDIA_COMMONS_DJVU; DIRECT VISUAL COLLATION; NO LOGIN; NO PRIVATE API/OBJECT-ID GUESSING; NO ACCESS BYPASS; NO OCR AS FINAL GLYPH AUTHORITY'
}
Path(evidence_path).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

doc = '''# Fusion Chart Historical Provenance Audit R1 — Batch 12BI

## 《類編曆法通書大全》「上四刻／下四刻」原葉物理校讀

Status: **DIRECT PUBLIC-DOMAIN FACSIMILE COLLATION / CADAL02094403 SCAN P82–83 / PHYSICAL GLYPHS CONFIRM 上四刻 + 下四刻 AND 本日 + 第二日 DATE ORIENTATION / STRONGLY CORROBORATES BATCH 12BH TRANSCRIPTION-ANOMALY DIAGNOSIS / DOES NOT PHYSICALLY COLLATE THE SHIQIE TARGET LEAF / DOES NOT ATTEST UPPER-ZI -> HAI BRANCH / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BH quarantined the public-transcription token `上四亥` in the Jiajing-44 (1565) 《筮篋理數日抄》. The same passage is internally symmetric with `下四刻` and then repeatedly uses `上四刻/下四刻` for the date-boundary mechanics. Because the exact Shiqie physical leaf was unavailable, Batch 12BH deliberately refused to call the token either a confirmed `亥` glyph or a confirmed OCR/transcription error.

Batch 12BI asks a narrower question: can an independent physical calendrical witness from the same technical discourse directly establish that `上四刻/下四刻` is an actual printed terminology pair, rather than a normalization invented by modern editors?

## 2. Public-domain physical witness

The reviewed object is the Wikimedia Commons public-domain CADAL scan:

- `CADAL02094403 類編曆法通書大全（一）.djvu`
- 89 scan pages
- DJVU SHA-256: `50535ad31514f733a4aebaf39824b2128e4fb1ebdc6a2fc33d9e7813d912a63e`
- target scan pages: `82–83`

The DJVU has no usable embedded text layer for this purpose. Final glyph judgment was therefore made by direct visual inspection of rendered scan pages; OCR was not used as glyph authority.

The exact impression date of this scanned copy is **not established in this batch**. The source is used only as an independent physical witness to the technical vocabulary and date-boundary mechanics printed on the reviewed leaves.

## 3. Direct collation — scan p.82

The leaf directly reads:

> 論定半夜子時隔界
>
> 子初初刻、初二刻、初三刻、初四刻，係上四刻，屬本日管。
>
> 子正一刻、正二刻、正三刻、正四刻，係下四刻，屬第二日管。

The glyphs relevant to this audit are physically unambiguous:

```text
上四刻    physically observed
下四刻    physically observed
本日      physically observed for the upper four-ke segment
第二日    physically observed for the lower four-ke segment
上四亥    not observed in this physical parallel
```

Scan p.83 continues the calendrical examples across the boundary and the instruction to distinguish the upper/lower four-ke division when selecting times.

## 4. Effect on the Batch 12BH anomaly

This physical witness materially strengthens—but does not over-close—the Batch 12BH diagnosis.

The combined evidence is now:

1. Shiqie public transcription contains the isolated token `上四亥` in a counting-label slot.
2. Its immediately parallel lower label is `下四刻`.
3. The same Shiqie passage then repeatedly says `上四刻屬本日管`, `下四刻屬第二日管`, and `是上四刻作二十六日管`.
4. The independent physical 《類編曆法通書大全》 leaf directly prints the symmetric pair `係上四刻` / `係下四刻` in the same night-Zi date-boundary discourse.
5. Other public transcription/OCR surfaces reviewed in Batch 12BH show that `刻` can be misrecognized as `亥` in this technical environment.

Therefore `上四亥` is now best classified as a **strongly corroborated transcription anomaly pending direct Shiqie physical-leaf collation**.

The remaining caution is essential: this batch has **not** observed the exact Shiqie target leaf. It therefore does not authorize the statement “the Shiqie original definitely prints 刻.”

## 5. Effect on HPA-ZDATE-006

None of the above supplies the missing mechanical bridge:

```text
upper/night Zi -> Hai earthly branch
```

Accordingly:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- explicit new Hai-branch vote: `0`
- runtime winner selected: `false`
- candidate collapsed: `false`
- algorithm reopen: `false`

The literal public-transcription string `上四亥` remains barred from use as evidence for branch reassignment unless the exact physical Shiqie leaf or another direct mechanical historical source independently validates that reading and semantics.

## 6. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-R1.json`

Hosted physical-render evidence:

- run `34760486843`, job `103732346260`, artifact `10319085691` — pages 1–35
- run `34760591933`, job `103732623688`, artifact `10318299257` — pages 36–89, including target p82–83

## 7. Next gate

Stop spending evidence weight on transcription-only `亥` hits. Priority remains:

1. direct physical acquisition of the Jiajing-44 Shiqie target leaf; or
2. an independent early physical source that explicitly says the upper/night-Zi segment is reassigned to the Hai earthly branch.

Until then the candidate remains source-scoped and unimplemented.
'''
Path(batch_doc).write_text(doc, encoding='utf-8')

# Upgrade the Batch 12BH machine record with the physical follow-up while preserving its target-leaf caution.
bh_path = Path('docs/research/ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-R1.json')
bh = json.loads(bh_path.read_text(encoding='utf-8'))
assert bh['batch_id'] == prev
ctrl = bh['independent_textual_control']
ctrl['physical_followup_batch'] = batch_id
ctrl['physical_followup'] = {
    'source_id': source_id,
    'public_domain_scan': 'CADAL02094403 類編曆法通書大全（一）.djvu',
    'scan_sha256': evidence['source']['scan_sha256'],
    'target_scan_pages_1_based': [82, 83],
    'direct_physical_reading': physical_lines,
    'effect': 'Direct physical parallel confirms 上四刻/下四刻 terminology and date orientation; exact Shiqie target leaf remains unobserved.'
}
bh['adjudication']['parallel_physical_control_confirmed'] = True
bh['adjudication']['exact_shiqie_target_glyph_remains_unobserved'] = True
bh['adjudication']['transcription_token_status'] = 'STRONGLY_CORROBORATED_TRANSCRIPTION_ANOMALY_PENDING_EXACT_SHIQIE_PHYSICAL_LEAF'
bh_path.write_text(json.dumps(bh, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Register the independent physical source.
reg_path = Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg = json.loads(reg_path.read_text(encoding='utf-8'))
assert not any(s.get('source_id') == source_id for s in reg['sources'])
reg['sources'].append({
    'source_id': source_id,
    'title': '《類編曆法通書大全》（一）「論定半夜子時隔界」',
    'author_attribution': '熊宗立編纂（received attribution）',
    'historical_period': 'TRADITIONAL_CALENDRICAL_TEXT; EXACT_SCAN_IMPRESSION_DATE_NOT_ESTABLISHED_IN_BATCH_12BI',
    'provider': 'Wikimedia Commons / CADAL public-domain facsimile',
    'url': evidence['source']['commons_url'],
    'source_role': 'DIRECT_FACSIMILE_PARALLEL_FOR_UPPER_LOWER_FOUR_KE_TERMINOLOGY_AND_DATE_ORIENTATION',
    'quality_notes': 'Direct no-OCR visual collation of CADAL02094403 scan pp.82–83. Physically prints 係上四刻/係下四刻 and assigns the upper segment to 本日, lower segment to 第二日. It is an independent parallel, not the exact Shiqie target leaf and not evidence for upper-Zi -> Hai branch.',
    'batch_12bi': {
        'scan_sha256': evidence['source']['scan_sha256'],
        'scan_page_count': 89,
        'target_pages_1_based': [82, 83],
        'upper_four_ke_glyph_confirmed': True,
        'lower_four_ke_glyph_confirmed': True,
        'explicit_hai_branch_reassignment': False,
        'hai_glyph_witness_increment': 0,
        'research_artifact': evidence_path
    }
})
reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Attach the physical parallel to HPA-ZDATE-006 without changing status or reopening product logic.
matrix_path = Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix = json.loads(matrix_path.read_text(encoding='utf-8'))
row = next(r for r in matrix['rows'] if r.get('rule_id') == 'HPA-ZDATE-006')
assert row['audit_status'] == 'MISSING_FROM_PRODUCT'
row['batch_12bi_leibian_lifa_tongshu_physical'] = {
    'source_id': source_id,
    'physical_witness': 'Wikimedia Commons/CADAL02094403, scan pp.82–83',
    'secure_reading': '係上四刻，屬本日管；係下四刻，屬第二日管。',
    'mechanical_scope': 'DIRECT_PHYSICAL_PARALLEL_FOR_UPPER_LOWER_FOUR_KE_TERMINOLOGY_AND_DATE_ORIENTATION; NOT_THE_EXACT_SHIQIE_TARGET_LEAF; NOT_AN_UPPER_ZI_TO_HAI_BRANCH_RULE',
    'shiqie_anomaly_effect': 'STRONGLY_CORROBORATES_TRANSCRIPTION_ANOMALY; EXACT_SHIQIE_PHYSICAL_GLYPH_REMAINS_UNOBSERVED',
    'hai_glyph_witness_increment': 0,
    'candidate_status_effect': 'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
    'runtime_winner_selected': False,
    'algorithm_reopen_authorized': False,
    'research_artifact': evidence_path
}
later = row.get('later_witnesses', [])
addition = 'Independent physical 《類編曆法通書大全》 CADAL02094403 pp.82–83 directly prints 係上四刻/係下四刻 with 本日/第二日 date assignment; this strongly corroborates the Shiqie 上四亥 transcription-anomaly diagnosis but does not physically settle the exact Shiqie glyph or attest a Hai-branch reassignment.'
if isinstance(later, list):
    if addition not in later:
        later.append(addition)
    row['later_witnesses'] = later
else:
    if addition not in later:
        row['later_witnesses'] = later.rstrip() + ' ' + addition
matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Advance the durable current-state ledger.
state_path = Path('docs/PROJECT-CURRENT-STATE-R1.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
assert state['schema_version'] == '1.67.0'
state['schema_version'] = '1.68.0'
audit = state['historical_audit']
assert audit['completed_batches'][-1] == prev
audit['completed_batches'].append(batch_id)
audit['latest_batch_doc'] = batch_doc
focus = audit.setdefault('current_focus', [])
focus.extend([
    'Batch 12BI directly collates the public-domain CADAL02094403 《類編曆法通書大全》 scan pp.82–83: the physical leaf prints 係上四刻/係下四刻 and assigns them to 本日/第二日 respectively; no OCR is used for final glyph judgment.',
    'This independent physical parallel strongly corroborates the Batch 12BH diagnosis that Shiqie public-transcription 上四亥 is unsafe and likely anomalous, but the exact Jiajing-44 Shiqie target leaf remains unobserved. Hai-branch mechanical vote remains +0; HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen.'
])
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Keep the continuity verifier's supplemental batch ledger synchronized.
verifier_path = Path('scripts/verify-project-continuity-state-r1.py')
s = verifier_path.read_text(encoding='utf-8')
old = '''    "BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG",\n    "BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH.md"'''
new = '''    "BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG",\n    "BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH",\n    "BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI.md"'''
assert old in s
verifier_path.write_text(s.replace(old, new, 1), encoding='utf-8')

print(json.dumps({
    'batch_id': batch_id,
    'batch_doc': batch_doc,
    'evidence_path': evidence_path,
    'source_id': source_id,
    'hpa_zdate_006_status': row['audit_status'],
    'hai_glyph_witness_increment': 0,
    'runtime_winner_selected': False,
    'candidate_collapsed': False,
    'algorithm_reopen': False,
    'state_schema_version': state['schema_version'],
}, ensure_ascii=False, indent=2))
