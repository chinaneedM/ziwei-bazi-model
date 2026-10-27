# Fusion Chart Historical Provenance Audit R1 — Batch 12OY

## Ming Datong multi-year leap-rule validation

Status: **LEAP-EXISTENCE + OLD-DATONG DAY-LEVEL PLACEMENT SAMPLE-VALIDATED / G09 STILL OPEN FOR MING-ERA BOUNDARY CENSUS**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
PRIMARY_1569_LEAP_EXISTENCE_RULE=CLOSED_SOURCE_SCOPED
OLD_DATONG_NO_ZHONGQI_DAY_LEVEL_PLACEMENT=CLOSED_SOURCE_SCOPED
SAMPLED_YEARS=7
PRECISION_PROFILES=4
PROFILE_YEAR_CONTROLS=28_OF_28_MATCH
KNOWN_LEAP_MONTHS=1531_LEAP6,1596_LEAP8,1629_LEAP4
G09_STATUS=OPEN_BLOCKING_GENERAL_ADAPTER
RUNTIME_SELECTION_AUTHORIZED=NO
```

Research record: `docs/research/MING-DATONG-MULTI-YEAR-LEAP-RULE-VALIDATION-R1.json`  
Sample oracle: `docs/research/MING-DATONG-MULTI-YEAR-LEAP-SAMPLE-ORACLE-R1.json`  
Research-only harness: `scripts/research_ming_datong_multi_year_leap_validation_r1.py`

## 1. Two different questions must not be conflated

The 1569 primary `步氣朔` material contains `推閏餘分法`. Its `閏餘` / `閏限` comparison answers **whether the year contains an intercalary month**. It does not by itself say which numbered month is intercalary.

The month position is a second rule. The late-Ming reform report preserved in `明史` explicitly contrasts old Datong with the new method: old Datong places leap months by whether a lunar month has a Zhongqi, while the new method additionally examines exact conjunction ordering.

## 2. Primary leap-existence layer

The primary-facsimile rule is normalized as: form the source `閏餘` under `朔策`, compare with `閏限 = 186552.09`, and at/above the limit treat the year as intercalary.

This separates sampled leap years 1531, 1596 and 1629 from sampled non-leap years 1532, 1578, 1616 and 1639.

## 3. Old-Datong placement is civil-day based

12OY assigns Pingqi Zhongqi by source civil-day labels:

`new_moon_start_day <= zhongqi_day < next_new_moon_start_day`.

A lunar month with no Zhongqi repeats the preceding month number as the intercalary month.

In 1596, the relevant Zhongqi occurs before the next conjunction in exact time, but both occupy the same source civil day. The old day-level rule therefore leaves the preceding month without Zhongqi and reproduces **閏八月**, exactly as Xing Yunlu's Datong worked example states. A counterfactual exact-order comparator under the same Pingqi schedule yields leap ninth month. This illustrates the late-Ming statement that the new method additionally examines conjunction order; it is not presented as a historical 1596 new-calendar computation.

## 4. Multi-year replay

Seven source controls are replayed under all four 12OX research precision profiles:

- 1531: full 13-month comparison, leap 6
- 1532: full 12-month non-leap comparison
- 1578: official Qintianjian physical 12/12 month-page sequence, non-leap
- 1596: Ming-authorial worked-example leap 8 identity
- 1616: full 12-month non-leap comparison
- 1629: partial official-almanac time table through month 6, including leap 4
- 1639: partial official-almanac time table through month 6, non-leap

Result: `7 years × 4 profiles = 28 / 28 controls matched`.

## 5. Why G09 is not yet closed globally

A general Ming historical calendar must survive years where a true conjunction or Pingqi Zhongqi lies extremely close to a source-day boundary. Seven samples do not prove arbitrary-year stability.

Therefore `MD-G09-MULTI-YEAR-LEAP-GENERALIZATION` remains `OPEN_BLOCKING_GENERAL_ADAPTER`.

## 6. Next batch

**12OZ — full Ming-era boundary census.**

Sweep 1368–1644 under all four research precision profiles, detect profile-dependent month identities and day-boundary critical cases, then rank them for direct almanac/reign-record validation before any G09 closure or runtime activation.

