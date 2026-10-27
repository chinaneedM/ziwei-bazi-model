# Fusion Chart Historical Provenance Audit R1 — Batch 12AI

## Ziwei late-Zi historical time-coordinate narrowing

Status: **HISTORICAL CLOCK FAMILY NARROWED / OBSERVATIONAL SOLAR-STELLAR BASIS SUPPORTED / CIVIL TIME NOT PROMOTED / LOCAL APPARENT SOLAR IS STRONGEST DAYTIME MODERN TRANSLATION / NATAL RUNTIME BINDING STILL OPEN / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AI addresses the remaining time-standard blocker for `HPA-ZDATE-006`. It does **not** ask again what `上五刻 / 下五刻` mean; Batch 12B already closed their upper/lower half-shichen orientation. The question here is narrower:

> Which modern coordinate, if any, may faithfully realize the historical `时刻` used by the Fullbook late-Zi rule?

The answer is narrowed but not fully closed.

## 2. Machine probe

Controlling workflow: `34322850489`  
Artifact: `10092539912`  
ZIP SHA-256: `9e3151f558b6425586fc2e2c593f5a01f82529f42f6cbd7e8f3e3973fc6df98f`

The exact-head probe fetched three public witnesses successfully:

- 《明史·天文志》 time-determination chapter — response SHA-256 `157eac2885f6bd3e6c72899f90539e4dd817cf63099c6e17508a8fc419293c16`
- 《明史·历志》 geographic gnomon/clepsydra passage — response SHA-256 `9c70e872519a96ff0bf034bb53a760538e574c99cbdb331b75457fb1c3405f7f`
- U.S. Naval Observatory `The Equation of Time` — response SHA-256 `ae81510e2c00f993413f0593c4706836c6635b57a4b2eac7e11b7de85deee768`

No authentication or access bypass was used.

## 3. Ming received institutional timekeeping

The reviewed 《明史·天文志》 passages distinguish the **fundamental determination of time** from the maintenance of a clock:

- the clepsydra must be calibrated at local noon and is described as supplementary when solar/astronomical instruments cannot be used;
- a correctly aligned sundial obtains the “correct time of Heaven” from daytime solar observation;
- nighttime time can be read from near-polar stars with a star instrument;
- the Xu Guangqi/Li Tianjing discussion explicitly treats Sun and stars as the fundamental reference instead of a merely human-adjusted clock.

This is a received dynastic-history witness to Ming institutional practice. It is **not** imported as Ziwei doctrine.

## 4. Geography is intrinsic

The reviewed 《明史·历志》 passage explicitly states that gnomon/clepsydra standards vary with north-south geography and polar altitude, and distinguishes Dadu from Nanjing.

Therefore a premodern `时刻` cannot be silently identified with one modern zone clock for all longitudes.

## 5. Modern coordinate translation

USNO provides the modern astronomical bridge:

- a calibrated sundial at a location reads **apparent solar time** from the true Sun and local meridian;
- local mean solar time instead uses the fictitious mean Sun;
- civil time is a zone system and is not identical to local solar time except under limited meridian conditions.

Accordingly Batch 12AI narrows, but does not collapse, the candidate space:

```text
PREMODERN_CIVIL_ZONE_TIME_AS_SOURCE_CLOCK=NOT_SUPPORTED
LOCAL_MEAN_SOLAR_TIME=DIRECT_INSTRUMENT_OUTPUT_NOT_OBSERVED_IN_REVIEWED_MING_DINGSHI_PASSAGES
LOCAL_APPARENT_SOLAR_TIME=STRONGEST_MODERN_DAYTIME_TRANSLATION_OF_SUNDIAL_READOUT
```

This is **not** yet equivalent to:

```text
ZIWEI_NATAL_RUNTIME_TIME_STANDARD=LOCAL_APPARENT_SOLAR_TIME
```

because the remaining bridge is source-specific.

## 6. Remaining source gates

Three independent questions remain:

1. Does the Fullbook/Nanyangtang natal-hour rule itself inherit this institutional observational clock regime?
2. Is historical nighttime star/clepsydra `时刻` mechanically equivalent to the current runtime's local-apparent-solar clock throughout the 23:00–01:00 interval?
3. Is natal `时刻` evaluated at the birthplace/local observation site, or at some school/institutional reference coordinate?

Until these close:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=PARTIALLY_NARROWED_NOT_CLOSED
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
```

## 7. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=10_CONFIRMED_10_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 8. Machine evidence

`docs/research/ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json`
