# BaZi Hidden-Stem Exact Exposure Presentation R1

Status: PRODUCTIZED READ-ONLY PRESENTATION SIDECAR  
Scope: natal exact same-stem identity links only

## Purpose

The released Ba Zi natal foundation already carries `BaziNatalState.exposures`. Each exposure is a mechanical link from one concrete hidden-stem instance to one concrete visible heavenly-stem instance when the two stem identities are exactly equal. This milestone makes that released fact layer visible in the unified Workbench without reopening the frozen `BAZI-LOCAL-APPLICATION-VIEW-V1` contract and without adding a browser-side hidden-stem calculator.

The presentation schema is `COMBINED-BAZI-HIDDEN-EXPOSURE-PRESENTATION-R1` and declares `semantics=EXACT_STEM_IDENTITY_MATCH_ONLY`.

## Canonical source closure

S11 is the registered source authority for the released hidden-stem membership and exposure layer. The narrow source table used here is S11, `八字干支五行藏干与十神库`, section 7.3 (`地支藏干表`), whose current canonical-runtime route is `sources/canonical-runtime/S11/segment-0009.txt` and whose table rows are anchored to `YHZP-CH-061`.

The engine does not ask the source to decide a strength concept. `generate_exposures()` takes the already-released hidden-stem memberships and visible four-pillar stems and emits a link only when `hidden.stem == visible.stem`. `validate_natal_state()` replays that exact generator and fails on any exposure divergence; the exposure projection also participates in the natal FactHash.

## Semantic boundary

R1 exposes only:

- exposure link identity;
- `match_kind=EXACT_STEM`;
- the exact hidden-stem instance and its source branch position;
- the exact visible-stem instance and pillar position;
- the shared stem identity;
- existing source refs.

R1 deliberately does not claim or calculate:

- 通根、得根、得地 or any root-strength grade;
- 月令 strength or seasonal weighting;
- Five-Element strength / weakness;
- 格局 success or failure;
- 喜忌、用神、吉凶;
- any predictive interpretation.

The separate released `affinities` layer is not exposed in this milestone. In particular, its `same_element_hidden_stem_instance_ids` must not be silently converted into a rooting or strength judgment.

## Candidate and lineage binding

For each Ba Zi application candidate, the sidecar replays the natal foundation from the exact same birth input and natal profile. It requires equality of both `natal_fact_hash` and `natal_computation_hash` before reading exposure links. Every hidden and visible instance referenced by an exposure must exist in that exact natal candidate, and the three stem identities (`link.stem`, hidden stem, visible stem) must agree exactly.

Multiple application candidates may legally reuse a natal candidate when later temporal/application lineage differs. The sidecar preserves every application candidate and therefore follows the same candidate-binding model as the released Nayin and natal relation presentation sidecars.

The Workbench writes only to a dedicated sibling panel next to the Ba Zi chart and never mutates or recomputes the four pillars.
