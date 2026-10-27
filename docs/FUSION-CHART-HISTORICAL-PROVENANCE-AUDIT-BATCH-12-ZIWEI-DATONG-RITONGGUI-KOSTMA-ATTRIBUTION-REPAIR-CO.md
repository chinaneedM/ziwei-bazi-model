# Batch 12CO — 《大統曆日通軌》KOSTMA 证据归属纠错

## Scope

This batch repairs a provenance metadata defect introduced by Batch 12CN. It does not alter deterministic chart runtime behavior.

## 1. Trigger

A cross-check against the current Korean institutional description conflicted with the earlier Batch 12CN claim that KOSTMA `DIC_A3_000150` explicitly contained day/night table families. A dedicated exact-record audit was therefore run rather than propagating the conflict.

Evidence run: GitHub Actions `35058829315` / job `104674602946`.

## 2. Exact-record result

`DIC_A3_000150` / `大統曆日通軌` lists exactly the following relevant computational tables in the audited record:

- `太陽冬至前後二象盈初縮末限`
- `太陽夏至前後二象縮初盈末限`
- `太陰遲疾度立成`

No audited field hit supports `日出入晨刻表`, `晝夜刻分表`, or `四方每時初昏去中星度數表` as contents of this record.

## 3. Holding-identifier repair

The exact-record audit yields Kyujanggak identifier `GK12437_00` for `DIC_A3_000150`. The earlier `GR35954_00` binding is withdrawn and retained only as an audit-trace tombstone in the external-source registry.

The `GK12437_00` binding is **metadata-level only**. This batch does not claim a directly opened first-party item page, physical impression date, facsimile glyph, or numeric table cell.

## 4. Historical consequence

Batch 12CN no longer proves a pre-1578 Datong-line day/night-ke table-class witness. The valid residue is narrower: a Sejong-era Datong/Tonggui calendrical-computation record with three named solar/lunar computational tables.

Therefore all of the following remain unresolved:

- an explicit pre-1578 `晨昏分 / 日出入 / 晝夜刻` numerical table witness;
- Nanjing `59/41` cell identity;
- daily ladder and intra-term change-day identity;
- rounding / quantization rule ancestry;
- direct transmission into the 1578 `三命通會` display.

## 5. Provenance defect accounting

```text
DEFECT_CLASS = PROVENANCE_METADATA_WRONG_RECORD_FIELD_AND_HOLDING_ATTRIBUTION
DEFECT_FOUND_INCREMENT = +1
DEFECT_REPAIRED_INCREMENT = +1
MATRIX_ROW_COUNT_CHANGE = 0
AUDITED_ROW_COUNT_CHANGE = 0
RUNTIME_ALGORITHM_CHANGE = 0
```

## 6. Next gate

1. Audit `DIC_A3_000151 / 大統曆註` separately; its generic description of `日月出入 / 晝夜長短` must not be promoted into an exact numerical-table claim without a page or explicit field.
2. Continue pre-1578 Datong annual-almanac and related first-party table searches.
3. Require readable page-level cells before comparing `59/41`, ladders, change days, or rounding fingerprints.

The deterministic product remains `CLOSED`; `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT` with no runtime change.
