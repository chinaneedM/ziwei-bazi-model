#!/usr/bin/env python3
from pathlib import Path
import json

batch_id='BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM'
batch_doc='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM.md'
evidence_path='docs/research/ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-R1.json'
source_id='EXT-ZIWEI-SHIQIE-JNA-JPSEARCH-IIIF-FASCICLE3-ACCESS-BOUNDARY'
prev='BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL'

viewer_url='https://www.digital.archives.go.jp/img/4756821'
thumbnail_url='https://www.digital.archives.go.jp/thumb/4756821/C103347219500.jpg'

evidence={
  'schema':'ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-R1',
  'batch_id':batch_id,
  'question':'Does the exact first-party National Archives viewer URI literally emitted by the exact Japan Search fascicle-three record expose a readable viewer/download/image route in an ordinary anonymous Chromium session, without constructing any URL or bypassing access controls?',
  'japan_search_record':{
    'record_id':'najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003',
    'official_item_id':4756821,
    'literal_viewer_field':'najda-root.rdf:Description.owl:sameAs-u',
    'literal_viewer_url':viewer_url,
    'literal_thumbnail_url':thumbnail_url,
    'resolution_run_id':34762934050,
    'resolution_artifact_id':10319273767,
    'resolution_artifact_digest':'sha256:a3c2e3b3f30455f4de316a9b4381ee5a65062e88eb5922357affb67243805b69',
    'route_provenance':'EXACT VALUES RETURNED BY THE PUBLIC JAPAN SEARCH RECORD; NOT DERIVED FROM ITEM-ID PATTERNS'
  },
  'ordinary_browser_probe':{
    'workflow_run_id':34766246768,
    'artifact_id':10320761950,
    'artifact_digest':'sha256:0093749d86190c8701e815f3158fefc4da6b9568cb9f77f2e2650e28c8b814dc',
    'viewer_navigation_status':403,
    'viewer_final_url':viewer_url,
    'viewer_title':'ERROR: The request could not be satisfied',
    'viewer_cloudfront_error':True,
    'viewer_anchor_count':0,
    'viewer_control_count':0,
    'viewer_image_element_count':0,
    'download_ui_observed':False,
    'successful_image_response_count':0,
    'thumbnail_navigation_status':403,
    'thumbnail_final_url':thumbnail_url,
    'thumbnail_cloudfront_error':True,
    'route_guessing_used':False,
    'login_used':False,
    'cookie_or_token_injection_used':False,
    'access_bypass_used':False
  },
  'adjudication':{
    'exact_first_party_viewer_uri_identity_closed':True,
    'previous_item_url_403_explained_by_wrong_route':False,
    'github_runner_first_party_content_surface_blocked':True,
    'target_canvas_identified':False,
    'target_glyph_observed':False,
    'download_resource_observed':False,
    'hai_glyph_witness_increment':0,
    'hpa_zdate_006_status':'MISSING_FROM_PRODUCT',
    'runtime_winner_selected':False,
    'candidate_collapsed':False,
    'algorithm_reopen':False,
    'next_gate':'Obtain a directly readable target physical leaf through another ordinary public first-party or independently bound facsimile route, or collate an independent early physical homolog. Do not infer viewer/download paths beyond source-emitted URIs.'
  },
  'access_policy':'EXACT PUBLIC JAPAN SEARCH RECORD + EXACT SOURCE-EMITTED FIRST-PARTY VIEWER/THUMBNAIL URIS + ORDINARY ANONYMOUS CHROMIUM ONLY; NO URL CONSTRUCTION; NO ADJACENT-ID ENUMERATION; NO LOGIN; NO COOKIE/TOKEN INJECTION; NO ACCESS BYPASS'
}
Path(evidence_path).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

Path(batch_doc).write_text('''# Fusion Chart Historical Provenance Audit R1 — Batch 12BM

## 《筮篋理數日抄》卷三：Japan Search 原樣 viewer URI × 國立公文書館第一方內容面存取邊界

Status: **EXACT JAPAN SEARCH FASCICLE-3 RECORD LITERALLY EMITS FIRST-PARTY VIEWER URI / VIEWER URI IS NOT GUESSED / ORDINARY CHROMIUM VIEWER HTTP 403 CLOUDFRONT / LITERAL THUMBNAIL HTTP 403 / NO VIEWER CONTROLS / NO DOWNLOAD UI / NO SUCCESSFUL IMAGE RESPONSE / WRONG-ROUTE HYPOTHESIS CLOSED / NO TARGET GLYPH OBSERVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BK established the exact National Archives fascicle-three object and its 69-canvas IIIF manifest, but ordinary navigation to the catalog item and manifest-declared image resources was blocked from the GitHub runner. That left one residual ambiguity: perhaps the content viewer had a different first-party URI that had simply not yet been resolved.

Batch 12BM closes that ambiguity without URL construction.

## 2. Exact viewer URI from Japan Search

The exact public Japan Search fascicle-three record `najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003` literally emits the National Archives viewer URI in its `owl:sameAs` field:

`https://www.digital.archives.go.jp/img/4756821`

The same record also literally emits a first-party thumbnail URI:

`https://www.digital.archives.go.jp/thumb/4756821/C103347219500.jpg`

These values were returned by the record itself. Neither path was reconstructed from the numeric item ID.

## 3. Ordinary-browser result

A normal anonymous Chromium session navigated directly to the literal viewer URI. The response was HTTP 403 and the rendered title was `ERROR: The request could not be satisfied`, with a CloudFront error surface.

No usable anchors, viewer controls, download UI, image elements or successful image responses were exposed.

The literal thumbnail URI was tested independently and also returned HTTP 403 with the same first-party/CloudFront access boundary.

No login, cookie/token injection, alternate endpoint discovery, sequential object enumeration or bypass technique was used.

## 4. What this closes

The evidence now separates object identity from execution-environment accessibility:

```text
exact fascicle-three record identity       closed
exact National Archives item identity      closed
exact official IIIF manifest identity      closed
exact first-party viewer URI               closed
exact source-emitted thumbnail URI         closed
viewer/content reachability from runner    blocked (403)
target physical glyph                      not observed
```

Therefore the earlier first-party 403 cannot reasonably be attributed to our having guessed the wrong viewer route. The route is exact; the content surface remains blocked in this execution environment.

## 5. Effect on HPA-ZDATE-006

No textual or mechanical evidence increment occurs:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- exact Shiqie target glyph observed: `false`
- Hai glyph/witness increment: `0`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

This batch is an access/provenance closure only.

## 6. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-R1.json`

Hosted evidence:

- Japan Search exact record resolution: run `34762934050`, artifact `10319273767`
- literal first-party viewer/thumbnail Chromium probe: run `34766246768`, artifact `10320761950`, digest `sha256:0093749d86190c8701e815f3158fefc4da6b9568cb9f77f2e2650e28c8b814dc`

## 7. Next gate

Do not spend further research cycles inventing National Archives viewer/download URLs from item `4756821`. The next admissible advance is a directly readable target leaf through another ordinary public first-party or independently bound facsimile route, or an independent early physical homolog that can be collated at the glyph level.
''',encoding='utf-8')

reg_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg=json.loads(reg_path.read_text(encoding='utf-8'))
src=next(s for s in reg['sources'] if s.get('source_id')==source_id)
src['batch_12bm']={
  'literal_japan_search_viewer_url':viewer_url,
  'literal_japan_search_thumbnail_url':thumbnail_url,
  'viewer_http_status':403,
  'thumbnail_http_status':403,
  'cloudfront_blocked':True,
  'download_ui_observed':False,
  'successful_image_response_count':0,
  'target_glyph_observed':False,
  'hai_glyph_witness_increment':0,
  'research_artifact':evidence_path
}
extra=' Batch 12BM closes the remaining viewer-route ambiguity: the exact Japan Search fascicle record itself emits /img/4756821 and the exact thumbnail URI, yet ordinary Chromium receives CloudFront HTTP 403 for both; the first-party target glyph remains unread.'
if extra.strip() not in src.get('quality_notes',''):
    src['quality_notes']=src.get('quality_notes','').rstrip()+extra
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

matrix_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix=json.loads(matrix_path.read_text(encoding='utf-8'))
row=next(r for r in matrix['rows'] if r.get('rule_id')=='HPA-ZDATE-006')
assert row['audit_status']=='MISSING_FROM_PRODUCT'
row['batch_12bm_shiqie_jna_literal_viewer_access_boundary']={
  'source_id':source_id,
  'viewer_uri_provenance':'LITERAL OWL:SAMEAS VALUE FROM EXACT JAPAN SEARCH FASCICLE-THREE RECORD; NOT DERIVED',
  'viewer_url':viewer_url,
  'viewer_http_status':403,
  'thumbnail_http_status':403,
  'wrong_viewer_route_hypothesis_closed':True,
  'target_glyph_observed':False,
  'hai_glyph_witness_increment':0,
  'candidate_status_effect':'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
  'runtime_winner_selected':False,
  'algorithm_reopen_authorized':False,
  'research_artifact':evidence_path
}
matrix_path.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

state_path=Path('docs/PROJECT-CURRENT-STATE-R1.json')
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state['schema_version']=='1.71.0',state['schema_version']
state['schema_version']='1.72.0'
audit=state['historical_audit']
assert audit['completed_batches'][-1]==prev,audit['completed_batches'][-1]
audit['completed_batches'].append(batch_id)
audit['latest_batch_doc']=batch_doc
audit.setdefault('current_focus',[]).extend([
  'Batch 12BM closes the National Archives viewer-route ambiguity: the exact Japan Search fascicle-three record literally emits first-party viewer /img/4756821 and its thumbnail URI, but ordinary Chromium receives CloudFront HTTP 403 for both in the GitHub runner.',
  'This is an access/provenance closure only. The Shiqie physical target glyph remains unread; HPA-ZDATE-006 stays MISSING_FROM_PRODUCT with Hai vote +0, no runtime winner, no candidate collapse and no algorithm reopen.'
])
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

verifier_path=Path('scripts/verify-project-continuity-state-r1.py')
s=verifier_path.read_text(encoding='utf-8')
old='''    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n    "BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL.md"'''
new='''    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n    "BATCH-12-ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-BL",\n    "BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-BM.md"'''
assert old in s
verifier_path.write_text(s.replace(old,new,1),encoding='utf-8')

print(json.dumps({
  'batch_id':batch_id,
  'state_schema_version':state['schema_version'],
  'viewer_status':403,
  'thumbnail_status':403,
  'target_glyph_observed':False,
  'hai_glyph_witness_increment':0,
  'hpa_zdate_006_status':row['audit_status'],
  'runtime_winner_selected':False,
  'candidate_collapsed':False,
  'algorithm_reopen':False
},ensure_ascii=False,indent=2))
