# Fusion Chart Historical Provenance & School Audit R1

## Batch 11U - G893 1940 Kyujanggak Precious-Book Identifier Binding

Status: **COMPLETE FOR DIRECT NO-OCR CATALOG-ITEM IDENTIFIER CONTINUITY; SIX TARGET VALUES REMAIN FAIL-CLOSED**

Batch ID: `BATCH-11-BAZI-G893-1940-PRECIOUS-CATALOG-U`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-1940-PRECIOUS-CATALOG-IDENTIFIER-BINDING-R1.json`

This batch closes the item-level continuity question left open by Batches 11R-11T. It does not inspect any G893 computational target folio and has no runtime effect.

## 1. Official 1940 provider object

The official Kyujanggak object is:

- title: `奎章閣貴重圖書關係書類`;
- compiler: `京城帝國大學`;
- year: `1940`;
- catalog identifier: `奎26786`;
- `BOOK_CD=GK26786_00`;
- `ITEM_CD=BBG`;
- one renderer volume;
- renderer pages `0001-0148`;
- direct native-image access;
- OCR not used.

The object was directly bound through the live provider detail/renderer surface.

## 2. The internal table defines the number field explicitly

Provider page `0125` directly shows the internal catalog heading:

- `奎章閣貴重圖書目錄`;
- section `朝鮮本（一）`;
- revision note `昭和十五年八月改訂`;
- field headers `書名`, `圖書番號`, `冊數`, `備考`.

Therefore the numbers on the subsequent table pages are not inferred call numbers or page sequence numbers. They are explicitly labeled `圖書番號`.

Direct page controls:

- page `0125` image SHA-256: `bdb4afa606130e8f2aeb6cc733e756fbb5a3818e828292a23c597c00323cb02f`;
- review mode: direct native-image visual review, no OCR.

## 3. Page 0129 directly binds 授時曆立成 to 圖書番號 893

Provider page `0129` directly shows:

| Entry | Directly read 圖書番號 | 冊數 |
| --- | ---: | ---: |
| `授時曆立成` | `893` | `1` |
| `授時曆捷法立成` | `892` | `1` |

The two works are adjacent but separate columns. This is a useful internal control because it prevents the Wang-Xun `授時曆立成` from being conflated with the Kang-Bo `授時曆捷法立成`.

Page `0129` native image SHA-256:

`5f383f699c6db4a7d35549e6ea17fda939b832b9bd26bf8e15bcbee866bc221d`

No OCR was used.

## 4. Catalog-item continuity to current 奎貴893 is now resolved

The current official provider record is:

- title: `授時曆立成`;
- catalog identifier: `奎貴893`;
- `BOOK_CD=GK00893_00`;
- extent: `1冊(102張)`.

The 1940 internal `奎章閣貴重圖書目錄` directly binds the same title to `圖書番號 893`, and the official institutional history independently supports custody continuity from the former Keijo collection to SNU after 1946.

Accordingly the project may now close the previously defined item-level criterion:

```text
CATALOG_ITEM_CONTINUITY_TO_CURRENT_奎貴893=RESOLVED
EXACT_ITEM_CONTINUITY_TO_CURRENT_GK00893_00=RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL
```

This means the prewar catalog item has now been bound to the current catalog item by the same title plus the explicit precious-book number 893.

It does **not** mean that the project has separately compared every physical leaf, seal, paper feature or binding between a 1940 physical inspection and today's scan. That narrower physical-material chain remains unseparately proven and is not required to reopen the catalog-item continuity question.

## 5. The 1930 generic main number 893 must not be used

Direct inspection of the 1930 `奎章閣圖書番號順目錄` showed that its generic main sequence around 893 contains unrelated titles. Therefore:

```text
1930_GENERIC_MAIN_NUMBER_893_AS_CURRENT_奎貴893=DISPROVEN
```

The relevant binding comes instead from the 1940 **precious-book catalog**, where the table explicitly identifies the field as `圖書番號` and directly pairs `授時曆立成` with `893`.

This distinction prevents a numerically convenient but historically false mapping.

## 6. Revised prewar evidence chain

The supported sequence is now:

1. 1908 `貴重圖書目錄`: target title not visibly seen in the directly reviewed bounded section;
2. provider-dated `[1912-1920]` composite `貴重圖書目錄`: target title not visibly seen in the complete 75-page renderer object;
3. 1928-1930: official collection transfer to Keijo Imperial University;
4. 1936: Rufus directly reports an undated Wang-Xun-attributed `授時曆立成` in Keijo University Library, separate from the Kang-Bo work;
5. 1940: `奎章閣貴重圖書目錄` directly records `授時曆立成 / 圖書番號 893 / 1冊` and separately `授時曆捷法立成 / 892 / 1冊`;
6. 1946 onward: official institutional collection custody passes to SNU;
7. current provider: `授時曆立成 / 奎貴893 / GK00893_00 / 1冊(102張)`.

The item-level catalog continuity question opened in Batch 11R is therefore closed at identifier level.

## 7. Epistemic boundaries remain strict

The 1940 identifier binding does **not** establish:

- the exact surviving-copy print year within the provider's `1418-1450` range;
- any G893 target folio;
- any target glyph;
- any of the six numerical values;
- equivalence with the adjacent Kang-Bo work;
- permission to vote across later or parallel witnesses.

Accordingly:

```text
CATALOG_ITEM_CONTINUITY_AS_TARGET_FOLIO_IDENTITY=FORBIDDEN
CATALOG_ITEM_CONTINUITY_AS_TARGET_GLYPH_AUTHORITY=FORBIDDEN
CATALOG_ITEM_CONTINUITY_AS_EXACT_PRINT_YEAR=FORBIDDEN
KANG_BO_ADJACENT_ENTRY_AS_TEXTUAL_IDENTITY=FORBIDDEN
SOURCE_COUNT_VOTING=FORBIDDEN
```

## 8. Six G893 numerical controls remain pending

No target value is added for:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

All remain:

`PENDING_DIRECT_TARGET_PAGE`.

## 9. Runtime and audit-count consequence

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

## 10. Next work

The highest-value G893 task is no longer proving prewar catalog-item identity. It is direct target-page acquisition and collation.

Priority:

1. continue public or authorized acquisition of the six exact G893 target pages;
2. use the 1940 identifier binding only as provenance/copy-identification support;
3. optionally search earlier prewar records to date when precious-book number 893 first appears, without reopening the now-closed 1940-to-current catalog-item binding;
4. do not import target values from Goryeosa, Ming editions, Ogawa, G894, Sillok or Kang-Bo merely because the G893 object identity is now stronger.
