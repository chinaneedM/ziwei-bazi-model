# Ba Zi Pillar Metadata Workbench Closure R1

Status: PRODUCT-CLOSURE IMPLEMENTATION  
Scope: deterministic read-only presentation only

## Problem

The field-parity matrix identified three Ba Zi pillar fields that were already emitted by `BaziChartService._build_view` and already travelled inside the combined Ba Zi bundle, but were not visible in the unified Workbench:

- `stem_element` — 天干五行
- `stem_polarity` — 天干阴阳
- `branch_element_affiliation` — 地支五行归属

This is a presentation gap, not a calculation gap.

## Solution

`bazi_pillar_metadata_assets.py` adds a narrow presentation sidecar to the unified Workbench. It reuses the exact successful `/api/resolve` response by cloning the browser `Response`; it does not call another calculation endpoint and does not regenerate any Ba Zi data.

For the currently selected Ba Zi application candidate, the sidecar validates every rendered pillar against the released source candidate before adding metadata:

1. expected pillar order must be `YEAR / MONTH / DAY / HOUR`;
2. rendered pillar position must equal the source pillar position;
3. rendered Ganzhi must equal the source pillar Ganzhi;
4. all three released metadata values must be non-empty strings.

Only after all four pillars pass does the sidecar append a read-only line:

`干五行：… · 阴阳：… · 支五行：…`

If validation fails, it renders nothing rather than guessing or positionally falling back to unrelated data.

## Candidate semantics

When time uncertainty creates multiple Ba Zi application candidates, the sidecar reads the explicit `.bazi-candidate-select` value and binds to that selected application candidate. A selector change triggers a fresh validation/render pass. There is no blind `bundle.candidates[0]` fallback when an explicit selector is present.

## Non-goals

This milestone does not add:

- 五行强弱 / 旺衰;
- 喜用神;
- prediction or interpretation;
- new Yin/Yang or Five-Element formulas;
- mutations to the Ba Zi bundle, selector, or core chart renderer.

The source registry semantics remain authoritative. The sidecar only exposes fields that were already released.

## Integration

The Workbench serves two additive assets:

- `/bazi-pillar-metadata.js`
- `/bazi-pillar-metadata.css`

The legacy combined `/api/resolve` response contract is unchanged.

## Validation

`tests/test_combined_browser_bazi_pillar_metadata_r1.py` locks:

- additive HTML injection;
- consumption of only the three released metadata fields;
- exact pillar position + Ganzhi validation;
- selected-candidate binding;
- read-only behavior;
- rerender on candidate change;
- real Workbench serving of both assets.

After this milestone is green, the field-parity matrix should reclassify the three rows from `ALREADY_RELEASED_NOT_YET_VISIBLE` to `ALREADY_VISIBLE` in a separate commit.
