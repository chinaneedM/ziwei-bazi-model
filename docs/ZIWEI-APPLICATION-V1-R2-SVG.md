# Ziwei Application V1-R2 — Twelve-Palace SVG Renderer

## Status

```text
RENDERER_ID=ZIWEI-TWELVE-PALACE-SVG-RENDERER-V1
RENDERER_VERSION=1.0.0
APPLICATION_PACKAGE_VERSION=1.1.0
STATUS=ACTIVE_APPLICATION_V1_R2_SVG
ACTIVATION_CONDITION=MERGED_TO_MAIN
UPSTREAM_APPLICATION=ZIWEI-APPLICATION-V1@1.0.0
ISSUE=#209
PR=#210
```

The status above is effective only when this document is present on `main`. A feature-branch copy is not an active renderer release.

This slice is downstream presentation only. It does not reopen Ziwei Foundation and does not alter V1, Temporal, Structural R1-R5, canonical sources, training state, model-learning or prediction controls.

## Public path

```text
ApplicationBirthRequest
-> ZiweiChartService.resolve()
-> ApplicationChartBundle
-> ChartViewModel
-> ZiweiTwelvePalaceSvgRenderer.render()
-> SvgRenderArtifact
```

The SVG renderer consumes `ChartViewModel` only. It does not receive a natal chart, temporal state or structural state.

## Twelve-palace geometry

The renderer uses the conventional 4 × 4 outer-ring Ziwei board. The center 2 × 2 area is reserved for renderer-neutral metadata.

```text
巳  午  未  申
辰          酉
卯          戌
寅  丑  子  亥
```

`address_index` is the geometry authority. Input `ChartViewModel.cells` tuple order is not a layout authority.

Frozen address-to-grid coordinates:

```text
子=0 -> (2,3)
丑=1 -> (1,3)
寅=2 -> (0,3)
卯=3 -> (0,2)
辰=4 -> (0,1)
巳=5 -> (0,0)
午=6 -> (1,0)
未=7 -> (2,0)
申=8 -> (3,0)
酉=9 -> (3,1)
戌=10 -> (3,2)
亥=11 -> (3,3)
```

This mapping is a renderer layout contract, not a new Ziwei structural fact.

## Visible content

Each palace group renders labels already present in `ChartViewModel`:

- palace stem/branch;
- natal palace designation;
- placements;
- Dignity status/grade;
- transformation badges;
- ring-member labels when enabled;
- Daxian / Annual / Minor-Limit overlay labels when enabled.

A full deterministic cell description is also stored in the SVG `<title>` element so compact visible layout does not redefine the underlying ViewModel.

The center panel contains only presentation metadata:

- presentation profile identity;
- selected temporal frame IDs;
- abbreviated FactHash and ViewHash when enabled.

No interpretation or prediction text is generated.

## Renderer profile

`SvgRendererProfile` owns renderer-only choices:

- width / height;
- margin / cell padding;
- font-family fallback string;
- header/body/metadata font sizes;
- show/hide hash, ring and temporal fields already present in the ViewModel.

Lexeme changes remain owned by `PresentationProfile` upstream. The renderer does not create a second naming system.

## Hash separation

The new `RenderHash` commits to:

- source `ViewHash`;
- `SvgRendererProfile`;
- renderer ID/version;
- frozen twelve-palace grid geometry;
- generated standalone SVG bytes.

Therefore:

```text
calculation fact change
-> FactHash + ComputationHash + ViewHash + RenderHash may change

presentation/lexeme selection change
-> ViewHash + RenderHash may change

renderer-only geometry/style change
-> RenderHash changes
-> FactHash / ComputationHash / ViewHash stay unchanged
```

## Safety boundary

Generated SVG:

- XML-escapes all user-facing labels before insertion;
- contains no JavaScript;
- contains no external images;
- contains no external fonts;
- contains no network dependencies;
- rejects unsupported ViewModel schema;
- requires exactly twelve unique address cells;
- canonicalizes cell and member ordering before rendering.

## Release validation gate

The exact merge-candidate head must pass:

- application fixture `1994-05-17 14:30 Beijing male` renders valid standalone SVG;
- exactly 12 unique palace groups;
- deterministic address geometry;
- selected temporal overlays visible;
- Dignity/transformation content preserved from ViewModel;
- repeated render byte-identical and RenderHash-identical;
- ViewModel cell tuple reordering does not change SVG;
- presentation lexeme change changes ViewHash and RenderHash;
- renderer-only geometry change changes RenderHash only;
- unsafe XML text is escaped;
- SVG artifact validates against independent JSON Schema;
- render call does not mutate source ViewModel;
- branch is behind=0;
- repository bootstrap PASS;
- `fortune-train verify` PASS;
- full unittest PASS;
- diff audit confirms no calculation/canonical/training/model-learning/prediction mutation.

## External calibration remains separate

Issue #208 remains the authoritative external Wenmo acceptance task. A visually plausible SVG is not evidence that the calculation matches the reference software. Renderer release and chart-calculation acceptance are separate gates.

After this renderer is active, the next product choice is between:

1. wrapping this standalone SVG in a local interactive application shell; or
2. completing the first Wenmo ChartDiff and fixing any genuine deterministic mismatch before further UI work.
