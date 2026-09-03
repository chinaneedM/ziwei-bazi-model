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
- `DISPUTED_CANDIDATE_ONLY`: the contract intentionally preserves multiple candidates. Product parity must not collapse them into a winner. A candidate-only row may be visible; the status records governance, not UI absence.

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
- Ba Zi target-flow timeline：大运 / 小运候选 / 流年 / 流月 / 流日 / 流时;
- Ba Zi target-flow classical identity annotations：十神 / 藏干 / 纳音 / 旬空 / 星运 / 自坐;
- Ba Zi target-flow neutral structural facts for released Dayun / annual / monthly layers;
- Ba Zi target-flow neutral support-evidence candidates with separate natal month-command and active-flow-month roles;
- 日主天干（直接消费 released `day_master_stem`）；
- 天干五行、天干阴阳、地支五行归属;
- 本命地支六合 / 三合 / 六冲 / 相穿（六害）/ 相刑关系事实;
- 本命天干五合关系事实;
- 本命藏干与四柱显干的 EXACT_STEM 同干匹配事实;
- shared time credentials with separate Zi Wei and Ba Zi policy labels;
- resolved combined / Zi Wei / Ba Zi Profile, RuleSet and Algorithm identities plus exact ManifestHash;
- deterministic Zi Wei target daily projection;
- Zi Wei 命宫干支 and 局纳音, read directly from the released `FiveElementBureau` natal structure;
- Zi Wei 五行局、命主/身主、命宫支/身宫支 and natal lunar coordinates already rendered by `ziwei_basic_info_assets.py`;
- Zi Wei 十二宫干支、星曜落宫/庙旺评级 and 四化标记 already rendered by the released twelve-palace SVG view;
- Zi Wei 长生十二神、岁前十二神、将前十二神、博士十二神 ring members already rendered by the released SVG view;
- Zi Wei selected Daxian/annual/month palace designations, temporal transformation badges and deterministic temporal auxiliaries;
- Zi Wei selected 小限 and annual 斗君 palace markers.

Zi Wei target hourly methods remain `DISPUTED_CANDIDATE_ONLY`: all released candidates are shown and no winner may be synthesized by the Workbench. Zi Wei dynamic Kui/Yue and Tianma method candidates are also `DISPUTED_CANDIDATE_ONLY` even after becoming visible, because visibility must not erase the no-selection contract.

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

## Visible Ba Zi natal relation inventory closure

A source-backed audit of `BaziNatalState.raw_relations` found two deterministic relation surfaces that were already released by the natal engine and are now rendered through read-only Workbench sidecars:

- `BAZI_NATAL_BRANCH_RELATIONS` — 本命地支六合、三合、六冲、相穿 / 六害、相刑关系身份;
- `BAZI_NATAL_STEM_FIVE_COMBINATIONS` — 本命天干五合关系身份.

Both rows are `ALREADY_VISIBLE`. Their backend source is the released `generate_raw_relations()` implementation in `src/fortune_training/bazi_chart/relations.py`. The branch sidecar binds to S14 sections 7.2 through 7.6; the stem sidecar binds to S14 section 7.1. Each presentation endpoint replays the exact natal candidate and requires equality of both natal FactHash and natal ComputationHash before exposing the relation participant instances.

The semantic boundary is intentionally narrow. The Workbench displays relation identity only. It does not expose `nominal_transformation_element`, does not decide whether a combination transforms, and does not synthesize structure success/failure, Five-Element strength, auspiciousness, winner selection or predictive interpretation. Multiple application candidates may legally reuse one natal candidate, so the sidecars preserve every application candidate while requiring reused natal lineages to project identical natal relation facts.

S14 does not provide a complete source table for 三会 or 破 under the current canonical closure. Those relations remain outside this productized surface rather than being filled from unsourced common mnemonics.

## Visible Ba Zi hidden-stem exact-match closure

`BaziNatalState.exposures` is also a released, hash-participating natal fact layer. `generate_exposures()` emits a link only when one concrete hidden-stem instance and one concrete visible four-pillar stem have exactly the same stem identity. `validate_natal_state()` mechanically replays the exposure set, so the presentation layer does not invent a new calculation.

`BAZI_NATAL_HIDDEN_STEM_EXPOSURE_MATCHES` records this surface as `ALREADY_VISIBLE`. The source basis is S11 section 7.3 (`地支藏干表`, current rows anchored to `YHZP-CH-061`) plus the already-released exact equality algorithm. The Workbench sidecar replays the exact natal candidate, validates natal FactHash and ComputationHash, and then renders only `match_kind=EXACT_STEM` links.

This is an identity match, not a strength judgment. The UI does not label the match as successful rooting, does not grade 通根 / 得地 / 旺衰, and does not expose the separate `affinities.same_element_hidden_stem_instance_ids` layer. Same-element affinity remains outside this closure until a distinct source-backed product semantics is justified.

## Visible Zi Wei natal inventory closure

A second audit compared the released natal model, the combined response, the basic-info renderer and `ZiweiTwelvePalaceSvgRenderer`. It found no new released-but-hidden product field in that audited surface. Instead, seven deterministic fields were already visible but absent from the Matrix inventory:

- `ZIWEI_FIVE_ELEMENT_BUREAU` — 五行局;
- `ZIWEI_MINGZHU_SHENZHU` — 命主 / 身主;
- `ZIWEI_LIFE_BODY_PALACE_BRANCHES` — 命宫支 / 身宫支;
- `ZIWEI_NATAL_LUNAR_COORDINATES` — 紫微生年 / 农历月坐标 / 农历日 / 出生时支;
- `ZIWEI_TWELVE_PALACE_GANZHI` — 十二宫干支;
- `ZIWEI_STAR_PLACEMENTS_DIGNITY` — 星曜落宫 / 庙旺评级;
- `ZIWEI_TRANSFORMATION_BADGES` — 四化标记.

These rows are classified `ALREADY_VISIBLE`. This milestone changes the parity inventory and its tests only; it does not alter the natal engine, selector, temporal coordinate lineage, SVG projection semantics or browser-side calculations. In particular, the basic-info sidecar continues to read the successful `/api/resolve` payload, while the SVG renderer continues to consume the released `ChartViewModel`.

## Visible Zi Wei ring and temporal-candidate closure

The SVG view already projected and rendered four released ring families but the parity inventory did not name them separately. They are now registered as `ALREADY_VISIBLE`:

- `ZIWEI_RING_CHANGSHENG12` — `RING.CHANGSHENG12` / 长生十二神;
- `ZIWEI_RING_TAISUI12` — `RING.TAISUI12` / 岁前十二神;
- `ZIWEI_RING_JIANGQIAN12` — `RING.JIANGQIAN12` / 将前十二神;
- `ZIWEI_RING_BOSHI12` — `RING.BOSHI12` / 博士十二神.

The same audit identified one genuine presentation gap: `PalaceViewCell.temporal_auxiliary_candidates` already carried released dynamic auxiliary-star candidates, but the SVG did not consume them. Renderer `1.2.1` now displays each candidate with its method identity and emits only identity fields that already exist on `ViewTemporalAuxiliaryCandidate`: `candidate_set_id`, `candidate_id`, `candidate_fact_hash`, `frame_type`, `frame_id`, `entity_id`, `method_id` and `authority_status`. It does not synthesize `candidate_set_hash` or a separate `star_id`.

`ZIWEI_TEMPORAL_AUXILIARY_CANDIDATES` remains `DISPUTED_CANDIDATE_ONLY`. The generator contract is still `CANDIDATES_PRESERVED_NO_SELECTION` with `MULTI_METHOD_CANDIDATES_NO_RANKING`: strict S01 Kui/Yue and WenMo-compatible Kui/Yue candidates remain side by side, and the case-method Tianma candidate remains a candidate when applicable. Neither SVG nor Workbench adds `selected`, `winner`, `rank`, priority or an inferred doctrinal verdict.

The combined Workbench already injects the backend-provided `ziwei_svg` directly, so this closure adds no second browser-side rule engine, time computation or selector.

## Visible Zi Wei temporal released-surface inventory closure

A subsequent engine → released view → SVG audit found five temporal surfaces that were already visible but had not been registered as separate Matrix rows:

- `ZIWEI_TEMPORAL_DESIGNATIONS` — selected 大限 / 流年 / 流月宫位动态标记;
- `ZIWEI_TEMPORAL_TRANSFORMATION_BADGES` — selected 大限 / 流年 / 流月 dynamic 四化 badges;
- `ZIWEI_TEMPORAL_AUXILIARIES` — deterministic non-candidate 动态流曜;
- `ZIWEI_MINOR_LIMIT_PALACE` — selected 小限落宫 marker;
- `ZIWEI_DOUJUN_PALACE` — selected annual 斗君落宫 marker.

All five are `ALREADY_VISIBLE`. `ZiweiViewProjectionCompiler` is the release boundary: it projects designation overlays to `ViewDesignationOverlay`, aggregates selected temporal transformations into `ViewPlacement.transformation_badges`, projects ordinary auxiliary activations to `ViewTemporalAuxiliary`, and places selected Minor Limit / annual Doujun frame IDs on the corresponding `PalaceViewCell`. `ZiweiTwelvePalaceSvgRenderer` only formats those released values as `时`, transformation badges, `流曜`, `小限` and `斗君` labels.

This closure intentionally does not add algorithms. In particular, ordinary `ViewTemporalAuxiliary` releases only `frame_type`, `frame_id`, `entity_id` and `label`; the Matrix must not invent candidate hashes, source metadata or ranking fields for it. The separate `ZIWEI_TEMPORAL_AUXILIARY_CANDIDATES` row remains `DISPUTED_CANDIDATE_ONLY`, and no candidate winner or priority is introduced.

The Matrix may therefore legitimately contain no `ALREADY_RELEASED_NOT_YET_VISIBLE` row. The status remains part of the R1 contract because future parity audits may identify additional released-but-hidden fields.

## Visible Ba Zi day-master inventory closure

A differential audit of `BaziChartService._build_view` and the unified `renderBazi` consumer confirms that `day_master_stem` was already released and already visible, but had no separate Matrix inventory row. `BAZI_DAY_MASTER_STEM` therefore records the field as `ALREADY_VISIBLE`.

The application view copies `chart.day_master_stem` into `view["day_master_stem"]`. The Workbench renders `日主：${view.day_master_stem}` directly from the released candidate view. It does not recover the value from the DAY pillar in browser code and adds no strength, favorable-element, auspiciousness or prediction semantics.

## Visible Ba Zi target-flow timeline inventory closure

A differential audit of `BaziApplicationFlowService._build_view`, `/api/resolve-flow` and `target_flow_assets.py` confirms that the unified Ba Zi target timeline was already released and already visible, but had no separate Matrix inventory row. `BAZI_TARGET_FLOW_TIMELINE` therefore records this product surface as `ALREADY_VISIBLE`.

The application flow emits `BAZI-UNIFIED-TARGET-TIMELINE-R1` with explicit layer order `NATAL → DAYUN → XIAOYUN → ANNUAL → MONTHLY → DAILY → HOURLY`. Dayun is the released active frame; Xiaoyun preserves every released method candidate and explicitly marks `UNRESOLVED_CLASSICAL_METHOD_ALTERNATIVES`; annual/monthly/daily/hourly are released deterministic target frames. The semantic scope remains `TEMPORAL_COORDINATES_ONLY_NO_INTERPRETATION`.

`FlowLocalCombinedChartApplication.resolve_flow_payload` returns the exact replay-validated `bazi_target_flow_bundle`. Workbench `renderCandidate` consumes `view.flow`, `view.timeline.xiaoyun.candidates`, `view.daily`, `view.hourly` and released classical annotations directly. It does not recompute Ganzhi, frame boundaries or Xiaoyun selection in browser code. This inventory closure introduces no strength, favorable-element, auspiciousness, winner or prediction semantics.

## Visible Ba Zi target-flow classical-annotation inventory closure

`BAZI_TARGET_FLOW_CLASSICAL_ANNOTATIONS` records the released `classical_annotations` product surface as `ALREADY_VISIBLE`. `temporal_classical_annotation_projection` annotates active Dayun, both Xiaoyun method candidates, annual, monthly, daily and hourly Ganzhi with visible-stem Ten God, ordered hidden stems and their Ten Gods, Nayin, Xunkong, day-master-relative Twelve Growth and self-relative Twelve Growth. Every resolved slot and the aggregate projection retain independent FactHash / ComputationHash lineage.

The projection preserves `XIAOYUN_CANDIDATES_PRESERVED_NO_WINNER`; equal annotations cannot merge or select a Xiaoyun method. Before the first Dayun, the released slot remains `PRE_DAYUN_NO_GANZHI_ANNOTATION` rather than receiving a synthetic pillar or annotation. `/api/resolve-flow` carries the projection inside the exact replay-validated `bazi_target_flow_bundle`, and Workbench `frameCard` renders the released values and status directly.

This closure adds no annotation algorithm or browser calculation. It introduces no strength, pattern, useful/favorable element, transformation-success, auspiciousness, interpretation or prediction semantics; target-time ShenSha remains an independently governed sidecar.

## Visible Ba Zi target-flow structural inventory closure

The same Application → `/api/resolve-flow` → Workbench audit confirms two additional released and already-visible target-flow surfaces that previously had no separate Matrix rows:

- `BAZI_TARGET_FLOW_STRUCTURAL_PROJECTION` — the read-only `BAZI-TARGET-FLOW-STRUCTURAL-PROJECTION-R1` view of active Dayun / annual / monthly participants, hidden stems, Ten-God bindings, exposure/affinity facts and neutral raw relation occurrences;
- `BAZI_TARGET_FLOW_STRUCTURAL_SUPPORT_PROJECTION` — the separate `BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1` view of natal month-command and active Flow solar-month roles plus exact-hidden-stem / same-element support evidence candidates.

`BaziApplicationFlowService._build_view` composes both projections into each exact target-flow candidate and binds their source and projection hashes. `FlowLocalCombinedChartApplication.resolve_flow_payload` releases that replay-validated candidate unchanged inside `bazi_target_flow_bundle`. Workbench `renderStructural` and `renderStructuralSupport` consume the two objects separately, exposing participant, relation, seasonal-role, affinity/exposure, rule/source and hash identity without running a second relation or support algorithm in browser code.

This is inventory closure only. Structural coverage remains limited to `DAYUN`, `ANNUAL` and `MONTHLY`; `XIAOYUN`, `DAILY` and `HOURLY` remain explicit exclusions. A nominal transformation element is not a transformation-success conclusion, and support evidence is not a `ROOT/NO_ROOT`, 得令, strength, weight, score, rank, winner, auspiciousness or prediction verdict.

## Visible combined resolved-profile lineage inventory closure

`COMBINED_RESOLVED_PROFILE_LINEAGE` records the already released and visible calculation-identity surface as `ALREADY_VISIBLE`. `CombinedChartApplicationResolution` carries the combined profile and the six resolved subsystem profiles for Zi Wei calculation/application/presentation and Ba Zi natal/temporal/application. The combined service validates those exact profile objects, their subsystem bindings and the final `ManifestHash`; the resolved profile snapshots separately retain their released RuleSet and Algorithm identities and versions.

`LocalCombinedChartApplication.resolve_payload` exposes the validated resolution and matching combined manifest through `/api/resolve`. Workbench `resolved_profile_lineage_assets.py` reads that successful response, requires combined integrity `PASS` plus a non-empty `manifest_hash`, then displays the backend-provided Profile / RuleSet / Algorithm identities and versions. It neither calls another calculation endpoint nor maintains a browser-side profile or rule registry.

This is inventory closure only. Profile identity means that one exact deterministic chart used one versioned calculation snapshot. It does not select a canonical doctrine winner, promote a compatibility profile to classical authority, unify Zi Wei and Ba Zi rules, formalize self-transformation direction, or add strength, auspiciousness, interpretation or prediction semantics.

## Governance

Future field-parity work follows this order:

1. inspect the deterministic engine output;
2. confirm whether the field reaches the released API/product bundle;
3. inspect the unified Workbench renderer;
4. classify the row using the four statuses above;
5. prioritize `ALREADY_RELEASED_NOT_YET_VISIBLE` rows;
6. touch core calculation logic only if the field is genuinely absent and a canonical source-backed rule is required.

Internal hashes, registry ordinals, generator/rule trace IDs and source anchors are not automatically product fields. They should be added to the matrix only when they have a defined user-facing or compatibility purpose.

## Validation

`tests/test_fusion_chart_field_parity_matrix_r1.py` guards the original evidence claims. `tests/test_fusion_chart_field_parity_ziwei_natal_visible_r1.py` proves that the seven Zi Wei natal inventory rows are registered as already visible. `tests/test_fusion_chart_field_parity_ziwei_temporal_auxiliary_r1.py` guards the four visible ring rows and the candidate-only dynamic auxiliary row, including exact released view-field parity for the SVG metadata. `tests/test_fusion_chart_field_parity_ziwei_temporal_released_surface_r1.py` guards the five already-visible temporal released-surface rows and the no-recalculation boundary from temporal engine through released view to SVG.

`tests/test_fusion_chart_field_parity_bazi_relations_visible_r1.py` guards the two Ba Zi natal relation rows, exact sidecar lineage/hash binding, and the non-judgmental presentation boundary that excludes transformation-element, winner, strength and prediction semantics. `tests/test_fortunechart_bazi_hidden_exposure_presentation_r1.py` guards the exact hidden/visible same-stem product surface and its exclusion of affinity/strength semantics. `tests/test_bazi_day_master_stem_product_closure_r1.py` guards the day-master Matrix row, application copy projection, direct Workbench consumption, and the no browser re-derivation / interpretive-semantics boundary. `tests/test_bazi_target_flow_timeline_product_closure_r1.py` guards the target-flow Matrix row, released timeline schema/layer order, exact `/api/resolve-flow` bundle exposure, direct Workbench consumption and non-interpretive boundary. `tests/test_bazi_target_flow_classical_annotations_product_closure_r1.py` guards the target-time classical annotation Matrix row, full released annotation set, candidate/pre-Dayun boundaries and direct Workbench consumption. `tests/test_bazi_target_flow_structural_product_closure_r1.py` guards both target-flow structural Matrix rows, exact released schemas and coverage, direct separate Workbench consumption, and the no-effect / no-root-verdict semantic boundaries.
