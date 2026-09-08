# Fusion Chart Historical Provenance Audit R1 — Batch 12Y

## NCC Jiwen/Dayuan direct public-sample review + Kamo public-route access control

Status: **DIRECT PUBLIC SAMPLE EVIDENCE UPGRADED / JIWEN FACSIMILE NATURE DIRECTLY OBSERVED / DAYUAN HANDWRITTEN COPY-TEXT SAMPLES DIRECTLY BOUND / TARGET PAGE NOT OBSERVED / KAMO RUNNER ROUTES TIMED OUT / ZERO TEXTUAL VOTE / NO ALGORITHM EFFECT**

### 1. Why this batch exists

Batch 12X bound two useful acquisition/collation routes but left an evidentiary distinction open:

- Jiwen's old-print reproduction character still relied materially on reproduction-route wording;
- Dayuan's handwritten copy-text character had direct samples, but the NCC source-emitted sample surface had not yet been separately hardened and reviewed;
- a Kamo Books route had been identified as another public catalog/sample surface but had not been tested at the exact live branch head.

The post-12X commits now close those narrow questions without pretending that the decisive `五凶神` page has been found.

### 2. NCC direct no-OCR visual review

Controlling review artifact:

`docs/research/ZIWEI-NCC-JIWEN-DAYUAN-PUBLIC-SAMPLE-VISUAL-REVIEW-R1.json`

Research run:

- workflow run `34241779981`
- workflow head `5fa32bfb53557f9092322274d41c1a7a99c94fa9`
- artifact `10062285198`
- artifact ZIP SHA-256 `6fd5a1a6c160d93f186aa3a0e1572dd5fd0763ce4a27716ed8673ebf23eb5048`

The review scope is deliberately narrow: only source-emitted images from the NCC `view_img` surfaces were inspected, and the inspection was performed visually without OCR.

#### Jiwen id 995

NCC exposes 11 relevant source-emitted image objects. Direct review of the large samples shows:

- the red Jiwen binding and title `十八飛星策天紫微斗數全集`;
- multiple two-page spreads that visibly reproduce old-print/woodblock-like page layouts;
- no reviewed sample is the `五凶神` target section;
- no reviewed sample exposes the late-Zi target sentence.

Therefore:

```text
JIWEN_FACSIMILE_NATURE=DIRECTLY_OBSERVED
JIWEN_TARGET_PAGE=NOT_OBSERVED_IN_REVIEWED_PUBLIC_SAMPLES
COPY_LEVEL_IDENTITY_TO_SNU_1870=UNRESOLVED
```

This is a real evidence upgrade: facsimile nature no longer needs to be inferred only from sales/reproduction wording. It is not, however, a new textual vote.

#### Dayuan id 7346

NCC likewise exposes 11 relevant source-emitted image objects. Direct review binds:

- modern Dayuan cover/binding and ISBN `9789866171680`;
- handwritten vertical copy-text pages 30–31;
- handwritten text/diagram pages 160–161;
- handwritten vertical copy-text pages 394–395.

None of those samples is the target `五凶神` page, and none exposes the late-Zi sentence.

Therefore:

```text
DAYUAN_COPY_TEXT_NATURE=DIRECTLY_OBSERVED
DAYUAN_TARGET_PAGE=NOT_OBSERVED_IN_REVIEWED_PUBLIC_SAMPLES
DAYUAN_STEMMATIC_RELATION_TO_JIWEN_SNU=UNRESOLVED
```

### 3. Philological firewall remains mandatory

The public directory surface previously recorded in Batch 12X contains `五神 百字千金訣`, while other received routes use `五凶神`.

The new sample review still does not expose the underlying heading page. Therefore:

```text
五神_TO_五凶神_MECHANICAL_EQUIVALENCE=NOT_AUTHORIZED
DIRECT_TARGET_PAGE_REQUIRED=YES
```

No normalization by familiarity, modern edition practice, or expected chapter structure is allowed.

### 4. Kamo public-route control

Exact-head workflow:

- run `34242503503`
- head `822956cdade256edd27df0fe92d656697d52597f`
- artifact `10062627609`
- artifact ZIP SHA-256 `d20f179a18834e7a7d18207df8810c96e9290c5188a5771e62546e89b2426c11`

Tested public routes:

- `https://www.kamo-books.co.jp/4174-03.htm`
- `https://www.kamo-books.co.jp/4174-04.htm`
- `https://www.kamo-books.co.jp/taiwan-sibi.htm`

All three requests timed out in the GitHub runner and zero image objects were obtained.

This result is classified only as:

```text
KAMO_GITHUB_RUNNER_PUBLIC_ROUTE_STATUS=TIMEOUT_ACCESS_BOUNDARY
KAMO_CONTENT_ABSENCE_CLAIM=FORBIDDEN
KAMO_TARGET_PAGE_ABSENCE_CLAIM=FORBIDDEN
```

No login, purchase, identifier guessing, access-control bypass, or hidden-resource enumeration was attempted.

Durable route-control artifact:

`docs/research/ZIWEI-KAMO-4174-03-04-PUBLIC-ROUTE-ACCESS-CONTROL-R1.json`

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

The deterministic product remains CLOSED.

The next high-value gate remains a directly readable volume-four `五凶神` page from Jiwen, Dayuan, SNU, Hanyang, Toyo, or another independently bound physical/copy-text witness.
