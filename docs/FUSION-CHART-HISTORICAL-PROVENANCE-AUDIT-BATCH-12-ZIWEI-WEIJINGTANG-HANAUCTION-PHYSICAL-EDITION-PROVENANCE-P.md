# Fusion Chart Historical Provenance Audit R1 — Batch 12P

## Weijingtang / Hanauction physical-edition provenance

Status: **SECONDARY COMMERCIAL PHYSICAL-EDITION LOCATOR BOUND / 味經堂藏板 CLAIM PRESERVED AT AUCTION-DESCRIPTION SCOPE / RENDERED THUMBNAIL BOUND / TARGET PAGE PENDING / ZERO TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

Batch 12P closes the post-12O Hanauction probe as a provenance locator, not as a new textual witness.

## 1. Public auction listing

Hanauction's public historical listing for its 229th auction currently exposes lot 134 on the 2026-04-04 sale:

`134 청판목판본 역학서 味經堂藏板 [신간합병십팔비성자미두수전집(新刻合倂十八飛星紫微斗數全集)] 6卷 6冊 완질(函) ... 2026/04/04`

The successful reproducible capture is workflow run `34214086632`, artifact `10051026199`, artifact ZIP SHA-256 `dcb2935c2d8ec63be385b71468577ed737d41149266c330ad30a6d9373f017df`.

The listing itself therefore binds, at **secondary commercial-auction description scope**:

- visible lot number: `134`;
- stable item object id: `102923`;
- auction id: `260`;
- title: `新刻合倂十八飛星紫微斗數全集`;
- seller/auction description: `청판목판본` / `味經堂藏板`;
- stated extent: `6卷 6冊 완질(函)`;
- auction date: `2026-04-04`.

This does **not** upgrade the seller/auction description into an institutional catalog assertion, nor does it independently date the printing.

## 2. Stable identity versus dynamic URL parameters

The public DOM emitted the same stable object `id=102923 / off_id=260` with different `ac_num` values on successive successful runs: first `120`, later `117`.

Therefore:

```text
STABLE_OBJECT_ID=102923
AUCTION_ID=260
VISIBLE_LOT_NUMBER=134
AC_NUM_AS_BIBLIOGRAPHIC_ID=FORBIDDEN
AC_NUM_STATUS=DYNAMIC_PRESENTATION_PARAMETER
```

An earlier search-engine route carrying `ac_num=297` is explicitly deprecated as canonical identity. The public listing DOM outranks the stale search-engine parameterization.

## 3. Rendered physical-set thumbnail

The exact lot row renders:

`https://www.hanauction.com/shopimage/102923S.JPG`

The workflow downloaded that already-rendered URL only; it did not enumerate or guess larger image filenames.

Machine identity:

```text
DIMENSIONS=114x66
BYTES=7832
SHA256=59973f47a016dc114c967506673b3e053681a6d4a3824ecb8385f7b450fd1385
ARTIFACT_FILE=listing-target-00.jpg
```

Direct visual review without OCR shows a low-resolution photographed multi-volume physical set consistent with the lot listing. The thumbnail is not sufficiently resolved to bind `五凶神`, the late-Zi sentence, or the `亥` glyph.

## 4. Closed-auction detail-page control

The direct detail application currently raises the normal notice `마감된 경매입니다.` (“auction ended”) and then exposes no usable item body in the browser probe.

No authentication, CAPTCHA bypass, hidden route enumeration, guessed image filenames, or anti-bot circumvention was attempted.

This is an access boundary, not evidence that higher-resolution historical photos never existed.

## 5. Authority and stemma boundary

Hanauction is useful here because it locates a photographed physical edition described as `味經堂藏板`. It is **not** equivalent to the Korea University / Hanyang / SNU institutional holdings already bound in prior batches.

Accordingly:

```text
SOURCE_AUTHORITY=SECONDARY_COMMERCIAL_AUCTION_PHYSICAL_EDITION_LOCATOR_NOT_TARGET_TEXT_AUTHORITY
WEIJINGTANG_IMPRINT=AUCTION_DESCRIPTION_BOUND_NOT_INSTITUTIONAL_CATALOG_VERIFIED
QING_EDITION=AUCTION_DESCRIPTION_BOUND_NOT_INDEPENDENTLY_DATED
TEXTUAL_STEMMA_INDEPENDENCE=UNRESOLVED
TARGET_PAGE=PENDING_DIRECT_PAGE
INDEPENDENT_TARGET_TEXT_WITNESS_ADDED=0
INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
```

A physical-edition locator is not a chart-rule candidate. No candidate is created merely because a different imprint label is visible in a sale description.

## 6. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

The next high-value gate is a directly readable `五凶神` page from this 味經堂 physical set, or an institutionally bound equivalent copy that can first be shown to be the same edition family and then collated at page level.

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

Machine evidence: `docs/research/ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json`.

The deterministic fusion-chart product remains CLOSED.
