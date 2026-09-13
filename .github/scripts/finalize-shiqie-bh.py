#!/usr/bin/env python3
from pathlib import Path
import json

batch_id = 'BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH'
batch_doc = 'docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH.md'
evidence_path = 'docs/research/ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-R1.json'
source_id = 'EXT-ZIWEI-SHIQIE-LISHU-RISHU-1565-SHIDIAN'
control_source_id = 'EXT-LIBIAN-LIFA-TONGSHU-DAQUAN-SHIDIAN'
prev = 'BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG'

shiqie_url = 'https://www.shidianguji.com/zh/book/NA06425/chapter/1m44zy4jwa4ab'
control_url = 'https://www.shidianguji.com/zh/book/SDZJ0731/chapter/1lcugwsgqj66n'

transcription_excerpt = (
    '初初刻、初一刻、初二刻、初三刻、初四刻，巳上是上四亥。'
    '正初刻、正一刻、正二刻、正三刻、正四刻，巳上是下四刻。'
    '論子時隔界，凡半夜子時隔界之類，一時有八刻二十分。'
    '上四刻屬本日管，下四刻屬第二日管。'
    '曰：謹按大明成化十八年壬寅歲，授時官曆，四月二十六日甲子夜子時初二刻，小滿，'
    '是上四刻作二十六日管，故有夜字。'
)

control_excerpt = (
    '論定半夜子時隔界。子初初刻、初二刻、初三刻、初四刻，係上四刻，屬本日管。'
    '子正一刻、正二刻、正三刻、正四刻，係下四刻，屬第二日管。'
)

evidence = {
    'schema': 'ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-R1',
    'batch_id': batch_id,
    'question': 'Does the public transcription token 上四亥 in the Jiajing-44 Shiqie Lishu Rishu constitute direct mechanical evidence that upper/night Zi is reassigned to Hai branch?',
    'source': {
        'title': '筮篋理數日抄',
        'author_metadata': '一壺天俱道人',
        'edition_metadata': '嘉靖44年刊本',
        'edition_year_ce': 1565,
        'dynasty_metadata': '明',
        'book_id': 'NA06425',
        'chapter_id': '1m44zy4jwa4ab',
        'chapter': '卷三 / 選時寶鏡局 / 論子時隔界',
        'provider': '識典古籍 public HTML transcription surface',
        'url': shiqie_url,
        'image_source_metadata': '日本内阁文库',
        'total_page_metadata': 2148,
        'source_role': 'PUBLIC_TRANSCRIPTION_LOCATOR_AND_TRANSMISSION_WITNESS_NOT_PHYSICAL_GLYPH_AUTHORITY',
    },
    'target_binding': {
        'target_token': '巳上是上四亥',
        'target_page_id': '7640563520069697576',
        'preceding_page_id': '7640563520069681192',
        'target_paragraph_id': '7649191097545588762',
        'following_paragraph_ids': ['7649191097545605146', '7649191097545621530'],
        'zi_boundary_body_paragraph_id': '7649191097545670682',
        'physical_target_leaf_observed': False,
        'literal_target_image_url_emitted_in_reviewed_public_ssr': False,
    },
    'public_transcription': {
        'excerpt': transcription_excerpt,
        'anomaly_token': '上四亥',
        'parallel_lower_label': '下四刻',
        'same_passage_semantic_labels': ['上四刻屬本日管', '下四刻屬第二日管', '是上四刻作二十六日管'],
        'date_orientation_supported_at_transcription_level': True,
        'explicit_upper_zi_to_hai_branch_rule_supported': False,
        'reason': 'The isolated 上四亥 occurs in a counting-label slot parallel to 下四刻 and is immediately followed by repeated 上四刻/下四刻 mechanics. Without the physical leaf, it cannot be promoted into a Hai-branch reassignment statement.',
    },
    'independent_textual_control': {
        'title': '類編曆法通書大全卷之一',
        'compiler_metadata': '明 熊宗立 編纂',
        'provider': '識典古籍 public transcription surface',
        'url': control_url,
        'excerpt': control_excerpt,
        'role': 'INDEPENDENT_TRANSMISSION_TEXTUAL_CONTROL_FOR_UPPER_FOUR_KE_LABEL_AND_DATE_ORIENTATION; NOT_PHYSICAL_GLYPH_AUTHORITY',
        'effect': 'Strengthens the reading that the conceptual label is 上四刻, but does not itself settle the physical glyph in the Shiqie target leaf or prove Hai-branch reassignment.',
    },
    'hosted_research_runs': [
        {
            'run_id': 34757884458,
            'job_id': 103725325831,
            'artifact_id': 10318013507,
            'artifact_zip_sha256': 'e4300ae6277c3add93dd9ad13cea527fb795a2bbcfac0f3d3623da4c58db5125',
            'role': 'PUBLIC_HTML_PAYLOAD_AND_METADATA_PROBE',
            'observations': ['HTTP 200', '嘉靖44年刊本', '日本内阁文库', '巳上是上四亥 x2', '上四刻屬本日管 x2'],
        },
        {
            'run_id': 34757969310,
            'job_id': 103725555573,
            'artifact_id': 10316869368,
            'artifact_zip_sha256': '05d3cce9694731ffe0c0b212e0fda80baa3b0ddb3c413e432bf34834ceff0221',
            'role': 'TARGET_PAGE_AND_PARAGRAPH_BINDING_PROBE',
        },
        {
            'run_id': 34758029250,
            'job_id': 103725721203,
            'artifact_id': 10316913977,
            'artifact_zip_sha256': 'e587497eb097f0fb53f9f5234922756b7ffd4ade9e50ca183f9927f1964ed9f6',
            'role': 'EXACT_TARGET_PAGE_PUBLIC_IMAGE_CONTRACT_PROBE',
            'target_image_download_count': 0,
        },
        {
            'run_id': 34758132419,
            'job_id': 103726004114,
            'artifact_id': 10317872820,
            'artifact_zip_sha256': '6dc815e18d16e68844865291ef6d14180341afe54965f80b03e9c4d3f00dfad2',
            'role': 'JAPAN_NATIONAL_ARCHIVES_PUBLIC_ROOT_ACCESS_BOUNDARY',
            'result': 'HTTP 403 on public root URLs from hosted runner; no hidden endpoint guessed',
        },
        {
            'run_id': 34758215209,
            'job_id': 103726225297,
            'artifact_id': 10318445180,
            'artifact_zip_sha256': '9b3a50d8e3eb9649f47db26350a221b0857aa0589bcdd7288ed11234cbc95b8a',
            'role': 'PUBLIC_CABINET_LIBRARY_CATALOG_LINK_DISCOVERY',
            'result': 'Catalog page HTTP 200 and title occurrences observed; no literal National Archives href emitted around target entries',
        },
    ],
    'adjudication': {
        'transcription_token_status': 'QUARANTINED_PENDING_PHYSICAL_LEAF',
        'likely_label_family': 'UPPER_FOUR_KE / LOWER_FOUR_KE',
        'physical_glyph_judgment_authorized': False,
        'hai_branch_reassignment_directly_attested': False,
        'hai_glyph_witness_increment': 0,
        'hpa_zdate_006_status': 'MISSING_FROM_PRODUCT',
        'runtime_winner_selected': False,
        'candidate_collapsed': False,
        'algorithm_reopen': False,
        'next_gate': 'Acquire the physical target leaf for the Jiajing-44 Shiqie copy or another independent early leaf that unambiguously states upper/night Zi -> Hai branch.',
    },
    'access_policy': 'PUBLIC_HTML_AND_LITERAL_RESOURCE CONTRACTS ONLY; NO LOGIN; NO PRIVATE API OR OBJECT-ID GUESSING; NO CERTIFICATE/ACCESS BYPASS; TRANSCRIPTION NOT FINAL GLYPH AUTHORITY',
}
Path(evidence_path).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

doc = f'''# Fusion Chart Historical Provenance Audit R1 — Batch 12BH

## 《筮篋理數日抄》嘉靖四十四年本「上四亥」转录异常审判

Status: **PUBLIC TRANSCRIPTION LOCATOR / JIAJING-44 (1565) EDITION METADATA / TARGET PAGE+PARAGRAPH IDS BOUND / `上四亥` QUARANTINED PENDING PHYSICAL LEAF / SAME PASSAGE REPEATEDLY SAYS `上四刻` AND `下四刻` / INDEPENDENT TONGSHU TRANSCRIPTION ALSO SAYS `係上四刻` / NO PHYSICAL TARGET GLYPH / NO HAI-BRANCH MECHANICAL VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BG strengthened the historical date orientation of night Zi but still did not supply the missing mechanical bridge `upper/night Zi -> Hai branch`.

A new public transcription of 《筮篋理數日抄》 appears at first glance to contain the unusually attractive token `上四亥`. Because that token would materially affect HPA-ZDATE-006, this batch treats it adversarially: it must survive internal philology, independent textual control, and physical-leaf verification before it can count as a Hai-branch witness.

## 2. Source identity and access surface

Public metadata delivered by the Shidian page identifies:

- title: 《筮篋理數日抄》
- author metadata: 一壺天俱道人
- edition metadata: **嘉靖44年刊本** (1565)
- image-source metadata: **日本内阁文库**
- book ID: `NA06425`
- chapter ID: `1m44zy4jwa4ab`
- total-page metadata: `2148`

This is a **public digital transcription/locator surface**. The target physical leaf itself has not yet been directly read in this project.

## 3. Target transcription

The delivered transcription reads:

> 初初刻、初一刻、初二刻、初三刻、初四刻，巳上是上四亥。
>
> 正初刻、正一刻、正二刻、正三刻、正四刻，巳上是下四刻。
>
> 論子時隔界，凡半夜子時隔界之類，一時有八刻二十分。上四刻屬本日管，下四刻屬第二日管。
>
> ……四月二十六日甲子夜子時初二刻，小滿，是上四刻作二十六日管，故有夜字。

The target is bound on the public payload to page ID `7640563520069697576`; target paragraph ID `7649191097545588762` contains `巳上是上四亥。`.

## 4. Philological/mechanical adjudication

`上四亥` is **not** accepted as a branch-reassignment statement.

The reasons are cumulative:

1. It occurs in a counting-label slot after a five-entry list of `初...刻` values.
2. The exactly parallel lower list ends `巳上是下四刻`.
3. The immediately following explanatory prose explicitly says `上四刻屬本日管，下四刻屬第二日管`.
4. The example sentence again says `是上四刻作二十六日管`.
5. An independent received transcription of 熊宗立《類編曆法通書大全》 preserves the same mechanism as `係上四刻，屬本日管` / `係下四刻，屬第二日管`.

Accordingly, the strongest defensible judgment is:

```text
Shiqie public transcription contains literal token 上四亥     OBSERVED
physical target leaf glyph = 亥                            NOT OBSERVED
上四亥 means upper Zi is reassigned to Hai branch          NOT ESTABLISHED
upper four ke = current/base day                            TRANSCRIPTION-LEVEL SUPPORT
lower four ke = second/next day                            TRANSCRIPTION-LEVEL SUPPORT
```

Even if a future physical collation were to confirm that the printed glyph really is `亥`, the sentence would still require contextual proof that it denotes an Earthly-Branch reassignment rather than a typographical/lexical anomaly. Mechanical identity cannot be inferred from a single glyph alone.

## 5. Access-boundary findings

The research path stayed fail-closed:

- Shidian public HTML returned the edition metadata, target transcription, page IDs and paragraph IDs.
- The reviewed public SSR payload did **not** emit a literal target-page image URL for the bound target page IDs.
- The National Archives of Japan public root returned HTTP 403 to the hosted runner; no hidden search endpoint or object ID was guessed.
- A public Cabinet Library catalog mirror listed the title but emitted no literal National Archives href around the entries.

Therefore no physical target leaf was obtained and no access restriction was bypassed.

## 6. Effect on HPA-ZDATE-006

No product or historical-winner state changes:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- new explicit Hai-branch mechanical vote: `0`
- physical Hai-glyph witness increment: `0`
- runtime winner selected: `false`
- candidate collapsed: `false`
- algorithm reopen: `false`

This batch is valuable precisely because it prevents an attractive transcription token from being overcounted.

## 7. Durable evidence

Machine-readable evidence:

`{evidence_path}`

Hosted research runs are recorded there with run/job/artifact IDs and artifact ZIP SHA-256 values.

## 8. Next gate

Acquire either:

1. the physical target leaf of the Jiajing-44 《筮篋理數日抄》 copy and read the disputed glyph directly; or
2. another independent early physical leaf that states in unambiguous mechanical terms that upper/night Zi is assigned to the Earthly Branch Hai.

Date-semantics-only witnesses and catalog duplicates must continue to receive zero Hai-branch mechanical votes.
'''
Path(batch_doc).write_text(doc, encoding='utf-8')

# External source registry: register the source as a transcription/locator, not glyph authority.
reg_path = Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg = json.loads(reg_path.read_text(encoding='utf-8'))
assert not any(s.get('source_id') == source_id for s in reg['sources'])
assert not any(s.get('source_id') == control_source_id for s in reg['sources'])
reg['sources'].append({
    'source_id': source_id,
    'title': '《筮篋理數日抄》卷三「論子時隔界」',
    'author_metadata': '一壺天俱道人',
    'historical_period': '明 / public metadata identifies 嘉靖44年刊本 (1565)',
    'edition': '嘉靖44年刊本（public platform metadata; target physical leaf not yet collated）',
    'provider': '識典古籍 public HTML transcription surface',
    'url': shiqie_url,
    'source_role': 'PUBLIC_TRANSCRIPTION_LOCATOR_AND_HIGH_RISK_GLYPH_ANOMALY_NOT_PHYSICAL_AUTHORITY',
    'quality_notes': 'Public payload says 巳上是上四亥, but the parallel lower label is 下四刻 and the same passage repeatedly says 上四刻/下四刻. Target page/paragraph IDs are bound, but no literal target-image URL was emitted on the reviewed SSR surface and no physical leaf has been read. Zero Hai-branch/mechanical vote pending physical collation.',
    'batch_12bh': {
        'book_id': 'NA06425',
        'target_page_id': '7640563520069697576',
        'target_paragraph_id': '7649191097545588762',
        'literal_transcription_token': '巳上是上四亥',
        'physical_target_leaf_observed': False,
        'hai_branch_mechanical_vote': 0,
        'research_artifact': evidence_path,
    },
})
reg['sources'].append({
    'source_id': control_source_id,
    'title': '《類編曆法通書大全》卷一「論定半夜子時隔界」',
    'compiler_metadata': '明 熊宗立 編纂',
    'historical_period': 'received Ming calendrical/almanac tradition; exact target physical leaf not collated in Batch 12BH',
    'provider': '識典古籍 public transcription surface',
    'url': control_url,
    'source_role': 'INDEPENDENT_TRANSMISSION_TEXTUAL_CONTROL_FOR_UPPER_LOWER_FOUR_KE_DATE_ORIENTATION',
    'quality_notes': 'Public transcription reads 係上四刻，屬本日管 / 係下四刻，屬第二日管. Used only as an independent textual control against overreading the Shiqie 上四亥 token; not counted as physical glyph authority or as an upper-Zi-to-Hai branch vote.',
})
reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Historical matrix: add a source-scoped zero-vote adjudication under HPA-ZDATE-006.
matrix_path = Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix = json.loads(matrix_path.read_text(encoding='utf-8'))
rows = [r for r in matrix['rows'] if r.get('rule_id') == 'HPA-ZDATE-006']
assert len(rows) == 1
row = rows[0]
assert 'batch_12bh_shiqie_1565_transcription_anomaly' not in row
row['batch_12bh_shiqie_1565_transcription_anomaly'] = {
    'source_id': source_id,
    'edition_metadata': '嘉靖44年刊本 / 1565',
    'public_transcription_token': '巳上是上四亥',
    'same_passage_control': '巳上是下四刻；上四刻屬本日管；下四刻屬第二日管；是上四刻作二十六日管',
    'target_page_id': '7640563520069697576',
    'target_paragraph_id': '7649191097545588762',
    'physical_target_leaf_observed': False,
    'transcription_token_status': 'QUARANTINED_PENDING_PHYSICAL_LEAF',
    'mechanical_scope': 'DATE_ORIENTATION_SUPPORTED_AT_TRANSCRIPTION_LEVEL; NO_DIRECT_UPPER_NIGHT_ZI_TO_HAI_BRANCH_REASSIGNMENT',
    'hai_glyph_witness_increment': 0,
    'runtime_winner_selected': False,
    'candidate_collapsed': False,
    'algorithm_reopen_authorized': False,
    'research_artifact': evidence_path,
}
later = row.get('later_witnesses', [])
addition = 'Jiajing-44/1565 Shiqie Lishu Rishu public transcription contains isolated 上四亥, but the parallel and explanatory text repeatedly says 上四刻/下四刻; without the physical target leaf this token is quarantined and contributes zero Hai-branch mechanical votes.'
if isinstance(later, list):
    if addition not in later:
        later.append(addition)
    row['later_witnesses'] = later
else:
    if addition not in later:
        row['later_witnesses'] = later.rstrip() + ' ' + addition
pa = row.get('proposed_action', '')
extra = ' Do not count the Shiqie 上四亥 transcription token as a Hai-branch witness unless direct physical collation and contextual mechanics close the ambiguity.'
if extra.strip() not in pa:
    row['proposed_action'] = pa.rstrip() + extra
matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Current state: append the supplemental batch and make it the latest research batch.
state_path = Path('docs/PROJECT-CURRENT-STATE-R1.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
assert state['historical_audit']['completed_batches'][-1] == prev
assert batch_id not in state['historical_audit']['completed_batches']
state['schema_version'] = '1.67.0'
state['historical_audit']['completed_batches'].append(batch_id)
state['historical_audit']['latest_batch_doc'] = batch_doc
focus = state['historical_audit']['current_focus']
focus_lines = [
    'Batch 12BH binds the Jiajing-44/1565 Shiqie Lishu Rishu public transcription to target page ID 7640563520069697576 and paragraph 7649191097545588762. The surface literally contains 巳上是上四亥, but the parallel lower label and explanatory mechanics repeatedly say 下四刻 / 上四刻屬本日管 / 下四刻屬第二日管.',
    'The Shiqie target physical leaf remains unread: the reviewed SSR surface emitted no literal target image URL, Japan National Archives public root returned hosted-runner 403, and a public Cabinet Library catalog mirror emitted no first-party object href. Therefore 上四亥 is quarantined as a transcription anomaly, Hai/mechanical vote increment remains 0, and HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no winner, collapse, or algorithm reopen.'
]
for line in focus_lines:
    if line not in focus:
        focus.append(line)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Continuity verifier: extend the documented zero-row-effect supplemental sequence.
verify_path = Path('scripts/verify-project-continuity-state-r1.py')
vs = verify_path.read_text(encoding='utf-8')
old_tail = '''    "BATCH-12-ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-BF",\n    "BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG.md"'''
new_tail = '''    "BATCH-12-ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-BF",\n    "BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG",\n    "BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH.md"'''
assert old_tail in vs
vs = vs.replace(old_tail, new_tail, 1)
verify_path.write_text(vs, encoding='utf-8')

print(json.dumps({
    'batch_id': batch_id,
    'batch_doc': batch_doc,
    'evidence': evidence_path,
    'hpa_zdate_006_status': row['audit_status'],
    'hai_glyph_witness_increment': row['batch_12bh_shiqie_1565_transcription_anomaly']['hai_glyph_witness_increment'],
    'state_schema_version': state['schema_version'],
    'completed_batch_tail': state['historical_audit']['completed_batches'][-3:],
}, ensure_ascii=False, indent=2))
