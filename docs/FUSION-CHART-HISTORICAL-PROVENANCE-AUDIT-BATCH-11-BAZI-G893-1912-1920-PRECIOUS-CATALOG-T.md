# Fusion Chart Historical Provenance & School Audit R1

## Batch 11T - G893 and the 1912-1920 Kyujanggak Precious-Book Catalog

Status: **COMPLETE FOR DIRECT NO-OCR FULL-OBJECT TITLE-PRESENCE REVIEW; NEGATIVE CATALOG WITNESS ONLY**

Batch ID: `BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-1912-1920-PRECIOUS-CATALOG-R1.json`

This batch closes the next catalog control opened by Batch 11S. It asks only whether the surviving Kyujanggak composite catalog object dated by the provider to `[1912-1920]` visibly contains `授時曆立成` or the shortened title `授時曆`.

It does not inspect a G893 computational target page and has no runtime effect.

## 1. Official provider object and dating scope

The provider object is:

- title: `貴重圖書目錄`;
- compiler: `朝鮮總督府 編`;
- catalog identifier: `奎26787`;
- `BOOK_CD=GK26787_00`;
- `ITEM_CD=BBG`;
- provider date: `[1912-1920]`;
- extent: `1冊(72張)`;
- edition: `筆寫本`;
- size: `27.8×20cm`;
- microfilm: `M/F82-16-42-A`.

The provider describes this as a bound composite of eight documents concerning precious books, specially handled books and a Tang-print subcatalog. Therefore the provider range `[1912-1920]` applies to the composite object and must not be collapsed into a single year for every internal document.

```text
PROVIDER_DATE_RANGE_AS_SINGLE_YEAR=FORBIDDEN
INTERNAL_DOCUMENT_DATE_WITHOUT_DIRECT_INTERNAL_DATING=UNRESOLVED
```

## 2. Full renderer-object review was completed without OCR

The project directly bound the official detail page and renderer manifest, then retrieved every provider renderer page `0001` through `0075`.

Recorded acquisition controls:

- detail-page workflow `34034296218`, artifact `9989648339`;
- renderer-manifest workflow `34034482284`, artifact `9989711290`;
- page `0001` workflow `34034687434`, artifact `9989777921`;
- pages `0002-0050` workflow `34034955051`, 49 artifacts;
- pages `0051-0075` workflow `34037480798`, 25 artifacts.

Coverage validation records:

```text
EXPECTED_PAGE_IDS=0001-0075
VALID_IMAGE_COUNT=75
MISSING_PAGE_COUNT=0
OCR_USED_TRUE_COUNT=0
ALL_PAGES_VALID_IMAGE=TRUE
ALL_PAGES_OCR_FALSE=TRUE
```

The review therefore covers the complete provider renderer object rather than a guessed section or OCR search result.

## 3. Direct title-presence result

Direct visual review of all 75 renderer pages found no visible:

- `授時曆立成`; or
- shortened `授時曆`.

The machine result is:

```text
1912_1920_COMPOSITE_CATALOG_授時曆立成_VISIBLE=FALSE
1912_1920_COMPOSITE_CATALOG_授時曆_VISIBLE=FALSE
REVIEW_MODE=DIRECT_NATIVE_IMAGE_VISUAL_REVIEW_NO_OCR
```

This is a negative title-presence witness for the surviving provider-dated composite catalog object only.

## 4. Epistemic boundaries

The negative result does **not** prove:

- physical absence of G893 from Kyujanggak during 1912-1920;
- absence of the same physical book under another title, handling class or identifier;
- discontinuity between a prewar Wang-Xun `授時曆立成` and current `奎貴893 / GK00893_00`;
- any exact date for the current surviving copy;
- any target folio, glyph or numerical value.

Accordingly:

```text
NEGATIVE_CATALOG_WITNESS_AS_PHYSICAL_ABSENCE=FORBIDDEN
CURRENT_PRECIOUS_STATUS_BACKPROJECTION=FORBIDDEN
NEGATIVE_CATALOG_WITNESS_AS_EXACT_ITEM_IDENTITY=FORBIDDEN
NEGATIVE_CATALOG_WITNESS_AS_PRINT_YEAR_EVIDENCE=FORBIDDEN
NEGATIVE_CATALOG_WITNESS_AS_TARGET_VALUE_EVIDENCE=FORBIDDEN
SOURCE_COUNT_VOTING=FORBIDDEN
```

## 5. Prewar continuity bracket after Batch 11T

The supported sequence is now:

1. 1908 `貴重圖書目錄`: target title not visibly seen in the complete bounded 子部 review;
2. provider-dated `[1912-1920]` composite `貴重圖書目錄` (`奎26787 / GK26787_00`): target title not visibly seen anywhere in the complete 75-page renderer object;
3. 1928-1930: official collection transfer to Keijo Imperial University;
4. 1936: Rufus reports an undated Wang-Xun-attributed `授時曆立成` in Keijo University Library;
5. 1946: the former Keijo Kyujanggak collection passes to SNU without a volume-count or place-of-preservation change in the official institutional history;
6. current provider: `奎貴893 / GK00893_00`, Wang-Xun-attributed, 102 leaves.

This narrows the catalog history but does not close individual-copy identity:

```text
EXACT_ITEM_CONTINUITY_TO_CURRENT_GK00893_00=UNRESOLVED
```

The 1930 numeric-order catalog remains the highest-value item-level control because it can potentially bind an older numeric identifier directly to a title or copy-specific record.

## 6. Six G893 numerical controls remain fail-closed

No target-page value is added for:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

All remain `PENDING_DIRECT_TARGET_PAGE`.

## 7. Runtime and audit-count consequence

None.

```text
HISTORICAL_PROVENANCE_ROW_COUNT=197
AUDITED_ROW_COUNT=165
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 8. Next work

1. directly read the 1930 京城帝國大學附屬圖書館 `奎章閣圖書番號順目錄` (`奎26775-v.1-7`) internal entry for `授時曆立成` or a copy-specific identifier;
2. inspect 1940 or other prewar catalog controls where they can bind an identifier rather than merely establish title presence;
3. search prewar photograph, microfilm or physical-description records matching `102張`, `38×24.8cm`, `M/F73-102-37-A` or equivalent copy-specific evidence;
4. continue independent acquisition of the six G893 target pages without importing values from Goryeosa, Ming, Ogawa, G894, Sillok or Kang Bo.
