# Fusion Chart Historical Provenance Audit R1 — Batch 12FY

## 《五石斋文史札记（二十八）》：2008年第3期第一方容器、维普目录与日期—页码锚点边界

Status: **PKU 2008 ISSUE 03 FIRST-PARTY CONTAINER CLOSED / CQVIP 31-ARTICLE TOC SURFACE CLOSED / 1949-09-30 p120 SECONDARY ANCHOR / 1950-01-01 p124 DISCOVERY ANCHOR / 1950-01-29 JOURNAL PAGE UNRESOLVED / PRIMARY JOURNAL TEXT NOT REVIEWED / FACSIMILE PAGE UNRESOLVED / ZERO GENEALOGY OR RUNTIME CHANGE**

## 1. Purpose

Batch 12FX proved that Deng Rui's serial transcription workflow was checked against the original diary source, but it did not close the exact journal page or facsimile page for the 1950-01-29 Tieqin purchase entry.

Batch 12FY therefore separates three coordinate systems that must not be collapsed:

1. the **2008 journal issue/article pagination** of 《中国典籍与文化》;
2. the **2012 derivative book pagination** of 《邓之诚文史札记》;
3. the **2007 volume-5 facsimile pagination/leaf sequence** of 《邓之诚日记》.

The immediate goal is the first coordinate system only.

## 2. Peking University first-party issue container

The Peking University journal platform directly exposes the back-issue route for *Chinese classics & culture* and a first-party issue page identified by:

- `jid=94408`
- `viid=12482306`
- `issueNo=03`
- displayed heading: `2008 , Issue 03 Table of Contents`
- ISSN `1004-3241`
- CN `11-2992/G2`
- supervisor: 中华人民共和国教育部
- organizer: 全国高等院校古籍整理研究工作委员会.

The page also exposes fulltext bridge links to publisher / national social-sciences / CNKI / Wanfang / CQVIP routes.

However, on the reviewed public static surface the target row for 《五石斋文史札记（二十八）》 is **not source-emitted**. No target article page range or article text is emitted either.

Therefore the first-party issue container is closed, but the target article row/page is not.

## 3. CQVIP current TOC surface

The current CQVIP journal page directly binds the same journal identity and displays:

- `2008年3期`
- `共：31篇`
- a TOC pagination control with pages `1 / 2`.

The directly reviewed first static TOC page exposes article page ranges only through `92-95`. The target article is not visible on that reviewed first page, and the second TOC page was not directly retrieved by the project.

This establishes a finite public TOC boundary only. It does **not** authorize the inference that the target starts immediately after p95, nor any guessed page range.

## 4. Secondary date—page anchors

Two non-primary page anchors can currently be reproduced:

- Qu Jun's article 《重大问题的再历史化》 cites 《五石斋文史札记》(二十八), the 1949-09-30 entry, at **journal p120**, 《中国典籍与文化》 2008(3).
- A lower-authority Wikipedia citation for Weng Dujian reports the 1950-01-01 entry in installment (二十八) at **journal p124**, total issue 66 / 2008 No.3.

The first is retained as a scholarly secondary exact date-page anchor pending primary journal collation. The second remains discovery-only pending stronger corroboration.

These anchors show that installment (二十八) reaches at least the p120/p124 region, but they do **not** locate 1950-01-29.

## 5. No linear pagination inference

Chronology cannot be converted into a page number by interpolation.

The interval:

`1949-09-30 -> p120`

`1950-01-01 -> p124`

does not imply any fixed number of diary days per journal page. Entries differ in length, selection, omission, editorial normalization and density. The 1950-01-29 page therefore remains:

`TARGET_1950_01_29_JOURNAL_PAGE=UNRESOLVED`.

Likewise, a journal page such as p120 or p124 cannot be mapped to volume-5 facsimile p120/p124 without a direct crosswalk.

## 6. Public access boundary

Reviewed routes produced the following bounded results:

- PKU issue/back-issue pages: issue identity closed, target row/text not emitted on reviewed static surface.
- CNKI bridge: public reviewed route returned 502.
- Wanfang bridge: JavaScript application shell, no target metadata emitted in the reviewed static surface.
- CQVIP legacy bridge: HTTP 412 on the reviewed route.
- Current CQVIP journal page: TOC first-page metadata available, target second-page row not directly retrieved.

No login bypass, paywall bypass, subscription purchase or copy request was attempted.

## 7. Target-entry / transaction firewall

The 1950-01-29 derivative quotation remains stronger than a generic later anecdote because FX closed Deng Rui's editor-checked serial route. Nevertheless:

`PRIMARY_JOURNAL_TARGET_TEXT=NOT_REVIEWED`

`TARGET_FACSIMILE_PAGE=UNRESOLVED`

`TARGET_HANDWRITING_DIRECTLY_COLLATED=false`.

Even after the journal page is closed, collection-level wording such as twelve boxes and `以归公` cannot by itself bind the historical 3482/3483 composite target or the 1823 士礼居 one-volume fingerprint to those boxes.

## 8. Product / genealogy consequence

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `DIRECT_SANMING_PARENT_VOTE_INCREMENT=0`; `PRE1578_ZHUNZHAI_RULE_WITNESS_INCREMENT=0`; `MATRIX_ROW_COUNT_CHANGE=0`; `ALGORITHM_REOPEN=0`; `CANDIDATE_COLLAPSE=0`; `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

Accounting remains **198 / 166 / 10** for Matrix rows / audited / current missing; provenance defects remain **13 / 13** repaired; chart algorithm defects remain **0**.

## 9. Highest next gate

1. Recover a primary or first-party article record / TOC row for 《五石斋文史札记（二十八）》 in 2008 Issue 03 and close its exact article page range.
2. Directly inspect the primary journal text around 1950-01-29 and close the exact journal page plus punctuation-independent wording.
3. Compare primary journal transcription against the 2012 derivative for omissions/normalization, without treating either as handwriting authority.
4. Resolve the exact 2007 facsimile volume-5 page/leaf for 1950-01-29 and directly collate the handwriting.
5. Search the directly reviewed target and adjacent pages for 《铜壶漏箭制度》, 《准斋心制几漏图式》, 3482/3483, 03482/03483, the 1823 士礼居 one-volume fingerprint or another stable identifier.
6. Continue Gu Tinglong 1950-01-06, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine-readable evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI-2008-ISSUE03-PAGINATION-BOUNDARY-R1.json`.
