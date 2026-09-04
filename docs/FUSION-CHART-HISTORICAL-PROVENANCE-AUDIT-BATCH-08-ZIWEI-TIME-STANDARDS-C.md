# Fusion Chart Historical Provenance Audit R1 — Batch 08C

## Ziwei time standards: Luoyang mean solar time vs local apparent solar time

Status: **AUDITED / TERMINOLOGY-SEPARATED / NO ALGORITHM REOPEN**

## 1. Philological boundary

`洛阳时间`、`平太阳时`、`真太阳时/视太阳时` are not interchangeable labels.

- Wang Tingzhi's Zhongzhou wording points to a Luoyang-region longitude standard.
- Mean solar time is the longitude-based uniform solar clock.
- Apparent/true solar time adds the equation-of-time variation.

Therefore the runtime's two candidates are mechanically different and must remain separately named.

## 2. Zhongzhou Luoyang candidate

Current runtime uses UTC + Luoyang longitude (112°26′) × 4 minutes/degree. It does **not** add equation of time. This is correctly modeled as `ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME`.

Verdict: `SUPPORTED_BUT_SCHOOL_SPECIFIC`.

## 3. Local apparent solar candidate

`SolarTimeEngine` first derives local mean solar time from longitude, then adds equation-of-time to obtain local apparent solar time. USNO's astronomical definition matches this decomposition.

Modern Ziwei practitioners use true/apparent solar time, but this does not prove an early or universal Ziwei rule.

Verdict: `MODERN_COMPATIBILITY_ONLY` for doctrinal authority, while the astronomical computation itself is mechanically supported.

## 4. Orthogonal candidate dimensions

Time standard does not select the flow-hour active-palace method. These remain independent axes:

- time: Luoyang mean solar vs local apparent solar;
- active address: Zhongzhou fixed-branch case vs 1581 day-anchored sequence.

## 5. Accounting

```text
TOTAL_MATRIX_ROWS=161
TOTAL_AUDITED_ROWS=121
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=8
```
