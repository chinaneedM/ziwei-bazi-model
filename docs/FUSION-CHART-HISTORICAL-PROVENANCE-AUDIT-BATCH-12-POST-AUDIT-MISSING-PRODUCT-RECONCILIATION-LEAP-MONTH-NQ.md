# Fusion Chart Historical Provenance Audit R1 — Batch 12NQ

## Post-audit reconciliation — HPA-ZT-015 Leap-month temporal frames

Status: **MISSING_FROM_PRODUCT PRESERVED / PARTIAL CANDIDATE PRODUCTIZATION ACKNOWLEDGED / STALE PROPOSED ACTION REPAIRED / NO ALGORITHM REOPEN**

Batch 12NP completed the current Historical Provenance Matrix at **220/220 audited**. 12NQ begins a second pass over the 10 rows still marked `MISSING_FROM_PRODUCT`, because later productization may have made some old gap descriptions stale.

The first target is `HPA-ZT-015 — Leap-month temporal frames`.

### 1. Why the row looked stale

HPA-ZT-015 still said:

- regular month generator marks leap-month policy unresolved;
- source method is mechanically complete but runtime still does not generate it;
- proposed action: implement a Zhongzhou leap-month temporal candidate.

That description predates the later temporal historical-candidate productization.

Current runtime now contains:

`ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1`

under:

`ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1@1.0.0`

and:

`ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1@1.0.0`.

Its selection status is:

`PRESERVED_NOT_SELECTED`.

### 2. What is already productized

The source-scoped candidate deterministically records:

- leap days 1–15 → preceding regular month;
- leap days 16–end → following regular month;
- corresponding temporal-month identity/Ganzhi continuity;
- source ID/refs;
- registry/runtime identity;
- authority status;
- candidate hash.

The Shared Ziwei Selector Projection emits it through:

`leap_month_method_candidates`.

The read-only Workbench consumes that returned array; browser code does not derive its own leap-month formula.

Therefore the old instruction “implement an explicit Zhongzhou leap-month temporal candidate” is already satisfied.

### 3. What remains deliberately fail-closed

The candidate API itself explicitly says that the cited Zhongzhou sentence does not close the leap-month **day-one flow-day origin geometry**.

Consequently the ordinary projection still returns:

`monthly_projection_status=LEAP_MONTH_UNRESOLVED_NO_FRAME`

and:

`daily_projection_status=PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME`.

The candidate further records:

`daily_origin_semantics=NOT_CLOSED_BY_THIS_MONTH_POLICY_API`

and:

`MONTH_ASSIGNMENT_CANDIDATE_ONLY_DAILY_GEOMETRY_REMAINS_FAIL_CLOSED`.

So there is still no source-authorized complete leap-month daily active palace / full temporal frame.

### 4. Relationship to HPA-ZTEMP-006

The Matrix already has a later, more precise row:

`HPA-ZTEMP-006 — Zhongzhou leap-month half-split temporal candidate`

with status:

`SUPPORTED_BUT_SCHOOL_SPECIFIC`.

That row correctly describes the **already productized source-scoped month-assignment candidate**.

HPA-ZT-015 is broader: **complete leap-month temporal frames**.

Keeping both rows is valid only if they are scoped separately:

- HPA-ZTEMP-006 = productized school-scoped half-split candidate;
- HPA-ZT-015 = remaining complete-frame/day-origin product gap.

This reconciliation makes that distinction explicit and avoids double-counting “implement the half split” as still missing.

### 5. PROV-DEFECT-036

Confirmed:

`PROV-DEFECT-036=HPA_ZT_015_STALE_PRODUCT_GAP_DESCRIPTION_AFTER_ZHONGZHOU_HALF_SPLIT_CANDIDATE_PRODUCTIZATION`

Repair:

- keep `HPA-ZT-015.audit_status=MISSING_FROM_PRODUCT`;
- update current implementation to acknowledge the released candidate;
- replace the obsolete “implement half-split candidate” action with the actual remaining work:
  - close day-one flow-day origin;
  - reconstruct full daily active-address geometry;
  - research competing leap-month methods;
  - keep ordinary monthly/daily fields fail-closed until source scope closes.

No runtime, schema, hash, candidate-selection or chart algorithm changed.

### 6. Accounting

- Matrix rows: **220**
- audited: **220**
- current `MISSING_FROM_PRODUCT`: **10 → 10**
- provenance defects: **35 → 36 confirmed / 35 → 36 repaired**
- chart algorithm defects: **0**
- algorithm reopens: **0**
- candidate collapses: **0**

`transmission_impact=NONE`.

Next: **12NR** — reconcile `HPA-ZIWEI-015`, `HPA-ZIWEI-016`, and `HPA-ZIWEI-022` against the Jielan 1581 source-scoped runtime plus actual API/Workbench candidate-profile surfaces.

Research record: `docs/research/ZIWEI-LEAP-MONTH-MISSING-PRODUCT-RECONCILIATION-R1.json`.  
Evidence: `docs/research/evidence/batch-12nq/ziwei-leap-month-missing-product-reconciliation.json`.
