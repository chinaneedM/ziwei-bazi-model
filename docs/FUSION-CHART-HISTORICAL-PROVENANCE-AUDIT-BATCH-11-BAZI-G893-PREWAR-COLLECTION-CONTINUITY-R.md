# Fusion Chart Historical Provenance & School Audit R1

## Batch 11R - Kyujanggak G893 Prewar Collection Continuity

Status: **COMPLETE FOR COLLECTION-LEVEL CUSTODY AND PREWAR OBJECT-FAMILY WITNESS; EXACT ITEM CONTINUITY TO CURRENT G893 REMAINS OPEN**

Batch ID: `BATCH-11-BAZI-G893-PREWAR-COLLECTION-CONTINUITY-R`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-PREWAR-COLLECTION-CONTINUITY-R1.json`
- `docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json`

This batch addresses a provenance question opened by the G893 image-access work:
whether the early Korean `授時曆立成` now catalogued as `奎貴893 /
GK00893_00` can be traced through the prewar Keijo Imperial University
collection.

It does not read any of the six pending target pages and has no runtime effect.

## 1. Current institutional object remains the controlling endpoint

The live SNU Kyujanggak record identifies:

- title: `授時曆立成`;
- call number: `奎貴893`;
- `BOOK_CD=GK00893_00`;
- attribution: `王恂 等奉勅撰`;
- edition: `甲寅字`;
- date: first half of the fifteenth century / Sejong 1418-1450;
- extent: `1冊(102張)`;
- size: `38×24.8cm`;
- microfilm: `M/F73-102-37-A`.

The exact surviving-copy print year remains unresolved within the provider
range because modern secondary reports disagree between 1434 and 1444.

## 2. Official collection-level custody is continuous

SNU Kyujanggak's official institutional history states that the Kyujanggak
collection was moved to the Keijo Imperial University library in three phases
from 1928 to 1930. It reports 160,561 transferred books, of which 140,913 were
designated as the Kyujanggak collection.

The same official history states that, when Seoul National University was
established in 1946, the Kyujanggak collection previously held at Keijo came
under the SNU Library Annex **without change in the number of volumes or place
of preservation**.

This closes:

```text
KYUJANGGAK_COLLECTION_LEVEL_KEIJO_TO_SNU_CUSTODY=SUPPORTED
```

It does not by itself identify one individual volume.

## 3. Rufus 1936 records a prewar Wang-Xun Shoushi-licheng object family

W. Carl Rufus, `Astronomy in Korea`, published in 1936 in
`Transactions of the Korea Branch of the Royal Asiatic Society`, describes
the Keijo University Library holdings around the Shoushi tradition.

He distinguishes:

1. a later-looking copy of Kang Bo's `授時曆成捷法立成`; and
2. a separate companion volume, described as undated, titled
   `授時曆立成` and credited to Wang Xun.

The report is important because it directly places a Wang-Xun-attributed,
undated Shoushi-licheng object family in the same institutional collection
before World War II.

However, Rufus does not give:

- `奎貴893`;
- `GK00893_00`;
- 102-leaf extent;
- 38×24.8 cm dimensions;
- `M/F73-102-37-A`;
- copy-specific seals, colophon or image.

Therefore:

```text
PREWAR_WANG_XUN_SHOUSHI_LICHENG_OBJECT_FAMILY=SUPPORTED
EXACT_IDENTITY_TO_CURRENT_GK00893_00=UNRESOLVED
```

Same title plus same attribution is not enough to collapse object identity.

## 4. The 1930 numeric-order catalog is the strongest next item-level bridge

The live SNU catalog directly identifies `奎章閣圖書番號順目錄`,
`奎26775-v.1-7`, compiled by the Keijo Imperial University Library in 1930,
and exposes original-image service for it.

This is precisely the type of prewar catalog capable of bridging collection
custody to an individual call number. In the current batch, however, the
internal entry for `授時曆立成` / the identifier corresponding to current
`奎貴893` has **not** been directly read.

Accordingly:

```text
1930_NUMERIC_ORDER_CATALOG=ITEM_LEVEL_LOCATOR
G893_INTERNAL_ENTRY_DIRECTLY_READ=FALSE
UNREAD_CATALOG_AS_ITEM_BINDING=FORBIDDEN
```

## 5. Kang Bo's derived work remains separate

Rufus's own phrasing distinguishes the Kang Bo work from the Wang-Xun
`授時曆立成`; this converges with the independent work-separation evidence
already registered in Batch 11Q.

The historical fact that the two volumes were described as companions does not
authorize textual identity, row-value transfer or copy conflation.

```text
KANG_BO_COMPANION_RELATIONSHIP_AS_TEXTUAL_IDENTITY=FORBIDDEN
```

## 6. Six target controls remain fail-closed

No target page or value is added:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

All remain `PENDING_DIRECT_TARGET_PAGE`.

Collection provenance, even when strong, is not target-glyph authority.

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

1. directly inspect the 1930 `奎章閣圖書番號順目錄` and bind the
   `授時曆立成` entry, old number and any copy-specific metadata;
2. search the 1908, 1912, 1920 and 1940 institutional catalogs for the same
   object and identifier chain;
3. search for prewar photographs, descriptions or microfilm registers matching
   102 leaves, 38×24.8 cm or `M/F73-102-37-A`;
4. continue authorized/public G893 target-page acquisition independently;
5. do not convert collection continuity or same-title attribution into a target
   value, exact print year, or individual-copy identity.
