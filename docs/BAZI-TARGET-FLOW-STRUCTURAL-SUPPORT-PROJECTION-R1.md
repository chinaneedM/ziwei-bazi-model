# Bazi Target-Flow Structural Support Projection R1

## Scope

This read-only application projection composes the released
`Bazi Structural Support Foundation R1` into every explicit Bazi target-flow
candidate:

```text
Natal + Flow + Structural Context
  -> Structural Support Foundation R1
    -> Target-Flow Structural Support Projection R1
```

It remains a separate downstream object named `structural_support`. It is not
merged into the neutral `structural` projection and does not alter Natal,
Temporal, Flow, or Structural facts.

## Seasonal roles

The projection preserves two typed, non-interchangeable references:

- `NATAL_MONTH_COMMAND` is permanently bound to the Natal `MONTH.BRANCH`,
  Natal FactHash, Natal month Ganzhi, TemporalSeed lineage, time/calendar
  registry lineage, rule identity, and sources.
- `ACTIVE_FLOW_SOLAR_MONTH` is bound to the active Flow `MonthlyFrame`, its
  Structural `MONTHLY` branch occurrence, start/end Jie facts, half-open
  interval, Flow FactHash, rule identity, and sources.

Changing target month can change the active Flow month reference but cannot
rewrite the Natal month-command reference. At an exact Jie instant the active
role binds the new half-open Flow month.

## Candidate-preserving evidence

Every support evidence candidate retains:

- visible-stem and supporting-branch occurrence IDs and layers;
- matching hidden-stem occurrence IDs;
- `EXACT_HIDDEN_STEM_MATCH` or `SAME_ELEMENT_HIDDEN_SUPPORT` identity;
- any seasonal role carried by the supporting branch;
- upstream affinity fact ID and exact-match exposure link IDs;
- rule-set ID/version and stable sources.

The two evidence classes remain separate. Exact matching candidates require
their upstream exposure links; same-element/different-stem candidates carry no
invented exposure. Repeated characters in Natal, Dayun, Annual, and Monthly
layers retain separate occurrence identities.

The projection also publishes independent scoped candidate-ID sets for the
Natal month command and active Flow solar month. These sets are not merged and
are not root or strength verdicts.

## Lineage, hashes, and replay

The application candidate binds Support FactHash and ComputationHash alongside
Natal, Temporal, Flow, and Structural hashes. Its identity, source FactHash,
and bundle ComputationHash therefore change if Support facts or computation
lineage change.

The projection owns another independently recomputable FactHash and
ComputationHash. Local integrity verifies:

- complete Structural/Flow/Temporal/Natal upstream hash bindings;
- Structural and Flow candidate index lineage;
- both seasonal references against the active MonthlyFrame and Structural
  occurrence set;
- candidate IDs, participant layers, scoped role sets, affinity/exposure IDs,
  rule identity, sources, and exact/same-element discrimination;
- the closed non-interpretive field boundary and both projection hashes.

Full application replay independently rebuilds Natal, Temporal, Flow,
Structural Context, Structural Support, and the final view. A modified payload
that is locally rehashed but otherwise structurally valid still fails full
replay.

## Read-only workbench

The target-flow pane renders the two seasonal references separately, then lists
every evidence candidate with occurrence IDs, layers, hidden-stem IDs, scoped
roles, affinity/exposure lineage, rule identity, stable sources, and the
projection hash. It provides no editing, method selection, ranking, or verdict
control.

Machine-readable contract:

- `schemas/bazi-application-flow-integration-r1.schema.json`

## Non-goals

R1 does not calculate or display `ROOT/NO_ROOT`, primary/secondary root,
strength, weights, scores, 得令/得地/得势, 旺衰, 格局, 用神/忌神, 调候, 病药,
transformation success, judgments, training data, interpretations, or
predictions. Xiaoyun, Daily, and Hourly remain outside the released Structural
Context and Support coverage.
