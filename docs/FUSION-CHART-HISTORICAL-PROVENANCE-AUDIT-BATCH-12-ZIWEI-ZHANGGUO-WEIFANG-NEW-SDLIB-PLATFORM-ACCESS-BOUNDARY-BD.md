# Fusion Chart Historical Provenance Audit R1 — Batch 12BD

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
