# Historical Provenance Audit — Batch 12OK

## Scope

Batch ID: `BATCH-12-ZIWEI-FOUR-TRANSFORMATION-WHOLE-TABLE-CANDIDATE-PRODUCTIZATION-OK`

Target: `HPA-ZIWEI-014`.

12OJ closed deterministic candidate readiness. 12OK closes the remaining product-surface gap without selecting a historical winner.

## Product surface

The Workbench now exposes a read-only endpoint:

`POST /api/ziwei-four-transformation-candidates`

The caller supplies the ordinary chart request only. It does **not** select a candidate family. The backend derives the birth-year stem from the exact validated Ziwei bundle and returns both registered divergent candidates simultaneously.

The response binds source bundle hashes, natal FactHash/ComputationHash, registry hash and per-candidate runtime hashes.

## Whole-table firewall

The existing 12OJ constraints remain mandatory:

- `whole_table_only=true`;
- `cell_level_hybridization_allowed=false`;
- `selection_status=PRESERVED_NOT_SELECTED`.

The browser does not carry Four-Transformation table constants. It only renders backend assignments.

## Matrix effect

`HPA-ZIWEI-014` changes:

`MISSING_FROM_PRODUCT -> HISTORICALLY_SUPPORTED`

This status means the competing historical/school table families are now preserved, replayable and inspectable as source-scoped candidates. It does **not** mean received Fullbook or Zhongzhou has been selected over Jielan/current S08.

After 12OK:

- Matrix: **222 / 222 audited**
- HISTORICALLY_SUPPORTED: **103**
- current MISSING_FROM_PRODUCT: **6**
- candidate extensions: **13**
- candidate registries / runtime resolvers: **4 / 4**
- provenance defects: **43 / 43 repaired**
- algorithm reopens / candidate collapses: **0 / 0**

## Next

**12OL — re-rank the six remaining MISSING_FROM_PRODUCT rows and continue from the highest implementation-ready family.**
