#!/usr/bin/env python3
from pathlib import Path
import json

batch_id='BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK'
batch_doc='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK.md'
evidence_path='docs/research/ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-R1.json'
source_id='EXT-ZIWEI-SHIQIE-JNA-JPSEARCH-IIIF-FASCICLE3-ACCESS-BOUNDARY'
prev='BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ'

evidence={
  'schema':'ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-R1',
  'batch_id':batch_id,
  'question':'Can the public Shidian volume-three transcription be deterministically aligned to the exact National Archives of Japan fascicle-three physical canvas so that the isolated 上四亥 token can be adjudicated from a first-party image without guessing or bypassing access controls?',
  'japan_search_reference':{
    'root_item_id':'najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ',
    'fascicle3_item_id':'najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003',
    'documented_public_item_api_run_id':34762934050,
    'artifact_id':10319273767,
    'artifact_digest':'sha256:a3c2e3b3f30455f4de316a9b4381ee5a65062e88eb5922357affb67243805b69',
    'role':'EXACT PUBLIC RECORD RESOLUTION; ITEM IDS WERE RETURNED BY JAPAN SEARCH AND NOT DERIVED OR ENUMERATED'
  },
  'official_national_archives_fascicle3':{
    'item_url':'https://www.digital.archives.go.jp/item/4756821',
    'manifest_url':'https://www.digital.archives.go.jp/api/iiif/4756821/manifest.json',
    'manifest_http_status':200,
    'manifest_content_type':'application/json',
    'manifest_body_len':63365,
    'manifest_sha256':'e9b2af8117d8f45922cd8e8656ef0ab7165e727db5c81c59b3d805ab135ba48e',
    'label':'筮篋理数日抄３',
    'reference_code':'子０６０－０００２-0003',
    'canvas_count':69,
    'attribution':'National Archives of JAPAN',
    'manifest_run_id':34763008839,
    'manifest_artifact_id':10319722109,
    'manifest_artifact_digest':'sha256:a689024e38ce78b1d0bdb9751d430acf4541567f72845bcfdeafb627bbc3559a',
    'authority_scope':'FIRST-PARTY CATALOG/DIGITAL-OBJECT STRUCTURE AND CANVAS ORDER; NOT A TARGET-GLYPH READING UNTIL THE TARGET CANVAS IS DIRECTLY IDENTIFIED AND READ'
  },
  'shidian_public_ssr':{
    'url':'https://www.shidianguji.com/zh/book/NA06425/chapter/1m44zy4jwa4ab',
    'http_status':200,
    'body_len':651684,
    'html_sha256':'a9c7b52d9d3180e103e8808ca6e6bfe79ebdce90c9d3fbbee08c79200e61f3ff',
    'chapter_id':'1m44zy4jwa4ab',
    'chapter_label':'卷三',
    'start_page_num':353,
    'end_page_num':408,
    'inclusive_transcription_page_count':56,
    'pagepass_unique_count':56,
    'parsed_paragraph_count':316,
    'start_end_unique_page_count':54,
    'target_paragraph_id':'7649191097545588762',
    'target_page_id':'7640563520069697576',
    'target_visible_page_ordinal_1_based':4,
    'target_transcription':'巳上是上四亥。',
    'nearby_mechanical_rule':'上四刻屬本日管，下四刻屬第二日管',
    'page_order_run_id':34763494286,
    'page_order_artifact_id':10319518306,
    'page_order_artifact_digest':'sha256:e0d50950e22af0f2b3fbf5047fb018a2a3349492ee899b46616791a74265df87',
    'authority_scope':'PUBLIC TRANSCRIPTION/LOCATOR LAYER ONLY; NOT PHYSICAL GLYPH AUTHORITY'
  },
  'alignment_adjudication':{
    'shidian_transcription_pages':56,
    'official_jna_canvases':69,
    'count_difference':13,
    'counts_match':False,
    'ordinal_mapping_authorized':False,
    'target_mapped_to_official_canvas':False,
    'reason':'The public transcription defines a complete 56-page volume-three span (353–408 inclusive), while the exact official fascicle-three manifest contains 69 canvases. The 13-canvas representation gap prevents a page-4-to-canvas-4 or fixed-offset inference without an independent alignment control.'
  },
  'official_image_access_tests':{
    'page1_literal_resource_status':403,
    'page1_service_info_status':403,
    'page1_standard_iiif_transform_status':403,
    'contract_probe_run_id':34763132512,
    'contract_probe_artifact_id':10319198130,
    'contract_probe_artifact_digest':'sha256:a429cee15f76c35cc461113f2c965292f2d76cd6f6db4820eaab3f5159ef7c48',
    'note':'All URLs were literal manifest resources or standard IIIF Image API transformations of the manifest-declared service ID; no object-id guessing was used.'
  },
  'ordinary_browser_access_test':{
    'item_navigation_status':403,
    'item_final_url':'https://www.digital.archives.go.jp/item/4756821',
    'page_title':'ERROR: The request could not be satisfied',
    'literal_viewer_candidates':[],
    'successful_image_response_count':0,
    'browser_probe_run_id':34765354700,
    'browser_probe_artifact_id':10320310873,
    'browser_probe_artifact_digest':'sha256:05d2c739204706ef09b0d591671608f1e87eded95abd21efec53f22b7e4c5ca2',
    'note':'Normal headless Chromium navigation from the exact public item URL remained blocked in the GitHub runner. No cookie/token injection, hidden endpoint, or bypass technique was attempted.'
  },
  'japan_search_target_text_probe':{
    'queries':['論子時隔界','上四亥','選時寶鏡局','日百刻配十二時'],
    'exact_target_text_hits':0,
    'run_id':34763331089,
    'artifact_id':10319842374,
    'artifact_digest':'sha256:97c3f6f1595e592e6d844c2129d150f711368f34f92baf10d323c5ed291fb36e',
    'authority_scope':'NEGATIVE CONTROL FOR PAGE-LEVEL PUBLIC SEARCH ONLY; NOT EVIDENCE THAT THE PHYSICAL TEXT IS ABSENT'
  },
  'rule_adjudication':{
    'hpa_zdate_006_status':'MISSING_FROM_PRODUCT',
    'exact_shiqie_target_glyph_observed':False,
    'hai_glyph_witness_increment':0,
    'upper_night_zi_to_hai_branch_directly_attested':False,
    'runtime_winner_selected':False,
    'candidate_collapsed':False,
    'algorithm_reopen':False,
    'next_gate':'Obtain a directly readable physical volume-three target leaf from the National Archives copy through an ordinary public route outside the blocked runner, or obtain an independent early physical witness explicitly mapping upper/night Zi to the Hai earthly branch.'
  },
  'access_policy':'PUBLIC JAPAN SEARCH API + EXACT FIRST-PARTY JNA MANIFEST + PUBLIC SHIDIAN SSR + ORDINARY FIRST-PARTY BROWSER NAVIGATION ONLY; NO LOGIN; NO COOKIE/TOKEN INJECTION; NO PRIVATE API; NO OBJECT-ID/CANVAS-ID GUESSING; NO ADJACENT-ID ENUMERATION; NO ACCESS BYPASS; NO ORDINAL PAGE MAPPING WHEN COUNTS DO NOT CLOSE'
}
Path(evidence_path).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc='''# Fusion Chart Historical Provenance Audit R1 — Batch 12BK

## 《筮篋理數日抄》卷三：Japan Search → 國立公文書館 IIIF → 識典頁序對齊與存取邊界

Status: **EXACT JAPAN SEARCH FASCICLE-3 RECORD RESOLVED / EXACT NATIONAL ARCHIVES IIIF MANIFEST HTTP 200 / OFFICIAL FASCICLE-3 HAS 69 CANVASES / SHIDIAN PUBLIC VOLUME-3 TRANSCRIPTION IS A COMPLETE 56-PAGE SPAN (353–408) / TARGET TRANSCRIPTION PAGE LOCATED BUT NOT PHYSICALLY MAPPED / 56 != 69, SO ORDINAL MAPPING IS FORBIDDEN / MANIFEST IMAGE RESOURCE + SERVICE + ORDINARY CHROMIUM ITEM ROUTE ALL BLOCKED FROM GITHUB RUNNER / NO TARGET GLYPH OBSERVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BJ established that the public YFShuhua route really reproduces the already tracked National Archives / Naikaku Bunko Shiqie set, but exposes only cover, preface and volume-one samples. Batch 12BK therefore asks a narrower question: can public machine-readable records align the volume-three transcription locus to an exact official physical canvas without guessing?

The answer is **not yet**. The route is materially stronger, but the physical target glyph remains unresolved.

## 2. Exact first-party fascicle-three object

A documented Japan Search public item query returned the exact volume-three record ID `najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003`. Following that returned record—not an inferred adjacent identifier—resolved the National Archives object whose public item URL is:

`https://www.digital.archives.go.jp/item/4756821`

The exact first-party IIIF manifest is:

`https://www.digital.archives.go.jp/api/iiif/4756821/manifest.json`

It returned HTTP 200 and identifies `筮篋理数日抄３`, reference code `子０６０－０００２-0003`, with **69 canvases**. The manifest SHA-256 is `e9b2af8117d8f45922cd8e8656ef0ab7165e727db5c81c59b3d805ab135ba48e`.

This closes the digital-object identity and official canvas order. It does **not** by itself identify the target canvas.

## 3. Public Shidian volume-three page order

The public Shidian SSR page for volume three returned HTTP 200. Its structured chapter record states:

- chapter: `卷三`
- `startPageNum = 353`
- `endPageNumWithoutSubchapter = 408`

That interval is exactly **56 pages inclusive**, and the independent `pagePass` sequence also contains 56 unique page IDs. This is important: the difference from the official 69-canvas manifest is not merely a parser dropping thirteen pages.

The target paragraph is publicly locatable as:

- paragraph ID `7649191097545588762`
- page ID `7640563520069697576`
- fourth visible transcription page in the derived chapter order
- transcription: `巳上是上四亥。`

Nearby explanatory text still states `上四刻屬本日管，下四刻屬第二日管`.

Shidian remains a **transcription/locator witness only** for this question. The isolated `亥` cannot be promoted to physical-glyph authority.

## 4. Why page 4 cannot be called official canvas 4

The two complete representations do not have the same cardinality:

```text
Shidian volume-three transcription pages   56
National Archives official IIIF canvases   69
difference                                 13
```

Therefore no fixed ordinal mapping is authorized. In particular, the target being the fourth Shidian page does **not** authorize treating official canvas 4 as the target. Nor is a fixed +13/-13 offset justified.

Any such mapping would be object-ID/page-order inference rather than evidence.

## 5. First-party image access boundary

The exact official manifest exposes literal resource/service IDs. A controlled probe of the first manifest-listed page produced:

- literal resource: HTTP 403
- service `info.json`: HTTP 403
- standard IIIF image transformation from the declared service ID: HTTP 403

A separate ordinary Chromium test then navigated to the exact public item URL. In the GitHub runner it also returned HTTP 403 with `ERROR: The request could not be satisfied`, emitted no usable viewer href, and produced zero successful image responses.

This closes a material ambiguity: the runner restriction is not merely an `urllib` header quirk. It persists under normal browser navigation in that environment.

No login, cookie/token injection, hidden endpoint discovery, adjacent-ID enumeration or access-bypass method was attempted.

## 6. Japan Search text-search control

Documented public Japan Search queries for `論子時隔界`, `上四亥`, `選時寶鏡局`, and `日百刻配十二時` returned no exact page-level target-text hits. This is only a public-search-surface control; it is **not** evidence that the physical page or wording is absent.

## 7. Effect on HPA-ZDATE-006

No rule vote changes:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- exact Shiqie target glyph observed: `false`
- Hai-branch glyph/witness increment: `0`
- upper/night Zi → Hai directly attested by this batch: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

The current safest reading remains: `上四亥` is a quarantined transcription anomaly candidate until its physical leaf is directly read. Batch 12BI's independent CADAL physical parallel (`係上四刻 / 係下四刻`) continues to strengthen that anomaly diagnosis, but cannot substitute for the exact Shiqie glyph.

## 8. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-R1.json`

Hosted evidence chain:

- Japan Search exact item reference: run `34762934050`, artifact `10319273767`
- exact official fascicle-three manifest: run `34763008839`, artifact `10319722109`
- official page-1 image-contract probe: run `34763132512`, artifact `10319198130`
- Japan Search target-text control: run `34763331089`, artifact `10319842374`
- Shidian chapter page-order probe: run `34763494286`, artifact `10319518306`
- ordinary Chromium first-party item-route probe: run `34765354700`, artifact `10320310873`

## 9. Next gate

The next admissible promotion requires either:

1. a directly readable physical volume-three target leaf of the National Archives copy obtained through an ordinary public route outside the blocked GitHub-runner surface; or
2. an independent early physical witness explicitly assigning upper/night Zi to the Hai earthly branch.

Until then, do not infer a canvas from ordinal position and do not convert `上四亥` into a runtime rule.
'''
Path(batch_doc).write_text(doc,encoding='utf-8')

reg_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg=json.loads(reg_path.read_text(encoding='utf-8'))
assert not any(s.get('source_id')==source_id for s in reg['sources'])
reg['sources'].append({
  'source_id':source_id,
  'title':'《筮篋理數日抄》卷三 Japan Search / 國立公文書館 IIIF 精確數字物件與存取邊界',
  'historical_period':'MING_JIAJING_44_COPY_DIGITIZED_BY_NATIONAL_ARCHIVES_OF_JAPAN; MODERN_FIRST_PARTY_DIGITAL_OBJECT_CONTRACT',
  'provider':'Japan Search + National Archives of Japan Digital Archive',
  'url':'https://www.digital.archives.go.jp/api/iiif/4756821/manifest.json',
  'source_role':'FIRST_PARTY_CATALOG_AND_DIGITAL_OBJECT_STRUCTURE; ACCESS_BOUNDARY CONTROL; NOT TARGET_GLYPH AUTHORITY UNTIL TARGET CANVAS IS DIRECTLY READ',
  'quality_notes':'Documented Japan Search item resolution binds the exact fascicle-three record to National Archives item 4756821. Its official IIIF manifest is HTTP 200 and contains 69 canvases. Public Shidian volume-three SSR independently defines a complete 56-page transcription span, so ordinal mapping is forbidden. Manifest image resources and ordinary Chromium item navigation are HTTP 403 in the GitHub runner. No bypass was attempted and the target physical glyph remains unread.',
  'batch_12bk':{
    'japan_search_item_id':'najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003',
    'official_item_id':4756821,
    'official_manifest_sha256':'e9b2af8117d8f45922cd8e8656ef0ab7165e727db5c81c59b3d805ab135ba48e',
    'official_canvas_count':69,
    'shidian_transcription_page_count':56,
    'page_count_difference':13,
    'ordinal_mapping_authorized':False,
    'target_leaf_exposed':False,
    'explicit_hai_branch_reassignment':False,
    'hai_glyph_witness_increment':0,
    'research_artifact':evidence_path
  }
})
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

matrix_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json')
matrix=json.loads(matrix_path.read_text(encoding='utf-8'))
row=next(r for r in matrix['rows'] if r.get('rule_id')=='HPA-ZDATE-006')
assert row['audit_status']=='MISSING_FROM_PRODUCT'
row['batch_12bk_shiqie_jna_fascicle3_page_order_and_access_boundary']={
  'source_id':source_id,
  'official_fascicle3_canvas_count':69,
  'shidian_complete_transcription_page_count':56,
  'page_count_difference':13,
  'target_shidian_page_id':'7640563520069697576',
  'target_shidian_page_ordinal_1_based':4,
  'target_transcription':'巳上是上四亥。',
  'target_official_canvas_resolved':False,
  'ordinal_mapping_authorized':False,
  'official_image_contract_status':'HTTP_403_IN_GITHUB_RUNNER',
  'ordinary_browser_item_status':'HTTP_403_IN_GITHUB_RUNNER',
  'target_text_increment':0,
  'hai_glyph_witness_increment':0,
  'candidate_status_effect':'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
  'runtime_winner_selected':False,
  'algorithm_reopen_authorized':False,
  'research_artifact':evidence_path
}
later=row.get('later_witnesses',[])
addition='Exact Japan Search/National Archives fascicle-three resolution now provides a 69-canvas first-party IIIF manifest, while the complete public Shidian volume-three transcription spans 56 pages (353–408) and places the isolated 上四亥 token on its fourth transcription page. Because 56 != 69 and official image/browser routes are HTTP 403 in the GitHub runner, no ordinal canvas mapping or physical glyph judgment is authorized; Hai vote remains zero.'
if isinstance(later,list):
    if addition not in later: later.append(addition)
    row['later_witnesses']=later
else:
    if addition not in later: row['later_witnesses']=later.rstrip()+' '+addition
matrix_path.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

state_path=Path('docs/PROJECT-CURRENT-STATE-R1.json')
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state['schema_version']=='1.69.0'
state['schema_version']='1.70.0'
audit=state['historical_audit']
assert audit['completed_batches'][-1]==prev
audit['completed_batches'].append(batch_id)
audit['latest_batch_doc']=batch_doc
audit.setdefault('current_focus',[]).extend([
  'Batch 12BK resolves the exact Shiqie fascicle-three Japan Search record to National Archives item 4756821 and its HTTP-200 first-party IIIF manifest with 69 canvases; the public Shidian volume-three SSR independently defines a complete 56-page span (353–408) and locates the isolated 上四亥 transcription on page ID 7640563520069697576.',
  'Because the complete representations are 56 transcription pages versus 69 official canvases, ordinal target-to-canvas mapping is forbidden. Literal manifest image/service requests and ordinary Chromium navigation to the exact official item remain HTTP 403 in the GitHub runner, so no physical target glyph or Hai vote is added; HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen.'
])
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

verifier_path=Path('scripts/verify-project-continuity-state-r1.py')
s=verifier_path.read_text(encoding='utf-8')
old='''    "BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ.md"'''
new='''    "BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ",\n    "BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-BK.md"'''
assert old in s
verifier_path.write_text(s.replace(old,new,1),encoding='utf-8')

print(json.dumps({
  'batch_id':batch_id,
  'batch_doc':batch_doc,
  'evidence_path':evidence_path,
  'source_id':source_id,
  'hpa_zdate_006_status':row['audit_status'],
  'official_canvas_count':69,
  'shidian_transcription_page_count':56,
  'ordinal_mapping_authorized':False,
  'hai_glyph_witness_increment':0,
  'target_leaf_exposed':False,
  'runtime_winner_selected':False,
  'candidate_collapsed':False,
  'algorithm_reopen':False,
  'state_schema_version':state['schema_version'],
},ensure_ascii=False,indent=2))
