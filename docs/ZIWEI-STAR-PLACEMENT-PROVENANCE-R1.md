# Ziwei Star Placement Provenance R1

## Scope

This release is a deterministic chart-presentation sidecar only. It exposes how each already-released natal star placement was generated and, for the fourteen main stars, which already-released main-star source family supplied the placement. It does not classify stars by auspiciousness, strength, event meaning, or doctrinal nature.

Schema: `ZIWEI-STAR-PLACEMENT-PROVENANCE-SIDECAR-R1`

Semantic scope: `PLACEMENT_GENERATOR_PROVENANCE_ONLY_NO_AUSPICIOUSNESS_OR_DOCTRINAL_STAR_CLASSIFICATION`

Classification policy: `GENERATOR_IDENTITY_AND_RELEASED_MAIN_STAR_SOURCE_REFS_ONLY`

## Released provenance families

The sidecar derives its family identity only from the `generator_id` already stored on each released `Placement`:

- `FOURTEEN_MAIN_STARS` — 十四主星
- `CORE_AUXILIARY` — 核心辅曜
- `DERIVED_AUXILIARY` — 派生辅曜
- `OPERATIONAL_MINOR_STARS` — 小星

An unknown placement generator fails closed instead of being guessed into a family.

For fourteen-main-star placements only, the existing main-star generator already carries two immutable source-reference tuples. The sidecar exposes those as:

- `ZIWEI_SYSTEM` — 紫微星系
- `TIANFU_SYSTEM` — 天府星系

No browser-side star-name list is used to make this split.

## Source binding

`ZiweiStarPlacementProvenanceService` accepts an existing validated `ApplicationChartBundle`. Every released provenance row preserves:

- entity id and display name;
- released palace address index and branch;
- generator id and algorithm version;
- backend generator-family id and label;
- optional main-star source-family id and label;
- original placement `source_refs`;
- row FactHash and ComputationHash.

The resolution additionally preserves the exact source application bundle hash plus the natal FactHash and ComputationHash.

The local endpoint `/api/ziwei-star-provenance` rebuilds the same Ziwei application request used by the combined Workbench, including the selected lunar-month coordinate, and requires the controller bundle hash and provenance source bundle hash to equal the exact combined Ziwei bundle hash.

## Integrity and replay

Validation is fail-closed. It recomputes generator-family identity, main-star source-family identity, every row FactHash/ComputationHash/row id, and the resolution FactHash/ComputationHash/BundleHash. Identical source application bundles must replay to an identical sidecar.

## Workbench boundary

The Workbench consumes only released backend fields such as `generator_family_label`, `main_star_system_label`, `generator_id`, `algorithm_version`, and `source_refs`. The browser asset contains no star entity classification table and no generator-id-to-family rule table.

The panel explicitly states that generation-source grouping is not a judgment of 吉凶, 强弱, or doctrinal star nature.

## Non-goals

This R1 does not release:

- 吉星 / 煞星 winner classifications;
- star-strength or favorable/unfavorable verdicts;
- prediction or event interpretation;
- browser-side reconstruction of placement rules;
- a new natal placement engine or a new ViewHash contract.
