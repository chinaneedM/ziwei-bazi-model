# Bazi Structural Support Foundation R1

Status: release candidate for Issue #221.

## Scope

Structural Support Foundation R1 is an immutable downstream projection:

```text
Natal Foundation
  -> Dayun Temporal
    -> Flow Context
      -> Structural Context R1
        -> Structural Support Foundation R1
```

It binds two non-interchangeable seasonal reference roles and projects neutral
root/support evidence candidates from released hidden-stem and affinity facts. It
does not mutate or reinterpret Natal, Temporal, Flow, or Structural R1 state.

## Typed seasonal references

`NATAL_MONTH_COMMAND` binds the released Natal `MONTH.BRANCH` occurrence. Its
identity contains the upstream Natal FactHash, `MONTH.BRANCH`, Natal month
Ganzhi/branch, Natal profile, source TemporalSeed identities, and available
Time/Calendar policy registry lineage. It is derived only from the Natal
candidate, so changing target time cannot change the reference.

`ACTIVE_FLOW_SOLAR_MONTH` binds the Structural R1 `MONTHLY` branch occurrence to
the exact upstream `MonthlyFrame`. It carries the frame and occurrence IDs,
active Ganzhi/branch, start/end Jie identities and UTC instants, and the released
half-open interval semantics. At an exact Jie instant it therefore binds the new
Flow month. It is never named or treated as the Natal month command.

## Shared primitives and evidence classes

The generator projects the existing Foundation and Structural R1 facts:

- Natal and active temporal `StemInstance` / `BranchInstance` occurrences;
- Natal and temporal hidden-stem memberships;
- Natal `StemBranchAffinityFact` plus Structural R1 dynamic affinities;
- Natal exposure links plus Structural R1 dynamic exposure links.

It creates no hidden-stem, Five-Element, polarity, affinity, exposure, or root
registry. `HIDDEN_STEMS` registry ordinal remains membership order and is absent
from support evidence facts.

Every active visible stem occurrence is evaluated against every active branch
occurrence already covered by those affinity facts. Two non-equivalent candidate
classes are preserved:

- `EXACT_HIDDEN_STEM_MATCH`: the branch contains the exact visible stem and the
  candidate binds the matching upstream exposure links;
- `SAME_ELEMENT_HIDDEN_SUPPORT`: the branch contains same-element hidden stems
  whose stem identity differs from the visible stem.

Because the shared affinity primitive reports exact matches inside its broader
same-element set, the support projection explicitly subtracts exact membership
from `SAME_ELEMENT_HIDDEN_SUPPORT`. It never collapses the two classes to a
boolean root verdict.

Each candidate retains visible and supporting occurrence IDs, matching hidden
occurrence IDs, participant layers, seasonal role membership, upstream affinity
and exposure identities, and rule/source lineage. Repeated characters in Natal,
Dayun, Annual, and Monthly layers therefore remain separate evidence.

## Scoped evidence sets

`natal_month_command_support_candidate_ids` is a deterministic projection of
candidates whose supporting branch is the fixed Natal month-command occurrence.
It is only a support evidence set; it does not assert 得令, 旺, 强, 格局, or any
other interpretive conclusion.

`active_flow_solar_month_support_candidate_ids` independently projects candidates
whose supporting branch is the active Flow monthly occurrence. The two sets are
never merged or substituted for one another.

## Candidate preservation

Every Structural R1 candidate is replayed against its exact upstream Flow
candidate. The Support FactHash binds both upstream Structural and Flow FactHash
identities. Candidates are deduplicated only when the complete Support FactHash
and ComputationHash are identical; all Structural, Flow, Temporal, and
TemporalSeed candidate lineage is retained.

When Flow selects `PRE_DAYUN`, no Dayun stem or branch exists in Structural R1,
so no Dayun support candidate can be fabricated. Natal, Annual, and Monthly
support facts continue to replay normally.

## Independent integrity and hashes

`BAZI-STRUCTURAL-SUPPORT-INTEGRITY-V1` verifies:

- exact upstream Natal, Temporal, Flow, and Structural fact bindings;
- the fixed Natal `MONTH.BRANCH` month-command reference and its Natal-only
  construction;
- the active Flow `MonthlyFrame` to Structural `MONTHLY` occurrence binding and
  half-open target interval;
- exact and same-element evidence replay from existing affinity, hidden-stem,
  and exposure IDs;
- exact/same-element semantic discrimination;
- participant, affinity, exposure, seasonal-role, and PRE_DAYUN integrity;
- the absence of weights, strength grades, or hidden-stem ordinals from support
  candidates;
- deterministic Support FactHash and ComputationHash replay.

`BAZI-STRUCTURAL-SUPPORT-HASH-V1` isolates the downstream layer:

- Support FactHash covers upstream fact identities, both seasonal reference
  facts, all occurrence-specific evidence candidates, and both scoped evidence
  sets;
- Support ComputationHash additionally binds the upstream Natal, Flow, and
  Structural computation hashes, resolved support profile, algorithm versions,
  rule/source lineage, and hash algorithm version.

The public machine-readable contract is
`schemas/bazi-structural-support-foundation-r1.schema.json`. Required
discrimination inputs are in
`tests/fixtures/bazi-structural-support-foundation-r1.json`.

## Non-goals

R1 does not implement `ROOT/NO_ROOT`, strong/weak or main/secondary root grades,
hidden-stem percentages or weights, 得令/得地/得势 verdicts, seasonal scores,
Day-Master strength, 格局, 用神/忌神, 调候, 病药, combination-transformation
success, relation suppression/cancellation/rescue/release/reactivation, automatic
temporal priority, Harm, Break, partial trines, directional triads, hidden
combinations, ShenSha, prediction, Ziwei fusion, or mutable/verdict UI behavior.
The separate read-only application composition is documented in
`docs/BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1.md`; it does not change
this generator or its coverage.
