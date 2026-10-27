# Fusion Chart Historical Provenance Audit R1 — Batch 09A

## Solar-term astronomy vs Bazi year/month boundary doctrine

Status: **AUDITED / ASTRONOMY-DOCTRINE SEPARATED / NO ALGORITHM REOPEN**

## 1. Separation principle

An accurate modern solar-term instant does not by itself prove how Bazi should consume that instant.

Batch 09A therefore audits separately:

- modern astronomical realization of the 24 solar terms;
- Bazi year pillar switching at Lichun;
- Bazi month branch switching at each Jie;
- instant-level boundary semantics.

## 2. Astronomical realization

HKO defines the 24 solar terms at 15° longitude intervals, including Lichun at 315°. Runtime uses a modern apparent-geocentric solar-longitude engine to find the instants.

Verdict: `MODERN_COMPATIBILITY_ONLY` as a computational realization, with high astronomical confidence.

## 3. Bazi year boundary

《命理探源》 explicitly says 推年以立春节为纲 and gives same-day examples where births before and after the stated Lichun hour receive different year pillars. 《千里命稿》 independently corroborates this.

Verdict: `HISTORICALLY_SUPPORTED` for the received Bazi rule.

## 4. Bazi month boundary

《三命通会》 preserves the month-season structure 正月寅立春雨水、二月卯惊蛰春分 ...; 《命理探源》 makes the mechanical boundary explicit: 推月以节令为纲 and switches on crossing the Jie.

Current runtime's Jie-only sequence exactly matches this structure.

Verdict: `HISTORICALLY_SUPPORTED`.

## 5. Exact instant

Historical worked examples distinguish birth hours before and after the almanac's stated 交节 time on the same date. Therefore the rule is an instant boundary, not a whole-date approximation.

Current half-open interval semantics match.

## 6. Accounting

```text
TOTAL_MATRIX_ROWS=170
TOTAL_AUDITED_ROWS=133
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```
