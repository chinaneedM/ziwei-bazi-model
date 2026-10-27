# Fusion Chart Historical Provenance Audit R1 — Batch 11G

## Ming Datong historical time-coordinate audit

Status: **AUDITED / INTERNAL DAY–TIME COORDINATE SOURCE-CLOSED / 子正 COMPUTATIONAL DAY BOUNDARY CLOSED / GEOGRAPHIC QISHUO REFERENCE STILL UNRESOLVED / GENERAL ADAPTER FAIL-CLOSED / NO ALGORITHM REOPEN**

Batch 11F adjudicated the Ming official conjunction correction denominator as D1. Batch 11G closes another independent subproblem: what exactly do the historical `定朔` day fraction and clock labels mean?

## 1. Primary 1569 source

The Zhou Xiang Longqing 3 facsimile directly preserves `推合朔時刻法` on zero-based PDF page 41.

Its mechanical structure binds the event `小餘` to the historical 12-shichen / 100-ke clock:

- event small remainder is multiplied by twelve;
- the time count is anchored at `子正`;
- the half-shichen `初` label is handled at the half-unit threshold;
- residual fractions are converted into ke.

The same book's qishuo constants use a 10000-unit day.

## 2. Received-text unit corroboration

The received `《明史》` Datong procedure states:

```text
日周一萬 = 一百刻
一刻 = 一百分
一分 = 一百秒
```

and its `推發斂加時` restates the 12-shichen conversion from `子正`.

This is used as corroboration because the 1569 facsimile is the stronger direct witness.

## 3. Ming worked replay

Xing Yunlu's `萬曆二十四年…〈大統〉` worked example gives a concrete replay:

```text
定朔 = 15039.22 source units
small remainder = 5039.22
發斂 shortcut multiplier = 1.20
5039.22 × 1.20 = 6047.064
recorded result = 乙丑日午正初刻
```

The test fixture recomputes the source arithmetic rather than trusting the prose statement.

## 4. Computational day boundary

For this calendar-astronomy coordinate, `小餘=0` is anchored to `子正`. The late `子初` half-shichen occurs before the next `子正` rollover; surviving Datong calculations preserve the label `夜子初` for that pre-boundary interval.

Therefore the source-scoped historical conclusion is:

```text
MING_DATONG_COMPUTATIONAL_DAY_BOUNDARY=ZI_ZHENG
```

This is **not** a Bazi or Ziwei change-day rule. The repository now carries an explicit firewall:

```text
ASTROLOGICAL_DAY_BOUNDARY_INFERENCE=FORBIDDEN
```

The already-independent Bazi and Ziwei date/day policies remain untouched.

## 5. Geography must be separated from the internal clock

Ming evidence also shows that Nanjing and Beijing cannot be collapsed:

- official historical records distinguish their polar altitude, sunrise/sunset and clepsydra behavior;
- late-Ming testimony records the policy dispute over which values should be printed;
- international peer-reviewed reconstruction verifies location dependence in the Shoushi/Datong sunrise-sunset tables.

But none of those facts licenses the inference:

```text
Nanjing sunrise table -> therefore every qishuo small remainder uses Nanjing meridian
```

or the equivalent Beijing inference.

So Batch 11G leaves:

```text
MING_DATONG_QISHUO_GEOGRAPHIC_REFERENCE=UNRESOLVED
NO_IMPLICIT_UTC_OR_MODERN_TIMEZONE_MAPPING=TRUE
NO_INHERITANCE_FROM_SUNRISE_SUNSET_TABLE_LOCATION=TRUE
```

## 6. Overseas evidence expansion

The Library of Congress digitized `《大明嘉靖三年歲次甲申大統曆》` (1524) is now registered as another page-level official-almanac oracle target. This deliberately broadens the evidence pool beyond the already used Chinese/Taiwanese and Japanese holdings.

## 7. Remaining gates

The historical calendar adapter is still not executable. Remaining work includes:

1. identify the qishuo/conjunction geographic or meridian reference;
2. complete 1569 盈缩/迟疾 table transcription;
3. close interpolation, carry and source-unit semantics;
4. replay the source-derived D1 method to the 1578 oracle;
5. collate exact 1578 Qintianjian almanac pages;
6. close invalid-date/month-length arithmetic;
7. generalize leap-month and multi-year behavior;
8. reuse the same historical regime for ten-year Dayun recurrence.

Accordingly:

```text
HPA-DAYUN-CAL-002=MISSING_FROM_PRODUCT
HISTORICAL_CALENDAR_ARITHMETIC_IMPLEMENTED=NO
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```
