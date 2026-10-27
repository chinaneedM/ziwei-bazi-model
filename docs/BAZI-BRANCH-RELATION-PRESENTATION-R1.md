# BaZi Branch Relation Presentation R1

Status: PRODUCTIZED READ-ONLY PRESENTATION SIDECAR  
Scope: natal deterministic relation identity only

## Purpose

The Ba Zi natal foundation already releases `BaziNatalState.raw_relations`. This milestone makes the released **earthly-branch relation facts** visible in the unified Workbench without reopening the frozen `BAZI-LOCAL-APPLICATION-VIEW-V1` application contract and without adding a second relation calculator in the browser.

The presentation sidecar emits only relations whose released `relation_family` starts with `BRANCH_`:

- `BRANCH_SIX_HARMONY` — 六合;
- `BRANCH_TRINE` — 三合;
- `BRANCH_CLASH` — 六冲;
- `BRANCH_CHUAN` — 相穿 / 六害;
- `BRANCH_PUNISHMENT` — 相刑.

## Canonical source closure

The registered relation identities are already implemented by `src/fortune_training/bazi_chart/relations.py`. Their canonical evidence is S14, `八字合冲刑害墓库与结构变化库`, especially the factual tables in sections 7.2 through 7.6. The derived-access mirror is `sources/derived-access/S14/segment-0008.txt`.

This productization does **not** load S14 into the runtime. The Workbench only projects already-released natal facts after replay/hash validation. Canonical sources remain governed by the repository source-access policy.

## Semantic boundary

The sidecar schema is `COMBINED-BAZI-BRANCH-RELATION-PRESENTATION-R1` and declares `semantics=RELATION_IDENTITY_ONLY`.

It intentionally publishes relation identity, orientation, arity, exact participant branch instances, rule-set identity/version and existing source refs. It intentionally does **not** publish `nominal_transformation_element` and does not decide:

- whether a harmony/trine transforms;
- whether any structure succeeds or fails;
- Five-Element strength or weakness;
- auspicious/inauspicious effects;
- any predictive interpretation or doctrinal winner.

Those exclusions are required to keep this feature inside deterministic chart presentation rather than prediction semantics.

## Candidate and lineage binding

For every Ba Zi application candidate, the sidecar replays the natal foundation from the same birth input/profile and requires exact equality of both `natal_fact_hash` and `natal_computation_hash`. Every relation participant must resolve to an actual `BranchInstance` in that exact natal candidate, and relation arity must match the number of emitted participants.

The browser binds the sidecar row to the explicitly selected Ba Zi application candidate. It writes only to a dedicated sibling presentation container and never mutates/recalculates the four-pillar chart data.
