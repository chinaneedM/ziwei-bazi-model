#!/usr/bin/env python3
from pathlib import Path
import json

batch_id='BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ'
batch_doc='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ.md'
evidence_path='docs/research/ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-R1.json'
source_id='EXT-ZIWEI-SHIQIE-YFSHUHUA-864433-PUBLIC-SAMPLES'
prev='BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI'

samples=[
  {
    'index':1,
    'url':'https://www.yfshuhua.com/wp-content/uploads/2025/02/00724-筮箧理数日抄_0124142020_1.jpg',
    'sha256':'ba38df0d322d263b4d6e4bb93b732e4cf70a1a7a0d08902985a35169198b9973',
    'size':94217,
    'secure_visual_scope':'FIRST-VOLUME OUTER COVER; title strip reads 理數日抄; image visibly carries 国立公文書館 / National Archives of Japan watermark; an 内閣文庫 collection label visibly contains identifier 15857 and set/volume notation 12 (1).',
    'target_leaf':False,
  },
  {
    'index':2,
    'url':'https://www.yfshuhua.com/wp-content/uploads/2025/02/00724-筮箧理数日抄_0124142024_4.jpg',
    'sha256':'9fff89a958f8f0fadfb0ef2a13b68dd667540602e7c976914ce140815d31d0cf',
    'size':144719,
    'secure_visual_scope':'PREFACE OPENING; left leaf heading visibly reads 筮篋理數日抄序; National Archives of Japan watermark visible.',
    'target_leaf':False,
  },
  {
    'index':3,
    'url':'https://www.yfshuhua.com/wp-content/uploads/2025/02/00724-筮箧理数日抄_0124142025_5.jpg',
    'sha256':'471a4e536a651dd642c18acded35247223f2cb76e9564ba44b5eb4ab934eff0b',
    'size':147555,
    'secure_visual_scope':'VOLUME-ONE OPENING; left leaf heading visibly reads 筮篋理數日抄卷之一; National Archives of Japan watermark visible.',
    'target_leaf':False,
  },
]

evidence={
  'schema':'ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-R1',
  'batch_id':batch_id,
  'question':'Does the publicly accessible YFShuhua listing expose an exact physical target leaf for the Jiajing-44 Shiqie night-Zi passage, or at least materially bind the listed set to National Archives of Japan / Naikaku Bunko physical imagery without crossing its paid-download boundary?',
  'secondary_public_listing':{
    'url':'https://www.yfshuhua.com/864433.html',
    'http_status':200,
    'body_len':72758,
    'html_sha256':'e14e6d8e4a1a9cc6607080f53f111cf150842e1b1b9a06e4fc7bb3a446c1e8e8',
    'title_occurrence_count':46,
    'metadata_scope':{
      'title':'筮箧理数日抄 / 筮篋理数日抄',
      'author':'一壶天俱道人（明）',
      'edition':'刊本（序刊）, 明嘉靖, 明嘉靖44年',
      'holding':'日本内阁文库',
      'former_collection':'红叶山文库',
      'set_count':'12冊',
      'listed_total_pages':1111,
      'listed_file_size':'1095.5MB',
      'copyright_label':'公开'
    },
    'authority_limit':'SECONDARY LISTING METADATA; NOT HISTORICAL TEXTUAL AUTHORITY; NOT A SUBSTITUTE FOR FIRST-PARTY CATALOG OR TARGET LEAF',
    'public_pdf_url_emitted':False,
    'literal_national_archives_object_url_emitted':False,
    'paid_download_area_present':True,
    'paid_or_member_download_accessed':False
  },
  'public_sample_images':samples,
  'visual_adjudication':{
    'public_sample_count':3,
    'national_archives_watermark_visible_on_samples':True,
    'naikaku_bunko_label_visible_on_cover_sample':True,
    'visible_cover_identifier':'15857',
    'visible_set_volume_notation':'12 (1)',
    'sample_two_preface_heading':'筮篋理數日抄序',
    'sample_three_volume_heading':'筮篋理數日抄卷之一',
    'volume_three_target_leaf_exposed':False,
    'night_zi_target_text_exposed':False,
    'exact_shiqie_upper_four_token_glyph_observed':False,
    'physical_copy_route_binding_strengthened':True,
    'independent_material_witness_increment':0,
    'reason_for_zero_increment':'The samples materially bind the secondary listing to National Archives/Naikaku Bunko imagery of the already-tracked Shiqie set; they do not establish a new independent copy and do not expose the target leaf.'
  },
  'hosted_research_runs':[
    {
      'run_id':34761086299,
      'job_id':103733927496,
      'artifact_id':10318857087,
      'artifact_digest':'sha256:b9bc70b32242198ef950d7383f4c5c9f783c097b80f3e3c6ccf7e09cfbe688e3',
      'role':'PUBLIC_HTML_AND_LITERAL_RESOURCE_CONTRACT_DISCOVERY'
    },
    {
      'run_id':34761220843,
      'job_id':103734284779,
      'artifact_id':10318454681,
      'artifact_digest':'sha256:ac53e375a0698056cb9f11e16047c551ba5799f6c74f8fa780f8fffd1c69591d',
      'role':'THREE_LITERAL_PUBLIC_SAMPLE_IMAGE_ACQUISITION'
    }
  ],
  'rule_adjudication':{
    'hpa_zdate_006_status':'MISSING_FROM_PRODUCT',
    'hai_glyph_witness_increment':0,
    'upper_night_zi_to_hai_branch_directly_attested':False,
    'runtime_winner_selected':False,
    'candidate_collapsed':False,
    'algorithm_reopen':False,
    'next_gate':'Acquire the exact volume-three physical leaf containing 論子時隔界 / the 上四亥 transcription locus, or an independent early physical source explicitly mapping upper/night Zi to Hai branch.'
  },
  'access_policy':'PUBLIC HTML AND THREE LITERAL PUBLIC SAMPLE IMAGE URLS ONLY; URL PERCENT-ENCODING USED ONLY FOR TRANSPORT; NO LOGIN; NO PAYMENT; NO MEMBER AJAX; NO PAID DOWNLOAD TARGET; NO PDF/OBJECT-ID GUESSING; NO ACCESS BYPASS'
}
Path(evidence_path).write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc='''# Fusion Chart Historical Provenance Audit R1 — Batch 12BJ

## 《筮篋理數日抄》YFShuhua 公開樣圖 × 日本國立公文書館影像路線核驗

Status: **PUBLIC SECONDARY LISTING + THREE LITERAL PUBLIC SAMPLE IMAGES / SAMPLES VISIBLY CARRY NATIONAL ARCHIVES OF JAPAN WATERMARK / COVER SHOWS 内閣文庫 LABEL + 15857 + 12(1) / PREFACE AND VOLUME-ONE OPENING PHYSICALLY VISIBLE / NO VOLUME-THREE TARGET LEAF / NO PUBLIC PDF OR LITERAL FIRST-PARTY OBJECT URL / PAID DOWNLOAD BOUNDARY NOT CROSSED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batches 12BH–12BI established two separate facts that must remain separate:

1. the Shidian transcription token `上四亥` is unsafe as branch-rule evidence and is now strongly corroborated as a likely transcription anomaly;
2. the exact Jiajing-44 《筮篋理數日抄》 physical target leaf has still not been observed.

Batch 12BJ tests one newly discovered secondary public route only to determine whether it exposes the exact leaf or materially binds the listed set to a physical National Archives/Naikaku Bunko image lineage.

## 2. Public listing boundary

The public page `https://www.yfshuhua.com/864433.html` returned HTTP 200. Its visible metadata describes a 12-volume Jiajing-44 set held by the Japanese Cabinet Library / Naikaku Bunko and formerly in the Momijiyama collection. The page reports 1111 pages and a 1095.5MB downloadable set.

This metadata is **secondary-site metadata only**. It is not used as historical textual authority.

Crucially, the public HTML exposes no literal public PDF URL and no literal National Archives object URL. Its download area is member/payment mediated. No paid or member download mechanism was called.

## 3. Three literal public sample images

The same public HTML emits exactly three title-specific JPEG sample URLs. Those literal URLs were fetched without authentication after ordinary percent-encoding of their Unicode paths.

### Sample 1 — outer cover

Direct visual review shows:

- cover title strip: `理數日抄`;
- visible `国立公文書館 / National Archives of Japan` image watermark;
- visible `内閣文庫` collection label;
- visible numeric identifier `15857`;
- visible set/volume notation `12 (1)`.

### Sample 2 — preface

The left leaf physically shows the heading:

> 筮篋理數日抄序

The National Archives of Japan watermark is again visible.

### Sample 3 — volume one

The left leaf physically shows:

> 筮篋理數日抄卷之一

Again the National Archives of Japan watermark is visible.

These three images materially bind the secondary listing to a physical National Archives/Naikaku Bunko image lineage of the same Shiqie set already under study.

## 4. What the samples do not establish

None of the three public images enters volume three. None contains `論子時隔界`, `上四亥`, `上四刻`, or the target night-Zi passage.

Therefore they do **not** authorize any judgment about the exact target glyph in the Jiajing-44 Shiqie leaf.

They also do not constitute a new independent material witness count: this is a route/copy binding for the already tracked Japanese Cabinet Library set, not a newly independent edition/copy.

## 5. Access-control result

The reviewed route ends at a clear boundary:

```text
public listing HTML                         accessible
three literal title-specific sample JPEGs accessible
public PDF URL                             not emitted
literal first-party National Archives URL not emitted
member/payment download                    present but not accessed
volume-three target leaf                   not exposed
```

No login, payment, member AJAX, hidden endpoint, sequential filename guessing, PDF guessing, or private object-ID inference was attempted.

## 6. Effect on HPA-ZDATE-006

No mechanical evidence increment occurs:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- Hai-branch vote increment: `0`
- target Shiqie glyph observed: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

This batch strengthens physical provenance/access-route control only.

## 7. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-R1.json`

Hosted evidence:

- HTML probe: run `34761086299`, job `103733927496`, artifact `10318857087`
- public sample images: run `34761220843`, job `103734284779`, artifact `10318454681`

## 8. Next gate

Do not spend additional weight on cover/preface samples. Priority remains a directly readable volume-three target leaf or another early physical source that explicitly maps upper/night Zi to the Hai earthly branch.
'''
Path(batch_doc).write_text(doc,encoding='utf-8')

reg_path=Path('docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json')
reg=json.loads(reg_path.read_text(encoding='utf-8'))
assert not any(s.get('source_id')==source_id for s in reg['sources'])
reg['sources'].append({
  'source_id':source_id,
  'title':'《筮篋理數日抄》YFShuhua 864433 公開樣圖路線',
  'historical_period':'SECONDARY_DIGITAL_ACCESS_ROUTE_TO_HISTORICAL_COPY',
  'provider':'YFShuhua public listing; sample images visibly reproduce National Archives of Japan imagery',
  'url':'https://www.yfshuhua.com/864433.html',
  'source_role':'ACCESS_ROUTE_AND_PHYSICAL_SAMPLE_MIRROR_NOT_HISTORICAL_TEXTUAL_AUTHORITY',
  'quality_notes':'Public HTML exposes three title-specific sample JPEGs only. Direct visual review shows National Archives of Japan watermark, 内閣文庫 cover label with visible 15857 and 12(1), preface heading 筮篋理數日抄序, and volume-one heading 筮篋理數日抄卷之一. No volume-three target leaf or public PDF/first-party object URL is exposed. Paid/member download was not accessed.',
  'batch_12bj':{
    'public_html_sha256':evidence['secondary_public_listing']['html_sha256'],
    'sample_count':3,
    'sample_sha256':[s['sha256'] for s in samples],
    'national_archives_watermark_visible':True,
    'naikaku_bunko_label_visible':True,
    'visible_identifier':'15857',
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
row['batch_12bj_shiqie_yfshuhua_naj_public_samples']={
  'source_id':source_id,
  'route_scope':'SECONDARY PUBLIC LISTING + THREE LITERAL PUBLIC SAMPLE JPEGS WITH NATIONAL ARCHIVES OF JAPAN WATERMARK',
  'physical_scope':'COVER + PREFACE + VOLUME-ONE OPENING ONLY; NO VOLUME-THREE TARGET LEAF',
  'visible_copy_markers':['内閣文庫','15857','12 (1)','筮篋理數日抄序','筮篋理數日抄卷之一'],
  'target_text_increment':0,
  'hai_glyph_witness_increment':0,
  'independent_material_witness_increment':0,
  'candidate_status_effect':'NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT',
  'runtime_winner_selected':False,
  'algorithm_reopen_authorized':False,
  'research_artifact':evidence_path
}
later=row.get('later_witnesses',[])
addition='Secondary public YFShuhua route exposes three National Archives of Japan-watermarked physical samples of the already-tracked Shiqie set (cover/preface/volume-one opening; visible 内閣文庫 15857 and 12(1)), but no volume-three target leaf, public PDF, or Hai-branch rule evidence.'
if isinstance(later,list):
    if addition not in later: later.append(addition)
    row['later_witnesses']=later
else:
    if addition not in later: row['later_witnesses']=later.rstrip()+' '+addition
matrix_path.write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

state_path=Path('docs/PROJECT-CURRENT-STATE-R1.json')
state=json.loads(state_path.read_text(encoding='utf-8'))
assert state['schema_version']=='1.68.0'
state['schema_version']='1.69.0'
audit=state['historical_audit']
assert audit['completed_batches'][-1]==prev
audit['completed_batches'].append(batch_id)
audit['latest_batch_doc']=batch_doc
audit.setdefault('current_focus',[]).extend([
  'Batch 12BJ binds the public YFShuhua Shiqie listing to three National Archives of Japan-watermarked physical sample images: cover with 内閣文庫 label / visible 15857 / 12(1), preface heading 筮篋理數日抄序, and volume-one heading 筮篋理數日抄卷之一.',
  'The route exposes no volume-three target leaf, public PDF, or literal first-party National Archives object URL; its member/payment download boundary was not crossed. No new independent copy or Hai-rule vote is added; HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen.'
])
state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

verifier_path=Path('scripts/verify-project-continuity-state-r1.py')
s=verifier_path.read_text(encoding='utf-8')
old='''    "BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH",\n    "BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI.md"'''
new='''    "BATCH-12-ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-BH",\n    "BATCH-12-ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-BI",\n    "BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SHIQIE-YFSHUHUA-NAJ-PUBLIC-SAMPLE-ROUTE-BJ.md"'''
assert old in s
verifier_path.write_text(s.replace(old,new,1),encoding='utf-8')

print(json.dumps({
  'batch_id':batch_id,
  'batch_doc':batch_doc,
  'evidence_path':evidence_path,
  'source_id':source_id,
  'hpa_zdate_006_status':row['audit_status'],
  'hai_glyph_witness_increment':0,
  'target_leaf_exposed':False,
  'runtime_winner_selected':False,
  'candidate_collapsed':False,
  'algorithm_reopen':False,
  'state_schema_version':state['schema_version'],
},ensure_ascii=False,indent=2))
