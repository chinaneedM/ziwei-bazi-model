# Fusion Chart Historical Provenance Audit R1 — Batch 12OR

## Qianli Republican Jiaoyun calendar-coordinate and remainder semantics

Status: **SOURCE MECHANICS NARROWED / EDGE-CASE CALENDAR SEMANTICS STILL OPEN / NO RUNTIME REGISTRATION**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
TARGET_ROWS=HPA-DAYUN-CAL-003,HPA-DAYUN-CAL-004
DIRECT_PHYSICAL_WITNESSES=1934,1936_韋千里命學講義
CURRENT_MISSING_FROM_PRODUCT_ROWS=4
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 1. Direct physical source strengthening

The Jiaoyun target passage is now bound directly to two National Library of China physical witnesses of 《韋千里命學講義》:

- 1934, 韋氏命苑, NLC 17jh007058 / 102955;
- 1936, 韋氏命苑, NLC 01jh000368 / 10155.

The target leaves were reviewed without OCR authority for glyph claims. Both preserve the same interval conversion, worked 140/190-unit calendarization and ten-year recurrence expression. The existing CText 《千里命稿》 surface remains later received corroboration only; no global title/edition absence claim is made.

## 2. Two-stage arithmetic must be preserved

The source does not describe one generic “add elapsed days” operation.

First, it counts the actual almanac date/shichen distance to the relevant Jie. It then converts:

```text
3 source-days -> 1 calendar-age year
1 source-day  -> 120 nominal remainder days
1 shichen     -> 10 nominal remainder days
```

Whole years are applied at the same numbered lunar month/day/shichen.

## 3. 140 / 190 are nominal 30-day-month positional units

Example 1:

```text
己巳 正月十五 子时 + 140 -> 己巳 六月初五 子时
140 = 4*30 + 20
```

Independent HKO 1929 calendar control places the two lunar dates only 137 actual elapsed days apart. Continuous actual-day addition is therefore incompatible with the worked result.

Example 2:

```text
戊辰 正月十五 子时 + 190 -> 戊辰 七月廿五 子时
190 = 6*30 + 10
```

HKO 1928 control places the two dates 215 actual elapsed days apart and shows an intercalary duplicate second lunar month between them. The source still lands at numbered month 7, so the inserted duplicate month does not consume an additional numbered-month step in this positional replay.

Source-scoped adjudication:

```text
QIANLI_REMAINDER = NOMINAL_30_DAY_MONTH_POSITIONAL_UNITS
CONTINUOUS_ACTUAL_ELAPSED_DAY_MODEL = REJECTED_FOR_THE_TWO_WORKED_EXAMPLES
```

This result is not imported into Ming Datong, Qing Shixian, modern Chinese-calendar or Wenzhen arithmetic.

## 4. Ordinary ten-year recurrence is explicit

The direct witnesses preserve recurrence at the same lunar coordinate:

```text
example 1: every 己 year, lunar 6/5, Zi-shichen
example 2: every 戊 year, lunar 7/25, Zi-shichen
```

Thus the ordinary-case Qianli recurrence is ten calendar years at the same numbered lunar month/day/shichen.

## 5. Remaining source blockers

Runtime registration remains forbidden because the source boundary is not closed for:

1. invalid target lunar day, such as day 30 landing in a small month;
2. a birth/anchor itself located in an intercalary month;
3. a destination month number occurring twice, requiring regular-vs-intercalary selection;
4. recurrence when the inherited target coordinate is invalid or duplicated.

These are source semantics, not implementation details that may be borrowed from another calendar regime.

## 6. Product outcome

Both HPA-DAYUN-CAL-003 and HPA-DAYUN-CAL-004 remain **MISSING_FROM_PRODUCT**.

No Republican/Qianli regime descriptor, historical Bazi temporal profile, runtime candidate, product selector, winner, production default, chart algorithm or schema behavior changes.

Accounting remains 222/222 audited, 4 MISSING_FROM_PRODUCT, provenance defects 44/44 repaired, historical candidate extensions 14, registries/runtime resolvers 5/5, chart algorithm defects/reopens/candidate collapses 0/0/0.

## 7. Transmission genealogy

12OR adds explicit work -> edition -> physical copy -> digital surrogate -> target passage -> source-scoped Qianli rule-family structure. No direct ancestry is asserted from Ming Datong, Qing Shixian, modern Chinese-calendar or Wenzhen methods.

## 8. Next

**12OS — Qianli invalid-date / leap-intercalary target semantics audit.**

Continue within Qianli and contemporary source families. If qualifying evidence does not close the edge cases, preserve that insufficiency explicitly and keep runtime fail-closed before re-ranking the remaining product-gap queue.

Research record: `docs/research/QIANLI-MINGXUE-JIANGYI-JIAOYUN-CALENDAR-SEMANTICS-R1.json`.
