# Ziwei Four-Transformation Historical Candidate Productization R1

Status: **CLOSED FOR READ-ONLY WHOLE-TABLE CANDIDATE VISIBILITY / NO PRODUCTION WINNER CHANGE**

## Contract

```text
candidate_api=ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATE-API-R1@1.0.0
registry=ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATES-R1@1.0.0
runtime_resolver=ZIWEI-FOUR-TRANSFORMATION-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0
selection_status=PRESERVED_NOT_SELECTED
whole_table_only=true
cell_level_hybridization_allowed=false
endpoint=/api/ziwei-four-transformation-candidates
```

The endpoint returns both divergent source-scoped families for the validated natal source stem:

- `RECEIVED-FULLBOOK-SHIDIAN-V3-FOUR-TRANSFORMATION-R1`
- `ZHONGZHOU-WANGTINGZHI-FOUR-TRANSFORMATION-R1`

It does not accept a winner selector.

## Source binding

The sidecar re-resolves the exact Ziwei application bundle used by the combined result and returns:

- combined manifest hash;
- Ziwei bundle hash;
- natal FactHash / ComputationHash;
- historical registry hash;
- each candidate runtime hash;
- source refs and source-family identity.

The source stem is read from the validated Ziwei natal structure.

## Browser boundary

The Workbench shows both source families side by side. It renders backend-returned `transformation_type` and `target_display_name` fields only.

The browser contains no historical table constants, no modulo/table computation, no cell editor, no winner button and no production profile selector.

## Production firewall

`S08_CURRENT_40_ASSIGNMENT_R1` remains the production rule set.

```text
production_default_changed=false
candidate_winner_selected=false
chart_algorithm_reopened=false
```

Product visibility is evidence inspection, not historical arbitration.
