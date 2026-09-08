#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N.md"
EVIDENCE_PATH = "docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json"
SOURCE_ID = "EXT-HANYANG-MINGJINGGE-ZIWEI-QUANJI-V4-1870"


def write(path: str, text: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main() -> int:
    evidence = {
        "schema": "ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "status": "HANYANG_OFFICIAL_VOLUME4_PHYSICAL_COPY_BOUND_PUBLIC_DIGITAL_RESOURCE_ROUTE_RETURNS_NO_RECORD_TARGET_PAGE_NOT_EXPOSED",
        "hpa_rule_id": "HPA-ZDATE-006",
        "purpose": "Upgrade the Batch 12M Hanyang independent-holding locator to a first-party Hanyang University Library volume-4 physical-copy record, bind item identity and physical description, and close the current public digital-resource route without inventing target-page absence.",
        "public_search_ui": {
            "workflow_run_id": 34177957476,
            "artifact_id": 10037915482,
            "artifact_zip_sha256": "da3d1d9dcab308edd3449451e65d4c0afac75c3b6a3f58931ee07cc482171f75",
            "route": "https://lib.hanyang.ac.kr/search/i-discovery",
            "query": "新刻合倂十八飛星策天紫微斗數全集",
            "local_holding_result_count_observed": 6,
            "volume4_visible_result": "新刻合倂十八飛星策天紫微斗數全集. 卷4",
            "volume4_publication_visible": "羊城 : 明經閣, 同治九年(1870).",
            "volume4_call_number_visible": "133.3 진412ㅅ v.4",
            "authentication_attempted": False,
            "hidden_api_guessing_attempted": False,
        },
        "observed_search_json": {
            "workflow_run_id": 34178106456,
            "artifact_id": 10037939265,
            "artifact_zip_sha256": "e0584b842d8ceb1ed205510dbec83766672fe0866459ae41207d371eb0466a9c",
            "request_origin": "NATURALLY_EMITTED_BY_PUBLIC_UI",
            "volume3_biblio_id": 484927,
            "volume4_biblio_id": 484926,
            "volume5_biblio_id": 484925,
            "volume6_biblio_id": 484924,
            "volume4_resources_summary_fields": {
                "thumbnailUrl": None,
                "imageUrl": None,
                "resources": None,
                "newResources": None,
            },
        },
        "official_volume4_detail": {
            "workflow_run_id": 34178157398,
            "artifact_id": 10037969864,
            "artifact_zip_sha256": "3cc4cde8a017bdb2acc27ecc7a77540d183541cc1189ffc675fceba603a5bf1c",
            "navigation": "PUBLIC_UI_CLICK_ONLY_NO_DETAIL_URL_GUESSING",
            "public_detail_url": "https://lib.hanyang.ac.kr/search/i-discovery/484926?type=biblios-list-view",
            "biblio_id": 484926,
            "title": "新刻合倂十八飛星策天紫微斗數全集. 卷4",
            "responsibility": "陳博(宋) 著 ; 徐良弼(淸) 校正",
            "edition": "木板本",
            "publication": "羊城 : 明經閣, 同治九年(1870).",
            "extent": "1冊",
            "physical_description": "四周單邊, 半郭 10.4 x 9.2 cm, 無界, 12行24字, 頭註, 上內向黑魚尾 ; 15.7 ×10.8 cm.",
            "set_extent_note": "6卷6冊",
            "cover_title_note": "紫微斗數",
            "inside_cover_title_note": "飛星紫微斗數",
            "banxin_title_note": "飛星斗數",
            "colophon_note": "同治九年(1870) 新鐫 陳希夷先生 飛星紫微斗數 羊城 明經閣板",
            "call_number": "133.3 진412ㅅ v.4",
            "holding": "[서울]백남학술정보관",
            "location": "고전자료실",
            "accession": "HOM000001861",
            "target_heading_visible_in_bibliographic_detail": False,
            "target_text_visible_in_bibliographic_detail": False,
            "public_digital_like_link_count": 0,
            "negative_target_text_absence_claim_authorized": False,
        },
        "observed_public_api": {
            "corrected_workflow_commit": "49c68f3a3458171b1beeba207f6e0178deca672d",
            "workflow_run_id": 34178359903,
            "artifact_id": 10038051901,
            "artifact_zip_sha256": "cdb48eeda45ef1b9c5ff63b11f9741b8b50634ced63b48276a6cd2fa68d00154",
            "routes_were_naturally_emitted_by_public_detail_ui": True,
            "route_guessing_attempted": False,
            "parameter_expansion_attempted": False,
            "authentication_attempted": False,
            "biblio_route": {
                "url": "https://lib.hanyang.ac.kr/pyxis-api/1/biblios/484926",
                "http_status": 200,
                "bytes": 4339,
                "sha256": "244cde73f14720aff0cac11804fc2d108bfa0c7c6f016e4c54c02f4c4bf5b802",
            },
            "items_route": {
                "url": "https://lib.hanyang.ac.kr/pyxis-api/1/biblios/484926/items",
                "http_status": 200,
                "bytes": 803,
                "sha256": "9d0bf8abaed6ffbe308102a234fc472316070555b3ac1a1f213824fe72defd28",
                "item_id": 872523,
                "barcode": "HOM000001861",
                "call_number": "133.3 진412ㅅ v.4",
                "branch": "[서울]백남학술정보관",
                "location": "고전자료실",
                "item_state": "ON_SHELF",
                "circulation_state": "NOT_AVAILABLE",
            },
            "resources_route": {
                "url": "https://lib.hanyang.ac.kr/pyxis-api/1/biblios/484926/resources?isForPyxis3=true",
                "http_status": 200,
                "bytes": 88,
                "sha256": "ee405585fef57176299e587571497d991c7d78cadf57e86d5affc3ec9a273d5c",
                "success": True,
                "code": "success.noRecord",
                "message": "조회된 결과가 없습니다.",
                "public_digital_resource_object_returned": False,
            },
        },
        "provenance_adjudication": {
            "hanyang_independent_holding_status": "OFFICIALLY_BOUND_FIRST_PARTY_PHYSICAL_COPY",
            "independent_from_snu_at_holding_object_level": True,
            "independent_target_text_witness_added": False,
            "independent_hai_glyph_witness_added": False,
            "reason": "Hanyang first-party catalogue and item APIs bind a separate volume-4 physical copy, but no target 五凶神 page or late-Zi line is exposed on the current public catalogue surface.",
            "public_digital_resource_route_status": "CLOSED_CURRENT_PUBLIC_CATALOG_RETURNS_SUCCESS_NO_RECORD",
            "target_page_acquisition_status": "PENDING_NON_PUBLIC_OR_OTHER_PUBLIC_PHYSICAL_PAGE_ROUTE",
        },
        "epistemic_boundaries": {
            "bibliographic_detail_as_target_text_evidence": "FORBIDDEN",
            "success_noRecord_as_physical_copy_absence": "FORBIDDEN",
            "success_noRecord_as_current_public_catalog_resource_object_status": "AUTHORIZED_ONLY_FOR_CURRENT_PUBLIC_RESOURCES_ROUTE",
            "independent_holding_as_independent_target_glyph_vote_without_target_page": "FORBIDDEN",
            "snu_and_hanyang_as_same_physical_copy": "NOT_SUPPORTED_DISTINCT_HOLDING_OBJECTS_BOUND",
            "negative_target_text_absence_from_catalog_detail": "FORBIDDEN",
        },
        "adjudication": {
            "hpa_zdate_006": "MISSING_FROM_PRODUCT",
            "hanyang_volume4_physical_copy": "BOUND",
            "hanyang_public_digital_resource_route": "NO_RECORD",
            "hanyang_five_xiong_shen_target_page": "PENDING_DIRECT_PAGE",
            "direct_independent_hai_glyph_witness_count_added": 0,
            "new_candidate_authorized": False,
            "candidate_selection_authorized": False,
            "confirmed_chart_algorithm_defect_count": 0,
            "algorithm_reopen_authorized": False,
            "candidate_collapse_count": 0,
            "algorithm_effect": "NONE",
            "next_gate": "DIRECT_FIVE_XIONG_SHEN_PAGE_FROM_HANYANG_PHYSICAL_COPY_OR_OTHER_INDEPENDENT_QUANJI_PHYSICAL_COPY",
        },
    }
    write(EVIDENCE_PATH, json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")

    batch = """# Fusion Chart Historical Provenance Audit R1 — Batch 12N

## 1870 Mingjingge Quanji: Hanyang official volume-4 physical-copy binding and public-resource closure

Status: **HANYANG FIRST-PARTY PHYSICAL COPY BOUND / VOLUME 4 ITEM IDENTITY CLOSED / CURRENT PUBLIC DIGITAL RESOURCE ROUTE RETURNS NO RECORD / FIVE-XIONG-SHEN TARGET PAGE STILL PENDING / NO ALGORITHM REOPEN**

Batch 12N upgrades the Batch 12M Hanyang University locator from a secondary bibliography to Hanyang University Library's own public catalogue, item and resource APIs.

## 1. Official public search

The public Hanyang UI at `/search/i-discovery` directly returned six local holdings for `新刻合倂十八飛星策天紫微斗數全集`. Volume 4 is visible as:

`新刻合倂十八飛星策天紫微斗數全集. 卷4 / 羊城 : 明經閣, 同治九年(1870)`

with call number `133.3 진412ㅅ v.4` at `[서울]백남학술정보관`.

The search interaction naturally emitted the public catalogue request. No hidden endpoint guessing, authentication or parameter expansion was used.

## 2. Structured record identity

The public search JSON binds:

```text
V3=484927
V4=484926
V5=484925
V6=484924
```

Volume 4 is therefore not merely a title-string locator; it is Hanyang bibliographic object `484926`.

## 3. Official volume-4 physical description

A click on the rendered public UI result naturally navigates to:

`/search/i-discovery/484926?type=biblios-list-view`

The first-party detail/API record directly gives:

- title: `新刻合倂十八飛星策天紫微斗數全集. 卷4`;
- responsibility: `陳博(宋) 著 ; 徐良弼(淸) 校正`;
- edition: `木板本`;
- publication: `羊城 : 明經閣, 同治九年(1870)`;
- extent: `1冊`, with set note `6卷6冊`;
- physical format: `四周單邊, 半郭 10.4 x 9.2 cm, 無界, 12行24字, 頭註, 上內向黑魚尾 ; 15.7 ×10.8 cm`;
- cover title: `紫微斗數`;
- inside-cover title: `飛星紫微斗數`;
- banxin title: `飛星斗數`;
- colophon note: `同治九年(1870) 新鐫 陳希夷先生 飛星紫微斗數 羊城 明經閣板`;
- item id: `872523`;
- accession/barcode: `HOM000001861`;
- call number: `133.3 진412ㅅ v.4`;
- location: `[서울]백남학술정보관 / 고전자료실`;
- item state: on shelf; circulation: not available.

This closes Hanyang as a first-party, separately held physical copy rather than a secondary locator.

## 4. Current public digital-resource boundary

The public detail UI naturally requested:

`/pyxis-api/1/biblios/484926/resources?isForPyxis3=true`

The exact observed request was replayed without modification. It returned HTTP 200 with:

```json
{"success":true,"code":"success.noRecord","message":"조회된 결과가 없습니다."}
```

Therefore the authorized conclusion is narrowly:

`HANYANG_CURRENT_PUBLIC_CATALOG_DIGITAL_RESOURCE_OBJECT=NO_RECORD`

This does **not** mean the physical volume has never been digitized, cannot be reproduced, or is absent from non-public/institutional systems.

## 5. Target-text boundary

Neither the bibliographic detail nor the public resources route exposes `五凶神`, `子有十刻`, or a page image. A catalogue detail is not a target-text search corpus, so no negative textual claim is permitted.

Accordingly:

```text
HANYANG_PHYSICAL_COPY=INDEPENDENTLY_BOUND
HANYANG_TARGET_PAGE=PENDING_DIRECT_PAGE
INDEPENDENT_TARGET_TEXT_WITNESS_ADDED=0
INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
```

The SNU and Hanyang holdings are distinct physical-object routes at the catalogue level. They become independent textual/glyph votes only after target pages are directly observed.

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
HANYANG_VOLUME4_BIBLIO_ID=484926
HANYANG_VOLUME4_ITEM_ID=872523
HANYANG_VOLUME4_ACCESSION=HOM000001861
HANYANG_PUBLIC_RESOURCES=success.noRecord
HANYANG_FIVE_XIONG_SHEN_TARGET_PAGE=PENDING_DIRECT_PAGE
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_COUNT_ADDED=0
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

Next gate: a directly readable `五凶神` target page from the Hanyang physical copy or another independent Quanji physical copy.

## 7. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Machine evidence: `docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
"""
    write(BATCH_DOC, batch)

    matrix_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    row = next((r for r in matrix.get("rows", []) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row or row.get("audit_status") != "MISSING_FROM_PRODUCT":
        raise SystemExit("HPA-ZDATE-006 matrix row drift")
    row["later_witnesses"] = row.get("later_witnesses", "") + " Batch 12N upgrades the Hanyang University route to first-party catalogue/object evidence: public UI search binds volume 4 to biblio 484926; official detail/API binds 木板本 / 羊城明經閣 / 同治九年(1870), item 872523, barcode HOM000001861, call number 133.3 진412ㅅ v.4, and a six-volume/six-book set. The exact public resources request naturally emitted by the detail UI returns success.noRecord. This closes only the current public digital-resource route; no 五凶神 page or late-Zi target text is exposed, so the independent Hanyang target-text/Hai-glyph witness count remains zero."
    row["proposed_action"] = "Keep HPA-ZDATE-006 MISSING_FROM_PRODUCT and unselected. Hanyang is now an officially bound independent physical-copy route, but do not convert holding independence into textual/glyph independence without a direct 五凶神 target page. Treat success.noRecord only as the current public catalogue resource-object boundary; continue target-page acquisition through Hanyang reproduction/onsite/public-image routes or another independent Quanji copy."
    row["mingjingge_hanyang_official_physical_copy_artifact"] = EVIDENCE_PATH
    row["hanyang_volume4_biblio_id"] = 484926
    row["hanyang_volume4_item_id"] = 872523
    row["hanyang_volume4_accession"] = "HOM000001861"
    row["hanyang_volume4_call_number"] = "133.3 진412ㅅ v.4"
    row["hanyang_physical_copy_status"] = "OFFICIALLY_BOUND_FIRST_PARTY"
    row["hanyang_current_public_digital_resource_status"] = "NO_RECORD"
    row["hanyang_five_xiong_shen_target_page_status"] = "PENDING_DIRECT_PAGE"
    row["independent_hai_glyph_witness_count_added_batch_12n"] = 0
    matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reg_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    if any(s.get("source_id") == SOURCE_ID for s in registry.get("sources", [])):
        raise SystemExit("Batch 12N source registry entry already exists")
    registry.setdefault("sources", []).append({
        "source_id": SOURCE_ID,
        "title": "漢陽大學校圖書館《新刻合倂十八飛星策天紫微斗數全集》卷4 同治九年明經閣木板本",
        "historical_period": "QING TONGZHI 9 / 1870 WOODBLOCK PHYSICAL COPY",
        "provider": "Hanyang University Library",
        "url": "https://lib.hanyang.ac.kr/search/i-discovery/484926?type=biblios-list-view",
        "source_role": "FIRST_PARTY_INDEPENDENT_PHYSICAL_COPY_AND_PUBLIC_CATALOG_RESOURCE_ROUTE_CONTROL_NOT_TARGET_GLYPH_AUTHORITY",
        "quality_notes": "First-party public UI/API binds biblio 484926, item 872523, barcode HOM000001861, 木板本, 羊城明經閣, 同治九年(1870), call number 133.3 진412ㅅ v.4 and physical format. The naturally emitted public resources route returns success.noRecord. No target 五凶神 page or late-Zi text is exposed; this source adds no independent target-text or Hai-glyph vote.",
        "biblio_id": 484926,
        "item_id": 872523,
        "accession": "HOM000001861",
        "call_number": "133.3 진412ㅅ v.4",
        "public_digital_resource_status": "NO_RECORD_ON_CURRENT_PUBLIC_RESOURCES_ROUTE",
        "target_page_status": "PENDING_DIRECT_PAGE",
        "research_artifact": EVIDENCE_PATH,
        "workflow_runs": [34177957476, 34178106456, 34178157398, 34178359903],
    })
    reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    state_path = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("schema_version") != "1.24.0":
        raise SystemExit(f"unexpected state schema version: {state.get('schema_version')}")
    audit = state["historical_audit"]
    if BATCH_ID in audit.get("completed_batches", []):
        raise SystemExit("Batch 12N already completed")
    state["schema_version"] = "1.25.0"
    audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    audit["current_focus"].extend([
        "Batch 12N upgrades the Batch 12M Hanyang locator to Hanyang University Library first-party evidence: public search binds 新刻合倂十八飛星策天紫微斗數全集 volume 4 to biblio 484926.",
        "Hanyang official detail/API binds volume 4 as 木板本 / 羊城 明經閣 / 同治九年(1870), item 872523, accession HOM000001861, call number 133.3 진412ㅅ v.4, with set extent 6卷6冊 and physical format 四周單邊 / 12行24字 / 頭註 / 上內向黑魚尾.",
        "Batch 12N public search/detail/API runs are 34177957476 / 34178106456 / 34178157398 / 34178359903 with artifacts 10037915482 / 10037939265 / 10037969864 / 10038051901.",
        "The exact Hanyang public resources route naturally emitted by the detail UI returns HTTP 200 + success.noRecord; current public catalog therefore exposes no digital resource object for biblio 484926.",
        "success.noRecord is only a current public resource-route boundary; it is not physical-copy absence, no-digitization-ever proof, or target-text absence proof.",
        "Hanyang is independent from the SNU holding at physical-object level, but without a direct 五凶神 page it adds zero independent target-text/Hai-glyph votes; HPA-ZDATE-006 remains MISSING_FROM_PRODUCT.",
        "Next high-value gate remains a direct 五凶神 target page from Hanyang volume 4 or another independent Quanji physical copy; Bodleian Ming-copy locator remains unbound because the official East Asian catalogue is challenge-protected in the runner and search-engine non-hits are not absence proof.",
    ])
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md"
    md = md_path.read_text(encoding="utf-8")
    anchor = "\n## Cross-chat continuity"
    if anchor not in md:
        raise SystemExit("matrix MD continuity anchor missing")
    note = """
- Batch 12N: upgrades Hanyang from the Batch 12M secondary holding locator to a first-party physical-copy record. Public UI/API binds `新刻合倂十八飛星策天紫微斗數全集. 卷4` to biblio `484926`, item `872523`, barcode `HOM000001861`, call number `133.3 진412ㅅ v.4`, `木板本 / 羊城明經閣 / 同治九年(1870)`, with six-volume/six-book set and detailed block-format metadata. The exact `/resources` request naturally emitted by the detail UI returns HTTP 200 + `success.noRecord`, closing only the current public catalogue resource-object route. No `五凶神` target page or late-Zi line is exposed, so Hanyang is independent at physical-holding level but adds zero independent target-text/Hai-glyph votes. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; counts remain 198 / 166 / 10 / 14; no algorithm reopen. Machine evidence: `docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json`.
"""
    md_path.write_text(md.replace(anchor, note + anchor, 1), encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if "截至 Batch 12M，Matrix 为" not in readme:
        raise SystemExit("README Batch 12M count marker missing")
    readme = readme.replace("截至 Batch 12M，Matrix 为", "截至 Batch 12N，Matrix 为", 1)
    latest_marker = "最新历史批次见 `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M.md`"
    if latest_marker not in readme:
        raise SystemExit("README latest Batch 12M marker missing")
    paragraph = "Batch 12N 又把 12M 中仅由韩国学中央研究院书目定位的汉阳大学馆藏提升为汉阳大学图书馆官方一手实体记录：公开 UI/API 直接绑定卷4 biblio `484926`、item `872523`、条码 `HOM000001861`、索书号 `133.3 진412ㅅ v.4`，并明确 `木板本 / 羊城明經閣 / 同治九年(1870)`、`6卷6冊` 与版式 `四周單邊、12行24字、頭註、上內向黑魚尾`。详情页自然请求的 `/resources` 接口又直接返回 HTTP 200 + `success.noRecord`，因此当前公开目录没有为该卷返回数字资源对象；这不能外推成“从未数字化”或“目标文不存在”。汉阳与 SNU 现可确认是不同馆藏实体路线，但在取得汉阳卷4《五凶神》目标页之前仍不能算独立文字/字形一票。12N 不新增候选、不改变 198/166/10/14 计数、不重开算法。 "
    readme = readme.replace(latest_marker, paragraph + f"最新历史批次见 `{BATCH_DOC}`", 1)
    readme_path.write_text(readme, encoding="utf-8")

    v_path = ROOT / "scripts/verify-project-continuity-state-r1.py"
    v = v_path.read_text(encoding="utf-8")
    const_anchor = 'ZIWEI_MINGJINGGE_SNU_EVIDENCE = ROOT / "docs/research/ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-R1.json"\n'
    if const_anchor not in v:
        raise SystemExit("verifier 12M constant anchor missing")
    v = v.replace(const_anchor, const_anchor +
        f'ZIWEI_MINGJINGGE_HANYANG_BATCH = ROOT / "{BATCH_DOC}"\n' +
        f'ZIWEI_MINGJINGGE_HANYANG_EVIDENCE = ROOT / "{EVIDENCE_PATH}"\n', 1)
    list_anchor = '    "BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M",\n]'
    if list_anchor not in v:
        raise SystemExit("verifier supplemental batch anchor missing")
    v = v.replace(list_anchor,
        '    "BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M",\n'
        '    "BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N",\n]', 1)
    v = v.replace(
        'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M.md"',
        f'LATEST_BATCH_DOC = "{BATCH_DOC}"', 1)
    tuple_anchor = 'ZIWEI_MINGJINGGE_SNU_BATCH, ZIWEI_MINGJINGGE_SNU_EVIDENCE):'
    if tuple_anchor not in v:
        raise SystemExit("verifier artifact tuple anchor missing")
    v = v.replace(tuple_anchor,
        'ZIWEI_MINGJINGGE_SNU_BATCH, ZIWEI_MINGJINGGE_SNU_EVIDENCE, ZIWEI_MINGJINGGE_HANYANG_BATCH, ZIWEI_MINGJINGGE_HANYANG_EVIDENCE):', 1)
    load_anchor = '    ziwei_mingjingge_snu_evidence = json.loads(ZIWEI_MINGJINGGE_SNU_EVIDENCE.read_text(encoding="utf-8"))\n'
    if load_anchor not in v:
        raise SystemExit("verifier 12M load anchor missing")
    v = v.replace(load_anchor, load_anchor +
        '    ziwei_mingjingge_hanyang_evidence = json.loads(ZIWEI_MINGJINGGE_HANYANG_EVIDENCE.read_text(encoding="utf-8"))\n', 1)

    check_anchor = '    focus_text = "\\n".join(audit_state.get("current_focus", ()))\n'
    if check_anchor not in v:
        raise SystemExit("verifier focus anchor missing")
    checks = r'''    # Batch 12N upgrades Hanyang from a secondary locator to a first-party physical-copy binding while preserving the target-page fail-closed boundary.
    if ziwei_mingjingge_hanyang_evidence.get("batch_id") != "BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N":
        fail("Batch 12N evidence batch identity mismatch")
    ui12n = ziwei_mingjingge_hanyang_evidence.get("public_search_ui", {})
    if ui12n.get("workflow_run_id") != 34177957476 or ui12n.get("artifact_id") != 10037915482:
        fail("Batch 12N public UI provenance regressed")
    sj12n = ziwei_mingjingge_hanyang_evidence.get("observed_search_json", {})
    if sj12n.get("volume4_biblio_id") != 484926 or sj12n.get("artifact_id") != 10037939265:
        fail("Batch 12N Hanyang volume-4 biblio binding regressed")
    det12n = ziwei_mingjingge_hanyang_evidence.get("official_volume4_detail", {})
    if det12n.get("biblio_id") != 484926 or det12n.get("edition") != "木板本" or det12n.get("accession") != "HOM000001861":
        fail("Batch 12N official Hanyang physical-copy identity regressed")
    if det12n.get("call_number") != "133.3 진412ㅅ v.4" or det12n.get("target_text_visible_in_bibliographic_detail") is not False:
        fail("Batch 12N detail/target boundary regressed")
    api12n = ziwei_mingjingge_hanyang_evidence.get("observed_public_api", {})
    if api12n.get("workflow_run_id") != 34178359903 or api12n.get("artifact_id") != 10038051901:
        fail("Batch 12N corrected API provenance regressed")
    if api12n.get("biblio_route", {}).get("sha256") != "244cde73f14720aff0cac11804fc2d108bfa0c7c6f016e4c54c02f4c4bf5b802":
        fail("Batch 12N biblio response digest regressed")
    if api12n.get("items_route", {}).get("barcode") != "HOM000001861" or api12n.get("items_route", {}).get("item_id") != 872523:
        fail("Batch 12N item identity regressed")
    res12n = api12n.get("resources_route", {})
    if res12n.get("http_status") != 200 or res12n.get("code") != "success.noRecord" or res12n.get("public_digital_resource_object_returned") is not False:
        fail("Batch 12N current public resource-route boundary regressed")
    prov12n = ziwei_mingjingge_hanyang_evidence.get("provenance_adjudication", {})
    if prov12n.get("hanyang_independent_holding_status") != "OFFICIALLY_BOUND_FIRST_PARTY_PHYSICAL_COPY" or prov12n.get("independent_target_text_witness_added") is not False:
        fail("Batch 12N Hanyang physical/textual independence boundary regressed")
    adj12n = ziwei_mingjingge_hanyang_evidence.get("adjudication", {})
    if adj12n.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12n.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12N HPA-ZDATE-006 boundary regressed")
    if adj12n.get("algorithm_reopen_authorized") is not False or adj12n.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12N algorithm boundary regressed")
    hy_source12n = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-HANYANG-MINGJINGGE-ZIWEI-QUANJI-V4-1870"), None)
    if not hy_source12n or hy_source12n.get("biblio_id") != 484926 or hy_source12n.get("public_digital_resource_status") != "NO_RECORD_ON_CURRENT_PUBLIC_RESOURCES_ROUTE":
        fail("Batch 12N Hanyang source-registry binding regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("mingjingge_hanyang_official_physical_copy_artifact") != "docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json":
        fail("Batch 12N Matrix artifact binding regressed")
    if nanyang_row.get("hanyang_current_public_digital_resource_status") != "NO_RECORD" or nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12n") != 0:
        fail("Batch 12N Matrix resource/witness-count boundary regressed")

'''
    v = v.replace(check_anchor, checks + check_anchor, 1)
    focus_tuple_anchor = '        "五凶神 target page",\n    ):'
    if focus_tuple_anchor not in v:
        raise SystemExit("verifier Batch 12M focus fragment anchor missing")
    v = v.replace(focus_tuple_anchor,
        '        "五凶神 target page",\n'
        '        "Batch 12N",\n'
        '        "484926",\n'
        '        "872523",\n'
        '        "HOM000001861",\n'
        '        "133.3 진412ㅅ v.4",\n'
        '        "success.noRecord",\n'
        '        "34178359903",\n'
        '        "10038051901",\n'
        '        "zero independent target-text/Hai-glyph votes",\n'
        '    ):', 1)
    v_path.write_text(v, encoding="utf-8")

    print(json.dumps({
        "batch": BATCH_ID,
        "evidence": EVIDENCE_PATH,
        "latest_doc": BATCH_DOC,
        "matrix_rows": len(matrix.get("rows", [])),
        "state_schema_version": state["schema_version"],
        "completed_batch_count": len(audit["completed_batches"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
