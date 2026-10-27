# Fusion Chart Historical Provenance Audit R1 — Batch 11E

## Ming Datong 1578 month-start oracle

Status: **AUDITED / COMPLETE TARGET-YEAR MONTH-START CHAIN MACHINE-FIXTURED / SAME-YEAR ALMANAC IMAGE STILL UNCOLLATED / GENERAL ARITHMETIC NOT CERTIFIED / NO ALGORITHM REOPEN**

Batch 11D located both a 1569 Ming Datong computational-method witness and the exact 1578 Qintianjian almanac. Batch 11E closes a narrower question: can the target year itself be represented by a reproducible independent month-start oracle while the general adapter remains fail-closed?

## 1. Complete official-record chain

`EXT-MINGSHILU-WANLI-1578-MONTH-STARTS` preserves the month-start Ganzhi for Wanli 6 months 1–12, followed by Wanli 7 month 1:

```text
癸丑 → 壬午 → 壬子 → 壬午 → 辛亥 → 辛巳
→ 庚戌 → 庚辰 → 己酉 → 戊寅 → 戊申 → 丁丑 → 丁未
```

Using the explicit 0-based sexagenary convention `甲子=0`, consecutive start differences modulo 60 yield:

```text
29 / 30 / 30 / 29 / 30 / 29 / 30 / 29 / 29 / 30 / 29 / 30
```

The sum is 354 days. The records move through consecutively numbered months 1–12 and then to the next year's month 1, so the represented Wanli-6 year contains no leap-month label.

## 2. Independent court-record corroboration

`EXT-WANLI-QIJUZHU-1578-MONTH-CORROBORATION` independently preserves multiple month starts and within-month dated entries. Several starts can be recomputed from multiple internal day/Ganzhi pairs rather than trusting a single heading.

This is used as corroboration, not as an edition-critical replacement for the Qintianjian almanac.

## 3. Machine evidence fixture

`tests/fixtures/ming-datong-1578-month-start-oracle-r1.json` records the full chain, volume-level locators, the Wanli-7 next anchor, explicit `甲子=0` indexing, derived month lengths, 354-day total, represented non-leap structure, and flags that forbid runtime selection/general calendar certification.

`tests/test_ming_datong_1578_month_start_oracle_r1.py` recomputes every transition and fails if the evidence fixture drifts.

## 4. Institutional context cross-check

`《明神宗顯皇帝實錄》` volume 80 records that on Wanli 6 month 10 day 1 the Qintianjian officials presented the following year's `大統曆`, after which it was distributed to officials and promulgated throughout the realm.

This is institutional evidence, not a computational rule.

## 5. Closure boundary

Closed for target-year evidence:

- complete 1578 month-start Ganzhi chain;
- twelve 29/30-day month lengths by deterministic transition;
- 354-day total;
- no leap month in the represented numbered-month chain.

Still open before an executable Ming adapter is permitted:

1. replay of the 1569 `步氣朔` arithmetic that generates the 1578 oracle;
2. page-level collation of the exact 1578 `明欽天監刊本`;
3. historical day boundary and clock coordinate;
4. enforcement/geographic/institutional scope;
5. invalid-date behavior;
6. multi-year generalization and ten-year Dayun recurrence under the same regime.

Therefore:

```text
HPA-DAYUN-CAL-002=MISSING_FROM_PRODUCT
HISTORICAL_CALENDAR_ARITHMETIC_IMPLEMENTED=NO
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

Next work is method-to-oracle replay and exact 1578 almanac page evidence, not speculative coding.
