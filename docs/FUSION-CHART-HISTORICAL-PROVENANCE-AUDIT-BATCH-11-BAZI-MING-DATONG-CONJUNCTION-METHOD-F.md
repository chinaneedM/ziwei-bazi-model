# Fusion Chart Historical Provenance Audit R1 — Batch 11F

## Ming Datong conjunction-method adjudication

Status: **AUDITED / D1 HISTORICALLY ADJUDICATED FOR MING OFFICIAL PRODUCTION / D2 DEMOTED TO LATER RECEIVED-TEXT VARIANT / GENERAL ADAPTER STILL FAIL-CLOSED / NO ALGORITHM REOPEN**

Batch 11E closed a machine-auditable 1578 month-start oracle. Batch 11F resolves a textual contradiction that directly affects how a future Ming Datong adapter must calculate the correction from mean conjunction to true conjunction.

## 1. The conflict

Two formula families circulate in received material:

- **D1** — divide the correction by the corresponding lunar `迟/疾行度`;
- **D2** — subtract the solar 820 unit from the lunar rate to form `定限度`, then divide by that.

These are not merely two modern implementation choices. They reflect a real transmission conflict.

## 2. 1569 primary Ming facsimile closes D1

The Zhou Xiang `《大明大統曆法》` Longqing 3 (1569) facsimile directly preserves `步氣朔卷第一`, the source constants, table structure and calculation methods.

Most importantly, zero-based PDF page 32 contains `推加減差分法`. Its mechanical instruction is unambiguous:

1. combine or subtract `盈缩差` and `迟疾差` according to same/different sign;
2. multiply the residual by 820;
3. in a 迟历 case divide by the corresponding `迟行度`;
4. in a 疾历 case divide by the corresponding `疾行度`;
5. the quotient is the conjunction `加减差`.

This is D1. It is not inferred from a modern reconstruction.

The same facsimile also preserves the upstream `推遲疾差度分法`, showing how the 迟/疾 table values are interpolated before the conjunction correction.

## 3. Independent Ming worked example

Xing Yunlu's `《古今律历考》` volume 49 explicitly labels its worked case `万历二十四年丙申岁闰八月朔日食历〈大统〉`.

At `求加减差`, the worked arithmetic multiplies the residual correction by 820 and divides by `迟行度一度一五二六`, then applies the resulting `加差` to `经朔` to obtain `定朔`.

The surviving digital text is a later Siku recension, so it is not ranked above the 1569 facsimile. It is nevertheless an independent Ming-authorial worked witness that corroborates D1.

## 4. Where D2 comes from

The Qing-compiled `《明史·历志》` received Datong text instead says to subtract 820 from `迟疾限行度` to create `定限度`, and then use that as the divisor.

That reading is preserved in the provenance record. It is not deleted. But chronology and actual Ming evidence no longer justify treating it as an equal production candidate.

## 5. Official-almanac validation

Modern computational validation checks D1 and D2 against 56 conjunction-time entries preserved in six official Ming Datong almanacs from 1531, 1532, 1604, 1616, 1629 and 1639.

The reported result is:

- D1: 56/56 within the printed official-almanac time bins;
- D2: most values outside those bins;
- one near-midnight D2 result crosses to the wrong calendar day.

This validation does not create historical authority by itself. Its role is stronger: it independently tests which transmitted formula reproduces contemporary operational artifacts. It agrees with the 1569 primary facsimile and the Ming worked example.

## 6. Adjudication

The evidence hierarchy is now convergent:

```text
1569 Ming primary facsimile -> D1
Ming Xing Yunlu worked Datong example -> D1
surviving official Ming almanac conjunction times -> D1
Qing-compiled Ming-shi received text -> D2
```

Therefore:

```text
MING_DATONG_CONJUNCTION_METHOD_HISTORICAL_ADJUDICATION=D1_SHOUSHI_STYLE_CHIJIXINGDU
D2_DISPOSITION=LATER_RECEIVED_TEXT_VARIANT_NOT_EQUAL_PRODUCTION_CANDIDATE
RUNTIME_SELECTION_AUTHORIZED=NO
```

This is exactly the distinction required by the research policy: genuine disputes remain candidates, but a contradicted transmission reading is not kept artificially equal after primary wording, independent Ming worked evidence and operational artifacts converge.

## 7. Why runtime remains fail-closed

Closing the conjunction denominator is only one subrule. A source-faithful historical calendar adapter still requires:

1. complete 1569 `盈缩` and `迟疾` table transcription;
2. exact interpolation, carry and source-unit semantics;
3. full D1 replay from source constants to the Batch 11E 1578 month-start oracle;
4. exact 1578 Qintianjian almanac page collation;
5. historical day boundary and clock coordinate;
6. enforcement/geographic/institutional scope;
7. invalid-date behavior;
8. multi-year leap-month reconstruction;
9. same-regime ten-year Dayun recurrence.

Accordingly:

```text
HPA-DAYUN-CAL-002=MISSING_FROM_PRODUCT
HISTORICAL_CALENDAR_ARITHMETIC_IMPLEMENTED=NO
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

## 8. Research-method continuity

Batch 11F also hardens the repository authority policy:

- research remains open-ended across editions, regions, languages and disciplines;
- stopping after the first usable source is forbidden when material additional witnesses remain searchable;
- contradictions are adjudicated by evidence weight, not source count;
- candidate preservation is for genuine unresolved/school differences, not demonstrated transmission errors.

These rules are now CI-gated through the continuity state.
