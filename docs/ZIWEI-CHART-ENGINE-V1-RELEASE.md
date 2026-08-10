# Ziwei Chart Engine V1 Release Contract

## Release status

```text
RELEASE_ID=ZIWEI-CHART-ENGINE-V1
RELEASE_VERSION=1.0.0
STATUS=RELEASE_CANDIDATE
FOUNDATION_BASE=PHASE-01-R1
ISSUE=#190
PR=#191
```

This document freezes the deterministic Ziwei chart-generation contract only after
all release gates pass. It does not define interpretation, prediction, training,
model-learning or graphical UI behavior.

## Frozen calculation profile

The single operational release profile is constructed by:

```python
ziwei_chart_engine_v1_profile(policy_registry)
```

Its immutable identity is:

```text
profile_id      = ZIWEI-CHART-ENGINE-V1
profile_version = 1.0.0
```

The release profile binds the current operational families already validated in
prior Foundation stages:

```text
Time/Calendar registry      PHASE-01-R1
Ziwei day boundary          ZI_START_23
Bazi day boundary           ZI_START_23
Bazi late-Zi stem policy    ZI_START_ROLLOVER
Ziwei leap-month placement  ZHONGZHOU_FIXED_15

Natal structure             ZIWEI-NATAL-STRUCTURE-V1
Main stars                  ZIWEI-FOURTEEN-MAIN-STARS-V1
Core auxiliary              WENMO_DEFAULT_CORE_AUX_R1
Minor stars                 WENMO_DEFAULT_MINOR_R1 v2.0.0
Dignity                     OPERATIONAL-ZIWEI-DIGNITY-R4 v4.0.0
Transformations             S08_CURRENT_40_ASSIGNMENT_R1
Temporal                    S10_CURRENT_TEMPORAL_R1
Rings                       WENMO_DEFAULT_RING_R1
Roles                       WENMO_DEFAULT_ROLE_R1
```

The use of `WENMO_DEFAULT_*` identifiers means an operational compatibility
selection, not canonical source authority. Historical/QS alternative RuleSets
remain separately addressable and are not overwritten by this release.

## Physical inventory and static state

V1 freezes the current deterministic physical inventory at:

```text
70 physical entities
70 Dignity annotations per complete V1 natal chart
717 generator-reachable Dignity cells
625 GRADED
92 UNRATED
```

The 70-entity inventory includes the R4 closure for:

```text
STAR.TIANSHOU
STAR.TIANSHANG
STAR.TIANSHI
```

No future star becomes part of V1 merely because it exists in source material.
Promotion of any additional physical entity requires a new release/profile version
and its own placement + reachable-state closure.

## Public runtime boundary

The stable JSON API remains:

```python
ZiweiChartFoundation.resolve(request)
```

The V1 typed handoff is:

```python
ZiweiChartFoundation.resolve_typed(request)
```

It returns `ZiweiTypedResolution` containing deduplicated `ZiweiChartCandidate`
objects. Each candidate preserves:

```text
effective absolute Ziwei birth year
sex
Time/Calendar branch indices
validated NatalChartState
IntegrityReport
FactHash / ComputationHash
```

A candidate can construct the downstream temporal context with:

```python
candidate.temporal_context()
```

This closes the prior integration gap where the public JSON resolver serialized
NatalChartState before the typed Temporal/View layers could consume it.

## End-to-end public V1 path

The release path is:

```text
BirthInput
-> TimeCalendarFoundation
-> ZiweiChartFoundation.resolve_typed
-> ZiweiChartCandidate
-> Natal Integrity
-> Natal FactHash / ComputationHash
-> ZiweiTemporalEngine
-> Temporal Integrity
-> Temporal FactHash / ComputationHash
-> ZiweiViewProjectionCompiler
-> ChartViewModel / ViewHash
-> renderer
```

No step in this path requires a caller to invoke a private method or reconstruct a
typed chart from JSON.

## Candidate and uncertainty semantics

Time uncertainty remains first-class:

```text
RESOLVED
RESOLVED_SINGLE_CHART_WITH_TIME_UNCERTAINTY
MULTI_CANDIDATE
FAILED
```

Candidates are deduplicated by canonical natal FactHash. Branch lineage is retained
in `branch_indices`. Identical facts with different computation lineage fail closed.
The typed release layer additionally fails closed if an identical natal fact is
somehow associated with a different effective absolute Ziwei birth year, because
Temporal frames depend on that year.

## Integrity and hash contract

V1 preserves the existing three-layer identity model:

```text
FactHash
  deterministic generated facts

ComputationHash
  FactHash + frozen profile + algorithm/generator versions + provenance lineage

ViewHash
  source hashes + presentation profile + selected temporal projection + view compiler version
```

Presentation changes do not rewrite canonical natal or temporal facts.
Provenance-only changes do not rewrite FactHash.

## Published JSON Schemas

V1 publishes and regression-validates:

```text
schemas/ziwei-chart-foundation-v1.schema.json
schemas/ziwei-temporal-state-v1.schema.json
schemas/ziwei-chart-view-v1.schema.json
```

The chart schema includes the public `integrity_reports` and `hashes` fields emitted
by the engine. Real V1 output, not a hand-written example, is validated against all
three schemas in CI.

## Compatibility guarantees

V1 release does not remove prior replay targets. In particular:

```text
WENMO_DEFAULT_MINOR_R1 v1.0.0
OPERATIONAL-ZIWEI-DIGNITY-R3 v3.0.0
```

remain valid historical profile components. R4/V1 requires minor v2.0.0 and does
not silently mutate R3 computation snapshots.

## Explicit post-V1 boundary

The following are not V1 release blockers unless a later audit proves they alter
one of the frozen deterministic contracts above:

```text
graphical square/circular UI
renderer-specific pixels/layout
interpretation and prediction runtime
Structural Runtime V2
Query/Evidence/Warrant/Reality/Possible-Worlds runtime
additional historical/profile variants
non-promoted physical stars
斗君/month temporal families beyond the current Daxian/Annual/Minor-Limit V1 scope
Bazi chart engine
```

New work reopens V1 only if it changes deterministic chart facts, profile identity,
Generator behavior, Canonical Fact boundaries, Integrity/Hash semantics or the
published V1 API/schema contract.

## Release gates

The candidate becomes `FROZEN_V1` only when all of the following pass on the final
PR head:

```text
python -m pip install -e .
./scripts/bootstrap-work-env.sh --check
fortune-train verify
python -m unittest discover -s tests -v
```

and regression proves:

```text
frozen V1 profile validates
public typed natal resolution works
70-entity / 70-annotation complete chart materializes
full public Natal -> Temporal -> View -> Renderer path works
chart JSON validates against its schema
temporal JSON validates against its schema
view JSON validates against its schema
legacy R3 replay remains valid
changed-file scope does not touch canonical/training/model-learning
```
