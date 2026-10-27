# Fusion Chart Historical Provenance & School Audit R1

## Batch 11J - Ming Datong 1569 Fixed-Point Precision Audit

Status: **COMPLETE FOR THE 1569 PRIMARY TABLE-GENERATION PRECISION MAP; DYNAMIC INTERPOLATION / D1 PRECISION GENERALIZATION REMAINS OPEN**

Batch ID: `BATCH-11-BAZI-MING-DATONG-FIXED-POINT-PRECISION-J`

This batch asks what fixed-point operators are actually required to reproduce the directly collated 1569 Zhou Xiang primary tables. It does not ask whether the general historical-calendar runtime is ready.

Primary-ledger closure is solar 185/185, lunar 遲疾 169/169 and lunar 行度 169/169, with zero within-edition variant or glyph-ambiguous rows.

The machine replay establishes four stage-scoped rules:

- 遲疾日率: floor to integral historical day-source units, 168/168; half-up matches only 90/168, so 78 rows discriminate.
- 損益捷法: truncate to four decimal source-second places, 168/168; half-up matches 92/168, so 76 rows discriminate.
- 遲/疾行度: generic mean-motion ± adjustment then ceiling to 1e-4 degree, 334/334; floor matches 0/334, half-up 154/334. Two central primary cells remain explicit overrides (limit 82 遲=1.0960; limit 85 疾=1.0960). All 336 visible cells match after overrides.
- 行度捷法: truncate reciprocal to 1e-7, 336/336; half-up matches 158/336, so 178 cells discriminate.

Solar three-difference accumulated/add/message values and lunar accumulated/adjacent 損益 relations match the primary at their stored fixed-point precision without adding a universal rounding operator.

Therefore:

`SINGLE_GLOBAL_ROUNDING_RULE = REJECTED_BY_PRIMARY_TABLE_EVIDENCE`

`TABLE_GENERATION_PRECISION_MAP = CLOSED_FOR_1569_PRIMARY_TABLES`

Xing Yunlu's 1596 `〈大統〉` example remains a local dynamic control: its longer raw 遲差 is printed as 4.546285 and its longer D1 quotient as 1526.64. These local truncations are not generalized to every dynamic calculation.

Volume 50's 1605 worked example is explicitly `〈授時〉`, not `〈大統〉`. It preserves unequal intermediate precision widths and is used only to reject a context-free “same author, same fixed width” assumption. It is not Datong production authority; its following 定望 line remains subject to image-level checking before stronger arithmetic conclusions.

Still open:

- dynamic Datong interpolation/D1 precision beyond the single 1596 worked example;
- cross-edition image-level variant causes;
- qishuo geographic/meridian reference;
- invalid-date/month-length addition semantics;
- multi-year leap-month behavior;
- ten-year Dayun recurrence.

The historical-calendar adapter remains fail-closed; no chart algorithm is reopened and no candidate is collapsed.


## Later explanatory alignment

A later explanatory witness strengthens the philological interpretation without changing the authority order. Mei Wending's Qing `《大統曆志》卷四` describes one lunar line-speed construction as `數止秒` and notes that any residue below seconds is collected upward into a second; in the alternate `布立成法` discussion it instead says values below seconds are discarded, while also preserving separate 83/84 transition treatment.

This aligns with the primary numeric result that different table stages use different fixed-point operators. It is not used to derive the 1569 values, overwrite the Zhou Xiang primary, or authorize runtime arithmetic. The directly collated 1569 ledger remains the decisive numeric evidence.
