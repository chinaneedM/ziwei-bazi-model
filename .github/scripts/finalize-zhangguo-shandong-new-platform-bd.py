#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-BD.md"
EVIDENCE_PATH = "docs/research/ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-R1.json"
AZ_PATH = ROOT / "docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json"
STATE_PATH = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
REGISTRY_PATH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
VERIFIER_PATH = ROOT / "scripts/verify-project-continuity-state-r1.py"

for p in (AZ_PATH, STATE_PATH, REGISTRY_PATH, VERIFIER_PATH):
    if not p.is_file():
        raise SystemExit(f"missing prerequisite: {p}")

az = json.loads(AZ_PATH.read_text(encoding="utf-8"))
packed_az = json.dumps(az, ensure_ascii=False)
for marker in ("151613020240003", "濰坊市圖書館", "萬曆二十二", "唐謙"):
    if marker not in packed_az:
        raise SystemExit(f"AZ prerequisite marker missing: {marker}")

probes = {
    "contract_probe": {
        "workflow_run_id": 34645996628,
        "job_id": 103416806990,
        "head_sha": "010db0ac000e8a57a7f3c99fe9e2f912c05d8c2d",
        "artifact_id": 10281512891,
        "artifact_name": "sdlib-new-platform-public-contract-probe",
        "artifact_zip_sha256": "a928ebde2ca48e6c38e32355b4abc943bbe63798e2688129c0a1828fee5c6c7a",
        "root_results": {
            "https://guji.sdlib.cn/": "URLError: <urlopen error timed out>",
            "https://guji.sdlib.cn/gujih5/": "URLError: <urlopen error timed out>"
        },
        "root_success_count": 0,
        "js_asset_count": 0,
        "candidate_literal_count": 0,
        "target_literal_hit_count": 0
    },
    "cross_egress_probe": {
        "workflow_run_id": 34646138731,
        "head_sha": "256c6821cf1c61b8678ea5eb685c3ece6d018f3a",
        "dns": {"host": "guji.sdlib.cn", "address": "58.59.15.30"},
        "jobs": [
            {
                "os": "Linux", "azure_region": "eastus", "job_id": 103417271132,
                "artifact_id": 10281888731,
                "artifact_zip_sha256": "070d95a0c6e9b3d10806ed0040c0fae5869c989c7c3551b2a4c731a68c07ee57",
                "tcp_443": "TIMEOUT", "tcp_80": "TIMEOUT", "tls_reached": False,
                "https_root": "TIMEOUT", "https_mobile": "TIMEOUT", "http_root": "TIMEOUT"
            },
            {
                "os": "Windows", "azure_region": "westus2", "job_id": 103417270900,
                "artifact_id": 10281619241,
                "artifact_zip_sha256": "f3a59f2a36d936f696b26526599d88a27b7dae2d2f56fa87c8e7b2d341916d68",
                "tcp_443": "TIMEOUT", "tcp_80": "TIMEOUT", "tls_reached": False,
                "https_root": "TIMEOUT", "https_mobile": "TIMEOUT", "http_root": "TIMEOUT"
            },
            {
                "os": "macOS", "azure_region": "westus", "job_id": 103417271136,
                "artifact_id": 10282178367,
                "artifact_zip_sha256": "f0fb18d3e93e0840674deec8979bee9fadb2835003463d763855ee1a569d9837",
                "tcp_443": "TIMEOUT", "tcp_80": "TIMEOUT", "tls_reached": False,
                "https_root": "TIMEOUT", "https_mobile": "TIMEOUT", "http_root": "TIMEOUT"
            }
        ],
        "all_reviewed_egresses_dns_resolved_same_ipv4": True,
        "all_reviewed_egresses_tcp_80_443_timed_out": True,
        "http_or_tls_layer_reached": False
    }
}

evidence = {
    "schema": "ZIWEI-ZHANGGUO-WEIFANG-NEW-SDLIB-PLATFORM-ACCESS-BOUNDARY-R1",
    "batch_id": BATCH_ID,
    "question": "Does the 2026 replacement Shandong Ancient Books digital platform now expose first-party object bytes or metadata for the high-value Weifang Wanli-22 / 1594 locator 151613020240003?",
    "target_locator": {
        "resource_id": "151613020240003",
        "title": "新編評註通玄先生張果星宗大全",
        "secondary_edition_claim": "明萬曆二十二年(1594)唐謙刻本",
        "secondary_holding_claim": "濰坊市圖書館",
        "locator_status": "HIGH_VALUE_SECONDARY_LOCATOR_NOT_FIRST_PARTY_OBJECT_BINDING"
    },
    "platform_migration_context": {
        "new_desktop_url": "https://guji.sdlib.cn/",
        "new_mobile_url": "https://guji.sdlib.cn/gujih5/",
        "public_announcement_report_url": "https://news.iqilu.com/shandong/shandonggedi/20260828/5940003.shtml",
        "report_date": "2026-08-28",
        "reported_builder": "山东省图书馆（山东省古籍保护中心）",
        "reported_scope": "新版整合18家公藏单位，古籍全文资源587部、5834册；支持聚合检索、纯影像/图文对照和全文穿透检索",
        "relation_to_batch_12az": "CURRENT_PUBLIC_PLATFORM_ENTRY_SUPERSEDES_OLD_SDLIB_COM_ENTRY_FOR_NEW_ACCESS_ATTEMPTS; AZ'S OLD-ROUTE RESULTS REMAIN HISTORICAL_EXECUTION_EVIDENCE"
    },
    "execution_evidence": probes,
    "access_adjudication": {
        "new_platform_hostname_dns_resolved": True,
        "resolved_ipv4": "58.59.15.30",
        "reviewed_runner_egress_count": 3,
        "reviewed_os": ["Linux", "Windows", "macOS"],
        "reviewed_azure_regions": ["eastus", "westus2", "westus"],
        "tcp_80_or_443_connection_obtained": False,
        "tls_handshake_obtained": False,
        "http_response_obtained": False,
        "first_party_frontend_bytes_obtained": False,
        "first_party_api_contract_recovered": False,
        "first_party_target_catalog_record_obtained": False,
        "first_party_target_image_or_page_bytes_obtained": False,
        "target_leaf_obtained": False,
        "boundary_class": "REVIEWED_GITHUB_MULTI_REGION_EGRESS_TCP_TIMEOUT_BEFORE_TLS_HTTP",
        "site_down_claim_authorized": False,
        "resource_gone_claim_authorized": False,
        "no_holding_inference_authorized": True,
        "no_digitization_inference_authorized": True,
        "whole_holding_text_negative_authorized": False
    },
    "witness_accounting": {
        "independent_exact_1594_material_witness_increment": 0,
        "independent_target_text_witness_increment": 0,
        "independent_hai_glyph_witness_increment": 0,
        "locator_strength_change": "CURRENT_PLATFORM_ENTRY_IDENTIFIED_AND_NETWORK_BOUNDARY_NARROWED; NO_ITEM_PROMOTION"
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

batch_doc = """# Fusion Chart Historical Provenance Audit R1 — Batch 12BD

## 《張果星宗大全》潍坊 1594 线索：山东古籍新版平台迁移与三出口 TCP 访问边界校勘

Status: **2026 NEW SHANDONG PLATFORM ENTRY IDENTIFIED / AZ OLD-ROUTE ACCESS CONTEXT SUPERSEDED FOR CURRENT ATTEMPTS / GUJI.SDLIB.CN DNS RESOLVES / LINUX+WINDOWS+MACOS THREE-REGION TCP 80/443 TIMEOUT / NO TLS OR HTTP RESPONSE / NO FIRST-PARTY FRONTEND OR TARGET OBJECT BYTES / WEIFANG 151613020240003 REMAINS HIGH-VALUE LOCATOR ONLY / ZERO NEW EXACT-1594 MATERIAL WITNESS / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12AZ audited the then-known Shandong/Weifang public routes for locator `151613020240003` and found only cross-egress timeouts. In August 2026, public institutional reporting announced a **new** Shandong Ancient Books Digital Resources Platform at `https://guji.sdlib.cn` with mobile entry `https://guji.sdlib.cn/gujih5/`.

Because the platform entry changed after AZ, BD reopens **only the access layer**. It does not reopen any deterministic chart algorithm.

## 2. Current platform migration context

A 2026-08-28 public report states that the new platform is built by 山东省图书馆（山东省古籍保护中心）, aggregates participating institutions, and supports unified retrieval, pure-image reading, image/text comparison, and full-text search.

Current advertised entries:

```text
PC=https://guji.sdlib.cn/
mobile=https://guji.sdlib.cn/gujih5/
```

This supersedes the old `guji.sdlib.com` entry **for current access attempts**. It does not retroactively invalidate AZ's historical execution evidence.

## 3. Target locator remains unchanged

```text
resource id=151613020240003
title=新編評註通玄先生張果星宗大全
secondary edition claim=明萬曆二十二年(1594)唐謙刻本
secondary holding claim=濰坊市圖書館
```

Those exact-year/imprint/holding fields remain locator evidence until a first-party target object or item record is obtained.

## 4. New-domain public contract probe

Workflow run `34645996628`, job `103416806990`, attempted only the public root/mobile entries and source-emitted frontend assets. No guessed API path, login, authentication bypass, or hidden identifier enumeration was used.

Result:

```text
https://guji.sdlib.cn/        -> connection timeout
https://guji.sdlib.cn/gujih5/ -> connection timeout
root_success_count=0
js_asset_count=0
candidate_api_literal_count=0
```

Artifact:

```text
id=10281512891
sha256=a928ebde2ca48e6c38e32355b4abc943bbe63798e2688129c0a1828fee5c6c7a
```

Because no root bytes were obtained, absence of source-emitted API literals is not evidence that the platform has no API.

## 5. Three-OS / three-region network-layer adjudication

A second workflow (`34646138731`) tested DNS, TCP 80/443, TLS and HTTP from three hosted-runner egresses.

All three independently resolve:

```text
guji.sdlib.cn -> 58.59.15.30
```

Observed results:

```text
Linux / eastus   : TCP 443 timeout; TCP 80 timeout; no TLS; HTTP/HTTPS timeout
Windows / westus2: TCP 443 timeout; TCP 80 timeout; no TLS; HTTP/HTTPS timeout
macOS / westus   : TCP 443 timeout; TCP 80 timeout; no TLS; HTTP/HTTPS timeout
```

Artifacts:

```text
Linux  10281888731  sha256=070d95a0c6e9b3d10806ed0040c0fae5869c989c7c3551b2a4c731a68c07ee57
Windows 10281619241 sha256=f3a59f2a36d936f696b26526599d88a27b7dae2d2f56fa87c8e7b2d341916d68
macOS   10282178367  sha256=f0fb18d3e93e0840674deec8979bee9fadb2835003463d763855ee1a569d9837
```

The reviewed failure occurs **before TLS and HTTP**. Therefore it cannot be attributed to a wrong frontend route, JavaScript parsing, HTTP status, or target query parameter.

## 6. Evidence firewall

BD authorizes only:

```text
CURRENT_GITHUB_RUNNER_ACCESS_BOUNDARY=TCP_TIMEOUT_BEFORE_TLS_HTTP
FIRST_PARTY_TARGET_OBJECT_BOUND=false
FIRST_PARTY_TARGET_PAGE_BYTES_OBTAINED=false
```

BD explicitly does **not** authorize:

```text
SITE_IS_DOWN
TARGET_NOT_HELD
TARGET_NOT_DIGITIZED
RESOURCE_GONE
WHOLE_HOLDING_TEXT_NEGATIVE
```

A multi-region GitHub egress boundary is not bibliographic absence.

## 7. Witness accounting

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

The Weifang locator remains high-value because it is edition-specific and institution-specific, but it still supplies no independently reviewed target leaf.

## 8. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

The missing mechanical bridge `upper/night Zi -> Hai branch` remains unproven.

## 9. Accounting

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

## 10. Next gate

1. Do not keep blind-retrying guessed Shandong endpoints from the same hosted-runner class. Retry only when a materially different access path exists (for example, a browser-visible public object, another institution's first-party catalog crosswalk, or user-authorized local/manual access evidence).
2. Continue looking for a genuinely independent first-party exact-1593/1594 item record or publicly obtainable target leaf outside the already deduplicated NIJL/Tohoku lineage.
3. Fudan `rb2314` remains a user-authorization boundary for target-specific appointment/reproduction inquiry.
4. Keep HPA-ZDATE-006 unresolved until direct historical rule evidence supplies the missing upper/night-Zi -> Hai mapping.
"""
(ROOT / BATCH_DOC).write_text(batch_doc, encoding="utf-8")

registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
sources = registry.get("sources", [])
weifang = next((s for s in sources if s.get("source_id") == "EXT-ZIWEI-ZHANGGUO-WEIFANG-1594-LOCATOR"), None)
if not weifang:
    raise SystemExit("Weifang source registry entry missing")
weifang["current_platform_access_control"] = {
    "batch_id": BATCH_ID,
    "new_desktop_url": "https://guji.sdlib.cn/",
    "new_mobile_url": "https://guji.sdlib.cn/gujih5/",
    "dns_ipv4": "58.59.15.30",
    "reviewed_runner_egresses": ["Linux/eastus", "Windows/westus2", "macOS/westus"],
    "tcp_80_443_result": "TIMEOUT_ACROSS_ALL_REVIEWED_EGRESSES",
    "tls_or_http_reached": False,
    "first_party_target_object_bound": False,
    "target_leaf_obtained": False,
    "site_down_claim_authorized": False,
    "resource_gone_claim_authorized": False,
    "no_holding_or_digitization_inference_authorized": True,
    "independent_witness_increment": 0,
    "research_artifact": EVIDENCE_PATH
}
weifang["url"] = "https://guji.sdlib.cn/"
weifang["provider"] = "Shandong Ancient Books / Weifang Library locator ecosystem; current official platform entry identified but first-party target object remains unreachable from reviewed GitHub egresses"
weifang["quality_notes"] = "High-value 1594 Weifang locator only. Batch 12AZ audited obsolete/older public routes; Batch 12BD re-audits the 2026 replacement guji.sdlib.cn entry. DNS resolves to 58.59.15.30, but Linux/eastus, Windows/westus2 and macOS/westus all time out at TCP 80/443 before TLS/HTTP. No first-party target bytes were obtained. This is an execution-egress boundary, not evidence of no holding, no digitization, or resource disappearance; zero witness/glyph increment."
registry["access_date"] = "2026-09-12"
REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
if state.get("schema_version") != "1.62.0":
    raise SystemExit(f"unexpected state schema before BD: {state.get('schema_version')}")
hist = state.get("historical_audit", {})
if not str(hist.get("latest_batch_doc", "")).endswith("TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC.md"):
    raise SystemExit("BD expected BC as latest batch")
completed = hist.setdefault("completed_batches", [])
if BATCH_ID not in completed:
    completed.append(BATCH_ID)
hist["latest_batch_doc"] = BATCH_DOC
for item in [
    "Batch 12BD reopens only the Shandong access layer after the 2026 replacement platform entry guji.sdlib.cn superseded the old sdlib.com route for current attempts; the high-value Weifang locator remains resource ID 151613020240003 with a secondary Wanli-22/1594 Tang-Qian/Weifang holding claim.",
    "Batch 12BD resolves guji.sdlib.cn to 58.59.15.30, but Linux/eastus, Windows/westus2 and macOS/westus hosted runners all time out on TCP 80 and 443 before TLS/HTTP. No first-party frontend, API contract, target catalog item or page bytes were obtained; this multi-region GitHub egress boundary authorizes no site-down, no-holding, no-digitization or resource-gone inference.",
    "Batch 12BD adds zero exact-1594 material witness, target-text or Hai-glyph votes. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; deterministic product CLOSED, algorithm defect count 0, reopen count 0 and candidate collapse count 0 remain unchanged."
]:
    if item not in hist.setdefault("current_focus", []):
        hist["current_focus"].append(item)
state["schema_version"] = "1.63.0"
state["updated_at"] = "2026-09-12"
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

ver = VERIFIER_PATH.read_text(encoding="utf-8")
old_tail = '    "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC",\n]'
new_tail = '    "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC",\n    "' + BATCH_ID + '",\n]'
if old_tail not in ver:
    raise SystemExit("continuity supplemental tail anchor missing")
ver = ver.replace(old_tail, new_tail, 1)
old_doc = 'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC.md"'
new_doc = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
if old_doc not in ver:
    raise SystemExit("continuity latest-doc anchor missing")
ver = ver.replace(old_doc, new_doc, 1)
VERIFIER_PATH.write_text(ver, encoding="utf-8")

print("Batch 12BD semantic files prepared")
