# Bazi Temporal Flow Context R1

Status: release candidate for Issue #217.

## Scope

This runtime projects one target UTC instant across a validated Natal candidate and every supplied Dayun `BaziTemporalCandidate`. It materializes only deterministic temporal coordinates:

```text
Natal FactHash
  -> Dayun Temporal FactHash
      -> target UTC instant
          -> active Pre-Dayun or Dayun frame
          -> active AnnualFrame
          -> active MonthlyFrame
```

Annual and Monthly frames are not Natal pillars and are never inserted into `BaziNatalState`. The query does not mutate the released Natal or Dayun hashes.

## Shared Time/Calendar path

`BaziTimeResolver.resolve_year_month()` is the single year/month coordinate path used by both Natal pillar resolution and this flow runtime. It owns:

- Start-of-Spring annual boundary selection;
- active and next `JIE` selection from `SolarTermEngine.adjacent_terms()`;
- `_JIE_TO_MONTH_BRANCH` mapping;
- Five-Tiger month-stem calculation.

There is no second annual/month sexagenary implementation. Both the continuous Dayun profile and the isolated Wenzhen China compatibility profile consume these shared coordinates. Wenzhen compatibility remains limited to Jiaoyun/Dayun realization.

## Frame semantics

Annual:

```text
[Start-of-Spring(pillar year), Start-of-Spring(next year))
```

Monthly:

```text
[active Jie, next Jie)
```

All comparisons are made on timezone-aware instants normalized to UTC. At an exact Start-of-Spring, Jie, or Dayun transition instant, the later frame is active. Frame identities hash UTC boundaries and are independent of display timezone.

## Dayun intersection and failure behavior

The active frame is exactly one of:

- `PRE_DAYUN` for `birth <= target < first Jiaoyun`;
- the one Dayun frame satisfying `start <= target < end`.

The query fails closed with an explicit diagnostic when the target is before birth, is timezone-naive, falls in an invalid schedule gap, or is at/after the end of the materialized Dayun schedule.

## Candidate preservation

The same target is replayed over every supplied TemporalCandidate. Matching Annual/Monthly coordinates do not collapse contexts because the upstream Temporal FactHash is part of the flow fact payload. Deduplication occurs only when the complete flow FactHash and ComputationHash are identical; all contributing candidate indices and TemporalSeed IDs remain as lineage.

## Independent integrity and hashes

`BAZI-FLOW-INTEGRITY-V1` replays:

- upstream Natal and Temporal FactHash references;
- calculation and temporal profile lineage;
- Time/Calendar policy-registry and year-boundary lineage;
- target containment and half-open Dayun selection;
- Annual Ganzhi and Start-of-Spring boundaries;
- Monthly Ganzhi and Jie boundaries.

`BAZI-FLOW-HASH-V1` defines a separate downstream boundary:

- `FlowFactHash` covers target, upstream fact references, active Dayun fact, AnnualFrame, MonthlyFrame, and year-boundary policy;
- `FlowComputationHash` additionally covers upstream computation hashes, the resolved Bazi calculation profile, profile/policy lineage, algorithms, and provenance.

The public contract is `schemas/bazi-flow-context-v1.schema.json`.

## Compatibility fixture

`tests/fixtures/bazi-flow-wenzhen-annual-month-r1.json` preserves the observed Wenzhen 2026 `丙午` annual and Jie-to-month sequence as a third-party compatibility witness. It is explicitly not canonical calendar authority and does not create a Wenzhen-specific annual/month algorithm.

## Non-goals

R1 does not implement dynamic stem/branch relation composition, relation suppression or activation, strength, seasonal scoring, pattern, useful-god selection, 调候, ShenSha, daily/hourly flow axes, prediction, UI, or Ziwei integration.
