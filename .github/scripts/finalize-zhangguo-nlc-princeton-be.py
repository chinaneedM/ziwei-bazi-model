#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
REGISTRY_PATH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
VERIFIER_PATH = ROOT / "scripts/verify-project-continuity-state-r1.py"

BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-BE"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-BE.md"
EVIDENCE_PATH = "docs/research/ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-R1.json"
SOURCE_ID = "EXT-ZIWEI-ZHANGGUO-NLC-PRINCETON-NJPX95-B1857"
PREV_BATCH = "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD"
PREV_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD.md"

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

if state.get("schema_version") != "1.63.0":
    raise SystemExit(f"unexpected state schema before BE: {state.get('schema_version')}")
audit = state.get("historical_audit", {})
batches = audit.get("completed_batches", [])
if not batches or batches[-1] != PREV_BATCH:
    raise SystemExit(f"unexpected completed-batch tail before BE: {batches[-1:]}")
if audit.get("latest_batch_doc") != PREV_DOC:
    raise SystemExit(f"unexpected latest batch doc before BE: {audit.get('latest_batch_doc')}")
if BATCH_ID in batches:
    raise SystemExit("BE already registered")
if any(s.get("source_id") == SOURCE_ID for s in registry.get("sources", [])):
    raise SystemExit("BE source already registered")

# Exact first-party chain captured during the research sequence. Distinguish the 1593
# preface/catalog date from the 1594 cover/imprint statement; do not collapse them.
evidence = {
    "schema": "ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-R1",
    "batch_id": BATCH_ID,
    "question": "Does the NLC Chinese Rare Books Union Catalogue expose a physically independent early-Wanli Zhang Guo Xingzong witness, and does its public image route expose the late-Zi target leaf?",
    "first_party_provider": "国家图书馆/中华古籍善本联合书目",
    "catalog_object": {
        "title": "新編評註通玄先生張果星宗大全",
        "responsibility": "陸位輯校",
        "record_id": "NJPX95-B1857",
        "index_name": "data_467",
        "shelf_or_collection_number": "TC183/2991",
        "holding_institution": "普林斯顿大学东亚图书馆",
        "detail_url": "http://read.nlc.cn/allSearch/searchDetail?searchType=62&showType=3&indexName=data_467&fid=NJPX95-B1857",
        "catalog_time_statement": "明萬曆癸巳 [21年, 1593]",
        "preface_statement": "萬曆癸巳韓擢《張果星宗序》",
        "juanduan_statement": "卷端又題\"金陵三山益軒唐謙鋟梓\"",
        "cover_statement": "封面鐫\"萬曆閼逢敦牂張果星宗命格大全周氏文光新梓\". 萬曆閼逢敦牂即萬曆二十二年",
        "bibliographic_adjudication": {
            "preface_year": 1593,
            "cover_imprint_year": 1594,
            "cover_imprint_year_basis": "NLC detail explicitly glosses 萬曆閼逢敦牂 as 萬曆二十二年",
            "tang_qian_juanduan_observed": True,
            "zhou_wenguang_cover_imprint_observed": True,
            "do_not_collapse_1593_preface_into_1594_imprint": True
        }
    },
    "search_contract_chain": [
        {
            "stage": "NLC_HTTP_LANDING_AND_SOURCE_CONTRACT",
            "workflow_run_id": 34752100584,
            "artifact_id": 10316301987,
            "artifact_digest": "sha256:73e4927440410b882927d73bfe503640dbf272d85d2043e6bd79913872cd7532",
            "landing_http_status": 200,
            "landing_body_len": 27201,
            "landing_sha256": "58a1723fa25320a54bf2a6de15c19ef3b25edd0d94c2b2f7977c1183356d4843",
            "search_type_62": "中华古籍资源库"
        },
        {
            "stage": "NLC_SOURCE_EMITTED_TITLE_GET_QUERY",
            "workflow_run_id": 34753132831,
            "job_id": 103712921272,
            "artifact_id": 10315982944,
            "artifact_digest": "sha256:8efaae7d2caecd51db2ec14d283cddcff7622e43d9ffea5f3040660ace4b405d",
            "long_traditional_hit": True,
            "long_simplified_hit": True,
            "short_traditional_hit": True,
            "short_simplified_hit": True,
            "result_emitted_record_id": "NJPX95-B1857"
        },
        {
            "stage": "NLC_EXACT_RESULT_DETAIL",
            "workflow_run_id": 34753175084,
            "job_id": 103713032070,
            "artifact_id": 10316627671,
            "artifact_digest": "sha256:ec515b14ec414045532bc37333f82307b378afd95ae65f304d0b67644408b183",
            "detail_http_status": 200,
            "detail_body_len": 21409,
            "detail_sha256": "a4699510e13d3e61154b2c4d0c4fd3894812c32429d7754de95199abeb44561e"
        },
        {
            "stage": "NLC_DETAIL_EMITTED_IMAGE_VIEWER_CONTRACT",
            "workflow_run_id": 34753246009,
            "job_id": 103713217854,
            "artifact_id": 10316806982,
            "artifact_digest": "sha256:4d37a4c5228de76fa45cc81f22a332c8febd026bbbdec62632748d2ba9f2ad8e",
            "open_object_pic_url": "http://read.nlc.cn/OutOpenBook/OpenObjectPic?aid=467&bid=3244.0&lid=905349&did=NJPX95-B1857",
            "open_object_pic_http_status": 200,
            "open_object_pic_body_len": 6200,
            "open_object_pic_sha256": "b7e365d430aba452f9ceb9a31dc8f3c0b230740373afe1cfa32ffc3c7771abe8",
            "permission_checks_observed": [
                "/OutOpenBook/dataInOutPermission",
                "/OutOpenBook/resInOutPermission",
                "/allSearch/picPermission"
            ],
            "permission_conditional_iframe_route": "/OutOpenBook/openBookPic?aid=467&bid=3244.0&lid=905349&did=NJPX95-B1857",
            "page_viewer_permission_gated": True,
            "permission_bypass_attempted": False
        }
    ],
    "image_access": {
        "detail_emitted_thumbnail_url": "http://read.nlc.cn/doc1/data16/zhgjsblhsm_zhonghuagujishanbenlianheshumu/20120418_04/905349/L/NJPX95B1857.jpg",
        "detail_emitted_large_image_entry_observed": True,
        "large_image_entry_public_http_200": True,
        "page_viewer_permission_gated": True,
        "direct_page_bytes_obtained": False,
        "target_leaf_obtained": False,
        "direct_target_glyph_collation_authorized": False,
        "login_or_auth_bypass_attempted": False
    },
    "independence_adjudication": {
        "physical_holding_independent_from_tohoku_nijl_lineage": True,
        "basis": "Distinct holder 普林斯顿大学东亚图书馆 and shelf/collection number TC183/2991; this is not the NIJL/Tohoku item-control chain closed in AW/BC.",
        "independent_exact_1594_material_witness_increment": 1,
        "independent_target_text_witness_increment": 0,
        "independent_hai_glyph_witness_increment": 0,
        "whole_volume_text_negative_authorized": False
    },
    "project_consequence": {
        "rule_id": "HPA-ZDATE-006",
        "audit_status": "MISSING_FROM_PRODUCT",
        "matrix_count_change": False,
        "identified_missing_candidate_family_count_change": False,
        "provenance_defect_count_change": False,
        "new_candidate_family": False,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen": False,
        "required_missing_bridge": "upper/night Zi -> Hai branch"
    }
}
(ROOT / EVIDENCE_PATH).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

batch_doc = """# Fusion Chart Historical Provenance Audit R1 — Batch 12BE

## 《新編評註通玄先生張果星宗大全》国图联合目录—普林斯顿独立万历二十二年物质见证与图像权限边界

Status: **NLC FIRST-PARTY UNION-CATALOG OBJECT BOUND / PRINCETON EAST ASIAN LIBRARY TC183/2991 / 1593 PREFACE DATE KEPT DISTINCT FROM 1594 COVER IMPRINT / TANG QIAN JUANDUAN + ZHOU WENGUANG COVER IMPRINT DIRECTLY CATALOGUED / INDEPENDENT EXACT-1594 MATERIAL WITNESS +1 / PUBLIC LARGE-IMAGE ENTRY EXISTS BUT PAGE VIEWER IS PERMISSION-GATED / NO TARGET LEAF / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Question

After Batch 12BD closed the current Shandong hosted-runner access boundary, the next gate was a genuinely independent first-party exact-1593/1594 item record or target leaf. BE asks:

> Can a first-party union catalog bind a physically independent early-Wanli copy, and can its own emitted image route expose the late-Zi target leaf without bypassing access control?

## 2. NLC search route and exact object binding

The National Library of China public HTTP search surface for `searchType=62` is reachable. The source page itself emits the search URL used in this batch. Long/short and traditional/simplified title queries all converge on one exact result:

```text
record/fid=NJPX95-B1857
indexName=data_467
title=新編評註通玄先生張果星宗大全
responsibility=陸位輯校
shelf/collection no=TC183/2991
holder=普林斯顿大学东亚图书馆
```

The exact result-emitted detail page returned HTTP 200 and is the controlling first-party object for this batch.

## 3. Date/imprint philology: 1593 is not silently collapsed into 1594

The NLC detail exposes three different bibliographic statements and they must remain separate:

```text
catalog time=明萬曆癸巳 [21年, 1593]
preface=萬曆癸巳韓擢《張果星宗序》
juanduan=卷端又題「金陵三山益軒唐謙鋟梓」
cover=封面鐫「萬曆閼逢敦牂張果星宗命格大全周氏文光新梓」；萬曆閼逢敦牂即萬曆二十二年
```

Therefore the evidence is adjudicated as:

```text
PREFACE_YEAR=1593
COVER_IMPRINT_YEAR=1594
TANG_QIAN_JUANDUAN_OBSERVED=true
ZHOU_WENGUANG_COVER_IMPRINT_OBSERVED=true
```

The 1593 catalog/preface year is not treated as proof that the physical printing occurred in 1593. The exact-1594 material control comes from the catalogued cover/imprint statement itself.

## 4. Independence from the NIJL/Tohoku lineage

This object is held by **Princeton University East Asian Library** under `TC183/2991`. It is not the NIJL/Tohoku item-control chain audited in AW/BC. Accordingly:

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=1
```

This is a physical-holding/provenance increment only. It is not yet a target-passage vote.

## 5. Public image entry and permission boundary

The exact NLC detail page emits both a thumbnail and a “查看大图” route. The emitted `OpenObjectPic` page itself returns HTTP 200. Its own script, however, checks:

```text
/OutOpenBook/dataInOutPermission
/OutOpenBook/resInOutPermission
/allSearch/picPermission
```

Only after those checks pass does it assign the iframe to the emitted `openBookPic` route. BE does not call that conditional page route directly, does not guess page identifiers, does not log in, and does not bypass any permission check.

Therefore:

```text
PUBLIC_LARGE_IMAGE_ENTRY_OBSERVED=true
PAGE_VIEWER_PERMISSION_GATED=true
DIRECT_PAGE_BYTES_OBTAINED=false
TARGET_LEAF_OBTAINED=false
DIRECT_TARGET_GLYPH_COLLATION_AUTHORIZED=false
```

This is an access boundary, not proof that the target leaf is absent.

## 6. Witness accounting

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=1
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
WHOLE_VOLUME_TEXT_NEGATIVE_AUTHORIZED=false
```

The Princeton object strengthens the independent material history of the early Wanli lineage, but the missing late-Zi rule bridge still requires direct target text.

## 7. Effect on HPA-ZDATE-006 and product state

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
REQUIRED_MISSING_BRIDGE=upper/night Zi -> Hai branch
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No deterministic chart behavior changes are authorized.

## 8. Accounting

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

## 9. Durable evidence chain

```text
NLC landing/contract: run 34752100584 / artifact 10316301987
NLC title GET:        run 34753132831 / artifact 10315982944
NLC exact detail:     run 34753175084 / artifact 10316627671
NLC image viewer:     run 34753246009 / artifact 10316806982
```

Machine-readable consolidation:

```text
docs/research/ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-R1.json
```

## 10. Next gate

1. Seek a legitimate Princeton/NLC public or reproduction route that can expose the target late-Zi leaf without bypassing the NLC permission chain.
2. Continue independent exact-1593/1594 holdings research; prioritize a copy with public page images rather than another catalog-only duplicate.
3. If a Princeton target page is lawfully obtained, bind provider URL/object ID/digest/page/leaf and visually collate it without OCR before adding a target-text or Hai-glyph vote.
4. Keep HPA-ZDATE-006 unresolved until direct rule evidence supplies `upper/night Zi -> Hai branch`.
"""
(ROOT / BATCH_DOC).write_text(batch_doc, encoding="utf-8")

registry["access_date"] = "2026-09-13"
registry["sources"].append({
    "source_id": SOURCE_ID,
    "title": "《新編評註通玄先生張果星宗大全》NJPX95-B1857",
    "author_responsibility": "陸位輯校",
    "historical_period": "明萬曆；NLC record separates a 1593 preface/catalog date from a 1594 cover imprint",
    "provider": "国家图书馆・中华古籍善本联合书目 / holder: 普林斯顿大学东亚图书馆",
    "url": "http://read.nlc.cn/allSearch/searchDetail?searchType=62&showType=3&indexName=data_467&fid=NJPX95-B1857",
    "record_id": "NJPX95-B1857",
    "shelf_or_collection_number": "TC183/2991",
    "source_role": "FIRST_PARTY_UNION_CATALOG_PHYSICAL_HOLDING_AND_EXACT_1594_IMPRINT_WITNESS",
    "quality_notes": "First-party NLC union-catalog object directly binds Princeton holding TC183/2991 and records the 1593 Han Zhuo preface, Tang Qian juanduan imprint statement, and a Zhou Wenguang cover explicitly glossed as Wanli 22 (1594). The emitted page-viewer route is permission-gated; no target leaf or late-Zi glyph has been directly collated.",
    "batch_12be": {
        "independent_exact_1594_material_witness_increment": 1,
        "target_leaf_obtained": False,
        "target_text_witness_increment": 0,
        "hai_glyph_witness_increment": 0,
        "page_viewer_permission_gated": True
    }
})
REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state["schema_version"] = "1.64.0"
state["updated_at"] = "2026-09-13"
audit["completed_batches"].append(BATCH_ID)
audit["latest_batch_doc"] = BATCH_DOC
audit["current_focus"].append(
    "Batch 12BE binds NLC union-catalog object NJPX95-B1857 / Princeton East Asian Library TC183/2991 as a physically independent early-Wanli copy: the first-party detail separates the 1593 Han Zhuo preface/catalog date from a cover explicitly glossed as Wanli 22 (1594), records Tang Qian at the juanduan and Zhou Wenguang on the cover, and therefore adds +1 independent exact-1594 material witness. The NLC detail emits a public large-image entry, but its viewer enforces data/resource/pic permission checks before the page iframe; no bypass was attempted, no page bytes or target late-Zi leaf were obtained, target-text/Hai-glyph increments remain 0, and HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no algorithm reopen or candidate collapse."
)
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

text = VERIFIER_PATH.read_text(encoding="utf-8")
old_tail = '''    "BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB",\n    "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC",\n    "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD",\n]'''
new_tail = '''    "BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB",\n    "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC",\n    "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD",\n    "BATCH-12-ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-BE",\n]'''
if old_tail not in text:
    raise SystemExit("continuity supplemental tail anchor missing")
text = text.replace(old_tail, new_tail, 1)
old_latest = 'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD.md"'
new_latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
if old_latest not in text:
    raise SystemExit("continuity latest-batch-doc anchor missing")
text = text.replace(old_latest, new_latest, 1)

anchor = '    contract = state.get("new_chat_startup_contract", {})\n'
if anchor not in text:
    raise SystemExit("continuity contract anchor missing")
verify_block = '''    # Batch 12BE: independent Princeton exact-1594 material witness; page viewer remains permission-gated.\n    princeton_path = ROOT / "docs/research/ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-R1.json"\n    princeton_doc = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-BE.md"\n    if not princeton_path.is_file() or not princeton_doc.is_file():\n        fail("Batch 12BE durable evidence/doc missing")\n    princeton = load_json(princeton_path)\n    if princeton.get("schema") != "ZIWEI-ZHANGGUO-NLC-PRINCETON-1594-HOLDING-AND-IMAGE-ACCESS-R1":\n        fail("Batch 12BE evidence schema mismatch")\n    pobj = princeton.get("catalog_object", {})\n    if pobj.get("record_id") != "NJPX95-B1857" or pobj.get("shelf_or_collection_number") != "TC183/2991":\n        fail("Batch 12BE Princeton object identity mismatch")\n    if pobj.get("holding_institution") != "普林斯顿大学东亚图书馆":\n        fail("Batch 12BE Princeton holder mismatch")\n    if pobj.get("catalog_time_statement") != "明萬曆癸巳 [21年, 1593]":\n        fail("Batch 12BE 1593 catalog/preface control mismatch")\n    bib = pobj.get("bibliographic_adjudication", {})\n    if bib.get("preface_year") != 1593 or bib.get("cover_imprint_year") != 1594:\n        fail("Batch 12BE preface/imprint year separation mismatch")\n    if not bib.get("do_not_collapse_1593_preface_into_1594_imprint"):\n        fail("Batch 12BE 1593/1594 firewall missing")\n    if not bib.get("tang_qian_juanduan_observed") or not bib.get("zhou_wenguang_cover_imprint_observed"):\n        fail("Batch 12BE imprint controls missing")\n    image_access = princeton.get("image_access", {})\n    if not image_access.get("page_viewer_permission_gated") or image_access.get("direct_page_bytes_obtained"):\n        fail("Batch 12BE page-viewer access boundary mismatch")\n    if image_access.get("target_leaf_obtained") or image_access.get("direct_target_glyph_collation_authorized"):\n        fail("Batch 12BE target-leaf firewall violated")\n    indep = princeton.get("independence_adjudication", {})\n    if indep.get("independent_exact_1594_material_witness_increment") != 1:\n        fail("Batch 12BE exact-1594 material witness increment mismatch")\n    if indep.get("independent_target_text_witness_increment") != 0 or indep.get("independent_hai_glyph_witness_increment") != 0:\n        fail("Batch 12BE target-text/Hai-glyph vote firewall violated")\n    consequence = princeton.get("project_consequence", {})\n    if consequence.get("rule_id") != "HPA-ZDATE-006" or consequence.get("audit_status") != "MISSING_FROM_PRODUCT":\n        fail("Batch 12BE HPA-ZDATE-006 status mismatch")\n    if any(consequence.get(k) for k in ("matrix_count_change", "new_candidate_family", "runtime_winner_selected", "candidate_collapsed", "algorithm_reopen")):\n        fail("Batch 12BE product-state firewall violated")\n    psource = next((s for s in source_registry.get("sources", []) if s.get("source_id") == "EXT-ZIWEI-ZHANGGUO-NLC-PRINCETON-NJPX95-B1857"), None)\n    if psource is None or psource.get("record_id") != "NJPX95-B1857" or psource.get("shelf_or_collection_number") != "TC183/2991":\n        fail("Batch 12BE external-source registry binding missing")\n\n'''
text = text.replace(anchor, verify_block + anchor, 1)
VERIFIER_PATH.write_text(text, encoding="utf-8")

print(json.dumps({
    "batch_id": BATCH_ID,
    "state_schema_version": state["schema_version"],
    "record_id": evidence["catalog_object"]["record_id"],
    "holder": evidence["catalog_object"]["holding_institution"],
    "preface_year": 1593,
    "cover_imprint_year": 1594,
    "exact_1594_material_witness_increment": 1,
    "target_text_witness_increment": 0,
    "hai_glyph_witness_increment": 0,
    "target_leaf_obtained": False,
}, ensure_ascii=False, sort_keys=True))
