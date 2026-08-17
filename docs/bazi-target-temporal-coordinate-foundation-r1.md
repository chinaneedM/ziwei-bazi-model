# Bazi Target Temporal Coordinate Foundation R1

Status: candidate implementation for Issue #292.

## Purpose

This layer resolves an explicit future/query/event local wall-time and spatial coordinate into auditable civil-time, UTC and local-apparent-solar (LAS) candidates.

It exists because the released `BaziFlowContext(target_utc)` is sufficient for absolute Annual/Monthly solar-term frames but is not sufficient for Bazi day/hour calculation, which also requires LAS and the active day-boundary/hour-stem profile.

## Contract

```text
TargetTemporalInput
  reported target local datetime
  target place label
  latitude / longitude
  IANA timezone id
  precision / uncertainty
        ↓
TargetTemporalCoordinateFoundation
        ↓
TargetTemporalCoordinateResolution
  civil realization candidates
  target UTC candidates
  target LMT / LAS candidates
  fold / gap / DST / tzdb / historical provenance
  independent integrity
  independent FactHash / ComputationHash
```

`TargetTemporalInput` is intentionally distinct from `BirthInput`. The core does not infer target coordinates from Natal birth coordinates.

## Location-policy boundary

R1 does not decide whether a future/event query should use birth place, current residence, event place, query place or another meridian. A future application/method profile must resolve that doctrine into an explicit `TargetTemporalInput` before calling this foundation.

The deterministic rule is only:

> Target LAS is calculated from the explicit target longitude and the resolved target UTC realization.

## Civil-time reuse

`CivilTimeResolver.resolve_local_time()` exposes the same existing ZoneInfo/IANA logic below the birth-specific adapter. Existing `CivilTimeResolver.resolve(BirthInput, ...)` delegates to it, preserving the released birth API and algorithm identity.

Target resolution preserves:

- timezone ID and tzdb version;
- UTC offset and DST offset;
- timezone abbreviation;
- fold identity;
- ambiguous and nonexistent wall-time classification;
- pre-1970 historical-confidence warning;
- uncertainty point-sample identity;
- no silent correction of gap times.

## Candidate preservation

Every legal civil realization remains a distinct target coordinate candidate. Candidate identity is not deduplicated by visible Bazi characters, UTC date, LAS date or any later day/hour projection.

Unresolved point samples remain in the resolution provenance. A target interval with no legal civil realization returns `FAILED` while retaining its unresolved provenance and a replayable bundle identity.

## Hash boundary

The layer publishes independent target-coordinate FactHash and ComputationHash. It does not absorb or mutate Natal, Jiaoyun/Dayun, or existing Flow hashes.

The FactHash binds the explicit target input and resolved civil/UTC/solar facts. The ComputationHash additionally binds the target profile, civil-time algorithm, SolarTime algorithm and shared sampling lineage.

## Daily/hourly seam

Issue #292 intentionally does not extend the released `BaziFlowContext` with DailyFrame or HourlyFrame fields.

The subsequent deterministic sidecar should consume:

```text
existing BaziFlowContext
+
TargetTemporalCoordinateCandidate
+
ResolvedBaziCalculationProfile
        ↓
Daily / Hourly Flow sidecar
```

It can then reuse `BaziTimeResolver.resolve()` with explicit target UTC + target LAS while leaving existing Annual/Monthly Flow identity byte-stable.

## Non-goals

No prediction, event interpretation, 旺衰, 格局, 用神, 喜忌, ShenSha, relation resolver, Ziwei+Bazi synthesis, canonical-source mutation, model-learning mutation, or automatic target-location doctrine is introduced here.
