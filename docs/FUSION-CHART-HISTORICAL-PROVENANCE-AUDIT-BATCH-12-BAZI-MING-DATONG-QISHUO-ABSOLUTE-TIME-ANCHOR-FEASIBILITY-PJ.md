# Fusion Chart Historical Provenance Audit R1 — Batch 12PJ

## Qishuo absolute-time anchor feasibility and uncertainty

Status: **MODERN ABSOLUTE EPHEMERIS FEASIBLE / DELTA-T NOT DOMINANT AT 1500–1600 / HISTORICAL CLOCK-STANDARD SEMANTICS UNRESOLVED / MD-G03 OPEN**

12PI proved that internal D1 ↔ official-almanac clock-bin pairs cannot identify their absolute longitude. 12PJ asks whether an independent modern astronomical anchor is precise enough to become a useful diagnostic.

JPL's DE431 spans years -13200 to +17191 and is specifically the long lunar integration suited to times more than a few centuries in the past, so the Ming target period is technically covered.

NASA's historical ΔT material places the typical uncertainty in 1300–1600 at about 20 seconds. The modern Beijing–Nanjing longitude signal used in the existing diagnostic is about 592 seconds. Thus ΔT uncertainty is not the dominant city-level discriminator for this period.

The larger unresolved issue is historical time-standard semantics. USNO defines equation of time as apparent solar time minus mean solar time and notes that the difference can reach about 16 minutes. That is larger than the Beijing–Nanjing longitude signal. This is not random ephemeris error; it is a coordinate-definition difference.

Batch 11G source-closes Datong's internal day boundary at 子正 and its 100-ke coordinate, but it does not source-close whether that qishuo clock is local apparent solar time, local mean solar time, calibrated clepsydra time, or another conventional computational coordinate, nor to which longitude it is attached.

Therefore a modern ephemeris experiment is technically feasible but not yet historically admissible as a meridian selector.

MD-G03 remains open. No runtime/default/candidate selection changes.

Next: 12PK — source-close the absolute time-standard semantics of qishuo 子正/刻 before numeric longitude fitting.

Research: docs/research/MING-DATONG-QISHUO-ABSOLUTE-TIME-ANCHOR-FEASIBILITY-R1.json
