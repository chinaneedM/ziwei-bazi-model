# Bazi Temporal Classical Annotations R1

## Scope

This slice enriches the released Bazi target-time timeline with deterministic,
read-only chart facts. It does not alter Natal, Jiaoyun/Dayun, Flow,
TargetCoordinate, Daily/Hourly, or Xiaoyun identities.

The supported layers are:

- active Dayun when a materialized Dayun Ganzhi exists;
- both Xiaoyun method candidates;
- Annual;
- Monthly;
- Daily;
- Hourly.

For every resolved layer the projection records:

1. visible-stem Ten God relative to the Natal day master;
2. registry-ordered hidden stems and each hidden stem's Ten God;
3. Nayin name, element, semantic identity and registry identity;
4. Xunkong identity;
5. Twelve Growth of the Natal day master at the layer branch;
6. self Twelve Growth of the layer stem at its own branch.

## Identity and candidate boundaries

Every layer has an independent `context_id`, `source_layer`, FactHash and
ComputationHash. Equal visible annotations at different temporal layers are not
deduplicated. Both Xiaoyun methods remain present under
`XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER`; annotation equality cannot select or
merge a method.

Before the first Dayun transition, the Dayun slot reports
`PRE_DAYUN_NO_GANZHI_ANNOTATION`. No synthetic Ganzhi or annotation is emitted.

## Sources and released registries

The projection composes existing released registries rather than introducing a
second doctrine:

- hidden stems and Ten Gods: S11-bound Bazi Chart Foundation registries,
  traced to `S11:YHZP-CH-061` and the released
  `S11:YHZP-CH-016|017|057|065` relation set;
- Nayin: `BAZI-NAYIN-REGISTRY-R1`, bound to `S01:ZZZA-PR-010` and
  `S01:ZZZA-PR-011`;
- Xunkong: `BAZI-XUNKONG-YHZP-R1`, bound to `S14:YHZP-CH-047` and `S14:7.7`;
- Twelve Growth: `BAZI-TWELVE-GROWTH-YIN-YANG-R1`, bound to the released S12
  source set.

## Hash and replay contract

Each layer separates physical annotation facts from computation lineage. The
aggregate FactHash binds layer status and child FactHashes; its ComputationHash
binds child ComputationHashes, stable sources and the versioned hash algorithm.

Application structural integrity rebuilds every layer from its timeline Ganzhi
and recorded day master. The existing full replay then rebuilds the application
from the Natal candidate, which independently binds the true day master. A
payload that changes an annotation and recomputes all local hashes therefore
still fails replay.

The machine contract is part of
`schemas/bazi-application-flow-integration-r1.schema.json`. The browser renders
all fields as read-only target-flow details.

## Explicit exclusions

This release does not calculate or infer:

- strength or body-strength verdicts;
- Pattern, Useful God, favorable/unfavorable elements;
- combination-transformation success or relation priority;
- dynamic ShenSha activation across temporal layers;
- auspiciousness, event interpretation, prediction or training data.

Dynamic ShenSha requires a separately sourced rule about which Natal and flow
anchors interact at each layer. It is not inferred merely because Natal
ShenSha registries exist.
