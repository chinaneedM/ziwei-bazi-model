# Fusion Chart Historical Provenance Audit — Batch 12CN

## Scope

Batch 12CM established that Zhou Xiang's 1569 public `《大明大統曆法》` fascicle is a genuine pre-1578 Datong technical witness but does not itself expose the required `晨昏分 / 日出入 / 晝夜刻` table. Batch 12CN therefore moves to the direct `《大統曆日通軌》` route.

The result is a material narrowing of the ancestry problem: an institutional Korean record directly describes a Sejong-era Datong-line technical compilation containing both a sunrise/sunset table and a day/night-ke-fen table, and it exposes a concrete Kyujanggak legacy holding identifier. The physical scan remains inaccessible in the present route, so the evidence is recorded at the institutional-content/holding-binding level rather than promoted to page-glyph authority.

## 1. Direct KOSTMA record

GitHub Actions run `35057301901` / job `104670045742` directly retrieved KOSTMA record `DIC_A3_000150` for `대통력일통궤(大統曆日通軌)`.

The record identifies:

```text
title       大統曆日通軌
record      DIC_A3_000150
type        고서/기술서
context     1433–1445 (Sejong-era calendar-reform context in the record)
repository  서울대학교 규장각한국학연구원
```

Most importantly, its content description explicitly enumerates three technical table families:

1. `日出入晨刻表` — sunrise/sunset morning-ke table by the 24 solar terms;
2. `晝夜刻分表` — day/night ke-fen table;
3. `四方每時初昏去中星度數表` — initial-dusk stellar-degree table by direction/time.

This is the first route in the present Sanming ancestry sequence that moves the target from a generic Datong title to an institutional record explicitly naming the required day/night table class before 1578.

## 2. Physical holding binding and access boundary

The KOSTMA `dicView` surface emits an old Kyujanggak `CONVIEW` target with:

```text
cn=GR35954_00
```

Batch 12CN then probed the exact legacy route in run `35057437846` / job `104670447349`:

```text
HTTP legacy route   -> 404 Not Found
HTTPS legacy route  -> connection reset by peer from GitHub runner
```

Therefore:

```text
KYUJANGGAK_OBJECT_BINDING_GR35954_00 = CONFIRMED_AT_SOURCE_EMITTED_LOCATOR_LEVEL
DIRECT_SCAN_OBTAINED = FALSE
DIRECT_PHYSICAL_GLYPH_COLLATION = FALSE
DIRECT_NUMERIC_CELL_COLLATION = FALSE
```

A dead or reset viewer route is an access boundary, not evidence that the holding or table is absent.

## 3. Four-layer provenance firewall

The following layers are deliberately not collapsed:

```text
underlying work lineage  -> Ming/Datong Tonggui tradition associated by the record with Yuan Tong
Joseon technical layer   -> Sejong-era 1433–1445 compilation/reform context in the institutional record
physical holding layer   -> current Kyujanggak legacy object locator GR35954_00
digital metadata layer   -> KOSTMA DIC_A3_000150 and current/legacy web routing
```

In particular, `GR35954_00` is **not** called a Chinese Ming Zhengtong physical edition on the strength of title, era, or underlying work lineage. Exact physical impression/copy details remain subject to first-party item-page or scan verification.

## 4. What this proves — and what it does not

Batch 12CN now supports:

```text
PRE_1578_DATONG_LINE_DAYNIGHT_TABLE_CLASS_WITNESS = TRUE
EXPLICIT_SUNRISE_SUNSET_TABLE_CLASS = TRUE
EXPLICIT_DAYNIGHT_KE_FEN_TABLE_CLASS = TRUE
CONCRETE_KYUJANGGAK_LEGACY_OBJECT_BINDING = TRUE
```

It does **not** yet support:

```text
GR35954_00_PHYSICAL_TABLE_CELLS_DIRECTLY_READ = FALSE
NANJING_59_KE_CAP_IN_THIS_WITNESS = UNRESOLVED
SANMING_59_41_NUMERIC_IDENTITY = UNRESOLVED
DAILY_LADDER_CHANGE_DAY_IDENTITY = UNRESOLVED
BATCH_12CI_ROUNDING_RULE = UNRESOLVED
DIRECT_PARENTAGE_TO_SANMING_1578 = UNRESOLVED
```

A Joseon recension is a valuable transmission witness but cannot by itself prove the exact Chinese line into Wan Minying's 1578 `《三命通會》`.

## 5. Tianwen transmission impact

The graph now distinguishes four nodes: the modern KOSTMA record, the Joseon Sejong recension layer, the Kyujanggak holding locator, and the day/night table family described by the record. Confirmed edges are limited to what the database surface actually supports: the record describes the recension, binds to the holding locator, and the recension is described as containing the target table family.

A direct numeric-parent edge from that table family to the Sanming 1578 day/night-ke table remains explicitly unresolved.

## 6. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

This evidence narrows the historical timekeeping ancestry search; it does not authorize a chart-runtime change.

## 7. Next gate

1. acquire a lawful readable scan or replacement first-party item surface for `GR35954_00` and collate the actual `日出入晨刻表 / 晝夜刻分表` cells;
2. test the solstitial cap, daily ladder, intra-term change days, and quantization against the Nanjing `59/41` and Sanming 1578 fingerprints;
3. continue pre-1578 annual Datong almanac and `楊瓚《閑中錄》` search in parallel to avoid treating the Joseon recension as the Chinese transmission path by default;
4. keep the Batch 12CI rounding/selection threshold open until explicit historical mechanics or exact cell reconstruction closes it.

Research record: `docs/research/ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-R1.json`.
