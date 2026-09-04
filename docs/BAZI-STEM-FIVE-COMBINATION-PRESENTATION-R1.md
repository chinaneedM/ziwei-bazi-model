# BaZi Stem Five-Combination Presentation R1

Status: PRODUCTIZED READ-ONLY PRESENTATION SIDECAR  
Scope: natal deterministic stem-combination identity only

## Purpose

The Ba Zi natal foundation already releases `BaziNatalState.raw_relations`, including the five stem-combination identities emitted as `STEM_COMBINATION`. This milestone makes those already-released **heavenly-stem five-combination facts** visible in the unified Workbench without reopening the frozen `BAZI-LOCAL-APPLICATION-VIEW-V1` contract and without adding a second relation calculator in the browser.

The presentation sidecar does not generate stem combinations. It filters the exact released `STEM_COMBINATION` rows from the replayed natal candidate and presents their exact stem instances.

## Canonical source closure

The released registry in `src/fortune_training/bazi_chart/relations.py` contains the five source-backed identities:

- 甲 + 己;
- 乙 + 庚;
- 丙 + 辛;
- 丁 + 壬;
- 戊 + 癸.

Their canonical evidence is S14, `八字合冲刑害墓库与结构变化库`, section 7.1 (`天干五合事实表`). The sidecar does not read or reinterpret the source corpus at runtime; it projects only the already-released relation facts after natal replay and hash validation.

## Semantic boundary

The sidecar schema is `COMBINED-BAZI-STEM-RELATION-PRESENTATION-R1` and declares `semantics=RELATION_IDENTITY_ONLY`.

The underlying raw relation also carries a `nominal_transformation_element`. R1 intentionally does **not** expose that field. A nominal transformation target is not proof that an actual transformation succeeds in the concrete chart. The presentation therefore emits only:

- relation identity and semantic relation identity;
- orientation and arity;
- exact participating year/month/day/hour stem instances;
- released rule-set identity/version;
- existing source refs.

It does not decide or imply:

- whether the pair actually transforms;
- the operative transformed element or `化神`;
- success/failure conditions;
- Five-Element strength or weakness;
- auspicious/inauspicious effects;
- any prediction, doctrinal winner, precedence or competition result.

## Candidate and lineage binding

For every Ba Zi application candidate, the sidecar replays the natal foundation from the same birth input/profile and requires exact equality of both `natal_fact_hash` and `natal_computation_hash`. Every relation participant must resolve to an actual `StemInstance` in that exact natal candidate, and relation arity must match the emitted participant count.

Multiple application candidates may legally reuse one natal candidate when their later temporal/application lineage differs. The sidecar therefore preserves every application candidate while requiring reused natal lineages to project identical stem-relation facts.

The browser binds the sidecar row to the explicitly selected Ba Zi application candidate. It writes only to a dedicated sibling presentation container and never mutates or recalculates the four-pillar chart.
