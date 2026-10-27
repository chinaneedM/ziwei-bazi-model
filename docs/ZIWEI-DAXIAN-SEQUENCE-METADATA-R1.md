# ZiWei Daxian Sequence Metadata R1

## Scope

This milestone closes one presentation gap for deterministic Zi Wei temporal state. The temporal engine already releases two sequence-level facts on `ZiweiTemporalState`:

- `daxian_direction`
- `first_daxian_nominal_age`

R1 copy-projects those facts into the released chart view and renders them in the server-generated SVG. It does not add or rerun a Daxian calculation rule.

## Released view contract

`ViewDaxianSequenceMetadata` contains exactly:

- `daxian_direction`: `FORWARD` or `REVERSE`
- `first_daxian_nominal_age`: the canonical first Daxian nominal age from `ZiweiTemporalState`

`ChartViewModel.daxian_sequence_metadata` is `null` when no temporal state is supplied. When a temporal state is supplied, both values are copied directly from that validated state.

The metadata participates in `view_hash` and therefore in application export/replay validation.

## Presentation boundary

`ZiweiTwelvePalaceSvgRenderer` displays the released values in the chart center only when temporal rendering is enabled. The combined Workbench continues to consume the server-produced `ziwei_svg` directly and performs no Daxian direction or starting-age calculation in JavaScript.

This metadata is Daxian-specific. It must not be reused as a Minor Limit direction or as evidence for any separate disputed temporal technique.

## Non-goals

R1 does not:

- change `ZiweiTemporalEngine`;
- introduce a second time or selector engine;
- infer a Minor Limit direction;
- infer a start palace, step count, overlap relation, auspiciousness, strength, or prediction;
- select among disputed methods.

## Closure gates

The milestone is closed only when focused tests, the parity matrix, strict view schema, application replay checks, full unit tests, `fortune-train verify`, and `combined-workbench-smoke` pass on the same commit.
