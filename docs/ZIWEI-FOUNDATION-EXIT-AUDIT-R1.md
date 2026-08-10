# Ziwei Foundation Exit Audit R1

## Decision

```text
AUDIT_ID=ZIWEI-FOUNDATION-EXIT-AUDIT-R1
STATUS=PASS
MANDATORY_FOUNDATION_SLICES=COMPLETE
NEXT_PHASE=ZIWEI-APPLICATION-V1
ISSUE=#204
BASELINE_MAIN=11c4403e8eada9108ba58be7a5cb5c36265f28e2
```

This audit closes the open-ended Ziwei Foundation phase. Future work must not reopen Foundation merely because another traditional semantic relation, historical term, interpretation rule, or UI feature is discovered. A Foundation reopen requires evidence that a missing item changes deterministic chart output, a frozen state contract, or the ability to produce a machine-consumable chart/application handoff.

## Gate A — deterministic natal chart: PASS

The frozen Ziwei Chart Engine V1 provides a typed public computation path from birth input through Time / Calendar resolution to validated `ZiweiChartCandidate` / `NatalChartState` output.

The natal contract already includes:

- twelve-palace structure and palace Ganzhi;
- deterministic physical placements;
- operational auxiliary/minor-star scope;
- Dignity annotations;
- natal transformations;
- role bindings and ring runtimes;
- independent integrity diagnostics;
- deterministic FactHash / ComputationHash;
- machine-readable state schema.

The Foundation does not require a new natal engine.

## Gate B — temporal overlay: PASS

`TemporalNatalContext` and `ZiweiTemporalEngine.generate()` provide a typed public runtime for:

- Daxian frames;
- Annual frames;
- Minor Limit frames;
- temporal designation overlays;
- temporal transformation activations.

Temporal state remains separate from natal physical placements. Dynamic frames do not relocate or rewrite natal physical entities.

## Gate C — structural closure: PASS

The active Structural Runtime chain is:

```text
R1 Neutral Z12 Topology
-> R2 Relative Palace Frame
-> R3 Borrow Projection
-> R4 Named Opposition / Trine / Sanfang-Sizheng Semantics
-> R5 Borrow-Resolved Sanfang/Sizheng Composition View
```

R3 preserves physical-resolution identity through `structure_physical_key`.
R4 preserves canonical semantic identity through `axis_key` and `group_key`.
R5 composes both without creating a second physical inventory or a second independent semantic cause.

Each structural layer remains independently versioned, hashed, integrity-validated and machine-serializable.

## Gate D — serialization and presentation boundary: PASS

The existing renderer-neutral `ChartViewModel` provides a presentation boundary for natal/temporal chart display and already supports a plain-text renderer. The View compiler does not write back into canonical or temporal state.

Structural state is intentionally not flattened into V1 `ChartViewModel`. R1-R5 are separate machine-consumable state objects with their own schemas and hashes. The next application service may expose them as optional overlays without mutating V1 presentation or canonical contracts.

Therefore the absence of a single all-in-one orchestration function is an Application Architecture gap, not a Foundation-computation gap.

## Gate E — integrity/source governance: PASS

The active release chain preserves independent upstream bindings and fail-closed validation:

- V1 natal integrity/hash lineage;
- temporal integrity/hash lineage;
- R1/R2 coordinate lineage;
- R3 borrow lineage and physical dedup identity;
- R4 named-semantic source lineage and canonical semantic identity;
- R5 R3/R4 cross-lineage composition and upstream hash replay.

R5 release regression specifically rejects stale `PASS` reports / stale hashes hiding tampered R3 or R4 content.

No Foundation Exit change modifies `sources/canonical/`, training state, model-learning, or prediction controls.

## Foundation backlog classification

The following items are explicitly **non-blocking** for Foundation Exit unless future evidence proves that they alter deterministic chart output or a frozen runtime contract:

- 气数位 directed semantic relation;
- 一六共宗 semantic relation;
- 夹宫 runtime;
- left/right 合宫 naming;
- pair-geometry strength;
- motif/configuration compiler;
- dynamic borrow beyond NATAL;
- prediction/reasoning runtime;
- graphical UI implementation.

### Qishu decision

气数位 is not required to compute, serialize, render, or structurally resolve the current Ziwei chart.

Its current source identity is a theme-relative directed semantic role corresponding to relative ordinal 9 / physical offset `+4`. It is not equivalent to generic trine identity and should remain a separately versioned semantic layer when implemented.

It is therefore scheduled **after the first usable Application V1 vertical slice**, unless a concrete application requirement demonstrates that the first software release cannot function without it.

## Application handoff boundary

The next phase is no longer Foundation research. It is product/application integration.

Target architecture:

```text
ApplicationBirthRequest
        ↓
ZiweiChartService
        ↓
ApplicationChartBundle
        ├── V1 natal candidate / hashes
        ├── Temporal context/state
        ├── R1 topology
        ├── R2 relative frame
        ├── R3 borrow projection
        ├── R4 named semantics
        ├── R5 resolved structural view
        └── ChartViewModel / deterministic exports
```

The bundle should reference existing state objects rather than duplicate their physical or semantic facts.

## Ziwei Application V1 initial scope

Application V1 should focus on an actually usable chart product, not prediction:

1. birth datetime / place / timezone / sex input;
2. one-call Ziwei computation orchestration;
3. full natal chart output;
4. Daxian / Annual / Minor Limit selection;
5. optional R5 structural overlay access;
6. plain-text output immediately;
7. renderer-neutral JSON for a twelve-palace graphical UI;
8. deterministic export / fixture / ChartDiff regression;
9. packaging suitable for the user's daily charting workflow.

Prediction/reasoning remains post-application and must not block this phase.

## Exit rule

After this audit is merged to `main`, the default scheduling rule is:

```text
new discovery
    ↓
does it change deterministic chart output,
frozen state shape, or application handoff correctness?
    ├── YES -> evaluate as Foundation/runtime defect
    └── NO  -> Application / semantic / interpretation backlog
```

The Ziwei Foundation phase is therefore closed as of this audit baseline.
