# Shared Ziwei Target Projection Workbench R1

## Status

R1.11 productizes the existing shared Ziwei target projection inside the unified target-flow Workbench as an additive, read-only browser view.

This milestone does **not** add a new Ziwei temporal engine, change any released Ziwei formula, choose an hourly method, alter BaZi target-flow computation, or change `/api/resolve-flow` response semantics.

## Source contract

The browser consumes the existing additive response field:

`shared_ziwei_selector_projection`

The projection has already passed the R1.10 integrity and deterministic full-replay gates before the endpoint returns it. The browser does not regenerate target coordinates, lunar dates, daily frames, or hourly method candidates.

For the currently displayed BaZi target-flow candidate, the Ziwei projection is bound only when exactly one projection candidate satisfies:

`projection_candidate.source_target_candidate_id == bazi_candidate.view.target.target_coordinate_candidate_id`

There is no positional fallback from the BaZi candidate array into the Ziwei projection candidate array. A missing or non-unique identity match is rendered as an unavailable binding rather than guessed.

## Presentation semantics

The Workbench renders the shared Ziwei chain as a separate read-only section beside the existing BaZi target-flow presentation:

- Daxian frame identity;
- annual frame identity and year;
- minor-limit age/frame identity;
- monthly projection status/frame/Ganzhi;
- daily projection under the label **“紫微流日（条文规则）”**;
- every hourly method candidate under **“紫微流时候选（案例方法；未作流派裁决）”**.

The daily view surfaces its existing rule/source lineage. The hourly view iterates the complete `hourly_method_candidates` collection and surfaces each candidate's `time_standard`, `authority_status`, `rule_id`, and source refs.

No hourly candidate is selected or visually promoted. The Workbench explicitly states that all candidates are shown in parallel and that no hour is automatically chosen.

## Independence and stale-state boundary

BaZi target-flow navigation remains unchanged. The existing BaZi candidate selector still controls which BaZi target candidate is displayed.

The Ziwei browser module observes that selection and resolves the corresponding projection by exact target-candidate identity. Ziwei-only selector changes invalidate only the Ziwei projection view; they do not mutate or invalidate the independent BaZi presentation contract.

The projection view also fails closed when the visible Ziwei chart is redrawn. A new explicit target-flow resolution is required before the Ziwei projection is shown again.

## Backward compatibility

The implementation is appended to the existing `/target-flow.js` and `/target-flow.css` responses by the Workbench composer. The released `TARGET_FLOW_JS` and `TARGET_FLOW_CSS` assets themselves remain unchanged.

If `shared_ziwei_selector_projection` is absent, malformed, or has no unique identity binding for the current target candidate, the new module clears/hides its view or shows a binding-unavailable message. Existing BaZi target-flow behavior continues without a JavaScript exception.

The module reads successful `/api/resolve-flow` responses through `Response.clone()`; it does not issue a second target-flow request and does not rewrite the request body or endpoint response.

## Explicitly excluded semantics

R1.11 does not add:

- auspicious/inauspicious judgments;
- predictions or event interpretation;
- a preferred hourly school/method;
- a selected hourly candidate;
- cross-system forced synchronization;
- a second timezone/DST/solar-time calculation path.

The existing hourly authority marker `CASE_METHOD_ONLY_NOT_GLOBAL_RULE` remains presentation-visible as data from the released projection.

## Regression coverage

`tests/test_combined_browser_ziwei_target_projection_r1.py` locks:

1. exact target-candidate-ID binding and rejection of positional fallback;
2. deterministic daily-rule wording;
3. full hourly-candidate iteration with neutral, candidate-only wording;
4. absence of selected-hour/prediction language in the new asset;
5. graceful behavior when the additive projection is absent;
6. Ziwei-only stale invalidation without writing Ziwei or BaZi presentation state;
7. composition of the old target-flow assets and the new Ziwei read-only assets on the real Workbench HTTP server.

Backend lineage, DST-fold candidate preservation, replay failure, strict schema rejection, and hourly candidate semantics remain covered by the existing R1.10 tests.
