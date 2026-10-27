# Historical Provenance Audit — Batch 12OO

## Scope

Target: `HPA-ZIWEI-018` — 1581 Jielan historical dignity table.

12OM closed internal CH70 raw-lexeme candidate readiness. 12ON closed CH69↔CH70 300-cell source cross-collation. 12OO closes the remaining **product-surface gap** only.

## Product surface

A new read-only endpoint is released:

`POST /api/ziwei-jielan-1581-dignity-candidate`

It returns:

- exact combined / Ziwei source hashes;
- historical registry and runtime hashes;
- all 300 CH70 source-lexeme rows;
- all 300 CH69↔CH70 cross-collation rows;
- frozen relation counts;
- explicit non-selection and non-coercion flags.

The Workbench adds a read-only panel that groups backend rows by star/entity and shows the twelve branches. No historical source tables or comparison formulas are embedded in browser JavaScript.

## Firewall

12OO does not alter the production dignity registry.

The following remain false:

- production grade mapping present;
- CH69 used to fill CH70;
- CH70 used to overwrite CH69;
- historical winner selected;
- production profile changed;
- chart algorithm reopened.

The CH70 source anomalies and CH69 unresolved text remain visible evidence.

## Matrix result

`HPA-ZIWEI-018` changes:

`MISSING_FROM_PRODUCT -> HISTORICALLY_SUPPORTED`

The reason is product completeness, not a new historical winner: the source family was already historically attested; the missing product representation is now present.

After 12OO:

- Matrix: **222 / 222 audited**
- HISTORICALLY_SUPPORTED: **104**
- MISSING_FROM_PRODUCT: **5**
- candidate extensions: **14**
- candidate registries / runtime resolvers: **5 / 5**
- provenance defects: **43 / 43**
- algorithm reopens: **0**

## Next

**12OP — HPA-ZT-015 leap-month day-one daily-origin geometry / historical candidate closure.**

Productization contract: `docs/ZIWEI-JIELAN-DIGNITY-HISTORICAL-CANDIDATE-PRODUCTIZATION-R1.md`.
