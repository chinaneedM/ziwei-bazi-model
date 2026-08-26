# Combined Target-Flow Fusion R2

## Purpose

`Combined Target-Flow Fusion R2` closes a composition gap in the deterministic
Ziwei+Bazi application layer. R1 already binds the common birth input, independent
Ziwei/Bazi calculation policies, the Bazi target-flow bundle, and the target
coordinate identity. R1 intentionally keeps the Ziwei side at the selected base
application identity.

R2 adds the already-released `SharedZiweiSelectorProjectionService` to that same
target-coordinate lineage. It does not introduce a new placement rule.

The resulting chain is:

```text
TargetTemporalInput
        |
        v
TargetTemporalCoordinateResolution
        |------------------------------|
        v                              v
BaziApplicationFlowResolution   SharedZiweiSelectorProjectionResolution
        |                              |
        |------------------------------|
                       v
        CombinedTargetFlowFusionR2Resolution
```

## Invariants

1. **One physical target coordinate, two independent calendars.**
   The target civil/UTC/local-apparent-solar coordinate hashes must match on the
   R1 composition, Bazi target flow, and Ziwei selector projection. Ziwei and
   Bazi then apply their own calendar, day-boundary, and late-Zi policies.

2. **No silent school choice.**
   Existing Ziwei hourly methods, Kui/Yue candidates, Tianma case candidates,
   and any other released method candidates remain independent. R2 records the
   resulting selector fact/computation hashes; it does not choose among them.

3. **R1 remains immutable.**
   R2 is additive. `CombinedTargetFlowResolution` R1 schemas, hashes, and replay
   semantics are not changed.

4. **Uncertainty remains uncertainty.**
   `RESOLVED` is emitted only when the target coordinate is singular, Bazi flow
   is singular, and Ziwei selector projection contains exactly one physical
   target candidate. DST folds, approximate-time sampling, boundary uncertainty,
   or multiple legal candidates produce `UNCERTAINTY_PRESENT`.

5. **No interpretation layer.**
   R2 contains no prediction, strength, 格局, 用神, 喜忌, auspiciousness, or
   event judgment.

## Hash lineage

R2 has three independent hashes:

- `source_fact_hash`: binds the base combined manifest, the frozen R1 target-flow
  bundle, physical target coordinate, Bazi target-flow facts, and Ziwei selector
  facts.
- `view_hash`: binds renderer-neutral target input/status and both target-flow
  view identities.
- `bundle_hash`: binds R2 schema/status, source/view hashes, target coordinate
  computation identity, Bazi bundle identity, Ziwei selector computation
  identity, and R2 algorithm version.

The structural validator verifies local consistency. Full replay recomputes the
entire R2 result from the request and therefore rejects a locally rehashed
mutation of an upstream binding.

## Ziwei target content now present in the fusion lineage

The Ziwei selector projection already provides, when legal for the target:

- Daxian layer projection;
- Annual layer projection;
- Minor-Limit age and natal-ring encounters;
- regular lunar Month projection;
- Day palace/designation, dynamic auxiliary stars, candidate sets and
  transformations;
- both Hour method candidates with independent palace/designation, auxiliary,
  candidate and transformation identity;
- independent Ziwei calendar-date and day-boundary policy lineage.

R2 references these facts through the selector fact/computation hashes and
returns the full selector object through `resolve_with_bundles()` without
duplicating it into a second physical inventory.

## Public API

```python
from fortune_training.combined_chart_application import (
    CombinedTargetFlowFusionR2Service,
)

service = CombinedTargetFlowFusionR2Service.from_repository(repository_root)
resolution = service.resolve(request)
base, bazi_flow, r1, target, ziwei_selector, r2 = (
    service.resolve_with_bundles(request)
)
```

Renderer-neutral serialization is available through
`combined_target_flow_fusion_r2_export()`.

## Deferred work

This layer deliberately does **not** perform:

- historical-source criticism;
- correctness ranking between schools;
- default-school selection;
- prediction or interpretation;
- UI redesign.

Those remain later phases after deterministic bottom-level chart content and
fusion composition are complete.
