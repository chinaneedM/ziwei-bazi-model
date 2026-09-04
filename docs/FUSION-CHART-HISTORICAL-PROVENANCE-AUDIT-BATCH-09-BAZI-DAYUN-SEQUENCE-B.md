# Fusion Chart Historical Provenance Audit R1 — Batch 09B

## Bazi Dayun Ganzhi sequence from the natal month pillar

Status: **AUDITED / SEQUENCE CLOSED / NO ALGORITHM REOPEN**

## 1. Scope separation

This batch audits only the Dayun Ganzhi sequence. It does not reopen:

- direction by year-stem polarity and sex;
- Jie anchor selection;
- 三日一岁 symbolic age;
- continuous vs Wenzhen calendar realization;
- ten-year boundary timestamp implementation.

## 2. Source rule

Later explicit Ziping witnesses state that the natal month pillar is the base of the luck sequence. In forward motion the first formal Dayun is the next sexagenary pillar; in reverse motion it is the previous pillar. Subsequent Dayun pillars continue one step at a time.

Examples include 丙寅→丁卯→戊辰… forward and 戊寅→丁丑→丙子→乙亥… reverse.

《三命通会》 provides the earlier direction/Jie/one-辰-ten-year framework.

## 3. Runtime replay

Runtime uses `ganzhi_index = month_index + step * index`, with formal Dayun index starting at 1. This exactly reproduces the explicit source examples.

The pre-Jiaoyun period is represented separately and must not be renumbered as formal Dayun #1 merely because some UIs display the natal month row.

## 4. Accounting

```text
TOTAL_MATRIX_ROWS=172
TOTAL_AUDITED_ROWS=136
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```
