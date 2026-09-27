# Fusion Chart Historical Provenance Audit R1 — Batch 12HJ

## 赵万里1951：瞿氏“六十二种”捐赠总结与1950“52种”统计时序防火墙

Status: **1951 PUBLICATION-TEXT QUOTATION BRIDGE CLOSES QU-FAMILY 62-TITLE DONATION SUMMARY + SONG 《春秋左传注疏》 NAMED MEMBER / DIRECT 1951 + 2011 PAGE COLLATION STILL OPEN / 52→62 TEN-TITLE ARITHMETIC INFERENCE FORBIDDEN / TARGET 3482-3483 UNRESOLVED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this batch matters

Batch 12HF used the Zhao Wanli 1951 passage only for Ding Huikang's six-title donation. The same passage also contains a separate Qu-family count that had not yet been modeled in the repository.

Xiao Ling's 2026 scholarly quotation bridge, citing `《赵万里文集：第一卷》 p.197`, reproduces Zhao Wanli's 1951 statement that the Qu brothers donated a Song edition of `《春秋左传注疏》` and other rare books totaling **62 titles**.

## 2. Publication layer

NLC bibliographic control already closes the original article as:

```text
赵万里
《永乐大典展览的意义——一九五一年八月北京图书馆举办》
《文物参考资料》
1951年第9期
pp.221–233
```

The original 1951 pages and 2011 collected-works p.197 remain **NOT DIRECTLY REVIEWED**.

Therefore 12HJ is a:

```text
CONTEMPORARY_PUBLICATION_TEXT_QUOTATION_BRIDGE
```

not a direct original-page collation.

## 3. Qu-family 62-title statement

The quoted passage places the statement inside a roughly two-year retrospective of rare books sent through the Cultural Relics Bureau to Beijing Library and names:

```text
瞿济苍
瞿凤起
瞿旭初
```

with:

```text
TRANSACTION = 捐赠
COUNT = 62种
EXPLICIT MEMBER = 宋刻《春秋左传注疏》
```

This gives the project one named member anchor inside the 62-title group.

## 4. 1950-02-11 comparator

The Song Yunbin diary public excerpt records Zhao Wanli's report on 1950-02-11 as:

```text
瞿氏另捐 52种
```

The evidence layers are therefore:

```text
1950-02-11:
52 titles
PUBLIC EXCERPT OF CONTEMPORANEOUS DIARY

1951 publication context:
62 titles
CONTEMPORARY PUBLICATION TEXT THROUGH 2011/2026 QUOTATION BRIDGE
```

## 5. Critical arithmetic firewall

```text
62 - 52 = 10
```

arithmetically, but:

```text
“后来又捐了10种”
  = NOT PROVED
```

Possible explanations include additional later transfers, cumulative-versus-event scope, title-count conventions, or reporting/editorial variation.

Gu Tinglong's mediated Jan-6 `42` count remains another unresolved comparator.

Thus:

```text
MONOTONIC 42 -> 52 -> 62 DONATION SEQUENCE
  = NOT SELECTED

COUNT NORMALIZATION
  = FORBIDDEN
```

## 6. Named-member anchor boundary

`宋刻《春秋左传注疏》` is now an explicit member example of the 62-title quotation bridge.

Still unresolved:

- exact NLC item identifier;
- accession number;
- exact transfer date;
- full 62-title list.

This named item may be used to search the historical accession chain, but it may not be used as a proxy for the target volume.

## 7. Target-volume firewall

The quotation does not name:

- 《铜壶漏箭制度》;
- 《准斋心制几漏图式》;
- 3482 / 3483;
- 03482 / 03483;
- the 1823 Huang Pilie / Shiliju one-volume fingerprint.

Therefore:

```text
TARGET_IN_QU_62 = UNRESOLVED
TARGET_IN_FEB1950_52 = UNRESOLVED
TARGET_PURCHASE_SELECTED = false
TARGET_DONATION_SELECTED = false
TARGET_DING_INTERMEDIARY_SELECTED = false
```

## 8. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`; provenance metadata defects `14 / 14 repaired`; chart algorithm defects `0`.

## 9. Highest next gate

1. Directly collate original/facsimile 1951 pp.221–233 and 2011 p.197.
2. Trace the Song `《春秋左传注疏》` member to a stable NLC item/accession record and use it to recover the rest of the 62-title group.
3. Do not explain `62-52` by arithmetic alone.
4. Continue 2018 pp.309–310, 1997 pp.446–449, Ji chapter 9, 2004 p.335/final `《編后記》` and the 2010 supplement route.

Research record: `docs/research/ZIWEI-ZHAO-WANLI-1951-QU-SIXTYTWO-DONATION-COUNT-CHRONOLOGY-FIREWALL-R1.json`.
