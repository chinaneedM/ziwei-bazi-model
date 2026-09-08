#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'docs/PROJECT-CURRENT-STATE-R1.json'
MATRIX=ROOT/'docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json'
MATRIX_MD=ROOT/'docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md'
REGISTRY=ROOT/'docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json'
README=ROOT/'README.md'
VERIFY=ROOT/'scripts/verify-project-continuity-state-r1.py'
BATCH_ID='BATCH-12-ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-T'
BATCH_PATH='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-T.md'
EVIDENCE_PATH='docs/research/ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-R1.json'

state=json.loads(STATE.read_text(encoding='utf-8'))
matrix=json.loads(MATRIX.read_text(encoding='utf-8'))
registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
assert state['schema_version']=='1.30.0', state['schema_version']
ha=state['historical_audit']
assert ha['latest_batch_doc'].endswith('TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S.md')
assert (ha['row_count'],ha['audited_row_count'],ha['current_missing_from_product_row_count'],ha['identified_missing_candidate_family_count'])==(198,166,10,14)
inv=state['invariants']
assert inv['deterministic_fusion_chart_product_r1']=='CLOSED'
assert inv['confirmed_chart_algorithm_defect_count']==0
assert inv['algorithm_reopen_count']==0
assert inv['candidate_collapse_count']==0

row=next(r for r in matrix['rows'] if r.get('rule_id')=='HPA-ZDATE-006')
assert row['audit_status']=='MISSING_FROM_PRODUCT'
assert row['algorithm_reopen_authorized'] is False

# This batch is a provenance bridge/dedup closure, not a new textual witness.
evidence={
  'schema':'ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-R1',
  'schema_version':'1.0.0','batch_id':BATCH_ID,'hpa_rule_id':'HPA-ZDATE-006',
  'status':'BATCH12A_DIRECT_FACSIMILE_AND_NAJ_NAIKAKU_MING_OBJECT_HIGH_CONFIDENCE_PHYSICAL_LINEAGE_CONVERGENCE_LEGACY_REGISTRATION_CROSSWALK_NOT_EXPLICITLY_CLOSED_NO_NEW_TEXTUAL_VOTE',
  'batch12a_direct_facsimile':{
    'source_id':'EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN',
    'acquisition_workflow_run_id':34116332295,'artifact_id':10016416872,
    'pdf_sha256':'32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7',
    'pdf_bytes':36203879,'pdf_page_count':527,
    'page_1_visual_review_no_ocr':{
      'cover_title':'紫微斗數全書 上',
      'legacy_shelf_label_columns':['漢','子六十','一五八五六','全二'],
      'normalized_legacy_class':'漢 / 子60','legacy_registration_number':'15856','physical_total':'全二'
    },
    'page_2_visual_review_no_ocr':{'author_surface':'陳希夷先生著','title':'紫微斗數全書','imprint':'南陽堂較梓'},
    'target_page':{
      'pdf_page_1_based':320,'volume':'卷五','heading':'論人生時要審的確',
      'direct_visual_line':'如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時',
      'glyph_authority':'DIRECT_FACSIMILE_VISUAL_READING_FROM_BATCH12A_MIRROR_NOT_FIRST_PARTY_NAJ_VIEWER'
    }
  },
  'national_archives_japan':{
    'source_id':'EXT-NAJ-ZWDSQS-MING-1078787','provider':'国立公文書館デジタルアーカイブ',
    'file_id':'1078787','file_url':'https://www.digital.archives.go.jp/file/1078787',
    'viewer_url':'https://www.digital.archives.go.jp/img/1078787',
    'first_item_id':'4468520','first_item_url':'https://www.digital.archives.go.jp/item/4468520',
    'official_index_metadata':{
      'title':'新鋟希夷陳先生紫微斗数全書','call_number':'子０６０－０００１','old_owner':'紅葉山文庫',
      'people':['選者:陳搏（宋）','補訂者:潘希尹（明）'],'bibliographic_label':'刊本:明:::','quantity':'2冊','access_class':'公開'
    },
    'official_2019_digitization_list':{'call_number':'子０６０－０００１','title':'新鍥希夷陳先生紫微斗数全書','digitization_target_listed':True},
    'batch12h_prior_binding':{'workflow_run_id':34134081787,'artifact_id':10023248966,'status':'OFFICIAL_ARCHIVE_CATALOG_AND_DIGITAL_OBJECT_IDENTITY_BOUND_TARGET_PAGE_NOT_OBSERVED'},
    'batch12t_runner_recheck':{
      'workflow_run_id':34224240506,'artifact_id':10054995877,
      'artifact_zip_sha256':'d15d25e8cb3838cfb19d33107cf2a4f5799a0cee1ce4c1106020e8c792fd2d6d',
      'known_routes':['/file/1078787','/item/4468520','/img/4468520'],
      'result':'CLOUDFRONT_ERROR_REQUEST_COULD_NOT_BE_SATISFIED','response_bytes_each':919,
      'adjudication':'RUNNER_CDN_ACCESS_BOUNDARY_ONLY_NOT_OBJECT_OR_DIGITIZATION_ABSENCE'
    }
  },
  'formal_facsimile_and_scholarly_controls':{
    'sdu_statement':'《新鋟希夷陳先生紫微斗數全書》七卷，（宋）陳摶撰，（明）潘希尹補。據内閣文庫藏明刊本影印。',
    'ncku_fullbook_row':'書林棲和堂葉梓行、南陽堂較梓；紅葉山文庫；今收於日本國立公文書館',
    'authority':'FORMAL_FACSIMILE_ROUTE_AND_MODERN_SCHOLARLY_GENEALOGY_NOT_TARGET_GLYPH_AUTHORITY'
  },
  'lineage_adjudication':{
    'convergent_fields':['title family','Ming printed status','Nanyangtang imprint','class 子60/子060','two-volume physical total','Naikaku/Red-Leaves/National-Archives lineage'],
    'physical_lineage_relation':'HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE',
    'legacy_registration_15856_to_current_call_number_crosswalk':'NOT_EXPLICITLY_DOCUMENTED_IN_REVIEWED_FIRST_PARTY_CATALOG_SURFACE',
    'exact_same_physical_object_claim_ceiling':'HIGH_CONFIDENCE_PROVENANCE_CONVERGENCE_NOT_FORMAL_OLD_NUMBER_CROSSWALK_CLOSED',
    'batch12a_and_batch12h_count_as_independent_textual_witnesses':False,
    'dedup_rule':'DO_NOT_DOUBLE_COUNT_BATCH12A_MIRROR_AND_NAJ_NAIKAKU_ROUTE_AS_TWO_PHYSICAL_OR_TEXTUAL_WITNESSES',
    'official_naj_target_page_directly_observed':False,
    'batch12a_direct_target_page_remains_valid':True,
    'independent_hai_glyph_witness_count_added':0
  },
  'epistemic_boundaries':{
    'mirror_target_page_as_official_naj_viewer_capture':'FORBIDDEN',
    'legacy_registration_15856_as_explicitly_first_party_crosswalked_to_current_call':'FORBIDDEN_UNTIL_DIRECT_CROSSWALK_OR_OFFICIAL_IMAGE_COMPARISON',
    'same_lineage_as_second_independent_vote':'FORBIDDEN',
    'runner_cloudfront_error_as_no_digitization_proof':'FORBIDDEN'
  },
  'adjudication':{
    'hpa_zdate_006':'MISSING_FROM_PRODUCT','new_chart_rule_candidate_authorized':False,
    'candidate_selection_authorized':False,'confirmed_chart_algorithm_defect_count':0,
    'algorithm_reopen_authorized':False,'candidate_collapse_count':0,'algorithm_effect':'NONE',
    'next_gate':'EXPLICIT_FIRST_PARTY_OLD_NUMBER_CROSSWALK_OR_OFFICIAL_NAJ_TARGET_PAGE; IN_PARALLEL SEEK_GENUINELY_INDEPENDENT_DIRECT_FIVE_XIONG_SHEN_PHYSICAL_WITNESS'
  }
}
(ROOT/EVIDENCE_PATH).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

batch='''# Fusion Chart Historical Provenance Audit R1 — Batch 12T

## Naikaku / National Archives Nanyangtang facsimile physical-lineage bridge

Status: **BATCH 12A DIRECT FACSIMILE ↔ NAIKAKU / NATIONAL ARCHIVES MING FULLBOOK HIGH-CONFIDENCE LINEAGE CONVERGENCE / OLD REGISTRATION CROSSWALK NOT EXPLICITLY CLOSED / DEDUP ONLY / ZERO NEW TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

Batch 12T revisits an unresolved bridge left between Batch 12A and Batch 12H. It does not discover a second late-Zi witness. It improves the provenance of the already-collated Batch 12A facsimile and prevents double counting.

### 1. Batch 12A physical marks, re-read directly without OCR

The controlling Batch 12A PDF remains SHA-256 `32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7`, 527 pages, artifact `10016416872`.

Its first page visibly carries:

- cover title `紫微斗數全書 上`;
- old shelf/registration label columns `漢 / 子六十 / 一五八五六 / 全二`.

The second page visibly carries `陳希夷先生著 / 紫微斗數全書 / 南陽堂較梓`.

The already-reviewed target page remains PDF p.320, 卷五《論人生時要審的確》, where the direct facsimile visibly reads `如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`.

### 2. First-party National Archives object

The National Archives of Japan public index binds `新鋟希夷陳先生紫微斗数全書` to `子０６０－０００１`, former owner `紅葉山文庫`, `刊本:明:::`, quantity `2冊`, with public digital object `file/1078787` and first item `4468520`. Its official 2019 digitization target list independently lists `子060-0001 新鍥希夷陳先生紫微斗数全書`.

Batch 12H had already closed this official archive/digital-object identity, but could not observe the target page.

### 3. Provenance convergence and ceiling

The physical/codicological fields now converge strongly: Ming Fullbook title family, Nanyangtang imprint, `子六十` ↔ `子060` class, two-volume total, and the Naikaku/Red-Leaves/National-Archives holding genealogy also preserved by the formal SDU facsimile route and NCKU edition study.

This supports `HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE` for the Batch 12A mirror.

However, no reviewed first-party catalog surface explicitly states that legacy registration number `漢15856` was migrated to current call `子060-0001`. Therefore Batch 12T does **not** claim a formally closed old-number crosswalk, and it does not rewrite the mirror p.320 image as a first-party National Archives viewer capture.

### 4. Runner access boundary

Recheck run `34224240506` / artifact `10054995877` followed only the already known first-party `/file/1078787`, `/item/4468520`, and `/img/4468520` routes. All three returned a 919-byte CloudFront `ERROR: The request could not be satisfied` page in the GitHub runner. This is a CDN/runner boundary only.

### 5. Dedup and rule effect

```text
BATCH12A_MIRROR_AND_NAJ_ROUTE_INDEPENDENT_WITNESSES=NO
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic product remains CLOSED. The next gate is either an explicit first-party legacy-number crosswalk / official NAJ target-page capture, or a genuinely independent directly readable `五凶神` physical witness.

Machine evidence: `docs/research/ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-R1.json`.
'''
(ROOT/BATCH_PATH).write_text(batch,encoding='utf-8')

# Matrix row: provenance-only fields; no row/count/status change.
row.update({
 'naikaku_nanyangtang_lineage_bridge_artifact':EVIDENCE_PATH,
 'naikaku_national_archives_file_id':'1078787','naikaku_national_archives_current_call_number':'子０６０－０００１',
 'batch12a_legacy_label':'漢 / 子六十 / 一五八五六 / 全二',
 'batch12a_to_naj_physical_lineage_relation':'HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE',
 'legacy_registration_15856_to_current_call_crosswalk':'NOT_EXPLICITLY_DOCUMENTED_IN_REVIEWED_FIRST_PARTY_CATALOG_SURFACE',
 'batch12a_naj_dedup_status':'DO_NOT_DOUBLE_COUNT_AS_TWO_PHYSICAL_OR_TEXTUAL_WITNESSES',
 'naj_official_target_page_status_batch_12t':'NOT_DIRECTLY_OBSERVED_RUNNER_CDN_BLOCKED',
 'independent_hai_glyph_witness_count_added_batch_12t':0
})
MATRIX.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Upgrade existing NAJ registry source; do not create a duplicate source object.
naj=next(s for s in registry['sources'] if s.get('source_id')=='EXT-NAJ-ZWDSQS-MING-1078787')
naj['batch12t_provenance_bridge']={
 'evidence':EVIDENCE_PATH,'batch12a_pdf_sha256':'32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7',
 'batch12a_legacy_label':'漢 / 子六十 / 一五八五六 / 全二',
 'lineage_relation':'HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE',
 'legacy_registration_crosswalk_status':'NOT_EXPLICITLY_FIRST_PARTY_CLOSED',
 'independent_textual_witness_increment':0,'independent_hai_glyph_increment':0,
 'dedup':'DO_NOT_DOUBLE_COUNT_BATCH12A_MIRROR_AND_NAJ_ROUTE'
}
REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# State.
state['schema_version']='1.31.0'
assert BATCH_ID not in ha['completed_batches']
ha['completed_batches'].append(BATCH_ID)
ha['latest_batch_doc']=BATCH_PATH
ha['current_focus'].extend([
 'Batch 12T bridges the already-collated Batch 12A 527-page Nanyangtang mirror to the Naikaku/National Archives Ming Fullbook lineage at high confidence from direct physical marks, without creating a second textual witness.',
 'Batch 12A PDF p1 directly shows old label 漢 / 子六十 / 一五八五六 / 全二 and p2 shows 陳希夷先生著 / 紫微斗數全書 / 南陽堂較梓; its p320 late-Zi target reading remains the direct facsimile glyph authority.',
 'National Archives first-party object file 1078787 / item 4468520 is 新鋟希夷陳先生紫微斗数全書 / 子060-0001 / 紅葉山文庫 / 明刊 / 2冊, and the official 2019 digitization list names the same call/title.',
 'Legacy registration 15856 -> current 子060-0001 is not explicitly crosswalked on the reviewed first-party catalog surfaces; therefore physical identity is HIGH_CONFIDENCE lineage convergence, not a formally closed old-number migration claim.',
 'Batch 12A mirror and NAJ/Naikaku route must not be double-counted; Batch 12T adds zero independent target-text/Hai-glyph votes and HPA-ZDATE-006 remains MISSING_FROM_PRODUCT.',
 'Run 34224240506 / artifact 10054995877 rechecked only known first-party NAJ routes and encountered the same 919-byte CloudFront request-unsatisfied boundary; this is not no-digitization evidence.'
])
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Human-readable ledgers.
md=MATRIX_MD.read_text(encoding='utf-8')
md += '\n\n### Batch 12T — Naikaku/National Archives Nanyangtang facsimile lineage bridge\n\n- Re-review of Batch 12A PDF SHA-256 `32ca49bb...e7` directly reads the p1 legacy label `漢 / 子六十 / 一五八五六 / 全二` and p2 `南陽堂較梓`.\n- NAJ first-party file `1078787` / item `4468520` remains `子060-0001`, Red-Leaves former holding, Ming print, 2 volumes; official 2019 digitization list confirms the call/title.\n- The evidence supports high-confidence same Naikaku/National-Archives Ming Fullbook lineage, while the explicit `15856 -> 子060-0001` catalog-number crosswalk remains unobserved.\n- Dedup: Batch 12A mirror and the NAJ route are not two independent witnesses. Hai-glyph increment = 0; HPA-ZDATE-006 and 198/166/10/14 are unchanged.\n'
MATRIX_MD.write_text(md,encoding='utf-8')
readme=README.read_text(encoding='utf-8')
readme += '\n\n- **Batch 12T (Naikaku/National Archives Nanyangtang provenance bridge):** direct re-review of the Batch 12A 527-page facsimile reads the old cover label `漢 / 子六十 / 一五八五六 / 全二` and `南陽堂較梓`, strongly converging with NAJ `子060-0001` / `2冊` / Ming / Red-Leaves lineage. The explicit legacy-registration `15856 -> 子060-0001` crosswalk remains unobserved, so this is a high-confidence provenance convergence and dedup closure, not a new independent textual vote or an official-NAJ target-page capture. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT and all algorithm invariants are unchanged.\n'
README.write_text(readme,encoding='utf-8')

# Continuity verifier update.
v=VERIFY.read_text(encoding='utf-8')
anchor='ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE = ROOT / "docs/research/ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-R1.json"\n'
assert anchor in v
v=v.replace(anchor,anchor+'ZIWEI_NAIKAKU_LINEAGE_BATCH = ROOT / "'+BATCH_PATH+'"\nZIWEI_NAIKAKU_LINEAGE_EVIDENCE = ROOT / "'+EVIDENCE_PATH+'"\n',1)
v=v.replace('    "BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S",\n]\nLATEST_BATCH_ID', '    "BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S",\n    "'+BATCH_ID+'",\n]\nLATEST_BATCH_ID',1)
v=v.replace('LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S.md"', 'LATEST_BATCH_DOC = "'+BATCH_PATH+'"',1)
v=v.replace('ZIWEI_TOYO_MEDIA_REPOSITORY_BATCH, ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE):', 'ZIWEI_TOYO_MEDIA_REPOSITORY_BATCH, ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE, ZIWEI_NAIKAKU_LINEAGE_BATCH, ZIWEI_NAIKAKU_LINEAGE_EVIDENCE):',1)
v=v.replace('    ziwei_toyo_media_repository_evidence = json.loads(ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE.read_text(encoding="utf-8"))\n', '    ziwei_toyo_media_repository_evidence = json.loads(ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE.read_text(encoding="utf-8"))\n    ziwei_naikaku_lineage_evidence = json.loads(ZIWEI_NAIKAKU_LINEAGE_EVIDENCE.read_text(encoding="utf-8"))\n',1)
check_anchor='    if invariants.get("confirmed_chart_algorithm_defect_count") != audit_summary.get("confirmed_chart_algorithm_defect_count"):\n'
assert check_anchor in v
checks='''    # Batch 12T upgrades/deduplicates the Batch 12A facsimile provenance without adding a new witness.\n    if ziwei_naikaku_lineage_evidence.get("batch_id") != "'''+BATCH_ID+'''":\n        fail("Batch 12T machine evidence batch identity mismatch")\n    bridge = ziwei_naikaku_lineage_evidence.get("lineage_adjudication", {})\n    if bridge.get("physical_lineage_relation") != "HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE":\n        fail("Batch 12T physical-lineage convergence regressed")\n    if bridge.get("legacy_registration_15856_to_current_call_number_crosswalk") != "NOT_EXPLICITLY_DOCUMENTED_IN_REVIEWED_FIRST_PARTY_CATALOG_SURFACE":\n        fail("Batch 12T old-registration crosswalk uncertainty regressed")\n    if bridge.get("batch12a_and_batch12h_count_as_independent_textual_witnesses") is not False or bridge.get("independent_hai_glyph_witness_count_added") != 0:\n        fail("Batch 12T dedup / zero-vote boundary regressed")\n    b12a = ziwei_naikaku_lineage_evidence.get("batch12a_direct_facsimile", {})\n    if b12a.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7":\n        fail("Batch 12T Batch12A PDF identity regressed")\n    if b12a.get("page_1_visual_review_no_ocr", {}).get("legacy_registration_number") != "15856":\n        fail("Batch 12T legacy registration visual binding regressed")\n    naj12t = ziwei_naikaku_lineage_evidence.get("national_archives_japan", {})\n    if naj12t.get("file_id") != "1078787" or naj12t.get("official_index_metadata", {}).get("call_number") != "子０６０－０００１":\n        fail("Batch 12T NAJ object binding regressed")\n    if naj12t.get("official_index_metadata", {}).get("quantity") != "2冊":\n        fail("Batch 12T NAJ two-volume binding regressed")\n    row12t = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)\n    if not row12t or row12t.get("batch12a_naj_dedup_status") != "DO_NOT_DOUBLE_COUNT_AS_TWO_PHYSICAL_OR_TEXTUAL_WITNESSES":\n        fail("Batch 12T matrix dedup boundary regressed")\n    naj_source12t = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-NAJ-ZWDSQS-MING-1078787"), None)\n    if not naj_source12t or naj_source12t.get("batch12t_provenance_bridge", {}).get("independent_hai_glyph_increment") != 0:\n        fail("Batch 12T NAJ registry provenance bridge regressed")\n\n'''
v=v.replace(check_anchor,checks+check_anchor,1)
v=v.replace('        "not proof of no digitization ever",\n', '        "not proof of no digitization ever",\n        "Batch 12T",\n        "漢 / 子六十 / 一五八五六 / 全二",\n        "1078787",\n        "10054995877",\n        "HIGH_CONFIDENCE",\n        "not explicitly crosswalked",\n',1)
VERIFY.write_text(v,encoding='utf-8')

print(json.dumps({'batch':BATCH_ID,'state_schema':state['schema_version'],'rows':ha['row_count'],'audited':ha['audited_row_count'],'missing':ha['current_missing_from_product_row_count'],'families':ha['identified_missing_candidate_family_count'],'reopen':inv['algorithm_reopen_count']},ensure_ascii=False))
