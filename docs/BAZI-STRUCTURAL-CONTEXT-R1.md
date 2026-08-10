# Bazi Structural Context R1

Status: release candidate for Issue #219.

## Scope

Structural Context R1 is an immutable downstream projection:

```text
Natal Foundation
  -> Dayun Temporal
    -> Flow Context (active Dayun + Annual + Monthly)
      -> Structural Context R1
```

It materializes active temporal stem/branch occurrences, temporal hidden-stem memberships, Ten-God bindings against the unchanged Natal Day Master, dynamic exposure/affinity facts, and raw relation occurrences. It does not mutate or replace any Natal, Temporal, or Flow state or hash.

## Shared primitives

The runtime directly reuses the released neutral Foundation primitives:

- `StemInstance` and `BranchInstance`;
- `generate_hidden_stems()`;
- `ten_god()` and `TenGodBinding`;
- `generate_exposures()`;
- `generate_affinities()`;
- `generate_raw_relations()`.

No second stem/branch, hidden-stem, Ten-God, affinity, or raw relation registry exists in the Structural layer. The generator runs over Natal occurrences followed by active temporal occurrences, then retains only overlay facts containing at least one temporal participant. Natal-only relations remain upstream references, so their released IDs are unchanged.

## Temporal participant identity and provenance

Every active `DayunFrame`, `AnnualFrame`, and `MonthlyFrame` already owns a stable namespaced `frame_id`. Structural participants use `<frame_id>.STEM` and `<frame_id>.BRANCH`, preserving distinct occurrence identity even when multiple layers contain the same character.

Each participant has a separate provenance binding containing:

- `layer`;
- `source_frame_id`;
- `source_flow_fact_hash`;
- `source_ganzhi`.

If Flow selects `PRE_DAYUN`, no Dayun stem or branch is created. Annual and Monthly participants remain active. PRE_DAYUN is a temporal interval state, not a Ganzhi pillar.

## Hidden stems and Ten Gods

Active temporal branches replay the shared hidden-stem membership registry. Registry ordinal remains membership order only; Structural R1 assigns no root weight or strength grade.

Every active temporal visible stem and temporal hidden stem receives one Ten-God binding relative to `natal_day_master_stem`. Dayun, Annual, and Monthly stems never become alternate Day Masters.

## Dynamic overlays

The combined active set derives only neutral occurrence facts:

- exact hidden-stem exposure links involving a temporal participant;
- visible-stem/branch affinity facts involving a temporal participant;
- released raw relation patterns involving a temporal participant.

Dynamic relations expose canonical participant layers and one neutral scope:

- `CROSS_LAYER` when Natal and temporal occurrences participate;
- `TEMPORAL_ONLY` when every participant is Dayun/Annual/Monthly.

Directed punishment orientation and participant order are preserved exactly. Symmetric/group relations retain the shared generator's existing participant semantics. A nominal transformation element on a stem combination or trine is only registry metadata, not a successful transformation claim.

## Candidate preservation

Every supplied `BaziFlowCandidate` is replayed independently. The Structural FactHash includes the upstream Flow FactHash, so candidates are not collapsed merely because their Annual and Monthly frames match. Deduplication is permitted only when the complete Structural FactHash and ComputationHash match; contributing Flow indices, Temporal indices, and TemporalSeed IDs remain lineage.

## Independent integrity and hashes

`BAZI-STRUCTURAL-INTEGRITY-V1` replays:

- upstream Natal, Temporal, and Flow bindings;
- active frame-to-participant Ganzhi and provenance;
- the PRE_DAYUN no-pillar rule;
- stem element/polarity and branch affiliation registries;
- hidden stems and Ten Gods against Natal Day Master;
- dynamic exposure, affinity, and raw relations through shared generators;
- Natal-only overlay exclusion;
- relation identity, participant existence, arity, orientation, layer scope, and upstream Natal references;
- the independent Structural hash bundle.

`BAZI-STRUCTURAL-HASH-V1` isolates this downstream layer:

- Structural FactHash binds upstream fact identities and the complete neutral active structural payload;
- Structural ComputationHash additionally binds upstream computation hashes, the resolved Structural profile, algorithm versions, rule-set lineage, sources, and hash algorithm version.

The public contract is `schemas/bazi-structural-context-r1.schema.json`. Required discrimination data is in `tests/fixtures/bazi-structural-context-r1.json`.

## Non-goals

R1 does not implement 害, 破, 半合, 三会, hidden combinations, combination-transformation success, cancellation, suppression, rescue, release, reactivation, interpretive priority, strength/root weights, seasonal scoring, 旺衰, 格局, 用神, 忌神, 调候, 病药, ShenSha, prediction, Ziwei fusion, or UI.
