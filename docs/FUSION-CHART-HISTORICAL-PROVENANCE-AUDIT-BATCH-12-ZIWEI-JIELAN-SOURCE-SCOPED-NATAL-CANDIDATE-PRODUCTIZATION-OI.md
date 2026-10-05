# Historical Provenance Audit — Batch 12OI

Batch ID: `BATCH-12-ZIWEI-JIELAN-SOURCE-SCOPED-NATAL-CANDIDATE-PRODUCTIZATION-OI`

## Scope

12OI implements the Tier-1 decision from 12OH: expose the already existing Jielan 1581 source-scoped natal resolver as a read-only candidate product surface.

Historical source conclusions are unchanged. The productization closes three previously confirmed gaps:

- `HPA-ZIWEI-015` — Jielan Kui/Yue Geng-stem variant;
- `HPA-ZIWEI-016` — Jielan Fire/Bell 巳酉丑 start-family variant;
- `HPA-ZIWEI-022` — Jielan Mingzhu birth-year-branch basis.

## Product boundary

The public identity is `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATE-API-R1@1.0.0`, backed by the existing `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0` registry and `ZIWEI-JIELAN-1581-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0` resolver.

Only `kui_yue`, `fire_bell` and `mingzhu` are released. Dignity and Shenzhu remain excluded because their unresolved source semantics must not be smuggled through a broader resolver payload.

The endpoint binds its output to the exact combined manifest, Ziwei bundle, natal fact/computation hashes, registry hash and runtime hash. The Workbench renders those returned facts and contains no placement formulas.

`selection_status=PRESERVED_NOT_SELECTED`. No production Profile selector, winner, rank or chart mutation is added.

## Matrix effect

`HPA-ZIWEI-015`, `HPA-ZIWEI-016` and `HPA-ZIWEI-022` leave `MISSING_FROM_PRODUCT` because their source-scoped candidates are now publicly visible and auditable. Their historical candidate identities remain source-specific and do not replace the production methods.

After 12OI:

- Matrix: **222 / 222 audited**;
- current `MISSING_FROM_PRODUCT`: **7**;
- `HISTORICALLY_SUPPORTED`: **102**;
- historical candidate extensions: **11**;
- candidate registries/runtime resolvers: **3 / 3**;
- provenance defects: **43 / 43 repaired**;
- production default / winner / algorithm reopen: **unchanged / none / 0**.

## Next

**12OJ — HPA-ZIWEI-014 whole-table Four-Transformation source families and candidate readiness.**

Productization document: `docs/ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATE-PRODUCTIZATION-R1.md`.
Research record: `docs/research/ZIWEI-JIELAN-SOURCE-SCOPED-NATAL-CANDIDATE-PRODUCTIZATION-R1.json`.
