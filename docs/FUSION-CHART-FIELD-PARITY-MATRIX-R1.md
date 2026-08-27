# Fusion Chart Field Parity Matrix R1

Status: ACTIVE PRODUCT-CLOSURE CONTRACT  
Scope: deterministic Zi Wei + Ba Zi charting only

## Purpose

`FUSION-CHART-FIELD-PARITY-MATRIX-R1.json` turns the product-closure audit into an evidence-backed, machine-readable field register. It exists to stop two recurring classes of error:

1. treating a field that is already visible in the unified Workbench as if it were still missing; and
2. treating a field that is already released by the deterministic engine as if a new classical formula were required merely because the UI does not render it.

The matrix is deliberately conservative. A row is added only when backend, API and Workbench evidence can be named. 文墨天机 and 问真八字 remain compatibility references, never doctrinal authorities.

## Status semantics

- `ALREADY_VISIBLE`: released deterministic data is already visible in the unified Workbench.
- `ALREADY_RELEASED_NOT_YET_VISIBLE`: released deterministic data reaches the product response but the Workbench does not yet consume it. These rows are the highest-value product-closure targets.
- `NOT_YET_FORMALIZED`: no released deterministic contract has been confirmed. Such a row requires source-backed rule formalization before UI work.
- `DISPUTED_CANDIDATE_ONLY`: the contract intentionally preserves multiple candidates. Product parity must not collapse them into a winner.

A missing UI field is therefore not evidence of a missing calculation rule.

## R1 evidence baseline

The first matrix is audited against commit `bea613f332a236bc4a8fde8b20d8023539fe33e5`, immediately after the R1.11 read-only Zi Wei target-projection Workbench closure.

The baseline explicitly records as already visible:

- Ba Zi four pillars, visible Ten Gods and hidden stems;
- Xunkong and both twelve-growth annotations (`星运` / `自坐`);
- 胎元 / 命宫 / 身宫;
- Xiaoyun method candidates;
- natal ShenSha fact candidates;
- Nayin presentation;
- Dayun / Jiaoyun;
- shared time credentials with separate Zi Wei and Ba Zi policy labels;
- deterministic Zi Wei target daily projection.

Zi Wei target hourly methods remain `DISPUTED_CANDIDATE_ONLY`: all released candidates are shown and no winner may be synthesized by the Workbench.

## First confirmed product-closure gaps

The first three `ALREADY_RELEASED_NOT_YET_VISIBLE` rows are narrow Ba Zi pillar metadata already emitted by `BaziChartService._build_view`:

- `stem_element` — 天干五行
- `stem_polarity` — 天干阴阳
- `branch_element_affiliation` — 地支五行归属

The unified `renderBazi` does not currently consume those keys. They are therefore UI-only closure work. The natal engine must not be modified to add them again.

## Governance

Future field-parity work follows this order:

1. inspect the deterministic engine output;
2. confirm whether the field reaches the released API/product bundle;
3. inspect the unified Workbench renderer;
4. classify the row using the four statuses above;
5. prioritize `ALREADY_RELEASED_NOT_YET_VISIBLE` rows;
6. touch core calculation logic only if the field is genuinely absent and a canonical source-backed rule is required.

Internal hashes, registry ordinals and semantic-role IDs are not automatically product fields. They should be added to the matrix only when they have a defined user-facing or compatibility purpose.

## Validation

`tests/test_fusion_chart_field_parity_matrix_r1.py` guards the initial evidence claims. In particular it ensures that fields already visible in the Workbench are not regressed into the missing category, verifies the three first UI-only gaps against the backend and renderer source, and preserves candidate-only Zi Wei hourly semantics.
