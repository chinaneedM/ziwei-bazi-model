# ZiWei Temporal Auxiliary Candidate Presentation R1

## Scope

This milestone is a read-only presentation closure for already-released ZiWei temporal auxiliary candidates. It does not add or alter star-placement rules, target-frame selection, shared time credentials, or temporal coordinates.

The released projection path is:

`ZiweiTemporalAuxiliaryCandidateGenerator` → `PalaceViewCell.temporal_auxiliary_candidates` → `ZiweiTwelvePalaceSvgRenderer` → combined Workbench `ziwei_svg`.

## Candidate semantics

The generator contract remains:

- schema: `ZIWEI-TEMPORAL-AUXILIARY-CANDIDATES-V1`
- semantic status: `CANDIDATES_PRESERVED_NO_SELECTION`
- method policy: `MULTI_METHOD_CANDIDATES_NO_RANKING`

The SVG therefore exposes every projected candidate in existing view order and preserves the released presentation identity:

- `candidate_set_id`
- `candidate_set_hash`
- `candidate_id`
- `candidate_fact_hash`
- `frame_type`
- `star_id`
- `method_id`
- `authority_status`

Visible labels include the method identity. No `selected`, `winner`, `rank`, priority, merge, or transformation verdict is introduced.

In particular, the strict S01 Kui/Yue method and the WenMo-compatible Kui/Yue method remain side-by-side candidates. The case-method Tianma candidate remains a candidate when its trigger applies.

## Source boundary

The existing generator declares the following source closure and this presentation layer does not load sources at runtime:

- S01 §十四（天魁/天钺、禄羊陀、天马）
- S01 §十七/步骤6（大限、流年动态星）
- S19（天魁、天钺、天马标准ID/别名）

Compatibility evidence is descriptive only; it does not override the canonical candidate policy.

## Workbench behavior

The combined Workbench already renders the backend-provided `ziwei_svg` directly. Therefore the SVG presentation is the Workbench presentation: no second browser-side rule engine, candidate resolver, or temporal recomputation is added.

`SvgRendererProfile(show_temporal=False)` suppresses both visible candidate labels and candidate metadata groups.

## Non-goals

This milestone does not:

- choose a preferred method;
- infer good/bad fortune, strength, transformation success, or predictive meaning;
- change target frame or day-switch semantics;
- modify `ZiweiTemporalAuxiliaryCandidateGenerator`;
- modify `ChartViewModel` or its hash contract;
- add unsupported ZiWei rules from compatibility software.
