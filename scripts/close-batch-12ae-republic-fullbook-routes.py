#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "BATCH-12-ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-AE"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-AE.md"
EVIDENCE_PATH = "docs/research/ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-R1.json"
HUIWENTANG_SOURCE_ID = "EXT-KONGFZ-HUIWENTANG-REPUBLIC-ZWDSQS-PHYSICAL"
JINZHANG_SOURCE_ID = "EXT-SHUCANG-JINZHANG-REPUBLIC-ZWDSQS-CATALOG"
JINYUAN_SOURCE_ID = "EXT-XINYI-JINYUAN-ZWDSQS-MODERN-TOC"


def dump(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    evidence = {
        "schema": "ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-R1",
        "batch_id": BATCH_ID,
        "access_date": "2026-09-09",
        "status": "HUIWENTANG_PHYSICAL_IMPRINT_DIRECTLY_OBSERVED_JINZHANG_CATALOG_AND_LATER_REPRINT_ROUTES_BOUND_TARGET_LEAF_NOT_OBSERVED",
        "huiwentang_kongfz": {
            "item_url": "https://book.kongfz.com/520108/4153377684/",
            "provider_page_http_status": 200,
            "provider_page_bytes": 146844,
            "provider_page_sha256": "66631ea7bde9ed88ab42c45d9a5857db568f50a84d06888d82e56085283cda8b",
            "provider_metadata": {
                "title": "紫薇斗数全书（1-4卷）",
                "author": "陈希夷",
                "printing": "石印",
                "binding": "线装",
                "extent": "4册",
                "publisher": "上海会文堂书局印行",
            },
            "direct_physical_title_image": {
                "sha256": "767f5d01986c8f4a2b655699fce7af50917afd76a34e321ecf8254e6e09a0e9a",
                "source_url": "https://www0.kfzimg.com/sw/kfz-cos/kfzimg/acbddfed/dcdc291a5fed16c3_b.jpg",
                "direct_no_ocr_reading": ["陳希夷先生著", "紫微斗數全書", "上海會文堂書局印行"],
            },
            "direct_outer_cover_image": {
                "sha256": "aa8418fde8b01fddb71db0ea3b8070be9326367d0d9326df07baf31c5217c25b"
            },
            "direct_ocr_used": False,
            "target_late_zi_leaf_observed": False,
            "research_run_id": 34312796793,
            "research_job_id": 102342735385,
            "artifact_id": 10088973230,
            "artifact_zip_sha256": "fd0e6633d92110c94a18b130b26da100b9a96ef382821e976a7d917662b2cbd4",
        },
        "jinzhang_routes": {
            "shucang_catalog": {
                "url": "https://homeinmists.ilotus.org/%E7%B6%B2%E7%AB%99%E5%85%AC%E5%91%8A/%E9%81%93%E5%AE%B6%E8%B3%87%E8%A8%8A/%E9%81%93%E5%AD%B8%E5%9C%96%E6%9B%B8%E5%87%BA%E7%89%88%E4%BF%A1%E6%81%AF/%E3%80%8A%E9%87%8D%E5%88%8A%E8%A1%93%E8%97%8F%E3%80%8B/",
                "http_status": 200,
                "decoded_bytes": 231050,
                "decoded_sha256": "cde0aa92987e966bdf90819c3bf7f7b6dbb5f63bedaaa3b40bbf07766f5be277",
                "direct_catalog_entry": "術藏 第五十九卷 / 紫微斗數全書 / [宋]陳希夷撰 / 民國錦章書局石印本 / 四卷一冊全 / 三三三",
                "volume": 59,
                "start_page": 333,
                "authority_scope": "MODERN_REPRINT_CATALOG_BIBLIOGRAPHIC_IDENTITY_NOT_TARGET_GLYPH_AUTHORITY",
            },
            "artron_oldset": {
                "url": "https://zxp.artron.net/specials/goods/goodsdetail/1689675",
                "http_status": 200,
                "decoded_bytes": 49534,
                "decoded_sha256": "8fdcc0d1ab0578c10fb407b783ef4f0d54c83ccb05608a3e0fa18cba2296774a",
                "seller_description": "《紫薇斗数全书》是据民国锦章书局石印本影印出版的图书；4卷1函（全）",
                "direct_photo_sha256": [
                    "e67063a9478aeec7f2ae923c9636b0eab24db80d6be1ac2ba839539bdb89e531",
                    "a94f63cac9cbd074b5a758f6bc54a609219c635836396c5e4e2c4e2b5f3e39cc",
                    "6bdae03ac4f4cded4d87cfd13edfa92c73094d82f6e5136db17fed5fb2fb688e",
                    "c9d82ff9a35e720756f8a351bb164ed35747e9a3f2b12e07566be9123a63c266",
                    "dad58d634ce29a8034d007c79aabcac52321f245122ba5fabdb18c79b69e0b4a",
                    "728a75d8faa70074b4d144f002bd2c6506518df942b5c2f4e96567b437ef8663",
                ],
                "direct_no_ocr_review": "PHOTOS_SHOW_FOUR_VOLUME_PHYSICAL_SET_TITLE_SURFACE_AND_OPEN_TEXT_LEAVES; NO_DIRECT_JINZHANG_IMPRINT_AND_NO_TARGET_LATE_ZI_LEAF_OBSERVED",
                "direct_jinzhang_imprint_observed": False,
                "target_late_zi_leaf_observed": False,
            },
            "research_run_id": 34313072473,
            "research_job_id": 102343557647,
            "artifact_id": 10089077451,
            "artifact_zip_sha256": "0d6eef5fa0df7659246e680ff2b4d3c3207d2b53bd9e2761e34650b7c654b473",
        },
        "jinyuan_modern_reprint": {
            "url": "https://hr.xinyi.hk/goods-5266.html",
            "http_status": 200,
            "decoded_bytes": 65105,
            "decoded_sha256": "65ee7e9ac7d8d82eebeccb7ef4a423ca779b45d3b95174e83a7f28d92b6d3e80",
            "edition_scope": "TAIWAN_JINYUAN_MODERN_REFORMAT_NOT_PHYSICAL_JINZHANG_GLYPH_AUTHORITY",
            "isbn": "9789868759374",
            "modern_toc_target_heading": "論人生時要審的確",
            "modern_toc_target_page": 175,
            "public_images_review": "COVER_AND_TABLE_OF_CONTENTS_ONLY; TARGET_BODY_PAGE_NOT_OBSERVED",
            "target_body_page_observed": False,
        },
        "fengshui168_version_study": {
            "url": "https://fengshui-168.net/thread-114827-1-1.html",
            "github_runner_status": "ACCESS_TIMEOUT_OR_FAILURE_NO_PAGE_BYTES_OBTAINED",
            "content_absence_claim_authorized": False,
        },
        "adjudication": {
            "huiwentang_physical_imprint_identity": "DIRECTLY_OBSERVED",
            "jinzhang_bibliographic_identity": "SUPPORTED_AT_SHUCANG_CATALOG_LEVEL",
            "jinzhang_direct_physical_imprint_in_reviewed_photos": "NOT_OBSERVED",
            "late_zi_target_page_observed": False,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "candidate_created": False,
            "candidate_selected": False,
            "algorithm_reopen_authorized": False,
            "algorithm_effect": "NONE",
            "next_gate": "DIRECT_TARGET_LEAF_FROM_HUIWENTANG_JINZHANG_OR_ANOTHER_IMPRINT_BOUND_FULLBOOK_COPY",
        },
        "safety": {
            "authentication_attempted": False,
            "purchase_attempted": False,
            "identifier_guessing_attempted": False,
            "access_control_bypass_attempted": False,
            "direct_ocr_used": False,
        },
    }
    dump(ROOT / EVIDENCE_PATH, evidence)

    batch = """# Fusion Chart Historical Provenance Audit R1 — Batch 12AE

## Republic-era Huiwentang physical imprint and Jinzhang catalog/facsimile routes

Status: **HUIWENTANG PHYSICAL IMPRINT DIRECTLY OBSERVED / JINZHANG CATALOG IDENTITY BOUND / JINZHANG IMPRINT NOT DIRECTLY OBSERVED IN REVIEWED PHOTOS / TARGET LATE-ZI LEAF NOT OBSERVED / ZERO TEXTUAL OR HAI-GLYPH VOTES / NO ALGORITHM EFFECT**

## 1. Scope

Batch 12AE continues `HPA-ZDATE-006` after Batch 12AD. It does not reopen deterministic chart algorithms. The batch separates three evidentiary layers that are easy to conflate:

1. a directly photographed Republic-era-looking Huiwentang physical Fullbook set;
2. catalog/facsimile routes that identify a Republic Jinzhang Fullbook edition;
3. modern reformat/reprint surfaces that can locate the target section but are not historical glyph authority.

The purpose is edition-route closure, not source-count voting.

## 2. Huiwentang physical copy

Kongfz public item `520108/4153377684` records `紫薇斗数全书（1-4卷）`, Chen Xiyi, stone printing, thread binding, four volumes and `上海会文堂书局印行`.

A source-emitted large physical photograph was directly reviewed without OCR. Its title surface visibly reads:

```text
陳希夷先生著
紫微斗數全書
上海會文堂書局印行
```

The image SHA-256 is `767f5d01986c8f4a2b655699fce7af50917afd76a34e321ecf8254e6e09a0e9a`.

This upgrades Huiwentang from a generic bibliographic mention to a directly observed physical-imprint route. The public photos do **not** show `《論人生時要審的確》`, so they add no target-text or Hai-glyph vote.

## 3. Jinzhang routes

### 3.1 `術藏` catalog binding

The public `《重刊術藏》` catalog directly places:

```text
術藏 第五十九卷
紫微斗數全書 [宋]陳希夷撰
民國錦章書局石印本 四卷一冊全
三三三
```

Thus the Jinzhang edition is reproducibly bound at modern reprint-catalog level to volume 59 starting at page 333. This is bibliographic identity, not direct target-glyph authority.

### 3.2 Artron physical set

Artron object `1689675` publicly describes a four-volume set as a reproduction based on the Republic Jinzhang lithographic edition. Six source-emitted physical photographs were directly reviewed without OCR. They visibly establish a physical four-volume Fullbook set and expose title/open-text surfaces, but none of the reviewed photographs directly shows a `錦章書局` imprint and none shows the target late-Zi leaf.

Therefore the seller description and photographs must remain two separate evidence layers:

```text
SELLER_JINZHANG_DESCRIPTION=OBSERVED
DIRECT_JINZHANG_IMPRINT_IN_REVIEWED_PHOTOS=NOT_OBSERVED
```

No direct Jinzhang physical-text vote is added.

## 4. Jinyuan modern reformat control

Xinyi's public product page for the Jinyuan edition (`ISBN 9789868759374`) identifies it as a modern reformat. Its public table of contents directly places `論人生時要審的確` at modern printed page 175. The public image set exposes cover and contents pages only; the target body page is not shown.

This is useful as a modern locator but cannot establish the historical Jinzhang wording or glyphs.

## 5. HPA-ZDATE-006 adjudication

Nothing in Batch 12AE changes the direct textual conflict already established by Nanyangtang and the Korea Springgang manuscript.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=UNRESOLVED
HUIWENTANG_PHYSICAL_IMPRINT=OBSERVED
HUIWENTANG_TARGET_LEAF=NOT_OBSERVED
JINZHANG_CATALOG_IDENTITY=BOUND
JINZHANG_DIRECT_TARGET_LEAF=NOT_OBSERVED
BATCH_12AE_TARGET_TEXT_WITNESS_INCREMENT=0
BATCH_12AE_HAI_GLYPH_WITNESS_INCREMENT=0
NEW_CANDIDATE_FAMILY=NO
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic fusion-chart product remains CLOSED.

## 6. Next evidence gate

The next high-value gate is no longer another generic Republic-edition catalog entry. It is a directly readable target leaf from one of these imprint-bound routes:

- Shanghai Huiwentang physical copy;
- Republic Jinzhang copy/facsimile whose internal imprint is directly visible;
- another independently bound Fullbook edition.

Modern contents pages, seller prose and reprint catalogs may locate that leaf but must not substitute for it.

## 7. Machine evidence

`docs/research/ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-R1.json`
"""
    (ROOT / BATCH_DOC).write_text(batch, encoding="utf-8")

    state_path = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.42.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12AE directly observes a Huiwentang physical Fullbook title surface reading 陳希夷先生著 / 紫微斗數全書 / 上海會文堂書局印行 from a source-emitted Kongfz photograph; no target late-Zi leaf is present in the reviewed public photos.",
        "Batch 12AE binds the Republic Jinzhang Fullbook at modern Shucang catalog level: volume 59 / 民國錦章書局石印本 / 四卷一冊全 / start page 333. This is bibliographic identity only, not target-glyph authority.",
        "Artron's four-volume physical-set photos establish a Fullbook object but do not directly expose a Jinzhang imprint or target leaf; the seller's Jinzhang-reproduction description therefore remains separate from physical-imprint observation.",
        "Xinyi/Jinyuan modern reformat contents place 論人生時要審的確 at modern page 175, but the body page is not publicly shown. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; Batch 12AE adds zero target-text/Hai votes and changes no 198/166/10/14 accounting or algorithm invariant.",
    ]
    for item in additions:
        if item not in audit["current_focus"]:
            audit["current_focus"].append(item)
    dump(state_path, state)

    matrix_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    row = next(r for r in matrix["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12ae_republic_routes_artifact"] = EVIDENCE_PATH
    row["huiwentang_physical_imprint_direct_reading"] = "上海會文堂書局印行"
    row["huiwentang_target_late_zi_leaf_status"] = "NOT_OBSERVED_IN_PUBLIC_PHOTOS"
    row["jinzhang_shucang_catalog_status"] = "VOLUME_59_REPUBLIC_JINZHANG_LITHOGRAPH_FOUR_JUAN_ONE_VOLUME_START_PAGE_333"
    row["jinzhang_direct_physical_imprint_status_batch_12ae"] = "NOT_OBSERVED_IN_REVIEWED_ARTRON_PHOTOS"
    row["jinyuan_modern_toc_target_page"] = 175
    row["jinyuan_modern_toc_scope"] = "MODERN_REFORMAT_LOCATOR_NOT_HISTORICAL_GLYPH_AUTHORITY"
    row["independent_hai_glyph_witness_count_added_batch_12ae"] = 0
    later = "Batch 12AE: direct Huiwentang physical title photo reads 上海會文堂書局印行; Shucang binds a Republic Jinzhang lithographic Fullbook at volume 59/page 333, while reviewed Artron photos do not directly expose Jinzhang imprint or the late-Zi target leaf. Jinyuan modern TOC locates the target heading at p175 only. Zero target-text/Hai votes."
    if later not in row.get("later_witnesses", []):
        row.setdefault("later_witnesses", []).append(later)
    dump(matrix_path, matrix)

    registry_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    additions_registry = [
        {
            "source_id": HUIWENTANG_SOURCE_ID,
            "title": "Kongfz physical 《紫微斗數全書》 Shanghai Huiwentang copy",
            "historical_period": "REPUBLIC_ERA_OR_REPUBLIC_STYLE_PHYSICAL_COPY_EXACT_PRINT_YEAR_UNRESOLVED",
            "edition": "上海會文堂書局印行 / 石印 / 線裝 / 四冊",
            "provider": "孔夫子旧书网 seller physical-copy listing",
            "url": "https://book.kongfz.com/520108/4153377684/",
            "source_role": "DIRECT_PUBLIC_PHYSICAL_IMPRINT_WITNESS_NOT_TARGET_TEXT_WITNESS",
            "quality_notes": "Source-emitted large photograph directly and visually reads 陳希夷先生著 / 紫微斗數全書 / 上海會文堂書局印行. No OCR used. Public photographs do not expose the late-Zi target leaf.",
            "title_image_sha256": "767f5d01986c8f4a2b655699fce7af50917afd76a34e321ecf8254e6e09a0e9a",
            "direct_target_page_observed": False,
            "independent_witness_increment": 0,
            "research_artifact": EVIDENCE_PATH,
        },
        {
            "source_id": JINZHANG_SOURCE_ID,
            "title": "《重刊術藏》卷59所收民國錦章書局《紫微斗數全書》目錄記錄",
            "historical_period": "MODERN_REPRINT_CATALOG_OF_REPUBLIC_JINZHANG_LITHOGRAPH",
            "edition": "術藏卷59 / 民國錦章書局石印本 / 四卷一冊全 / p333",
            "provider": "白雲深處人家海外站《重刊術藏》目录",
            "url": "https://homeinmists.ilotus.org/",
            "source_role": "BIBLIOGRAPHIC_EDITION_ROUTE_NOT_TARGET_GLYPH_AUTHORITY",
            "quality_notes": "Direct provider catalog page binds title, Republic Jinzhang lithograph, four-juan/one-volume extent and start page 333. No target leaf is exposed on the catalog surface.",
            "shucang_volume": 59,
            "start_page": 333,
            "direct_target_page_observed": False,
            "independent_witness_increment": 0,
            "research_artifact": EVIDENCE_PATH,
        },
        {
            "source_id": JINYUAN_SOURCE_ID,
            "title": "進源版《紫微斗數全書》現代重排公開目錄",
            "historical_period": "2012_2020_MODERN_REFORMAT",
            "edition": "進源書局 / ISBN 9789868759374 / 272 pages",
            "provider": "星易圖書",
            "url": "https://hr.xinyi.hk/goods-5266.html",
            "source_role": "MODERN_SECTION_LOCATOR_NOT_HISTORICAL_GLYPH_AUTHORITY",
            "quality_notes": "Public TOC places 論人生時要審的確 at modern page 175. Public samples show cover/contents only; target body page not observed.",
            "target_heading": "論人生時要審的確",
            "modern_target_page": 175,
            "direct_target_page_observed": False,
            "independent_witness_increment": 0,
            "research_artifact": EVIDENCE_PATH,
        },
    ]
    existing = {s.get("source_id") for s in registry["sources"]}
    for item in additions_registry:
        if item["source_id"] not in existing:
            registry["sources"].append(item)
    dump(registry_path, registry)

    matrix_md_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md"
    matrix_md = matrix_md_path.read_text(encoding="utf-8")
    marker = "### Batch 12AE — Republic Huiwentang physical + Jinzhang catalog routes"
    if marker not in matrix_md:
        matrix_md += "\n\n" + marker + "\n\n- Kongfz source-emitted physical title image directly reads `上海會文堂書局印行`; no target late-Zi leaf is shown.\n- `《重刊術藏》` directly catalogs the Fullbook in volume 59 as a Republic Jinzhang lithograph, four juan in one volume, beginning at p333; this is bibliographic identity only.\n- Artron reviewed physical-set photos do not directly show a Jinzhang imprint or target leaf. Jinyuan's modern TOC locates `論人生時要審的確` at p175 but does not show its body page.\n- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; zero new target-text/Hai votes and no algorithm effect.\n"
        matrix_md_path.write_text(matrix_md, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    summary = f"- **Batch 12AE (Republic Huiwentang/Jinzhang routes):** a Kongfz source-emitted physical title photo directly reads `上海會文堂書局印行`; `《重刊術藏》` binds a Republic Jinzhang lithographic Fullbook to volume 59/page 333; reviewed Artron set photos expose no direct Jinzhang imprint or late-Zi target leaf, and Jinyuan's modern TOC only locates `論人生時要審的確` at p175. Zero target-text/Hai votes; `HPA-ZDATE-006`, 198/166/10/14 and all algorithm invariants remain unchanged. See `{BATCH_DOC}`.\n"
    if "Batch 12AE (Republic Huiwentang/Jinzhang routes)" not in readme:
        readme_path.write_text(readme + "\n" + summary, encoding="utf-8")

    verifier_path = ROOT / "scripts/verify-project-continuity-state-r1.py"
    verifier = verifier_path.read_text(encoding="utf-8")
    anchor = f'ZIWEI_SANFENGE_QUARK_EVIDENCE = ROOT / "docs/research/ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-R1.json"\n'
    if "ZIWEI_REPUBLIC_ROUTES_BATCH" not in verifier:
        if anchor not in verifier:
            raise SystemExit("continuity constant anchor missing")
        verifier = verifier.replace(anchor, anchor + f'ZIWEI_REPUBLIC_ROUTES_BATCH = ROOT / "{BATCH_DOC}"\nZIWEI_REPUBLIC_ROUTES_EVIDENCE = ROOT / "{EVIDENCE_PATH}"\n', 1)

    batch_line = '    "BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD",\n'
    if f'"{BATCH_ID}"' not in verifier:
        if batch_line not in verifier:
            raise SystemExit("continuity batch-list anchor missing")
        verifier = verifier.replace(batch_line, batch_line + f'    "{BATCH_ID}",\n', 1)
    old_latest = 'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD.md"'
    verifier = verifier.replace(old_latest, f'LATEST_BATCH_DOC = "{BATCH_DOC}"', 1)

    load_anchor = '    ziwei_sanfenge_quark_evidence = json.loads(ZIWEI_SANFENGE_QUARK_EVIDENCE.read_text(encoding="utf-8"))\n'
    if "ziwei_republic_routes_evidence =" not in verifier:
        if load_anchor not in verifier:
            raise SystemExit("continuity evidence-load anchor missing")
        verifier = verifier.replace(load_anchor, load_anchor + '    ziwei_republic_routes_evidence = json.loads(ZIWEI_REPUBLIC_ROUTES_EVIDENCE.read_text(encoding="utf-8"))\n', 1)

    source_anchor = '        "EXT-SANFENGE-ZWDSQS-V4-QUARK-PUBLIC-SHARE",\n'
    if HUIWENTANG_SOURCE_ID not in verifier:
        if source_anchor not in verifier:
            raise SystemExit("continuity source anchor missing")
        verifier = verifier.replace(source_anchor, source_anchor + f'        "{HUIWENTANG_SOURCE_ID}",\n        "{JINZHANG_SOURCE_ID}",\n        "{JINYUAN_SOURCE_ID}",\n', 1)

    check_anchor = '    invariants = state.get("invariants", {})\n'
    if "Batch 12AE Republic Huiwentang/Jinzhang routes" not in verifier:
        if check_anchor not in verifier:
            raise SystemExit("continuity check anchor missing")
        check = f'''    # Batch 12AE Republic Huiwentang/Jinzhang routes: edition identity only, zero target votes.\n    if not ZIWEI_REPUBLIC_ROUTES_BATCH.is_file() or not ZIWEI_REPUBLIC_ROUTES_EVIDENCE.is_file():\n        fail("Batch 12AE continuity artifacts missing")\n    if ziwei_republic_routes_evidence.get("batch_id") != "{BATCH_ID}":\n        fail("Batch 12AE evidence identity mismatch")\n    h12ae = ziwei_republic_routes_evidence.get("huiwentang_kongfz", {{}})\n    if h12ae.get("direct_physical_title_image", {{}}).get("sha256") != "767f5d01986c8f4a2b655699fce7af50917afd76a34e321ecf8254e6e09a0e9a":\n        fail("Batch 12AE Huiwentang physical-image binding regressed")\n    if "上海會文堂書局印行" not in h12ae.get("direct_physical_title_image", {{}}).get("direct_no_ocr_reading", []):\n        fail("Batch 12AE Huiwentang imprint reading regressed")\n    j12ae = ziwei_republic_routes_evidence.get("jinzhang_routes", {{}}).get("shucang_catalog", {{}})\n    if j12ae.get("volume") != 59 or j12ae.get("start_page") != 333:\n        fail("Batch 12AE Jinzhang Shucang catalog binding regressed")\n    a12ae = ziwei_republic_routes_evidence.get("adjudication", {{}})\n    if a12ae.get("independent_target_text_witness_increment") != 0 or a12ae.get("independent_hai_glyph_witness_increment") != 0 or a12ae.get("algorithm_reopen_authorized") is not False:\n        fail("Batch 12AE witness/algorithm firewall regressed")\n    row12ae = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)\n    if not row12ae or row12ae.get("huiwentang_physical_imprint_direct_reading") != "上海會文堂書局印行" or row12ae.get("independent_hai_glyph_witness_count_added_batch_12ae") != 0:\n        fail("Batch 12AE Matrix binding regressed")\n\n'''
        verifier = verifier.replace(check_anchor, check + check_anchor, 1)

    verifier_path.write_text(verifier, encoding="utf-8")
    print(BATCH_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
