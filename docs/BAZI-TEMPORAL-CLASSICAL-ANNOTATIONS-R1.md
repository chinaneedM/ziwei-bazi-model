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
- Nayin: `BAZI-NAYIN-REGISTRY-R1@1.0.1`, bound to `S11:YHZP-CH-014`;
- Xunkong: `BAZI-XUNKONG-YHZP-R1`, bound to `S14:YHZP-CH-047` and `S14:7.7`;
- Twelve Growth: `BAZI-TWELVE-GROWTH-YIN-YANG-R1@1.0.1`, with primary source
  `S11:YHZP-CH-015` and later ZPZQ witnesses `S12:ZPZQ-CH-05` /
  `S12:ZPZQ-R-0006`.

### Historical provenance follow-up

Historical Audit Batch 07 CI closure found that the composed temporal layer still carried the pre-repair Nayin and Twelve-Growth source refs even after their component registries had been corrected. `BAZI-TEMPORAL-CLASSICAL-ANNOTATION-PROJECTION-R1` was therefore bumped from `1.0.0` to `1.0.1` as a provenance-only repair. Placement/identity formulas were not reopened.

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


### Batch 11A hidden-stem order/hash semantics

Historical provenance audit separated hidden-stem **membership** from registry/display
**order**. The received YHZP hidden-stem verse preserves a textual sequence that
differs from the repository display tuple for several branches. Later Ziping
material also introduces main-qi / residual-qi distinctions, but no exact
twelve-branch hierarchy is inferred from the repository ordinal.

A provenance/hash defect was therefore repaired forward-only:

- `BAZI-TEMPORAL-CLASSICAL-ANNOTATION-PROJECTION-R1` is now `1.0.2`;
- `BAZI-TEMPORAL-CLASSICAL-ANNOTATION-HASH-R1` is now `1.0.1`;
- `registry_ordinal` and hidden-stem list ordering no longer alter annotation
  FactHash when membership and semantic bindings are unchanged;
- ComputationHash explicitly binds `hidden_stem_registry_order`;
- output order, hidden-stem membership, Ten Gods and all temporal coordinates are unchanged.

This matches the natal foundation contract: membership is a fact, display order
is lineage. No ordinal is a root-strength grade.

### Batch 12ML natal-day-master / Ten-God projection audit

HPA-BAZI-FLOW-002 now closes within the historical scope of audited HPA-BAZI-003, with direct NTL-9900014379 five-yang/five-yin table corroboration. The target composer calls the same natal `ten_god` function for visible and hidden stems; all seven annotation slots use the natal day master, not the target daily stem. 100 stem pairs and 4200 legal layer annotations replay against a visually collated oracle. Equal Xiaoyun candidates remain separate; pre-Dayun emits no synthetic annotation.

Local annotation/hash validation proves internal consistency only. Rebuilding every annotation under a substituted day master and recomputing local hashes can pass local structural validation; the complete request-bound upstream replay rejects the substitution. Keep both validation layers. This is the released contract, not a newly discovered chart defect. No strength, pattern, useful-god or interpretation authority follows from the identity mapping.

The physical witness is a catalog-assigned 1926 received edition; it does not prove earliest rule origin or a classical seven-layer software interface. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-TEMPORAL-TEN-GOD-PROJECTION-AUDIT-ML.md` and `docs/research/BAZI-TEMPORAL-TEN-GOD-PROJECTION-AUDIT-R1.json`. Runtime, schemas, hashes and profile versions remain unchanged.


### Batch 12MN NaYin / XunKong / Twelve-Growth projection decomposition

HPA-BAZI-FLOW-004 is now a decomposed composition summary rather than a single unresolved historical claim. The runtime continues to use `BAZI-TEMPORAL-CLASSICAL-ANNOTATION-PROJECTION-R1@1.0.2`; the audit separates three child projections:

- `HPA-BAZI-FLOW-008`: target-Ganzhi NaYin identity, inherited unchanged from audited `HPA-BAZI-006`;
- `HPA-BAZI-FLOW-009`: target-Ganzhi six-Xun XunKong identity, inherited unchanged from audited `HPA-BAZI-007`;
- `HPA-BAZI-FLOW-010`: Twelve-Growth identity under the released source-scoped profile, preserving two distinct anchors: natal day master → target branch and target stem → its target branch, inherited from audited `HPA-BAZI-008`.

The audit replays 600 natal-day-master × legal-Ganzhi coordinates and 4,200 resolved Dayun / two Xiaoyun candidates / annual / monthly / daily / hourly slots against the already-audited parent APIs. Illegal Ganzhi remain rejected before component projection. Equal Xiaoyun facts do not select a candidate; before formal Dayun, no synthetic Dayun Ganzhi is created.

This closes identity inheritance only. It does **not** establish that historical texts taught a seven-layer software composition, does not convert Twelve-Growth phase names into strength judgments, and does not add XunKong auspiciousness, NaYin omen, pattern, useful-god, event or prediction semantics. Any alternate Twelve-Growth profile remains separately source-scoped and unranked.

The Matrix description for HPA-BAZI-FLOW-004 had lagged the Batch 11A runtime profile bump and still named `@1.0.1`. It is synchronized to the live `@1.0.2` descriptor here as downstream bookkeeping of the already-counted `PROV-DEFECT-009`; no new defect is counted and no runtime/schema/hash calculation changes. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-TEMPORAL-CLASSICAL-IDENTITY-PROJECTION-AUDIT-MN.md` and `docs/research/BAZI-TEMPORAL-CLASSICAL-IDENTITY-PROJECTION-AUDIT-R1.json`.
