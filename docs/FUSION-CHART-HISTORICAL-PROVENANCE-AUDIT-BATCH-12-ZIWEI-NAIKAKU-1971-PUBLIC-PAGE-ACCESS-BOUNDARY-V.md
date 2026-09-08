# Fusion Chart Historical Provenance Audit R1 — Batch 12V

## Naikaku 1971 public page-access boundary

Status: **OFFICIAL ITEM API + 405 CONTENT OBJECTS BOUND / ALL TESTED API-EMITTED PAGE JPEG ROUTES RETURN 401 UNAUTHENTICATED / TARGET 15856 → 子060-0001 ENTRY STILL UNRESOLVED / NO WHOLE-CATALOG NEGATIVE / ZERO RULE EFFECT / NO ALGORITHM REOPEN**

Batch 12V follows Batch 12U and tests whether the official 1971 revised-catalog digital object can yield the target entry through normal unauthenticated, first-party routes without login, transmission entitlement, request submission, identifier guessing, or access-control bypass.

### 1. Target-entry search probe

Research run `34230231815` / artifact `10057469073` / ZIP SHA-256 `e900b2242ed74f087761d4b34ebc9ab1d00735b84aeda59b6344ecc38bc841c4` queried the documented NDL Lab page-search API for exact PID `12282052` using:

- `紫微斗數`
- `紫微斗数`
- `紫微`
- `15856`
- `一五八五六`
- `子六十`
- `子060`
- `陳希夷`

All eight documented page-search requests returned HTTP 200 with `hit=0`. This is route evidence only: the NDL Lab corpus/index is separately scoped and the result does **not** prove that the 1971 catalog lacks the target entry.

The documented Lab full-text JSON route returned HTTP 403. The ordinary NDL Digital Collections search URL returned the client application shell without a server-rendered PID/result body, so the initial HTML cannot be used as target-entry evidence.

### 2. Exact item API and content inventory

The exact first-party item API for PID `12282052` returned HTTP 200, 364566 bytes, SHA-256 `0642e44194b40c25380a3a8476d2e92f2b52eb94dcca99d2afb5bc08f91a4a8d`.

It directly binds the already established catalog identity and exposes **405 content/page objects**. The API therefore resolves the digital object's page inventory at metadata level even though the target catalog entry remains unread.

### 3. API-emitted page-route test

Research run `34234090185` / artifact `10059056472` / ZIP SHA-256 `4e174340a0fca80cfb2f0b44d387d18932a0ea2da8abc33695139f051d1cf147` tested only `publicPath` values emitted by that exact item API.

The sample was:

- digital page 1;
- digital page 203;
- digital pages 376–405, covering the final 30 content objects where the National Archives method article says the document-name list is located at the end of the revised catalog.

All **32/32** API-emitted JPEG requests returned HTTP 401 Unauthorized; zero images were obtained.

No hidden identifier was guessed and no authentication/session/token was supplied.

### 4. Epistemic ceiling

The evidence now supports:

```text
1971_REVISED_CATALOG_ITEM_API=PUBLIC_METADATA_READABLE
1971_REVISED_CATALOG_CONTENT_OBJECT_COUNT=405
NDL_LAB_TARGET_QUERY_COUNT=8
NDL_LAB_TARGET_QUERY_HITS=0_EACH
NDL_LAB_FULLTEXT_JSON=HTTP_403
API_EMITTED_PAGE_ROUTE_PROBES=32
API_EMITTED_PAGE_ROUTE_HTTP_401=32
UNAUTHENTICATED_TARGET_ENTRY_IMAGE=NOT_OBSERVED
LEGACY_REGISTRATION_15856_TO_CURRENT_CALL=UNRESOLVED
WHOLE_CATALOG_TARGET_ABSENCE_CLAIM=FORBIDDEN
```

The 401 result closes only the unauthenticated direct-page route tested here. It does not prove that an authorized NDL transmission/viewing session, reading-room route, copy service, or another first-party catalog crosswalk cannot supply the target entry.

### 5. Rule effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
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

The deterministic product remains CLOSED. The next old-number gate is an authorized direct 1971 catalog page/OCR view or another explicit first-party `15856 -> 子060-0001` mapping. In parallel, the higher-value chart-rule research gate remains an independent direct historical `五凶神` physical page.

Machine evidence: `docs/research/ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-R1.json`.
