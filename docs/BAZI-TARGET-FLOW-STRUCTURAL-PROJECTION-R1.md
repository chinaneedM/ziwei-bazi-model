# Bazi Target-Flow Structural Projection R1

## Scope

This projection exposes the released `Bazi Structural Context R1` inside each
explicit Bazi target-flow candidate. It is a read-only composition layer, not a
second relation calculator:

```text
Natal + active Dayun/Annual/Monthly Flow
  -> Bazi Structural Context R1
    -> Bazi Target-Flow Structural Projection R1
```

The projection covers only the layers supported by the released Structural
Context: `DAYUN`, `ANNUAL`, and `MONTHLY`. `XIAOYUN`, `DAILY`, and `HOURLY`
are recorded in `excluded_layers`; this version does not silently extend the
relation table to those layers. A `PRE_DAYUN` interval creates no Dayun
participant.

## Preserved facts and lineage

Every projected temporal participant retains its occurrence `instance_id`,
source layer, source Ganzhi, parent `source_frame_id`, and upstream Flow
FactHash. Equal characters in different frames therefore remain different
participants.

Every neutral relation occurrence retains:

- occurrence and semantic relation IDs;
- relation family, arity, orientation, and neutral scope;
- participant instance IDs and participant layers;
- rule-set ID and version;
- stable source references;
- nominal transformation element when present.

`nominal_transformation_element` is registry metadata only. It does not mean
that a combination transformed successfully. No effect, priority, strength,
winner, cancellation, prediction, or interpretation field is permitted.

## Candidate preservation

Structural Context may aggregate only byte-identical structural facts with the
same computation lineage. The projection retains every contributing source
Flow candidate index. Each application-flow candidate must point to exactly one
such Structural candidate containing its own Flow index; missing, duplicate, or
out-of-range lineage fails closed.

## Hashes and replay

The application candidate directly binds the source Structural FactHash and
ComputationHash. Both are included in candidate identity; the fact hash enters
the application source hash and the computation hash enters the bundle hash.

The projection additionally owns an independently recomputable FactHash and
ComputationHash. Structural validation checks its schema/profile/algorithm,
coverage boundary, parent-frame provenance, participant-layer replay, relation
arity/scope, rule identity, sources, forbidden interpretive fields, and both
projection hashes. Full application replay then reconstructs the Structural
Context from Natal and Flow inputs and compares the exact final output. A
locally modified and rehashed projection therefore still fails full replay.

## Read-only workbench

The target-flow pane lists each neutral relation with layers, scope,
participants, relation ID, rule identity, and sources. A nominal transformation
element is labeled as a non-transformation conclusion. The pane also displays
the Structural and projection hashes; it does not offer editing or rule
selection controls.

Machine-readable contract:

- `schemas/bazi-application-flow-integration-r1.schema.json`

## Non-goals

R1 does not calculate relation effects, transformation success, strength,
seasonal weighting, pattern, useful/favorable elements, ShenSha meanings,
judgments, training data, or predictions. It does not extend Structural Context
to Xiaoyun, Daily, or Hourly without a separately sourced and versioned runtime
contract.
