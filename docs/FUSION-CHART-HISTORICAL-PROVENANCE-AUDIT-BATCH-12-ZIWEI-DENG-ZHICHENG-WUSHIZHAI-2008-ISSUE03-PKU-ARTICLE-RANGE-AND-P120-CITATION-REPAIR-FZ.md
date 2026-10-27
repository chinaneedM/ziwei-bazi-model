# Fusion Chart Historical Provenance Audit R1 — Batch 12FZ

## 《五石斋文史札记（二十八）》：北大平台 121–129 页文章范围闭合与 FY p120 二手页码纠错

Status: **FIRST-PARTY PLATFORM ARTICLE RANGE 121–129 CLOSED / FY p120 SECONDARY ANCHOR CONFLICT CONFIRMED AND REPAIRED FORWARD-ONLY / JAN-29 EXACT JOURNAL PAGE UNRESOLVED / PRIMARY JOURNAL TEXT NOT REVIEWED / FACSIMILE PAGE UNRESOLVED / ZERO RUNTIME CHANGE**

## 1. Trigger

Batch 12FY closed the official 2008年第3期 issue container but could not obtain the target article row/page range. It therefore retained two non-primary page leads: a scholarly secondary citation assigning the 1949-09-30 entry to p120, and a lower-authority discovery citation assigning the 1950-01-01 entry to p124.

A further search of Peking University's own journal-platform index now source-emits:

- title: `《五石斋文史札记》(二十八)`;
- authors: 邓之诚、邓瑞;
- source: `中国典籍与文化 2008, (03)`;
- exact page range: **121–129**;
- Fulltext label present in the indexed metadata.

The live article-detail route is not stably rendered on the reviewed public surface, so this batch closes bibliographic page-range metadata, not page images or article glyphs.

## 2. Exact article-range consequence

`ARTICLE_PAGE_RANGE = 121–129`

`ARTICLE_RANGE_AUTHORITY = FIRST_PARTY_PKU_PLATFORM_INDEX_METADATA`

`PRIMARY_PAGE_IMAGES_REVIEWED = false`

`PRIMARY_ARTICLE_TEXT_REVIEWED = false`

This is materially stronger than the FY issue-container-only state. The search space for any entry actually present in installment (二十八) is now the published article span 121–129. It does not prove that the 1950-01-29 entry was serialised, and it does not identify an exact page for that date.

## 3. FY p120 conflict and forward-only repair

FY registered Qu Jun's secondary scholarly citation as an exact date-page anchor:

`1949-09-30 -> p120 -> 《五石斋文史札记》(二十八)`

But p120 lies outside the first-party article range 121–129. The project therefore can no longer treat p120 as a valid within-article page anchor.

This is recorded as:

`PROV-DEFECT-014 = PROVENANCE_METADATA_SECONDARY_PAGE_ANCHOR_CONFLICTS_WITH_FIRST_PARTY_ARTICLE_RANGE`

The original FY evidence is **not rewritten**. The current external-source registry is repaired forward-only so the p120 citation remains visible as a historical audit trace but is reclassified as conflicting and non-authoritative for article pagination pending direct primary p120 review, an explicit erratum, or another demonstrated pagination system.

Defect accounting:

`DEFECT_FOUND_INCREMENT=+1`

`DEFECT_REPAIRED_INCREMENT=+1`

`CONFIRMED_PROVENANCE_METADATA_DEFECTS=14`

`REPAIRED_PROVENANCE_METADATA_DEFECTS=14`

## 4. p124 control

The lower-authority citation placing 1950-01-01 at p124 is **range-consistent** with the first-party 121–129 article span. Range consistency is not independent confirmation.

Therefore p124 remains:

`LOWER_AUTHORITY_DISCOVERY_ONLY`

and is not promoted to primary or scholarly page authority.

## 5. 1950-01-29 target boundary

The exact 1950-01-29 journal page remains `UNRESOLVED`.

The primary journal text remains `NOT_REVIEWED`.

The 2007 facsimile volume-5 page/leaf remains `UNRESOLVED`.

The handwriting remains `NOT_REVIEWED`.

No linear date-to-page interpolation, density estimate, or p124→later-page guess is authorized. The only safe new bound is the article-level 121–129 span **if the Jan-29 entry is actually present in the installment**.

## 6. Product / genealogy consequence

No transmission node or edge is added. No acquisition edge, SAME_OBJECT relation, runtime rule change, candidate collapse, or algorithm reopen is authorized.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 7. Highest next gate

1. Directly retrieve or review the primary article pages 121–129, or a source-emitted fulltext object, and locate the 1950-01-29 entry without interpolation.
2. If present, bind its exact journal page and punctuation-independent wording and compare against the 2012 derivative for omission/normalization.
3. Resolve the p120 conflict only from a primary p120 page, explicit erratum, demonstrated alternate pagination, or equally strong evidence.
4. Resolve the exact 2007 facsimile volume-5 page/leaf for 1950-01-29 and directly collate the handwriting.
5. Search the target and adjacent pages for 《铜壶漏箭制度》, 《准斋心制几漏图式》, 3482/3483, 03482/03483, the 1823 士礼居 one-volume fingerprint, or another stable item identifier.
6. Continue Gu Tinglong 1950-01-06, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI-2008-ISSUE03-PKU-ARTICLE-RANGE-P120-REPAIR-R1.json`.
