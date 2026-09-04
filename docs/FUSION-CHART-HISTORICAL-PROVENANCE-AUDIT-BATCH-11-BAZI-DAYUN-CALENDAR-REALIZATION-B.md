# Fusion Chart Historical Provenance Audit R1 — Batch 11B

## Bazi Dayun calendar realization and ten-year handover boundaries

Status: **AUDITED / HISTORICAL CALENDARIZED SCHEDULE FAMILY IDENTIFIED / FAIL-CLOSED PRODUCT GAP / NO ALGORITHM REOPEN**

## 1. Three different questions must not be conflated

1. Which Jie is used and how the birth-to-Jie interval is measured.
2. How that interval becomes a symbolic luck age.
3. How the symbolic age becomes a real calendar handover instant, and how later ten-year Dayun boundaries are realized.

The first two have substantial source closure. The third is where calendar systems diverge.

## 2. Historical discrete conversion

Song 《五行精纪》 and Ming 《三命通会》 preserve actual elapsed day/shichen counting and the three-days-one-year family. At whole-shichen resolution, the source coordinate closes the 360/30/10 conversion.

The current continuous runtime agrees at that source resolution, but interpolation to arbitrary microseconds is a modern engineering extension.

## 3. Classical lunisolar calendarization

《三命通会》 goes beyond the symbolic ratio. Its worked discussion explicitly adjusts the real handover date for small months and a leap month and then says later luck frames change after ten anniversaries.

This is a source-closed rule family, but it is not safely executable with the current calendar adapter: ChineseCalendarEngine deliberately implements the modern Chinese calendar for 1901–2100 under Beijing Standard Time and explicitly excludes historical calendar regimes.

Therefore the historical calendarized schedule is MISSING_FROM_PRODUCT, not silently approximated.

## 4. Later Qianli method

《千里命稿》 gives a separate later operational method: advance the whole calendar age, then add converted remainder days to obtain an exact year/month/day/hour handover. It also gives recurring exchange-date examples.

This remains a distinct source-scoped candidate and is not equated with either the Ming lunisolar adjustment or Wenzhen compatibility behavior.

## 5. Current runtime profiles

The released runtime remains valid as explicitly modern profiles:

- continuous: UTC interval ×120 at microsecond precision;
- Wenzhen compatibility: Gregorian month displacement on fixed UTC+8;
- Dayun boundaries: proleptic-Gregorian ten-year anniversaries in UTC or fixed China standard time.

None is relabeled as ancient calendar authority.

## 6. Candidate-family accounting

The classical/later calendarized Dayun schedule is counted as one newly identified candidate family with multiple subrules/variants. First handover and later ten-year boundaries are not double-counted as separate candidate families.

```text
TOTAL_MATRIX_ROWS=197
TOTAL_AUDITED_ROWS=165
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=13
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```
