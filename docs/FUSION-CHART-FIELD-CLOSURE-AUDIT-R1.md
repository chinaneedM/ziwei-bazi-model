# Fusion Chart Field Closure Audit R1

## Decision

```text
AUDIT_ID=FUSION-CHART-FIELD-CLOSURE-AUDIT-R1
STATUS=PASS_WITH_EXPLICIT_PRODUCT_BACKLOG
BASELINE_BRANCH=agent/fusion-chart-core-r1-20260822
BASELINE_COMMIT=cf6a4fa952d242384f0dce6083cb5a13802a1af0
CURRENT_STRUCTURAL_CLOSURE=R1-R8
MANDATORY_DETERMINISTIC_CORE=CLOSED
NEXT_PHASE=FIELD_PARITY_AND_PRODUCT_CLOSURE
```

This audit freezes the deterministic Ziwei + Bazi fusion charting baseline and classifies remaining work by field family. The original baseline commit remains historical evidence; the active branch has subsequently extended the read-only Ziwei structural surface through R8 and productized R6-R8 through an additive application sidecar. This audit is a product/charting audit only. It does not authorize prediction, interpretation, model training, winner selection among disputed schools, or silent reconciliation of Ziwei and Bazi time conventions.

The audit uses the repository contracts as authority for what is already released. Wenmo Tianji and Wenzhen Bazi are compatibility/reference products only; their displayed fields may identify product-parity gaps but do not override canonical source rules or existing typed runtime contracts.

## Core invariant

The fusion product has one shared physical target-time credential, but each subsystem keeps its own deterministic policy projection:

```text
shared civil / UTC / location / solar-time credential
        ├── Bazi calculation profile
        │      ├── Bazi day boundary
        │      ├── late-Zi stem policy
        │      └── Start-of-Spring / Jie flow coordinates
        └── Ziwei calculation profile
               ├── Ziwei chart-date policy
               ├── leap-month policy
               └── Ziwei daily/hourly selector projection
```

No fusion layer may make one subsystem's day-boundary, leap-month, or late-Zi convention overwrite the other subsystem.

## A. Shared time / calendar / candidate lineage — CLOSED

Released coverage includes:

- civil local datetime, timezone and location identity;
- historical timezone handling;
- UTC resolution;
- true/local-apparent-solar-time provenance;
- DST fold/gap handling;
- uncertainty candidate preservation;
- shared time credential and candidate-lineage hashes;
- subsystem-specific policy projections;
- explicit target-time / target-place coordinates;
- target-time replay into both Ziwei and Bazi without cross-overwrite.

The R2 combined target-flow fusion binds the exact same target-coordinate resolution into the released Bazi target-flow bundle and Ziwei selector projection while preserving independent subsystem semantics.

Status: **CLOSED**.

## B. Bazi natal identity fields — CLOSED

Released deterministic natal/application coverage includes:

- four pillars;
- hidden stems;
- visible and hidden Ten Gods;
- Nayin annotation;
- Xunkong;
- Twelve Growth / Changsheng annotations;
- Taiyuan;
- Minggong;
- Shenggong;
- neutral stem/branch relation identities;
- explicit candidate identity and integrity hashes.

These are chart facts or profiled annotations. They do not imply strength, pattern, favorable element, or event interpretation.

Status: **CLOSED for deterministic chart identity**.

## C. Bazi temporal chain — CLOSED

Released typed chain:

```text
Natal
  -> Jiaoyun / Dayun
  -> Annual
  -> Monthly
  -> Daily
  -> Hourly
```

The target-flow application integration preserves PRE_DAYUN, Dayun, Annual, Monthly, Daily and Hourly identities, target-coordinate provenance, structural projections and candidate lineage.

Xiaoyun remains explicitly candidate-preserving where source methods differ. The product must not silently select one school as universal truth.

Status: **CLOSED**.

## D. Bazi ShenSha — RELEASED CORE, PRODUCT EXPANSION OPEN

The repository already contains a source-bound deterministic ShenSha fact registry and preserves alternate anchors separately where source rules differ.

Current status does not mean "all ShenSha ever used by every commercial product". New ShenSha items should be added only when:

1. the rule is source-identifiable;
2. the anchor domain is explicit;
3. conflicting source methods are represented as distinct profiles/candidates rather than merged;
4. the output remains a fact annotation and not an interpretive verdict.

Status: **CORE RELEASED; PARITY EXPANSION OPEN**.

## E. Ziwei natal structure and physical inventory — CLOSED

Released deterministic Ziwei coverage includes:

- twelve-palace structure and palace Ganzhi;
- Life/Body palace geometry;
- Five Bureau;
- fourteen main stars;
- released auxiliary / dependent / minor-star inventory;
- role bindings;
- four ring runtimes;
- natal transformations;
- dignity annotations, including explicit unrated states where the released registry has no grade;
- deterministic fact/computation hashes and integrity replay.

Status: **CLOSED for current released physical inventory**.

## F. Ziwei structural relations — CLOSED FOR RELEASED R1-R8

Released chain:

```text
R1 neutral Z12 topology
-> R2 relative palace frame
-> R3 borrow projection
-> R4 named opposition / trine / Sanfang-Sizheng semantics
-> R5 borrow-resolved composition view
-> R6 Qishu position projection
-> R7 One-Six Common-Root projection
-> R8 adjacent-palace pair geometry
```

R3 preserves physical-resolution identity through `structure_physical_key`. R4 preserves canonical semantic identity through `axis_key` and `group_key`. R5 composes both without creating a second physical inventory or a second independent semantic cause.

R6 is a separately versioned S04-backed directed Qishu relation over R2 ordinal 9 / clockwise offset 4. R7 is a separately versioned S04-backed One-Six Common-Root relation. R8 exposes the two mechanically adjacent palace identities around each origin while explicitly withholding flank/夹宫/夹格 semantics.

The application-facing `ZiweiStructuralRelationProjectionService` composes R6-R8 as a read-only sidecar bound to the exact released `ApplicationChartBundle` and R2 hashes. The unified Workbench consumes that sidecar through `/api/ziwei-structural-relations`; it does not recompute structural geometry in browser JavaScript.

Each structural layer remains independently versioned, hashed and integrity-validated. The R6-R8 sidecar additionally performs full replay and publishes a composition bundle hash without changing the frozen V1 application-bundle hash contract.

The following remain outside this closure unless separately formalized from source-backed mechanical rules:

- 夹宫 / 夹格成立判断;
- pair-geometry strength;
- motif/configuration compiler;
- dynamic structural projection beyond the time layers explicitly released by each profile;
- event, endpoint, score, auspiciousness or predictive interpretation.

`ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` remains `NOT_YET_FORMALIZED`. SAME/OPPOSITE/OTHER palace topology and R8 adjacency geometry are not selectors for OUTWARD_DISSIPATION / INWARD_RECEPTION.

Status: **CLOSED for released R1-R8; interpretive/flank extensions remain unclaimed**.

## G. Ziwei temporal fields — CORE CLOSED, FULL PRODUCT PARITY OPEN

Released temporal/runtime coverage includes:

- Daxian;
- Annual frames;
- Minor Limit;
- Doujun;
- regular monthly frames;
- temporal designation overlays;
- temporal transformations;
- target daily/hourly Ziwei selector projection;
- case-scoped hourly-method alternatives where source/time-standard rules differ.

The fusion R2 target-flow layer exposes Ziwei selector candidates from the same explicit target coordinate used by Bazi flow.

Remaining work is chiefly product-surface closure: ensure all deterministic temporal facts intended for the daily charting workflow are exposed consistently in the workbench and portable desktop application.

Status: **CORE CLOSED; PRESENTATION/PARITY OPEN**.

## H. Fusion application composition — R2 CLOSED

The combined application has these independent, hash-bound layers:

```text
Combined birth chart identity
  + Bazi target-flow application bundle
  + explicit TargetCoordinate resolution
  + Ziwei shared-target selector projection
  -> Combined Target-Flow Fusion R2
```

R2 composition semantics are fixed to:

`INDEPENDENT_BUNDLE_IDENTITY_COMPOSITION_ONLY`

It does not synthesize a new astrological doctrine, infer a cross-system verdict, or rewrite upstream subsystem objects.

The workbench exposes the additive R2 endpoint and the CI smoke exercises the released R1 and R2 surfaces together.

Status: **CLOSED**.

## I. Product field-parity backlog — OPEN

This is the active development class. It should be handled as a field-by-field audit against the actual workbench, Wenmo reference screenshots and Wenzhen reference screenshots.

Each candidate field must be classified as one of:

- `ALREADY_RELEASED_AND_VISIBLE`
- `ALREADY_RELEASED_NOT_YET_VISIBLE`
- `DETERMINISTIC_RUNTIME_MISSING`
- `SOURCE_PROFILE_OR_SCHOOL_CONFLICT`
- `REFERENCE_PRODUCT_ONLY`
- `INTERPRETIVE_OR_PREDICTIVE_OUT_OF_SCOPE`

Priority order:

1. expose already-released deterministic fields that are currently hidden in the application UI;
2. add missing deterministic fields whose source rule is clear and testable;
3. preserve disputed source methods as explicit candidates/profiles;
4. reject product-only labels that cannot be traced to a deterministic rule;
5. keep interpretation/prediction out of the charting release.

R6 Qishu, R7 One-Six Common-Root and R8 adjacent-palace geometry are now product-visible and therefore belong in the Field Parity register as `ALREADY_VISIBLE`; they are no longer open UI gaps.

## J. UI / desktop closure — OPEN

The current workbench and portable Windows launcher are operational, but visual parity and information density are not yet final.

UI work must consume released typed objects and must not duplicate calculation logic in browser JavaScript. In particular:

- browser code must not recompute time/calendar rules;
- browser code must not select candidate zero silently;
- browser code must not rewrite Ziwei selectors while computing Bazi flow;
- browser code must keep system-specific time conventions visible;
- stale-view guards must invalidate derived panels after source/target edits;
- future field panels should be read-only projections of released runtime objects.

Status: **OPEN**.

## Explicit non-goals for this phase

The following remain out of scope until the fusion charting product is complete:

- AI interpretation;
- prediction;
- event verdicts;
- strength/pattern/favorable-element arbitration unless separately released as deterministic profiled research;
- cross-system semantic synthesis;
- training-system work unrelated to deterministic chart correctness or packaging.

## Next implementation sequence

```text
1. Keep the machine-readable field parity register synchronized with released backend/API/Workbench surfaces.
2. Mark every current workbench field as visible / hidden / missing.
3. Close ALREADY_RELEASED_NOT_YET_VISIBLE items first.
4. Implement deterministic missing fields one family at a time only when the source rule is mechanically closed.
5. Preserve disputed methods as explicit profiles/candidates rather than selecting a winner.
6. Add ChartDiff fixtures for disputed/edge cases.
7. Re-run full verify + unit suite + workbench smoke after each atomic slice.
8. Only after field closure, perform the final UI density/layout pass.
```

## Reopen rule

A previously closed deterministic layer is reopened only if evidence shows one of:

- incorrect deterministic chart/time output;
- broken candidate preservation;
- invalid frozen hash/integrity lineage;
- missing field required to reproduce an already-claimed deterministic contract;
- incorrect typed handoff between released layers.

A commercial-product display difference, a traditional interpretive term, or a new school opinion alone is not sufficient.

## Exit statement

The original `cf6a4fa952d242384f0dce6083cb5a13802a1af0` audit baseline closed the mandatory deterministic fusion core through Combined Target-Flow Fusion R2. The active branch has since added source-backed Ziwei Structural Runtime R6-R8 and productized those relations through a read-only application/Workbench sidecar without reopening or rewriting the frozen foundation.

The active development frontier remains **field parity and product closure**, not another rewrite of the time/calendar, Bazi natal/flow, Ziwei natal/structural, or fusion identity foundations.
