# Fusion Chart Historical Provenance Audit R1 — Batch 12HB

## 蔡成普 /《学习时报》2026：1950—1954 四次“捐献、转让”699种总括统计作用域

Status: **STUDY TIMES ORIGINAL PUBLICATION DIRECTLY REVIEWED / JAN-1950 52-TITLE DONATION + MAR-1950–APR-1954 FOUR-EVENT 699-TITLE AGGREGATE CLOSED AT MODERN SPECIALIST-SYNTHESIS LEVEL / 699 NOT DECOMPOSED / 转让 NOT NORMALIZED TO 收购 OR 出售 / TARGET 3482-3483 ROUTE UNRESOLVED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this batch matters

Batch 12HA added a first-party National Library retrospective with the adjacent count cluster:

```text
善本书20种及收购书190种
```

Older project batches also preserve later recountings of 304, 123 and 300+ title purchase components.

A 2026 specialist synthesis supplies a different statistical level: a multi-event aggregate. Its value is to prevent false arithmetic normalization between sources.

## 2. Original publication

蔡成普《五代书香传文脉，薪火相继守典籍——常熟铁琴铜剑楼的传承与守护》 was published by 《学习时报》 on 2026-04-20.

Original:
`https://paper.studytimes.cn/cntheory/2026-04/20/content_9956406.html`

Study Times web mirror:
`https://www.studytimes.cn/wscy/202604/t20260419_87234.html`

The original publication was directly reviewed.

## 3. Aggregate chronology

The article states at the synthesis level:

```text
1950年1月
  捐献铁琴铜剑楼藏书 52种

1950年3月—1954年4月
  分4次
  向国家“捐献、转让”
  善本合计 699种
```

This closes only the modern specialist synthesis:

```text
JAN_1950_52_DONATION
  = CLOSED_AT_2026_SPECIALIST_SYNTHESIS_LEVEL

MAR1950_APR1954_EVENT_COUNT
  = 4

MAR1950_APR1954_AGGREGATE_TITLES
  = 699
```

The four exact event dates, individual counts and transaction subtypes are not supplied.

## 4. Transaction-word firewall

The source uses the combined wording:

```text
捐献、转让
```

Therefore:

```text
转让 == 收购
  = NOT_PROVED

转让 == 出售
  = NOT_PROVED

699 == PURCHASE_TOTAL
  = NOT_AUTHORIZED

699 == DONATION_TOTAL
  = NOT_AUTHORIZED
```

The aggregate cannot be converted into a priced-acquisition ledger.

## 5. Count-reconciliation firewall

12HB does not resolve the relationships among:

- 12HA: `善本20种 / 收购190种`;
- later Ji-based recountings: `304`, `123`, `300+`;
- 12HB: four-event aggregate `699`.

```text
DECOMPOSE_699_BY_ARITHMETIC
  = false

RECONCILE_190_WITH_123_OR_300_PLUS
  = false

SUM_EXISTING_REPORTED_COUNTS_TO_EXPLAIN_699
  = false
```

Different sources may be using different event windows, transaction categories, collection scopes or counting conventions.

## 6. Target-volume firewall

The article does not identify:

- 《铜壶漏箭制度》;
- 《准斋心制几漏图式》;
- 3482 / 3483;
- 03482 / 03483;
- the 1823 Huang Pilie / Shiliju one-volume fingerprint.

Therefore:

```text
TARGET_IN_JAN1950_52 = UNRESOLVED
TARGET_IN_LATER_699 = UNRESOLVED
TARGET_PURCHASE_SELECTED = false
TARGET_DONATION_SELECTED = false
TARGET_OTHER_TRANSFER_SELECTED = false
TARGET_EXACT_ACQUISITION_DATE = UNRESOLVED
```

## 7. Product / genealogy consequence

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

Accounting remains `198 / 166 / 10`, provenance metadata defects `14 / 14 repaired`, chart algorithm defects `0`.

## 8. Highest next gate

1. Recover the four underlying March-1950-to-April-1954 event records.
2. Close exact dates, per-event counts and original transaction vocabulary before reconciling any totals.
3. Search those direct records for target titles/numbers and the 1823 one-volume fingerprint.
4. Continue direct 1997 pp.446–449, Ji chapter 9, 2004 p.335/final 《編后記》 and 2010 supplement routes.

Research record: `docs/research/ZIWEI-CAI-CHENGPU-2026-TIEQIN-1950-1954-FOUR-TRANSFER-699-AGGREGATE-SCOPE-R1.json`.
