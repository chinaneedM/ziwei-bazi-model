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

The matrix originated from the audit at commit `bea613f332a236bc4a8fde8b20d8023539fe33e5`, immediately after the R1.11 read-only Zi Wei target-projection Workbench closure. `evidence_baseline_commit` intentionally remains that initial audit anchor; individual rows may subsequently move from a gap state to a closed state when their Workbench evidence changes.

The register records as visible:

- Ba Zi four pillars, visible Ten Gods and hidden stems;
- Xunkong and both twelve-growth annotations (`星运` / `自坐`);
- 胎元 / 命宫 / 身宫;
- Xiaoyun method candidates;
- natal ShenSha fact candidates;
- Nayin presentation;
- Dayun / Jiaoyun;
- 天干五行、天干阴阳、地支五行归属;
- shared time credentials with separate Zi Wei and Ba Zi policy labels;
- deterministic Zi Wei target daily projection;
- Zi Wei 命宫干支 and 局纳音, read directly from the released `FiveElementBureau` natal structure.

Zi Wei target hourly methods remain `DISPUTED_CANDIDATE_ONLY`: all released candidates are shown and no winner may be synthesized by the Workbench.

## Closed first product-closure gaps

The first three rows originally classified `ALREADY_RELEASED_NOT_YET_VISIBLE` were narrow Ba Zi pillar metadata already emitted by `BaziChartService._build_view`:

- `stem_element` — 天干五行
- `stem_polarity` — 天干阴阳
- `branch_element_affiliation` — 地支五行归属

They are now `ALREADY_VISIBLE`. The closure is presentation-only: `bazi_pillar_metadata_assets.py` reuses the exact successful combined response, binds to the explicitly selected Ba Zi application candidate, validates pillar position and Ganzhi identity, then renders the three released values. No natal formula, Five-Element strength rule, polarity rule, prediction rule, or candidate winner was added.

The same product-closure principle now covers two Zi Wei natal fields that were already released in `FiveElementBureau` but hidden from the Workbench:

- `life_palace_ganzhi` — 命宫干支
- `nayin_name` — 局纳音

Both are now `ALREADY_VISIBLE`. `ziwei_basic_info_assets.py` consumes the exact successful `/api/resolve` response and renders those two fields from `combined_resolution.ziwei_bundle.candidate.chart.structure.bureau`. No Life-Palace stem derivation, Nayin lookup, chart regeneration, interpretation, or selector mutation occurs in the browser.

The matrix may therefore temporarily contain no `ALREADY_RELEASED_NOT_YET_VISIBLE` row. The status remains part of the R1 contract because future parity audits may identify additional released-but-hidden fields.

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

`tests/test_fusion_chart_field_parity_matrix_r1.py` guards the evidence claims. It verifies that currently visible fields are not regressed into a missing category, proves the closed Ba Zi pillar metadata rows are consumed by the read-only sidecar from released source fields with exact-candidate/pillar validation, proves the Zi Wei 命宫干支 / 局纳音 rows are consumed directly from the released bureau structure without browser-side recomputation, and preserves candidate-only Zi Wei hourly semantics.