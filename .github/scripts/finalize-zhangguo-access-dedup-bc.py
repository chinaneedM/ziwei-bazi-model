#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC.md"
EVIDENCE_PATH = "docs/research/ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-R1.json"
STATE_PATH = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
REGISTRY_PATH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
AW_PATH = ROOT / "docs/research/ZIWEI-ZHANGGUO-1594-NIGHT-ZI-PHYSICAL-COLLATION-R1.json"
BB_PATH = ROOT / "docs/research/ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-FIRST-PARTY-HOLDING-RECONCILIATION-R1.json"

for p in (STATE_PATH, REGISTRY_PATH, AW_PATH, BB_PATH):
    if not p.is_file():
        raise SystemExit(f"missing prerequisite: {p}")

aw = json.loads(AW_PATH.read_text(encoding="utf-8"))
bb = json.loads(BB_PATH.read_text(encoding="utf-8"))
if aw.get("source", {}).get("bid") != "100238879":
    raise SystemExit("AW NIJL BID control changed")
if aw.get("source", {}).get("date") != "萬曆22 / 1594":
    raise SystemExit("AW edition-date control changed")
if bb.get("target_catalog_record", {}).get("call_number") != "rb2314":
    raise SystemExit("BB Fudan call-number control changed")
if bb.get("target_catalog_record", {}).get("resource_smjlh") != "34053686":
    raise SystemExit("BB Fudan catalogue-id control changed")

registration_numbers = [
    "01793921822", "01793921831", "01793921849", "01793921857", "01793921865"
]

evidence = {
    "schema": "ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-R1",
    "batch_id": BATCH_ID,
    "question": "Does the NACSIS/CiNii Wanli-22 Tohoku record add an independent 1594 witness beyond Batch 12AW, and what first-party access route currently exists for the Fudan Ming-Wanli holding from Batch 12BB?",
    "tohoku_nacsis_control": {
        "provider": "CiNii Books / NACSIS-CAT",
        "url": "https://ci.nii.ac.jp/ncid/BD05367609",
        "ncid": "BD05367609",
        "title": "新編評註通玄先生張果星宗大全",
        "responsibility": "陸位輯校",
        "publication": "周氏文光, 萬暦22 [1594]",
        "physical_extent": "5冊",
        "size": "24.4×15.4cm",
        "holding_count": 1,
        "holding_institution": "東北大学 附属図書館本館",
        "volume_registration_numbers": {
            "巻之1-2": "01793921822",
            "巻之3-4": "01793921831",
            "巻之5-6": "01793921849",
            "巻之7-8": "01793921857",
            "巻之9-10": "01793921865"
        },
        "edition_notes": [
            "序末に萬暦癸巳",
            "封面に萬暦閼逢敦牂(甲午)",
            "封面に周氏文光新梓",
            "和漢古書につき記述対象資料毎に書誌データ作成"
        ],
        "relationship_to_batch_12aw": {
            "aw_provider": "National Institute of Japanese Literature / Tohoku University Library",
            "aw_bid": "100238879",
            "same_title": True,
            "same_wanli_22_1594_date": True,
            "same_holding_institution_family": True,
            "explicit_bid_to_registration_number_crosswalk_observed": False,
            "physical_object_identity_status": "HIGH_CONFIDENCE_SAME_INSTITUTIONAL_EDITION_LINEAGE_NOT_FORMALLY_CLOSED_TO_EXACT_ACCESSION_OBJECT",
            "duplicate_vote_forbidden": True,
            "independent_exact_1594_material_witness_increment": 0,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0
        },
        "registration_number_count": len(registration_numbers)
    },
    "fudan_access_control": {
        "target_call_number": "rb2314",
        "target_resource_book_no": "FDU01001127121",
        "target_catalogue_id": "34053686",
        "target_barcode": "AB0613271-80",
        "first_party_ancient_book_service_url": "https://library.fudan.edu.cn/gj1/list.htm",
        "first_party_department_url": "https://library.fudan.edu.cn/e7/db/c42796a518107/page.htm",
        "first_party_document_delivery_url": "https://library.fudan.edu.cn/a9/64/c42780a698724/page.htm",
        "rare_book_appointment_required": True,
        "appointment_lead_time": "one working day",
        "appointment_target_fields": ["书名", "索书号", "函册数"],
        "reading_mode": "closed-stack / in-library reading",
        "outside_reader_first_visit_requires_identity_and_introduction_letter": True,
        "special_document_reproduction_policy": "古籍、缩微胶卷等特殊文献酌情提供；exact target eligibility and fee require provider-side confirmation",
        "public_target_image_or_fulltext_obtained": False,
        "target_specific_reproduction_request_submitted": False,
        "external_action_authorized": False,
        "target_leaf_obtained": False,
        "independent_target_text_witness_increment": 0,
        "independent_hai_glyph_witness_increment": 0
    },
    "chongqing_locator_control": {
        "secondary_locator_claim": "A secondary Chinese rare-book union-catalog transcription describes a Chongqing Library holding of the target title as a Wanli-22 / 1594 printed copy, six volumes.",
        "secondary_locator_promoted_to_first_party_item_fact": False,
        "first_party_general_ancient_collection_url": "https://www.cqlib.cn/web/column/col5003502.html",
        "first_party_general_collection_scope": "重庆图书馆自述馆藏古籍2.3万余种约30万册、善本3千余种约5万册",
        "first_party_exact_target_item_record_obtained": False,
        "public_target_opac_route_resolved": False,
        "target_leaf_obtained": False,
        "independent_exact_1594_material_witness_increment": 0,
        "independent_target_text_witness_increment": 0,
        "independent_hai_glyph_witness_increment": 0,
        "no_holding_inference_authorized": True
    },
    "project_consequence": {
        "audit_row": "HPA-ZDATE-006",
        "audit_status": "MISSING_FROM_PRODUCT",
        "matrix_row_count_change": False,
        "identified_missing_candidate_family_count_change": False,
        "provenance_defect_count_change": False,
        "new_candidate_family": False,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen": False
    }
}
(ROOT / EVIDENCE_PATH).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

batch_doc = """# Fusion Chart Historical Provenance Audit R1 — Batch 12BC

## 《張果星宗大全》东北大学 NACSIS 1594 馆藏 crosswalk、复旦访问路径与独立见证去重校勘

Status: **TOHOKU NACSIS WANLI-22 HOLDING METADATA BOUND / BATCH-12AW DUPLICATE-VOTE FIREWALL ENFORCED / EXACT NIJL-BID-TO-ACCESSION CROSSWALK NOT FORMALLY CLOSED / FUDAN OBJECT-LEVEL APPOINTMENT ROUTE ESTABLISHED / FUDAN PUBLIC TARGET IMAGE NOT OBTAINED / SPECIAL-DOCUMENT REPRODUCTION ONLY CASE-BY-CASE / NO REQUEST SUBMITTED / CHONGQING EXACT-1594 CLAIM REMAINS SECONDARY LOCATOR / ZERO NEW TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12BB established a first-party Fudan physical holding dated only `明萬曆間` and left two high-value routes: obtain a target leaf from Fudan, or find another genuinely independent exact 1593/1594 physical witness. Subsequent discovery surfaced NACSIS/CiNii record `BD05367609`, which at first glance looked like a new exact-1594 Tohoku witness.

BC tests that apparent increment against the already-collated Batch 12AW NIJL/Tohoku witness before any vote is counted, and separately records the current first-party access path for Fudan `rb2314`.

## 2. NACSIS/CiNii bibliographic control

CiNii Books / NACSIS-CAT record:

```text
NCID=BD05367609
title=新編評註通玄先生張果星宗大全
responsibility=陸位輯校
publication=周氏文光, 萬暦22 [1594]
extent=5冊
size=24.4×15.4cm
holding count=1
holding=東北大学 附属図書館本館
巻之1-2=01793921822
巻之3-4=01793921831
巻之5-6=01793921849
巻之7-8=01793921857
巻之9-10=01793921865
```

The same record also reports `序末に萬暦癸巳`, cover dating `萬暦閼逢敦牂(甲午)`, and `周氏文光新梓`.

These details are materially stronger than a generic title/date search result because they bind the edition to one Tohoku holding and five volume-level registration numbers.

## 3. Critical dedup firewall against Batch 12AW

Batch 12AW already directly collated:

```text
provider=National Institute of Japanese Literature / Tohoku University Library
BID=100238879
title=新編評註通玄先生張果星宗大全
date=萬曆22 / 1594
canvas count=439
target canvas=195
```

The NACSIS record and AW therefore converge on title, exact Wanli-22/1594 dating, and the Tohoku institutional holding family. However, the reviewed public metadata does **not** explicitly state:

```text
NIJL BID 100238879 == Tohoku registration 01793921822..01793921865
```

Accordingly BC records:

```text
EXACT_PHYSICAL_ACCESSION_CROSSWALK=HIGH_CONFIDENCE_NOT_FORMALLY_CLOSED
DUPLICATE_VOTE_FORBIDDEN=true
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

This is intentionally conservative. A missing explicit accession crosswalk is not permission to count the same institutional edition lineage twice.

## 4. Fudan first-party access route for rb2314

Fudan's current ancient-book service page states that rare books use an appointment service: readers should reserve one working day in advance and provide title, call number and case/volume count. The Ancient Book Reading Room is closed-stack and in-library reading; first-time outside readers require identity documentation and an introduction letter.

The target identifiers remain:

```text
call number=rb2314
resource book no=FDU01001127121
catalogueId=34053686
barcode=AB0613271-80
location=复旦大学 / 光华楼古籍书库
```

Current document-delivery policy says ancient books, microfilm and other special documents are supplied only **case by case**. That general policy does not establish that this exact target is reproducible, digitized, free, or remotely deliverable.

Therefore:

```text
FUDAN_OBJECT_LEVEL_APPOINTMENT_ROUTE=ESTABLISHED
FUDAN_PUBLIC_TARGET_IMAGE_OBTAINED=false
FUDAN_TARGET_SPECIFIC_REPRODUCTION_ELIGIBILITY=UNRESOLVED
FUDAN_REPRODUCTION_REQUEST_SUBMITTED=false
TARGET_LEAF_OBTAINED=false
```

No email, booking, copying request or other external action was submitted in this batch.

## 5. Chongqing locator remains locator-scoped

A secondary rare-book union-catalog transcription describes a Chongqing Library target-title holding as a Wanli-22 / 1594 printed copy in six volumes. Chongqing Library's own public site confirms a large ancient-book collection, but the reviewed first-party surfaces do not expose an exact target-title item record or target leaf.

Thus:

```text
CHONGQING_SECONDARY_EXACT_1594_LOCATOR=true
CHONGQING_FIRST_PARTY_EXACT_TARGET_ITEM_BOUND=false
CHONGQING_TARGET_LEAF_OBTAINED=false
INDEPENDENT_EXACT_1594_WITNESS_INCREMENT=0
```

Do not convert a secondary locator plus a first-party general collection description into a first-party target holding claim.

## 6. Effect on HPA-ZDATE-006

BC adds access and identity precision only. It does not add the missing historical mechanical edge:

```text
upper/night Zi -> Hai branch
```

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

## 7. Accounting

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

No Matrix count changes are authorized.

## 8. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-R1.json
```

## 9. Next gate

1. Prefer a **publicly obtainable target leaf** from a genuinely independent exact 1593/1594 physical copy. Jangseogak remains independently cataloged but its target leaf is still not publicly obtained.
2. Continue first-party item-level pursuit of the Chongqing/Weifang locators; do not promote secondary exact-year claims without item metadata or object bytes.
3. Fudan `rb2314` is now an explicit external-action boundary: a target-specific appointment/reproduction inquiry may be pursued only with user authorization and whatever identity/contact information the provider requires.
4. Keep the separate Fullbook cloudy/rain current-time acquisition chain open; do not conflate that unresolved mechanism with late-Zi witness counting.
"""
(ROOT / BATCH_DOC).write_text(batch_doc, encoding="utf-8")

registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
sources = registry.get("sources", [])
by_id = {s.get("source_id"): s for s in sources}
aw_source = by_id.get("EXT-ZIWEI-ZHANGGUO-NIJL-1594")
if not aw_source:
    raise SystemExit("registry AW source missing")
aw_source["nacsis_tohoku_dedup_control"] = {
    "ncid": "BD05367609",
    "url": "https://ci.nii.ac.jp/ncid/BD05367609",
    "publication": "周氏文光, 萬暦22 [1594]",
    "holding": "東北大学 附属図書館本館",
    "registration_numbers": registration_numbers,
    "exact_nijl_bid_to_registration_crosswalk_observed": False,
    "identity_status": "HIGH_CONFIDENCE_SAME_INSTITUTIONAL_EDITION_LINEAGE_NOT_FORMALLY_CLOSED_TO_EXACT_ACCESSION_OBJECT",
    "duplicate_vote_forbidden": True,
    "independent_witness_increment": 0,
    "batch_id": BATCH_ID
}
fudan = by_id.get("EXT-ZIWEI-ZHANGGUO-FUDAN-RB2314-MING-WANLI")
if not fudan:
    raise SystemExit("registry Fudan source missing")
fudan["current_access_control"] = {
    "ancient_book_service_url": "https://library.fudan.edu.cn/gj1/list.htm",
    "department_url": "https://library.fudan.edu.cn/e7/db/c42796a518107/page.htm",
    "document_delivery_url": "https://library.fudan.edu.cn/a9/64/c42780a698724/page.htm",
    "rare_book_appointment_required": True,
    "appointment_lead_time": "one working day",
    "closed_stack_in_library_reading": True,
    "special_document_reproduction": "CASE_BY_CASE_GENERAL_POLICY; TARGET_ELIGIBILITY_UNRESOLVED",
    "public_target_image_obtained": False,
    "request_submitted": False,
    "batch_id": BATCH_ID
}
registry["access_date"] = "2026-09-12"
REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
if state.get("schema_version") != "1.61.0":
    raise SystemExit(f"unexpected state schema before BC: {state.get('schema_version')}")
hist = state.get("historical_audit", {})
if not str(hist.get("latest_batch_doc", "")).endswith("FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB.md"):
    raise SystemExit("BC expected BB as latest batch")
completed = hist.setdefault("completed_batches", [])
if BATCH_ID not in completed:
    completed.append(BATCH_ID)
hist["latest_batch_doc"] = BATCH_DOC
focus = hist.setdefault("current_focus", [])
for item in [
    "Batch 12BC binds NACSIS/CiNii NCID BD05367609 to a Tohoku Main Library Wanli-22 [1594] five-volume target-title holding with volume registrations 01793921822/831/849/857/865 and Zhou Shi Wenguang publication metadata; because no public metadata explicitly crosswalks those accessions to NIJL BID 100238879, exact physical accession identity is HIGH_CONFIDENCE_NOT_FORMALLY_CLOSED and duplicate voting against Batch 12AW is forbidden.",
    "Batch 12BC establishes the current Fudan first-party access boundary for rb2314 / FDU01001127121 / catalogueId 34053686: rare-book appointment one working day in advance, closed-stack in-library reading, and special-document reproduction only case-by-case. No target-specific reproduction request or public target image has been obtained.",
    "The Chongqing Wanli-22 / 1594 six-volume claim remains a secondary locator only: Chongqing Library first-party pages confirm a major ancient-book collection but no exact target item record or target leaf was obtained. BC adds zero exact-1594 independent witness, target-text or Hai-glyph votes; HPA-ZDATE-006 remains MISSING_FROM_PRODUCT and all algorithm invariants remain unchanged."
]:
    if item not in focus:
        focus.append(item)
state["schema_version"] = "1.62.0"
state["updated_at"] = "2026-09-12"
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("Batch 12BC semantic files prepared")
