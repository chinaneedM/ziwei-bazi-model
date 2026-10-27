# Fusion Chart Historical Provenance & School Audit R1

## Batch 11W - Lee Eun-Hee / Jing Bing 1998 Official Journal Archive Binding

Status: **COMPLETE FOR DIRECT OFFICIAL ARTICLE IDENTITY + ABSTRACT; FULL TEXT AND SIX G893 TARGET PAGES REMAIN FAIL-CLOSED**

Batch ID: `BATCH-11-BAZI-G893-LEE-JING-1998-OFFICIAL-ARCHIVE-W`

Machine-readable evidence:

- `docs/research/G893-LEE-JING-1998-OFFICIAL-JOURNAL-ARCHIVE-R1.json`

This batch upgrades one important G893 specialist source from bibliographic-only identification to a directly verified official journal record. It does not retrieve the protected/full article from CNKI, does not expose any G893 target page, and has no runtime effect.

## 1. Official 1998 issue and paper record are directly bound

The official 《中國科技史料》 CBPT/CNKI journal portal directly exposes the 1998 issue 02 identity:

- `yearId = adaf0591-da7f-47b1-a26b-f97893bc2011`;
- `issueId = 081bfc10-b643-4702-9389-346193d8815e`.

The issue contains ten paper records. The unique title+author match is:

- paper UUID: `5c4276d953bd47ca2679c70209d179cf`;
- title: `朝鲜奎章阁本的《授时历立成》`;
- authors: `李银姬 / 景冰`;
- author units: `韩国延世大学天文系 / 中国科学院自然科学史研究所`;
- publication date: `1998-06-30`;
- classification: `P1-093.12`;
- CNKI node: `ZGKS802.008`.

The captured official HTML SHA-256 is:

`e36670c425afd627551d25acec219eb1b4c7cb4285edef6aceff83adaf454825`.

## 2. The official abstract is now a direct source, not a mediated quotation

The official journal page itself states, in substance, that the paper studies the one-volume Kyujanggak 《授时历立成》 in Korea attributed to Wang Xun; it assigns the underlying work to the Yuan-period Shoushi tradition and the Korean printing/republication to King Sejong's reign; it also highlights the four-dark-star material as a supplement to the transmitted Shoushi corpus.

This matters because the project no longer needs Li Liang 2018 or KCI/RISS merely to establish what the 1998 paper itself claims at abstract level.

It does **not** make the paper a primary historical witness, and it does not replace the physical G893 object.

## 3. Exact 1434 versus 1444 copy dating remains unresolved

The official 1998 abstract is only reign-scoped. It does not supply a copy-specific colophon or exact year.

Therefore:

```text
G893_EXACT_SURVIVING_COPY_PRINT_YEAR=UNRESOLVED_WITHIN_PROVIDER_1418_1450_RANGE
LEE_JING_1998_ABSTRACT_AS_EXACT_1434_OR_1444_PROOF=FORBIDDEN
```

Batch 11M's 1434/1444 secondary conflict remains intact.

## 4. Full text remains outside the public official-journal HTML

The public paper page directly exposes:

- abstract;
- English abstract;
- reference list;
- publication metadata.

Its full-text panel explicitly routes outward through CNKI node `ZGKS802.008`.

No authentication/paywall bypass was attempted. No public target-page plate or computational-table image is exposed on the official article page captured by this batch.

Accordingly:

```text
LEE_JING_1998_FULL_ARTICLE_DIRECTLY_RETRIEVED=false
PUBLIC_TARGET_FIGURE_EXPOSED=false
PAYWALL_OR_AUTH_BYPASS_ATTEMPTED=false
```

## 5. Batch 11U and 11V remain controlling in their own scopes

Batch 11U remains the identity control:

```text
EXACT_ITEM_CONTINUITY_TO_CURRENT_GK00893_00=RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL
1930_GENERIC_MAIN_NUMBER_893_AS_CURRENT_奎貴893=DISPROVEN
```

Batch 11V remains the digital M/F route control:

```text
G893_CURRENT_MF_PDF_ROUTE=CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED
```

Batch 11W changes neither result.

## 6. Six numerical controls remain pending

No target page or target glyph was obtained from the 1998 article.

All remain `PENDING_DIRECT_TARGET_PAGE`:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

The article abstract cannot be used to prepopulate any of them.

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

1. seek legitimate full-article access or an openly reviewable scan and inspect whether pages 73–77 reproduce G893 tables or plates;
2. continue public/authorized acquisition of the six exact `GK00893_00` target pages independently of the article;
3. if a target figure is found, bind table heading, limit number, row identity and visible glyph before recording any numeric value;
4. keep exact 1434 versus 1444 copy dating unresolved absent copy-specific primary/provider evidence;
5. continue the broader cross-edition, cross-region and cross-language search horizon.
