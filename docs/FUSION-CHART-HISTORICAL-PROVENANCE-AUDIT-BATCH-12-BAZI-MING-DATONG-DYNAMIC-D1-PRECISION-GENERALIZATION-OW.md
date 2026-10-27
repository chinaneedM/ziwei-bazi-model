# Fusion Chart Historical Provenance Audit R1 — Batch 12OW

## Ming Datong dynamic D1 precision generalization

Status: **CROSS-YEAR FINAL-TIME VALIDATION CLOSED / DYNAMIC INTERMEDIATE PRECISION PROFILE STILL OPEN / RUNTIME FAIL-CLOSED**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
D1_FINAL_TIME_OPERATIONAL_VALIDATION=56_OF_56_IN_PRINTED_BINS
D2_COMPARATOR=8_OF_56_IN_PRINTED_BINS
DYNAMIC_INTERMEDIATE_PRECISION_POLICY=OPEN
G05_STATUS=OPEN_BLOCKING_GENERAL_ADAPTER
RUNTIME_SELECTION_AUTHORIZED=NO
```

Research record: `docs/research/MING-DATONG-DYNAMIC-D1-PRECISION-GENERALIZATION-R1.json`  
Machine fixture: `docs/research/MING-DATONG-D1-56-CONJUNCTION-VALIDATION-R1.json`

## 1. Why 12OW does not simply copy the 1596 truncations

The 1596 `古今律曆考` Datong worked example is a genuine local dynamic arithmetic control: its within-limit lunar difference is printed after truncation to six decimal degree places, and its D1 correction is printed after truncation to two decimal source units.

That is strong evidence for that worked example. It is not yet a source rule saying all years and all dynamic stages use those exact widths.

## 2. New cross-year final-time evidence

The public comparison source has a fixed GitHub upstream. 12OW parses its first conjunction-time table directly from commit `d6aae82b63b79a6f8659ea3e064024b7d8ac3077`, blob `4c55fdab0c1352681e125f7cd6cc711bcf6614c5`, rather than hand-copying the numbers.

The resulting fixture contains 56 conjunction-time observations from six surviving Ming Datong almanac years: 1531, 1532, 1604, 1616, 1629 and 1639.

Machine result:

- D1 inside printed almanac interval: **56 / 56**
- D2 inside printed interval: **8 / 56**
- D2 outside interval: **48 / 56**
- D2 changes the sexagenary day in the 1639 fifth-month near-midnight case.

The narrowest published control is 1639 month 4, `巳正四刻`: the published decimal representation spans 0.0016 day, i.e. **2.304 minutes full width**, and D1 lies inside while D2 lies outside.

This is much stronger than a day-label-only oracle for identifying the operational D1 path.

## 3. Why G05 still stays open

These surviving almanacs expose the **final conjunction time bin**. They do not expose the historical intermediate residues after each dynamic interpolation/division.

Therefore final-time agreement cannot by itself tell us whether the Ming computation used full precision until final output, exactly the 1596 local six-decimal/two-decimal truncations, half-up at those same widths, truncation only at stored table widths, or another source-bounded sequence that lands in the same printed time bin.

The 1578 chain is also not a dynamic precision discriminator: its day-boundary margins are much wider than the sub-stage uncertainty under discussion.

The 1605 Shoushi example remains a negative generalization control, not Datong authority. Later Mei Wending precision wording remains explanatory, not a Ming dynamic rule.

## 4. 1527 peer-reviewed reconstruction boundary

The registered Li Yong 2011 study remains valuable cross-year reconstruction evidence. But the later explicit conjunction-time comparison notes that the 2011 paper did not compare Ming almanac conjunction times. It therefore cannot supply the missing historical intermediate precision operator.

No authority layer is upgraded by citation count.

## 5. Gate result

`MD-G05-DYNAMIC-D1-PRECISION-GENERALIZATION` remains:

`OPEN_BLOCKING_GENERAL_ADAPTER`.

What 12OW closes is the narrower subclaim:

`D1_CROSS_YEAR_FINAL_TIME_OPERATIONAL_CONSISTENCY = CLOSED`.

The required historical-calendar runtime result remains fail-closed.

## 6. Next batch

**12OX — 56-bin precision-profile sensitivity harness.**

Research-only replay must compare at least:

1. full decimal precision until final output;
2. the 1596 local six-decimal Chi-difference + two-decimal D1-correction truncation;
3. half-up at those same widths;
4. truncation only at stored table widths.

If all plausible profiles fit the printed bins, the final-time corpus cannot discriminate the historical precision rule and G05 remains open. If the corpus discriminates profiles, numerical fit still must not be mistaken for primary historical wording.

