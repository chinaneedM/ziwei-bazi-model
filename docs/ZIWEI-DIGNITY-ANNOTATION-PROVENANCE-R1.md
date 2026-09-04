# ZIWEI Dignity Annotation Provenance R1

## Status

Released deterministic presentation sidecar for the existing Ziwei `DignityAnnotation` facts.

This release does **not** add a Dignity/brightness calculation rule. It exposes the exact annotation provenance already carried by the selected Ziwei application bundle.

## Semantic boundary

The sidecar schema is:

`ZIWEI-DIGNITY-ANNOTATION-PROVENANCE-SIDECAR-R1`

The fixed semantic scope is:

`EXISTING_DIGNITY_ANNOTATION_PROVENANCE_ONLY_NOT_S01_FROZEN_BRIGHTNESS_NO_AUSPICIOUSNESS_STRENGTH_OR_PREDICTION`

The fixed authority fields are:

- `authority_class = PROJECT_OPERATIONAL_REGISTRY`
- `s01_brightness_authority = NOT_CLAIMED`

These fields are required because S01's active runtime boundary says:

- `BRIGHTNESS_PRIMARY_INPUT=FROZEN_CHART`
- `S01_RECALCULATE_BRIGHTNESS_PERMISSION=NO`
- `SOURCE_BRIGHTNESS_REFERENCE_CAN_OVERWRITE=NO`

Therefore the project's operational Dignity registry must not be relabeled as S01 canonical frozen-chart brightness.

## Released facts

For each existing `DIGNITY` annotation, the sidecar publishes only already released deterministic identity/provenance:

- annotation id
- target star identity and display label
- exact target palace address
- existing annotation `status` and `grade`
- scale id/version
- rule-set id/version
- generator id/algorithm version
- source refs
- row FactHash / ComputationHash

At the resolution level it publishes:

- exact source application bundle hash
- exact natal FactHash / ComputationHash
- exact source Dignity rule-set and algorithm bindings
- sidecar FactHash / ComputationHash / BundleHash
- integrity report

The production Ziwei profile currently selects `OPERATIONAL-ZIWEI-DIGNITY-R4@4.0.0`, but the sidecar validates the exact Dignity identity present in the supplied application profile rather than re-running a browser-side registry.

## Source binding and replay

The local endpoint is:

`POST /api/ziwei-dignity-provenance`

It resolves from the same combined request as the main Workbench, reconstructs the exact Ziwei application bundle, and fails closed unless the sidecar source hash equals the combined resolution's Ziwei bundle hash.

Resolution is replayed twice. Identical source bundles must produce identical provenance objects.

## Workbench contract

Workbench 1.11 adds the read-only panel:

`庙旺注解来源 / 权威边界`

The browser consumes backend-published rows. It does not contain a Dignity registry, star identity classification table, or brightness selector.

The panel explicitly states that the operational registry is not S01 frozen-chart brightness authority.

## Explicit non-goals

This release does not publish or infer:

- S01 frozen-chart brightness values
- a new brightness recalculation method
- auspiciousness / inauspiciousness
- benefic / malefic star classification
- strength scores or strength verdicts
- prediction or event interpretation
- a doctrinal winner among competing external systems

WenMo calibration references remain provenance evidence only. They are not promoted to canonical authority.
