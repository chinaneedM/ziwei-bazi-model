#!/usr/bin/env python3
from pathlib import Path
import json

batch_id='BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL'
batch_doc='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL.md'
evidence_path='docs/research/ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-R1.json'
source_id='EXT-ZIWEI-SHIQIE-LISHU-RISHU-1565-SHIDIAN'
prev='BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK'
target_page_id='7640563520069697576'
api_body_sha='460a68650881f42750a8226fdd4a5ed610e1b7a200d4a4a95735c0724cd90572'
ref_page_ids=[
  '7640563520069746728','7640563520069763112','7640563520069795880','7640563520069812264',
  '7640563520069828648','7640563520069845032','7640563520069861416','7640563520069877800'
]

evidence={
  'schema':'ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-R1',
  'batch_id':batch_id,
  'question':'Does ordinary anonymous navigation of the public Shidian fascicle-three chapter itself return target-page image metadata or a target-page image for pageId 7640563520069697576, without replaying, constructing, or enumerating private/hidden routes?',
  'public_chapter':{
    'url':'https://www.shidianguji.com/zh/book/NA06425/chapter/1m44zy4jwa4ab',
    'navigation_http_status':200,
    'title':'卷三-筮篋理數日抄全文原文-識典古籍',
    'book_id':'NA06425',
    'chapter_id':'1m44zy4jwa4ab',
    'target_page_id':target_page_id,
    'target_paragraph_id':'7649191097545588762',
    'target_transcription':'巳上是上四亥。',
    'rendered_ssr_contains_target_text':True,
    'rendered_ssr_contains_target_page_id':True,
    'authority_scope':'PUBLIC SSR TRANSCRIPTION/LOCATOR ONLY; NOT PHYSICAL GLYPH AUTHORITY'
  },
  'passive_browser_probe':{
    'run_id':34765718210,
    'artifact_id':10320391963,
    'artifact_digest':'sha256:1665c297d024f7cf234574a5f38e6594168c7c1ab8c3742eb8546d586364060a',
    'result':'ORDINARY BROWSER NAVIGATION EMITTED PUBLIC READ-API REQUESTS AND SIGNED REF-IMAGE REQUESTS; HYDRATED CLIENT DISPLAYED DATA-ERROR PLACEHOLDER WHILE SSR TARGET TEXT/PAGE ID REMAINED IN HTML.'
  },
  'source_emitted_read_api_capture':{
    'run_id':34765824117,
    'artifact_id':10320861185,
    'artifact_digest':'sha256:79ba56e995d27d26e7fb83fdf243c46ef3a03c4d43e261def860e30e9c5f29ae',
    'captured_response_count':4,
    'all_http_status':200,
    'all_application_body':{'errorCode':31000,'errorMsg':''},
    'all_application_body_len':33,
    'all_application_body_sha256':api_body_sha,
    'target_text_returned_by_api':False,
    'target_page_id_returned_by_api':False,
    'endpoints':[
      {'path':'/api/ancientlib/read/book/dynamic-info/get','method':'POST','source_emitted_payload':{'bookId':'NA06425'}},
      {'path':'/api/ancientlib/read/review/chapter-list/','method':'GET','source_emitted_query_scope':{'bookId':'NA06425','chapterId':'1m44zy4jwa4ab','volumeVersion':1}},
      {'path':'/api/ancientlib/read/book/paragraphs/v3/','method':'POST','source_emitted_payload_scope':{'bookId':'NA06425','chapterId':'1m44zy4jwa4ab','pageSize':100,'currentPage':0,'forwardParaNum':10,'omitContent':False,'requestMode':0,'bookVersion':0}},
      {'path':'/api/ancientlib/read/book/pages/v3/','method':'POST','source_emitted_payload_scope':{'bookId':'NA06425','pageIndex':1,'pageSize':40,'startPageNum':353,'endPageNum':409,'version':1,'needCheckVersion':True,'ptoken_present':True}}
    ],
    'interpretation':'The public page itself attempted a pages request whose range covers the opening forty pages of the 353–408 volume-three transcription span, but the browser received only application error 31000. HTTP 200 therefore does not constitute page-data availability.'
  },
  'source_emitted_image_capture':{
    'successful_image_response_count':16,
    'signed_ref_image_response_count':15,
    'placeholder_response_count':1,
    'unique_ref_page_ids':ref_page_ids,
    'target_page_id_present_in_ref_images':False,
    'full_page_image_for_target_observed':False,
    'inference_from_ref_url_pattern_authorized':False,
    'note':'The signed images are source-emitted /ref/ resources. Their page IDs are preserved only as passive observations. The target page ID was absent, so no URL pattern may be extrapolated to construct a target resource.'
  },
  'rule_adjudication':{
    'hpa_zdate_006_status':'MISSING_FROM_PRODUCT',
    'exact_shiqie_target_glyph_observed':False,
    'hai_glyph_witness_increment':0,
    'upper_night_zi_to_hai_branch_directly_attested':False,
    'runtime_winner_selected':False,
    'candidate_collapsed':False,
    'algorithm_reopen':False,
    'next_gate':'Obtain a directly source-emitted/readable target-page image for pageId 7640563520069697576, or another independently bound physical witness. Do not replay anti-bot requests, derive target image URLs from neighboring /ref/ resources, or treat HTTP 200 with errorCode 31000 as page data.'
  },
  'access_policy':'ORDINARY PUBLIC SHIDIAN BROWSER NAVIGATION + PASSIVE DOM/NETWORK OBSERVATION ONLY; CAPTURE ONLY REQUESTS/RESPONSES THE PAGE ITSELF EMITS; NO MANUAL API REPLAY; NO SIGNATURE/TOKEN RECONSTRUCTION; NO PAGE/OBJECT ID ENUMERATION; NO URL-PATTERN DERIVATION; NO LOGIN; NO COOKIE/TOKEN INJECTION; NO ACCESS BYPASS'
}
Path(evidence_path).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc='''# Fusion Chart Historical Provenance Audit R1 — Batch 12BL

## 《筮篋理數日抄》卷三：識典普通瀏覽器自行發出的 read API 與影像請求之存取邊界

Status: **PUBLIC CHAPTER HTTP 200 / SSR STILL BINDS TARGET TRANSCRIPTION + TARGET PAGE ID / ORDINARY ANONYMOUS BROWSER SOURCE-EMITS `paragraphs/v3` + `pages/v3` / ALL CAPTURED READ-API RESPONSES HTTP 200 BUT APPLICATION BODY IS ONLY `errorCode=31000` / SOURCE-EMITTED `pages/v3` REQUEST RANGE COVERS THE TARGET REGION BUT RETURNS NO PAGE DATA / 15 SIGNED `/ref/` IMAGE RESPONSES OBSERVED, TARGET PAGE ID ABSENT / NO TARGET FULL-PAGE IMAGE / NO URL-PATTERN INFERENCE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BK closed the National Archives route at a clean boundary: the exact official fascicle-three object and 69-canvas manifest are known, but the 56-page Shidian transcription cannot be ordinally mapped onto those canvases, and the first-party image surface is HTTP 403 from the GitHub runner.

Batch 12BL therefore tests a different, narrower route: **what does an ordinary anonymous browser receive when it opens the public Shidian volume-three chapter and lets the page make its own requests?**

The probe is passive. It does not manually replay the observed APIs, regenerate anti-bot parameters, infer adjacent page URLs, enumerate IDs, inject cookies/tokens, or use a hidden/private interface.

## 2. The public SSR still binds the target locus exactly

Ordinary navigation to:

`https://www.shidianguji.com/zh/book/NA06425/chapter/1m44zy4jwa4ab`

returns HTTP 200. The rendered/SSR HTML still contains both:

- target paragraph ID `7649191097545588762`
- target page ID `7640563520069697576`
- transcription `巳上是上四亥。`

The same target page continues with `巳上是下四刻。` and the following section `論子時隔界` states `上四刻屬本日管，下四刻屬第二日管`.

This remains a strong **locator/transcription layer**, not physical-glyph authority.

## 3. What the ordinary browser itself requested

Without manual replay, the public page emitted HTTP requests including:

- `book/dynamic-info/get`
- `review/chapter-list/`
- `book/paragraphs/v3/`
- `book/pages/v3/`

The source-emitted `pages/v3` POST payload scoped itself to:

```text
bookId       NA06425
pageIndex    1
pageSize     40
startPageNum 353
endPageNum   409
version      1
```

A page token was present in the browser-generated request, but it is not copied into the durable evidence because it is ephemeral and unnecessary to the historical adjudication.

This is important provenance: the browser itself attempted to obtain the relevant opening page block of volume three. It does **not** authorize us to replay or reconstruct that request.

## 4. HTTP 200 is not page availability here

Four selected read responses were captured exactly as received by the browser. Every one had HTTP 200 and every body was the same 33-byte JSON object:

```json
{"errorCode":31000,"errorMsg":""}
```

The identical body SHA-256 is:

`460a68650881f42750a8226fdd4a5ed610e1b7a200d4a4a95735c0724cd90572`

Therefore:

- `paragraphs/v3` returned no target text or target page record;
- `pages/v3` returned no page list, no target page ID, no `picUrl`, no `thumbUrl` and no target image metadata;
- HTTP status alone must not be misclassified as a successful page-data response.

## 5. Source-emitted signed images do not expose the target page

The same ordinary browser session successfully loaded sixteen image responses. One is the site's no-network placeholder. Fifteen are signed `.../ref/...` image resources emitted by the public page.

Across those fifteen `ref` responses, the observed unique embedded page IDs are:

- `7640563520069746728`
- `7640563520069763112`
- `7640563520069795880`
- `7640563520069812264`
- `7640563520069828648`
- `7640563520069845032`
- `7640563520069861416`
- `7640563520069877800`

The target page ID `7640563520069697576` is absent.

These are `ref` resources, not an observed target full-page image. Their URL structure must **not** be extrapolated backward to manufacture a target-page URL. That would replace evidence with pattern inference.

## 6. Effect on HPA-ZDATE-006

No rule vote changes:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- exact Shiqie target glyph observed: `false`
- Hai glyph/witness increment: `0`
- upper/night Zi → Hai directly attested by this batch: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

The isolated `上四亥` remains a quarantined transcription anomaly candidate. The surrounding mechanics still say `上四刻 / 下四刻`, and Batch 12BI's independently collated physical parallel remains consistent with `刻`, but neither fact licenses silently rewriting the exact Shiqie glyph before that leaf is read.

## 7. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-R1.json`

Hosted evidence:

- ordinary public-browser passive network probe: run `34765718210`, artifact `10320391963`, digest `sha256:1665c297d024f7cf234574a5f38e6594168c7c1ab8c3742eb8546d586364060a`
- source-emitted read-response body capture: run `34765824117`, artifact `10320861185`, digest `sha256:79ba56e995d27d26e7fb83fdf243c46ef3a03c4d43e261def860e30e9c5f29ae`

The second artifact preserves the response bodies and exact browser-emitted request metadata. The durable repository evidence intentionally omits ephemeral anti-bot/signature token values.

## 8. Next gate

Promotion now requires either:

1. a directly source-emitted and readable full-page image bound to target page ID `7640563520069697576`; or
2. an independently bound physical witness resolving the same glyph/rule question.

Until then, do not replay the 31000-producing request, do not derive an image URL from neighboring `ref` resources, and do not convert the transcriptional `亥` into a mechanical Hai-branch rule.
'''
Path(batch_doc).write_text(doc,encoding='utf-8')

reg_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg=json.loads(reg_path.read_text(encoding='utf-8'))
src=next(s for s in reg['sources'] if s.get('source_id')==source_id)
assert src['provider'].startswith('識典古籍')
assert 'batch_12bl' not in src
src['batch_12bl']={
  'ordinary_browser_probe_run_id':34765718210,
  'ordinary_browser_probe_artifact_id':10320391963,
  'source_emitted_read_capture_run_id':34765824117,
  'source_emitted_read_capture_artifact_id':10320861185,
  'pages_request_scope':{'pageIndex':1,'pageSize':40,'startPageNum':353,'endPageNum':409},
  'captured_read_api_application_error_code':31000,
  'target_page_id':target_page_id,
  'target_page_returned_by_read_api':False,
  'source_emitted_ref_image_unique_page_ids':ref_page_ids,
  'target_page_present_in_ref_images':False,
  'target_leaf_exposed':False,
  'hai_glyph_witness_increment':0,
  'research_artifact':evidence_path
}
addition=' Batch 12BL passively captured the ordinary anonymous browser requests that the public chapter itself emits: pages/v3 and paragraphs/v3 are HTTP 200 but return only application errorCode 31000, while 15 successful signed /ref/ images omit the target page ID. No replay or URL-pattern derivation is authorized; the target physical leaf remains unread and Hai vote stays zero.'
if addition.strip() not in src.get('quality_notes',''):
    src['quality_notes']=src.get('quality_notes','').rstrip()+addition
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

matrix_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix=json.loads(matrix_path.read_text(encoding='utf-8'))
row=next(r for r in matrix['rows'] if r.get('rule_id')=='HPA-ZDATE-006')
assert row['audit_status']=='MISSING_FROM_PRODUCT'
assert 'batch_12bl_shiqie_shidian_source_emitted_read_api_boundary' not in row
row['batch_12bl_shiqie_shidian_source_emitted_read_api_boundary']={
  'source_id':source_id,
  'public_chapter_http_status':200,
  'target_page_id':target_page_id,
  'target_transcription':'巳上是上四亥。',
  'ssr_target_locator_present':True,
  'source_emitted_pages_request_scope':{'pageIndex':1,'pageSize':40,'startPageNum':353,'endPageNum':409},
  'captured_read_api_http_status':200,
  'captured_read_api_application_error_code':31000,
  'target_page_record_returned':False,
  'source_emitted_ref_image_count':15,
  'target_page_present_in_ref_images':False,
  'target_full_page_image_observed':False,
  'url_pattern_inference_authorized':False,
  'hai_glyph_witness_increment':0,
  'candidate_status_effect':'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
  'runtime_winner_selected':False,
  'algorithm_reopen_authorized':False,
  'research_artifact':evidence_path
}
later=row.get('later_witnesses',[])
addition2='Ordinary anonymous Shidian navigation source-emits pages/v3 for pageIndex 1, pageSize 40, startPageNum 353, endPageNum 409, but the captured HTTP-200 response body is only application errorCode 31000; 15 source-emitted signed /ref/ images omit target pageId 7640563520069697576. No target glyph or Hai vote is added.'
if isinstance(later,list):
    if addition2 not in later: later.append(addition2)
    row['later_witnesses']=later
else:
    if addition2 not in later: row['later_witnesses']=later.rstrip()+' '+addition2
matrix_path.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

state_path=Path('docs/PROJECT-CURRENT-STATE-R1.json')
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state['schema_version']=='1.70.0'
state['schema_version']='1.71.0'
audit=state['historical_audit']
assert audit['completed_batches'][-1]==prev
audit['completed_batches'].append(batch_id)
audit['latest_batch_doc']=batch_doc
audit.setdefault('current_focus',[]).extend([
  'Batch 12BL passively captures the ordinary anonymous Shidian browser requests for the exact Shiqie volume-three chapter. The page itself emits paragraphs/v3 and pages/v3, and the pages request covers pageIndex 1 / pageSize 40 / startPageNum 353 / endPageNum 409, but every selected HTTP-200 read response contains only application errorCode 31000 and no target page data.',
  'Fifteen source-emitted signed /ref/ image responses were observed, spanning eight non-target page IDs; target pageId 7640563520069697576 is absent. No API replay, token reconstruction, ID enumeration or URL-pattern derivation is authorized. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; exact physical target glyph unread; Hai vote +0; no runtime winner, candidate collapse or algorithm reopen.'
])
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

verifier_path=Path('scripts/verify-project-continuity-state-r1.py')
s=verifier_path.read_text(encoding='utf-8')
old='''    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK.md"'''
new='''    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n    "BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL.md"'''
assert old in s
verifier_path.write_text(s.replace(old,new,1),encoding='utf-8')

print(json.dumps({
  'batch_id':batch_id,
  'batch_doc':batch_doc,
  'evidence_path':evidence_path,
  'source_id':source_id,
  'hpa_zdate_006_status':row['audit_status'],
  'api_application_error_code':31000,
  'target_page_returned_by_api':False,
  'target_page_present_in_ref_images':False,
  'hai_glyph_witness_increment':0,
  'target_leaf_exposed':False,
  'runtime_winner_selected':False,
  'candidate_collapsed':False,
  'algorithm_reopen':False,
  'state_schema_version':state['schema_version'],
},ensure_ascii=False,indent=2))
