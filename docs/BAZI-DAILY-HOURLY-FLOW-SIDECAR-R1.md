# Bazi Daily/Hourly Flow Sidecar R1

## Scope

This release materializes deterministic Daily and Hourly Bazi target-time coordinates as an identity-separated downstream sidecar.

```text
existing BaziFlowCandidate
  target UTC
  active PRE_DAYUN / DAYUN
  AnnualFrame
  MonthlyFrame
        +
TargetTemporalCoordinateCandidate
  explicit target civil realization
  target UTC
  explicit target LAS / longitude lineage
        +
ResolvedBaziCalculationProfile
        ↓
BaziDailyHourlyFlowCandidate
  DailyFrame
  HourlyFrame
  independent integrity
  independent FactHash / ComputationHash
```

The released `BaziFlowContext` is not extended or rewritten. Its FactHash and ComputationHash remain upstream identities.

## Authority and coordinate boundary

Daily/Hourly projection uses the released `BaziTimeResolver.resolve()` path. It does not implement a second sexagenary day/hour algorithm.

The target Local Apparent Solar Time is consumed only from the explicit `TargetTemporalCoordinateCandidate`. Birth longitude is not a fallback. Target longitude remains bound through the target-coordinate identity and the sidecar context.

Annual and Monthly frames remain authoritative upstream Flow facts. The shared resolver's year/month outputs are used only as consistency checks; this sidecar does not mint competing Annual/Monthly frames.

## DailyFrame

`DailyFrame` records:

- stable frame ID;
- Ganzhi and sexagenary index;
- resolver `effective_day_date`;
- half-open LAS interval;
- active day-boundary policy;
- source Flow FactHash;
- source TargetCoordinate FactHash and candidate ID;
- Natal calculation profile identity.

Supported day-boundary semantics are inherited from the released calculation profile, including `MIDNIGHT` and `ZI_START_23`.

## HourlyFrame

`HourlyFrame` records:

- stable frame ID;
- Ganzhi and sexagenary index;
- branch;
- half-open two-hour LAS interval;
- resolver `hour_stem_source_date`;
- late-Zi policy;
- source DailyFrame ID;
- source Flow and TargetCoordinate identities;
- Natal calculation profile identity.

The Zi interval is `[23:00, 01:00)` in LAS clock semantics.

## Candidate preservation

The engine joins Flow candidates and TargetCoordinate candidates only when normalized target UTC is identical. It preserves distinct compatible lineages, including civil folds, uncertainty samples, target spatial identities, and calculation-profile computation lineages even when visible Daily/Hourly Ganzhi match.

No deduplication by visible characters is performed.

## Integrity

Integrity replay fails closed on mismatches involving at least:

- Flow and TargetCoordinate integrity;
- Flow/Target upstream fact and computation hashes;
- upstream Natal/Temporal fact lineage;
- calculation-profile and policy lineage;
- target candidate ID/index and Flow candidate index lineage;
- target UTC, LAS, and explicit longitude lineage;
- shared Bazi resolver Daily/Hourly replay;
- authoritative Flow Annual/Monthly consistency;
- frame IDs, half-open intervals, and frame-source bindings;
- algorithm-version lineage.

## Hash isolation

DailyHourly FactHash commits to downstream temporal facts and upstream fact identities. DailyHourly ComputationHash additionally commits to upstream computation identities, source candidate indices, the complete resolved calculation profile, algorithm versions, and the sidecar hash algorithm.

The sidecar never mutates Natal, Temporal, Flow, or TargetCoordinate hashes.

## Non-goals

R1 does not implement target-location doctrine selection, geocoding, ShenSha, strength, pattern, useful-god, Classical relation operability/resolution, event interpretation, prediction, or Ziwei+Bazi synthesis.
