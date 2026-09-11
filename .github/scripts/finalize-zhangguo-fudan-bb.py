#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH_ID = 'BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB'
BATCH_DOC = 'docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB.md'
EVIDENCE_PATH = 'docs/research/ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-FIRST-PARTY-HOLDING-RECONCILIATION-R1.json'
TITLE_QUERY_PATH = ROOT / 'docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-TITLE-QUERY-R1.json'
DETAIL_PATH = ROOT / 'docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-ITEM-DETAIL-R1.json'
CONTRACT_PATH = ROOT / 'docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-GUJI-CONTRACT-PROBE-R1.json'
GENERAL_PATH = ROOT / 'docs/research/ZIWEI-ZHANGGUO-FUDAN-GENERAL-CATALOG-CONTRACT-PROBE-R1.json'
JIANGSU_PATH = ROOT / 'docs/research/ZIWEI-ZHANGGUO-FUDAN-JIANGSU-1594-PUBLIC-CATALOG-PROBE-R1.json'

for p in (TITLE_QUERY_PATH, DETAIL_PATH, CONTRACT_PATH, GENERAL_PATH, JIANGSU_PATH):
    if not p.is_file():
        raise SystemExit(f'missing Batch 12BB precursor evidence: {p}')

title = json.loads(TITLE_QUERY_PATH.read_text(encoding='utf-8'))
detail = json.loads(DETAIL_PATH.read_text(encoding='utf-8'))
packed_title = json.dumps(title, ensure_ascii=False, sort_keys=True)
packed_detail = json.dumps(detail, ensure_ascii=False, sort_keys=True)

for marker in (
    '新編評註通玄先生張果星宗大全', '明萬曆間', 'FDU01001127121',
    'fudan_ancient_001127121', '34053686', 'rb2314', '10冊(1函)', '刻本', '善本', '綫裝',
):
    if marker not in packed_title:
        raise SystemExit(f'Fudan title-query positive-control marker missing: {marker}')
for marker in ('AB0613271-80', '光华楼古籍书库', '古籍馆藏', '在馆', '34053686', 'rb2314'):
    if marker not in packed_detail:
        raise SystemExit(f'Fudan holdings positive-control marker missing: {marker}')

adjud = detail.get('adjudication', {})
if adjud.get('detail_http_200') is not True or adjud.get('holdings_http_200') is not True:
    raise SystemExit('Fudan detail/holdings HTTP controls are not both 200')
if adjud.get('first_party_catalog_item_bound') is not True or adjud.get('first_party_holding_item_bound') is not True:
    raise SystemExit('Fudan first-party catalog/holding binding not closed')
if adjud.get('exact_1594_or_wanli_22_marker_observed') is not False:
    raise SystemExit('Exact-1594 firewall changed; manual adjudication required')
if adjud.get('tang_qian_marker_observed') is not False:
    raise SystemExit('Tang-Qian firewall changed; manual adjudication required')
if detail.get('holding_total') != 1:
    raise SystemExit('Fudan holding_total is not exactly one')

evidence = {
    'schema': 'ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-FIRST-PARTY-HOLDING-RECONCILIATION-R1',
    'batch_id': BATCH_ID,
    'question': 'Does Fudan first-party catalog evidence establish an independent Ming-Wanli physical holding of the target Zhangguo title, and does it establish the secondary-locator claim of an exact Wanli-22 / 1594 Tang-Qian edition?',
    'authority_chain': {
        'ancient_book_portal': 'https://guji.fudan.edu.cn/',
        'portal_source_emitted_label': '綫裝古籍書目',
        'portal_source_emitted_general_catalog_entry': 'https://opac.fudan.edu.cn/#/gjRedirect',
        'opac_result_route': '/resultGj',
        'public_api_base': 'https://fdulspgw.fudan.edu.cn/urdh',
        'title_search_contract': 'POST /open-api/opac/search/advanced; resourceType=10; field=resource_ztm; matchType=contains',
        'detail_contract': 'GET /open-api/opac/search/smjlh/{resource_smjlh}',
        'holdings_contract': 'GET https://fdulspgw.fudan.edu.cn/alsp/open-api/opac/v2/holdings?catalogueId={resource_smjlh}',
        'contract_origin': 'SOURCE_EMITTED_BY_FUDAN_PUBLIC_FRONTEND',
    },
    'target_catalog_record': {
        'title': '新編評註通玄先生張果星宗大全',
        'extent': '10卷',
        'physical_extent': '10冊(1函)',
        'responsibility': ['(唐)張果撰', '(明)陸位輯'],
        'catalog_date': '不详#明萬曆間',
        'edition_type': '刻本',
        'rare_book_class': '善本',
        'binding': '綫裝',
        'call_number': 'rb2314',
        'resource_book_no': 'FDU01001127121',
        'doc_id': 'fudan_ancient_001127121',
        'resource_smjlh': '34053686',
        'catalog_item_identity': 'DIRECT_FIRST_PARTY_OPAC_MATCH',
    },
    'physical_holding': {
        'holding_total': 1,
        'call_number': 'rb2314',
        'barcode': 'AB0613271-80',
        'permanent_location_name': '复旦大学',
        'sub_location_name': '光华楼古籍书库',
        'individual_library_name': '古籍馆藏',
        'item_status_name': '在馆',
        'catalogue_id': '34053686',
        'binding_status': 'DIRECT_FIRST_PARTY_HOLDINGS_API_ITEM',
    },
    'edition_adjudication': {
        'independent_fudan_ming_wanli_material_holding_control_established': True,
        'exact_wanli_22_or_1594_observed_in_first_party_record': False,
        'tang_qian_observed_in_first_party_record': False,
        'secondary_locator_exact_1594_tang_qian_claim_promoted': False,
        'exact_1594_material_witness_increment': 0,
        'ming_wanli_material_holding_control_increment': 1,
        'target_leaf_obtained': False,
        'independent_target_text_witness_increment': 0,
        'independent_hai_glyph_witness_increment': 0,
        'whole_holding_negative_authorized': False,
        'reason': 'Fudan first-party OPAC and holdings bind one physical target-title item dated only 明萬曆間. Neither the item detail nor holdings expose 萬曆二十二/1594 or 唐謙, and no target leaf was obtained.',
    },
    'jiangsu_public_route_boundary': {
        'http_and_https_timed_out_from_reviewed_runner': True,
        'no_holding_inference_authorized': False,
        'no_digitization_inference_authorized': False,
        'witness_increment': 0,
    },
    'project_consequence': {
        'audit_row': 'HPA-ZDATE-006',
        'audit_status': 'MISSING_FROM_PRODUCT',
        'new_candidate_family': False,
        'runtime_winner_selected': False,
        'candidate_collapsed': False,
        'algorithm_reopen': False,
        'provenance_defect_count_change': False,
        'matrix_row_count_change': False,
    },
    'source_artifacts': [
        str(TITLE_QUERY_PATH.relative_to(ROOT)),
        str(DETAIL_PATH.relative_to(ROOT)),
        str(CONTRACT_PATH.relative_to(ROOT)),
        str(GENERAL_PATH.relative_to(ROOT)),
        str(JIANGSU_PATH.relative_to(ROOT)),
        'docs/research/ZIWEI-ZHANGGUO-FUDAN-1594-PUBLIC-SEARCH-CONTRACT-PROBE-R1.json',
        'docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-DETAIL-CONTRACT-PROBE-R1.json',
    ],
}
(ROOT / EVIDENCE_PATH).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

batch_doc = """# Fusion Chart Historical Provenance Audit R1 — Batch 12BB

## 《張果星宗大全》复旦大学明万历间实体馆藏一手绑定与“1594 唐谦刻本”证据边界校勘

Status: **FUDAN FIRST-PARTY GENERAL-ANCIENT-BOOK-CATALOG ROUTE CLOSED / TARGET CATALOG RECORD DIRECTLY BOUND / ONE PHYSICAL HOLDING DIRECTLY BOUND / INDEPENDENT MING-WANLI MATERIAL HOLDING CONTROL +1 / EXACT WANLI-22 OR 1594 NOT ATTESTED / TANG-QIAN NOT ATTESTED / SECONDARY 1594 LOCATOR NOT PROMOTED / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

After Batch 12BA separated the SOAS/NCL 1593 metadata from the 1797 Morrison physical reprint, a secondary rare-book locator pointed to another copy of 《新編評註通玄先生張果星宗大全》 at Fudan and described a Wanli-22 / 1594 Tang-Qian edition. BB tests that claim only through **Fudan first-party public systems** before allowing any early-witness vote.

The batch deliberately distinguishes four questions:

```text
DOES_FUDAN_HAVE_A_TARGET_TITLE_PHYSICAL_ITEM?
IS_THE_ITEM_MING_WANLI?
IS_IT_EXACTLY_WANLI_22 / 1594?
HAS_THE_TARGET_LATE-ZI LEAF BEEN DIRECTLY COLLATION-BOUND?
```

A positive answer to an earlier question does not imply a positive answer to a later one.

## 2. First-party route discovery: 古籍 portal -> general ancient-book OPAC

Fudan's public ancient-book portal source-emits the route:

```text
館藏書目
綫裝古籍書目 -> https://opac.fudan.edu.cn/#/gjRedirect
```

An initially visible `/guji/gujisearch/mingGuji` endpoint belongs to the **明人文集书目** specialty database, not the general line-bound ancient-book holding catalog. BB therefore rejects that specialty endpoint as authority for a general Fudan holding negative or positive and follows the portal's own `綫裝古籍書目` route instead.

## 3. Public OPAC contract recovered from the Fudan frontend

The OPAC's own public frontend exposes:

```text
API base=https://fdulspgw.fudan.edu.cn/urdh
resource type: 古籍 = 10
title field: 题名关键词 = resource_ztm
match type=contains
POST /open-api/opac/search/advanced
GET  /open-api/opac/search/smjlh/{id}
GET  https://fdulspgw.fudan.edu.cn/alsp/open-api/opac/v2/holdings?catalogueId={id}
```

The search-result route passes the record's `resource_smjlh` into `/gjInfo/`; the detail frontend decodes that value and calls the public item-detail and holdings APIs. No hidden object identifier was guessed.

## 4. Direct target-title catalog hit

The first-party ancient-book OPAC directly returns:

```text
title=新編評註通玄先生張果星宗大全
responsibility=(唐)張果撰; (明)陸位輯
extent=10卷
physical extent=10冊(1函)
date=不详#明萬曆間
edition=刻本
rare-book class=善本
binding=綫裝
call number=rb2314
resource book no=FDU01001127121
docId=fudan_ancient_001127121
resource_smjlh=34053686
```

This closes target catalog-item identity at the Fudan first-party OPAC level.

## 5. Direct physical-holding binding

Using source-emitted `resource_smjlh=34053686`, the first-party holdings API returns exactly one holding:

```text
holding_total=1
call number=rb2314
barcode=AB0613271-80
permanent location=复旦大学
sub-location=光华楼古籍书库
individual library=古籍馆藏
item status=在馆
catalogueId=34053686
```

Therefore BB authorizes:

```text
FUDAN_TARGET_TITLE_PHYSICAL_HOLDING=ESTABLISHED
FUDAN_MING_WANLI_MATERIAL_HOLDING_CONTROL_INCREMENT=1
```

This is institutionally independent of the SOAS/Morrison lineage audited in BA.

## 6. Critical firewall: “明萬曆間” is not “萬曆二十二年 / 1594”

The Fudan first-party catalog and holdings expose `明萬曆間`, but do **not** expose `萬曆二十二`, `万历二十二`, `1594`, `唐謙`, or `唐谦`.

Accordingly:

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=0
SECONDARY_LOCATOR_1594_TANG_QIAN_CLAIM_PROMOTED=false
```

The secondary locator remains useful for discovery, but its exact-year/imprint statement cannot substitute for first-party edition evidence.

## 7. No target-leaf vote

The item record proves a material holding; it does not expose a reviewed target leaf for the late-Zi passage. No target-leaf image/full-text object was directly collated.

```text
TARGET_LEAF_OBTAINED=false
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

No whole-holding textual negative is authorized.

## 8. Jiangsu/Nanjing route boundary

A parallel first-party Jiangsu/Nanjing ancient-book-platform probe timed out over both reviewed HTTP and HTTPS routes from the GitHub runner. BB records this only as an execution-environment/public-route boundary; reachability failure is not bibliographic absence.

## 9. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

Fudan materially strengthens the independent Ming-Wanli copy landscape, but it does not supply the missing mechanical bridge `upper/night Zi -> Hai branch` and does not justify changing deterministic runtime behavior.

## 10. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

BB is a provenance/access-only adjudication and changes no Matrix row count.

## 11. Durable artifacts

```text
docs/research/ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-FIRST-PARTY-HOLDING-RECONCILIATION-R1.json
docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-TITLE-QUERY-R1.json
docs/research/ZIWEI-ZHANGGUO-FUDAN-OPAC-ITEM-DETAIL-R1.json
```

## 12. Next gate

1. Seek a Fudan first-party digitized-image or reproduction route for `rb2314 / FDU01001127121 / catalogueId 34053686`; if a target leaf becomes available, collate it directly without OCR.
2. Continue seeking a genuinely independent first-party copy whose **physical edition field itself** binds Wanli-22 / 1594 (or 1593) and then bind the target leaf.
3. Keep the Shandong/Weifang and Jiangsu/Nanjing leads locator-scoped until first-party object bytes or item metadata become reachable.
4. Do not collapse HPA-ZDATE-006 until direct rule evidence supplies the missing upper/night-Zi -> Hai mapping.
"""
(ROOT / BATCH_DOC).write_text(batch_doc, encoding='utf-8')

registry_path = ROOT / 'docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json'
registry = json.loads(registry_path.read_text(encoding='utf-8'))
registry['access_date'] = '2026-09-12'
source_id = 'EXT-ZIWEI-ZHANGGUO-FUDAN-RB2314-MING-WANLI'
sources = [s for s in registry.setdefault('sources', []) if s.get('source_id') != source_id]
sources.append({
    'source_id': source_id,
    'title': '《新編評註通玄先生張果星宗大全》复旦大学古籍馆藏 rb2314',
    'provider': '复旦大学图书馆古籍特藏 / Fudan OPAC and holdings API',
    'url': 'https://opac.fudan.edu.cn/#/gjRedirect',
    'source_role': 'FIRST_PARTY_MING_WANLI_PHYSICAL_HOLDING_CONTROL_EXACT_1594_NOT_PROVEN',
    'catalog_date': '明萬曆間',
    'resource_book_no': 'FDU01001127121',
    'doc_id': 'fudan_ancient_001127121',
    'catalogue_id': '34053686',
    'call_number': 'rb2314',
    'barcode': 'AB0613271-80',
    'holding_location': '复旦大学 / 光华楼古籍书库',
    'item_status': '在馆',
    'physical_extent': '10冊(1函)',
    'edition_type': '刻本',
    'rare_book_class': '善本',
    'binding': '綫裝',
    'first_party_physical_holding_bound': True,
    'exact_1594_or_wanli_22_proven': False,
    'tang_qian_proven': False,
    'target_leaf_obtained': False,
    'ming_wanli_material_holding_control_increment': 1,
    'independent_exact_1594_material_witness_increment': 0,
    'independent_target_text_witness_increment': 0,
    'independent_hai_glyph_witness_increment': 0,
    'batch_id': BATCH_ID,
    'research_artifact': EVIDENCE_PATH,
    'quality_notes': 'Fudan first-party ancient-book portal -> OPAC -> target result -> detail -> holdings chain binds one in-library target-title physical item dated only 明萬曆間. No first-party 萬曆二十二/1594 or 唐謙 marker and no target leaf were observed; secondary exact-1594 locator claims are not promoted.'
})
registry['sources'] = sources
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

state_path = ROOT / 'docs/PROJECT-CURRENT-STATE-R1.json'
state = json.loads(state_path.read_text(encoding='utf-8'))
if state.get('schema_version') != '1.60.0':
    raise SystemExit(f'unexpected state schema version: {state.get("schema_version")}')
state['schema_version'] = '1.61.0'
state['updated_at'] = '2026-09-12'

def find_holder(x):
    if isinstance(x, dict):
        if x.get('latest_batch_doc', '').endswith('PROVENANCE-RECONCILIATION-BA.md'):
            return x
        for v in x.values():
            got = find_holder(v)
            if got is not None:
                return got
    elif isinstance(x, list):
        for v in x:
            got = find_holder(v)
            if got is not None:
                return got
    return None

holder = find_holder(state)
if holder is None:
    raise SystemExit('could not locate current historical-audit state holder')
batch_list_key = None
for k, v in holder.items():
    if isinstance(v, list) and v and v[-1] == 'BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA':
        batch_list_key = k
        break
if batch_list_key is None:
    raise SystemExit('could not locate supplemental batch ledger')
holder[batch_list_key].append(BATCH_ID)
holder['latest_batch_doc'] = BATCH_DOC
focus = holder.get('current_focus')
if not isinstance(focus, list):
    raise SystemExit('current_focus missing')
focus.extend([
    'Batch 12BB follows the Fudan ancient-book portal source-emitted 綫裝古籍書目 route into the Fudan OPAC, rather than misusing the 明人文集书目 specialty endpoint as a general holdings catalog.',
    'Fudan first-party OPAC directly binds 新編評註通玄先生張果星宗大全 / 10卷 / 10冊(1函) / 刻本 / 善本 / 綫裝 / 明萬曆間 to call number rb2314, resource book no FDU01001127121, docId fudan_ancient_001127121 and catalogueId 34053686; the first-party holdings API then binds one actual in-library item, barcode AB0613271-80, at 复旦大学光华楼古籍书库.',
    'Batch 12BB therefore adds one independent Fudan Ming-Wanli material-holding control, but not an exact 1594 physical-witness vote: the first-party record exposes neither 萬曆二十二/1594 nor 唐謙. The secondary exact-1594/Tang-Qian locator remains unpromoted, and the Jiangsu timeout remains a route boundary rather than a no-holding conclusion.',
    'Batch 12BB adds zero target-text and Hai-glyph votes because no target leaf was obtained. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen. Next gate is a Fudan/SOAS first-party image or reproduction route, or another independent first-party exact 1593/1594 physical target leaf.'
])
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

verifier_path = ROOT / 'scripts/verify-project-continuity-state-r1.py'
verifier = verifier_path.read_text(encoding='utf-8')
ba_const = 'ZIWEI_ZHANGGUO_BA_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-R1.json"\n'
if ba_const not in verifier:
    raise SystemExit('BA verifier constant anchor missing')
verifier = verifier.replace(
    ba_const,
    ba_const + f'ZIWEI_ZHANGGUO_BB_BATCH = ROOT / "{BATCH_DOC}"\nZIWEI_ZHANGGUO_BB_EVIDENCE = ROOT / "{EVIDENCE_PATH}"\n',
    1,
)
ledger_anchor = '    "BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\n'
if ledger_anchor not in verifier:
    raise SystemExit('BA supplemental-ledger anchor missing')
verifier = verifier.replace(
    ledger_anchor,
    f'    "BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA",\n    "{BATCH_ID}",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\n',
    1,
)
old_latest = 'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA.md"'
if old_latest not in verifier:
    raise SystemExit('BA latest-doc anchor missing')
verifier = verifier.replace(old_latest, f'LATEST_BATCH_DOC = "{BATCH_DOC}"', 1)
main_anchor = 'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_BA_BATCH, ZIWEI_ZHANGGUO_BA_EVIDENCE):\n'
if main_anchor not in verifier:
    raise SystemExit('BA main artifact anchor missing')
verifier = verifier.replace(
    main_anchor,
    'def main() -> int:\n'
    '    for path in (ZIWEI_ZHANGGUO_BB_BATCH, ZIWEI_ZHANGGUO_BB_EVIDENCE):\n'
    '        if not path.is_file():\n'
    '            fail(f"Batch 12BB continuity artifact missing: {path.relative_to(ROOT)}")\n\n'
    '    for path in (ZIWEI_ZHANGGUO_BA_BATCH, ZIWEI_ZHANGGUO_BA_EVIDENCE):\n',
    1,
)
load_anchor = '    ziwei_zhangguo_ba_evidence = json.loads(ZIWEI_ZHANGGUO_BA_EVIDENCE.read_text(encoding="utf-8"))\n'
if load_anchor not in verifier:
    raise SystemExit('BA evidence-load anchor missing')
verifier = verifier.replace(load_anchor, load_anchor + '    ziwei_zhangguo_bb_evidence = json.loads(ZIWEI_ZHANGGUO_BB_EVIDENCE.read_text(encoding="utf-8"))\n', 1)
checks_anchor = '    # Provenance/access-only batches can advance without changing any Matrix row.\n'
if checks_anchor not in verifier:
    raise SystemExit('supplemental-batch check anchor missing')
bb_checks = '''    # Batch 12BB Fudan first-party Ming-Wanli target holding reconciliation.
    if ziwei_zhangguo_bb_evidence.get("batch_id") != "BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB":
        fail("Batch 12BB evidence identity mismatch")
    target12bb = ziwei_zhangguo_bb_evidence.get("target_catalog_record", {})
    if target12bb.get("title") != "新編評註通玄先生張果星宗大全" or target12bb.get("catalog_date") != "不详#明萬曆間":
        fail("Batch 12BB Fudan title/date binding regressed")
    if target12bb.get("resource_book_no") != "FDU01001127121" or target12bb.get("resource_smjlh") != "34053686" or target12bb.get("call_number") != "rb2314":
        fail("Batch 12BB Fudan catalog identifiers regressed")
    hold12bb = ziwei_zhangguo_bb_evidence.get("physical_holding", {})
    if hold12bb.get("holding_total") != 1 or hold12bb.get("barcode") != "AB0613271-80" or hold12bb.get("sub_location_name") != "光华楼古籍书库" or hold12bb.get("item_status_name") != "在馆":
        fail("Batch 12BB Fudan physical-holding binding regressed")
    edition12bb = ziwei_zhangguo_bb_evidence.get("edition_adjudication", {})
    if edition12bb.get("independent_fudan_ming_wanli_material_holding_control_established") is not True or edition12bb.get("ming_wanli_material_holding_control_increment") != 1:
        fail("Batch 12BB Ming-Wanli material control accounting regressed")
    if edition12bb.get("exact_wanli_22_or_1594_observed_in_first_party_record") is not False or edition12bb.get("tang_qian_observed_in_first_party_record") is not False or edition12bb.get("secondary_locator_exact_1594_tang_qian_claim_promoted") is not False:
        fail("Batch 12BB exact-1594/Tang-Qian evidence firewall regressed")
    if edition12bb.get("exact_1594_material_witness_increment") != 0 or edition12bb.get("target_leaf_obtained") is not False or edition12bb.get("independent_target_text_witness_increment") != 0 or edition12bb.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12BB target-witness accounting regressed")
    effect12bb = ziwei_zhangguo_bb_evidence.get("project_consequence", {})
    if effect12bb.get("audit_status") != "MISSING_FROM_PRODUCT" or effect12bb.get("runtime_winner_selected") is not False or effect12bb.get("candidate_collapsed") is not False or effect12bb.get("algorithm_reopen") is not False or effect12bb.get("matrix_row_count_change") is not False:
        fail("Batch 12BB HPA/algorithm/matrix firewall regressed")
    registry12bb = {s.get("source_id"): s for s in registry.get("sources", ())}.get("EXT-ZIWEI-ZHANGGUO-FUDAN-RB2314-MING-WANLI")
    if not registry12bb or registry12bb.get("first_party_physical_holding_bound") is not True or registry12bb.get("exact_1594_or_wanli_22_proven") is not False or registry12bb.get("independent_exact_1594_material_witness_increment") != 0:
        fail("Batch 12BB Fudan registry evidence firewall regressed")

'''
verifier = verifier.replace(checks_anchor, bb_checks + checks_anchor, 1)
verifier_path.write_text(verifier, encoding='utf-8')

print('Batch 12BB semantic files prepared')
