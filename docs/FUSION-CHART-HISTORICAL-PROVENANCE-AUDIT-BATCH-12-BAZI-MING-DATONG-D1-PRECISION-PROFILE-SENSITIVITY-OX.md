# Fusion Chart Historical Provenance Audit R1 — Batch 12OX

## Ming Datong D1 precision-profile sensitivity

Status: **56-BIN CORPUS NON-DISCRIMINATING / G05 REMAINS OPEN / NO RUNTIME SELECTION**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
D1_FINAL_TIME_BINS=56
TESTED_PRECISION_PROFILES=4
ALL_PROFILES_MATCH_ALL_BINS=YES
MAX_PROFILE_SPREAD_APPROX=0.088_SECONDS
MIN_PROFILE_TO_BIN_EDGE_MARGIN_APPROX=13.65_SECONDS
G05_STATUS=OPEN_BLOCKING_GENERAL_ADAPTER
RUNTIME_SELECTION_AUTHORIZED=NO
```

Research record: `docs/research/MING-DATONG-D1-PRECISION-PROFILE-SENSITIVITY-R1.json`  
Research-only Decimal harness: `scripts/research_ming_datong_d1_precision_profile_sensitivity_r1.py`

## 1. What was tested

12OW proved that a D1 computation is operationally consistent with all 56 published Ming almanac time bins in the comparison corpus. 12OX asks the more difficult question: can those same bins decide **which intermediate precision policy** the historical computation used?

The harness first reconstructs arbitrary sampled-year conjunction state from the same repository-bound 1569 constants/tables used by the 1578 source replay. It then validates the generator against all 13 existing 1578 true-conjunction points before touching the six-year comparison corpus.

Four deliberately different research profiles are then replayed:

1. full Decimal precision through the dynamic stages;
2. the locally observed 1596 lunar-Chiji six-place truncation plus D1-correction two-place truncation;
3. half-up at those same local widths;
4. a stored-table-width experiment truncating dynamic degree results to 1e-8 while leaving the D1 correction unquantized.

Profiles 2–4 are sensitivity experiments, not claims of historical authority.

## 2. Result

Every profile falls inside every one of the 56 printed time bins:

`4 profiles × 56 rows = 224 / 224 profile-row fits`.

The largest separation among the four profile outputs occurs at 1639 month 4 and is below 0.0000011 day, approximately **0.088 seconds**.

The closest any tested output gets to a printed-bin edge occurs at 1604 first month and still leaves more than 0.00015 day, approximately **13.65 seconds**.

So the smallest edge margin is more than 150 times the largest profile spread.

This is a direct non-discrimination result: the observational bins are simply too coarse to select among these precision profiles.

## 3. Historical implication

The 56-bin corpus is excellent evidence for D1 versus D2. It is not fine-grained evidence for the intermediate truncation/carry policy.

Therefore:

- the 1596 six-place / two-place behavior remains locally source-closed;
- it is **not** promoted to a universal Ming Datong rule;
- numerical fit cannot replace historical source scope;
- `MD-G05-DYNAMIC-D1-PRECISION-GENERALIZATION` remains `OPEN_BLOCKING_GENERAL_ADAPTER`.

Future G05 closure requires either additional Ming worked arithmetic exposing intermediate values, or much finer observational output capable of discriminating profiles, plus a historical authority bridge.

## 4. Forward-only snapshot discipline

12OX does not rewrite Batch 11J or 12OW historical snapshot conclusions. The Batch 11J field remains exactly `OPEN_BEYOND_THE_1596_DATONG_WORKED_EXAMPLE`; 12OX records the later negative-discrimination result only in new forward fields/artifacts.

## 5. Next batch

**12OY — multi-year month/leap generalization (G09).**

Move to the independent general-calendar gate. Build a source-derived multi-year oracle plan that includes ordinary years and intercalary years, beginning with the already observed leap-six 1531 and leap-four 1629 controls. The 56-row time corpus itself is partial and must not be misrepresented as a complete annual month/leap generator.

