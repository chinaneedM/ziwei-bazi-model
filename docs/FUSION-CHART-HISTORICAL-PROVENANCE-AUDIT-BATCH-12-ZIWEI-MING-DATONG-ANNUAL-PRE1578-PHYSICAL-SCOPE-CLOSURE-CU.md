# Fusion Chart Historical Provenance Audit — Batch 12CU

## Scope

This batch closes a specific pending route left by Batches 12CQ and 12CT: whether four already-acquired, securely dated pre-1578 Ming official `大統曆` annual calendars directly expose a `晨昏分 / 日出入 / 晝夜刻` numerical table capable of carrying the 1578 `《三命通會》` seasonal fingerprint.

This is a **four-object physical-scope closure**, not a claim that all Ming Datong annual calendars lack such material.

## 1. Physical evidence reused without re-acquisition

Existing workflow:

```text
.github/workflows/audit-ncl-ming-datong-annual-pre1578.yml
run = 35101414335
artifact = 10448114363
artifact name = ncl-ming-datong-annual-pre1578-physical
artifact digest = sha256:f56cfab2e5e51ac33e72dc08bb1b901be5c1b5ea0091726a60b1a888e13253b9
```

The artifact was still live and was reused directly. No second acquisition and no duplicate evidentiary vote were created.

The four physical objects are:

| source | dated title | edition metadata | pages | PDF SHA-256 |
|---|---|---|---:|---|
| NCL-06283 | `大明永樂十五年大統曆` (1417) | 明欽天監刊本 | 18 | `3a6511b01c07e50f70ea3b8ccda4831604122703874a61a358564ee0e28b813c` |
| NCL-06284 | `大明景泰三年歲次壬申大統曆` (1452) | 明欽天監刊本 | 49 | `683bf93900aa90b57ef2c83e70b87f7aa927933cf0b607005daaae57eff71a1c` |
| NCL-06289 | `大明正德元年大統曆` (1506) | 明欽天監刊本 | 29 | `f42c04ff34847bce35cf0a28db761b9083db6b215cf2a2e300e69c34ed1fa2d7` |
| NCL-06302 | `大明嘉靖二十二年歲次癸卯大統曆` (1543) | 明欽天監刊本 | 24 | `3a1de17f7b2f63892472520900e9ee9dba15d7a19d09d8a0a91bf6b8ab15d6b6` |

Total direct visual scope: **120 rendered physical pages at 200 dpi**.

## 2. Review method and OCR firewall

The pre-existing locator workflow used OCR only to propose page candidates. It produced essentially no strong target locator. That weakness was not converted into a negative textual claim.

For this batch the complete 120-page image set was reviewed visually at page-layout level. Pages whose layout departs from the ordinary monthly-calendar form were then enlarged and reviewed separately, including:

- NCL-06283 p10 and pp17-18;
- NCL-06284 pp41 and 43;
- NCL-06289 pp21-23;
- NCL-06302 p21.

OCR has **no authority** for the final adjudication below.

The negative result is deliberately scoped to an independently identifiable target table. It is **not** a glyph-by-glyph claim that no isolated character such as `晝`, `夜`, `晨`, `昏` or `刻` occurs anywhere inside every daily column.

## 3. Direct visual result

The four witnesses overwhelmingly consist of monthly daily-almanac pages, with front/back matter and miscellaneous annual diagrams/tables. The structurally unusual endmatter pages were individually enlarged.

Across the reviewed physical surfaces, no independently identifiable table was observed that could be bound as:

```text
晨昏分立成
日出入數值表
晝夜刻數值表
```

and no table surface was observed that directly exposes the combined Sanming target fingerprint:

```text
夏至 59/41
+ Sanming-like intermediate integer ladder
+ intra-term change-day instructions comparable to
  大寒 43/57 -> 十三後日 -> 44/56
  雨水 47/53 -> 後四日 -> 48/52
```

Therefore these four public annual-calendar objects cannot presently serve as the missing direct page-level bridge to the 1578 display.

## 4. What this does and does not prove

```text
FOUR_SPECIFIC_ANNUAL_CALENDARS_TARGET_TABLE = NOT_OBSERVED
FOUR_SPECIFIC_ROUTES_AS_DIRECT_SANMING_PARENT = NOT_ESTABLISHED
WHOLE_MING_DATONG_ANNUAL_TRADITION_ABSENCE = NOT_AUTHORIZED
OTHER_ANNUAL_YEARS / OTHER_COPIES / OTHER_FASCICLES = UNRESOLVED
```

This matters because Batches 12CF and 12CL already established the Nanjing 59-ke regional/policy layer, while Batch 12CG mechanically replayed several Sanming integer anchors from the Nanjing daily curve. The remaining problem is no longer simply “find a dated Ming Datong calendar”; it is to locate the **specific computational carrier or table family** that turns that regional curve into the displayed seasonal integer ladder and its change-day thresholds.

## 5. Transmission impact

No positive graph edge is added.

The four dated annual calendars remain valid Datong historical witnesses, but the reviewed surfaces do not expose the target table. Consequently:

```text
independent numeric vote increment = 0
transmission edge increment = 0
recension vote increment = 0
```

This is a negative scope closure only and does not weaken already established Nanjing/Datong continuity evidence outside these four physical objects.

## 6. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_RUNTIME_CANDIDATE=false
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
CANDIDATE_COLLAPSE=NONE
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No historical-audit Matrix count changes are authorized by this batch.

## 7. Next gate

The highest-value route now shifts from generic annual calendars to the **original `《大統曆法通軌》` computational carrier**:

1. bind an independent directly readable `大統曆法通軌` physical witness, prioritizing the Kyujanggak Joseon movable-type recension and the NLC Ming-manuscript route;
2. locate `晨昏立成 / 晨昏分` at page level;
3. visually bind the physical cells before any numerical use;
4. test the resulting daily/seasonal values against the exact 1578 pp134–136 target, including 59/41, intermediate anchors, change days and the unresolved historical quantization threshold;
5. keep `大統曆法通軌` distinct from the corrected Batch 12CO `DIC_A3_000150 / 大統曆日通軌` record unless an explicit bibliographic bridge is demonstrated.

Research record:

`docs/research/ZIWEI-MING-DATONG-ANNUAL-PRE1578-PHYSICAL-SCOPE-CLOSURE-R1.json`
