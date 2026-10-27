# ZiWei Transformation Provenance Workbench Presentation R1

## Scope

This milestone closes a presentation-only gap for the already released Zi Wei `TransformationActivation` rows carried by:

`combined_resolution.ziwei_bundle.candidate.chart.transformations`

It does not add or change the S08 transformation assignment table, transformation generation, star placement, palace-stem topology, temporal selection, day-boundary policy, doctrine selection, auspiciousness, interpretation, prediction, or training behavior.

## Released source contract

The canonical Zi Wei chart already publishes each `TransformationActivation` with:

- `activation_id`
- `transformation_type`
- `target_entity_id`
- `target_display_name`
- `target_address`
- `source_layer`
- `source_stem`
- `context_id`
- `assignment_id`
- `mechanism_id`
- `generator_id`
- `algorithm_version`
- `source_refs`

The Workbench presentation copies those released values from the successful `/api/resolve` payload. It does not reconstruct the S08 assignment table or resolve a target star independently.

## Workbench presentation

`src/fortune_training/combined_chart_application/ziwei_transformation_provenance_assets.py` is an additive read-only sidecar.

After a successful `/api/resolve`, it:

1. reads only `combined_resolution.ziwei_bundle.candidate.chart.transformations`;
2. requires an array and validates the minimum released lineage shape before presentation;
3. preserves canonical row order and does not sort or select activations;
4. shows transformation type, target, address, source layer/stem, context, assignment/mechanism, generator/version and source references;
5. keeps `activation_id` and `target_entity_id` in a subordinate technical trace instead of promoting raw internal identifiers to the primary chart surface;
6. clears and hides the panel when the field is absent, empty, malformed, a response cannot be parsed, or a new form submission starts.

The browser constructs text with DOM `textContent`; released payload values are not inserted as HTML.

`workbench_local_app.py` publishes the CSS/JS assets over the existing loopback server. No new backend endpoint or schema is introduced, and `CombinedChartWorkbenchLocalApp/1.12` is retained because the browser surface is additive and read-only.

## Safety boundaries

- `ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` remains `NOT_YET_FORMALIZED`.
- Palace-stem `SAME` / `OPPOSITE` / `OTHER` topology is not promoted to outward/inward self-transformation direction.
- `ZIWEI_TARGET_HOURLY_CANDIDATES` remains `DISPUTED_CANDIDATE_ONLY`.
- The browser does not contain or reproduce the S08 40-row assignment table.
- The browser does not choose a transformation ruleset or doctrine winner.
- Zi Wei and Ba Zi time/day-boundary policies remain independent.
- No prediction, auspiciousness, strength, preference, or interpretation decision is introduced.

## Field Parity Matrix boundary

This milestone does not edit `docs/FUSION-CHART-FIELD-PARITY-MATRIX-R1.md` merely to mark a presentation closure. The canonical transformation field already exists; this change only exposes its released provenance in the local Workbench.

## Verification closure

Closure requires same-SHA PASS for:

- `fortune-train verify`
- full `python -m unittest discover -s tests -p 'test_*.py'`
- `python scripts/combined-workbench-smoke.py`
