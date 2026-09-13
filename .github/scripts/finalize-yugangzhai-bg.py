#!/usr/bin/env python3
from pathlib import Path
import json

batch_id='BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG'
batch_doc='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG.md'
evidence_path='docs/research/ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-R1.json'
source_id='EXT-ZIWEI-YUGANGZHAI-1602-COMMONS-CADAL02038286'
prev='BATCH-12-ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-BF'

facsimile_lines=[
  '夜子時',
  '曆家以子之前四刻屬今日爲夜子時而以子',
  '之後四刻屬明日今人生子以夜半者皆作明',
  '日推筭萬一以初爲正則四柱已差兩柱矣禍',
  '福豈不舛乎要之如西域法分二十四時而後',
  '無兩日共一時犬牙參錯之弊也',
]

evidence={
  'schema':'ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-R1',
  'batch_id':batch_id,
  'question':'Does an independent near-contemporary Ming witness physically attest night-Zi pre/post-midnight date attribution, and does it explicitly supply the still-missing upper/night-Zi-to-Hai branch reassignment bridge?',
  'source':{
    'title':'鬱岡齋筆麈',
    'author':'王肯堂',
    'historical_period':'明',
    'edition_identity':'明萬曆三十年（1602）王懋錕刻本（public bibliographic/facsimile metadata corroboration）',
    'scan_provider':'Wikimedia Commons',
    'commons_file':'CADAL02038286 鬱岡齋筆麈（三）.djvu',
    'commons_url':'https://commons.wikimedia.org/wiki/Special:Redirect/file/CADAL02038286%20%E9%AC%B1%E5%B2%A1%E9%BD%8B%E7%AD%86%E9%BA%88%EF%BC%88%E4%B8%89%EF%BC%89.djvu',
    'scan_sha256':'c4ffdcf04c4a49e6e7d3e4d7f93a25f6740096ac9f27f1db0ccc08cdb6a6de08',
    'scan_page_count':169,
    'target_scan_pages_1_based':[87,88],
    'shidian_locator':{
      'book_id':'CADAL02038284',
      'chapter_id':'1l7mkadqnliiy',
      'url':'https://www.shidianguji.com/zh/book/CADAL02038284/chapter/1l7mkadqnliiy',
      'public_html_status':200,
      'public_html_body_len':1284506,
      'public_html_sha256':'01a0a3e8ea517569b174b4338cb0412607e434e0b93a14984173384f2c889a7a',
      'role':'LOCATOR_AND_TRANSCRIPTION_CORROBORATION_NOT_FINAL_GLYPH_AUTHORITY'
    }
  },
  'physical_collation':{
    'method':'DIRECT_VISUAL_COLLATION_OF_RENDERED_PUBLIC_DOMAIN_DJVU_PAGES; NO_OCR_USED_FOR_FINAL_GLYPH_JUDGMENT',
    'page_87_lines':facsimile_lines[:3],
    'page_88_lines':facsimile_lines[3:],
    'normalized_reading':'曆家以子之前四刻屬今日，爲夜子時；而以子之後四刻屬明日。今人生子以夜半者皆作明日推筭，萬一以初爲正，則四柱已差兩柱矣，禍福豈不舛乎？要之如西域法分二十四時，而後無兩日共一時犬牙參錯之弊也。',
    'secure_semantics':[
      '子之前四刻屬今日',
      '子之前四刻被明稱爲夜子時',
      '子之後四刻屬明日',
      '作者明確警告把夜半子生一概作明日推算可令四柱差兩柱',
      '作者提出分二十四時以避免兩日共一時的犬牙參錯'
    ],
    'explicit_hai_branch_reassignment_present':False
  },
  'workflow_evidence':{
    'physical_probe_run_id':34756513240,
    'physical_probe_job_id':103721687957,
    'physical_probe_artifact_id':10316898759,
    'physical_probe_artifact_zip_sha256':'f98d7602c73f3c44ac9f65d06da6efc3bcf9bd27d613418b91156270d3aee7a4',
    'rendered_page_band':[70,96]
  },
  'rule_adjudication':{
    'independent_ming_night_zi_date_semantics_witness':True,
    'near_contemporary_to_1594_zhangguo':True,
    'date_attribution_bridge_strengthened':True,
    'upper_night_zi_to_hai_branch_explicitly_attested':False,
    'hai_glyph_witness_increment':0,
    'hpa_zdate_006_status':'MISSING_FROM_PRODUCT',
    'runtime_winner_selected':False,
    'candidate_collapsed':False,
    'algorithm_reopen':False,
    'required_missing_bridge':'upper/night Zi -> Hai branch'
  },
  'access_policy':'PUBLIC_SHIDIAN_HTML_AS_LOCATOR; PUBLIC_DOMAIN_WIKIMEDIA_COMMONS_DJVU_FOR_PHYSICAL_COLLATION; NO LOGIN; NO PRIVATE API GUESSING; NO ACCESS BYPASS; NO OCR AS FINAL GLYPH AUTHORITY'
}
Path(evidence_path).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc='''# Fusion Chart Historical Provenance Audit R1 — Batch 12BG

## 《鬱岡齋筆麈》萬曆三十年「夜子時」原葉物理校讀

Status: **DIRECT PUBLIC-DOMAIN FACSIMILE COLLATION / MING WANLI-30 (1602) WANG KENTANG WITNESS / SCAN P87–88 DIRECTLY ATTESTS PRE-MIDNIGHT FOUR KE = TODAY = 夜子時 AND POST-MIDNIGHT FOUR KE = TOMORROW / AUTHOR WARNS UNIFORM NEXT-DAY TREATMENT CAN SHIFT TWO PILLARS / NO EXPLICIT 亥-BRANCH REASSIGNMENT / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AW established an early 1594 Zhang Guo Xingzong witness for two facts that must not be conflated: birth-time Zi/Hai confusion exists, and a night-Zi upper/lower-four-ke distinction exists. It still did **not** directly state the mechanical bridge `upper/night Zi -> Hai branch`.

Batch 12BG asks whether a separate Ming witness close in time can independently fix the temporal/date semantics of the night-Zi split, and whether that witness itself supplies the missing Hai-branch reassignment.

## 2. Source and physical scan

The source is 王肯堂《鬱岡齋筆麈》. Public bibliographic/facsimile metadata identifies the relevant edition tradition as the **明萬曆三十年（1602）王懋錕刻本**.

A public-domain Wikimedia Commons DJVU was acquired directly:

- file: `CADAL02038286 鬱岡齋筆麈（三）.djvu`
- SHA-256: `c4ffdcf04c4a49e6e7d3e4d7f93a25f6740096ac9f27f1db0ccc08cdb6a6de08`
- page count: `169`
- target scan pages: `87–88`

The final glyph judgment below was made by direct visual collation of the rendered facsimile pages, not OCR.

## 3. Direct physical collation

### Scan p.87

> 夜子時
>
> 曆家以子之前四刻屬今日爲夜子時而以子
>
> 之後四刻屬明日今人生子以夜半者皆作明

### Scan p.88

> 日推筭萬一以初爲正則四柱已差兩柱矣禍
>
> 福豈不舛乎要之如西域法分二十四時而後
>
> 無兩日共一時犬牙參錯之弊也

Normalized only for punctuation, not mechanics:

> 曆家以子之前四刻屬今日，爲夜子時；而以子之後四刻屬明日。今人生子以夜半者皆作明日推筭，萬一以初爲正，則四柱已差兩柱矣，禍福豈不舛乎？要之如西域法分二十四時，而後無兩日共一時犬牙參錯之弊也。

## 4. Philological/mechanical adjudication

The physical leaf securely establishes all of the following:

1. `子之前四刻` is assigned to **今日**.
2. The same pre-midnight four-ke segment is explicitly named **夜子時**.
3. `子之後四刻` is assigned to **明日**.
4. Wang Kentang considers indiscriminately treating midnight-Zi births as the next day capable of shifting **two pillars**.
5. He prefers a 24-hour division to avoid one traditional double-hour straddling two civil/calendar dates.

This is an important independent Ming witness for the **orientation and date attribution** of night Zi. It is also very close chronologically to the 1594 Zhang Guo Xingzong witness.

But it does **not** state that the pre-midnight/night-Zi segment is mechanically reclassified as the earthly branch `亥`.

Therefore:

```text
pre-midnight upper/night Zi -> current/today date     DIRECTLY ATTESTED
post-midnight lower Zi -> next/tomorrow date          DIRECTLY ATTESTED
upper/night Zi -> Hai branch                          NOT DIRECTLY ATTESTED
```

The date-semantic bridge is stronger; the branch-reassignment bridge remains missing.

## 5. Effect on HPA-ZDATE-006

No status change is authorized:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- new explicit `亥`-branch vote: `0`
- runtime winner selected: `false`
- candidate collapsed: `false`
- algorithm reopen: `false`

The current product still lacks a source-scoped runtime method for the Nanyangtang-style half-Zi-to-Hai natal-hour candidate, but this batch does not by itself prove that candidate's branch mapping.

## 6. Relationship to the 1594 Zhang Guo witness

The two independent Ming witnesses now converge on a narrower historical point:

- Zhang Guo Xingzong 1594: night Zi has an upper/lower-four-ke division; the surrounding birth-time discussion explicitly recognizes Zi/Hai confusion.
- Yugangzhai 1602: pre-midnight four ke are `今日` and called `夜子時`; post-midnight four ke are `明日`.

What still cannot be inferred without another direct text is that the first statement's upper four ke and the second statement's night-Zi/current-day segment **must therefore be labeled Hai branch**. That inference remains philologically plausible but mechanically unclosed.

## 7. Access/research controls

The research path used only:

1. Shidian public HTML already delivered without authentication, as a locator/transcription aid;
2. a Wikimedia Commons public-domain DJVU for physical-page collation;
3. direct visual reading of the target pages.

No CText restriction was bypassed, no login was used, no private API was guessed, and OCR was not used as final glyph authority.

## 8. Durable evidence

Machine-readable evidence is stored at:

`docs/research/ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-R1.json`

Hosted research run:

- run `34756513240`
- job `103721687957`
- artifact `10316898759`
- artifact ZIP SHA-256 `f98d7602c73f3c44ac9f65d06da6efc3bcf9bd27d613418b91156270d3aee7a4`

## 9. Next gate

Continue prioritizing an independent early source whose physical target leaf says, in direct mechanical terms, that the upper/night-Zi segment is `亥` or otherwise unambiguously maps that segment to Hai branch. Catalog-only duplicates and date-semantics-only witnesses must not be counted as that missing bridge.
'''
Path(batch_doc).write_text(doc,encoding='utf-8')

reg_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg=json.loads(reg_path.read_text(encoding='utf-8'))
assert not any(s.get('source_id')==source_id for s in reg['sources'])
reg['sources'].append({
  'source_id':source_id,
  'title':'《鬱岡齋筆麈》卷三「夜子時」',
  'author':'王肯堂',
  'historical_period':'明',
  'edition':'明萬曆三十年（1602）王懋錕刻本（public bibliographic/facsimile metadata）',
  'provider':'Wikimedia Commons public-domain CADAL facsimile; Shidian public HTML locator',
  'url':'https://commons.wikimedia.org/wiki/Special:Redirect/file/CADAL02038286%20%E9%AC%B1%E5%B2%A1%E9%BD%8B%E7%AD%86%E9%BA%88%EF%BC%88%E4%B8%89%EF%BC%89.djvu',
  'source_role':'DIRECT_FACSIMILE_WITNESS_FOR_MING_NIGHT_ZI_DATE_ATTRIBUTION',
  'quality_notes':'Direct no-OCR physical collation of public-domain DJVU scan pages 87–88. Securely attests 子之前四刻屬今日/夜子時 and 子之後四刻屬明日, plus the warning that uniform next-day treatment can shift two pillars. It does not explicitly reclassify upper/night Zi as Hai branch, so it is not a Hai-glyph/mechanical branch vote.',
  'batch_12bg':{
    'scan_sha256':'c4ffdcf04c4a49e6e7d3e4d7f93a25f6740096ac9f27f1db0ccc08cdb6a6de08',
    'scan_page_count':169,
    'target_pages_1_based':[87,88],
    'physical_text_confirmed':True,
    'pre_midnight_four_ke_today_night_zi_confirmed':True,
    'post_midnight_four_ke_tomorrow_confirmed':True,
    'explicit_hai_branch_reassignment':False,
    'hai_glyph_witness_increment':0,
    'research_artifact':evidence_path
  }
})
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

matrix_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix=json.loads(matrix_path.read_text(encoding='utf-8'))
rows=[r for r in matrix['rows'] if r.get('rule_id')=='HPA-ZDATE-006']
assert len(rows)==1, len(rows)
row=rows[0]
assert 'batch_12bg_yugangzhai_1602' not in row
row['batch_12bg_yugangzhai_1602']={
  'source_id':source_id,
  'physical_witness':'王肯堂《鬱岡齋筆麈》萬曆三十年（1602）刻本傳統，Wikimedia Commons CADAL02038286，scan pp.87–88',
  'secure_reading':'曆家以子之前四刻屬今日爲夜子時而以子之後四刻屬明日……則四柱已差兩柱矣……',
  'mechanical_scope':'DIRECT_INDEPENDENT_MING_ATTESTATION_OF_PRE_MIDNIGHT_FOUR_KE_AS_TODAY_NIGHT_ZI_AND_POST_MIDNIGHT_FOUR_KE_AS_TOMORROW; NO_EXPLICIT_UPPER_NIGHT_ZI_TO_HAI_BRANCH_REASSIGNMENT',
  'candidate_status_effect':'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
  'hai_glyph_witness_increment':0,
  'runtime_winner_selected':False,
  'algorithm_reopen_authorized':False,
  'research_artifact':evidence_path
}
later=row.get('later_witnesses','')
addition=' Independent Ming Wanli-30/1602 Wang Kentang Yugangzhai facsimile directly attests pre-midnight four ke as 今日/夜子時 and post-midnight four ke as 明日, but does not state a Hai-branch reassignment.'
if addition.strip() not in later:
    row['later_witnesses']=later.rstrip()+addition
matrix_path.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

state_path=Path('docs/PROJECT-CURRENT-STATE-R1.json')
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state.get('schema_version')=='1.65.0', state.get('schema_version')
audit=state['historical_audit']
assert audit['completed_batches'][-1]==prev, audit['completed_batches'][-1]
assert batch_id not in audit['completed_batches']
audit['completed_batches'].append(batch_id)
audit['latest_batch_doc']=batch_doc
audit['current_focus'].append('Batch 12BG directly collates Wang Kentang 《鬱岡齋筆麈》 night-Zi physical facsimile pages 87–88 from the public-domain Commons CADAL02038286 scan: 子之前四刻屬今日 and is explicitly called 夜子時, while 子之後四刻屬明日; Wang warns that indiscriminate next-day treatment can shift two pillars.')
audit['current_focus'].append('The 1602 Yugangzhai witness strengthens independent Ming date-orientation semantics but contains no explicit upper/night-Zi -> Hai branch reassignment. Hai-glyph/mechanical vote increment remains 0; HPA-ZDATE-006 stays MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen.')
state['schema_version']='1.66.0'
state['updated_at']='2026-09-13'
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

verifier_path=Path('scripts/verify-project-continuity-state-r1.py')
text=verifier_path.read_text(encoding='utf-8')
old='    "BATCH-12-ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-BE",\n    "BATCH-12-ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-BF",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-BF.md"'
new='    "BATCH-12-ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-BE",\n    "BATCH-12-ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-BF",\n    "BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-BG.md"'
assert old in text
verifier_path.write_text(text.replace(old,new,1),encoding='utf-8')

# Machine invariants for this research-only batch.
assert state['invariants']['deterministic_fusion_chart_product_r1']=='CLOSED'
assert state['invariants']['confirmed_chart_algorithm_defect_count']==0
assert state['invariants']['algorithm_reopen_count']==0
assert state['invariants']['candidate_collapse_count']==0
assert state['invariants']['ziwei_self_inward_transformation_direction']=='NOT_YET_FORMALIZED'
assert row['audit_status']=='MISSING_FROM_PRODUCT'
assert row['algorithm_reopen_authorized'] is False
