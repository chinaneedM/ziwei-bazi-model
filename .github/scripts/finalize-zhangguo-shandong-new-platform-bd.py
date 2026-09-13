#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-SHANDONG-NEW-PLATFORM-MIGRATION-RECHECK-BD"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-SHANDONG-NEW-PLATFORM-MIGRATION-RECHECK-BD.md"
EVIDENCE_PATH = "docs/research/ZIWEI-ZHANGGUO-SHANDONG-NEW-PLATFORM-MIGRATION-RECHECK-R1.json"
STATE_PATH = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
REGISTRY_PATH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
AZ_PATH = ROOT / "docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json"
VERIFIER_PATH = ROOT / "scripts/verify-project-continuity-state-r1.py"

for p in (STATE_PATH, REGISTRY_PATH, AZ_PATH, VERIFIER_PATH):
    if not p.is_file():
        raise SystemExit(f"missing prerequisite: {p}")

az = json.loads(AZ_PATH.read_text(encoding="utf-8"))
if az.get("locator_claim", {}).get("resource_id") != "151613020240003":
    raise SystemExit("AZ Weifang resource-id control changed")

probe = {
    "workflow_run_id": 34645996628,
    "job_id": 103416806990,
    "artifact_id": 10281512891,
    "artifact_name": "sdlib-new-platform-public-contract-probe",
    "artifact_digest": "sha256:a928ebde2ca48e6c38e32355b4abc943bbe63798e2688129c0a1828fee5c6c7a",
    "head_sha": "010db0ac000e8a57a7f3c99fe9e2f912c05d8c2d",
    "runner_region": "westus2",
    "roots_tested": [
        "https://guji.sdlib.cn/",
        "https://guji.sdlib.cn/gujih5/"
    ],
    "root_success_count": 0,
    "js_asset_count": 0,
    "candidate_literal_count": 0,
    "target_literal_hit_count": 0,
    "result": "BOTH_PUBLIC_NEW_PLATFORM_ROOTS_CONNECTION_TIMEOUT_BEFORE_HTML_OR_JS_CONTRACT_OBTAINED",
    "policy": "SOURCE_EMITTED_CONTRACT_ONLY_NO_GUESSED_API_CALLS_NO_LOGIN_NO_AUTH_BYPASS"
}

evidence = {
    "schema": "ZIWEI-ZHANGGUO-SHANDONG-NEW-PLATFORM-MIGRATION-RECHECK-R1",
    "batch_id": BATCH_ID,
    "question": "Does the current guji.sdlib.cn public surface remove Batch 12AZ's old Shandong route boundary enough to bind Weifang resource 151613020240003 to first-party object metadata or page bytes?",
    "prior_az_control": {
        "resource_id": "151613020240003",
        "title": "新編評註通玄先生張果星宗大全",
        "locator_edition_claim": "明萬曆二十二年(1594)唐謙刻本",
        "locator_holding_claim": "濰坊市圖書館藏",
        "authority_scope": "LOCATOR_ONLY_PENDING_FIRST_PARTY_SHANDONG_OBJECT_BINDING"
    },
    "new_platform_probe": probe,
    "adjudication": {
        "new_platform_root_reachable_from_reviewed_runner": False,
        "source_emitted_frontend_contract_obtained": False,
        "first_party_target_object_metadata_obtained": False,
        "first_party_target_page_bytes_obtained": False,
        "target_leaf_obtained": False,
        "direct_glyph_collation_authorized": False,
        "resource_gone_claim_authorized": False,
        "no_digitization_claim_authorized": False,
        "whole_holding_text_negative_authorized": False,
        "independent_exact_1594_material_witness_increment": 0,
        "independent_target_text_witness_increment": 0,
        "independent_hai_glyph_witness_increment": 0,
        "interpretation": "The current .cn roots time out from the reviewed GitHub runner before any HTML or source-emitted API contract is obtained. This extends the execution-environment/public-route boundary; it does not prove object absence or textual absence."
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
        "algorithm_reopen": False
    }
}
(ROOT / EVIDENCE_PATH).write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Append the new-platform recheck to the durable AZ machine evidence without rewriting its original controls.
az["new_platform_migration_recheck_batch_12bd"] = probe | {
    "first_party_target_object_metadata_obtained": False,
    "first_party_target_page_bytes_obtained": False,
    "witness_vote_increment": 0,
    "scope": "EXECUTION_ENVIRONMENT_PUBLIC_ROUTE_BOUNDARY_ONLY"
}
AZ_PATH.write_text(json.dumps(az, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

batch_doc = """# Fusion Chart Historical Provenance Audit R1 — Batch 12BD

## 《張果星宗大全》山东古籍新版平台迁移重试与潍坊 1594 路由边界复核

Status: **CURRENT G U J I.SDLIB.CN ROOTS PROBED / BOTH ROOTS TIME OUT FROM REVIEWED GITHUB RUNNER / NO HTML OR SOURCE-EMITTED API CONTRACT OBTAINED / WEIFANG 151613020240003 REMAINS LOCATOR-ONLY / NO FIRST-PARTY OBJECT METADATA OR PAGE BYTES / NO TARGET LEAF / ZERO NEW 1594, TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Question

Batch 12AZ tested the then-reviewed Shandong routes and found cross-runner timeout boundaries. A current public platform route under `guji.sdlib.cn` later became the obvious recheck target. BD asks only:

> Can the current `.cn` public surface be reached from the controlled runner, and can its own emitted frontend contract bind Weifang resource `151613020240003` to first-party metadata or page bytes?

## 2. Prior locator remains unchanged

The retained research locator is:

```text
resource_id=151613020240003
title=新編評註通玄先生張果星宗大全
locator edition claim=明萬曆二十二年(1594)唐謙刻本
locator holding claim=濰坊市圖書館藏
```

As in AZ, those edition/holding fields remain locator-scoped until a Shandong first-party object response is actually obtained.

## 3. New-platform contract probe

Controlling run:

```text
workflow_run_id=34645996628
job_id=103416806990
head_sha=010db0ac000e8a57a7f3c99fe9e2f912c05d8c2d
runner region=westus2
artifact_id=10281512891
artifact_digest=sha256:a928ebde2ca48e6c38e32355b4abc943bbe63798e2688129c0a1828fee5c6c7a
```

Only two public roots were requested:

```text
https://guji.sdlib.cn/
https://guji.sdlib.cn/gujih5/
```

Both timed out before any response body was obtained. Consequently:

```text
ROOT_SUCCESS_COUNT=0
JS_ASSET_COUNT=0
SOURCE_EMITTED_API_LITERAL_COUNT=0
TARGET_LITERAL_HIT_COUNT=0
```

The probe deliberately stopped there. It did not invent endpoint paths from the old platform, guess hidden APIs, log in, replay credentials, or attempt any access-control bypass.

## 4. Adjudication

The `.cn` platform recheck does **not** close AZ's object-binding gate:

```text
FIRST_PARTY_TARGET_OBJECT_METADATA_OBTAINED=false
FIRST_PARTY_TARGET_PAGE_BYTES_OBTAINED=false
TARGET_LEAF_OBTAINED=false
DIRECT_GLYPH_COLLATION_AUTHORIZED=false
```

The timeout also does **not** authorize:

```text
RESOURCE_GONE=true
NO_DIGITIZATION=true
PHYSICAL_HOLDING_ABSENT=true
TARGET_PASSAGE_ABSENT=true
```

It is an execution-environment/public-route reachability boundary only.

## 5. Witness accounting

```text
INDEPENDENT_EXACT_1594_MATERIAL_WITNESS_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

The 1594 NIJL/Tohoku physical page from Batch 12AW remains the controlling directly read early witness. The Weifang record remains a high-value acquisition locator, not a counted witness.

## 6. Effect on product and algorithm state

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No deterministic chart behavior changes are authorized.

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

## 8. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-SHANDONG-NEW-PLATFORM-MIGRATION-RECHECK-R1.json
```

## 9. Next gate

1. Do not repeat GitHub-runner probes against the same `.cn` roots without a material network/platform change.
2. Continue first-party item-level research for another exact 1593/1594 holding whose catalog or image service is reachable from the current environment.
3. If Weifang `151613020240003` becomes reachable through a source-emitted route, bind bibliographic metadata first, then acquire and visually collate the target leaf before adding any witness vote.
4. Fudan `rb2314` remains an external-action boundary for appointment/reproduction inquiry and requires explicit user authorization before submitting anything.
"""
(ROOT / BATCH_DOC).write_text(batch_doc, encoding="utf-8")

registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
source = next((s for s in registry.get("sources", []) if s.get("source_id") == "EXT-ZIWEI-ZHANGGUO-WEIFANG-1594-LOCATOR"), None)
if source is None:
    raise SystemExit("Weifang source registry entry missing")
source["batch_12bd_new_platform_recheck"] = {
    "current_public_roots_tested": probe["roots_tested"],
    "workflow_run_id": probe["workflow_run_id"],
    "artifact_id": probe["artifact_id"],
    "artifact_digest": probe["artifact_digest"],
    "result": probe["result"],
    "first_party_target_object_bound": False,
    "target_page_bytes_obtained": False,
    "witness_vote_increment": 0,
    "scope": "PUBLIC_ROUTE_REACHABILITY_BOUNDARY_ONLY"
}
REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
if state.get("schema_version") != "1.62.0":
    raise SystemExit(f"unexpected state schema before BD: {state.get('schema_version')}")
audit = state["historical_audit"]
if audit.get("completed_batches", [])[-1] != "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC":
    raise SystemExit("BC is not current completed-batch tail")
if BATCH_ID in audit["completed_batches"]:
    raise SystemExit("BD already registered")
state["schema_version"] = "1.63.0"
audit["completed_batches"].append(BATCH_ID)
audit["latest_batch_doc"] = BATCH_DOC
audit["current_focus"].append(
    "Batch 12BD rechecks the current guji.sdlib.cn public roots for Weifang locator 151613020240003. Workflow 34645996628 / artifact 10281512891 timed out on both root and /gujih5/ before HTML or source-emitted API contracts were obtained; this extends only the execution-environment/public-route boundary. The Weifang 1594/Tang-Qian claim remains locator-scoped, adds zero material/text/Hai-glyph votes, and HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen."
)
state["updated_at"] = "2026-09-13"
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Keep the continuity verifier exact about zero-row-effect supplemental batches.
text = VERIFIER_PATH.read_text(encoding="utf-8")
old_tail = '    "BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB",\n    "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC",\n]'
new_tail = '    "BATCH-12-ZIWEI-ZHANGGUO-FUDAN-MING-WANLI-HOLDING-RECONCILIATION-BB",\n    "BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC",\n    "' + BATCH_ID + '",\n]'
if old_tail not in text:
    raise SystemExit("continuity supplemental tail anchor missing")
text = text.replace(old_tail, new_tail, 1)
old_doc = 'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-TOHOKU-NACSIS-FUDAN-ACCESS-DEDUP-BC.md"'
new_doc = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
if old_doc not in text:
    raise SystemExit("continuity latest-doc anchor missing")
text = text.replace(old_doc, new_doc, 1)
VERIFIER_PATH.write_text(text, encoding="utf-8")

print("Batch 12BD semantic files prepared")
