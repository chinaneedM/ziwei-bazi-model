# Fusion Chart Historical Provenance Audit R1 — Batch 08B

## Ziwei temporal frames: flow-year, Five-Tigers month Ganzhi, flow-day, flow-hour wording split, leap month

Status: **AUDITED / PHILOLOGICAL DECOMPOSITION / TWO SOURCE-CLOSED PRODUCT GAPS / NO ALGORITHM REOPEN**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=8
```

## 1. Philological method used

Batch 08B is the first temporal batch explicitly applying the repository's 训诂 rule.

Surface wording is not treated as mechanical identity. In particular:

- `月上起初一` is read in the layered syntax of the sentence as “on/from the already-established month palace, establish day 1”;
- `日上起子时` correspondingly means “on/from the established day palace, establish Zi hour”;
- `流日子宫起子时` is treated as a near-equivalent later wording when its sentence context clearly refers to the flow-day palace;
- `命盘的子垣起子时` is **not** silently normalized into the same rule, because it mechanically points to the fixed branch-labelled 子 palace.

Therefore the early layered-hour method and the fixed-branch case method remain separate candidates.

## 2. Early-print temporal chain

1581 《新刻纂集紫微斗数捷览》 chapter 《安流年斗君法》 gives one compact layered chain:

- the flow-year TaiSui palace anchors the year;
- the annual Doujun determines first-month palace and months proceed forward;
- on the month palace, day 1 begins and days proceed forward;
- on the day palace, Zi hour begins and hours proceed forward.

Current runtime already matches the first three relevant geometries: annual active palace = target-year branch palace; regular flow-month sequence from Doujun; flow-day active palace = monthly active + lunar day - 1.

The fourth geometry, day-anchored flow-hour active palace, is source-closed but not emitted by runtime.

## 3. Five-Tigers / 五虎遁

《五行精纪》第二十八卷《起月建例》 preserves the complete five-group year-stem-to-Yin-month-stem mnemonic. Current `month_ganzhi` is an exact table realization.

This rule is separated from month-boundary doctrine. It maps a supplied year stem and regular lunar-month ordinal; it does not by itself decide solar-term versus lunar month boundaries in other systems.

## 4. Flow-hour dispute

### Candidate A — 1581 day-anchored sequence

`日上起子时皆顺行`

Mechanical reading: Zi hour active palace = current flow-day active palace; each later hour advances by the hour-branch ordinal.

This candidate is currently **MISSING_FROM_PRODUCT**.

### Candidate B — Zhongzhou fixed-branch case wording

Modern Zhongzhou material also contains `命盘的子垣起子时；丑垣起丑时……` and a worked case that puts 午时命宫 at 午.

Current runtime matches this fixed-branch case method exactly, while separately preserving Luoyang mean-solar-time and local-apparent-solar-time candidates.

The two active-address methods are not collapsed. Time standard and active-palace method are orthogonal candidate dimensions.

### Safe productization condition

The 1581 candidate must not be added by passing one shared daily palace into both time-standard candidates. If the two time standards resolve different effective dates around a boundary, each must bind to its own correctly resolved month/day parent before the day-anchored hour palace is computed.

## 5. Leap month

S10 and Wang Tingzhi's Zhongzhou teaching preserve a complete leap-month method: days 1–15 belong to the preceding month; day 16 through month end belong to the following month; flow-day palace progression does not reset.

Therefore the old status `SOURCE_INSUFFICIENT` is obsolete. The runtime still reports `UNRESOLVED_NOT_GENERATED`, so this is now classified as **MISSING_FROM_PRODUCT**, specifically a source-closed Zhongzhou school candidate. It must not silently become the universal default.

## 6. New granular rows

- HPA-ZTEMP-001 flow-year TaiSui active palace;
- HPA-ZTEMP-002 Five-Tigers month Ganzhi;
- HPA-ZTEMP-003 flow-day active palace;
- HPA-ZTEMP-004 1581 day-anchored flow-hour candidate;
- HPA-ZTEMP-005 Zhongzhou fixed-branch flow-hour case method;
- HPA-ZTEMP-006 Zhongzhou leap-month half-split candidate.

## 7. Accounting

```text
TOTAL_MATRIX_ROWS=159
TOTAL_AUDITED_ROWS=118
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=8
NEW_SOURCE_CLOSED_PRODUCT_GAPS=2
```

The two new product gaps are candidates, not evidence that the closed production default is wrong.
